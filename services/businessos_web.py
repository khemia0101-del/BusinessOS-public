#!/usr/bin/env python3
"""Small optional gateway for authenticated inbound business messages.

The owner-facing dashboard lives in dashboard/. This service only provides a
generic health/status endpoint and routes an approved inbound message to the
matching employee task queue. Provider-specific adapters should normalize their
payload before calling this gateway.
"""

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import hmac
import html
import json
import os
import re
import subprocess


CORE_ROOT = Path(os.environ.get("BUSINESSOS_ROOT", "/opt/businessos/core"))
STATE_ROOT = Path(os.environ.get("BUSINESSOS_STATE_ROOT", "/var/lib/businessos"))
COMMUNICATIONS = STATE_ROOT / "communications"
INBOUND_LOG = COMMUNICATIONS / "inbound-message.jsonl"
REJECT_LOG = COMMUNICATIONS / "inbound-message-rejected.jsonl"
UNASSIGNED_LOG = COMMUNICATIONS / "inbound-message-unassigned.jsonl"
ROUTED_LOG = COMMUNICATIONS / "inbound-message-routed.jsonl"
EMPLOYEES = Path(os.environ.get("BUSINESSOS_EMPLOYEES_FILE", str(CORE_ROOT / "employees.json")))
HERMES = os.environ.get("HERMES_BIN", "hermes")
HERMES_RUN_AS = os.environ.get("HERMES_RUN_AS", "").strip()
WEBHOOK_SECRET = os.environ.get("INBOUND_WEBHOOK_SECRET", "").strip()
WEBHOOK_PATH = os.environ.get("INBOUND_WEBHOOK_PATH", "/webhooks/inbound-message")
INSTANCE_ID = os.environ.get("BUSINESSOS_INSTANCE_ID", "unconfigured")
BUSINESS_STAGE = os.environ.get("BUSINESS_STAGE", "pre_acquisition")
MAX_BODY_BYTES = int(os.environ.get("INBOUND_WEBHOOK_MAX_BYTES", "1048576"))


for log_path in (INBOUND_LOG, REJECT_LOG, UNASSIGNED_LOG, ROUTED_LOG):
    log_path.parent.mkdir(parents=True, exist_ok=True)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path, value):
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def load_json(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def normalize_phone(value):
    if not value:
        return ""
    raw = str(value).strip()
    digits = re.sub(r"\D+", "", raw)
    if not digits:
        return ""
    if raw.startswith("+"):
        return "+" + digits
    if len(digits) == 10:
        return "+1" + digits
    return "+" + digits


def find_value(value, keys):
    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).lower() in keys and nested not in (None, ""):
                return nested
        for nested in value.values():
            found = find_value(nested, keys)
            if found not in (None, ""):
                return found
    if isinstance(value, list):
        for nested in value:
            found = find_value(nested, keys)
            if found not in (None, ""):
                return found
    return None


def employee_index():
    data = load_json(EMPLOYEES, {"employees": []})
    by_phone = {}
    by_email = {}
    for employee in data.get("employees", []):
        phone = normalize_phone((employee.get("phone") or {}).get("e164"))
        email = str(employee.get("email") or "").strip().lower()
        if phone:
            by_phone[phone] = employee
        if email:
            by_email[email] = employee
    return data, by_phone, by_email


def run_hermes(arguments, timeout=25):
    command = [HERMES] + arguments
    if HERMES_RUN_AS:
        command = ["runuser", "-u", HERMES_RUN_AS, "--"] + command
    return subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)


def create_task(employee, sender, body, provider, payload):
    agent_id = employee.get("agent_id") or employee.get("employee_id") or "business-orchestrator"
    employee_id = employee.get("employee_id") or "unknown"
    name = employee.get("name") or sender or "unknown sender"
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]
    title = f"Inbound {provider} message from {name}"
    task_body = (
        f"Employee: {name}\nEmployee id: {employee_id}\nSender: {sender}\n"
        f"Provider: {provider}\nAgent id: {agent_id}\nReceived: {utc_now()}\n\n"
        f"Message:\n{body}\n\nSource log: {INBOUND_LOG}\n"
    )
    result = run_hermes(
        [
            "kanban", "--board", "businessos-employees", "create", title,
            "--assignee", agent_id, "--body", task_body,
            "--idempotency-key", f"inbound-{digest}", "--created-by", "businessos-gateway",
        ]
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout[-1000:],
        "stderr": result.stderr[-1000:],
        "agent_id": agent_id,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "BusinessOSGateway/1.0"

    def send_json(self, status, value):
        encoded = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def send_html(self, status, value):
        encoded = value.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def authorized(self):
        if not WEBHOOK_SECRET:
            return False
        supplied = (self.headers.get("x-businessos-webhook-secret") or "").strip()
        authorization = (self.headers.get("authorization") or "").strip()
        if authorization.lower().startswith("bearer "):
            supplied = authorization[7:].strip()
        return bool(supplied) and hmac.compare_digest(supplied, WEBHOOK_SECRET)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/health", "/api/businessos/status"):
            return self.send_json(
                200,
                {
                    "ok": True,
                    "service": "businessos-gateway",
                    "instance": INSTANCE_ID,
                    "stage": BUSINESS_STAGE,
                    "webhook_configured": bool(WEBHOOK_SECRET),
                    "time": utc_now(),
                },
            )
        if path == "/":
            return self.send_html(
                200,
                "<!doctype html><html><head><meta charset='utf-8'><title>BusinessOS gateway</title>"
                "<style>body{font:15px system-ui;margin:48px;color:#15171a}main{max-width:680px}"
                "code{background:#f1f3f5;padding:2px 5px;border-radius:4px}</style></head><body><main>"
                f"<h1>BusinessOS gateway</h1><p>Instance: <code>{html.escape(INSTANCE_ID)}</code></p>"
                "<p>This service routes authenticated inbound events. Open the configured dashboard for the owner workspace.</p>"
                "</main></body></html>",
            )
        return self.send_json(404, {"ok": False, "error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != WEBHOOK_PATH:
            return self.send_json(404, {"ok": False, "error": "not_found"})

        length = int(self.headers.get("content-length") or 0)
        if length < 1 or length > MAX_BODY_BYTES:
            return self.send_json(413, {"ok": False, "error": "invalid_body_size"})

        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return self.send_json(400, {"ok": False, "error": "invalid_json"})

        provider = (self.headers.get("x-businessos-provider") or "unknown").strip()[:80]
        sender_phone = normalize_phone(
            find_value(payload, {"from", "sender", "phone", "from_number", "from_phone"})
        )
        sender_email = str(
            find_value(payload, {"email", "from_email", "sender_email"}) or ""
        ).strip().lower()
        body = str(find_value(payload, {"message", "body", "text", "content"}) or "")
        entry = {
            "received_at": utc_now(),
            "provider": provider,
            "sender_phone": sender_phone,
            "sender_email": sender_email,
            "body": body,
            "payload": payload,
        }

        if not self.authorized():
            append_jsonl(REJECT_LOG, {**entry, "payload": "<redacted>", "reason": "unauthorized"})
            return self.send_json(401, {"ok": False, "error": "unauthorized"})

        append_jsonl(INBOUND_LOG, entry)
        data, by_phone, by_email = employee_index()
        employee = by_phone.get(sender_phone) or by_email.get(sender_email)
        if not employee:
            append_jsonl(UNASSIGNED_LOG, entry)
            return self.send_json(
                202,
                {"ok": True, "route_status": "unassigned", "employees_known": len(data.get("employees", []))},
            )

        result = create_task(employee, sender_phone or sender_email, body, provider, payload)
        append_jsonl(ROUTED_LOG, {**entry, "route_result": result})
        return self.send_json(200, {"ok": True, "route_status": "routed", "agent_id": result["agent_id"]})

    def log_message(self, format_string, *arguments):
        print(f"{self.address_string()} - {format_string % arguments}")


def main():
    host = os.environ.get("BUSINESSOS_GATEWAY_HOST", "127.0.0.1")
    port = int(os.environ.get("BUSINESSOS_GATEWAY_PORT", "8787"))
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()

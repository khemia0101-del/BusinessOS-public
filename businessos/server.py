"""Private HTTP API. Bind to loopback behind an authenticated TLS reverse proxy."""

import base64
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

from businessos.finance import ValidationError, project_cash, working_capital
from businessos.construction import calculate_wip
from businessos.runtime import MAX_FILE_BYTES, Runtime, encode


def make_handler(runtime, tokens, stage="pre_acquisition"):
    if not tokens or any(len(t) < 24 for t in tokens.values()) or len(set(tokens.values())) != len(tokens):
        raise ValidationError("Distinct owner, reviewer, and browser-worker tokens of at least 24 characters are required")

    class Handler(BaseHTTPRequestHandler):
        server_version = "BusinessOS"

        def setup(self):
            super().setup()
            self.connection.settimeout(20)

        def log_message(self, *args):
            pass  # URLs, messages and credentials are not application logs.

        def send(self, code, value, content_type="application/json", filename=None):
            body = value if isinstance(value, bytes) else encode(value).encode()
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if filename:
                self.send_header("Content-Disposition", "attachment; filename=\"" + filename.replace('"', '').replace("\r", "").replace("\n", "") + "\"")
            self.end_headers()
            self.wfile.write(body)

        def role(self):
            provided = self.headers.get("Authorization", "")
            for role, token in tokens.items():
                if hmac.compare_digest(provided.encode(), ("Bearer " + token).encode()):
                    return role
            return None

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/healthz":
                return self.send(200, {"ok": True, "service": "businessos-runtime", "stage": stage, "business_id": runtime.business_id})
            role = self.role()
            if role is None:
                return self.send(401, {"error": "Authentication required"})
            try:
                if path == "/notebook/jobs" and role == "worker":
                    return self.send(200, runtime.list("notebook_job"))
                if role not in ("owner", "reviewer"):
                    return self.send(403, {"error": "Role cannot access this resource"})
                if path == "/snapshot":
                    return self.send(200, {**runtime.snapshot(), "stage": stage, "role": role})
                if path.startswith("/sources/"):
                    identifier = unquote(path.split("/")[2])
                    if path.endswith("/download"):
                        source, data = runtime.source_bytes(identifier)
                        return self.send(200, data, "application/octet-stream", source["filename"])
                    return self.send(200, runtime.get("source", identifier))
                if path.startswith("/reports/") and path.endswith("/memo"):
                    return self.send(200, runtime.memo(unquote(path.split("/")[2])).encode(), "text/markdown; charset=utf-8", "underwriting.md")
                return self.send(404, {"error": "Not found"})
            except ValidationError as error:
                return self.send(400, {"error": str(error)})
            except Exception:
                return self.send(500, {"error": "Read failed; inspect private runtime integrity"})

        def do_POST(self):
            role = self.role()
            if role is None:
                return self.send(401, {"error": "Authentication required"})
            path = urlparse(self.path).path
            try:
                if self.headers.get("Transfer-Encoding") or not self.headers.get("Content-Type", "").startswith("application/json"):
                    raise ValidationError("Use JSON with Content-Length")
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_FILE_BYTES * 2:
                    return self.send(413, {"error": "Request size exceeded"})
                data = json.loads(self.rfile.read(length), parse_constant=lambda _: (_ for _ in ()).throw(ValidationError("Nonfinite JSON numbers")))
                if not isinstance(data, dict):
                    raise ValidationError("JSON object required")
                if path.startswith("/notebook/jobs/") and path.endswith("/claim"):
                    if role != "worker":
                        return self.send(403, {"error": "Browser worker identity required"})
                    result = runtime.claim_notebook_job(path.split("/")[3], role)
                elif path.startswith("/notebook/jobs/") and path.endswith("/result"):
                    if role != "worker":
                        return self.send(403, {"error": "Browser worker identity required"})
                    result = runtime.notebook_result(path.split("/")[3], data, role)
                elif path.startswith("/reports/") and path.endswith("/review"):
                    if role != "reviewer":
                        return self.send(403, {"error": "Independent reviewer identity required"})
                    result = runtime.review_report(path.split("/")[2], data["decision"], data.get("exceptions", []), data["rationale"], role)
                elif path.startswith("/initiatives/") and path.endswith("/action"):
                    if role not in ("owner", "reviewer") or (data.get("action") in ("pilot", "active") and role != "reviewer"):
                        return self.send(403, {"error": "Independent reviewer required for promotion"})
                    result = runtime.initiative_action(path.split("/")[2], data, role, stage)
                else:
                    if role != "owner":
                        return self.send(403, {"error": "Owner identity required"})
                    if path == "/company":
                        result = runtime.configure(data, role)
                    elif path == "/sources":
                        result = runtime.ingest(base64.b64decode(data["content_base64"], validate=True), data["filename"], data["document_id"], data["origin"], role)
                        result = {k: v for k, v in result.items() if k != "segments"}
                    elif path == "/reports":
                        result = runtime.create_report(data, role)
                    elif path == "/initiatives":
                        result = runtime.save_initiative(data, role)
                    elif path == "/projections":
                        result = runtime.save_projection(data, role)
                    elif path == "/working-capital":
                        result = working_capital(data["components"])
                    elif path == "/wip":
                        runtime.source_refs(data.get("source_ids"))
                        result = calculate_wip(data)
                    elif path == "/notebook/jobs":
                        result = runtime.notebook_job(data, role)
                    else:
                        return self.send(404, {"error": "Not found"})
                return self.send(200, result)
            except (ValueError, KeyError, TypeError, UnicodeError) as error:
                return self.send(400, {"error": str(error) if isinstance(error, ValidationError) else "Invalid request fields or file content"})
            except Exception:
                return self.send(500, {"error": "Operation failed; no success confirmed"})

    return Handler


def serve(root, business_id, port):
    runtime = Runtime(root, business_id)
    tokens = {role: os.environ.get("BUSINESSOS_" + role.upper() + "_TOKEN", "") for role in ("owner", "reviewer", "worker")}
    stage = os.environ.get("BUSINESS_STAGE", "pre_acquisition")
    if stage not in ("pre_acquisition", "transition", "operating"):
        stage = "pre_acquisition"
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(runtime, tokens, stage))
    print(f"BusinessOS runtime listening on loopback port {port}; company {business_id}", flush=True)
    server.serve_forever()

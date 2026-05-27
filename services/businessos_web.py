#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import hmac
import html
import json
import os
import re
import subprocess

ROOT = Path('/opt/businessOS')
LOG = ROOT / 'memory-system/communications/sendblue-webhook.jsonl'
REJECT_LOG = ROOT / 'memory-system/communications/sendblue-webhook-rejected.jsonl'
UNASSIGNED_LOG = ROOT / 'memory-system/communications/sendblue-unassigned.jsonl'
ROUTE_LOG = ROOT / 'memory-system/communications/sendblue-routed.jsonl'
EMPLOYEES = ROOT / 'employees.json'
PUBLIC_PATH = '/oFpYcvDjUZ2TmaawGFCxUhJqTMYXRY8g'
PUBLIC_URL = 'http://4.151.184.237' + PUBLIC_PATH
SECRET = os.environ.get('SENDBLUE_SECRET_KEY', '').strip().strip('"').strip("'")
HERMES = '/home/azureuser/.local/bin/hermes'

for p in [LOG, REJECT_LOG, UNASSIGNED_LOG, ROUTE_LOG]:
    p.parent.mkdir(parents=True, exist_ok=True)

def append_jsonl(path, obj):
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')

def load_json(path, fallback):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return fallback

def normalize_phone(value):
    if not value:
        return ''
    s = str(value).strip()
    digits = re.sub(r'\D+', '', s)
    if not digits:
        return ''
    if s.startswith('+'):
        return '+' + digits
    if len(digits) == 10:
        return '+1' + digits
    if len(digits) == 11 and digits.startswith('1'):
        return '+' + digits
    return '+' + digits

def find_value(obj, keys):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in keys and v:
                return v
        for v in obj.values():
            found = find_value(v, keys)
            if found:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_value(v, keys)
            if found:
                return found
    return None

def extract_sender(payload):
    keys = {'from','sender','phone','number','from_number','fromnumber','from_phone','fromphone','contact_phone','contactphone','source_number'}
    return normalize_phone(find_value(payload, keys))

def extract_body(payload):
    keys = {'message','body','text','content','message_body','messagebody'}
    v = find_value(payload, keys)
    return '' if v is None else str(v)

def employee_index():
    data = load_json(EMPLOYEES, {'employees': []})
    by_phone = {}
    for emp in data.get('employees', []):
        phone = normalize_phone((emp.get('phone') or {}).get('e164'))
        if phone:
            by_phone[phone] = emp
    return data, by_phone

def run_azureuser(args, timeout=25):
    cmd = ['runuser', '-u', 'azureuser', '--'] + args
    return subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)

def create_kanban_task(emp, sender, body, payload):
    agent_id = emp.get('agent_id') or emp.get('employee_id') or 'business-orchestrator'
    employee_id = emp.get('employee_id') or 'unknown'
    name = emp.get('name') or sender
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]
    title = f'Inbound Sendblue message from {name}'
    task_body = f'''Employee: {name}\nEmployee id: {employee_id}\nSender: {sender}\nAgent id: {agent_id}\nReceived: {datetime.now(timezone.utc).isoformat()}\n\nMessage:\n{body}\n\nSource log: {LOG}\n'''
    args = [HERMES, 'kanban', '--board', 'businessos-employees', 'create', title, '--assignee', agent_id, '--body', task_body, '--idempotency-key', f'sendblue-{digest}', '--created-by', 'sendblue-webhook']
    proc = run_azureuser(args)
    return {'returncode': proc.returncode, 'stdout': proc.stdout[-2000:], 'stderr': proc.stderr[-2000:], 'agent_id': agent_id}

def command_text(args, timeout=12):
    try:
        proc = run_azureuser(args, timeout=timeout)
        return (proc.stdout or proc.stderr or '').strip()
    except Exception as exc:
        return f'error: {exc}'

def last_lines(path, n=5):
    if not path.exists():
        return []
    try:
        return path.read_text(encoding='utf-8', errors='ignore').splitlines()[-n:]
    except Exception:
        return []

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, code=200, obj=None):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(json.dumps(obj or {'ok': True}, ensure_ascii=False).encode('utf-8'))

    def _send_html(self, code=200, text=''):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))

    def _authorized(self):
        if not SECRET:
            return True
        got = (self.headers.get('sb-signing-secret') or '').strip()
        return bool(got) and hmac.compare_digest(got, SECRET)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ('/health', '/webhooks/sendblue/health'):
            return self._send_json(200, {'ok': True, 'service': 'businessos-web', 'public_url': PUBLIC_URL})
        if path == '/api/businessos/status':
            return self._send_json(200, self.status_payload())
        if path == PUBLIC_PATH:
            return self._send_html(200, self.status_html())
        return self._send_json(404, {'ok': False, 'error': 'not_found'})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != '/webhooks/sendblue':
            return self._send_json(404, {'ok': False, 'error': 'not_found'})
        length = int(self.headers.get('content-length') or 0)
        raw = self.rfile.read(length) if length else b''
        text = raw.decode('utf-8', errors='replace')
        try:
            payload = json.loads(text) if text else {}
        except Exception as exc:
            payload = {'_raw': text, '_json_error': str(exc)}
        entry = {
            'received_at': datetime.now(timezone.utc).isoformat(),
            'path': self.path,
            'headers': {k: ('<redacted>' if k.lower() in {'sb-signing-secret','authorization'} else v) for k, v in self.headers.items()},
            'sender': extract_sender(payload),
            'body': extract_body(payload),
            'json': payload,
        }
        if not self._authorized():
            entry['rejected_reason'] = 'missing_or_invalid_sb_signing_secret'
            append_jsonl(REJECT_LOG, entry)
            return self._send_json(401, {'ok': False, 'error': 'unauthorized'})
        append_jsonl(LOG, entry)
        data, by_phone = employee_index()
        emp = by_phone.get(entry['sender'])
        if not emp:
            entry['route_status'] = 'unassigned_no_employee_phone_match'
            append_jsonl(UNASSIGNED_LOG, entry)
            return self._send_json(200, {'ok': True, 'route_status': 'unassigned', 'sender': entry['sender'], 'employees_known': len(data.get('employees', []))})
        result = create_kanban_task(emp, entry['sender'], entry['body'], payload)
        entry['route_status'] = 'routed_to_kanban'
        entry['route_result'] = result
        append_jsonl(ROUTE_LOG, entry)
        return self._send_json(200, {'ok': True, 'route_status': 'routed', 'agent_id': result['agent_id'], 'kanban_returncode': result['returncode']})

    def status_payload(self):
        employees, _ = employee_index()
        return {
            'ok': True,
            'public_url': PUBLIC_URL,
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'profiles': command_text([HERMES, 'profile', 'list']),
            'boards': command_text([HERMES, 'kanban', 'boards', 'list']),
            'employees_count': len(employees.get('employees', [])),
            'services': {
                'hermes_gateway': command_text(['systemctl', 'is-active', 'hermes-gateway.service']),
                'businessos_web': command_text(['systemctl', 'is-active', 'businessos-web.service']),
            },
            'recent_sendblue': last_lines(LOG, 3),
            'recent_unassigned': last_lines(UNASSIGNED_LOG, 3),
            'recent_routed': last_lines(ROUTE_LOG, 3),
        }

    def status_html(self):
        payload = self.status_payload()
        profiles = html.escape(payload['profiles'])
        boards = html.escape(payload['boards'])
        recent_unassigned = html.escape('\n'.join(payload['recent_unassigned']) or 'No unassigned Sendblue messages yet.')
        recent_routed = html.escape('\n'.join(payload['recent_routed']) or 'No routed Sendblue messages yet.')
        return f'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BusinessOS Live</title>
<style>
body{{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:#0b1020;color:#e8edf8}}main{{max-width:1180px;margin:0 auto;padding:32px}}.top{{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}}h1{{font-size:34px;margin:0 0 8px}}p{{color:#aeb9cf}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:20px}}.card{{border:1px solid #25304a;background:#121a2e;border-radius:8px;padding:18px}}.ok{{color:#51d88a}}.warn{{color:#ffd166}}pre{{white-space:pre-wrap;word-break:break-word;background:#08101f;border:1px solid #26314f;border-radius:6px;padding:12px;color:#d7e2f7;max-height:360px;overflow:auto}}.pill{{display:inline-block;padding:4px 8px;border:1px solid #33476d;border-radius:999px;margin:3px;color:#c8d5ee}}a{{color:#82b7ff}}</style>
</head><body><main>
<div class="top"><div><h1>BusinessOS Live Architecture</h1><p>Hermes Business Pod status, profiles, boards, and employee-message routing.</p></div><div><span class="pill">Updated {html.escape(payload['updated_at'])}</span></div></div>
<div class="grid">
<section class="card"><h2>Services</h2><p>Hermes Gateway: <b class="ok">{html.escape(payload['services']['hermes_gateway'])}</b></p><p>BusinessOS Web/Sendblue Router: <b class="ok">{html.escape(payload['services']['businessos_web'])}</b></p><p>Sendblue webhook: <code>http://4.151.184.237/webhooks/sendblue</code></p><p>Health: <a href="/health">/health</a></p></section>
<section class="card"><h2>Agent Architecture</h2><p><span class="pill">Orchestrator gpt-5.5</span><span class="pill">Researcher gpt-5.4</span><span class="pill">CGO gpt-5.4</span><span class="pill">Compliance gpt-5.4</span><span class="pill">Evaluator gpt-5.4</span><span class="pill">QA / Small Agents gpt-5.4-mini</span></p><p>Employee agents are created from <code>/opt/businessOS/employees.json</code>. Current employees: <b>{payload['employees_count']}</b></p></section>
<section class="card"><h2>Current Profiles</h2><pre>{profiles}</pre></section>
<section class="card"><h2>Kanban Boards</h2><pre>{boards}</pre></section>
<section class="card"><h2>Recent Routed Sendblue</h2><pre>{recent_routed}</pre></section>
<section class="card"><h2>Recent Unassigned Sendblue</h2><pre>{recent_unassigned}</pre></section>
</div></main></body></html>'''

    def log_message(self, fmt, *args):
        print(f'{self.address_string()} - {fmt % args}', flush=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '80'))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

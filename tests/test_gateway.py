"""Local HTTP regression tests; never invoke Hermes or contact a business system."""

from copy import deepcopy
from http.client import HTTPResponse
from pathlib import Path
import json
import os
import runpy
import socket
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

from services import businessos_web as gateway


def employee():
    return {
        "employee_id": "employee-test", "agent_id": "agent-test", "name": "Test Employee",
        "status": "active", "email": "employee@example.test", "phone": {"e164": "+15550000001"},
        "consent": {
            "employee_agent_enabled": True, "approved_channel": "email",
            "approved_scope": "Collect workflow feedback only", "approved_by": "owner",
            "approved_at": "2026-08-28T10:00:00Z",
        },
    }


class GatewayTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        configuration = {
            "WEBHOOK_SECRET": "test-secret", "INSTANCE_ID": "test-instance",
            "INBOUND_LOG": self.directory / "inbound.jsonl",
            "REJECT_LOG": self.directory / "rejected.jsonl",
            "UNASSIGNED_LOG": self.directory / "unassigned.jsonl",
            "ROUTED_LOG": self.directory / "routed.jsonl",
        }
        for key, value in configuration.items():
            patcher = patch.object(gateway, key, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.roster = {"employees": [employee()]}
        loader = patch.object(gateway, "load_json", side_effect=lambda *_: self.roster)
        loader.start()
        self.addCleanup(loader.stop)
        runner = patch.object(gateway, "run_hermes", return_value=subprocess.CompletedProcess([], 0, "private stdout", "private stderr"))
        self.hermes = runner.start()
        self.addCleanup(runner.stop)
        self.server = gateway.ThreadingHTTPServer(("127.0.0.1", 0), gateway.Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def message(self, **changes):
        return {"event_id": "event-private-id", "sender_email": "employee@example.test", "body": "private message text", **changes}

    def post(self, payload=None, headers=None, raw=None):
        request_headers = {"x-businessos-webhook-secret": "test-secret", "x-businessos-provider": "email"}
        request_headers.update(headers or {})
        body = raw if raw is not None else json.dumps(self.message() if payload is None else payload)
        encoded = body.encode("utf-8")
        request_headers.setdefault("Content-Length", str(len(encoded)))
        request_headers["Host"] = "127.0.0.1"
        request = f"POST {gateway.WEBHOOK_PATH} HTTP/1.0\r\n"
        request += "".join(f"{name}: {value}\r\n" for name, value in request_headers.items())
        # Send one request buffer so early rejection cannot race a second body send on Windows.
        with socket.create_connection(self.server.server_address, timeout=3) as connection:
            connection.sendall(request.encode("iso-8859-1") + b"\r\n" + encoded)
            response = HTTPResponse(connection)
            response.begin()
            return response.status, json.loads(response.read())

    def logs(self):
        return "\n".join(path.read_text(encoding="utf-8") for path in self.directory.glob("*.jsonl"))

    def test_success_routes_approved_scope_without_sensitive_logs(self):
        status, response = self.post()
        self.assertEqual((status, response["route_status"]), (200, "routed"))
        command = self.hermes.call_args.args[0]
        task_body = command[command.index("--body") + 1]
        self.assertIn("Collect workflow feedback only", task_body)
        self.assertIn("untrusted business evidence", task_body)
        for value in ("private message text", "employee@example.test", "event-private-id", "private stdout", "private stderr", "test-secret"):
            self.assertNotIn(value, self.logs())

    def test_unauthorized_rejected_before_body_parsing(self):
        status, _ = self.post(raw="private malformed text", headers={"x-businessos-webhook-secret": "wrong"})
        self.assertEqual(status, 401)
        self.hermes.assert_not_called()
        self.assertNotIn("private", self.logs())

    def test_non_ascii_secret_header_fails_closed(self):
        self.assertEqual(self.post(headers={"x-businessos-webhook-secret": "é"})[0], 401)

    def test_no_configured_secret_fails_closed(self):
        with patch.object(gateway, "WEBHOOK_SECRET", ""):
            self.assertEqual(self.post()[0], 401)

    def test_bearer_authentication(self):
        self.assertEqual(self.post(headers={"authorization": "Bearer test-secret", "x-businessos-webhook-secret": ""})[0], 200)

    def test_cli_nonzero_is_retryable_failure(self):
        self.hermes.return_value = subprocess.CompletedProcess([], 2, "private stdout", "private stderr")
        status, response = self.post()
        self.assertEqual(status, 503)
        self.assertTrue(response["retryable"])
        self.assertNotIn("routed", response.values())
        self.assertNotIn("private", self.logs())

    def test_cli_exceptions_are_retryable(self):
        for error in (FileNotFoundError("private details"), subprocess.TimeoutExpired("hermes", 25)):
            with self.subTest(error=type(error).__name__):
                self.hermes.side_effect = error
                status, response = self.post()
                self.assertEqual(status, 503)
                self.assertTrue(response["retryable"])
        self.assertNotIn("private", self.logs())

    def test_retries_keep_stable_event_idempotency_key(self):
        self.post()
        first = self.hermes.call_args.args[0]
        self.post(self.message(body="same provider event retried"))
        second = self.hermes.call_args.args[0]
        self.assertEqual(first[first.index("--idempotency-key") + 1], second[second.index("--idempotency-key") + 1])
        self.post(self.message(event_id="different-event"))
        third = self.hermes.call_args.args[0]
        self.assertNotEqual(second[second.index("--idempotency-key") + 1], third[third.index("--idempotency-key") + 1])

    def test_unknown_sender_is_not_queued(self):
        status, response = self.post(self.message(sender_email="unknown@example.test"))
        self.assertEqual((status, response["route_status"]), (202, "unassigned"))
        self.assertTrue(response["action_required"])
        self.hermes.assert_not_called()

    def test_inactive_missing_or_wrong_scope_is_not_queued(self):
        for change in (
            {"status": "inactive"}, {"agent_id": ""}, {"consent": []},
            {"consent": {**employee()["consent"], "employee_agent_enabled": False}},
            {"consent": {**employee()["consent"], "approved_channel": "sms"}},
            {"consent": {**employee()["consent"], "approved_scope": ""}},
            {"consent": {**employee()["consent"], "approved_by": ""}},
        ):
            with self.subTest(change=change):
                self.roster = {"employees": [{**employee(), **change}]}
                status, response = self.post()
                self.assertEqual((status, response["route_status"]), (202, "held"))
        self.hermes.assert_not_called()

    def test_duplicate_or_conflicting_identity_is_not_queued(self):
        self.roster["employees"].append(deepcopy(employee()))
        self.assertEqual(self.post()[1]["route_status"], "unassigned")
        self.roster = {"employees": [employee()]}
        self.assertEqual(self.post(self.message(sender_phone="+15559999999"))[1]["route_status"], "unassigned")
        self.hermes.assert_not_called()

    def test_phone_only_identity_can_route_on_approved_channel(self):
        self.assertEqual(self.post({"event_id": "phone-event", "sender_phone": "+1 (555) 000-0001", "body": "Feedback"})[0], 200)

    def test_malformed_rosters_fail_closed(self):
        for roster in ([], {"employees": None}, {"employees": [None, {"phone": "bad"}]}):
            with self.subTest(roster=roster):
                self.roster = roster
                self.assertEqual(self.post()[1]["route_status"], "unassigned")
        self.hermes.assert_not_called()

    def test_invalid_messages_are_not_queued(self):
        for message in ([], {}, self.message(event_id=""), self.message(body=1), self.message(extra="raw vendor field"), self.message(sender_email="")):
            with self.subTest(message=message):
                self.assertEqual(self.post(message)[0], 400)
        self.hermes.assert_not_called()

    def test_invalid_json_length_and_provider(self):
        self.assertEqual(self.post(raw="{")[0], 400)
        self.assertEqual(self.post(headers={"Content-Length": "invalid"})[0], 400)
        self.assertEqual(self.post(headers={"Content-Length": "1048577"})[0], 413)
        self.assertEqual(self.post(headers={"x-businessos-provider": ""})[0], 400)
        self.hermes.assert_not_called()

    def test_stage_values_and_invalid_stage_fallback(self):
        for configured, expected in (("pre_acquisition", "pre_acquisition"), ("transition", "transition"), ("operating", "operating"), ("post_acquisition", "pre_acquisition"), ("", "pre_acquisition")):
            with self.subTest(stage=configured), patch.dict(os.environ, {"BUSINESS_STAGE": configured}):
                configuration = runpy.run_path(gateway.__file__)
                self.assertEqual(configuration["BUSINESS_STAGE"], expected)


if __name__ == "__main__":
    unittest.main()

"""Local stand-ins for accounts a repo declares. Fixture tokens only."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def load_services(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("services", []))


class SimHandler(BaseHTTPRequestHandler):
    services: list[dict] = []

    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/health"):
            self._json({"ok": True, "team": "gradia-sim", "services": [item["name"] for item in self.services]})
            return
        if self.path.startswith("/slack/api/auth.test"):
            if not self._authorized():
                self._json({"ok": False, "error": "invalid_auth"}, status=401)
                return
            self._json({"ok": True, "team": "gradia-sim", "user": "range-bot", "team_id": "T_SIM", "user_id": "U_SIM"})
            return
        self._json({"ok": False, "error": "unknown_method"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path.startswith("/slack/api/chat.postMessage"):
            if not self._authorized():
                self._json({"ok": False, "error": "invalid_auth"}, status=401)
                return
            self._json({"ok": True, "channel": "C_SIM", "ts": "1.0"})
            return
        self._json({"ok": False, "error": "unknown_method"}, status=404)

    def _authorized(self) -> bool:
        token = ""
        for item in self.services:
            if item.get("name") == "slack":
                token = str(item.get("token", ""))
        header = self.headers.get("Authorization", "")
        return header == f"Bearer {token}" and bool(token)

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        return


def serve(services_path: Path, host: str = "127.0.0.1", port: int = 8787) -> None:
    SimHandler.services = load_services(services_path)
    ThreadingHTTPServer((host, port), SimHandler).serve_forever()


if __name__ == "__main__":
    serve(Path("/opt/sim/services.json"))

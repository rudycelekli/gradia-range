"""Operator client. The host is already booted. This file does not create accounts."""

import hashlib
import json
import sys
from pathlib import Path


class Host:
    def __init__(self, body: dict) -> None:
        self._series = int(body["series"])
        self._clock = int(body["clock"])
        self._events = [dict(event) for event in body["events"]]
        self._password = dict(body["password"])
        self._session = dict(body["session"])
        self._minted = int(body["minted"])

    def login(self, email: str, password: str) -> dict:
        canonical = email.strip().lower()
        stored = self._password.get(canonical)
        digest = hashlib.sha256(password.encode()).hexdigest()
        if stored is None or digest != stored:
            self._append("login_failed", "product", email=canonical or None, ok=False)
            return {"ok": False, "email": canonical}
        token = self._token(canonical)
        self._append("login", "product", email=canonical, ok=True)
        return {"ok": True, "email": canonical, "token": token}

    def activity(self, token: str, name: str) -> dict:
        email = self._session.get(token)
        if email is None:
            self._append("activity", "product", ok=False, name=name)
            return {"ok": False, "name": name}
        self._append("activity", "product", email=email, ok=True, name=name)
        return {"ok": True, "email": email, "name": name}

    def log(self) -> list[dict]:
        rows = []
        allowed = {"signup", "login", "login_failed", "activity"}
        for event in self._events:
            if event.get("kind") not in allowed:
                continue
            rows.append({key: event.get(key) for key in ("t", "kind", "email", "ok", "name")})
        return rows

    def dump(self) -> dict:
        return {
            "series": self._series,
            "clock": self._clock,
            "events": self._events,
            "password": self._password,
            "session": self._session,
            "minted": self._minted,
        }

    def _token(self, email: str) -> str:
        self._minted += 1
        token = hashlib.sha256(f"{self._series}:{self._minted}:{email}".encode()).hexdigest()
        self._session[token] = email
        return token

    def _append(self, kind: str, seat: str, *, email: str | None = None, ok: bool | None = None, name: str | None = None) -> None:
        self._events.append({"t": self._clock, "kind": kind, "seat": seat, "email": email, "ok": ok, "name": name})
        self._clock += 1


def main(argv: list[str]) -> None:
    command = argv[1]
    state = Path(argv[2])
    host = Host(json.loads(state.read_text(encoding="utf-8")))
    if command == "login":
        result = host.login(argv[3], argv[4])
    elif command == "activity":
        result = host.activity(argv[3], argv[4])
    elif command == "log":
        print(json.dumps(host.log()))
        return
    else:
        raise SystemExit("unknown command: " + command)
    state.write_text(json.dumps(host.dump()), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main(sys.argv)

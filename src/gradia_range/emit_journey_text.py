"""Text files the journey emitter writes into a Harbor task."""

INSTRUCTION = """The host for this episode is already booted. Its state file is `/opt/range/state.json`. Copy that file to `/tmp/range-state.json` and drive the copy with `/opt/range/client.py`.

```
cp /opt/range/state.json /tmp/range-state.json
python3 /opt/range/client.py login /tmp/range-state.json ada@example.test ada-pass
python3 /opt/range/client.py activity /tmp/range-state.json TOKEN review
python3 /opt/range/client.py log /tmp/range-state.json
```

`login` prints a JSON object with `token`. Pass that token to `activity`. `log` prints the operator-visible rows.

A published account is already on the host:

- email: ada@example.test
- password: ada-pass

Sign in with that account and record one activity named `review`. Then write `/workspace/report.json` from the operator log.

The report is one JSON object:

- `assessment` is `complete`.
- `journey` is every operator-visible event of kind `signup`, `login`, `login_failed`, or `activity`, in clock order, after the review exists. Each item has exactly the keys `t`, `kind`, `email`, `ok`, and `name`. Use JSON null where a value is absent. `ok` is a boolean.
- `findings` lists each email that failed to sign in exactly three times. Each finding has `id` `login-burst`, `email`, `severity` `high`, and `times` as the clock values of those three failures, in order.

The reward is 1 only when the assessment, the full journey, the review activity, and the findings all match the host. A missing row, an extra row, a wrong clock, or a wrong email scores 0.
"""

DOCKERFILE = """FROM python:3.13-slim-bookworm
WORKDIR /workspace
COPY app /opt/range
ENV PYTHONDONTWRITEBYTECODE=1
"""

CLIENT = '''"""Operator client. The host is already booted. This file does not create accounts."""

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
'''

SOLVE = r"""#!/bin/bash
set -euo pipefail
APP="${RANGE_APP:-/opt/range}"
OUT="${RANGE_REPORT:-/workspace/report.json}"
STATE="${RANGE_STATE:-/tmp/range-state.json}"
PY="${RANGE_PYTHON:-python3}"
export PYTHONPATH="$APP"
cp "$APP/state.json" "$STATE"
TOKEN="$("$PY" "$APP/client.py" login "$STATE" ada@example.test ada-pass | "$PY" -c 'import json,sys; print(json.load(sys.stdin)["token"])')"
"$PY" "$APP/client.py" activity "$STATE" "$TOKEN" review >/dev/null
"$PY" "$APP/client.py" log "$STATE" > "${STATE}.log"
"$PY" - "$OUT" "${STATE}.log" <<'PY'
import json
import sys
from pathlib import Path

out, log_path = sys.argv[1], sys.argv[2]
journey = json.loads(Path(log_path).read_text(encoding="utf-8"))
times = {}
for row in journey:
    if row.get("kind") != "login_failed" or not row.get("email"):
        continue
    times.setdefault(row["email"], []).append(row["t"])
findings = [
    {"id": "login-burst", "email": email, "severity": "high", "times": hits}
    for email, hits in sorted(times.items())
    if len(hits) == 3
]
body = {"assessment": "complete", "journey": journey, "findings": findings}
Path(out).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
PY
"""

TEST = """#!/bin/bash
set -euo pipefail
mkdir -p /logs/verifier
export PYTHONPATH="${RANGE_TESTS:-/tests}"
python3 "${RANGE_TESTS:-/tests}/grade_journey.py" \
  "${RANGE_REPORT:-/workspace/report.json}" \
  /logs/verifier/reward.json \\
  /logs/verifier/reward.txt
"""

GRADER = '''#!/usr/bin/env python3
"""Grade the journey report. Writes reward.json and reward.txt."""

import json
import sys
from pathlib import Path

from journey import grade


def main() -> None:
    report_path, reward_json, reward_txt = sys.argv[1:]
    try:
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        report = {}
    scores = grade(report)
    Path(reward_json).write_text(json.dumps(scores) + "\\n", encoding="utf-8")
    Path(reward_txt).write_text(str(scores["reward"]) + "\\n", encoding="utf-8")


if __name__ == "__main__":
    main()
'''

TASK_TOML = """schema_version = "1.4"
version = "1.0"

[task]
name = "system0/journey"
description = "Reconcile the live host clock, the review activity, and a three-failure sign-in finding."
authors = [{ name = "Gradia Range" }]
keywords = ["range", "system0", "journey", "telemetry"]

[metadata]
difficulty = "hard"
category = "cybersecurity"
tags = ["live-host", "multi-check", "binary-reward"]
objective_planted = false

[verifier]
timeout_sec = 180.0

[agent]
timeout_sec = 1800.0

[environment]
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048
storage_mb = 10240
allow_internet = false
"""

WATCH_INSTRUCTION = """The host for this episode is already booted. Its state file is `/opt/range/state.json`. Copy that file to `/tmp/range-state.json` and drive the copy with `/opt/range/client.py`.

```
cp /opt/range/state.json /tmp/range-state.json
python3 /opt/range/client.py login /tmp/range-state.json ada@example.test ada-pass
python3 /opt/range/client.py activity /tmp/range-state.json TOKEN review
python3 /opt/range/client.py log /tmp/range-state.json
```

`login` prints a JSON object with `token`. Pass that token to `activity`.

A published account is already on the host:

- email: ada@example.test
- password: ada-pass

Sign in and record one activity named `review`. Then write `/workspace/handoff.json`.

The file is a JSON list of four objects, in this order, for the sign-in burst on the operator log:

1. `frm` `watch`, `to` `sense`
2. `frm` `sense`, `to` `confirm`
3. `frm` `confirm`, `to` `close`
4. `frm` `close`, `to` `tell`

Every object has `kind` `handoff`, `seat` `operator`, and `gap` `login_burst`. `t` is the clock of the last operator-visible row after the review, and the same `t` on all four objects.

The reward is 1 only when the list matches that chain. A wrong clock, a missing handoff, or an extra object scores 0.
"""

WATCH_TOML = TASK_TOML.replace('name = "system0/journey"', 'name = "system0/watch"').replace(
    "Reconcile the live host clock, the review activity, and a three-failure sign-in finding.",
    "Write the operator handoff chain for the sign-in burst after the review.",
)

WATCH_SOLVE = r"""#!/bin/bash
set -euo pipefail
APP="${RANGE_APP:-/opt/range}"
OUT="${RANGE_REPORT:-/workspace/handoff.json}"
STATE="${RANGE_STATE:-/tmp/range-state.json}"
PY="${RANGE_PYTHON:-python3}"
export PYTHONPATH="$APP"
cp "$APP/state.json" "$STATE"
TOKEN="$("$PY" "$APP/client.py" login "$STATE" ada@example.test ada-pass | "$PY" -c 'import json,sys; print(json.load(sys.stdin)["token"])')"
"$PY" "$APP/client.py" activity "$STATE" "$TOKEN" review >/dev/null
"$PY" "$APP/client.py" log "$STATE" > "${STATE}.log"
"$PY" - "$OUT" "${STATE}.log" <<'PY'
import json
import sys
from pathlib import Path

out, log_path = sys.argv[1], sys.argv[2]
journey = json.loads(Path(log_path).read_text(encoding="utf-8"))
clock = journey[-1]["t"]
pairs = (("watch", "sense"), ("sense", "confirm"), ("confirm", "close"), ("close", "tell"))
body = [
    {"t": clock, "kind": "handoff", "seat": "operator", "frm": frm, "to": to, "gap": "login_burst"}
    for frm, to in pairs
]
Path(out).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
PY
"""

WATCH_TEST = """#!/bin/bash
set -euo pipefail
mkdir -p /logs/verifier
export PYTHONPATH="${RANGE_TESTS:-/tests}"
python3 "${RANGE_TESTS:-/tests}/grade_watch.py" \\
  "${RANGE_REPORT:-/workspace/handoff.json}" \\
  /logs/verifier/reward.json \\
  /logs/verifier/reward.txt
"""

WATCH_GRADER = '''#!/usr/bin/env python3
"""Grade the watch handoff. Writes reward.json and reward.txt."""

import json
import sys
from pathlib import Path

from handoff import grade


def main() -> None:
    report_path, reward_json, reward_txt = sys.argv[1:]
    try:
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        report = {}
    scores = grade(report)
    Path(reward_json).write_text(json.dumps(scores) + "\\n", encoding="utf-8")
    Path(reward_txt).write_text(str(scores["reward"]) + "\\n", encoding="utf-8")


if __name__ == "__main__":
    main()
'''


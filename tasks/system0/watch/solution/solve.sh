#!/bin/bash
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

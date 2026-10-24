#!/bin/bash
set -euo pipefail
mkdir -p /logs/verifier
export PYTHONPATH="${RANGE_TESTS:-/tests}"
python3 "${RANGE_TESTS:-/tests}/grade_watch.py" \
  "${RANGE_REPORT:-/workspace/handoff.json}" \
  /logs/verifier/reward.json \
  /logs/verifier/reward.txt

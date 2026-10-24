#!/bin/bash
mkdir -p /logs/verifier
python3 /tests/check_report.py \
  --report /workspace/report.json \
  --root /workspace/repo \
  --revision c13b414b7a5a8a0a9c4f967be40bfa2c5a3a175e \
  --scope packages-twenty-shared \
  --prefixes packages/twenty-shared \
  --patch /workspace/fix.patch \
  --reward-dir /logs/verifier
status=$?
if [ ! -f /logs/verifier/reward.txt ]; then
  echo 0 > /logs/verifier/reward.txt
  echo '{"objective":0,"report":0,"reward":0}' > /logs/verifier/reward.json
fi
exit $status

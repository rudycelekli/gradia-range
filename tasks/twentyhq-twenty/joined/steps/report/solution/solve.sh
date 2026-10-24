#!/bin/bash
set -euo pipefail
cat > /workspace/report.json <<'EOF'
{
  "revision": "c13b414b7a5a8a0a9c4f967be40bfa2c5a3a175e",
  "scope": [
    "packages-twenty-server",
    "packages-twenty-front",
    "packages-twenty-shared"
  ],
  "assessment": "complete",
  "findings": []
}
EOF

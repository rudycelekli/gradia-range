#!/usr/bin/env python3
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
    Path(reward_json).write_text(json.dumps(scores) + "\n", encoding="utf-8")
    Path(reward_txt).write_text(str(scores["reward"]) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

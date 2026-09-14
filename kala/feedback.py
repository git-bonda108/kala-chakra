"""Lightweight learning loop: capture user feedback for later evaluation.

Feedback is appended as JSON lines to data/feedback.jsonl. This is the labeled
signal an offline job can use to score narration quality over time and to grow
the eval dataset. No PII beyond what the user typed is stored.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_PATH = os.path.join(_DATA_DIR, "feedback.jsonl")


def record_feedback(entry: dict) -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)
    entry = {"ts": datetime.now(timezone.utc).isoformat(), **entry}
    with open(_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_feedback(limit: int = 200) -> list:
    if not os.path.exists(_PATH):
        return []
    rows = []
    with open(_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows[-limit:]


def summary() -> dict:
    rows = load_feedback(10000)
    up = sum(1 for r in rows if r.get("rating") == "up")
    down = sum(1 for r in rows if r.get("rating") == "down")
    total = len(rows)
    return {
        "total": total,
        "up": up,
        "down": down,
        "satisfaction": round(up / total, 3) if total else None,
    }

#!/usr/bin/env python3
"""Add compact, non-blocking operating context when the plugin starts."""

from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> None:
    try:
        json.load(__import__("sys").stdin)
    except (json.JSONDecodeError, OSError):
        pass

    root = Path(os.environ.get("PLUGIN_ROOT", Path(__file__).resolve().parents[1]))
    records = sum(1 for path in (root / "knowledge").rglob("*.json") if path.name != "index.json")
    context = (
        "Frontend Taste Engineer is active. Classify the task, retrieve only relevant guidance, "
        "preserve mandatory accessibility and integrity rules, verify claims with evidence, and "
        f"use the offline fallback if MCP is unavailable. Local knowledge files detected: {records}."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()

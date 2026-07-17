#!/usr/bin/env python3
"""Add compact operating context and safely check for Git-backed updates."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> None:
    try:
        json.load(__import__("sys").stdin)
    except (json.JSONDecodeError, OSError):
        pass

    root = Path(os.environ.get("PLUGIN_ROOT", Path(__file__).resolve().parents[1]))
    records = sum(1 for path in (root / "knowledge").rglob("*.json") if path.name != "index.json")
    update_context = ""
    if os.environ.get("FTE_AUTO_UPDATE", "1").strip().lower() not in {"0", "false", "no", "off"}:
        try:
            sys.path.insert(0, str(root / "scripts"))
            from plugin_auto_update import run_auto_update

            update = run_auto_update()
            if update.status == "updated":
                update_context = (
                    f" Auto-update installed {update.available_version}; start a new Codex task after this one "
                    "to load the new plugin version."
                )
            elif update.status in {"update-failed", "verification-failed"}:
                update_context = " The last automatic update check failed safely; the existing plugin remains available."
        except Exception:
            update_context = " The automatic update check was unavailable; the existing plugin remains available."
    context = (
        "Frontend Taste Engineer is active. Classify the task, retrieve only relevant guidance, "
        "preserve mandatory accessibility and integrity rules, verify claims with evidence, and "
        f"use the offline fallback if MCP is unavailable. Local knowledge files detected: {records}."
        f"{update_context}"
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()

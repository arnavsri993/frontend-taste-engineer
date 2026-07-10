#!/usr/bin/env python3
"""Start the real server and exercise initialize, tools/list, and tools/call."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SERVER = Path(__file__).resolve().parents[1] / "server.py"


def main() -> int:
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "classify_frontend_task", "arguments": {"task": "Build an accessible responsive dialog in React"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "search_frontend_guidance", "arguments": {"query": "dialog keyboard focus responsive", "budget_records": 6, "context_budget": 2600}}},
    ]
    payload = "".join(json.dumps(message) + "\n" for message in messages)
    completed = subprocess.run(
        [sys.executable, str(SERVER)],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
        check=False,
    )
    if completed.returncode:
        print(json.dumps({"passed": False, "error": completed.stderr[-1000:]}, indent=2))
        return 1
    try:
        responses = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
        if len(responses) != 4:
            raise AssertionError(f"expected 4 responses, got {len(responses)}")
        tools = responses[1]["result"]["tools"]
        classification = responses[2]["result"]["structuredContent"]
        search = responses[3]["result"]["structuredContent"]
        assert any(item["name"] == "search_frontend_guidance" for item in tools)
        assert classification["task_type"] == "component-build"
        assert search["summary"]["estimated_context_tokens"] <= 2600
        assert search["records"]
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc), "stdout": completed.stdout[-2000:]}, indent=2))
        return 1
    print(json.dumps({
        "passed": True,
        "server": responses[0]["result"]["serverInfo"],
        "tool_count": len(tools),
        "classification": classification,
        "retrieved_ids": [item["id"] for item in search["records"]],
        "context_tokens": search["summary"]["estimated_context_tokens"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

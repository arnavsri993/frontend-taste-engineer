from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PLUGIN_ROOT / "scripts" / "plugin_auto_update.py"
SPEC = importlib.util.spec_from_file_location("fte_plugin_auto_update", SCRIPT)
assert SPEC and SPEC.loader
updater = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = updater
SPEC.loader.exec_module(updater)


def plugin_payload(*, version: str, source_type: str, source: str) -> dict:
    return {
        "installed": [
            {
                "name": "frontend-taste-engineer",
                "marketplaceName": "personal",
                "version": version,
                "marketplaceSource": {"sourceType": source_type, "source": source},
            }
        ]
    }


class QueueRunner:
    def __init__(self, *responses: dict) -> None:
        self.responses = list(responses)
        self.commands: list[list[str]] = []

    def __call__(self, command, timeout):
        self.commands.append(list(command))
        if not self.responses:
            raise AssertionError("Unexpected updater command")
        return updater.CommandResult(0, json.dumps(self.responses.pop(0)), "")


class FailingRunner:
    def __init__(self, first_response: dict) -> None:
        self.first_response = first_response
        self.commands: list[list[str]] = []

    def __call__(self, command, timeout):
        self.commands.append(list(command))
        if len(self.commands) == 1:
            return updater.CommandResult(0, json.dumps(self.first_response), "")
        return updater.CommandResult(1, "", "fatal: credential-bearing remote detail")


class PluginAutoUpdateTests(unittest.TestCase):
    def test_trusted_git_marketplace_updates_and_requires_restart(self) -> None:
        runner = QueueRunner(
            plugin_payload(
                version="0.3.0+codex.old",
                source_type="git",
                source="https://github.com/arnavsri993/frontend-taste-engineer.git",
            ),
            {"selectedMarketplaces": ["personal"], "upgradedRoots": ["/snapshot"], "errors": []},
            plugin_payload(
                version="0.4.0+codex.new",
                source_type="git",
                source="https://github.com/arnavsri993/frontend-taste-engineer.git",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            result = updater.run_auto_update(
                force=True,
                state_path=Path(directory) / "state.json",
                runner=runner,
                codex_binary="/usr/bin/codex-test",
            )
        self.assertEqual(result.status, "updated")
        self.assertEqual(result.available_version, "0.4.0+codex.new")
        self.assertTrue(result.restart_required)
        self.assertEqual(
            runner.commands[1],
            ["/usr/bin/codex-test", "plugin", "marketplace", "upgrade", "personal", "--json"],
        )

    def test_local_marketplace_is_never_overwritten(self) -> None:
        runner = QueueRunner(
            plugin_payload(
                version="0.3.0",
                source_type="local",
                source="/workspace/frontend-taste-engineer",
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            result = updater.run_auto_update(
                force=True,
                state_path=Path(directory) / "state.json",
                runner=runner,
                codex_binary="codex-test",
            )
        self.assertEqual(result.status, "local-development")
        self.assertEqual(len(runner.commands), 1)

    def test_untrusted_git_marketplace_is_rejected(self) -> None:
        runner = QueueRunner(
            plugin_payload(
                version="0.3.0",
                source_type="git",
                source="https://github.com/example/frontend-taste-engineer.git",
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            result = updater.run_auto_update(
                force=True,
                state_path=Path(directory) / "state.json",
                runner=runner,
                codex_binary="codex-test",
            )
        self.assertEqual(result.status, "untrusted-source")
        self.assertEqual(len(runner.commands), 1)

    def test_recent_check_is_deferred_without_starting_codex(self) -> None:
        runner = QueueRunner()
        now = dt.datetime(2026, 7, 17, 5, 0, tzinfo=dt.timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            state.write_text(
                json.dumps(
                    {
                        "checked_at": "2026-07-17T04:30:00Z",
                        "installed_version": "0.4.0",
                        "available_version": "0.4.0",
                        "marketplace": "personal",
                    }
                ),
                encoding="utf-8",
            )
            result = updater.run_auto_update(
                now=now,
                interval_seconds=3600,
                state_path=state,
                runner=runner,
                codex_binary="codex-test",
            )
        self.assertEqual(result.status, "deferred")
        self.assertEqual(runner.commands, [])

    def test_status_mode_does_not_refresh_marketplace(self) -> None:
        runner = QueueRunner(
            plugin_payload(
                version="0.4.0",
                source_type="git",
                source="arnavsri993/frontend-taste-engineer@main",
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            result = updater.run_auto_update(
                status_only=True,
                state_path=Path(directory) / "state.json",
                runner=runner,
                codex_binary="codex-test",
            )
        self.assertEqual(result.status, "ready")
        self.assertEqual(len(runner.commands), 1)

    def test_failed_refresh_keeps_installed_version_and_suppresses_stderr(self) -> None:
        runner = FailingRunner(
            plugin_payload(
                version="0.4.0",
                source_type="git",
                source="https://github.com/arnavsri993/frontend-taste-engineer.git",
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            result = updater.run_auto_update(
                force=True,
                state_path=Path(directory) / "state.json",
                runner=runner,
                codex_binary="codex-test",
            )
        self.assertEqual(result.status, "update-failed")
        self.assertEqual(result.installed_version, "0.4.0")
        self.assertNotIn("credential-bearing", result.message)


if __name__ == "__main__":
    unittest.main()

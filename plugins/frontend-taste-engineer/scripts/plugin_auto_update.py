#!/usr/bin/env python3
"""Safely refresh a Git-installed Frontend Taste Engineer plugin.

The updater delegates fetching, staging, and cache activation to Codex's plugin
manager. It never downloads an archive itself and never edits an installed
plugin cache. Local marketplace installs are deliberately left alone so a
development checkout cannot be replaced by a background update.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlparse


PLUGIN_NAME = "frontend-taste-engineer"
TRUSTED_GITHUB_REPOSITORY = "arnavsri993/frontend-taste-engineer"
DEFAULT_INTERVAL_SECONDS = 6 * 60 * 60
DEFAULT_TIMEOUT_SECONDS = 12.0
LOCK_STALE_SECONDS = 5 * 60


@dataclasses.dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


@dataclasses.dataclass(frozen=True)
class UpdateResult:
    status: str
    message: str
    installed_version: str | None = None
    available_version: str | None = None
    marketplace: str | None = None
    checked_at: str | None = None
    restart_required: bool = False

    def value(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


CommandRunner = Callable[[Sequence[str], float], CommandResult]


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _isoformat(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def default_state_path() -> Path:
    override = os.environ.get("FTE_UPDATE_STATE_FILE")
    if override:
        return Path(override).expanduser()
    if os.environ.get("XDG_CACHE_HOME"):
        root = Path(os.environ["XDG_CACHE_HOME"]).expanduser()
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Caches"
    elif os.name == "nt" and os.environ.get("LOCALAPPDATA"):
        root = Path(os.environ["LOCALAPPDATA"])
    else:
        root = Path.home() / ".cache"
    return root / PLUGIN_NAME / "auto-update-state-v1.json"


def _read_state(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, Mapping) else {}


def _write_state(path: Path, result: UpdateResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    payload = {"schema_version": 1, **result.value()}
    try:
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _parse_checked_at(value: object) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _should_defer(state: Mapping[str, Any], now: dt.datetime, interval_seconds: int) -> bool:
    checked_at = _parse_checked_at(state.get("checked_at"))
    if checked_at is None:
        return False
    return (now - checked_at).total_seconds() < max(0, interval_seconds)


def _subprocess_runner(command: Sequence[str], timeout: float) -> CommandResult:
    completed = subprocess.run(
        list(command),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def _run_json(runner: CommandRunner, command: Sequence[str], timeout: float) -> tuple[Mapping[str, Any] | None, str | None]:
    try:
        result = runner(command, timeout)
    except subprocess.TimeoutExpired:
        return None, f"Command timed out after {timeout:g} seconds."
    except OSError as exc:
        return None, f"Could not start Codex: {exc}."
    if result.returncode != 0:
        # Git errors can echo credential-bearing remote URLs. Keep persistent
        # updater state diagnostic enough without copying command output.
        return None, f"Codex exited with status {result.returncode}."
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, "Codex returned invalid JSON."
    if not isinstance(payload, Mapping):
        return None, "Codex returned an unexpected JSON value."
    return payload, None


def _installed_plugin(payload: Mapping[str, Any]) -> Mapping[str, Any] | None:
    installed = payload.get("installed")
    if not isinstance(installed, list):
        return None
    for item in installed:
        if isinstance(item, Mapping) and item.get("name") == PLUGIN_NAME:
            return item
    return None


def _normalize_github_repository(source: object) -> str | None:
    if not isinstance(source, str):
        return None
    value = source.strip()
    if value.startswith("git@github.com:"):
        value = value.removeprefix("git@github.com:")
    elif value.startswith("ssh://git@github.com/"):
        value = value.removeprefix("ssh://git@github.com/")
    elif "://" in value:
        parsed = urlparse(value)
        if parsed.hostname not in {"github.com", "www.github.com"}:
            return None
        value = parsed.path.lstrip("/")
    if "@" in value:
        value = value.rsplit("@", 1)[0]
    value = value.removesuffix(".git").strip("/").lower()
    return value if value.count("/") == 1 else None


def _marketplace_source(plugin: Mapping[str, Any]) -> tuple[str | None, str | None]:
    marketplace = plugin.get("marketplaceSource")
    if not isinstance(marketplace, Mapping):
        return None, None
    source_type = marketplace.get("sourceType")
    source = marketplace.get("originUrl") or marketplace.get("url") or marketplace.get("source")
    return (str(source_type).lower() if source_type is not None else None, str(source) if source is not None else None)


def _acquire_lock(path: Path) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        try:
            if time.time() - path.stat().st_mtime <= LOCK_STALE_SECONDS:
                return False
            path.unlink()
            descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except (FileNotFoundError, FileExistsError, OSError):
            return False
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
    finally:
        os.close(descriptor)
    return True


def _release_lock(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


def run_auto_update(
    *,
    force: bool = False,
    status_only: bool = False,
    interval_seconds: int = DEFAULT_INTERVAL_SECONDS,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    state_path: Path | None = None,
    now: dt.datetime | None = None,
    runner: CommandRunner = _subprocess_runner,
    codex_binary: str | None = None,
) -> UpdateResult:
    """Refresh the trusted Git marketplace and report whether a restart is needed."""

    moment = now or _utc_now()
    checked_at = _isoformat(moment)
    state_file = state_path or default_state_path()
    state = _read_state(state_file)
    if not force and not status_only and _should_defer(state, moment, interval_seconds):
        return UpdateResult(
            status="deferred",
            message="The automatic update check is not due yet.",
            installed_version=state.get("available_version") or state.get("installed_version"),
            available_version=state.get("available_version"),
            marketplace=state.get("marketplace"),
            checked_at=state.get("checked_at"),
            restart_required=bool(state.get("restart_required", False)),
        )

    binary = codex_binary or shutil.which("codex")
    if not binary:
        return UpdateResult("codex-unavailable", "The Codex CLI is not available on PATH.", checked_at=checked_at)

    lock_file = state_file.with_suffix(state_file.suffix + ".lock")
    try:
        locked = _acquire_lock(lock_file)
    except OSError as exc:
        return UpdateResult("state-unavailable", f"The updater could not create its local state lock: {exc}.", checked_at=checked_at)
    if not locked:
        return UpdateResult("busy", "Another Frontend Taste Engineer update check is already running.", checked_at=checked_at)

    try:
        before_payload, error = _run_json(runner, [binary, "plugin", "list", "--json"], timeout_seconds)
        if error or before_payload is None:
            result = UpdateResult("check-failed", error or "Could not inspect installed plugins.", checked_at=checked_at)
            _write_state(state_file, result)
            return result

        before = _installed_plugin(before_payload)
        if before is None:
            result = UpdateResult("not-installed", "Frontend Taste Engineer is not installed.", checked_at=checked_at)
            _write_state(state_file, result)
            return result

        installed_version = str(before.get("version") or "unknown")
        marketplace_name = str(before.get("marketplaceName") or "") or None
        source_type, source = _marketplace_source(before)
        if source_type == "local":
            result = UpdateResult(
                "local-development",
                "Automatic GitHub updates are disabled for a local marketplace checkout.",
                installed_version,
                installed_version,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result
        if source_type != "git":
            result = UpdateResult(
                "unsupported-source",
                "Automatic updates require a Git-backed Codex marketplace.",
                installed_version,
                installed_version,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result
        repository = _normalize_github_repository(source)
        if repository != TRUSTED_GITHUB_REPOSITORY:
            result = UpdateResult(
                "untrusted-source",
                "The configured Git marketplace is not the trusted Frontend Taste Engineer repository.",
                installed_version,
                installed_version,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result
        if status_only:
            return UpdateResult(
                "ready",
                "A trusted Git-backed installation is ready for automatic updates.",
                installed_version,
                installed_version,
                marketplace_name,
                checked_at,
            )
        if not marketplace_name:
            result = UpdateResult(
                "check-failed",
                "The installed plugin did not report its marketplace name.",
                installed_version,
                installed_version,
                checked_at=checked_at,
            )
            _write_state(state_file, result)
            return result

        upgrade_payload, error = _run_json(
            runner,
            [binary, "plugin", "marketplace", "upgrade", marketplace_name, "--json"],
            timeout_seconds,
        )
        if error or upgrade_payload is None:
            result = UpdateResult(
                "update-failed",
                error or "Codex could not refresh the Git marketplace.",
                installed_version,
                installed_version,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result
        if upgrade_payload.get("errors"):
            result = UpdateResult(
                "update-failed",
                "Codex reported an error while refreshing the Git marketplace.",
                installed_version,
                installed_version,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result

        after_payload, error = _run_json(runner, [binary, "plugin", "list", "--json"], timeout_seconds)
        if error or after_payload is None:
            result = UpdateResult(
                "verification-failed",
                error or "The refreshed installation could not be verified.",
                installed_version,
                None,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result
        after = _installed_plugin(after_payload)
        if after is None:
            result = UpdateResult(
                "verification-failed",
                "The plugin was missing after the marketplace refresh; the prior cache was not modified by this script.",
                installed_version,
                None,
                marketplace_name,
                checked_at,
            )
            _write_state(state_file, result)
            return result

        available_version = str(after.get("version") or "unknown")
        if available_version != installed_version:
            result = UpdateResult(
                "updated",
                f"Frontend Taste Engineer updated from {installed_version} to {available_version}.",
                installed_version,
                available_version,
                marketplace_name,
                checked_at,
                True,
            )
        else:
            result = UpdateResult(
                "current",
                f"Frontend Taste Engineer {installed_version} is current.",
                installed_version,
                available_version,
                marketplace_name,
                checked_at,
            )
        _write_state(state_file, result)
        return result
    except OSError as exc:
        return UpdateResult("state-unavailable", f"The updater could not use its local state file: {exc}.", checked_at=checked_at)
    finally:
        _release_lock(lock_file)


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Ignore the normal check interval.")
    parser.add_argument("--status", action="store_true", help="Inspect update eligibility without network access.")
    parser.add_argument(
        "--interval-seconds",
        type=_positive_int,
        default=int(os.environ.get("FTE_UPDATE_INTERVAL_SECONDS", DEFAULT_INTERVAL_SECONDS)),
        help="Minimum time between automatic checks (default: 21600).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=float(os.environ.get("FTE_UPDATE_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)),
        help="Timeout for each Codex plugin-manager command (default: 12).",
    )
    parser.add_argument("--state-file", type=Path, default=None, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if os.environ.get("FTE_AUTO_UPDATE", "1").strip().lower() in {"0", "false", "no", "off"} and not args.force and not args.status:
        result = UpdateResult("disabled", "Automatic updates are disabled by FTE_AUTO_UPDATE.")
    else:
        result = run_auto_update(
            force=args.force,
            status_only=args.status,
            interval_seconds=args.interval_seconds,
            timeout_seconds=max(0.1, args.timeout_seconds),
            state_path=args.state_file,
        )
    print(json.dumps(result.value(), indent=2, sort_keys=True))
    failed = {
        "check-failed",
        "codex-unavailable",
        "not-installed",
        "state-unavailable",
        "untrusted-source",
        "unsupported-source",
        "update-failed",
        "verification-failed",
    }
    return 0 if result.status not in failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

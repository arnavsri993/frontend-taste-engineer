#!/usr/bin/env python3
"""Run the complete 0.4 release gate and validate the full plugin archive."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
RESULTS = PLUGIN_ROOT / "evals" / "results"
SKILL_VALIDATOR = Path("/Users/arnavsrivastava/.codex/skills/.system/skill-creator/scripts/quick_validate.py")
PLUGIN_VALIDATOR = Path("/Users/arnavsrivastava/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py")


def run(label: str, command: list[str]) -> dict[str, object]:
    completed = subprocess.run(command, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    return {
        "label": label,
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": completed.stdout[-1200:],
        "stderr_tail": completed.stderr[-1200:],
    }


def main() -> int:
    commands = [
        run("validate-all", [sys.executable, str(PLUGIN_ROOT / "scripts" / "validate_all.py")]),
        run("unit-tests", [sys.executable, "-m", "unittest", "discover", "-s", str(PLUGIN_ROOT / "mcp-server" / "tests"), "-v"]),
        run("retrieval-evals", [sys.executable, str(PLUGIN_ROOT / "evals" / "run_retrieval_evals.py")]),
        run("frontend-evals", [sys.executable, str(PLUGIN_ROOT / "evals" / "run_frontend_evals.py")]),
        run("copy-evals", [sys.executable, str(PLUGIN_ROOT / "evals" / "run_copy_evals.py")]),
        run("skill-validator", [sys.executable, str(SKILL_VALIDATOR), str(PLUGIN_ROOT / "skills" / "frontend-taste-engineer")]),
        run("plugin-validator", [sys.executable, str(PLUGIN_VALIDATOR), str(PLUGIN_ROOT)]),
        run("package-plugin", [sys.executable, str(PLUGIN_ROOT / "scripts" / "package_plugin.py")]),
    ]
    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = str(manifest["version"])
    base_version = version.split("+", 1)[0]
    archive = PLUGIN_ROOT / "dist" / f"frontend-taste-engineer-plugin-{base_version}.zip"
    checks: dict[str, bool] = {
        "commands": all(item["passed"] for item in commands),
        "version_bumped": base_version == "0.4.0" and "+codex." in version,
        "migration_present": (PLUGIN_ROOT / "migrations" / "source-derived-design-and-copy-v1.md").is_file(),
        "archive_present": archive.is_file(),
        "codex_only_manifest": "apps" not in manifest,
    }
    eval_summaries = {}
    for name in ("retrieval", "frontend", "copy"):
        path = RESULTS / f"{name}.json"
        value = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        eval_summaries[name] = {"passed": bool(value.get("passed")), "path": str(path)}
        checks[f"{name}_eval"] = bool(value.get("passed"))
    frontend = json.loads((RESULTS / "frontend.json").read_text(encoding="utf-8"))
    checks["ten_rendered_frontends"] = frontend.get("case_count") == 10 and frontend.get("scored_cases") == 10 and all(item.get("capture_integrity") for item in frontend.get("cases") or [])
    copy = json.loads((RESULTS / "copy.json").read_text(encoding="utf-8"))
    checks["ten_copy_cases"] = copy.get("case_count") == 10
    annotations = json.loads((PLUGIN_ROOT / "evals" / "copy" / "grubby-pair-annotations.json").read_text(encoding="utf-8"))
    checks["twenty_one_pairs"] = annotations.get("pair_count") == 21 and len(annotations.get("annotations") or []) == 21
    archive_entries: list[str] = []
    archive_sha = ""
    if archive.is_file():
        archive_sha = hashlib.sha256(archive.read_bytes()).hexdigest()
        with zipfile.ZipFile(archive) as bundle:
            archive_entries = bundle.namelist()
        blocked = {".app.json", "scripts/package_skill.py", "dist/frontend-taste-engineer-skill.zip"}
        checks["archive_codex_only"] = not any(entry in blocked or entry.endswith("frontend-taste-engineer-skill.zip") for entry in archive_entries)
        checks["archive_has_runtime"] = all(required in archive_entries for required in (".codex-plugin/plugin.json", ".mcp.json", "skills/frontend-taste-engineer/SKILL.md", "mcp-server/server.py"))
    else:
        checks["archive_codex_only"] = False
        checks["archive_has_runtime"] = False
    passed = all(checks.values())
    report = {
        "schema_version": 1,
        "evaluation": "release-validation",
        "passed": passed,
        "version": version,
        "checks": checks,
        "commands": commands,
        "evaluations": eval_summaries,
        "archive": {"path": str(archive), "sha256": archive_sha, "entries": len(archive_entries)},
        "limitations": ["The private-term denylist is optional unless FTE_PRIVATE_TERMS_FILE is configured.", "Human screen-reader and subjective visual review remain outside deterministic release validation."],
    }
    out = PLUGIN_ROOT / "audits" / "generated" / "release-validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "version": version, "archive": str(archive), "archive_sha256": archive_sha, "report": str(out)}, indent=2))
    if not passed:
        print(json.dumps({key: value for key, value in checks.items() if not value}, indent=2), file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

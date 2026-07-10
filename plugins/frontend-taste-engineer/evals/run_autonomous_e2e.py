#!/usr/bin/env python3
"""Run the installed plugin against one synthetic minimal prompt and save evidence."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Sequence


EVAL_ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = EVAL_ROOT.parent
PROMPT = "Make a website directed to Alex containing “You made it — Arnav”"
DEFAULT_RESULTS = EVAL_ROOT / "results" / "e2e" / "minimal-alex-message"

PACKAGE_JSON = {
    "name": "frontend-taste-engineer-synthetic-e2e",
    "private": True,
    "version": "0.0.0",
    "type": "module",
    "scripts": {
        "build": "node build.mjs",
        "preview": "python3 -m http.server 4173 --directory dist",
        "capture": "node capture.mjs"
    }
}

BUILD_SCRIPT = r'''import { cp, mkdir, readdir, rm, stat } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const dist = path.join(root, "dist");
await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

const required = path.join(root, "index.html");
try { await stat(required); } catch { throw new Error("index.html is required for the production build"); }

for (const name of await readdir(root)) {
  if (["dist", "artifacts", "node_modules", "build.mjs", "capture.mjs", "package.json", "DESIGN.md"].includes(name)) continue;
  const source = path.join(root, name);
  const info = await stat(source);
  if (info.isDirectory() && name !== "assets") continue;
  if (info.isFile() && !/[.](html|css|js|json|svg|png|jpg|jpeg|webp|ico)$/i.test(name)) continue;
  await cp(source, path.join(dist, name), { recursive: true });
}
console.log(JSON.stringify({ built: true, output: dist }));
'''

CAPTURE_SCRIPT = r'''import { mkdir } from "node:fs/promises";
import { spawn, spawnSync } from "node:child_process";
import path from "node:path";

const root = process.cwd();
const output = path.join(root, "artifacts", "screenshots");
await mkdir(output, { recursive: true });
const chrome = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const server = spawn("python3", ["-m", "http.server", "4173", "--directory", "dist"], { cwd: root, stdio: "ignore" });
await new Promise(resolve => setTimeout(resolve, 900));
try {
  for (const [name, size] of [["desktop", "1440,1000"], ["mobile", "390,844"]]) {
    const target = path.join(output, `${name}.png`);
    const result = spawnSync(chrome, ["--headless=new", "--hide-scrollbars", "--disable-gpu", "--no-sandbox", `--window-size=${size}`, `--screenshot=${target}`, "http://127.0.0.1:4173"], { encoding: "utf8" });
    if (result.status !== 0) throw new Error(`Chrome capture failed for ${name}: ${result.stderr}`);
    console.log(JSON.stringify({ captured: name, size, target }));
  }
} finally {
  server.kill("SIGTERM");
}
'''


def write_fixture(root: Path) -> None:
    (root / "package.json").write_text(json.dumps(PACKAGE_JSON, indent=2) + "\n", encoding="utf-8")
    (root / "build.mjs").write_text(BUILD_SCRIPT, encoding="utf-8")
    (root / "capture.mjs").write_text(CAPTURE_SCRIPT, encoding="utf-8")


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:24]
    except OSError:
        return None
    if len(data) == 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    return None


def command_observed(trace: str, *terms: str) -> bool:
    folded = trace.casefold()
    return all(term.casefold() in folded for term in terms)


def run(args: argparse.Namespace) -> int:
    codex = Path(args.codex or shutil.which("codex") or "")
    if not codex.exists():
        raise RuntimeError("Codex CLI is unavailable")
    results = Path(args.results_dir).resolve()
    if results.exists():
        shutil.rmtree(results)
    results.mkdir(parents=True)
    (results / "prompt.txt").write_text(PROMPT + "\n", encoding="utf-8")

    fixture = Path(tempfile.mkdtemp(prefix="fte-synthetic-e2e-"))
    write_fixture(fixture)
    command = [
        str(codex), "exec", "--cd", str(fixture), "--skip-git-repo-check", "--ephemeral",
        "--json", "--dangerously-bypass-approvals-and-sandbox", "--dangerously-bypass-hook-trust",
        "--output-last-message", str(results / "final-message.md"), PROMPT,
    ]
    environment = dict(os.environ)
    environment.setdefault("CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    try:
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=int(args.timeout), check=False, env=environment)
    except subprocess.TimeoutExpired as exc:
        completed = subprocess.CompletedProcess(command, 124, exc.stdout or "", (exc.stderr or "") + "\nTimed out")
    (results / "codex-events.jsonl").write_text(completed.stdout or "", encoding="utf-8")
    (results / "codex-stderr.log").write_text(completed.stderr or "", encoding="utf-8")

    snapshot = results / "fixture"
    shutil.copytree(fixture, snapshot, ignore=shutil.ignore_patterns("node_modules", ".git"))
    final_message_path = results / "final-message.md"
    if final_message_path.exists():
        final_message_path.write_text(final_message_path.read_text(encoding="utf-8").replace(str(fixture), "fixture"), encoding="utf-8")
    build = subprocess.run(["npm", "run", "build"], cwd=snapshot, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    (results / "independent-build.log").write_text((build.stdout or "") + (build.stderr or ""), encoding="utf-8")

    trace = (completed.stdout or "") + "\n" + (results / "final-message.md").read_text(encoding="utf-8") if (results / "final-message.md").exists() else (completed.stdout or "")
    design = (snapshot / "DESIGN.md").read_text(encoding="utf-8") if (snapshot / "DESIGN.md").exists() else ""
    index = (snapshot / "index.html").read_text(encoding="utf-8") if (snapshot / "index.html").exists() else ""
    source_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in snapshot.iterdir() if path.is_file() and path.suffix in {".html", ".css", ".js", ".md"})
    screenshots = []
    for path in sorted(snapshot.rglob("*.png")):
        dimensions = png_dimensions(path)
        screenshots.append({"path": str(path.relative_to(snapshot)), "dimensions": list(dimensions) if dimensions else None})
    widths = [item["dimensions"][0] for item in screenshots if item["dimensions"]]
    screenshot_paths = " ".join(item["path"] for item in screenshots)
    trace_lower = trace.lower()
    checks = {
        "codex_exit": {"passed": completed.returncode == 0, "evidence": f"exit={completed.returncode}"},
        "skill_activation": {"passed": command_observed(trace, "frontend-taste-engineer") and command_observed(trace, "classify_frontend_task"), "evidence": "Codex trace contains plugin and classifier activity."},
        "autonomous_mode": {"passed": "autonomous-zero-brief-build" in (trace + design), "evidence": "Mode appears in trace or DESIGN.md."},
        "concept_inference": {"passed": "alex" in (design + index).lower() and ("personal-expressive" in (trace + design).lower() or "playful" in design.lower()), "evidence": "Synthetic recipient and expressive concept are present."},
        "design_thesis": {"passed": "design thesis" in design.lower() and len(design.splitlines()) >= 12, "evidence": "DESIGN.md contains a substantive design thesis."},
        "finished_copy": {"passed": "alex" in index.lower() and "arnav" in index.lower() and not any(term in source_text.lower() for term in ("lorem ipsum", "todo copy", "placeholder text")), "evidence": "Requested synthetic content is present without placeholder copy."},
        "complete_frontend": {"passed": (snapshot / "index.html").exists() and any(snapshot.glob("*.css")) and len(source_text) >= 3000, "evidence": "HTML, CSS, and substantial authored source exist."},
        "application_run": {"passed": any(term in trace_lower for term in ("http.server", "127.0.0.1", "npm run capture", "browser")), "evidence": "Trace records a running local interface or capture command."},
        "desktop_mobile_capture": {"passed": any(width >= 1000 for width in widths) and any(width <= 500 for width in widths), "evidence": screenshots},
        "screenshot_inspection": {"passed": ("view_image" in trace_lower or "browser" in trace_lower) and all(name in screenshot_paths.lower() for name in ("desktop", "mobile")), "evidence": "Trace records visual inspection and desktop/mobile artifacts exist."},
        "refinement": {"passed": any(term in (trace + design).lower() for term in ("three highest-impact", "three highest impact", "top three", "highest-impact weaknesses")) and (trace_lower.count("npm run capture") >= 2 or "revised capture" in design.lower()), "evidence": "Top-three review and recapture evidence found."},
        "production_build": {"passed": build.returncode == 0 and "npm run build" in trace_lower, "evidence": f"independent_exit={build.returncode}; agent build observed={ 'npm run build' in trace_lower }"},
        "honest_report": {"passed": (results / "final-message.md").exists() and any(term in (results / "final-message.md").read_text(encoding="utf-8").lower() for term in ("limitation", "verified", "build", "screenshot")), "evidence": "Final message reports executed evidence or limitations."},
    }
    result: dict[str, Any] = {
        "schema_version": 1,
        "evaluation": "autonomous-zero-brief-build-e2e",
        "fixture_policy": "synthetic-public-safe",
        "prompt": PROMPT,
        "passed": all(item["passed"] for item in checks.values()),
        "checks": checks,
        "artifacts": {
            "trace": "codex-events.jsonl",
            "stderr": "codex-stderr.log",
            "final_message": "final-message.md",
            "fixture": "fixture/",
            "screenshots": screenshots,
            "independent_build": "independent-build.log",
        },
        "limitations": ["Automated evidence does not prove screen-reader usability.", "Raster screenshots require manual visual privacy and quality inspection."],
    }
    (results / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "results": str(results), "failed_checks": [name for name, item in checks.items() if not item["passed"]]}, indent=2))
    if args.keep_fixture:
        print(json.dumps({"fixture": str(fixture)}))
    else:
        shutil.rmtree(fixture, ignore_errors=True)
    return 0 if result["passed"] else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--keep-fixture", action="store_true")
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())

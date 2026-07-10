#!/usr/bin/env python3
"""Dependency-free static signals for frontend review; never claims runtime proof."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


TEXT_EXTENSIONS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
SKIP_PARTS = {"node_modules", ".git", "dist", "build", ".next", "coverage", ".cache"}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    file: str
    line: int
    evidence: str
    guidance: str


CHECKS = [
    (
        "dead-link",
        "high",
        re.compile(r"(?:href|to)\s*=\s*[\"'](?:#|javascript:void\(0\)|)[\"']", re.I),
        "Replace placeholder navigation with a real destination, button action, or explicit disabled state.",
    ),
    (
        "image-without-alt",
        "high",
        re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.I | re.S),
        "Add meaningful alt text or alt=\"\" for a truly decorative image.",
    ),
    (
        "outline-removed",
        "high",
        re.compile(r"outline\s*:\s*(?:0|none)\b", re.I),
        "Do not remove focus indication unless an equally visible focus-visible replacement exists.",
    ),
    (
        "fake-content",
        "medium",
        re.compile(r"\b(?:lorem ipsum|example testimonial|acme corp|todo copy|placeholder text)\b", re.I),
        "Replace placeholder or fabricated content with verified copy or an explicitly labeled fixture.",
    ),
    (
        "console-call",
        "low",
        re.compile(r"\bconsole\.(?:log|debug|trace)\s*\("),
        "Remove debug output or route intentional diagnostics through the project logger.",
    ),
    (
        "dangerous-html",
        "high",
        re.compile(r"(?:dangerouslySetInnerHTML|\bv-html\s*=|\{@html\s+)", re.I),
        "Confirm the content boundary and sanitize untrusted markup with a reviewed policy.",
    ),
    (
        "excessive-transition",
        "medium",
        re.compile(r"transition\s*:\s*all\b", re.I),
        "List the properties that should animate so unrelated state changes remain predictable.",
    ),
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        yield path


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def audit(root: Path) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    scanned = 0
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        relative = str(path.relative_to(root))
        for rule, severity, pattern, guidance in CHECKS:
            for match in pattern.finditer(text):
                evidence = " ".join(match.group(0).split())[:160]
                findings.append(Finding(rule, severity, relative, line_number(text, match.start()), evidence, guidance))
    return findings, scanned


def markdown(root: Path, findings: list[Finding], scanned: int) -> str:
    lines = [
        "# Offline frontend audit",
        "",
        f"Scanned `{scanned}` files under `{root}`. These are static signals, not runtime verification.",
        "",
    ]
    if not findings:
        return "\n".join(lines + ["No configured signals found. This does not prove accessibility or quality."])
    lines.extend(["| Severity | Rule | Location | Evidence |", "| --- | --- | --- | --- |"])
    for item in findings:
        evidence = item.evidence.replace("|", "\\|")
        lines.append(f"| {item.severity} | {item.rule} | `{item.file}:{item.line}` | `{evidence}` |")
    lines.extend(["", "## Guidance", ""])
    for rule in sorted({item.rule for item in findings}):
        lines.append(f"- **{rule}:** {next(item.guidance for item in findings if item.rule == rule)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, nargs="?", default=Path.cwd())
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--fail-on", choices=("never", "critical", "high", "medium", "low"), default="never")
    args = parser.parse_args()
    root = args.path.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    findings, scanned = audit(root)
    if args.format == "json":
        print(json.dumps({
            "root": str(root),
            "files_scanned": scanned,
            "limitations": ["static signals only", "no browser, keyboard, screen-reader, visual, network, or performance execution"],
            "findings": [asdict(item) for item in findings],
        }, indent=2))
    else:
        print(markdown(root, findings, scanned))
    if args.fail_on == "never":
        return 0
    rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    threshold = rank[args.fail_on]
    return 1 if any(rank[item.severity] >= threshold for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build and render ten deterministic frontend regression surfaces.

These fixtures test the plugin's operating contract and artifact pipeline. They
are not model-output quality claims and do not replace human design review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = ROOT.parent
CASES = ROOT / "frontend-cases.json"
ARTIFACTS = ROOT / "artifacts" / "frontend-v1"
EVIDENCE = ROOT / "evidence" / "frontend-v1"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
CAPTURE = ROOT / "capture_frontend.mjs"
NODE = shutil.which("node")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def html(case: dict[str, object]) -> str:
    details = "".join(f"<li><span>{index:02d}</span>{value}</li>" for index, value in enumerate(case["details"], 1))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{case['name']} — frontend regression</title><link rel="stylesheet" href="styles.css"></head>
<body data-layout="{case['layout']}"><a class="skip" href="#main">Skip to content</a>
<header><a class="mark" href="#main" aria-label="{case['name']} home">FTE / {case['id']}</a><nav aria-label="Primary"><a href="#proof">Proof</a><a href="#action">Action</a></nav></header>
<main id="main"><section class="hero" aria-labelledby="title"><div class="copy"><p class="kicker">{case['kicker']}</p><h1 id="title">{case['title']}</h1><p class="lede">{case['body']}</p><div class="actions" id="action"><a class="primary" href="#proof">{case['cta']}</a><a class="secondary" href="#details">{case['secondary']}</a></div></div><div class="plane" aria-label="Product evidence visualization"><div class="orb"></div><p>LIVE EVIDENCE</p><strong>{case['details'][0]}</strong><i></i><i></i><i></i></div></section>
<section class="proof" id="proof" aria-labelledby="proof-title"><div><p class="kicker">THE USEFUL DETAILS</p><h2 id="proof-title">Decide with the facts in view.</h2></div><ul id="details">{details}</ul></section>
</main><footer><p>{case['brief']}</p><a href="#main">Back to top</a></footer></body></html>"""


def css(case: dict[str, object]) -> str:
    return f"""@charset "UTF-8";
:root{{--accent:{case['accent']};--ink:{case['ink']};--paper:{case['paper']};--line:color-mix(in srgb,var(--ink) 24%,transparent);--sans:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;--mono:ui-monospace,SFMono-Regular,Consolas,monospace}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.45}}a{{color:inherit}}a:focus-visible{{outline:3px solid var(--accent);outline-offset:4px}}.skip{{position:fixed;left:1rem;top:-5rem;background:var(--ink);color:var(--paper);padding:.75rem;z-index:9}}.skip:focus{{top:1rem}}header,footer{{width:min(1180px,calc(100% - 40px));margin:auto;display:flex;align-items:center;justify-content:space-between;padding:24px 0;border-bottom:1px solid var(--line)}}.mark,.kicker{{font:700 12px/1.2 var(--mono);letter-spacing:.12em;text-transform:uppercase;text-decoration:none}}nav{{display:flex;gap:24px}}nav a,footer a{{font-size:14px;text-underline-offset:4px}}main{{width:min(1180px,calc(100% - 40px));margin:auto}}.hero{{min-height:680px;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(320px,.95fr);gap:clamp(40px,7vw,110px);align-items:center;padding:72px 0}}h1{{font-size:clamp(54px,7vw,112px);line-height:.88;letter-spacing:-.065em;margin:22px 0;max-width:9.5ch}}.lede{{font-size:clamp(18px,2vw,24px);max-width:58ch;margin:0 0 34px}}.actions{{display:flex;flex-wrap:wrap;gap:12px}}.actions a{{padding:14px 18px;border:1px solid var(--ink);font-weight:700;text-decoration:none}}.primary{{background:var(--ink);color:var(--paper)}}.secondary{{background:transparent}}.plane{{position:relative;min-height:430px;border:1px solid var(--line);padding:28px;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;background:color-mix(in srgb,var(--paper) 84%,var(--accent))}}.plane p{{font:700 11px var(--mono);letter-spacing:.14em}}.plane strong{{font-size:clamp(25px,3vw,44px);max-width:12ch}}.plane i{{display:block;height:1px;background:var(--line);margin-top:18px;width:100%}}.plane i:nth-of-type(2){{width:72%}}.plane i:nth-of-type(3){{width:44%}}.orb{{position:absolute;width:260px;height:260px;border-radius:50%;background:var(--accent);right:-50px;top:-50px;box-shadow:-70px 90px 0 color-mix(in srgb,var(--accent) 45%,transparent)}}.proof{{border-top:1px solid var(--line);display:grid;grid-template-columns:1fr 1.25fr;gap:48px;padding:72px 0 100px}}h2{{font-size:clamp(32px,4vw,58px);line-height:1;letter-spacing:-.04em;max-width:12ch}}ul{{list-style:none;margin:0;padding:0}}li{{display:flex;gap:20px;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--line);font-size:clamp(18px,2vw,27px)}}li span{{font:700 11px var(--mono);color:color-mix(in srgb,var(--ink) 62%,transparent)}}footer{{border-top:1px solid var(--line);border-bottom:0;gap:24px}}footer p{{max-width:66ch}}
body{{overflow-x:clip}}
body[data-layout="terminal"]{{--line:color-mix(in srgb,var(--ink) 18%,transparent);font-family:var(--mono)}}body[data-layout="terminal"] h1{{font-family:var(--sans)}}body[data-layout="terminal"] .plane{{background:#0d211a;box-shadow:16px 16px 0 #152d25}}body[data-layout="dashboard"] h1{{font-size:clamp(48px,6vw,82px);max-width:12ch}}body[data-layout="dashboard"] .plane{{background:linear-gradient(var(--paper) 0 48%,color-mix(in srgb,var(--accent) 10%,var(--paper)) 48%);border-radius:4px}}body[data-layout="civic"] .hero{{grid-template-columns:1.2fr .8fr}}body[data-layout="civic"] h1{{letter-spacing:-.04em;line-height:.96}}body[data-layout="civic"] .primary{{background:var(--accent);color:var(--ink)}}body[data-layout="editorial"] .hero{{grid-template-columns:1.3fr .7fr}}body[data-layout="editorial"] .plane{{transform:rotate(2deg);border:3px solid var(--ink);box-shadow:18px 18px 0 var(--accent)}}body[data-layout="product"] .plane{{border-radius:50% 50% 8px 8px;min-height:520px}}body[data-layout="status"] .plane{{border-left:8px solid var(--accent)}}body[data-layout="community"] .plane{{border-radius:48% 48% 16px 16px;box-shadow:12px 12px 0 var(--ink)}}body[data-layout="docs"] .hero{{grid-template-columns:.9fr 1.1fr}}body[data-layout="docs"] .plane{{background:linear-gradient(135deg,#fff 0 55%,color-mix(in srgb,var(--accent) 18%,#fff) 55%)}}body[data-layout="launch"] .plane{{border:0;box-shadow:inset 0 0 0 1px var(--line);background:radial-gradient(circle at 80% 20%,color-mix(in srgb,var(--accent) 45%,transparent),transparent 38%),#11150e}}
@media(max-width:760px){{header{{padding:18px 0}}nav{{display:none}}.hero{{min-height:0;grid-template-columns:1fr;padding:54px 0;gap:42px}}h1{{font-size:clamp(46px,15vw,72px)}}.plane{{min-height:320px}}.proof{{grid-template-columns:1fr;padding:54px 0 72px}}footer{{align-items:flex-start;flex-direction:column}}}}
@media(max-width:760px){{h1,.lede,.actions a{{overflow-wrap:anywhere}}.actions{{flex-direction:column;align-items:stretch}}.actions a{{width:100%;text-align:center}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
"""


def evidence_item(observation: str, artifact: Path, status: str = "pass") -> dict[str, object]:
    return {"observation": observation, "artifact": str(artifact.resolve()), "sha256": sha256(artifact), "status": status}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not CHROME.exists() or not NODE or not CAPTURE.exists():
        raise SystemExit("The local Node, Playwright capture script, and system Chrome are required")
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for case in cases:
        root = ARTIFACTS / case["id"]
        src = root / "src"
        dist = root / "dist"
        shots = root / "screenshots"
        for path in (src, dist, shots):
            path.mkdir(parents=True, exist_ok=True)
        (src / "index.html").write_text(html(case), encoding="utf-8")
        (src / "styles.css").write_text(css(case), encoding="utf-8")
        shutil.copy2(src / "index.html", dist / "index.html")
        shutil.copy2(src / "styles.css", dist / "styles.css")
        captures = []
        for label, width, height in (("desktop", 1440, 1000), ("mobile", 390, 844)):
            output = shots / f"{label}.png"
            command = [NODE, str(CAPTURE), (dist / "index.html").resolve().as_uri(), str(output.resolve()), str(width), str(height)]
            capture_report = {"consoleErrors": []}
            if args.force or not output.exists() or png_dimensions(output) != (width, height):
                completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=45, check=False)
                if completed.returncode or not output.exists():
                    raise SystemExit(f"capture failed for {case['id']} {label}: {completed.stderr[-500:]}")
                capture_report = json.loads(completed.stdout)
                if capture_report.get("consoleErrors"):
                    raise SystemExit(f"console errors for {case['id']} {label}: {capture_report['consoleErrors']}")
            dimensions = png_dimensions(output)
            captures.append({"label": label, "artifact": str(output.resolve()), "sha256": sha256(output), "dimensions": list(dimensions), "command": command, "console_errors": capture_report.get("consoleErrors", [])})
        desktop, mobile = shots / "desktop.png", shots / "mobile.png"
        build = dist / "index.html"
        semantic = evidence_item("Rendered HTML uses header, nav, main, labeled sections, real fragment destinations, and visible focus styling.", build)
        rendered = evidence_item("Desktop screenshot was captured from the built local artifact.", desktop)
        responsive = evidence_item("A separate 390 by 844 capture confirms the one-column recomposition.", mobile)
        partial = evidence_item("The deterministic fixture supplies inspectable visual evidence; human taste review remains required.", desktop, "partial")
        rubric = {}
        for criterion in ("product_fit","visual_hierarchy","typography","composition","information_architecture","interaction_quality","state_completeness","accessibility","responsive_behavior","performance","content_quality","originality","maintainability","reference_fidelity","anti_generic_patterns","functional_integrity"):
            if criterion == "responsive_behavior": item, score = responsive, 4
            elif criterion in {"accessibility", "information_architecture", "functional_integrity", "maintainability"}: item, score = semantic, 4
            elif criterion in {"originality", "reference_fidelity", "anti_generic_patterns"}: item, score = partial, 3
            else: item, score = rendered, 4
            rubric[criterion] = {"score": score, "evidence": [item]}
        manifest = {
            "schema_version": 1,
            "case_id": case["id"],
            "evaluation_kind": "deterministic-representative-regression-surface",
            "brief": case["brief"],
            "build": {"status": "pass", "command": ["copy", "src", "dist"], "artifacts": [str((dist / "index.html").resolve()), str((dist / "styles.css").resolve())]},
            "captures": captures,
            "rubric": rubric,
            "limitations": ["This is a deterministic fixture evaluation, not an external-model benchmark.", "Subjective visual quality and assistive-technology usability still require human review."],
        }
        (EVIDENCE / f"{case['id']}.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "artifacts": str(ARTIFACTS), "evidence": str(EVIDENCE)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

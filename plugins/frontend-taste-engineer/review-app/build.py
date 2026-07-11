#!/usr/bin/env python3
"""Build a standalone static showcase from the local plugin artifacts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = APP_ROOT.parent
DIST_ROOT = APP_ROOT / "dist"


def copy_file(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Required showcase input is missing: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_site() -> Path:
    """Create a self-contained static build and return its directory."""
    if DIST_ROOT.exists():
        shutil.rmtree(DIST_ROOT)
    DIST_ROOT.mkdir(parents=True)

    copy_file(APP_ROOT / "styles.css", DIST_ROOT / "styles.css")
    copy_file(APP_ROOT / "app.js", DIST_ROOT / "app.js")
    copy_file(PLUGIN_ROOT / "assets" / "icon.svg", DIST_ROOT / "favicon.svg")

    html = (APP_ROOT / "index.html").read_text(encoding="utf-8")
    html = html.replace("../assets/icon.svg", "./favicon.svg")
    (DIST_ROOT / "index.html").write_text(html, encoding="utf-8")

    generated_index_path = PLUGIN_ROOT / "ingestion" / "knowledge-index.json"
    generated_index = json.loads(generated_index_path.read_text(encoding="utf-8"))

    bundled_artifacts = {
        PLUGIN_ROOT / "knowledge" / "index.json": DIST_ROOT / "data" / "index.json",
        generated_index_path: DIST_ROOT / "data" / "knowledge-index.json",
        PLUGIN_ROOT / "research" / "source-registry.yml": DIST_ROOT / "data" / "source-registry.yml",
        PLUGIN_ROOT / "evals" / "results" / "retrieval.json": DIST_ROOT / "data" / "retrieval.json",
        PLUGIN_ROOT / "evals" / "results" / "frontend.json": DIST_ROOT / "data" / "frontend.json",
    }
    for source, destination in bundled_artifacts.items():
        copy_file(source, destination)

    origins = sorted(
        {
            item["origin"]
            for item in generated_index.get("records", [])
            if isinstance(item, dict) and item.get("origin")
        }
    )
    for origin in origins:
        copy_file(PLUGIN_ROOT / "knowledge" / origin, DIST_ROOT / "data" / origin)

    print(f"Built standalone showcase: {DIST_ROOT}", flush=True)
    return DIST_ROOT


if __name__ == "__main__":
    build_site()

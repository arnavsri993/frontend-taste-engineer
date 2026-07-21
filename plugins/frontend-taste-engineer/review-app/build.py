#!/usr/bin/env python3
"""Build the standalone Leonida Heat Ledger static application."""

from __future__ import annotations

import shutil
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parent
DIST_ROOT = APP_ROOT / "dist"

SECURITY_HEADERS = """/*
  Content-Security-Policy: default-src 'self'; base-uri 'none'; connect-src 'self'; font-src 'self'; form-action 'none'; frame-ancestors 'none'; img-src 'self' data:; object-src 'none'; script-src 'self'; style-src 'self'
  Permissions-Policy: camera=(), geolocation=(), microphone=()
  Referrer-Policy: strict-origin-when-cross-origin
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
"""


def copy_file(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Required application input is missing: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_site() -> Path:
    """Create a self-contained static build and return its directory."""
    if DIST_ROOT.exists():
        shutil.rmtree(DIST_ROOT)
    DIST_ROOT.mkdir(parents=True)

    for filename in ("index.html", "styles.css", "app.js", "favicon.png"):
        copy_file(APP_ROOT / filename, DIST_ROOT / filename)

    assets_root = APP_ROOT / "assets"
    if not assets_root.is_dir():
        raise FileNotFoundError(f"Required application assets are missing: {assets_root}")
    shutil.copytree(assets_root, DIST_ROOT / "assets")

    copy_file(APP_ROOT / "index.html", DIST_ROOT / "404.html")
    (DIST_ROOT / "_redirects").write_text("/* /index.html 200\n", encoding="utf-8")
    (DIST_ROOT / "_headers").write_text(SECURITY_HEADERS, encoding="utf-8")

    print(f"Built standalone Leonida Heat Ledger application: {DIST_ROOT}", flush=True)
    return DIST_ROOT


if __name__ == "__main__":
    build_site()

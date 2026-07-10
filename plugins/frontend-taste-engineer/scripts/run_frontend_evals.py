#!/usr/bin/env python3
"""Compatibility entrypoint for evidence-backed frontend output evaluation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "evals" / "eval_core.py"
spec = importlib.util.spec_from_file_location("fte_frontend_eval_core_script", path)
if not spec or not spec.loader:
    raise RuntimeError(f"Cannot load {path}")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

if __name__ == "__main__":
    raise SystemExit(module.frontend_main())

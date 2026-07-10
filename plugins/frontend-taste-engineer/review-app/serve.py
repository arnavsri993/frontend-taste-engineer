#!/usr/bin/env python3
"""Serve the local read-only review UI from the plugin root."""

from __future__ import annotations

import argparse
import functools
import http.server
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=plugin_root)
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Frontend Taste Engineer review: http://{args.host}:{args.port}/review-app/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

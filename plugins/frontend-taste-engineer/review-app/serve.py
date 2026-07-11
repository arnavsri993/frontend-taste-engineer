#!/usr/bin/env python3
"""Build and serve the standalone Frontend Taste Engineer showcase."""

from __future__ import annotations

import argparse
import functools
import http.server

from build import DIST_ROOT, build_site


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Serve the existing dist directory without rebuilding it.",
    )
    args = parser.parse_args()
    dist_root = DIST_ROOT if args.no_build else build_site()
    if not dist_root.is_dir():
        parser.error("No dist directory exists. Run build.py or omit --no-build.")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dist_root)
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    server.daemon_threads = True
    print(f"Frontend Taste Engineer showcase: http://{args.host}:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build and serve the standalone Leonida Heat Ledger application."""

from __future__ import annotations

import argparse
import functools
import http.server
from pathlib import Path
from urllib.parse import urlsplit

from build import DIST_ROOT, build_site


class ApplicationRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve static assets and fall back to the application shell for routes."""

    def end_headers(self) -> None:
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; base-uri 'none'; connect-src 'self'; font-src 'self'; "
            "form-action 'none'; frame-ancestors 'none'; img-src 'self' data:; "
            "object-src 'none'; script-src 'self'; style-src 'self'",
        )
        self.send_header("Permissions-Policy", "camera=(), geolocation=(), microphone=()")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        super().end_headers()

    def send_head(self):  # type: ignore[override]
        request_path = urlsplit(self.path).path
        candidate = Path(self.translate_path(request_path))
        if not candidate.exists() and not Path(request_path).suffix:
            self.path = "/index.html"
        return super().send_head()


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
    handler = functools.partial(ApplicationRequestHandler, directory=dist_root)
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    server.daemon_threads = True
    print(f"Leonida Heat Ledger: http://{args.host}:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

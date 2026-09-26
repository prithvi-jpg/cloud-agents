#!/usr/bin/env python3
"""Serve a run's observer room with a live read-only state endpoint."""

from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from render_test_room import build_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8893)
    args = parser.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("The observer server must bind to a loopback host")
    if not 1 <= args.port <= 65535:
        raise SystemExit("Port must be between 1 and 65535")
    if not (run_dir / "manifest.json").exists():
        raise SystemExit(f"Run manifest does not exist: {run_dir}")

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=str(run_dir), **handler_kwargs)

        def do_GET(self) -> None:
            request_path = urlparse(self.path).path
            if request_path == "/api/state":
                body = json.dumps(build_payload(run_dir), ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
                return
            if request_path == "/":
                self.path = "/test-room.html"
            super().do_GET()

        def log_message(self, format_string: str, *format_args: object) -> None:
            print(f"[observer] {format_string % format_args}")

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Observer room: http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

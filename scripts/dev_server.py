#!/usr/bin/env python3

from __future__ import annotations

import argparse
import functools
import http.server
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "tmp" / "dev-site"
WATCH_PATHS = [
    REPO_ROOT / "docs",
    REPO_ROOT / "docs_es",
    REPO_ROOT / "overrides",
    REPO_ROOT / "mkdocs.base.yml",
    REPO_ROOT / "mkdocs.yml",
    REPO_ROOT / "mkdocs.es.yml",
]


def mkdocs_command() -> list[str]:
    venv_mkdocs = REPO_ROOT / ".venv" / "bin" / "mkdocs"
    if venv_mkdocs.exists():
        return [str(venv_mkdocs)]
    return ["mkdocs"]


def build_site() -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    command = mkdocs_command()

    subprocess.run(
        [*command, "build", "--strict", "-f", "mkdocs.yml", "--site-dir", str(SITE_DIR)],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(
        [*command, "build", "--strict", "-f", "mkdocs.es.yml", "--site-dir", str(SITE_DIR / "es")],
        cwd=REPO_ROOT,
        check=True,
    )


def snapshot() -> dict[str, int]:
    state: dict[str, int] = {}
    for path in WATCH_PATHS:
        if not path.exists():
            continue
        if path.is_file():
            state[str(path)] = path.stat().st_mtime_ns
            continue

        for item in path.rglob("*"):
            if item.is_file():
                state[str(item)] = item.stat().st_mtime_ns
    return state


def watch(stop_event: threading.Event, interval: float) -> None:
    previous = snapshot()
    while not stop_event.is_set():
        time.sleep(interval)
        current = snapshot()
        if current == previous:
            continue

        print("[dev-server] Change detected. Rebuilding EN + ES...", flush=True)
        try:
            build_site()
            previous = current
            print("[dev-server] Rebuild complete.", flush=True)
        except subprocess.CalledProcessError as error:
            print(f"[dev-server] Rebuild failed with exit code {error.returncode}. Keeping previous output.", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the combined EN/ES MkDocs site locally.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("[dev-server] Building initial combined site...", flush=True)
    try:
        build_site()
    except subprocess.CalledProcessError as error:
        print(f"[dev-server] Initial build failed with exit code {error.returncode}.", file=sys.stderr, flush=True)
        return error.returncode

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE_DIR))
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    stop_event = threading.Event()
    watcher = threading.Thread(target=watch, args=(stop_event, args.interval), daemon=True)
    watcher.start()

    def shutdown(*_: object) -> None:
        stop_event.set()
        server.shutdown()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print(f"[dev-server] Serving combined site on http://{args.host}:{args.port}/", flush=True)
    print(f"[dev-server] Spanish version available at http://{args.host}:{args.port}/es/", flush=True)
    try:
        server.serve_forever()
    finally:
        stop_event.set()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

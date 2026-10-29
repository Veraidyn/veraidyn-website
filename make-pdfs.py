#!/usr/bin/env python3
"""
Render each long-form article to a PDF in assets/papers/.

The HTML page is the source of record. These PDFs are generated from it, so
the downloadable file and the web page can never say different things. The
layout comes from the @media print rules in assets/site.css.

Run this before publishing any change to an article, or the PDF goes stale:

    python make-pdfs.py

The script serves the project itself on a free local port, so it does not
matter whether your dev server is running. It uses the Chromium browser
already on the machine (Edge or Chrome) rather than downloading one.
"""

import http.server
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

HERE = pathlib.Path(__file__).parent.resolve()
OUT_DIR = HERE / "assets" / "papers"

# Each entry maps an article URL path to the PDF filename it produces.
# Add a line here when a new paper is published.
PAPERS = [
    ("/resources/trust-lives-between-two-systems/", "measuring-trust-in-agentic-systems.pdf"),
    ("/resources/seven-domains-of-agentic-assessment/", "seven-domains-of-agentic-assessment.pdf"),
    ("/resources/trust-is-repaired-not-revoked/", "trust-is-repaired-not-revoked.pdf"),
]

BROWSERS = [
    r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
    r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
    r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
    r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
]


def find_browser():
    for raw in BROWSERS:
        p = pathlib.Path(os.path.expandvars(raw))
        if p.exists():
            return p
    for name in ("chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return pathlib.Path(found)
    sys.exit("No Chromium browser found. Install Chrome or Edge, or render by "
             "opening the page and using Print to PDF.")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(port):
    # Must be threading. A browser opens several connections at once for the
    # stylesheet and fonts; a single-threaded server deadlocks on the first
    # keep-alive connection and the page never finishes loading.
    handler = lambda *a, **kw: QuietHandler(*a, directory=str(HERE), **kw)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def wait_for_pdf(target, timeout=90.0):
    """Return the final size once the file exists and has stopped growing."""
    deadline = time.time() + timeout
    last = -1
    stable = 0
    while time.time() < deadline:
        if target.exists():
            size = target.stat().st_size
            if size > 0 and size == last:
                stable += 1
                if stable >= 3:          # same size three polls running
                    return size
            else:
                stable = 0
            last = size
        time.sleep(0.4)
    return 0


def main():
    browser = find_browser()
    port = free_port()
    httpd = serve(port)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Rendering with %s" % browser.name)
    print("Serving %s on port %d\n" % (HERE.name, port))

    # A throwaway profile. Without this the render fails silently whenever the
    # browser is already running against its normal profile, which it usually is.
    profile = pathlib.Path(tempfile.mkdtemp(prefix="veraidyn-pdf-"))

    failures = 0
    for url_path, filename in PAPERS:
        target = OUT_DIR / filename
        url = "http://127.0.0.1:%d%s" % (port, url_path)
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--user-data-dir=%s" % profile,
            "--print-to-pdf=%s" % target,
            url,
        ]
        if target.exists():
            target.unlink()

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

        # The browser hands the render to a detached child and the parent exits
        # almost immediately, so the exit code says nothing about whether the
        # PDF was written. Wait for the file to appear and stop growing.
        size = wait_for_pdf(target)

        if size:
            print("  %-46s %6.0f KB" % (filename, size / 1024))
        else:
            failures += 1
            print("  FAILED: %s" % filename)
            if res.stderr.strip():
                print("    %s" % res.stderr.strip().splitlines()[-1])

    httpd.shutdown()
    shutil.rmtree(profile, ignore_errors=True)

    if failures:
        sys.exit("\n%d paper(s) failed to render." % failures)
    print("\nWrote %d PDF(s) to assets/papers/." % len(PAPERS))
    print("These are published assets and ARE committed. Re-run after editing "
          "an article so the download matches the page.")


if __name__ == "__main__":
    main()

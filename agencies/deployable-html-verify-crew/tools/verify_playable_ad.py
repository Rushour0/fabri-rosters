"""Frozen-contract boot-smoke for a self-contained playable-ad index.html.

Ported from ludexel-app engines/web/ludexel_web/smoke.py (the pure-Python Tier-0
gate). No browser, no Node — deterministic string/HTML checks only. A game that
passes here is deployable into the engines/web `freeform` genre. Input/output is
the standard fabri custom-tool contract: a JSON object on stdin, a JSON object on
stdout; paths are resolved under $FABRI_SANDBOX_ROOT and may not escape it.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# Tokens that must never appear in a freeform game's inline JS: network egress,
# persistent storage, iframe/parent escape, dynamic code execution. Over-matching
# fails safe (a false positive costs a repair cycle, never a breach).
_EGRESS = {
    "network fetch()": re.compile(r"\bfetch\s*\("),
    "XMLHttpRequest": re.compile(r"\bXMLHttpRequest\b"),
    "WebSocket": re.compile(r"\bWebSocket\b"),
    "EventSource": re.compile(r"\bEventSource\b"),
    "navigator.sendBeacon": re.compile(r"\bsendBeacon\b"),
    "dynamic import()": re.compile(r"\bimport\s*\("),
    "document.cookie": re.compile(r"\bdocument\s*\.\s*cookie\b"),
    "localStorage": re.compile(r"\blocalStorage\b"),
    "sessionStorage": re.compile(r"\bsessionStorage\b"),
    "indexedDB": re.compile(r"\bindexedDB\b"),
    "window.top / window.parent escape": re.compile(r"\bwindow\s*\.\s*(top|parent)\b"),
    "eval()": re.compile(r"\beval\s*\("),
    "new Function()": re.compile(r"\bnew\s+Function\s*\("),
}
_MAX = 3_000_000  # generous cap for a self-contained game with base64 art.


def _is_remote(url: str) -> bool:
    u = (url or "").strip().lower()
    return u.startswith(("http://", "https://", "//", "ftp:", "ws://", "wss://"))


class _Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canvas = 0
        self.external: list[str] = []
        self.scripts: list[str] = []
        self._in = False
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "canvas":
            self.canvas += 1
        elif tag == "script":
            src = a.get("src", "").strip()
            if src:
                self.external.append(f"<script src={src!r}>")
            else:
                self._in = True
                self._buf = []
        elif tag == "link":
            if _is_remote(a.get("href", "")):
                self.external.append(f"<link href={a.get('href')!r}>")
        elif tag in ("img", "image", "audio", "video", "source", "track"):
            if _is_remote(a.get("src", "")):
                self.external.append(f"<{tag} src={a.get('src')!r}>")
        elif tag in ("iframe", "object", "embed", "frame"):
            self.external.append(f"<{tag}> (nested browsing context)")

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in:
            self._in = False
            self.scripts.append("".join(self._buf))
            self._buf = []


def smoke(html: str) -> list[str]:
    """Return blocking problems (empty == the game is deployable)."""
    problems: list[str] = []
    if not html or not html.strip():
        return ["index.html is empty"]
    if len(html.encode("utf-8", "ignore")) > _MAX:
        problems.append("index.html exceeds the size cap")
    low = html.lower()
    if "<html" not in low and "<!doctype" not in low:
        problems.append("index.html is not a complete HTML document")
    s = _Scan()
    try:
        s.feed(html)
        s.close()
    except Exception as e:  # noqa: BLE001
        return problems + [f"index.html could not be parsed as HTML: {str(e)[:120]}"]
    if s.canvas == 0:
        problems.append("no <canvas> element — a freeform game must render to a canvas")
    elif s.canvas > 1:
        problems.append(f"expected exactly one <canvas>, found {s.canvas}")
    for ref in s.external:
        problems.append(f"external/remote resource is forbidden: {ref}")
    js = "\n".join(s.scripts)
    for label, pat in _EGRESS.items():
        if pat.search(js):
            problems.append(f"forbidden API in inline script: {label}")
    if "__smokeReady" not in js:
        problems.append(
            "missing the window.__smokeReady = true boot hook (set it once the "
            "first playable frame has rendered)"
        )
    return problems


def _sandbox_path(value: str) -> Path:
    root = Path(os.environ.get("FABRI_SANDBOX_ROOT", ".")).resolve()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes FABRI_SANDBOX_ROOT")
    return path


def main() -> None:
    args = json.loads(sys.stdin.read())
    html_path = args.get("html_path")
    try:
        path = _sandbox_path(html_path)
        if not path.is_file():
            print(json.dumps({"ok": False, "problems": [f"missing file: {html_path}"]}))
            raise SystemExit(1)
        problems = smoke(path.read_text(encoding="utf-8", errors="replace"))
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - never leak host paths
        print(json.dumps({
            "ok": False,
            "problems": [f"{type(exc).__name__} while verifying {html_path}"],
        }))
        raise SystemExit(1)
    print(json.dumps({"ok": not problems, "problems": problems}))
    raise SystemExit(0 if not problems else 1)


if __name__ == "__main__":
    main()

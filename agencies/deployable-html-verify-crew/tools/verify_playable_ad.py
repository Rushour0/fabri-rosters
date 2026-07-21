"""Tier-0 static boot-smoke for a self-contained playable-ad index.html.

A faithful port of ludexel-app engines/web/ludexel_web/smoke.py: pure-Python,
no browser, no Node — deterministic HTML/string checks plus a best-effort JS
syntax parse (via esprima if installed, degrading gracefully if not, exactly
like the sibling engine). This is a **Tier-0 static gate**, not proof the game
boots at runtime — the load-bearing containment in engines/web is the play
surface's opaque-origin sandbox + strict CSP, not this lint. A game that passes
here is *eligible* for the freeform genre; a real headless boot probe is Tier-1.

Standard fabri custom-tool contract: one JSON object on stdin, one JSON object
on stdout matching output_schema; paths are jailed to $FABRI_SANDBOX_ROOT and
the tool refuses to run without it.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

try:  # esprima is a light pure-Python dep; degrade gracefully if absent.
    import esprima  # type: ignore
except Exception:  # pragma: no cover - import guard
    esprima = None  # type: ignore

# Tokens that must never appear in a freeform game's inline JS. Over-matching
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

# ES2020+ operators esprima (ES2017) cannot parse; normalized before the syntax
# check so a valid modern game is never falsely rejected.
_OPTIONAL_CHAIN = re.compile(r"\?\.")
_NULLISH = re.compile(r"\?\?")
_OPTIONAL_CATCH = re.compile(r"\bcatch\s*\{")


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


def _normalize_modern_js(src: str) -> str:
    src = _OPTIONAL_CHAIN.sub(".", src)
    src = _NULLISH.sub("||", src)
    src = _OPTIONAL_CATCH.sub("catch (e) {", src)
    return src


def _syntax_errors(scripts: list[str]) -> list[str]:
    """Best-effort syntax faults that survive ES2020->ES2017 normalization."""
    if esprima is None:
        return []
    problems: list[str] = []
    for idx, src in enumerate(scripts):
        if not src.strip():
            continue
        try:
            esprima.parseScript(src)
            continue
        except Exception:
            pass
        try:
            esprima.parseScript(_normalize_modern_js(src))
        except Exception as exc:  # real syntax fault
            problems.append(
                f"inline <script> #{idx + 1} has a JavaScript syntax error: {str(exc)[:160]}"
            )
    return problems


def smoke(html: str) -> list[str]:
    """Return blocking problems (empty == the game passes the Tier-0 gate)."""
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
    problems.extend(_syntax_errors(s.scripts))
    return problems


def _sandbox_root() -> Path:
    root = os.environ.get("FABRI_SANDBOX_ROOT")
    if not root:
        raise ValueError("FABRI_SANDBOX_ROOT is not set")
    return Path(root).resolve()


def _sandbox_path(value: str) -> Path:
    root = _sandbox_root()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes FABRI_SANDBOX_ROOT")
    return path


def _run(args: dict) -> tuple[bool, list[str]]:
    html_path = args.get("html_path")
    if not isinstance(html_path, str) or not html_path:
        return False, ["html_path must be a non-empty string"]
    path = _sandbox_path(html_path)
    if not path.is_file():
        return False, [f"missing file: {html_path}"]
    if path.stat().st_size > _MAX:  # refuse oversized files before reading them
        return False, ["index.html exceeds the size cap"]
    problems = smoke(path.read_text(encoding="utf-8", errors="replace"))
    return not problems, problems


def main() -> None:
    args_repr = "<stdin>"
    try:
        args = json.loads(sys.stdin.read())
        if not isinstance(args, dict):
            raise ValueError("tool input must be a JSON object")
        args_repr = str(args.get("html_path"))
        ok, problems = _run(args)
    except Exception as exc:  # noqa: BLE001 - never leak host paths / tracebacks
        print(json.dumps({"ok": False, "problems": [f"{type(exc).__name__} while verifying {args_repr}"]}))
        raise SystemExit(1)
    print(json.dumps({"ok": ok, "problems": problems}))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()

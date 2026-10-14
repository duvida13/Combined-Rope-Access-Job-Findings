#!/usr/bin/env python3
"""Reject status/classification contradictions in an incremental findings file."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
LINK_RE = re.compile(r"\]\((https?://[^)]+)\)")
COUNT_RE = re.compile(r"\((\d+)\)\s*$")
CLOSURE_RE = re.compile(
    r"(?:reported|status:)\s*(?:closed|expired|withdrawn|removed|invalid)"
    r"|http\s*(?:404|410)",
    re.IGNORECASE,
)


def normalize_url(raw: str) -> str:
    parts = urlsplit(raw.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if parts.port:
        host = f"{host}:{parts.port}"
    query = urlencode(
        [
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
        ]
    )
    return urlunsplit(("https", host, parts.path.rstrip("/") or "/", query, ""))


def section_kind(heading: str) -> str | None:
    value = heading.lower()
    if value.startswith("new findings"):
        return "new"
    if value.startswith("previously listed findings"):
        return "rechecked"
    if value.startswith("source-reported closures"):
        return "closures"
    if value.startswith("source-reported reopenings"):
        return "reopenings"
    return None


def validate_text(text: str) -> list[str]:
    sections: dict[str, list[tuple[str, str]]] = defaultdict(list)
    declared_counts: dict[str, int] = {}
    current: str | None = None

    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            current = section_kind(heading)
            if current and (match := COUNT_RE.search(heading)):
                declared_counts[current] = int(match.group(1))
            continue
        if not current or not line.startswith("- ["):
            continue
        match = LINK_RE.search(line)
        if match:
            sections[current].append((normalize_url(match.group(1)), line))

    errors: list[str] = []
    active = {url for kind in ("new", "rechecked") for url, _ in sections[kind]}
    closures = {url for url, _ in sections["closures"]}
    for url in sorted(active & closures):
        errors.append(f"URL appears as both opportunity and closure: {url}")

    for kind in ("new", "rechecked"):
        for url, line in sections[kind]:
            if CLOSURE_RE.search(line):
                errors.append(f"Closure status appears in {kind} section: {url}")

    for url, line in sections["rechecked"]:
        if "current source status:" not in line.lower():
            errors.append(f"Rechecked finding omits current source status: {url}")

    for kind, expected in declared_counts.items():
        actual = len(sections[kind])
        if actual != expected:
            errors.append(f"{kind} heading declares {expected} links but contains {actual}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_merge_status.py MERGE_FINDINGS.md", file=sys.stderr)
        return 2
    argument = sys.argv[1]
    if argument == "-":
        text = sys.stdin.read()
        label = "stdin"
    else:
        path = Path(argument)
        if not path.is_file():
            print(f"not a file: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
        label = str(path)
    errors = validate_text(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"status classification valid: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

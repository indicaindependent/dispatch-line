#!/usr/bin/env python3
"""The Dispatch Line — deterministic format gate (public reference implementation).
Pure Python, no dependencies. Fails closed: returns (False, [reasons]) on any violation.

Usage:
    from validator import validate
    ok, errors = validate(text, concept="THE EXAMPLE CONCEPT")

Or from the CLI:
    echo "🟥 THE EXAMPLE ..." | python3 validator.py --concept "THE EXAMPLE"
"""
import re, sys, argparse

SQUARES = {"🟥", "🟦", "🟩", "🟧", "🟨", "🟪", "🟫", "⬛", "⬜"}
BANNED = [
    "follow for more", "follow me", "subscribe", "link in bio",
    "retweet", "new version", "stop what you're doing", "buy me", "donate",
]
OUTLETS = r"(Reuters|AP|AFP|Al Jazeera|Bloomberg|CNN|BBC|CNBC|Guardian|NYT|WSJ)"

def validate(text, concept=None, min_chars=200, max_chars=300):
    """Return (ok, errors[]). Enforces the Dispatch Line format rules."""
    e = []
    t = (text or "").strip()
    if not t:
        return False, ["empty text"]

    n = len(t)
    if n > max_chars:
        e.append(f"over {max_chars} chars ({n})")
    if n < min_chars:
        e.append(f"under {min_chars} chars ({n}) — use the whole budget")

    # opens with a topic color-square
    if not any(t.startswith(sq) for sq in SQUARES):
        e.append("must open with a topic color-square")

    # ALL-CAPS named concept in the headline line
    head = t.split("\n", 1)[0]
    if not re.search(r"\b[A-Z][A-Z0-9 ]{4,40}\b", head):
        e.append("no ALL-CAPS named concept in the headline line")
    if concept and concept.upper() not in t.upper():
        e.append(f"declared concept '{concept}' not found in text")

    # never end on a question
    if t.rstrip().endswith("?"):
        e.append("must NOT end on a question mark")

    # no links / URLs (self-contained, no click-away)
    if "http://" in t or "https://" in t or re.search(r"\b\w+\.(com|app|io|net|org|uk)\b", t):
        e.append("no link/URL allowed (self-contained)")

    # bare receipts: no em-dash outlet tag, no inline "according to"
    if re.search(r"—\s*" + OUTLETS, t) or re.search(r"(according to|per)\s+" + OUTLETS, t, re.I):
        e.append("receipts must be bare (no outlet source tag / 'according to')")

    # hashtags: at most 2, clean PascalCase
    tags = re.findall(r"#\w+", t)
    if len(tags) > 2:
        e.append(f"max 2 hashtags ({len(tags)} found)")
    for tag in tags:
        if not re.match(r"#[A-Z][A-Za-z0-9]+$", tag):
            e.append(f"tag not clean PascalCase: {tag}")

    # banned phrases
    tl = t.lower()
    for b in BANNED:
        if b in tl:
            e.append(f"banned phrase: '{b}'")

    return (len(e) == 0, e)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept", default=None)
    ap.add_argument("--text", default=None, help="post text; if omitted, read stdin")
    a = ap.parse_args()
    txt = a.text if a.text is not None else sys.stdin.read()
    ok, errs = validate(txt, a.concept)
    print("PASS" if ok else "FAIL")
    for x in errs:
        print("  -", x)
    sys.exit(0 if ok else 1)

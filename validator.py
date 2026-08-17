#!/usr/bin/env python3
"""The Dispatch Line — deterministic format gate (public reference implementation).
Pure Python, no dependencies. Fails closed: returns (False, [reasons]) on any violation.

FORMAT NOTE (v2, corrected): the Dispatch Line is PROSE-FIRST. An earlier version
required a leading colored square + an ALL-CAPS "named concept" opener. Re-analysis of
real standalone-post ("root") engagement data plus current Bluesky ranking behavior showed
that styling actively HURTS a standalone post's reach: prose openers roughly doubled the
likes of emoji+CAPS openers. Bluesky's feed is conversation/engagement-velocity driven and
discounts broadcast/engagement-bait styling. So this validator now BANS the leading square
and the ALL-CAPS shout opener, and rewards a natural prose lede.

Usage:
    from validator import validate
    ok, errors = validate(text, concept="the refinery war")

CLI:
    echo "Ukraine has stopped fighting for territory..." | python3 validator.py --concept "the refinery war"
"""
import re, sys, argparse

SQUARES = {"🟥", "🟦", "🟩", "🟧", "🟨", "🟪", "🟫", "⬛", "⬜"}
BANNED = [
    "follow for more", "follow me", "subscribe", "link in bio",
    "retweet", "new version", "stop what you're doing", "buy me", "donate",
]
OUTLETS = r"(Reuters|AP|AFP|Al Jazeera|Bloomberg|CNN|BBC|CNBC|Guardian|NYT|WSJ)"

def validate(text, concept=None, min_chars=200, max_chars=300):
    """Return (ok, errors[]). Enforces the PROSE-FIRST Dispatch Line rules."""
    e = []
    t = (text or "").strip()
    if not t:
        return False, ["empty text"]

    n = len(t)
    if n > max_chars:
        e.append(f"over {max_chars} chars ({n})")
    if n < min_chars:
        e.append(f"under {min_chars} chars ({n}) — use the whole budget")

    # BAN the penalized broadcast opener: no leading colored square
    if any(t.startswith(sq) for sq in SQUARES):
        e.append("must NOT open with a colored square (prose-first; styling suppresses reach)")

    head = t.split("\n", 1)[0]
    # BAN an ALL-CAPS shout at the very start of the headline (the old gimmick)
    if re.match(r"^[\W]*[A-Z][A-Z0-9 ]{5,}\b", head):
        e.append("headline opens with an ALL-CAPS shout — write a natural prose lede instead")
    # must open with a real word (letter or quote), not an emoji/symbol
    if not re.match(r"[A-Za-z\"']", t):
        e.append("open with a word, not an emoji/symbol")

    # coined concept should still appear, woven into the prose (any case) — keeps the lexicon idea
    if concept:
        c = concept.strip()
        if c.lower().startswith("the "):
            c = c[4:]
        if c and c.lower() not in t.lower():
            e.append(f"coined concept '{concept}' not present in the post")

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

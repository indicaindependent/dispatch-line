# Architecture & Design

## Why single posts, and why prose-first
A study of one active account plus large single-post accounts found that self-contained text posts out-engaged click-away link cards. A follow-up correction (re-cutting the data on **roots/standalone posts only**) found that opening with a colored square + ALL-CAPS concept **reduced** engagement versus a plain prose lede — roughly halving likes. Bluesky's 2026 feed ranks on conversation + first-hour engagement velocity and discounts broadcast/engagement-bait styling. So the Dispatch Line is prose-first: a natural lede, a bare receipt, a sharp turn, and one coined concept woven in — no square, no shout.

## Components (swap in your own)
- **Catalyst source:** any research/news API for your beat. Prefer items < 48h old.
- **Compose model:** any capable instruction-following LLM. Feed it `prompt_spec.md` plus the day's catalyst.
- **Validator:** `validator.py` — pure-Python, no deps. Fails closed. Bans the square + shout opener.
- **Scheduler:** any poster that can publish to your account at a chosen time. Fire into your measured best window with jitter.
- **Datastore:** any table. Record the post, concept, topic, char count, and a next-day engagement snapshot.

## The self-tuning loop
Each day: source → compose → validate → schedule → log. A day later, snapshot engagement back onto the record. Over weeks, compare engagement by concept-type, topic, and time to bias future composition. Keep the tuner simple and never let it override the honesty guardrails.

## Guardrails
- **Live-data rule:** every claim/receipt looked up fresh at compose time.
- **No-fabrication:** the receipt must be a real, dated fact; if none exists, HOLD.
- **Human-in-the-loop first:** ship in draft-to-approval mode; earn autonomy.
- **Single target:** the scheduler is wired to one account only.

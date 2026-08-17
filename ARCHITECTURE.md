# Architecture & Design

## Why single posts
A study of one active account plus large single-post accounts found that self-contained text posts, opened with a colored-square + named concept and ended on a turn (not a question), consistently out-engaged both prose openers and click-away link cards. The Dispatch Line operationalizes that as a daily habit.

## Components (swap in your own)
- **Catalyst source:** any research/news API or feed for your beat. Prefer items < 48h old.
- **Compose model:** any capable instruction-following LLM. Feed it `prompt_spec.md` as the system instruction plus the day's catalyst.
- **Validator:** `validator.py` — pure-Python, no deps. Fails closed.
- **Scheduler:** any poster that can publish to your account at a chosen time. Fire into your measured best window (find it with the study method) with ±minutes jitter.
- **Datastore:** any table/collection. Record the post, concept name, topic, char count, and a next-day engagement snapshot.

## The self-tuning loop
Each day: source → compose → validate → schedule → log. A day later, snapshot the post's engagement back onto its record. Over weeks, compare engagement by concept-type, topic, square, and time to bias future composition. Keep it simple and auditable; do not let the tuner override the honesty guardrails.

## Guardrails
- **Live-data rule:** every claim/receipt is looked up fresh at compose time.
- **No-fabrication:** the receipt must be a real, dated fact; if none exists, HOLD.
- **Human-in-the-loop first:** ship in draft-to-approval mode; earn autonomy.
- **Single target:** the scheduler is wired to one account only.

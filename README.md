# The Dispatch Line 📮

**An autonomous "one great post a day" system for Bluesky — a daily, self-contained conversation-starter that coins a named concept, built on measured engagement data.**

![license](https://img.shields.io/badge/license-MIT-blue) ![type](https://img.shields.io/badge/type-architecture-purple) ![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

This repo is the **generic, public architecture** for a system that composes and schedules one high-quality standalone post per day into your best engagement window. It grew out of a data study (see the companion *bluesky-engagement-study* repo) and is written so you can adapt it to your own stack.

> It is a reference architecture + a runnable skeleton — not a turnkey bot. You wire it to your own compose model, scheduler, and datastore.

## The idea
Most automated posting is either link-dumps or threads. The Dispatch Line does one thing well: **each day, publish a single, complete, provocative statement that names a concept** — a repeatable mental handle for something happening in your beat. Over time your account becomes the one that gives people *language* for a topic. That lexicon is the moat.

## The post format
```
🟥 THE <NAMED CONCEPT IN CAPS>

<one self-contained present-tense claim: named actor + verb + stakes>

<one bare receipt line — the detail that proves it is real>

<the TURN — the implication/contradiction that makes people weigh in>
```
Design rules (all data-backed — see the study repo):
- Open with a **topic-mapped colored square + an ALL-CAPS named concept**.
- Make one **self-contained** claim; no link-card, no click-away.
- Ground it in **one real, dated receipt** (never fabricate).
- End on a **turn**, never a question mark.
- Use most of the **character budget** (~240–298).
- Coin **one named concept per day**.

## Architecture
```
 catalyst source ──▶ compose ──▶ validate ──▶ schedule ──▶ log + 24h snapshot ──▶ self-tune
   (your research     (your LLM   (rules gate) (your        (datastore)          (learn which
    / news feed)       of choice)              scheduler)                         concepts land)
```
1. **Source** — pull the day's freshest item in your beat from whatever research/news feed you use.
2. **Compose** — an LLM writes the Dispatch Line to the format above, with the rules as hard constraints.
3. **Validate** — a light, deterministic gate (see `validator.py`) enforces every rule before anything can post.
4. **Schedule** — hand the validated text to your scheduler; fire into your measured best window with a little time-jitter so it isn't robotic.
5. **Log + learn** — record the post, its concept name, and a next-day engagement snapshot; use it to learn which concept-types land.

## What's in here
- [`validator.py`](validator.py) — the deterministic format gate (runnable, dependency-free).
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — the full design + guardrails.
- [`prompt_spec.md`](prompt_spec.md) — the compose-model instruction spec.
- [`schema.example.json`](schema.example.json) — a suggested log-record shape.

## Guardrails (do not skip)
- **Look every fact up live.** Never post a stale or assumed claim.
- **Never fabricate the receipt.** If there is no clean, fresh catalyst, **hold** and notify yourself — do not post filler. Honesty is the brand.
- **Draft-to-approval first.** Run in review mode for a week before going autonomous.
- **One target account.** Wire it to fire to exactly one account, by design.

## License
MIT — see [LICENSE](LICENSE).

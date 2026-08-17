# The Dispatch Line 📮

**An autonomous "one great post a day" system for Bluesky — a daily, self-contained, prose-first conversation-starter that coins a named concept, built on measured engagement data.**

![license](https://img.shields.io/badge/license-MIT-blue) ![type](https://img.shields.io/badge/type-architecture-purple) ![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

This repo is the **generic, public architecture** for a system that composes and schedules one high-quality standalone post per day into your best engagement window. It grew out of a data study (see the companion *bluesky-engagement-study* repo) and is written so you can adapt it to your own stack.

> Reference architecture + a runnable skeleton — not a turnkey bot. You wire it to your own compose model, scheduler, and datastore.

## The idea
Most automated posting is link-dumps or threads. The Dispatch Line does one thing well: **each day, publish a single, complete, provocative statement that names a concept** — a repeatable mental handle for something happening in your beat. Over time your account becomes the one that gives people *language* for a topic. That lexicon is the moat.

## The post format — PROSE-FIRST
> **Design note (v2, corrected):** an earlier version of this project opened each post with a colored square and an ALL-CAPS "named concept" headline. Re-analysis of real **standalone-post** engagement data — plus how Bluesky's feed actually ranks in 2026 — showed that styling **hurts** a standalone post: plain prose openers roughly **doubled** the likes of emoji+CAPS openers. Bluesky's Discover feed is conversation/engagement-velocity driven and discounts broadcast/engagement-bait styling. So the format is now prose-first: **no leading square, no shout headline.** (The old finding was a confound — it came from *in-thread replies*, which win on content + thread context, not formatting.)

Write it as natural prose:
1. **A prose lede** — a named actor + present-tense verb + the stakes, in one breath, weaving in one coined concept naturally (e.g. *"…call it the refinery war."*).
2. **One bare receipt** — a real, dated detail that proves it's real. No source tag, no "according to X".
3. **The turn** — a sharp implication or contradiction that makes people react. Never a question mark.
4. Optional: ≤2 clean PascalCase hashtags.

Example:
> Ukraine has stopped fighting for territory and started fighting for fuel — call it the refinery war. Six hundred drones hit Russia in a single wave this week, and the Orsk refinery is still burning. The front line isn't a line anymore. It's a supply chain, and Kyiv just proved it can cut it.

## Architecture
```
 catalyst source ──▶ compose ──▶ validate ──▶ schedule ──▶ log + 24h snapshot ──▶ self-tune
   (your research     (your LLM   (rules gate) (your        (datastore)          (learn which
    / news feed)       of choice)              scheduler)                         concepts land)
```
1. **Source** — pull the day's freshest item in your beat.
2. **Compose** — an LLM writes the Dispatch Line to the prose-first format, with the rules as hard constraints.
3. **Validate** — a deterministic gate (see `validator.py`) enforces every rule before anything can post (bans the square + shout opener, requires the concept, no "?" ending, full budget, bare receipts).
4. **Schedule** — fire into your measured best window with a little time-jitter.
5. **Log + learn** — record the post, its concept, and a next-day engagement snapshot; learn which concept-types land.

## What's in here
- [`validator.py`](validator.py) — the deterministic prose-first gate (runnable, dependency-free).
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — the full design + guardrails.
- [`prompt_spec.md`](prompt_spec.md) — the compose-model instruction spec.
- [`schema.example.json`](schema.example.json) — a suggested log-record shape.

## Guardrails (do not skip)
- **Look every fact up live.** Never post a stale or assumed claim.
- **Never fabricate the receipt.** No clean fresh catalyst → **hold**, don't post filler. Honesty is the brand.
- **Draft-to-approval first.** Run in review mode for a week before going autonomous.
- **One target account.** Wire it to fire to exactly one account, by design.

## Lesson baked in
Never generalize an *in-thread reply* finding to a *standalone post*. Re-cut the data on the same post type you're designing for — formatting that helps a reply survive inside a thread can suppress a standalone post's reach.

## License
MIT — see [LICENSE](LICENSE).

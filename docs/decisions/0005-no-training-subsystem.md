# 0005 — No practice/film/training subsystem

**Status:** accepted · 2026-08-12

## Context

Low-minute players are one of the five problems this project exists to fix. A
bench player earns few counting stats, therefore little XP, therefore never
improves enough to earn minutes — a dead end that makes the whole mode unplayable
outside a starting role.

The obvious fix is an alternative income source: practice sessions, film study,
training drills. Something you *do* between games that pays out. Sports RPGs
generally have one.

## Decision

**No practice, film, or training subsystem.** No sessions to schedule, no drills
to allocate, no between-game activity loop.

The intent is met by two thin mechanisms instead:

1. **Expectation-relative scoring** — production is measured against what a
   player of your rating, position, and minutes *should* produce, so six points
   in eight minutes can beat fourteen in thirty-four. Opportunity largely
   normalizes out, which is the actual root of the problem.
2. **A baseline XP floor keyed to minutes** — full at garbage-time minutes,
   decaying smoothly toward zero at starter minutes. The decay must be **smooth,
   not a threshold**: a cutoff at twenty minutes means nineteen and twenty-one
   produce an earnings cliff, which is arbitrary and invites gaming.

## Consequences

**Buys:** the low-minute problem is solved by the scoring model rather than by a
parallel system with its own UI, its own balance surface, and its own way to be
gamed. Two mechanisms instead of a subsystem.

**Costs:** there is no *activity* between games — the only thing you do is play
and record. For a player who wanted a management layer, this project will feel
thin. That is a deliberate trade and it may prove wrong.

**Forecloses:** any mechanic where the player allocates effort off-court. If that
turns out to be the missing texture, this ADR gets superseded rather than
quietly worked around.

## The offseason carve-out

[`ROADMAP.md`](../../ROADMAP.md) Phase 4 includes an **offseason training block**
that pays out currency between seasons. This ADR does **not** prohibit it, and the
distinction is load-bearing rather than a convenient reading:

| Rejected here | The offseason block |
|---|---|
| Repeatable, in-season | Once per season, at the boundary |
| An activity loop with allocation decisions | A ceremony with a payout |
| A parallel income stream competing with games | A punctuation mark between them |
| Adds a UI surface you return to constantly | Adds a screen you see once a year |

What was rejected is *machinery* — an ongoing system to interact with. A
once-a-year payout is not that. If the offseason block ever grows drill selection,
effort allocation, or anything you optimize, it has become the thing this ADR
rejected and needs a superseding decision.

## Alternatives considered

**A full training subsystem.** Rejected as too much machinery for the problem —
and it addresses the symptom (low income) rather than the cause (income tracks
opportunity rather than performance).

**A flat XP-per-game floor, regardless of minutes.** Simpler than the decaying
floor. Rejected because it pays a starter the same bonus as a benchwarmer, so it
either matters too much at the top or too little at the bottom.

**Nothing at all — let expectation-relative scoring carry it alone.** Tempting,
and it may prove sufficient. The floor is kept because a player with three
minutes has a sample too small for expectation to say anything meaningful about,
and zero is a bad answer to that.

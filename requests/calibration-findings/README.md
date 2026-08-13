# Calibration Findings

Everything ran green and the **economy is wrong**.

No crash, no failing test, no corrupt ledger. The fold replays, the prices
compute, the worksheet renders — and the career it produced doesn't look like a
career. Progression too fast or too slow. An archetype that turned out to be
flavour text. A build that converged to uniform anyway. A bench player with no
path out.

This is the track that makes **P4** operational. `GAME_DESIGN.md` claims the
economy is falsifiable — calibrated against real player development rather than
tuned by taste. A claim like that needs somewhere for the falsifications to land.

> **Not a bug.** If something *failed*, it belongs in
> [`../bugfix-requests/`](../bugfix-requests/). Tie-break: **did anything fail?**
> Green run + implausible career = here.

## Why this track exists separately

A code bug has one right answer. A calibration finding usually has four
candidates, and picking the wrong one makes things worse:

| Candidate | Symptom it explains |
|---|---|
| **Expectation model** too easy or too hard to beat | Income wrong across the board, at every rating |
| **Cost curve** too shallow or too steep | Income fine, but the same XP buys too much or too little |
| **Affinity table** not biting | Builds converge; the archetype pick doesn't change the destination |
| **Milestone windfalls** doing too much work | The curve is fine between milestones and jumps at them |

A finding that jumps to "make XP smaller" without distinguishing these will fix
the number and break the shape. The diagnosis step exists to separate them.

## What a finding owes

**Evidence, not vibes.** A finding needs the career that produced it — the slug,
the seasons, the ruleset version live at the time — plus the comparison that made
it look wrong. "This feels fast" is a legitimate *report*; the finding it becomes
has to name what it's fast relative to.

**A replay plan.** This is the obligation that makes the track distinct. Careers
already played were played under the old ruleset, so every fix has to answer:

- Which ruleset version does this change, and does it become a **new version** or
  amend an unreleased one?
- Which careers replay, and does replaying shift a player's recorded history
  underneath them?
- If history does shift, is that acceptable, or does the old ruleset stay pinned
  for existing careers and the change apply only to new ones?

Both answers are legitimate. Choosing silently is not. This is precisely the
capability event sourcing was adopted for (ADR 0003) — a finding here is the
system working, not failing.

## The pipeline

| # | Stage | Skill | Produces |
|---|---|---|---|
| 1 | **Intake** | `/make-bugfix-request` (reused) | `CALIBRATION_FINDING.md` — the career, the comparison, the suspicion |
| 2 | **Diagnose** | `/diagnose-bug` (reused) | `ROOT_CAUSE_ANALYSIS.md` — which of the four candidates, with the others refuted |
| 3–4 | **Plan + Implement** | `/create-implementation-plan` → `/implement-plan` | Shared back half, plus the replay plan |

The front-half skills are reused rather than duplicated; the artifacts differ,
the panels don't.

## Definition of done

**The finding is reproduced as a fixture, the ruleset changes, and a replay
proves the new shape.**

A calibration fix without a pinned fixture is a tuning session. The fixture is a
career — real or synthetic — whose trajectory is asserted, so the next retune
can't silently undo this one.

## Layout

```
calibration-findings/
  <slug>/
    CALIBRATION_FINDING.md     # stage 1
    ROOT_CAUSE_ANALYSIS.md     # stage 2
    IMPLEMENTATION_PLAN.md     # stage 3 — includes the replay plan
    IMPLEMENTATION_REPORT.md   # stage 4
    reviews/
  _done/<slug>/
```

**Status grammar:** `intake` → `diagnosed` → `planned` → `retuned`

## Index

| Finding | Stage | Notes |
|---|---|---|
| _(none yet — nothing to calibrate until Phase 2)_ | | |

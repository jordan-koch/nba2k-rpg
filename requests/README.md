# Requests

The project's work intake — three parallel tracks under one inbox. Every
substantial change enters here.

| Track | For | Start with |
|---|---|---|
| **[feature-requests/](feature-requests/)** | New capability — an engine mechanic, an app surface, a dataset, a skill | `/make-feature-request` |
| **[bugfix-requests/](bugfix-requests/)** | A defect in existing code, config, or tooling | `/make-bugfix-request` |
| **[calibration-findings/](calibration-findings/)** | Everything ran green and the **economy is wrong** | see that track's README |

**Not every question is a request.** A *decision* you would rather park than
answer now belongs in [ESCALATIONS.md](../ESCALATIONS.md), recorded against the
moment that reopens it. Parking blocks nothing and starts no track.

Each track's **README is the contract** — layout, status grammar, the live Index,
and the `_done/` archive convention. The back half
(`/create-implementation-plan` → `/implement-plan`) is shared and auto-detects
the track from the artifact's path.

## Why three tracks and not two

A code defect and an economy defect look similar and triage completely
differently.

A career that reaches 90 OVR in two seasons is not a crash. The code did exactly
what it was told; the ledger replays; every test is green. The question is *which*
of several things is wrong: the **expectation model** is too easy to beat, the
**cost curve** is too shallow, the **affinity table** doesn't bite, or the
**milestone windfalls** are doing more work than intended. Each has a different
investigation and a different fix.

Calibration findings also carry a second obligation a code bug doesn't: **fixing
forward is only half the work.** The careers already played were played under the
old ruleset. Every finding owes a **replay plan** alongside the fix — which
ruleset version changes, which careers replay, and whether a player's recorded
history shifts underneath them.

See [calibration-findings/README.md](calibration-findings/README.md).

## Principles

Two rules run through every panel in every track:

- **Greedy, but gated.** Agents propose *everything* — generating options is
  cheap, so be ambitious. Scope-growing or expensive ideas get **tiered and
  deferred for your decision**, never silently folded into the build.
- **Generate → converge → triage → you decide.** Adversarial agents record *all*
  findings with severity and confidence and never self-censor. The merge step
  builds the convergence map and surfaces the gated calls. **You** dispose them —
  the panel proposes, you decide.

And one that matters more here than in a typical repo:

- **Label your epistemics.** *Measured*, *verified*, *inferred*, *assumed*,
  *unconfirmed* are different words and mean different things. Much of this
  project rests on beliefs about a game's file formats and a league's
  statistics — a request that says "2K ratings history is available by season"
  when nobody has checked is a liability. Say `unconfirmed` and it becomes a task.

## Weight — the panel is the default

Not every change needs every stage. But **which changes don't is decided here,
against a written request — never in advance.**
[ADR 0010](../docs/decisions/0010-panels-by-default.md) settles this: the roadmap
used to pre-register ceremony with a ★ and a size estimate, both guessed before
the work existed. They're gone.

> **The full pipeline runs unless a skip is argued in writing.** The burden of
> proof is on the cheap path.

**Entry.** This governs work that gets a request at all. Typo fixes, dependency
bumps, and doc edits never enter the pipeline — `/commit` has a "maps to no
roadmap row" path for those.

**Three hard triggers. Any one and the panel runs; no argument is available:**

| | Trigger | Why it's disqualifying |
|---|---|---|
| 1 | Intake's **Open Questions** came out non-empty | That *is* a blurry edge, and it's mechanical — the agent already wrote it down |
| 2 | **Explicitly out** couldn't be filled | Intake already treats an empty one as "interview more". Still empty means the edges aren't known |
| 3 | It touches something **expensive to reverse** | A settled ADR, a pillar, the event schema, a dataset contract, or anything another roadmap item pins |

Clear all three and a skip becomes *available* — at the cost of a written
argument in the request's closing **Stage plan** section, naming which triggers it
cleared. That section is what gets surfaced to the user at the intake handoff,
which is already human-gated, so nothing new interrupts.

**Skipping doesn't mean shipping unreviewed.** `/implement-plan` has a
direct-build mode that takes the intake artifact in place of a plan. Its
adversarial reviewers were never plan-bound — the roster is derived from what the
diff touched — so they run at full strength. A small change spawns a small panel
on its own; there is no trim lever and deliberately shouldn't be.

What a skip genuinely forfeits is **verification by execution against numbered
acceptance criteria**, because a skipped item never wrote any. That is the
content of the decision, not a gap in it — an item that needs numbered criteria
trips trigger 1.

See [CLAUDE.md](../CLAUDE.md) for where this sits in the repo.

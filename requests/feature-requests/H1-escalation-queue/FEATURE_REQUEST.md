> **Status:** scoped · created 2026-08-15 · decided · next: plan

# Feature Request — Escalation Queue (Harness H1)

## Problem / Motivation

**Decisions arrive in the middle of building, and there is nowhere to put one.**

Item 1.1 `app-shell` surfaced this as the project's real constraint — not build speed.
Eight decisions arrived synchronously in one sitting, each one stopping work until it was
answered. The cost isn't the deciding; it's that deciding and building are welded together, so
progress is hostage to whoever is available to answer, and the answers get made in whatever
order the build happens to hit them rather than when the evidence is best.

The failure has a quieter half. A worker facing a judgment call today has exactly two moves:
**interrupt**, or **guess silently**. There is no third option, and the second leaves no trace —
a decision made by default looks identical to a decision nobody noticed was there. Nothing in
the repo records "I picked A over B here, and I wasn't sure."

This already has a concrete instance sitting in prose.
[`ROADMAP.md`](../../../ROADMAP.md) parks three hypotheses — a serviceability gate for the web
UI, a design/UX specialist, and an autonomous stage dispatcher — in a paragraph under
*"Parked, not scheduled"*, each said to have "a named moment to re-decide". A paragraph is not a
queue: nothing will surface them at the moment they matter, and the named moments are named only
in the prose describing them.

## Desired Outcome

A parked decision can be recorded instead of asked, and it comes back at the moment it bears on
the work.

Concretely, when the user picks up a roadmap item, one place tells them which parked decisions
touch that item. A worker who hits a judgment call mid-build writes it down, states what it
assumed, and keeps going — so the assumption is visible rather than silent, and the user reads
it on their own schedule rather than the build's. The three hypotheses currently in `ROADMAP.md`
prose live there instead of in a paragraph.

The observable signal: item 1.3 can start by reading the queue and learning what was parked
against it, and a decision the user has not yet made is no longer a reason for anything to stop.

## Rough Ideas (non-binding)

`ROADMAP.md`'s H1 row names three deliverables: an `ESCALATIONS.md`, the parked-decision format,
and a structural test that every entry names a real roadmap item. Recorded as the roadmap's own
sketch, not as a spec — scoping is free to choose a different home, shape, or enforcement.

## Scope Signals

- **In:** the queue itself, its entry format, a structural test, and migrating the three
  hypotheses currently parked in `ROADMAP.md` prose into it.
- **Explicitly out:**
  - **Not a replacement for `[OPEN-N]`.** [`GAME_DESIGN.md`](../../../GAME_DESIGN.md) §8 parks
    ten design questions, already indexed by answering phase in `ROADMAP.md`'s closing table.
    That mechanism stays.
  - **Not a blocking mechanism.** Settled by the user during intake: parking never stops work.
    A queue that can halt a build has moved the interruption, not removed it.
  - **Not a priority or urgency system.** Settled by the user: the queue is drained at roadmap
    item boundaries, so the item id is the sort key and urgency has no job.
  - **Not a change to how the pipeline skills behave.** Whether anything *writes* to the queue
    automatically is genuinely open (below) — but no skill's decision logic changes here.
- **Not now / later:** anything that reads the queue programmatically; a resolved-entry archive
  if the file grows; entries that carry a decision's rationale rather than pointing at an ADR.

## Affected Area & Pointers

**Process and docs, not application code.** Nothing under `src/` or `app/` is touched. The
closest existing kin is the structural-test layer.

A cold scoping agent should open, in this order:

- [`ROADMAP.md`](../../../ROADMAP.md) — the H1 row and `Blocks: 1.3`; *"Why H1 exists"*; and
  *"Parked, not scheduled"*, which names the three seed entries.
- [`tests/test_repo_structure.py`](../../../tests/test_repo_structure.py) — the idiom the new
  test must match. `test_adr_numbers_are_unique_and_contiguous` and
  `test_every_adr_is_listed_in_the_index` are the closest analogues: both parse a document and
  assert it against the filesystem.
- [`tests/test_request_links.py`](../../../tests/test_request_links.py) — where the `_done/`
  exemption idiom comes from, if the queue ever needs one for resolved entries.
- [`GAME_DESIGN.md`](../../../GAME_DESIGN.md) §8 — the `[OPEN-N]` mechanism this must not
  duplicate.
- [`.claude/skills/diagnose-bug/SKILL.md`](../../../.claude/skills/diagnose-bug/SKILL.md) — its
  **Escalation** section is a name collision and a possible overlap: today that hand-off has
  nowhere to go once the RCA is written.
- [`docs/decisions/0010-panels-by-default.md`](../../../docs/decisions/0010-panels-by-default.md)
  — the **Stage plan** section it introduced is the other place a decision now gets recorded in
  this repo. The queue must not duplicate or contradict it.
- [`ops/README.md`](../../../ops/README.md) — for the *"inert until it is re-applied"* failure
  mode it already documents for `branch-protection.json`, which is the risk the wiring question
  below is really about.

## Constraints / Non-negotiables

- **The repo is public.** No machine-specific paths, ids, or personal identifiers.
- **Parking never blocks.** User-settled during intake.
- **Drained at item boundaries.** User-settled during intake. This has a consequence worth
  carrying into scoping: an entry that names no roadmap item would never surface under this
  cadence. That narrows open question 3 below — it does not settle it.
- **The structural test matches the existing idiom** in `tests/test_repo_structure.py`: parse a
  document, assert against the filesystem, fail with a message that explains the *why*.
- **`H1` blocks `1.3`**, per the roadmap. That cell is binding: 1.3 `correction-by-append` may
  not start until this lands.

## Open Questions for Scoping

1. **What does the queue hold?** Three candidate boundaries, and the choice is load-bearing
   because two other parking mechanisms already exist. Narrowest: build-time decisions only,
   leaving `[OPEN-N]` and `/diagnose-bug`'s Escalation where they are. Middle: also absorb the
   murky-cause hand-off, which today has no home. Widest: one index of every open question in
   the project, which would restructure `GAME_DESIGN.md` §8 and `ROADMAP.md`'s open-questions
   table.
2. **How far does the wiring go?** At the roadmap's literal three deliverables, *nothing writes
   to the queue* — which is the same shape as the inert-config failure `ops/README.md`
   documents. Options run from roadmap-literal, through adding a discoverability pointer in
   `CLAUDE.md` and `requests/README.md`, to teaching the pipeline skills to park their gated
   calls. The last is the real payoff and clearly the largest.
3. **Does the test hard-require a roadmap id, or allow an `unscheduled` escape hatch?**
   Hard-requiring forces every parked decision to have a named moment, which is the discipline
   the roadmap prose was reaching for. An escape hatch is more honest about genuinely unmoored
   questions but is the path of least resistance and will absorb entries. The item-boundary
   drain cadence argues for hard-requiring it; that is an argument, not a decision.

An adjacent question scoping may want to fold in or explicitly reject: whether a *resolved*
entry stays in the file with its resolution recorded (mirroring this repo's ADR-immutability
ethos) or is removed once decided.

## Stage plan

**Full pipeline.** Trigger 1 fired: Open Questions is non-empty, with three genuine design
questions whose answers change what gets built — in particular the boundary against two existing
mechanisms, which is expensive to get wrong because it would leave the project with two
overlapping places to look for a parked question.

Trigger 3 is arguable rather than clear: the entry format is pinned by every entry written after
it, and the roadmap makes this item binding on 1.3. Not relied on — trigger 1 is sufficient on
its own.

No skip is proposed.

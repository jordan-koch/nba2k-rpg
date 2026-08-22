# Bugfix Requests

Defects in existing code, config, or tooling — a builder that crashes, a broken
path resolution, a fold that drops an event, a CI workflow that passes when it
shouldn't, a skill that misfires.

> **Not for implausible careers.** If everything ran clean and the *economy* is
> wrong — progression too fast, an archetype that doesn't bite, a build that
> converges — that's
> [`../calibration-findings/`](../calibration-findings/): different triage,
> different artifacts, and it owes a replay plan this track doesn't. Tie-break:
> **did anything fail?** If it all went green and the career is still wrong, it's
> a calibration finding.

## The pipeline

| # | Stage | Skill | Produces |
|---|---|---|---|
| 1 | **Intake** | `/make-bugfix-request` | `BUGFIX_REQUEST.md` — symptom, reproduction, blast radius |
| 2 | **Diagnose** | `/diagnose-bug` | `ROOT_CAUSE_ANALYSIS.md` — a refute-the-diagnosis panel, not a confirm-it one |
| 3–4 | **Plan + Implement** | `/create-implementation-plan` → `/implement-plan` | Shared with the feature track |

Stages 3–4 are the feature track's back half, reused. They auto-detect the track
from the artifact's path.

**All four stages run by default** — [ADR 0010](../../docs/decisions/0010-panels-by-default.md).
Stage 3 is skippable only by an argument written into this request's closing
**Stage plan** section and cleared against the three hard triggers in
[`../README.md`](../README.md#weight--the-panel-is-the-default). Stage 2 has its
own funnel already: `/diagnose-bug` sizes its own ceremony against how murky the
cause turns out to be, which is the same principle applied at the moment the
evidence exists. Stage 4 always runs — with no plan to consume it enters
**direct-build mode**, taking the `ROOT_CAUSE_ANALYSIS.md` as intent.

## Definition of done

**A red reproduction goes green, and a regression test is left behind.**

Both halves are required. A fix without a test is an invitation to fix it again —
and in a repo where agents do most of the writing, the test is the only thing
that remembers.

The reproduction is written *first*, at diagnosis time, and it must **fail**
before the fix lands. A repro that passes against the broken code is not a repro;
it means the diagnosis is wrong. That red-to-green transition is the evidence,
and `/implement-plan` will ask for it.

Where the test lives depends on what broke:

| Broke | Test goes |
|---|---|
| The domain core — ledger, fold, economy, rulesets | `tests/` (pytest, against committed fixtures) |
| The API | `tests/` — a request/response test against the app |
| The web app | A component or end-to-end test alongside it |
| A dataset builder | `tests/` against a cached fixture, never a live pull |
| An assumption about an upstream source | A test on the *contract*, so the next upstream change fails loudly |
| CI or workflow config | A structural assertion in `tests/test_repo_structure.py` |

## A note on ledger bugs

A defect in the fold or in an event schema is the highest-severity class of bug
this project can have, because **the ledger has no upstream**. There is no
encrypted save to re-ingest from and no API to re-pull. If a bug corrupts
`careers/*/events.jsonl`, the career is gone.

Two consequences for triage:

1. **Never repair by rewriting history.** A fix that edits recorded events is not
   a fix, it's a second incident. Corrections are appends (ADR 0003).
2. **Reproduce against a fixture, never against a live career.** Copy the events
   into `tests/fixtures/` and work there.

## Layout

```
bugfix-requests/
  <slug>/
    BUGFIX_REQUEST.md          # stage 1
    ROOT_CAUSE_ANALYSIS.md     # stage 2
    IMPLEMENTATION_PLAN.md     # stage 3 (skipped when the fix is obvious)
    IMPLEMENTATION_REPORT.md   # stage 4
    reviews/                   # panel working files
  _done/<slug>/                # archived at terminal stage
```

**Status grammar:** `intake` → `diagnosed` → `planned` → `fixed`

A skipped stage skips its status, and the absent artifact is the record that it
did. The **Stage plan** section carries the argument.

Same active-vs-done convention as the feature track: one move into `_done/` at
the terminal stage, Index row stays with its link updated.

## Index

| Bug | Stage | Notes |
|---|---|---|
| [pipeline-status-rollover](pipeline-status-rollover/) | intake | Stage-3/4 skills leave sibling artifact statuses stale and write a token no grammar defines. Reds the build on every item reaching stage 3 |

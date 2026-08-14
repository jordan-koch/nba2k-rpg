# Feature Requests

Home for every substantial new piece of work — an engine mechanic, an app
surface, a dataset builder, a skill. The point is a **light, repeatable set of
guardrails** around how an idea travels from *"I want X"* to *"a cold agent can
implement X"* — without turning a one-hour change into a week of process.

> **Bugs go elsewhere.** A **defect** in existing code has its own track
> ([`../bugfix-requests/`](../bugfix-requests/)). An **economy that ran green and
> produced a wrong career** has a third
> ([`../calibration-findings/`](../calibration-findings/)). Tie-break: missing =
> feature, broken-that-exists = bug, ran-clean-but-implausible = calibration.

## The pipeline

| # | Stage | Skill | Produces | Shape |
|---|---|---|---|---|
| 1 | **Intake** | `/make-feature-request` | `FEATURE_REQUEST.md` | Interview — turns a raw idea into a scoped, repo-grounded request. Fast, single-agent. |
| 2 | **Scope** | `/scope-feature` | `PROJECT_SCOPE.md` | Panel: 3 divergent scopers → merge/converge → 2 adversarial. Settles fit + testable acceptance criteria. |
| 3 | **Plan** | `/create-implementation-plan` | `IMPLEMENTATION_PLAN.md` | Panel: 3 planners → merge → 2 code-grounded adversaries + 1 meta-audit. Cold-handoff plan. |
| 4 | **Implement** | `/implement-plan` | code + `IMPLEMENTATION_REPORT.md` | Panel: core reviewers + auto-scaled specialists → execution-based verify → meta-audit. Proves every acceptance criterion by running it. |

Each stage produces one artifact and is **human-gated** — you review and edit
before invoking the next. A tiny change might only need a request; a
well-understood one might jump straight to a plan.
[`ROADMAP.md`](../../ROADMAP.md) marks the items that earn the full panel with ★.

## Roadmap items are pre-scoped requests

Every row in `ROADMAP.md`'s phase tables is intended to become one directory
here and one feature branch. The roadmap already carries the deliverable, the
size, and the dependencies — intake starts from that rather than from nothing.

Use the roadmap id as the slug prefix where it helps: `1.2-career-ledger`.

## Every dataset comes from here

No source gets pulled and no dataset gets registered without a request behind it.
A dataset carries **contracts** — a grain, a set of keys, a freshness
expectation, an upstream that can change without warning — and those are
decisions, not implementation details.

A dataset request must settle, before any code:

- **Grain.** One row per *what*? "Player per game" and "player per team-stint per
  game" are different tables, and the difference is invisible until a mid-season
  trade breaks a join.
- **Keys.** What makes a row unique, and is that enforceable as a test?
- **Coverage.** Which seasons does this source actually have? Structurally-absent
  data is not missing data, and conflating them produces silently wrong averages.
- **Update semantics.** Append-only, or does history get restated?
- **Cost.** How many requests for a full pull, at what pacing, over what
  wall-clock? What gets cached in `var/cache/` so a re-run is free?
- **Registration.** The logical name it takes in `datasets/manifest.json`.
  Consumers resolve by name; nothing hardcodes a path.

## Acceptance criteria

"Testable" has a specific meaning here. A criterion is testable when a **cold
agent can run one command and get a pass or fail** — not when a human can eyeball
a number and nod.

- ✅ *`pytest tests/test_replay.py` is green: folding `events.jsonl` twice
  produces byte-identical state.*
- ✅ *A career recorded under ruleset `v1` replays under `v2` with no migration
  step — `pytest -m replay` proves it.*
- ✅ *`rpg_core.economy.price()` returns the same value for a 7'0" playmaker's
  ball handling as the pinned fixture in `tests/fixtures/affinity.json`.*
- ❌ *The XP numbers feel about right.*

Criteria that only a human can prove — whether a career *feels* distinct, whether
82 games of entry is tolerable — are legitimate and central to this project, but
must be **marked user-run** so the acceptance panel doesn't claim them.

## Layout

The directory **is** the unit of work:

```
feature-requests/
  <slug>/                      # kebab-case (e.g. 1.2-career-ledger)
    FEATURE_REQUEST.md         # stage 1
    PROJECT_SCOPE.md           # stage 2
    IMPLEMENTATION_PLAN.md     # stage 3
    IMPLEMENTATION_REPORT.md   # stage 4 — acceptance ledger + what shipped
    reviews/                   # panel working files — the provenance trail
  _done/<slug>/                # archived once it reaches a terminal stage
```

**Active-vs-done.** An item lives at the track root while in flight; when it
reaches the terminal stage — `implemented` — it moves **once** into `_done/`.
That single move is the only lifecycle action, so a plain `ls feature-requests/`
shows only active work. The Index keeps the row with its link pointing into
`_done/`.

Every artifact opens with a status blockquote:

> **Status:** &lt;stage&gt; · created &lt;YYYY-MM-DD&gt; · &lt;open | decided&gt; · next: &lt;stage or "implement"&gt;

**Status grammar:** `intake` → `scoped` → `planned` → `implemented`

## Index

| Feature | Stage | Notes |
|---|---|---|
| [1.1-app-shell](1.1-app-shell/) | planned | Roadmap 1.1. FastAPI + React/Vite seam, health endpoint, frontend CI job. Unblocks the rest of Phase 1 |

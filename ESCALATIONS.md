# Escalations

A place to **park a decision instead of interrupting**.

A worker who hits a judgment call mid-build has two moves, and both are bad. Interrupt — which
is the synchronous tax [ROADMAP.md](ROADMAP.md)'s H1 row exists to remove. Or guess silently —
which leaves no trace at all, because a decision made by default is indistinguishable from one
nobody noticed was there.

This file is the third move: **record the question, name the moment it bears on, say what you
actually assumed, and keep going.** The assumption is the load-bearing part. Everything else in
this repo can record a question; nothing else records what someone did while the question stayed
open.

## What belongs here

A **decision with alternatives**, parked against a moment when the evidence to settle it will be
better than it is today.

Not a task, and not a backlog. The symptom of a wrong entry is an `Assumed:` field with no
plausible alternative — if there was only ever one thing to do, nothing was ever parked.

**No agent resolves an entry.** Agents park and read; disposition is the user's.

## The register map

This is the sixth place a question can be parked in this repo, so the boundary is the point.
Before adding an entry, check it doesn't belong to one of the five that came first:

| Register | What goes there | Why it isn't this |
|---|---|---|
| `GAME_DESIGN.md` §8 — `[OPEN-N]` | Open questions about **the game's design**: what the economy should reward, whether a lever is needed at all | Numbered, cross-referenced from the design text, and indexed by the phase that answers them. Each gets a scoping panel with the loop in hand. **Cross-reference these; never migrate one here.** |
| `DESIGN.md` §2 — Open mechanism work | Unsettled **mechanism math** — the expectation model, shrinkage, the cost curve | Each subsection already names its phase and item, so it is a spec waiting to be written rather than a decision waiting to be made |
| `DESIGN.md` §4 — Open engineering questions | Engineering questions carrying **no id and no named moment** | **The sharpest overlap** — it is nearly what this file is, minus the discipline. Prefer an entry here when you can name the moment; leave it there when you genuinely cannot |
| ADR 0010 — a request's **Stage plan** | Which pipeline stages one *specific request* runs, and the argument for skipping any | Per-request ceremony, decided at intake and scoped to that item. It answers "how much process," never "what should this do" |
| `/diagnose-bug` — the **Escalation** section | A bug whose root cause came back murky, with the candidates weighed | **Blocking, and bug-scoped**: it ends with "this bug is NOT ready to plan." An entry here blocks nothing |

Nothing mechanical can tell a build-time decision from an engineering question. That is why this
map is prose at the point of use rather than a test — but see the guard note below for the half
that *is* mechanical.

**On the word "escalation."** It now means two things in this repo. `/diagnose-bug`'s Escalation
is **blocking and bug-scoped** — a murky cause that stops the bug reaching the plan stage. An
entry in this file is **non-blocking and moment-scoped**. Two mechanisms, one index: a murky bug
should park an entry here naming the moment it bears on, and the bug still waits.

## Parking never blocks — and the file is not exempt from CI

Two different claims, and both hold:

- **No open entry ever stops anything.** It does not stop a stage, fail a build, gate a merge, or
  put an item into an error state. An open entry is a memory, not a gate. This is the one place
  the repo has where "I don't know yet" is a valid, recorded, permanent answer.
- **The file itself is ordinary tracked markdown.** A *malformed* entry fails
  `tests/test_escalations.py` exactly as malformed markdown fails any other guard. That is not a
  contradiction of the rule above: the guard fails on a broken **record**, never on an unanswered
  **question**.

**Contrast with `ROADMAP.md`'s `Blocks` cell**, which is the repo's real blocking mechanism: a
`Blocks` cell stops the named item from starting, and an entry in this file never does.

**Trigger for ADR 0011.** There is deliberately no ADR recording this boundary — the map above
carries it at the point of use, and the guard makes part of it mechanical. **The first time
someone proposes absorbing `[OPEN-N]` or `DESIGN.md` §4 into this file, that is the second
litigation, and ADR 0011 gets written then.**

## The entry format

Six required fields, and the guard checks every one. Change this shape and you change
`tests/test_escalations.py` in the same commit.

| Field | Rule |
|---|---|
| **id + title** | The heading. Id matches `E-NNN` and is unique across the file |
| **`Bears on:`** | **Required, and must resolve** — a roadmap item id (`1.3`, `H2`), a phase name (`Phase 3`), or `post-v1`. **The moment alone: nothing else on the line, and no backticks** — commentary belongs in the body. There is no `unscheduled` hatch: an entry nothing will ever reopen is invisible, and the two registers above exist for a genuinely unmoored question |
| **`Parked:`** | The date the entry entered *this file*, `YYYY-MM-DD`. Where it originally surfaced is `Source:` |
| **`Assumed:`** | What was **actually done** while the question stayed open — or the literal `none — not hit yet`. Label the epistemics: `measured` / `verified` / `inferred` / `assumed` / `unconfirmed` |
| **`Source:`** | Where it surfaced — a path, optionally `:line`. Written as code, not a link |
| **`Status:`** | `open` or `resolved`. Nothing else |

`Status:` is the single source of truth, and the section an entry sits in must agree with it —
`open` entries under `## Open`, `resolved` entries under `## Resolved`. A resolved entry **stays**,
with its resolution pointer written into the body rather than added as a seventh field.

Copy this. It parses green under the same guards as every real entry:

```markdown
### E-000 — Should a resolved entry ever be archived out of this file?

- **Bears on:** post-v1
- **Parked:** 2026-08-21
- **Assumed:** resolved entries stay in place — `inferred` from the immutability ethos in
  `docs/decisions/README.md`, and cheap to revisit while the file is short
- **Source:** `ESCALATIONS.md`
- **Status:** open

One short paragraph of context. What the alternatives are, and what would make the answer
obvious later — not the rationale for a decision, which belongs in the artifact that records it.
```

**E-000 is a template, never a parked decision.** It bears on `post-v1` deliberately, so that a
drain at any real moment returns nothing for it. Do not answer it, and do not renumber a real
entry to `E-000`.

## Open

### E-001 — Does the web app need a serviceability gate, and what would it test?

- **Bears on:** Phase 3
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet. Moment is `inferred`: `ROADMAP.md:248` makes "genuinely
  serviceable" part of what Phase 3 proves, which is the first point a gate could fail against
  something real
- **Source:** `ROADMAP.md:217-222 @ a408d4f` (pre-migration text; those lines now point back here)
- **Status:** open

"Serviceable" is a v1 constraint in **both** directions — it must genuinely do the job with no
reaching for a spreadsheet, and it explicitly does not need to be beautiful. It is nowhere
defined and nowhere tested. That, rather than design polish, is what a gate would be for. The
alternative is that it stays a judgment call, which is defensible for a hobby project and costs
nothing until the app is big enough to rot quietly.

### E-002 — Is a design/UX specialist reviewer worth adding to the panels?

- **Bears on:** Phase 3
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet. Moment is `inferred`, not grounded in any text: Phase 3 is
  simply where the app surfaces stop being one page
- **Source:** `ROADMAP.md:217-222 @ a408d4f` (pre-migration text; those lines now point back here)
- **Status:** open

A hypothesis, not a plan. Design polish is explicitly not a v1 gate, so the case for a
specialist rests on whether the app's surfaces get numerous enough that consistency between them
stops happening by default. Alternative: fold the concern into the serviceability gate in E-001
and never staff it separately.

### E-003 — Should stage dispatch be autonomous rather than user-invoked?

- **Bears on:** H2
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet. Moment is `inferred`: H2 is the first harness row that defines
  a worker an autonomous dispatcher would have to drive
- **Source:** `ROADMAP.md:217-222 @ a408d4f` (pre-migration text; those lines now point back here)
- **Status:** open

Today every pipeline stage is invoked by hand. An autonomous dispatcher would decide which stage
runs next. It is also exactly the kind of machinery that reads as progress while removing the
human from the one loop this project's process is built around, so the alternative — leaving
dispatch manual permanently — is a real position rather than a null option.

### E-004 — Is an OpenAPI snapshot test worth adding once there is a real endpoint?

- **Bears on:** 1.8
- **Parked:** 2026-08-21
- **Assumed:** dropped at item 1.1 — `verified` from the source below. It asserted nothing the
  health test did not already cover when the API had one two-field endpoint
- **Source:** `requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:369`
- **Status:** open

The 1.1 panel dropped this and named 1.8 as the right moment, on the reasoning that a snapshot
test earns its keep once the schema is big enough that a change can be accidental. `box-score-entry`
is the first endpoint with a payload worth snapshotting.

### E-005 — Should the frontend's API types be generated from OpenAPI rather than hand-written?

- **Bears on:** 1.8
- **Parked:** 2026-08-21
- **Assumed:** hand-written, via the typed fetch wrapper at `app/src/api/client.ts` — `verified`
  from the source below. Item 1.1 built that wrapper explicitly as the seam codegen would later
  slot into
- **Source:** `requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:370`
- **Status:** open

Codegen was ruled machinery-for-one-two-field-object at 1.1. The `BoxScore` DTO at 1.8 is the
first type where hand-writing the frontend's copy means two places that must agree.

### E-006 — `.gitignore`'s blanket `build/` rule will shadow the Phase 2 builder directory

- **Bears on:** 2.1
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet, because `build/` does not exist. `measured` at item 1.1 and
  re-confirmed by the source below
- **Source:** `requests/feature-requests/_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861`
- **Status:** open

`.gitignore:63` blanket-matches `build/` at any depth. `CLAUDE.md` prescribes a
`build/build-*.py` → `datasets/` builder pattern for Phase 2, so the first builder written would
be silently untracked with nothing complaining — the same class of shadowing the career-ledger
carve-out exists to prevent. The 1.1 plan explicitly asked that this become an intake item rather
than be rediscovered at 2.1. Alternatives are a `!build/build-*.py` carve-out, a narrower ignore
rule, or a different directory name.

### E-007 — The roadmap cites a tenth open question that was never written

- **Bears on:** post-v1
- **Parked:** 2026-08-21
- **Assumed:** recorded, **not answered** — `measured` today: `ROADMAP.md:334` cites it and
  `GAME_DESIGN.md` §8 runs `[OPEN-1]` through `[OPEN-9]` and stops
- **Source:** `ROADMAP.md:334`
- **Status:** open

The roadmap's open-questions index carries a tenth row, `[OPEN-10]` — whether the offseason
training payout scales with age — with no matching entry in the design document that owns that
series. (The id appears in this body deliberately and never in an entry title: titles are guarded
against it, so that this file indexes that register without starting to impersonate it.) Recording
it here indexes the orphan; it does not dispose of it. Disposing of it means either writing the
missing question into `GAME_DESIGN.md` §8 or deleting the roadmap row, and it touches ADR 0005's
training carve-out, so it is not a one-line fix. Deliberately parked at `post-v1` alongside the
aging work it belongs to.

### E-008 — Does a superseding correction event carry the full box score or a delta?

- **Bears on:** 1.3
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet
- **Source:** `ROADMAP.md:57-62`
- **Status:** open

ADR 0003 settles that corrections are appends and never mutate a recorded event, but not what a
correction event contains. A full replacement is simpler to fold and trivially idempotent; a
delta is smaller and makes "what actually changed" readable without diffing two records. The fold
resolves either, so this is a format decision rather than an architectural one — which is exactly
why it will be tempting to make it silently while building the fold.

### E-009 — Does a correction event pin the ruleset version live, or inherit the corrected event's?

- **Bears on:** 1.3
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet
- **Source:** `docs/decisions/0003-event-sourced-tracked-ledger.md`
- **Status:** open

ADR 0003 requires every event to pin the ruleset version live when it was recorded, and ADR 0004
makes a pinned version immutable. Neither says which version a *correction* pins. Inheriting the
corrected event's keeps a replay of history identical under any later retune. Pinning live makes
the correction a new statement under current rules, which silently re-scores the corrected game —
so fixing a typo in a two-season-old box score could move a career's totals under an economy that
did not exist when it was played. Both are defensible and the fold's version resolution has to be
written to match one of them. This is the 1.3 decision that can quietly rewrite a career that has
no upstream copy, which is why it is parked rather than left to be settled mid-build.

## Resolved

*None yet. Resolved entries stay here with `Status: resolved` and a pointer, in the body, to
wherever the answer was actually recorded.*

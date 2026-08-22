> **Status:** implemented · created 2026-08-15 · decided · next: commit

# Project Scope — Escalation Queue (Harness H1)

## Fit Verdict

**Clean.** All three scopers reached `clean` independently.

Grounded rather than asserted:

- **A reserved, binding slot exists.** `ROADMAP.md:197` is the H1 row — `ESCALATIONS.md`, the
  parked-decision format, a structural test that every entry names a real roadmap item;
  `Blocks: 1.3`; IN-PROGRESS.
- **An accepted ADR already assumes the mechanism.**
  [ADR 0010](../../../docs/decisions/0010-panels-by-default.md) rejects "require the user to
  approve a stage plan on every item" *because* "it makes the human a gate on the routine path,
  which is precisely the synchronous-interruption tax roadmap item H1 exists to remove."
- **Contract applicability verified by filesystem probe, not assumed.** No
  `datasets/manifest.json` (item 2.1 NOT STARTED), no `careers/`, no `rulesets/`, and
  `src/rpg_core/` contains only `__init__.py`. The five dataset contracts and the ledger/economy
  constraints are therefore genuinely N/A — recorded rather than invented. ADR 0003's append-only
  rule and ADR 0004's version immutability are not engaged.
- **The substrate is idiomatic.** `tests/test_repo_structure.py` already holds five
  parse-a-document-and-assert-against-the-filesystem tests, and `tests/test_layering.py` is the
  closer shape for a parser guard.

Two frictions recorded rather than hidden:

**Fragmentation.** This is the *sixth* place a question can be parked — after `GAME_DESIGN.md` §8
`[OPEN-N]`, `DESIGN.md` §2, `DESIGN.md` §4, ADR 0010's Stage plan section, and `/diagnose-bug`'s
Escalation. `DESIGN.md` §4 is the sharpest overlap: bullets with no ids and no named moment,
literally what the queue is for minus the discipline. Nothing mechanical can distinguish a
build-time decision from an engineering question, which is why the boundary header is the
load-bearing deliverable rather than the file.

**Inertness.** At the roadmap's three literal deliverables, nothing writes to and nothing reads
the queue — structurally identical to the "inert until it is re-applied" failure `ops/README.md`
documents for `branch-protection.json`. All three scopers named this independently as the
feature-killing risk. Decisions 1 and 5 below are the response.

## Problem

Decisions arrive mid-build and there is nowhere to put one. A worker facing a judgment call has
exactly two moves — interrupt, or guess silently — and the second leaves no trace: a decision
made by default is indistinguishable from one nobody noticed was there.

Item 1.1 surfaced this as the project's real constraint rather than build speed: eight decisions
arrived synchronously in one sitting, each stopping work until answered, in whatever order the
build hit them rather than when the evidence was best.

The failure already has instances sitting in prose and in archives. `ROADMAP.md:217-222` parks
three hypotheses in a paragraph, each said to have "a named moment to re-decide" — with the
moments named only in the prose describing them. Three more decisions with explicitly named
moments were verified stranded inside `_done/1.1-app-shell/`, a directory
`tests/test_request_links.py:36` deliberately skips and nobody reopens.

## Goals / Non-Goals

**Goals**

1. **Make the third move exist.** A worker hitting a judgment call records the question, the
   alternatives, and — load-bearing — **the assumption actually taken** while proceeding, then
   keeps going. The `Assumed:` field addresses the half of the problem nothing in the repo
   currently touches.
2. **Pin the entry format deliberately**, because every later entry inherits it. Keep the field
   set minimal so a revision at entry six is an edit, not a migration. Cheapness, not foresight,
   is the mitigation for designing a format from retrospective examples.
3. **Make the pointer mechanical rather than aspirational** — a structural test parses every
   entry's named moment and asserts it exists in `ROADMAP.md`.
4. **Draw the boundary against the five existing parking mechanisms in the queue's own header**,
   where a worker about to add an entry actually reads it.
5. **Discharge the three `ROADMAP.md:217-222` hypotheses into real entries**, leaving the
   paragraph pointing at the queue rather than carrying the content.
6. **Recover the decisions already lost into `_done/1.1-app-shell/`** — what makes the queue an
   artifact with content on day one rather than an empty schema.
7. **Give the queue at least one seam that actually reads it**, so it is not the inert-config
   failure.
8. **Unblock `Blocks: 1.3` fast**, so `correction-by-append` can start — and can start by reading
   what was parked against it.
9. **Leave a cold agent able to answer "what was parked against this item?"** from one file, with
   no institutional memory and without being asked anything.

**Non-Goals**

1. **Not a replacement for `[OPEN-N]`.** `GAME_DESIGN.md` §8 and its phase index stay exactly as
   they are. Cross-references only, never a migration. The widest option in Open Question 1 is
   rejected outright.
2. **Not absorbing `DESIGN.md` §2 or §4.** Phase 0's exit condition was "every document doing one
   job."
3. **Not a blocking mechanism.** User-settled at intake. No open entry is ever an error state.
   (See the F-33 carve-out under Decisions.)
4. **Not a priority, urgency, severity, owner, or due-date system.** User-settled: the moment *is*
   the sort key.
5. **Not an ADR replacement, and not a duplicate of ADR 0010's Stage plan.** An entry is a
   question *parked*; an ADR is a decision *made*; a Stage plan is per-request ceremony.
6. **Not a general TODO list or shadow backlog.** An entry must be a decision with alternatives,
   not a task. Symptom to watch: an entry whose `Assumed:` field has no plausible alternative.
7. **Entries do not carry a decision's rationale.** They name the question, the assumption, and
   where the answer will be recorded; rationale lives in the artifact pointed at.
8. **No agent ever resolves an entry.** Agents park and read; disposition is the user's.
9. **Nothing under `src/` or `app/`.** No endpoint, DTO, domain model, event type, or dataset
   registration.
10. **No programmatic consumer beyond the pytest guard.** No API route, no importable runtime
    parser, no UI surface.
11. **No new CI job.** The tests join the existing "Lint, types, tests" job, so
    `ops/branch-protection.json` and `tests/test_ci_contexts.py` stay untouched.
12. **No resolved-entry archive or rotation in v1.**
13. **Not fixing the substance of any parked decision.** Migrating and recovering means
    *recording*, not deciding. `[OPEN-10]` in particular is recorded, not answered.
14. **No commit and no merge.** Lands on a branch through `/commit`; the PR stays the user's.

## Acceptance Criteria

Tier-tagged per finding F-04. **[C]** core · **[F]** folded cheap win · **[G]** gated item the
user approved.

1. **[C]** `uv run pytest tests/test_escalations.py -q` is green, and the module carries a
   docstring in the `tests/test_repo_structure.py:1-9` / `tests/test_layering.py:1-17` idiom
   explaining why the guard exists.
2. **[C]** **Parser positive assertion.** A pure module-level function parses valid moments out of
   `ROADMAP.md`. A test asserts the returned set is **non-empty**, contains known-good ids
   (`0.1`, `1.3`, `H2`, `4.6`), and that its size is ≥ 30. *Deliberately not an exact 38-id set —
   finding F-28 showed that fires in unrelated PRs whenever a row is added.*
3. **[C]** **Parser negative assertion, corrected per findings F-27 and F-06.** The leading cell
   must **match an id pattern** (`^\d+\.\d+$` or `^H\d+$`); emptiness is *not* the discriminator,
   because the v1 scope tables' data rows lead with `**Creation**`-style bold text, not empty
   cells. The test proves **all three** non-item tables contribute zero ids — `ROADMAP.md:23-35`,
   `:41-51`, `:75-84` — plus the open-questions table whose leading cells are `**[OPEN-N]**`.
4. **[C]** **Non-vacuity.** The test asserts the entry regex matched at least one entry and fails
   with "no entries parsed — the entry format drifted from the regex" if it matched zero. Without
   this, a format change turns the guard into `assert not []` and it passes forever.
5. **[C]** **Proven red and green against `tmp_path`, mutating no tracked file**, in the
   `tests/test_layering.py:85-100` idiom: a fabricated queue naming moment `9.9` returns exactly
   that one violation; a fabricated queue naming `1.3`, `H2`, `Phase 3`, and `post-v1` returns
   none. Both fixtures fabricate **the roadmap too**, so the green case is hermetic (finding F-07).
6. **[C]** **The real assertion:** the parser over the actual queue finds zero violations.
7. **[C]** **The failure message is the record**, mirroring `tests/test_layering.py:112-123`: it
   names the queue file, the offending entry id, the offending moment, and states the rule.
8. **[C]** **Field and vocabulary guards.** Every entry carries all **six** required fields —
   `Bears on:`, `Parked:`, `Assumed:`, `Source:`, `Status:`, and a title with an id matching
   `^E-\d{3}$`, unique. `Status:` values come from a closed vocabulary. *Six, not five — finding
   F-26 caught that `Source:` was required by the tests while absent from the pinned format. Every
   entry carries provenance uniformly rather than conditionally.*
9. **[C]** **State is stored once (finding F-08).** `Status:` is the single source of truth, and a
   test asserts the `## Open` / `## Resolved` section an entry sits in agrees with its `Status:` —
   the same invariant `test_index_stage_cells_match_their_artifact_status_headers` already
   enforces between the Index and artifact headers.
10. **[C]** **Register-boundary guard.** No entry title contains `[OPEN-`, and the queue contains
    its boundary header naming `GAME_DESIGN.md`, `DESIGN.md`, ADR 0010's Stage plan, and
    `/diagnose-bug`'s Escalation.
11. **[C]** **Goal 1 is proven, not assumed (finding F-01 — this criterion exists because the
    panel found goal 1 had none).** The header's fenced worked-example entry parses green under
    the *same* regex and field guards as real entries. A worker copying the template cannot
    produce a malformed entry, which is what "the third move exists" reduces to mechanically.
12. **[C]** **Seed migration proven**, in the substring idiom of
    `test_no_document_still_claims_there_is_no_application`: the queue contains distinctive
    strings for all **seven** seeds — the three `ROADMAP.md:217-222` hypotheses, the three
    recovered `_done/1.1-app-shell/` strays, and the `[OPEN-10]` orphan. *Seven reconciles the
    inconsistency findings F-10/F-29 raised, using the F-02 correction that
    `PROJECT_SCOPE.md:319` was a shipped fold, not a stranded decision — three strays, not four.*
13. **[C]** **No duplicate source.** `ROADMAP.md` no longer enumerates the three hypotheses
    inline; the paragraph is reduced to a pointer. This is what stops the migration leaving two
    sources of truth. The paragraph's substantive observation — that "serviceable" is a v1
    constraint in both directions and is nowhere defined or tested — is preserved, not dropped.
14. **[G]** **The read seam exists.** `/make-feature-request` Step 2 carries a bullet telling
    intake to surface queue entries naming this item's moment, and a substring test proves the
    bullet is present. *Approved as Decision 1.*
15. **[G]** **The `/commit` drain-hole check exists.** `/commit` Step 4 carries a bullet: when
    flipping a roadmap row to `DONE`, surface open entries naming it. Substring-tested.
    *Approved as Decision 5.*
16. **[G]** **The `/diagnose-bug` pointer exists.** Its Escalation section carries one line
    telling it to also park a queue entry naming the moment the bug bears on. Substring-tested.
    *Approved as Decision 3.*
17. **[F]** `uv run pytest tests/test_repo_structure.py -q` is green with
    `test_core_documents_exist` extended to include the queue, and its docstring — which says
    "the three documents that carry the design" over a five-name tuple — corrected in the same
    edit.
18. **[F]** `uv run pytest tests/test_request_links.py -q` is green with `SCANNED_TREES` extended
    to root-level `*.md`. **Measured 2026-08-15:** `_dead_links()` over all five root documents
    returns `[]` today, so this costs zero cleanup.
19. **[F]** **Discoverability proven mechanically:** `CLAUDE.md`'s project map and `README.md`'s
    project map block both contain the queue's name, each substring-tested.
20. **[F]** **The measured doc drift is fixed (finding F-35).** `CLAUDE.md:216` says "**Nine**
    decisions are settled" while three other lines say ten. One word.
21. **[C]** `uv run ruff check`, `ruff format --check`, and `mypy` all exit 0 with the new module
    present. mypy is strict over `src` and `tests`, so the parser is fully annotated with zero new
    `# type: ignore`.
22. **[C]** `uv run pytest` green overall — in particular `test_no_leaks.py` (a new tracked `.md`
    is scanned; **the repo is public and entries record real assumptions**).
23. **[C]** **`CLAUDE.md` budget not worsened by more than one line.** Measured baseline: 221
    lines. `(Get-Content CLAUDE.md).Count` increases by at most 1 versus HEAD.
24. **[C] USER-RUN, not panel-claimable.** Picking up item 1.3, the entries naming 1.3 surface
    without the user being asked anything; the user can answer an entry by editing the queue alone
    with no build running; and the parked context reads as useful rather than as noise.

## Scope (tiered)

**Core (must)**

1. `ESCALATIONS.md` at the **repo root** — the name `ROADMAP.md:197` commits to. Root because
   discoverability *is* the mechanism: the three hypotheses failed precisely by being somewhere
   nobody looks.
2. **A boundary header written for the worker about to add an entry**, carrying: what the queue is
   for; a **register map** disambiguating it from `[OPEN-N]`, `DESIGN.md` §2, `DESIGN.md` §4, ADR
   0010's Stage plan, and `/diagnose-bug`'s Escalation; the ADR-0011 trigger (Decision 6); and one
   line recording that a `Blocks` cell stops work while a queue entry never does.
3. **The entry format, six required fields:** id (`E-NNN`), `Bears on:` (a required named moment),
   `Parked:` (a date), `Assumed:` (what was actually done, or an explicit "none — not hit yet"),
   `Source:` (where it surfaced), `Status:`.
4. **Hard-require a named moment — no bare `unscheduled` hatch.** The drain cadence makes an
   unmoored entry structurally invisible, and the repo already has two homes for a genuinely
   unmoored question.
5. `tests/test_escalations.py` — a **new module**, not an append to `test_repo_structure.py`. The
   request's constraint binds the *idiom*, and a parser guard is closer to `test_layering.py`.
6. **Seed migration** — the three hypotheses become entries; the paragraph becomes a pointer.
7. **Resolved entries stay**, with a `Status:` flip and a resolution pointer, in a `## Resolved`
   section. Mirrors `docs/decisions/README.md:26-31`.
8. **Discoverability**: one line in `CLAUDE.md`'s project-map fenced block (inside the fence, so it
   adds no link-check surface) and one row in `README.md`'s project map.
9. `ROADMAP.md` row H1 advanced by `/commit` against the diff, never hand-edited.
10. **The read seam** — `/make-feature-request` Step 2 bullet. *Promoted from gated by Decision 1.*
11. **The `/commit` drain check** — Step 4 bullet. *Promoted from gated by Decision 5.*
12. **The `/diagnose-bug` pointer** — one line. *Promoted from gated by Decision 3.*

**Folded in (cheap wins)**

1. **Widen the moment vocabulary** to `item id | phase name | post-v1` instead of item ids only.
   One regex alternation; lets the serviceability-gate entry name `Phase 3`.
2. **Recover the three stranded decisions** from `_done/1.1-app-shell/`, each with a `Source:`
   citation — the OpenAPI snapshot test (`PROJECT_SCOPE.md:369`, moment 1.8), OpenAPI→TypeScript
   codegen (`:370`, moment 1.8), and the client-side router seam
   (`IMPLEMENTATION_PLAN.md:859-861`, moment 1.10).
3. **Record `[OPEN-10]` as a seed entry** — measured orphan, recorded not answered.
4. **Add the queue to `test_core_documents_exist`** and fix that test's docstring.
5. **Extend `test_request_links.py` to root-level `*.md`** — measured clean today.
6. **A worked example entry** in a fenced template in the header.
7. **One line in `requests/README.md`** beside the three-track table — the only pointer location
   covered by the link checker today, so the one pointer that cannot silently rot.
8. **A one-line name disambiguation** in both the queue and `/diagnose-bug`, noting "escalation"
   now means two things — one non-blocking and moment-scoped, one blocking and bug-scoped.
9. **Fix `CLAUDE.md:216`'s "Nine decisions"** — measured drift from the ADR 0010 commit.

**Gated — resolved** — see Decisions.

## Above & Beyond

Carried from the panel, retiered by the user's decisions:

| Proposal | Tier |
|---|---|
| Register-map table in the queue's header | **core** — the load-bearing deliverable, not an enhancement |
| Widen moment vocabulary instead of an `unscheduled` hatch | **cheap fold** |
| Resolved-in-place with a resolution pointer, and ADR graduation | **cheap fold** |
| Recover the lost decisions from `_done/1.1-app-shell` | **cheap fold** |
| Extend `test_request_links.py` to root documents | **cheap fold** |
| A worked example entry in the header's fenced template | **cheap fold** |
| Record `ROADMAP.md`'s `Blocks`-cell semantics in the header | **cheap fold** |
| Teach `/make-feature-request` to READ the queue | **core** — approved, Decision 1 |
| Give `/diagnose-bug`'s hand-off a destination | **core** — approved as a pointer, Decision 3 |
| One-line `/commit` surface when an item advances to DONE | **core** — approved, Decision 5 |
| Teach `/scope-feature` and `/implement-plan` to WRITE entries | **deferred** — own request, Decision 2 |
| Mirror guard for `[OPEN-N]` citations | **deferred** — follow-up, Decision 4 |
| ADR 0011 recording the boundary | **deferred** — with a written trigger, Decision 6 |
| An `/update-docs` check for queue drift | **drop** — weak; the sweep is what gets skipped when someone is in a hurry |
| A read-only drain command (`ops/escalations.py --for 1.3`) | **drop** — request's "not now" |
| A `Supersedes:` field | **drop** — real in principle, no instance yet |
| A resolved-entry archive / `_done/` split | **drop** — the two-section format makes it a later mechanical move |
| A per-entry `Surfaced by:` field | **drop** — `Bears on:` under a second name; two fields that must agree is a bug source |

## Risks & Unknowns

1. **Inertness** — dominant, all three scopers independently. Mitigated by Decisions 1, 3, and 5;
   not eliminated, because nothing yet *writes* entries automatically.
2. **The observable signal may not fire.** "Item 1.3 can start by reading the queue" only holds if
   something is parked against 1.3 by then. The seven seeds make this true on day one.
3. **Fragmentation** — a sixth parking place. `DESIGN.md` §4 is the sharpest overlap. The header's
   register map is the only mitigation, and it is prose.
4. **The test is trivially vacuous if written naively.** `for entry in parsed: assert …` over an
   empty list passes forever. AC 4 exists for this.
5. **Parser brittleness.** `ROADMAP.md` mixes four table shapes in one file, and the harness table
   carries an extra `Blocks` column. AC 3 is the corrected discriminator.
6. **Roadmap renumbering tax, with precedent.** ADR 0010 just deleted two columns from every
   table. Item ids are hand-edited cells; a renumbering silently orphans entries.
7. **Scope creep has a binding cost.** `Blocks: 1.3` is binding, and 1.3 is the append-only
   correction model ADR 0003 treats as load-bearing. Every gated item adopted delays it.
8. **Mis-filing under the nearest moment.** Hard-requiring a moment pressures a worker to attach an
   unmoored question to whatever row is closest, corrupting the drain while looking correct. The
   widened vocabulary reduces but does not remove this.
9. **Name collision.** "Escalation" now means two things in one repo. Mitigated by a one-liner in
   both places; not solved.
10. **Public repo.** Entries record real assumptions taken when nobody was sure — world-readable
    forever. `test_no_leaks.py` blocks paths and emails, not indiscretion.
11. **The format is pinned by every later entry** and is being designed from *retrospective*
    examples rather than a real mid-build parking event. Mitigation is cheapness, not foresight.
12. **Entry-id collisions across branches (finding F-38).** Sequential `E-NNN` in one file merges
    cleanly into duplicates. Unmitigated in v1 — the uniqueness guard in AC 8 catches it at CI
    rather than preventing it. Acceptable while entries are few.
13. **UNCONFIRMED — whether the drain cadence actually fires.** "Drained at item boundaries"
    assumes every item boundary passes through `/make-feature-request`. That holds while every
    roadmap row becomes a request, which ADR 0010's entry condition does *not* guarantee for doc
    edits. Label: `unconfirmed`, and it is the assumption the whole cadence rests on.
14. **INFERRED, not verified — the seed moments.** The recovered strays carry moments (1.8, 1.8,
    1.10) that were the 1.1 panel's judgment as of 2026-08-14, and the three hypotheses' moments
    are this panel's reading of prose. A cold planner should not treat them as measured.
15. **Adjacent measured defect, not fixed here.** `update-docs/SKILL.md:76-77` prescribes a
    `Measure-Object -Line` command for the `CLAUDE.md` budget that under-reports. Worth its own
    bugfix request; out of scope.
16. **Maintenance, small and permanent.** One more root document, one more test to keep green, one
    more file every doc sweep considers.

## Affected Area & Pointers

Read in this order. All line numbers verified by the panel on 2026-08-15.

- **`ROADMAP.md:195-222`** — the spec of record. The H1 row (`:197`), *Why H1 exists*
  (`:199-203`), and *Parked, not scheduled* (`:216-221`) naming the three seeds.
- **`ROADMAP.md` — the parser's input, all four table shapes.** Item tables at `:151-158`,
  `:176-188`, `:232-241`, `:253-259`, `:268-275`; the harness table at `:195-198` **with its extra
  `Blocks` column**; the v1 scope tables at `:23-35`, `:41-51`, `:75-84` (bold leading cells, not
  empty — see AC 3); the open-questions table at `:324-334`.
- **`tests/test_layering.py`** — the closest idiom. Docstring `:1-17` (why a pure function proven
  against `tmp_path`: subagents have read-only git), the red/green proofs `:85-100`, the
  failure-message test `:112-123`.
- **`tests/test_repo_structure.py`** — module docstring `:1-9`; the module-level regex convention
  `:21`, `:30`; `test_core_documents_exist` (extend); the substring-assertion idiom `:260-273`.
- **`tests/test_request_links.py`** — `SCANNED_TREES:24` (extend to root), `_dead_links:40-64`,
  the `_done/` skip `:36`, the fenced-block exemption `:26`.
- **`requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:369`, `:370`, and
  `IMPLEMENTATION_PLAN.md:859-861`** — the three recovered seeds. Note `PROJECT_SCOPE.md:319` is
  **not** one (finding F-02: a shipped fold, not a stranded decision).
- **[ADR 0010](../../../docs/decisions/0010-panels-by-default.md)** — the Stage plan mechanism,
  its entry condition (which exempts doc edits and is why the drain cadence is `unconfirmed`), and
  `:125-128` where H1 is named as the mechanism it depends on.
- **[`docs/decisions/README.md`](../../../docs/decisions/README.md)** `:20`, `:26-34` — the
  immutability ethos the resolved-entries-stay rule borrows. An **analogy** to ADR 0003, not an
  application of it: ADR 0003's append-only rule governs `careers/**/events.jsonl` only.
- **[`GAME_DESIGN.md`](../../../GAME_DESIGN.md) §8** — the `[OPEN-N]` mechanism this must not
  duplicate, and the measured `[OPEN-10]` orphan (`ROADMAP.md:334` cites it; §8 stops at
  `[OPEN-9]`).
- **[`.claude/skills/diagnose-bug/SKILL.md`](../../../.claude/skills/diagnose-bug/SKILL.md)**
  `:132-142` and `:161-162` — the dead-end hand-off and the name collision.
- **[`.claude/skills/make-feature-request/SKILL.md`](../../../.claude/skills/make-feature-request/SKILL.md)**
  `:74-92` (Step 2, the read seam) and
  **[`.claude/skills/commit/SKILL.md`](../../../.claude/skills/commit/SKILL.md)** Step 4 (the
  drain check) plus its keep-it-lightweight rule.
- **[`ops/README.md`](../../../ops/README.md)** `:20-37` — the "inert until re-applied" failure
  this feature's headline risk is named after.
- **NOT APPLICABLE, verified by filesystem probe** and recorded so a cold planner does not go
  looking: `datasets/manifest.json`, `careers/`, `rulesets/`, `lib/` (all absent);
  `src/rpg_core/` (only `__init__.py`).

## Decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | **Add one READ bullet** to `/make-feature-request` Step 2 | The minimum antidote to the risk all three scopers called feature-killing, landing exactly where the request's observable signal fires. Adds a read to a checklist and changes no decision logic — gated only because it edits a skill file, brushing the request's "no skill behavior changes" non-goal |
| 2 | **No skill WRITES entries in this item** — deferred to its own request | The format has not survived contact with a single real parking event; automating writes risks flooding a queue whose value is being short enough to read in one sitting; and `Blocks: 1.3` makes this a trade of ledger progress for harness polish |
| 3 | **`/diagnose-bug`'s hand-off gets a destination — as a pointer only** | The RCA keeps its Escalation section (the evidence trail, not duplicated) and gains one line telling it to park a queue entry. Two mechanisms, one index. Preserves the non-blocking property exactly: the bug still waits; the queue only remembers that it is waiting |
| 4 | **Record `[OPEN-10]` as a seed entry; hold the mirror guard** | The guard would ship RED until the orphan is disposed, putting a `GAME_DESIGN.md` decision on the critical path of a binding `Blocks: 1.3` — and the orphan touches ADR 0005's carve-out, not a one-line fix. Land H1, dispose the orphan, then add the guard green |
| 5 | **`/commit` checks for open entries when it flips a row to `DONE`** | Closes the drain hole finding F-32 found: an open entry naming 1.3 goes permanently invisible once 1.3 closes. `/commit` Step 4 already parses roadmap rows and flips statuses — it is the one thing running at exactly that moment |
| 6 | **No ADR 0011 yet — with a written trigger** | The header carries the boundary at the point of use, and the register guard makes part of it mechanical. Counter-precedent is recent and on point: 1.1's Decision 3 chose a guard test over a tenth ADR because "a test failing the build is a stronger record than prose." **Trigger, recorded in the header:** the first time someone proposes absorbing `[OPEN-N]` or `DESIGN.md` §4, that is the second litigation and ADR 0011 gets written then |
| 7 | **Root, and added to `test_core_documents_exist`** | All three scopers said root — the hypotheses failed by being where nobody looks. The deletion guard is real protection: without it, removing the file silently empties the mechanism. The minimalist's dissent (a queue is not a design document) is answered by fixing the docstring, which already lied over a five-name tuple |

**One carve-out recorded rather than left as a contradiction (finding F-33).** "Parking never
blocks" governs the *decision*: no open entry stops a stage, fails a build, or gates a merge. It
does **not** exempt the queue file from ordinary CI — a malformed entry fails
`tests/test_escalations.py` exactly as malformed markdown fails any other guard. Those are
different claims, and the header states both.

## Panel Trail

Raw, unfiltered panel output — three scopers' proposals in
[`reviews/scope-proposals.md`](reviews/scope-proposals.md); all 48 adversary findings, both
adversary summaries, and the convergence map in
[`reviews/scope-adversarial.md`](reviews/scope-adversarial.md). Panel health: 3/3 scopers, 2/2
adversaries, 0 degraded lenses, 48 findings (3 blockers, 20 majors). All three blockers — F-01
(goal 1 unproven), F-26 (format field contradiction), F-27 (mis-grounded parser assertion) — are
resolved in the acceptance criteria above and annotated where they landed.

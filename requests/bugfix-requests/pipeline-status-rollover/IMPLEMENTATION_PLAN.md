> **Status:** planned · created 2026-08-21 · decided · next: implement

<!-- This opens at `planned`, not the `plan` that create-implementation-plan/SKILL.md:176 prescribes.
     `plan` is defect 2 of the bug this plan fixes; the grammar at requests/bugfix-requests/README.md:86
     is the authority. Its three sibling artifacts and the Index cell were rolled to `planned` in the
     same edit set — that is defect 1, also being fixed here. Both deviations are recorded in §5. -->

# Implementation Plan — Make the pipeline skills obey the status grammar they cite

> **One-line goal:** the three red repro tests go green, every stage word a pipeline skill writes is
> one its track declares, and the two stage-advancing skills roll the artifacts already in the
> directory · **Target component:** four `.claude/skills/*/SKILL.md` files and
> `tests/test_repo_structure.py`

## 1. Onboarding — read these first

**What this is.** Three track READMEs each declare a status grammar on one line. Six pipeline skills
each restate that vocabulary as a hand-typed literal in a `> **Status:** <word>` template, with no
mechanical link back. Three of the six drifted, and two stage-advancing skills also forgot to roll
the artifacts already sitting in the item directory. Nothing under `src/`, `app/`, `careers/`,
`datasets/` or `rulesets/` is touched.

**Branch state.** Work on `bugfix/pipeline-status-rollover`. **Do not branch off `main`** — the RCA
and the three red tests landed in `fb0406e`, which is not on `main`; from `main` you would see a
fully green suite and conclude there is nothing to fix.

**Baseline, measured at planning time:** `uv run ruff check` → clean; `uv run mypy` → Success, 16
source files. For the pytest baseline see the decision table in Phase 1 step 1 — it is deliberately
*not* stated as a single expected number, for the reason recorded there.

| Read | Why |
|---|---|
| `ROOT_CAUSE_ANALYSIS.md` (this directory) | The decided upstream artifact — **consume it, do not re-open it.** Its verdict, the red-repro table, the four-instance evidence, the two-invariant analysis, and the tiered fix posture are the whole mandate. Note its own Status line opens at `diagnosed` rather than the template's `root-cause`: that is defect 4 being avoided in the act of writing, and it is the strongest single piece of evidence in the file |
| `BUGFIX_REQUEST.md` (this directory) | Context. Its **Affected Area & Pointers** is the fastest map of every touched file; its reproduction note explains why the two defect classes fail independently |
| `tests/test_repo_structure.py` | The repro **and** the regression guard, one file. Read the module constants and the two helpers *before* touching any skill — the fix is prose graded by regexes over specific line windows, so wording and placement are the whole job |
| `.claude/skills/scope-feature/SKILL.md` | The reference implementation the fix copies. It does three things in order: rolls the sibling, sets the Index cell, opens the new artifact. **Copy that order, not just the sentence** |
| `.claude/skills/create-implementation-plan/SKILL.md` | Defects 1 and 2. Its Step 5 sets the Index and its own artifact and never mentions the siblings; its template writes `plan` while the adjacent comment cites "this README status grammar" as authority |
| `.claude/skills/implement-plan/SKILL.md` | Defects 1 and 3, plus the two-valued track resolution the terminal word must derive from |
| `.claude/skills/diagnose-bug/SKILL.md` | Defect 4. Also the **second** correct rollover, and the in-repo precedent `DERIVES_TERMINAL` was written around ("or the terminal stage word") — preserve both while changing the token |
| `requests/bugfix-requests/README.md` | This item's track contract: the Definition of Done, the grammar this fix makes enforceable, and the `_done/` archive convention |
| `requests/README.md` | States that each track README **is the contract** for its status grammar. That documented ownership is why the fix cites the READMEs rather than relocating the grammar |

## 2. Architecture map

Two invariants govern a stage word. **A** — the Index cell agrees with every `*.md` in the item
directory — is guarded by `test_index_stage_cells_match_their_artifact_status_headers`. **B** — the
word is one the track's grammar declares — was guarded by nothing until the repro landed. A compares
a directory *against itself*, which is why three of the four instances stayed silent.

The fix does not move the grammar. It makes each restatement legal, adds the missing rollover
instruction, derives the terminal word from the resolved track, and points each restatement at its
authority. **The guard is the enforcement; the citation is the documentation.**

Three regexes in `tests/test_repo_structure.py` grade the prose, and two of them only look inside a
window computed by `_advance_status_section` — from the first `advance status` match to the next
`^##` heading. **That helper is fence-blind.** Measured: the window is lines 167→184 in
`create-implementation-plan` and 254→276 in `implement-plan`, and **both windows contain the
```` ```markdown ```` fence and the template blockquote inside it.** Prose added below the fence
opening is still inside the window; prose added after the next `##` heading is not.

## 3. Phased implementation

**The per-phase gate.** Each phase ends with all of: `uv run pytest -q` · `uv run ruff check` ·
`uv run ruff format --check` · `uv run mypy` · **and the node self-verification guards belonging to
every skill edited in that phase**, because each of those skills says to run them "whenever this file
changes":

```
node .claude/skills/implement-plan/tests/merge_fallback_guard.mjs
node .claude/skills/implement-plan/tests/verify_batching_guard.mjs
node .claude/skills/create-implementation-plan/tests/merge_fallback_guard.mjs
node .claude/skills/create-implementation-plan/tests/merge_failure_repro.mjs
node .claude/skills/scope-feature/tests/merge_fallback_guard.mjs
```

Then `/commit`. **All commands in this plan are PowerShell** — `grep` does not exist in this shell;
use `Select-String`.

### Phase 1 — The fix: red repro to fully green

**Goal.** All three repro tests go green, and the readers the renames invalidate move with them.
Deliberately **atomic**: the suite cannot be green partway through, and a half-landed rename actively
misdirects the next pipeline run.

**Steps**

1. **Establish the baseline as a decision table, not a halt.** Run `uv run pytest -q --tb=no` and read
   the result against this table. *(The earlier draft of this plan pinned `HEAD` to `fb0406e` and made
   any other count an unconditional STOP. Both were wrong: this plan is itself committed before
   implementation begins, so `HEAD` is the plan's commit; and the STOP contradicted the very next
   step. The pytest counts are what actually discriminate.)*

   | Observed | Meaning | Do |
   |---|---|---|
   | Exactly the 3 named repro tests fail | Expected baseline | Proceed |
   | Those 3 **plus** `test_index_stage_cells_match_their_artifact_status_headers` | The stage-3 run that wrote this plan followed the still-broken skill and left this directory inconsistent | **Repair it in this phase** — set all four `*.md` here and the Index cell to `planned` — and record it in the report as live evidence for defect 1 |
   | 0 failures | You are on `main`, or on the wrong branch | Stop and report |
   | Anything else | Unrelated drift | Stop and report; do not fold it in |

2. **Read `tests/test_repo_structure.py`'s constants and helpers in full** before touching a skill.
   Apply every edit by **exact-text match, never by line number** — the first insertion shifts
   everything below it.

3. **EDIT A — defect 2.** In `create-implementation-plan/SKILL.md`, change the Index instruction, the
   artifact stage line, and the template blockquote from `plan` to `planned`.

4. **EDIT B — defect 4.** In `diagnose-bug/SKILL.md`, change the template blockquote and its Step 5
   instruction from `root-cause` to `diagnosed`. **Preserve the "(or the terminal stage word)"
   phrasing** — `DERIVES_TERMINAL` was written around it, and it is the precedent EDIT E copies.

5. **EDIT C — defect 1, twice.** Add a sibling-rollover bullet to `create-implementation-plan` Step 5
   and `implement-plan` Step 7, copying `scope-feature`'s order. Each bullet must satisfy all four of
   these, which replace the unfalsifiable "is it followable?":
   - names the concrete artifacts to roll for **both** tracks (`FEATURE_REQUEST.md` / `PROJECT_SCOPE.md`
     and `BUGFIX_REQUEST.md` / `ROOT_CAUSE_ANALYSIS.md`);
   - says the target word is the **same** one being written to the Index;
   - says the edit is in-place and git is not to be run;
   - lands **inside** the `_advance_status_section` window (verified mechanically in step 9).

6. **EDIT D — defect 3, and a scope call worth naming.** Make `implement-plan`'s track resolution
   three-valued. **This corrects a factual premise of the decided RCA:** its Open Question 2 answer
   says "the machinery already exists", and it does not — the resolution is two-valued, and its
   `requests/<track>-requests/…` template **cannot compose for the third track** (the directory is
   `requests/calibration-findings/`, not `requests/calibration-requests/`). Fix **both** halves of
   that sentence — the work-dir *and* the track-README path — using three **literal** paths, not a
   template. Without this, calibration resolves to `feature` and defect 3 ships half-fixed with the
   guard green.

7. **EDIT E — the terminal word.** Make `implement-plan`'s terminal token derive from the resolved
   track (`implemented` / `fixed` / `retuned`). **Do not replace it with a `<placeholder>`** — see the
   Phase 1 acceptance for why.

8. **EDIT F — the two unguarded restatements.** Reword `implement-plan/SKILL.md:29` ("The feature ends
   at status `implemented`") and `:324` ("the report + `implemented` status"). Both are track-blind and
   sit **outside every guarded window**, so no test will ever catch them — which is exactly why they
   need a step of their own rather than a mention in the checklist.

9. **EDIT G — the stage-discovery readers.** Four sites look items up by the tokens this phase
   retires: `create-implementation-plan` (a feature at `scoped`, a bug RCA at `root-cause`) and
   `implement-plan` (an item at the `plan` stage). These are **functional, not cosmetic** — land the
   rename alone and the next pipeline run hunts the Index for a word that no longer exists. No test
   covers them.

10. **Verify placement mechanically, not by eye.** This is the single most likely way the phase looks
    done and is not:

    ```
    uv run python -c "import sys; sys.path.insert(0,'tests'); import test_repo_structure as t; from pathlib import Path; [print(n, bool(t.ROLLS_A_SIBLING.search(t._advance_status_section(Path('.claude/skills')/n/'SKILL.md').read_text(encoding='utf-8')))) for n in ('create-implementation-plan','implement-plan')]"
    ```

11. **Sweep for survivors:**
    `Select-String -Path ".claude\skills\*\SKILL.md" -Pattern '`plan`|`root-cause`'`

**Acceptance**

- `uv run pytest -q --tb=no` reports **82 passed, 0 failed** — 79 + 3, no test added or removed. This
  is the red-to-green transition the track's Definition of Done requires. Capture the exact output.
- Each of the three repro tests passes individually, and
  `test_index_stage_cells_match_their_artifact_status_headers` still passes (invariant A was never
  modified — RCA Open Question 4).
- **`implement-plan`'s template still reads a real declared word, not a `<placeholder>`.** Verify
  specifically: `SKILL_STATUS_TEMPLATE` is `[a-z-]+` and **cannot match a leading `<`**, so a
  placeholder makes the conformance guard *vacuous* rather than green — silently dropping that skill
  from coverage. All three planners independently named this the most tempting wrong move.
- The survivor sweep returns no stage-sense `` `plan` `` or `` `root-cause` `` under `.claude/skills/`.
- `implement-plan`'s resolution names three tracks and three **literal** paths; `requests/calibration-findings/`
  confirmed as the real directory name.
- `:29` and `:324` are reworded (checked by eye — no test covers them).

**Commit note.** Hand to `/commit`. Suggested subject: *"Make the pipeline skills obey the status
grammar they cite"*. Expect its roadmap step to take the "no roadmap change" path — this is a process
defect, not a numbered item; do not invent a row.

### Phase 2 — Cite the authority, and close the remaining literals

**Goal.** Answer the one design call the RCA left open, and fix the last two literals the repro cannot
see. Every step here is inert to the guards, which is the point.

**Steps**

1. **Record the decision before implementing it: no shared prose home.** Three grounds, all grounded:
   there is no single grammar to home (three tracks declare three different ones, so a shared file
   would be track-keyed and become a *seventh* restatement); `_declared_stage_tokens()` parses
   `**Status grammar:**` from exactly those three READMEs, so relocating would red the guard being
   installed; and `requests/README.md` already declares each track README "the contract", so the
   authority existed and only the citation was missing.

2. **Add one authority line beside each of the six template blockquotes**, naming the resolved track
   README as the source of truth and naming the enforcing test.
   **Placement is load-bearing: put it OUTSIDE the ```` ```markdown ```` fence, never inside.** All six
   blockquotes are the first line inside a fence that agents copy *verbatim* into the artifact they
   create. This is not hypothetical — `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md` carries exactly such
   a meta-comment copied out of the template region. Anything inside the fence lands at the top of
   every future request, scope, RCA, plan and report.
   Write **literal** paths (`requests/bugfix-requests/README.md`), not `requests/<track>/README.md` —
   inside a skill, `<track>` means `bugfix`/`feature`, so that template points at a directory that does
   not exist.

3. **Fix `make-bugfix-request`'s `next: root-cause`** → `next: diagnose`.

4. **Align `create-implementation-plan`'s track resolution** with the three-valued form Phase 1 gave
   `implement-plan`, and fix the duplicate two-valued work-dir templates in *both* skills' opening
   sections. Leaving the two back-half skills stating the same sentence differently is how the next
   drift starts.

5. **Add the both-invariants note to `update-docs/SKILL.md`'s requests section:** the Index mirrors the
   artifact blockquote, **and** both must be words the resolved track's grammar declares.

**Acceptance**

- All six templates carry an adjacent authority line **outside** the fence, naming a literal README
  path and the enforcing test.
- `Select-String -Path ".claude\skills\*\SKILL.md" -Pattern 'root-cause'` returns only the two
  **frontmatter stage-chain** restatements (`diagnose-bug` and `make-bugfix-request`), which are
  deliberately kept — see Decision 4 — plus genuine English prose. No stage tokens, no `next:` values.
- `uv run pytest -q` is still **82 passed**; `tests/test_request_links.py` green; all four gates clean.
- `git status --short` shows only modifications — no new file under `.claude/skills/` or `docs/`.

**Commit note.** Suggested subject: *"Cite the track README beside every stage-word restatement"*.

### Phase 3 — Two hardening guards *(approved: land both)*

**Goal.** Close the two ways this can go quiet again. Both were the RCA's gated tier; the user
approved both. Phases 1–2 alone already satisfy the Definition of Done, so this adds protection
rather than completing the fix.

**Steps**

1. **GUARD 1 — the Index cell against its own track's grammar.** Invariant A only proves the Index and
   the artifacts agree; a hand-edited Index could carry an invented word if every artifact matched it.
   Add a **new** per-track helper and keep `_declared_stage_tokens()` as the union wrapper under its
   existing name, so its call site keeps working unchanged and the conformance test keeps its **union**
   semantics (a skill legitimately serves several tracks — do not narrow it to one).
   Two notes for the docstring: the Index `stage_cell` capture is `(?P<stage>\w+)` and **does not match
   hyphens**, so a hypothetical `root-cause` cell captures as `root` — say so, or the failure text
   misleads; and the calibration track's placeholder row is not a slug-link row at all, so the empty
   track is handled by construction rather than by a special case.
   The `stage_cell` regex is **function-local**, not a module constant — copy the pattern, or hoist it
   to a module-level constant and have both tests use it. It cannot be imported as-is.

2. **GUARD 2 — stop the conformance guard going vacuous.** If a template is ever rewritten as
   `<placeholder>`, `SKILL_STATUS_TEMPLATE` stops matching it and that skill silently leaves coverage.
   **Hardcode the expected skill set as a module constant**, mirroring the `STAGE_ADVANCING_SKILLS`
   idiom — do **not** derive the subject set from "skills that currently write a concrete token", which
   is circular and shares the exact blind spot it is meant to catch.

3. **Prove both red-first, in isolation.** Break each deliberately, capture the failing output, revert,
   capture the pass. Run the break with `-k` to isolate: breaking an Index cell for guard 1 also reds
   invariant A, so a full-suite run shows two failures and the evidence gets ambiguous.

**Acceptance**

- Both tests exist and pass; red-first evidence captured for **both** (failing output + passing output
  after revert). A guard shipped without that pair is not accepted.
- The conformance test still passes with **union** semantics — verify it was not narrowed.
- **The three repro tests are untouched** — not edited, not relaxed, not reworded. They are the
  acceptance contract.
- `uv run pytest -q` reports **84 passed**. State the total explicitly in the report.
- All four gates clean. This is the only phase touching Python, so mypy strict matters here — new tests
  need `-> None`.
- No temporary red-first edit survived: `git diff --stat` shows only `tests/test_repo_structure.py`.

**Commit note.** Suggested subject: *"Guard the Index cell and the stage-token guard itself"*.

### Phase 4 — Park what this fix deliberately leaves open

**Goal.** Record the adjacent gaps rather than losing them. **This phase does *not* close the item
out** — see the hand-off note below, which is a correction to an earlier draft.

**Steps**

1. **Park E-010 — the `_done/` link-scan trade-off.** The cost is measured, not theoretical: the 1.1
   planning panel already caught defect 2, and the finding was archived into a tree the link checker
   deliberately skips. Found, recorded, and lost. There is a **second** archived record too — an HTML
   comment in `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md` saying the repo's contract wins over the
   skill's template — i.e. a hand-worked-around instance nobody propagated.
   Follow the six-field format exactly; every field is checked by `tests/test_escalations.py`. Next
   free id is **E-010**. **`Bears on:` is `H2`** — the next harness row that will re-read the skill
   corpus. *(The panel recommended `post-v1`; the user chose `H2` on the grounds that an entry parked
   at `post-v1` is the one least likely to be reopened, which is the failure mode the queue exists to
   prevent.)* `Source:` is `tests/test_request_links.py`, written as code, not a link.

2. **Park E-011 — the fifth instance.** `/diagnose-bug`'s three non-confirmed verdict exits
   (`closed-works-as-intended`, `cannot-reproduce`, `redirected-to-feature`) are stage words no grammar
   declares. They escape the conformance guard only because they sit in inline prose rather than a
   `> **Status:**` blockquote. **Parked, not fixed** — the cheap fix (adding them to the grammar line)
   would widen the declared vocabulary for **all three** tracks via the union and weaken the guard
   everywhere. That is a design change, not hardening. `Bears on:` `H2`.

3. **Consider a clause in E-010 for the `reviews/` carve-out.** `_done/1.1-app-shell/reviews/preflight.md`
   opens at `> **Status:** preflight` — a word no grammar declares, green today only because invariant
   A globs non-recursively. After this fix that exemption lives in skill bullets and nowhere in the
   track contracts: a hand-restated rule with no authority, which is the exact pattern being retired.

**Acceptance**

- `ESCALATIONS.md` carries both entries with all six fields, and `uv run pytest tests/test_escalations.py -q`
  passes — that guard checks every field and resolves `Bears on:`, so a malformed entry reds here
  rather than rotting.
- `Bears on: H2` resolves (H2 is a real roadmap row).
- Full suite green; all four gates clean.

**Commit note.** Suggested subject: *"Park the two gaps this fix deliberately leaves open"*.

### Close-out — owned by `/implement-plan` Step 7, not by this plan

**This plan deliberately does not contain a close-out phase.** An earlier draft made "write the
report, roll the four artifacts, move the directory to `_done/`, hand to `/commit`" a fifth phase.
That is verbatim what the executing skill does in its **own Step 7**, which runs *after* the
acceptance panel — so duplicating it here would have the implementer write the report twice, and
would archive `IMPLEMENTATION_PLAN.md` out from under the run still executing it. The report's spine
is the acceptance ledger, which cannot be written before the panel that produces it.

Four track-specific facts Step 7 needs, since this is the **first** item ever to complete the bugfix
track:

1. **The terminal word is `fixed`, not `implemented`.** If the just-fixed skill is followed and still
   says `implemented`, EDIT E did not land. That is the direct behavioural proof of defect 3.
2. **Four artifacts roll, not one** — request, RCA, plan, report — plus the Index cell. That is the
   direct behavioural proof of defect 1.
3. **Re-read `.claude/skills/implement-plan/SKILL.md` from disk before Step 7.** Skill text is loaded
   into the session at invocation; a mid-run edit does not retroactively change what the agent is
   following. Without an explicit re-read the likely outcome is following the stale, unfixed Step 7
   from context — writing `implemented`, forgetting the siblings — and then misreading the resulting
   red as evidence that Phase 1 failed.
4. **The report template's `**Branch:** implement/<slug>` field is wrong for this item.** The live
   branch is `bugfix/pipeline-status-rollover`. Write the real branch name; **do not rename or recreate
   the branch to match a template** — that would strand the repro. (Three branch conventions coexist in
   this repo with none written down authoritatively; that is the same restatement-drift shape as the
   bug being fixed, one level up.)

Also refresh the Index **Notes** cell at close-out, not just the Stage cell — both archived feature
rows carry outcome-shaped notes, and this row's note is written from the diagnosis. No test catches
it, which is why it needs to be an instruction.

## 4. Testing & verification

The repro is the acceptance contract: `3 failed → 82 passed` in Phase 1, `84 passed` after Phase 3.
Its three tests may not be edited, relaxed, or reworded at any point.

**What no test covers, and must therefore be checked by hand:** the two track-blind restatements at
`implement-plan:29`/`:324` (outside every window), the four stage-discovery readers (functional but
ungraded), the authority lines' placement outside the fence, and the Index Notes cell. Every one of
these is a place where the phase can look done and not be.

**The regexes are satisfiable by keyword insertion.** `ROLLS_A_SIBLING` matches on the phrase
`Status blockquote`; `DERIVES_TERMINAL` on `terminal stage word`. Passing them is necessary, not
sufficient — which is why EDIT C carries a four-part checklist instead of "is it followable?".

**Regression posture.** Additive prose plus two new tests. The one behavioural change is that
`/implement-plan` now writes a different terminal word per track — exercised immediately, by this
item's own close-out.

## 5. Decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | **No shared prose home for the grammar** | Three grounds, three planners, independently. There is no single grammar to home; `_declared_stage_tokens()` parses from exactly the three READMEs; and `requests/README.md` already assigns the authority. A shared file would be a seventh restatement |
| 2 | **Land both hardening guards** *(user)* | Each closes a gap this defect walked through. Four independent discoveries, none of which fixed it, is the argument for guarding rather than observing |
| 3 | **Park the fifth instance as E-011, don't fix it** *(user)* | Widening the grammar line would widen the union for all three tracks and weaken the guard everywhere — a design change, not hardening |
| 4 | **Leave the frontmatter stage-chains alone** — both `diagnose-bug`'s and `make-bugfix-request`'s *(user, en bloc)* | They live in the description that drives skill **dispatch**, where "root cause" is the English phrase a user actually types. Degrading dispatch for consistency in an ungraded sentence is a bad trade. Both sites named, so neither is re-chased |
| 5 | **Phase 1 stays atomic** *(user, en bloc)* | The suite cannot be green partway; a half-landed rename actively misdirects the next pipeline run. Grouping steps by defect inside one phase preserves diff reviewability without ever pushing a knowingly-red branch |
| 6 | **Align `create-implementation-plan`'s track resolution too, in Phase 2** *(user, en bloc)* | Its own stage word is right for every track, so this is adjacent rather than required — but one sentence, and divergence between the two back-half skills is how the next drift starts |
| 7 | **`Bears on: H2` for E-010** *(user, overriding the panel)* | The panel recommended `post-v1` "with eyes open"; the user chose the nearer moment because an entry parked at `post-v1` is the least likely to be reopened, which is the queue's own failure mode |
| 8 | **Declined: a guard over the stage-discovery readers** | Recorded here rather than buried, because it is the most consequential decline. Their phrasing is free prose with no stable anchor, so a regex over it would be fragile and would pin wording the fix should be free to improve. They are fixed in Phase 1 and left ungoverned; the honest cost is that a future rename can break them silently again |
| 9 | **Declined: a `next:`-field guard** | RCA hardening (a). The `next:` value is advisory routing, not a stage claim, and guarding it would pin phrasing across six skills for no invariant |

## 6. Risks & gotchas

1. **The `<placeholder>` trap** — the single most tempting wrong move, and it makes the guard vacuous
   rather than green. Named in Phase 1's acceptance because a note is not enough.
2. **`_advance_status_section` is fence-blind.** The window ends at the first `^##` heading, which in
   both files sits *inside* a code fence — so the window includes the fence and the template. Prose
   below the fence opening is still inside the window; the failure mode is adding prose *after* the
   next `##`, which is outside. Verify mechanically (Phase 1 step 10), never by eye.
3. **Editing the skill you are executing.** Phase 1 changes `implement-plan/SKILL.md` while
   `/implement-plan` is running from context loaded at invocation. Re-read from disk before Step 7.
4. **`git mv` stages a rename from the index, not the working tree.** If the close-out edits a file's
   status and then moves the directory, the move carries the *pre-edit* content unless the edit was
   staged first. This exact mistake reddened CI on the previous item; the tells are a `| 0` line in
   `git diff --cached --stat` and `rename (100%)` in the commit output.
5. **This is the bugfix track's first complete run.** If anything about the `_done/` move surprises
   you, that is new information about the track contract and belongs in the report, not a silent
   workaround.
6. **Keyword-satisfiable regexes** — see §4. Passing is necessary, not sufficient.

## 7. Files to touch (checklist)

- [ ] `.claude/skills/create-implementation-plan/SKILL.md` — `plan` → `planned` (×3); sibling-rollover bullet; three-valued resolution; the two stage-discovery readers; authority line; the duplicate work-dir template in its opening section
- [ ] `.claude/skills/implement-plan/SKILL.md` — sibling-rollover bullet; three-valued resolution (**both** halves: work-dir *and* track-README path); track-derived terminal; `:29` and `:324`; the stage-discovery reader; authority line; the duplicate work-dir template
- [ ] `.claude/skills/diagnose-bug/SKILL.md` — `root-cause` → `diagnosed` (template + Step 5), preserving "(or the terminal stage word)"; authority line
- [ ] `.claude/skills/make-bugfix-request/SKILL.md` — `next: root-cause` → `next: diagnose`; authority line
- [ ] `.claude/skills/scope-feature/SKILL.md` — authority line only (it is already correct)
- [ ] `.claude/skills/make-feature-request/SKILL.md` — authority line only
- [ ] `.claude/skills/update-docs/SKILL.md` — the both-invariants note
- [ ] `tests/test_repo_structure.py` — two new guards + the per-track helper (Phase 3 only)
- [ ] `ESCALATIONS.md` — E-010 and E-011
- [ ] This directory's four artifacts + the bugfix Index — rolled to `fixed` **by Step 7**, not by a phase here

## 8. Conventions (bake these in)

- **Commits go through `/commit` only.** Never `git commit` ad hoc, never `--amend`, never force-push,
  never push `main`, never `git merge`.
- **Subagent git is read-only** — no `checkout`/`reset`/`restore`/`clean`/`stash`.
- **`ROADMAP.md` statuses are advanced by `/commit` against the diff.** Expect "no roadmap change" here.
- **The repo is public** — no machine-specific paths, ids, or personal identifiers in tracked files,
  this plan and the `reviews/` trail included.
- **Windows dev, Linux CI.** Never write files with PowerShell `Set-Content`/`Out-File` — in PS 5.1 they
  mangle UTF-8 and add a BOM. Use the file-editing tools.
- **mypy is strict over `src` and `tests`** — full annotations, zero new `# type: ignore`.
- **ruff `line-length = 100`**; PTH forbids bare `open()`.
- *Not applicable, stated so nobody reaches for them:* resolve-by-name, the append-only ledger, ruleset
  immutability, cost-side-only pricing. **This change touches no data at all** — no dataset, no
  manifest, no ledger, no ruleset, no economy, nothing under `src/` or `app/`, no cloud spend. That is
  why this plan carries **no data-contracts section**: an argued omission, not an oversight.

## 9. Code-grounding verification

**37 code references emitted by the panel; a sample independently re-verified against the working tree
before this plan was written; 0 unresolvable.** Panel health: 3/3 planners, 2/2 adversaries, 1/1
meta-audit, 0 degraded lenses, 37 findings (2 blockers, 14 majors), no refutations.

Independently confirmed by re-reading the files, not taken on trust:

| Claim | Verified |
|---|---|
| `SKILL_STATUS_TEMPLATE` cannot match `<placeholder>` | **True** — pattern is `[a-z-]+`; a match attempt against `> **Status:** <placeholder>` returns `False` |
| `requests/<track>-requests/…` cannot compose for calibration | **True** — the directories are `feature-requests`, `bugfix-requests`, `calibration-findings` |
| `implement-plan:29` and `:324` are track-blind restatements | **True**, both verbatim, both outside every guarded window |
| The `_advance_status_section` windows contain the markdown fence | **True** — 167→184 and 254→276, both containing ```` ```markdown ```` |
| `_done/1.1-app-shell/reviews/preflight.md` opens at an undeclared `preflight` | **True** |
| `requests/README.md` calls each track README "the contract" | **True** |

**Two blockers were applied rather than asked**, both objective sequencing errors: the preflight gate
pinned `HEAD` to a commit that cannot be current when the plan executes (replaced with a decision
table), and the close-out phase duplicated `/implement-plan`'s own Step 7 while archiving the plan out
from under the run still executing it (removed; folded into the hand-off note). Fourteen majors and the
citation corrections — including a report-template line range that overshot its fence by three lines —
are applied throughout.

## References

- `requests/bugfix-requests/pipeline-status-rollover/ROOT_CAUSE_ANALYSIS.md` — the decided upstream artifact
- `requests/bugfix-requests/pipeline-status-rollover/BUGFIX_REQUEST.md` — the intake
- `reviews/plan-proposals.md` · `reviews/plan-adversarial.md` — this panel's raw trail
- `requests/bugfix-requests/README.md` — the track contract and the Definition of Done
- `requests/README.md` — each track README is the contract for its grammar
- `tests/test_repo_structure.py` — the repro, the guards, and the regexes that grade the prose
- `.claude/skills/scope-feature/SKILL.md` — the reference implementation

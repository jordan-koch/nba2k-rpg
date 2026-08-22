# Planning Panel — Raw Proposals

Raw, unfiltered output from the three divergent planners. Kept verbatim so the
trail survives the merge's trimming.


---

## Planner: 0

```json
{
  "planner": "code-grounded",
  "ok": true,
  "onboarding_files": [
    {
      "path": "requests/bugfix-requests/pipeline-status-rollover/ROOT_CAUSE_ANALYSIS.md",
      "why": "The decided upstream artifact. Consume it, do not re-open it. Its Verdict (confirmed-bug, four instances across three skills), its red-repro table (lines 28-32), its four-instance evidence (lines 62-85), and its tiered fix posture (lines 118-135) are the contract this plan executes. Note its own Status line opens at `diagnosed`, not `root-cause` — that was defect 4 being avoided in the act of writing."
    },
    {
      "path": "requests/bugfix-requests/pipeline-status-rollover/BUGFIX_REQUEST.md",
      "why": "Context only. Its `Affected Area & Pointers` (lines 69-83) is the fastest map of the touched files, and its Open Questions (lines 91-106) are what the RCA answered — question 1 left one design call explicitly to this plan (`shared prose home vs guard-and-keep-the-restatements`), which Phase 4 decides."
    },
    {
      "path": "tests/test_repo_structure.py",
      "why": "The whole mechanical contract lives here. Lines 32-60 are the module-level constants the three red tests key off (`SKILL_STATUS_TEMPLATE`, `ROLLS_A_SIBLING`, `TERMINAL_TOKENS`, `DERIVES_TERMINAL`); lines 63-80 are the two helpers (`_declared_stage_tokens`, `_advance_status_section`) that decide WHERE in a skill file a phrase must land to count. Read these before editing any SKILL.md — the fix is prose, but the acceptance is regex."
    },
    {
      "path": ".claude/skills/scope-feature/SKILL.md",
      "why": "Lines 136-149 are the CORRECT pattern the fix copies. `:139` rolls the sibling, `:140-143` sets the Index cell, `:144` opens the new artifact, `:149` is the template blockquote. Whatever Phases 1-3 write into the other two skills should read like this."
    },
    {
      "path": ".claude/skills/create-implementation-plan/SKILL.md",
      "why": "Defect 1 + defect 2 live here. Step 5 at lines 158-183 (missing the rollover bullet; writes `plan` at :172, :173, :176), and Step 1's lookup prose at :56 and :65-66 which also says `root-cause` — collateral instances the RCA's four-instance count did not enumerate."
    },
    {
      "path": ".claude/skills/implement-plan/SKILL.md",
      "why": "Defect 1 + defect 3 live here. Step 7 at lines 251-275 (no rollover bullet; hardcodes `implemented` at :259 and :268), plus :29, :61, :92-93 and :324 which restate `plan`/`implemented` as track-blind literals."
    },
    {
      "path": ".claude/skills/diagnose-bug/SKILL.md",
      "why": "Defect 4. `:107` writes `root-cause` in the template blockquote and `:97` and `:154` restate it in prose. Its Step 5 at :150-154 is simultaneously the SECOND correct rollover pattern (`Status blockquote` at :152) and the tolerated track-derived-terminal shape (`or the terminal stage word` at :154) — the two phrases `ROLLS_A_SIBLING` and `DERIVES_TERMINAL` were written to match."
    },
    {
      "path": "requests/bugfix-requests/README.md",
      "why": "This item's own track contract. `:86` declares the grammar `intake → diagnosed → planned → fixed` — the authority the fix makes real. `:37-46` is the Definition of Done (red repro goes green + regression test left behind). `:96-98` is the Index row this item's rollover must move."
    },
    {
      "path": "requests/feature-requests/README.md",
      "why": "`:104` declares the four-field Status blockquote shape and `:106` the feature grammar. `:96-100` is the `_done/` archive convention Phase 6 executes, and `:112-117` shows two already-archived items whose Index links point into `_done/` — the shape this item's row must end in."
    }
  ],
  "architecture_notes": "TOUCHED AREA: process documentation and one structural test module. Nothing under `src/`, `app/`, `careers/`, `datasets/`, or `rulesets/` is touched — verified by grepping the eight skill directories for stage tokens: only `SKILL.md` files carry them, and the three panel scripts (`create-implementation-plan/plan_panel.js`, `implement-plan/acceptance_panel.js`, `scope-feature/scope_panel.js`) contain no stage-word literals at all. So no ledger, no ruleset version, no dataset manifest entry, and no ADR 0008 pricing surface is in scope. There is consequently no data-contracts section in this plan, and no verification phase for `docs/data-access.md` — this change depends on no external source claim.\n\nTHE STRUCTURE AS IT ACTUALLY IS\n\nThree track READMEs each declare exactly one status grammar on a single line matched by `STATUS_GRAMMAR = re.compile(r\"\\*\\*Status grammar:\\*\\*\\s*(?P<tokens>.+)\")` (tests/test_repo_structure.py:38):\n  - requests/feature-requests/README.md:106 — `intake → scoped → planned → implemented`\n  - requests/bugfix-requests/README.md:86 — `intake → diagnosed → planned → fixed`\n  - requests/calibration-findings/README.md:88 — `intake → diagnosed → planned → retuned`\n`_declared_stage_tokens()` (tests/test_repo_structure.py:63-71) unions the backticked words out of those three lines into `{diagnosed, fixed, implemented, intake, planned, retuned, scoped}` — confirmed verbatim in the current red output.\n\nSix pipeline skills each restate that vocabulary as a literal template blockquote, with no mechanical link back to the READMEs. Grepped and confirmed, one per skill:\n  scope-feature:149 `scoped` · make-feature-request:176 `intake` · make-bugfix-request:130 `intake` · diagnose-bug:107 `root-cause` · create-implementation-plan:176 `plan` · implement-plan:268 `implemented`.\nTwo of those six are not in the declared union. That is defect 2 and defect 4.\n\nTWO INVARIANTS, ONE GUARDED — this is the architectural fact the fix hangs on.\n  Invariant A: the Index cell agrees with every `*.md` in the item directory. Guarded since before this bug by `test_index_stage_cells_match_their_artifact_status_headers` (tests/test_repo_structure.py:454-487). Note its loop at :479 is `item_dir.glob(\"*.md\")` — NON-recursive, so `reviews/` is exempt. That is why `_done/1.1-app-shell/reviews/preflight.md` can carry `> **Status:** preflight` (a word no grammar declares) and stay green. It also follows the Index link, so `_done/` directories ARE checked by this guard, unlike test_request_links.py which skips them at :41.\n  Invariant B: the word is one the track's grammar contains. Guarded by nothing until the repro landed. A skill writing a made-up token CONSISTENTLY into both the Index and its own artifact satisfies A perfectly — which is exactly why defects 2, 3 and 4 were silent and only defect 1 was loud.\n\nTHE THREE SEAMS THE FIX HOOKS INTO — all three are regex-shaped, so the prose must land in a specific REGION of a specific file, not merely somewhere in it.\n\n  Seam 1 — `_advance_status_section(body)` (tests/test_repo_structure.py:74-80). It finds the FIRST case-insensitive match of `advance status` (`ADVANCE_STATUS`, :52) and slices to the first following `^##\\s` (`NEXT_SECTION`, :53). That regex is fence-blind, so the slice stops at the first `##` heading INSIDE the fenced template. Measured boundaries today:\n    - scope-feature: 136 → 152 (stops at `## Fit Verdict`, :153)\n    - diagnose-bug: 150 → 176 (stops at `## What good looks like`, :177)\n    - create-implementation-plan: 167 → 183 (stops at `## 1. Onboarding`, :184)\n    - implement-plan: 254 → 275 (stops at `## 1. Acceptance ledger`, :276)\n  Every phrase Phases 1 and 3 add must land inside those windows.\n\n  Seam 2 — `ROLLS_A_SIBLING = re.compile(r\"Status blockquote|sibling|every artifact\", re.IGNORECASE)` (:55), applied only to the seam-1 slice, for the four names in `STAGE_ADVANCING_SKILLS` (:46-51). `scope-feature:139` and `diagnose-bug:152` both match via the literal words \"Status blockquote\".\n\n  Seam 3 — `DERIVES_TERMINAL = re.compile(r\"terminal (?:stage word|token)|track's terminal\", re.IGNORECASE)` OR `len(named) > 1` where `named` is the subset of `TERMINAL_TOKENS = {implemented, fixed, retuned}` (:59) appearing as substrings in implement-plan's seam-1 slice (:342-353). `diagnose-bug:154` — \"(or the terminal stage word)\" — is the in-repo precedent for the phrase.\n\n  Seam 4 — `SKILL_STATUS_TEMPLATE = re.compile(r\"^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)\", re.MULTILINE)` (:41), applied to the WHOLE file for every `.claude/skills/*/SKILL.md`. Two consequences worth knowing before editing: a `> **Status:** <placeholder>` line matches nothing (`<` is outside `[a-z-]`) and would silently make that skill invisible to the guard — so the template must keep a real, declared word; and an HTML comment beside the template is NOT scanned, so a comment naming the other tracks' terminals is safe.\n\nWHY A SHARED PROSE HOME IS NOT THE ANSWER (this plan's answer to RCA Open Question 1's remainder). The template blockquote is the thing a cold agent COPIES — see scope-feature:148-149, where the fenced block is literally the artifact's first line. Moving it to a seventh file makes the copy source a second hop and does not remove the restatement, because each skill still needs a concrete example inline. And ESCALATIONS.md:25-40 shows this repo already treats \"one more register\" as a cost requiring an explicit boundary argument. The durable fix is the one the RCA already named and already wrote: make the READMEs mechanically authoritative and keep the restatements pointed at them. Phase 4 makes each restatement cite its authority; Phase 5 closes the one remaining unguarded surface (the Index cell itself).\n\nSCOPE FOUND BEYOND THE RCA'S FOUR INSTANCES — and it is functional, not cosmetic. `implement-plan/SKILL.md:61` tells the agent to look in the Index \"for an item at the `plan` stage\", and `:92-93` says a ready plan reads `plan · … · decided`. Once Phase 2 makes stage 3 write `planned`, those two lines actively misdirect the next stage-4 run. Likewise `create-implementation-plan/SKILL.md:56` and `:65-66` say a ready bugfix RCA reads `root-cause`, which Phase 2 makes false. No test covers these (they are not `> **Status:**` blockquote lines), so they must be fixed by hand in the same phase as the token they mirror. This is the RCA's \"the six restatements remain six\" made concrete.",
  "phases": [
    {
      "name": "Phase 0 — Baseline and orientation (no edits)",
      "goal": "Confirm the implementer starts from exactly the state this plan was written against, so a surprise is a real signal rather than drift.",
      "steps": [
        "Confirm the branch: `git branch --show-current` should print `bugfix/pipeline-status-rollover`. HEAD should be `fb0406e Diagnose the pipeline status drift and land its red repro` — the RCA's line 34 says the repro was 'not yet committed', which was true when written; it has since landed, and `git ls-files requests/bugfix-requests` shows BUGFIX_REQUEST.md and ROOT_CAUSE_ANALYSIS.md tracked. Do NOT re-land the repro.",
        "Run `uv run pytest -q`. Expected: `3 failed, 79 passed` — exactly the three named in the RCA's table at lines 28-32. Any other failure is pre-existing drift; stop and report it rather than folding it in.",
        "Run `uv run ruff check`, `uv run ruff format --check` and `uv run mypy`. All three are clean today (measured: 'All checks passed!', 'Success: no issues found in 16 source files'). This is the baseline every later phase must return to.",
        "Read tests/test_repo_structure.py:32-80 — the constants and the two helpers. Specifically internalize that `_advance_status_section` (:74-80) slices from the first 'advance status' to the first following `^##`, and that the slice therefore STOPS INSIDE the fenced template block. Every phrase added in Phases 1 and 3 must land before that boundary.",
        "Note the one-way hazard now, before touching anything: do NOT introduce the string 'advance status' anywhere EARLIER in create-implementation-plan/SKILL.md or implement-plan/SKILL.md than its current position (:167 and :254 respectively). `ADVANCE_STATUS.search` takes the FIRST match; an earlier one silently relocates the window all three seams depend on."
      ],
      "acceptance": [
        "`uv run pytest -q` reports exactly 3 failures and 79 passes, and the three failing node ids are `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares`, `test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory`, `test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token`.",
        "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` all exit 0.",
        "No file has been modified: `git status --short` is empty."
      ],
      "commit_note": "No commit. This phase reads only."
    },
    {
      "name": "Phase 1 — Defect 1: the sibling-rollover instruction",
      "goal": "Make `create-implementation-plan` Step 5 and `implement-plan` Step 7 tell you to roll the artifacts already sitting in the directory, matching the pattern `scope-feature/SKILL.md:139` and `diagnose-bug/SKILL.md:152` already use. This is the blocking defect — the only one of the four that reds a build today.",
      "steps": [
        "Read `.claude/skills/scope-feature/SKILL.md:136-146` first. It is the pattern: `:139` rolls the sibling ('Set the request's Status blockquote to `scoped`'), `:140-143` sets the Index cell, `:144` opens the new artifact. Copy its shape, not its words verbatim — stage 3 and 4 have MORE than one sibling.",
        "In `.claude/skills/create-implementation-plan/SKILL.md`, inside Step 5's advance-status region (currently :167-183, between 'Then advance status' at :167 and the fenced template's `## 1. Onboarding` at :184), add a bullet BEFORE the existing Index bullet at :170-172. Prescribed text: '- Roll **every artifact already in `<work-dir>`** — set each one\\'s Status blockquote to `planned`: `FEATURE_REQUEST.md` + `PROJECT_SCOPE.md` for a feature, `BUGFIX_REQUEST.md` + `ROOT_CAUSE_ANALYSIS.md` for a bug. Only `*.md` directly in the item directory — `reviews/` is exempt.'",
        "The `reviews/` carve-out in that bullet is load-bearing and must not be dropped: `test_index_stage_cells_match_their_artifact_status_headers` globs `item_dir.glob(\"*.md\")` at tests/test_repo_structure.py:479, which is non-recursive. `_done/1.1-app-shell/reviews/preflight.md` carries `> **Status:** preflight` — a word no grammar declares — and is green precisely because of that. An implementer who rolls `reviews/` too is doing unnecessary and misleading work.",
        "In `.claude/skills/implement-plan/SKILL.md`, inside Step 7's advance-status region (currently :254-275, between 'Then advance status' at :254 and `## 1. Acceptance ledger` at :276), add the equivalent bullet BEFORE the Index bullet at :257-259. Prescribed text: '- Roll **every artifact already in `<work-dir>`** — set each one\\'s Status blockquote to the resolved track\\'s terminal stage word. That is the intake doc, the upstream artifact, and `IMPLEMENTATION_PLAN.md`; `reviews/` is exempt. They move together with the Index cell, never after it.' (Phase 3 supplies what 'terminal stage word' resolves to; the phrase can land here now and satisfies both seam 2 and seam 3.)",
        "Apply both edits by EXACT-TEXT match, never by line number — the second edit shifts nothing in the first file, but Phase 2 will shift line numbers inside both.",
        "Re-run `uv run pytest tests/test_repo_structure.py -q`. `test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory` must flip to green; the other two stay red."
      ],
      "acceptance": [
        "`uv run pytest tests/test_repo_structure.py::test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory -q` is GREEN.",
        "`uv run pytest -q` reports `2 failed, 80 passed` — one fewer failure than Phase 0, no new ones.",
        "Grepping `.claude/skills/create-implementation-plan/SKILL.md` for `advance status` still returns exactly one hit, and it is still the Step 5 occurrence. Same for `implement-plan/SKILL.md` and its Step 7 occurrence.",
        "Both new bullets name `reviews/` as exempt.",
        "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` still exit 0 (no Python was touched, so this is a no-regression check)."
      ],
      "commit_note": "Roll the sibling artifacts in the stage-3 and stage-4 skills. Copies the pattern at scope-feature/SKILL.md:139 into create-implementation-plan Step 5 and implement-plan Step 7, with the reviews/ carve-out made explicit. Turns test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory green. Run /commit — never `git commit` ad hoc."
    },
    {
      "name": "Phase 2 — Defects 2 and 4: tokens no grammar declares",
      "goal": "Make every stage word a pipeline skill instructs one that its track README actually declares — including the prose restatements no test can see, which become actively wrong the moment the template is fixed.",
      "steps": [
        "In `.claude/skills/create-implementation-plan/SKILL.md`, replace `plan` with `planned` at all four sites: `:172` ('set this item\\'s **Index** row Stage cell to `plan`'), `:173` ('opens at stage `plan`'), `:176` (the template blockquote `> **Status:** plan · created …`), and `:65-66` in Step 1's disposition gate ('a ready scope correctly reads `scoped · … · decided · next: plan`' — that `next: plan` is the NEXT-STAGE field and stays `plan`; the change here is only if a stage-word literal appears). Read each site before editing: at :65-66 the words `plan` appear twice with different meanings, and only the stage-word sense changes.",
        "Still in that file, fix the Step 1 lookup at `:56`: 'or `requests/bugfix-requests/README.md` for a confirmed-bug RCA at `root-cause`' → `at \\`diagnosed\\``. Then `:65-66`: 'a ready bugfix RCA reads `root-cause · … · decided · next: plan`' → '`diagnosed · … · decided · next: plan`'. These two are NOT covered by any test — they are prose, not `> **Status:**` blockquotes — but they are the lookup instructions the next bugfix run follows, and Phase 2 makes them false if left.",
        "In `.claude/skills/diagnose-bug/SKILL.md`, replace `root-cause` with `diagnosed` at `:97` ('**`confirmed-bug`** → `root-cause · … · decided · next: plan`'), `:107` (the template blockquote), and `:154` ('header) to `root-cause` (or the terminal stage word)'). Do NOT touch the trailing '(or the terminal stage word)' clause at :154 — it is the tolerated shape the RCA cites at line 107-108 and the in-repo precedent Phase 3 copies.",
        "In `.claude/skills/implement-plan/SKILL.md`, fix the two stage-word restatements that Phase 2 invalidates: `:61` ('for an item at the `plan` stage') → '`planned`', and `:92-93` ('a ready plan reads `plan · … · decided · next: implement`, so the word `plan` appearing is *expected*') → '`planned · … · decided · next: implement`, so the word `planned` appearing is *expected*'. The parenthetical's point — gate on the disposition, not the stage word — survives unchanged.",
        "Sanity-grep afterwards: `rg '`(plan|root-cause)`' .claude/skills/*/SKILL.md` should return only occurrences where `plan` means the stage NAME or the artifact (e.g. `next: plan`, `IMPLEMENTATION_PLAN.md`), never a Status stage word.",
        "Re-run `uv run pytest tests/test_repo_structure.py -q`. `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` must flip green — its red output today is exactly `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}`."
      ],
      "acceptance": [
        "`uv run pytest tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares -q` is GREEN.",
        "`uv run pytest -q` reports `1 failed, 81 passed`; the only remaining failure is `test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token`.",
        "Every `> **Status:** <word>` line across all eight `.claude/skills/*/SKILL.md` files carries a word in `{intake, scoped, diagnosed, planned, implemented, fixed, retuned}`. Verify by grep, not by assertion: `rg '^>\\s*\\*\\*Status:\\*\\*\\s*([a-z-]+)' .claude/skills -g '**/SKILL.md'` returns six lines and every stage word is declared.",
        "`create-implementation-plan/SKILL.md:56` and `:65-66` (or their post-edit equivalents) say `diagnosed`, not `root-cause`; `implement-plan/SKILL.md:61` and `:92-93` say `planned`, not `plan`.",
        "ruff check, ruff format --check, mypy all still exit 0."
      ],
      "commit_note": "Use the stage words the track READMEs actually declare. `plan` → `planned` in create-implementation-plan and `root-cause` → `diagnosed` in diagnose-bug, in the templates AND in the lookup prose that mirrors them. Turns test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares green. Run /commit."
    },
    {
      "name": "Phase 3 — Defect 3: a track-derived terminal",
      "goal": "Stop `implement-plan` from writing one track's terminal word while serving all three. Feature ends at `implemented`, bugfix at `fixed`, calibration at `retuned` — and it is the last stage, so nothing downstream is left to notice a wrong one.",
      "steps": [
        "Read `.claude/skills/implement-plan/SKILL.md:53-55` first — Step 1 already resolves `<track>` from the upstream artifact path ('`<track>` = `bugfix` when the upstream path is under `bugfix-requests/`, else `feature`'). The terminal word follows from that same resolution; no new machinery is needed. This is the RCA's answer to Open Question 2 (its lines 105-108).",
        "In Step 7's advance-status region, rewrite the Index bullet at `:257-259` so it names the word per track rather than hardcoding one. Prescribed text: '- In the **track README** … set this item\\'s **Index** row Stage cell to **the resolved track\\'s terminal stage word** — `implemented` (feature) · `fixed` (bugfix) · `retuned` (calibration) — matching the row by its `[<slug>]` link.'",
        "Rewrite `:260` the same way: '- The report opens at the same terminal stage word · created <today> · decided · next: commit.'",
        "Leave the template blockquote at `:268` reading `> **Status:** implemented · …` — do NOT replace `implemented` with a `<placeholder>`. A placeholder is invisible to `SKILL_STATUS_TEMPLATE` (tests/test_repo_structure.py:41), whose `[a-z-]+` cannot match a leading `<`, so this skill would silently drop out of the conformance guard's coverage. Instead add an HTML comment directly beneath it, following the existing precedent at create-implementation-plan/SKILL.md:177-178: '<!-- `implemented` is the FEATURE track\\'s terminal stage word. Write the RESOLVED track\\'s: feature → `implemented` · bugfix → `fixed` · calibration → `retuned`. -->'",
        "Fix the two track-blind restatements outside the guarded region: `:29` ('The feature ends at status `implemented`.') → 'The item ends at its track\\'s terminal stage word — `implemented`, `fixed`, or `retuned`.'; and `:324` ('the report + `implemented` status') → 'the report + the terminal status'.",
        "Confirm the phrasing satisfies BOTH halves of the assertion at tests/test_repo_structure.py:349 — `DERIVES_TERMINAL` matches on 'terminal stage word', AND `named` now contains all three of `{implemented, fixed, retuned}` so `len(named) > 1`. Belt and braces: if a later edit rewords the phrase, the token list still holds.",
        "Re-run the full suite. All three repro tests are now green — this is the bugfix track's Definition of Done (requests/bugfix-requests/README.md:37)."
      ],
      "acceptance": [
        "`uv run pytest tests/test_repo_structure.py::test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token -q` is GREEN.",
        "`uv run pytest -q` reports `82 passed, 0 failed` — the red repro is fully green and all 79 originally-passing tests still pass.",
        "The template blockquote at implement-plan/SKILL.md still matches `SKILL_STATUS_TEMPLATE` with a DECLARED word — verify the conformance test still names `implement-plan` in its scan by temporarily asserting, or simply confirm the line still reads `> **Status:** implemented`.",
        "`implement-plan/SKILL.md` no longer contains a sentence asserting that the terminal status is `implemented` unconditionally: `:29` and `:324` both name the per-track variation.",
        "ruff check, ruff format --check, mypy all exit 0."
      ],
      "commit_note": "Derive the terminal stage word from the resolved track. implement-plan serves all three tracks, whose terminals differ; Step 7 now names each, and Step 1's existing path-based track resolution supplies the answer. All three red repro tests are now green. Run /commit."
    },
    {
      "name": "Phase 4 — Point each restatement at its authority (the Open-Question-1 call)",
      "goal": "Settle the design call the RCA left open at its lines 99-104: whether the skills get a shared prose home. Decision: NO shared home — keep the six restatements, and make each one cite the track README as the source of truth. The guard is what stops drift; a seventh file would not.",
      "steps": [
        "Record the decision in the plan's Decisions section with its three grounds: (1) the template blockquote is the thing an agent COPIES — see scope-feature/SKILL.md:148-149 where the fence IS the artifact's first line — so a pointer-only skill adds a hop without removing the restatement; (2) requests/README.md:16 already declares each track README 'the contract', so the authority exists and only the citation is missing; (3) ESCALATIONS.md:25-40 shows this repo charges an explicit boundary argument for every new register, and a seventh vocabulary home would owe one.",
        "Add ONE sentence beside each of the six template blockquotes naming its authority. `create-implementation-plan/SKILL.md:177-178` already does this — it cites 'this README status grammar' — and is the model; the irony the RCA notes at its line 72-74 (it cited the authority while violating it) disappears once Phase 2 has landed. Prescribed shape: '<!-- The stage word comes from the resolved track README\\'s **Status grammar** line (requests/<track>-requests/README.md), which is the source of truth. tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares enforces it. -->'",
        "Apply it to the four skills that still lack it: scope-feature (beside :149), diagnose-bug (beside :107), make-feature-request (beside :176), make-bugfix-request (beside :130). implement-plan gets the version written in Phase 3; create-implementation-plan's existing :177-178 comment gets the test name appended.",
        "Add a matching line to `.claude/skills/update-docs/SKILL.md`, in the 'requests/ — do the Index rows match the artifacts?' section at :131-135, naming the grammar as the second thing to reconcile against. That section currently says only that the Index mirrors the blockquote (invariant A) and never that either must be a declared word (invariant B) — the exact asymmetry the RCA identifies at its lines 45-55.",
        "Do NOT create a new shared file. Do NOT move the templates. Do NOT add a `docs/decisions/00NN-*.md` ADR for this — no ADR is being invalidated or added; verify with `uv run pytest tests/test_repo_structure.py::test_every_adr_is_listed_in_the_index` and `::test_adr_numbers_are_unique_and_contiguous`, both of which must stay green untouched."
      ],
      "acceptance": [
        "All six `.claude/skills/*/SKILL.md` template blockquotes have an adjacent comment naming `requests/<track>-requests/README.md` as the source of truth and naming the enforcing test.",
        "`.claude/skills/update-docs/SKILL.md`'s requests/ section names BOTH invariants: the Index mirrors the blockquote, AND both must be words the track's Status grammar declares.",
        "`uv run pytest -q` is still `82 passed` — the comments are inert to every guard, which is the point: they are documentation, and the test is the enforcement.",
        "No new file was created under `.claude/skills/` or `docs/`: `git status --short` shows only modifications, no additions.",
        "ruff check, ruff format --check, mypy all exit 0."
      ],
      "commit_note": "Cite the authority beside every stage-word restatement. Answers the RCA's Open Question 1: the six restatements stay (the template is the copy source), each now points at its track README and at the test that enforces it. No new register. Run /commit."
    },
    {
      "name": "Phase 5 — Hardening, gated: close the Index-cell gap and the next-field token",
      "goal": "Take the two hardening items from the RCA's lines 130-135 that are cheap and clean, and decline the third with a reason. This is the RCA's explicitly gated tier — if the acceptance panel or the user judges it scope creep, this is the ONE phase in this plan that may be dropped whole without weakening the Definition of Done.",
      "steps": [
        "Hardening (b) — the Index cell is checked against artifacts but never against the grammar. Refactor `_declared_stage_tokens()` (tests/test_repo_structure.py:63-71) into a per-track helper: `def _declared_stage_tokens(track: str) -> set[str]` returning one track's tokens, plus a thin `_all_declared_stage_tokens() -> set[str]` that unions the three. Keep the union call site in `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` at :280 working unchanged. Annotate both for mypy strict.",
        "Add `test_index_stage_cells_use_only_their_own_track_s_grammar()`. Reuse the `stage_cell` regex already written at :465 (`^\\|\\s*\\[(?P<slug>[^\\]]+)\\]\\((?P<link>[^)]+)\\)\\s*\\|\\s*(?P<stage>\\w+)`), iterate `REQUEST_TRACKS`, and assert each matched row's stage word is in that track's declared set. Note it is GREEN today — feature rows read `implemented`, the bugfix row reads `diagnosed` — so it is a pure regression guard, and the calibration README's placeholder row at :94 does not match the regex (no `[slug](link)`), so the empty track is handled by construction rather than by a special case.",
        "Hardening (a) — the `next:` field. `make-bugfix-request/SKILL.md:130` writes `next: root-cause`, a word no grammar declares. Fix it to `next: diagnose`, matching the stage NAME in that track's pipeline table (requests/bugfix-requests/README.md:20 calls stage 2 'Diagnose'). Add one clause to each track README's grammar block declaring the field: 'The `next:` field names the **stage that runs next** from the pipeline table above, or `none`.'",
        "DECLINE a mechanical guard on `next:`, and record why: its live values include free-form targets — `<feature-slug>` at diagnose-bug/SKILL.md:102, `commit` at implement-plan/SKILL.md:268, `—` in the archived 1.1 artifacts — so any regex is either vacuous or wrong. A declared sentence plus the one-word fix is the honest stopping point.",
        "DECLINE hardening (c) — the `_done/` skip. It is at tests/test_request_links.py:41, not `:36` as both upstream artifacts state (`:36` is the `def _scanned_files()` line); note the correction. The skip is deliberate and documented at that module's :19-20, and the failure it caused — a finding archived into a tree nobody reopens — is precisely what ROADMAP.md:197's H1 `escalation-queue` (Status DONE) now exists to catch. Re-litigating it here would duplicate a harness row that already landed.",
        "Re-run everything, including mypy — this is the only phase that touches Python."
      ],
      "acceptance": [
        "A new test `test_index_stage_cells_use_only_their_own_track_s_grammar` exists in tests/test_repo_structure.py and is GREEN against the repo as-is.",
        "Prove it actually bites, don't assert it: temporarily edit one Index Stage cell to a bogus word, confirm the new test goes RED naming that row, then revert. Record the red output in the implementation report.",
        "`_declared_stage_tokens` is now per-track and `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` still passes unchanged.",
        "`make-bugfix-request/SKILL.md` writes `next: diagnose`; all three track READMEs declare what the `next:` field contains.",
        "`uv run pytest -q` reports `83 passed` (82 + the new guard), `uv run ruff check` and `uv run ruff format --check` pass, `uv run mypy` reports success on 16 source files with no new `Any` or untyped-def errors.",
        "The declined items (a-guard and c) are written into the plan's Decisions with their reasons, so the next reader does not re-chase them."
      ],
      "commit_note": "Guard the Index cell against its own track's grammar, and fix the one non-grammar `next:` token. Closes hardening (a) and (b) from the RCA; (c) is declined — the `_done/` skip at tests/test_request_links.py:41 is deliberate and its cost is what ROADMAP H1 already addresses. Run /commit."
    },
    {
      "name": "Phase 6 — Dogfood: run the fixed instructions on this very item",
      "goal": "The strongest available acceptance for a bug about instructions is to follow the fixed instructions and stay green. This item is itself a bugfix at stage `planned` with three sibling artifacts — exactly the shape defect 1 breaks. This phase merges with `/implement-plan`'s Step 7 rather than duplicating it.",
      "steps": [
        "Confirm the starting state matches what stage 3 should have left: `requests/bugfix-requests/README.md`'s Index row for `pipeline-status-rollover` reads `planned`, and BUGFIX_REQUEST.md, ROOT_CAUSE_ANALYSIS.md and IMPLEMENTATION_PLAN.md all carry `> **Status:** planned`. If the Index says `plan` or a sibling still says `diagnosed`, that IS defect 1 and defect 2 caught live — fix it here and say so in the report, because it is direct evidence the fix was needed.",
        "Write `IMPLEMENTATION_REPORT.md` following the NOW-FIXED implement-plan Step 7: it opens at `fixed` (the BUGFIX track's terminal stage word), not `implemented`.",
        "Roll every `*.md` directly in `requests/bugfix-requests/pipeline-status-rollover/` to `fixed` — BUGFIX_REQUEST.md, ROOT_CAUSE_ANALYSIS.md, IMPLEMENTATION_PLAN.md, IMPLEMENTATION_REPORT.md. Leave `reviews/` alone.",
        "Set the Index Stage cell at requests/bugfix-requests/README.md:98 to `fixed`.",
        "Move the directory to `requests/bugfix-requests/_done/pipeline-status-rollover/` per that README's :91-92 archive convention, and repoint the Index link to `_done/pipeline-status-rollover/`. Use a plain filesystem move — do NOT run `git mv` or any other git command; `/commit` stages the rename. (`test_index_stage_cells_match_their_artifact_status_headers` FOLLOWS the Index link at tests/test_repo_structure.py:475, so the `_done/` artifacts are still checked and must all read `fixed`.)",
        "Run the full gate one final time. A green run here means: the fixed stage-4 instructions, followed literally on a real bugfix item, leave the repo green — which is the precise thing that was false when this bug was filed.",
        "Hand off to `/commit`. It will find no matching ROADMAP row (this is a process defect, not a numbered item — the H-series at ROADMAP.md:197-198 covers `escalation-queue` and `domain-engineer`, neither of which is this), so its 'maps to no roadmap row' path applies and no Status column changes. Do not invent a row. `/commit` also checks ESCALATIONS.md for open entries bearing on a closing row (commit/SKILL.md:141); there are none for this item — E-001 through E-009 bear on Phase 3, H2, 1.3, 1.8, 2.1 and post-v1."
      ],
      "acceptance": [
        "`uv run pytest -q` is fully green after the archive move — including `test_index_stage_cells_match_their_artifact_status_headers`, which now reads through the `_done/` link and finds four artifacts all declaring `fixed`.",
        "`requests/bugfix-requests/README.md`'s Index row reads `| [pipeline-status-rollover](_done/pipeline-status-rollover/) | fixed | … |`.",
        "No artifact directly in the item directory declares anything other than `fixed`; `reviews/` (if present) is untouched.",
        "`uv run pytest tests/test_request_links.py -q` is green — the archived directory is skipped by that module (:41), so relative links out of it are no longer checked, and nothing else broke.",
        "ruff check, ruff format --check, mypy all exit 0.",
        "The IMPLEMENTATION_REPORT's acceptance ledger cites the RED-to-GREEN transition with real output: `3 failed, 79 passed` at Phase 0 → `83 passed` at the end."
      ],
      "commit_note": "Close out pipeline-status-rollover by following its own fix. Report opens at `fixed` (the bugfix track's terminal word), all four artifacts and the Index roll together, item archived to _done/. Run /commit — it pushes the branch; the PR stays the user's."
    }
  ],
  "testing": "THE ACCEPTANCE CONTRACT IS THE BUGFIX TRACK'S, NOT A FEATURE'S. requests/bugfix-requests/README.md:37 states it: \"A red reproduction goes green, and a regression test is left behind.\" Both halves are already satisfiable here because the regression test IS the repro — the three assertions landed in commit fb0406e and stay in the tree permanently.\n\nTHE RED REPRO, MEASURED TODAY (not quoted from the RCA — re-run at planning time):\n  `uv run pytest -q` → `3 failed, 79 passed`. The three:\n    tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares — fails with `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}` against declared vocabulary `['diagnosed', 'fixed', 'implemented', 'intake', 'planned', 'retuned', 'scoped']`. Catches defects 2 and 4. Closed by Phase 2.\n    tests/test_repo_structure.py::test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory — fails with `['create-implementation-plan', 'implement-plan']`. Catches defect 1. Closed by Phase 1.\n    tests/test_repo_structure.py::test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token — fails with \"implement-plan's advance-status section hardcodes ['implemented'] and serves all three tracks\". Catches defect 3. Closed by Phase 3.\n  `uv run ruff check` → All checks passed. `uv run mypy` → Success: no issues found in 16 source files. Both are clean on the repro, so any lint or type failure later is caused by this work.\n\nPER-PHASE GATE — every phase ends the same way, and a phase is not done until all four are green: `uv run pytest` · `uv run ruff check` · `uv run ruff format --check` · `uv run mypy`. `ruff format --check` is in the list deliberately: .github/workflows/ci.yml:39-40 runs it as its own step, so a locally-green-but-unformatted tree still reds the PR. Then `/commit` — which stages by path, runs the doc-drift checks, and asks before writing. Never `git commit` ad hoc, never amend, never push to main.\n\nTHE EXPECTED COUNT LADDER, so a cold implementer can tell progress from accident:\n  Phase 0: 3 failed / 79 passed · Phase 1: 2 failed / 80 passed · Phase 2: 1 failed / 81 passed · Phase 3: 0 failed / 82 passed · Phase 5: 0 failed / 83 passed (the new Index-grammar guard) · Phase 6: 83 passed after the archive move.\nAny deviation from this ladder means an edit did something other than what this plan intended — stop and read the failure rather than piling on another edit.\n\nTWO VERIFICATIONS THAT MUST BE RUN, NOT ASSERTED:\n  1. Phase 5's new guard must be proven to bite. Temporarily set one Index Stage cell to a bogus word, confirm `test_index_stage_cells_use_only_their_own_track_s_grammar` goes RED naming that row, revert. A guard that has never been seen red is a guard nobody has tested — and a test that passes vacuously is exactly how invariant B went unguarded in the first place.\n  2. Phase 3 must confirm implement-plan is still VISIBLE to the conformance guard after the terminal edit. If the template blockquote were changed to a `<placeholder>`, `SKILL_STATUS_TEMPLATE` (tests/test_repo_structure.py:41) would match nothing for that skill and it would silently drop out of coverage while the suite stayed green. Verify by grep that the line still reads `> **Status:** implemented`.\n\nREGRESSION SAFETY. The 79 pre-existing tests are the blast-radius check and must never drop. Three in particular are load-bearing for this change and should be watched by name: `test_index_stage_cells_match_their_artifact_status_headers` (invariant A — Phase 6 exercises it through the `_done/` link), `test_process_artifacts_have_no_dead_relative_links` (Phase 4 adds comments containing paths; a mistyped one reds this), and `test_every_live_intake_artifact_declares_a_stage_plan` (Phase 6's archive move takes this item out of its scope, which is correct and expected).\n\nNOT TESTED, AND SAID PLAINLY. The prose restatements outside the guarded regions — create-implementation-plan:56 and :65-66, implement-plan:29, :61, :92-93 and :324 — are fixed in Phases 2 and 3 but no assertion covers them, because they are narrative sentences rather than status blockquotes. They are verified by grep and by reading, and they are the residue the RCA names at its lines 126-129 (\"the six restatements remain six\"). Do not fabricate a regex guard for them; a fragile prose test is worse than an honest gap.\n\nNOTHING USER-RUN, NOTHING THAT SPENDS MONEY. This change runs no panel scripts, pulls no source, and touches no cloud service. `/commit` pushes the branch; opening and merging the PR stays the user's, and CI re-runs the same four gates there under `enforce_admins: true`.",
  "risks": [
    "THE REGEX WINDOW MOVES. `_advance_status_section` (tests/test_repo_structure.py:74-80) takes the FIRST case-insensitive `advance status` match and slices to the first following `^##`. Introducing that phrase earlier in create-implementation-plan/SKILL.md or implement-plan/SKILL.md silently relocates the window all three seams depend on — the tests could go green on the wrong region, or red for a reason that looks unrelated to the edit. Mitigation: after every edit to those two files, grep for `advance status` and confirm exactly one hit each, still in Step 5 / Step 7.",
    "THE SLICE ENDS INSIDE THE FENCED TEMPLATE. `NEXT_SECTION` (:53) is fence-blind, so create-implementation-plan's window stops at `## 1. Onboarding` (:184) and implement-plan's at `## 1. Acceptance ledger` (:276). A rollover or terminal phrase added AFTER those headings — which looks like the natural place, since that is where the template body is — lands outside the window and the test stays red with no obvious reason. Mitigation: the prescribed bullets go in the bullet list, before the fence opens.",
    "A `<placeholder>` TEMPLATE SILENTLY DISABLES THE CONFORMANCE GUARD. `SKILL_STATUS_TEMPLATE`'s `[a-z-]+` (:41) cannot match a leading `<`, so rewriting `> **Status:** implemented` as `> **Status:** <terminal>` makes implement-plan invisible to `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` — green, and uncovered. This is the single most tempting wrong move in Phase 3, because it reads as the cleanest fix. Mitigation: keep a real declared word in the blockquote and put the per-track variation in an adjacent HTML comment, following create-implementation-plan:177-178.",
    "ROLLING `reviews/` BY MISTAKE. The invariant-A guard globs `item_dir.glob(\"*.md\")` at :479 — non-recursive. `_done/1.1-app-shell/reviews/preflight.md` carries `> **Status:** preflight`, a word no grammar declares, and is green only because of that non-recursion. A rollover instruction that says 'every artifact' without the carve-out invites the next agent to rewrite panel working files, which are provenance and should not be retroactively restaged. Mitigation: the `reviews/` exemption is written into both new bullets in Phase 1 and is an acceptance criterion.",
    "PHASE 2 BREAKS THE NEXT STAGE'S LOOKUP IF THE PROSE IS NOT FIXED WITH THE TEMPLATE. `implement-plan/SKILL.md:61` says to find the Index item at the `plan` stage; the moment stage 3 writes `planned`, that instruction fails to match and a cold agent either stalls or picks the wrong item. Same for `create-implementation-plan:56` pointing at `root-cause`. No test covers either line. Mitigation: both are explicit steps in Phase 2 with grep-based acceptance, and they must land in the SAME commit as the template change — a half-landed Phase 2 is worse than none.",
    "LINE NUMBERS IN THIS PLAN GO STALE THE MOMENT PHASE 1 LANDS. Every citation here was read against HEAD `fb0406e`; Phase 1 inserts bullets into both stage-advancing skills and shifts everything below. Mitigation: apply every edit by exact-text match, never by line number, and re-read the region before each edit rather than trusting a number from this document.",
    "PHASE 5 IS THE ONLY PHASE THAT TOUCHES PYTHON, AND IT REFACTORS A HELPER TWO TESTS SHARE. Splitting `_declared_stage_tokens()` (:63-71) into per-track and union forms puts `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares`'s call site at :280 in the blast radius, under mypy strict. Mitigation: keep the union function's name and signature stable, annotate both, and re-run the whole file rather than only the new test.",
    "THE HARDENING TIER CAN EAT THE FIX. The RCA gates it explicitly (its line 130: 'gated not assumed'), and a `next:`-field guard in particular is a tar pit — the field's live values include a free-form `<feature-slug>` (diagnose-bug:102), so any regex is vacuous or wrong. Mitigation: Phase 5 is the one droppable phase, the guard on `next:` is declined by decision rather than deferred by silence, and Phases 1-3 alone satisfy the Definition of Done.",
    "PHASE 6 ARCHIVES THE ITEM, WHICH CHANGES WHICH GUARDS SEE IT. Moving to `_done/` takes the request out of `test_every_live_intake_artifact_declares_a_stage_plan` (:255 filters `_done`) and out of the link checker (test_request_links.py:41) — but NOT out of `test_index_stage_cells_match_their_artifact_status_headers`, which follows the Index link at :475 into `_done/` and checks every artifact there. An implementer who assumes `_done/` means 'exempt from everything' will leave a sibling at `planned` and red the build at the very last step. Mitigation: Phase 6's acceptance names this guard specifically.",
    "BOTH UPSTREAM ARTIFACTS MIS-CITE tests/test_request_links.py:36 as the `_done/` skip. It is at :41; `:36` is the `def _scanned_files()` line. Harmless to the fix, but a cold agent following the citation reads a function signature and may conclude the artifact is wrong about more than it is. Mitigation: the correction is recorded in Phase 5's decline note rather than left for rediscovery."
  ],
  "files_to_touch": [
    {
      "path": ".claude/skills/create-implementation-plan/SKILL.md",
      "change": "Phase 1: add a sibling-rollover bullet inside Step 5's advance-status region (currently :167-183), before the Index bullet at :170-172, naming `planned` and exempting `reviews/`. Phase 2: `plan` → `planned` at the Index instruction (:172), the artifact stage line (:173) and the template blockquote (:176); `root-cause` → `diagnosed` in Step 1's Index lookup (:56) and its disposition-gate example (:65-66). Phase 4: append the enforcing test's name to the existing authority comment at :177-178. Do not add the string 'advance status' anywhere above :167."
    },
    {
      "path": ".claude/skills/implement-plan/SKILL.md",
      "change": "Phase 1: add a sibling-rollover bullet inside Step 7's advance-status region (currently :254-275), before the Index bullet at :257-259, exempting `reviews/`. Phase 2: `plan` → `planned` in the Step 1 Index lookup (:61) and the disposition gate (:92-93). Phase 3: rewrite :257-259 and :260 to name the resolved track's terminal word with all three spelled out; keep the template blockquote at :268 reading `implemented` and add an HTML comment beneath it naming feature/bugfix/calibration terminals; fix the track-blind sentences at :29 and :324. Do not add 'advance status' anywhere above :254."
    },
    {
      "path": ".claude/skills/diagnose-bug/SKILL.md",
      "change": "Phase 2: `root-cause` → `diagnosed` at the verdict-routing line (:97), the template blockquote (:107), and the Step 5 Index/blockquote instruction (:154) — preserving the '(or the terminal stage word)' clause at :154 verbatim, since it is the DERIVES_TERMINAL precedent Phase 3 copies. Phase 4: add the authority comment beside :107. The Step 5 rollover line at :152 is already correct and must not be disturbed."
    },
    {
      "path": ".claude/skills/scope-feature/SKILL.md",
      "change": "Phase 4 only: add the authority comment beside the template blockquote at :149. Lines 136-146 are the correct pattern the fix copies and must not change — every other edit in this plan is measured against them."
    },
    {
      "path": ".claude/skills/make-bugfix-request/SKILL.md",
      "change": "Phase 5: `next: root-cause` → `next: diagnose` at :130, matching the stage name in that track's pipeline table (requests/bugfix-requests/README.md:20). Phase 4: add the authority comment beside the same template blockquote. The `## Stage plan` section this file supplies is asserted by test_both_intake_templates_carry_a_stage_plan_section (:209-232) — do not disturb that heading."
    },
    {
      "path": ".claude/skills/make-feature-request/SKILL.md",
      "change": "Phase 4 only: add the authority comment beside the template blockquote at :176. Its `intake` token is already grammar-correct. Same `## Stage plan` heading caution as above."
    },
    {
      "path": ".claude/skills/update-docs/SKILL.md",
      "change": "Phase 4: extend the 'requests/ — do the Index rows match the artifacts?' section at :131-135 to name BOTH invariants — the Index mirrors the artifact blockquote (already there), AND both must be words the resolved track's Status grammar declares (missing today, which is the exact asymmetry the RCA identifies)."
    },
    {
      "path": "tests/test_repo_structure.py",
      "change": "Phase 5 only: split `_declared_stage_tokens()` (:63-71) into a per-track helper plus a union wrapper, keeping the :280 call site working under mypy strict; add `test_index_stage_cells_use_only_their_own_track_s_grammar` reusing the `stage_cell` regex shape from :465. The three repro tests at :270, :299 and :330 are the acceptance contract and must NOT be edited, relaxed, or reworded to make a fix pass."
    },
    {
      "path": "requests/bugfix-requests/README.md",
      "change": "Phase 5: add one clause to the grammar block at :86 declaring what the `next:` field contains. Phase 6: set the Index Stage cell at :98 to `fixed` and repoint its link to `_done/pipeline-status-rollover/`."
    },
    {
      "path": "requests/feature-requests/README.md",
      "change": "Phase 5 only: add the same `next:`-field clause beside the grammar at :106 (the four-field blockquote shape is already documented at :104). No Index change — no feature item is in flight."
    },
    {
      "path": "requests/calibration-findings/README.md",
      "change": "Phase 5 only: add the same `next:`-field clause beside the grammar at :88. Its Index placeholder row at :94 matches no stage-cell regex and needs no change — the track is unexercised, which is exactly why guarding beats observing (RCA lines 109-112)."
    },
    {
      "path": "requests/bugfix-requests/pipeline-status-rollover/BUGFIX_REQUEST.md",
      "change": "Phase 6: Status blockquote → `fixed`, then move with the directory into `_done/`. This is the sibling defect 1 exists to protect; rolling it by hand here is the dogfood."
    },
    {
      "path": "requests/bugfix-requests/pipeline-status-rollover/ROOT_CAUSE_ANALYSIS.md",
      "change": "Phase 6: Status blockquote → `fixed`, then move with the directory into `_done/`. Content is DECIDED and must not be edited otherwise — its diagnosis is the contract, not a draft."
    },
    {
      "path": "requests/bugfix-requests/pipeline-status-rollover/IMPLEMENTATION_PLAN.md",
      "change": "Written by this stage opening at `planned` (not `plan` — the corrected token, applied to its own artifact). Phase 6: → `fixed`, then archived with the directory."
    },
    {
      "path": "requests/bugfix-requests/pipeline-status-rollover/IMPLEMENTATION_REPORT.md",
      "change": "New in Phase 6. Opens at `fixed` — the bugfix track's terminal word, per the newly-fixed implement-plan Step 7, NOT `implemented`. Its acceptance ledger carries the measured 3-failed → 83-passed transition."
    }
  ],
  "code_references": [
    {
      "ref": "tests/test_repo_structure.py:270-296 test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares",
      "claim": "Red repro for defects 2 and 4. Scans every `.claude/skills/*/SKILL.md` for `> **Status:** <word>` lines and asserts each word is in the union of the three READMEs' grammars. Measured red output: `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}`. Closed by Phase 2."
    },
    {
      "ref": "tests/test_repo_structure.py:299-327 test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory",
      "claim": "Red repro for defect 1, the blocking one. Measured red output: `['create-implementation-plan', 'implement-plan']`. Closed by Phase 1."
    },
    {
      "ref": "tests/test_repo_structure.py:330-353 test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token",
      "claim": "Red repro for defect 3. Measured red output: \"implement-plan's advance-status section hardcodes ['implemented'] and serves all three tracks\". Passes when DERIVES_TERMINAL matches OR more than one terminal token appears in the section. Closed by Phase 3."
    },
    {
      "ref": "tests/test_repo_structure.py:74-80 _advance_status_section",
      "claim": "Defines WHERE a phrase must land to count: first `advance status` match to the first following `^##`. Fence-blind, so the window stops inside the template block. Measured windows — scope-feature 136-152, diagnose-bug 150-176, create-implementation-plan 167-183, implement-plan 254-275."
    },
    {
      "ref": "tests/test_repo_structure.py:41 SKILL_STATUS_TEMPLATE",
      "claim": "`^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)` — its `[a-z-]+` cannot match a leading `<`, so a `<placeholder>` template makes a skill invisible to the conformance guard. This is why Phase 3 keeps a real word in implement-plan's blockquote."
    },
    {
      "ref": "tests/test_repo_structure.py:55 ROLLS_A_SIBLING",
      "claim": "`Status blockquote|sibling|every artifact`, case-insensitive — the exact vocabulary Phase 1's new bullets must contain, and only within the advance-status window."
    },
    {
      "ref": "tests/test_repo_structure.py:59-60 TERMINAL_TOKENS and DERIVES_TERMINAL",
      "claim": "`{implemented, fixed, retuned}` and `terminal (?:stage word|token)|track's terminal`. Phase 3's wording satisfies both halves so a later reword cannot silently un-fix it."
    },
    {
      "ref": "tests/test_repo_structure.py:454-487 test_index_stage_cells_match_their_artifact_status_headers",
      "claim": "Invariant A — the guard that was already there. Its loop at :479 is `item_dir.glob(\"*.md\")`, non-recursive (hence `reviews/` is exempt), and it follows the Index link at :475, so `_done/` directories ARE checked. Phase 6 exercises both facts."
    },
    {
      "ref": ".claude/skills/scope-feature/SKILL.md:136-146",
      "claim": "The correct pattern. `:139` rolls the sibling, `:140-143` sets the Index cell, `:144` opens the new artifact at `scoped`/`next: plan`. Phase 1 copies its shape into the two skills that lack it."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:167-176",
      "claim": "Defects 1 and 2 together. 'Then advance status' at :167; the Index bullet at :170-172 writes `plan`; :173 opens the artifact at `plan`; :176 is the template blockquote — and no bullet mentions the two siblings sitting at `scoped`/`diagnosed`."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:56 and :65-66",
      "claim": "Collateral instances beyond the RCA's four: both tell the agent a ready bugfix RCA sits at `root-cause`, which Phase 2 makes false. Not covered by any test; fixed by hand in Phase 2."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:49-51",
      "claim": "Step 1 already resolves `<track>`, `<work-dir>` and the track README from the upstream artifact's path — the machinery the derived terminal word reuses, so Phase 3 adds no new resolution logic."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:251-268",
      "claim": "Defects 1 and 3. Step 7 opens at :251, 'Then advance status' at :254, the Index bullet at :257-259 writes `implemented` unconditionally, :260 repeats it, :268 is the template blockquote — and no bullet mentions the siblings."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:53-55",
      "claim": "The path-based track resolution that answers RCA Open Question 2: '`<track>` = `bugfix` when the upstream path is under `bugfix-requests/`, else `feature`'. The terminal word follows from this."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:29, :61, :92-93, :324",
      "claim": "Four more track-blind or stale restatements the RCA did not enumerate. :61 and :92-93 tell the agent to look for stage `plan`, which Phase 2 renames to `planned` — a functional break if left. :29 and :324 assert the terminal is `implemented` for every track."
    },
    {
      "ref": ".claude/skills/diagnose-bug/SKILL.md:107",
      "claim": "Defect 4 — the template writes `root-cause` where the bugfix grammar (requests/bugfix-requests/README.md:86) says `diagnosed`. Found by the diagnosis, in the very skill running it."
    },
    {
      "ref": ".claude/skills/diagnose-bug/SKILL.md:150-154",
      "claim": "Simultaneously the second CORRECT rollover ('Update the `BUGFIX_REQUEST.md` Status blockquote', :152 — matches ROLLS_A_SIBLING) and the tolerated track-derived-terminal shape ('or the terminal stage word', :154 — matches DERIVES_TERMINAL). Phase 3 copies the latter; Phase 2 changes only the `root-cause` literal beside it."
    },
    {
      "ref": ".claude/skills/make-bugfix-request/SKILL.md:130",
      "claim": "Hardening (a): `> **Status:** intake · … · next: root-cause` — the stage word is fine, the `next:` value names no declared stage. Phase 5 changes it to `diagnose`."
    },
    {
      "ref": "requests/feature-requests/README.md:106",
      "claim": "Declares `intake → scoped → planned → implemented`, parsed by STATUS_GRAMMAR at tests/test_repo_structure.py:38. With :104 it is the four-field blockquote contract the skills restate."
    },
    {
      "ref": "requests/bugfix-requests/README.md:86",
      "claim": "Declares `intake → diagnosed → planned → fixed` — the grammar this item's own artifacts must obey, and the reason its RCA opened at `diagnosed` rather than the template's `root-cause`."
    },
    {
      "ref": "requests/calibration-findings/README.md:88",
      "claim": "Declares `intake → diagnosed → planned → retuned`. Its Index at :92-94 is an empty placeholder row that matches no stage-cell regex, so guarding this track costs nothing and needs no live item — the RCA's answer to Open Question 3."
    },
    {
      "ref": "requests/bugfix-requests/README.md:37-46",
      "claim": "The Definition of Done this plan is measured against: a red reproduction goes green and a regression test is left behind. The repro IS the regression test, already committed."
    },
    {
      "ref": "requests/bugfix-requests/README.md:91-92",
      "claim": "The archive convention Phase 6 executes: one move into `_done/` at the terminal stage, Index row stays with its link updated."
    },
    {
      "ref": "tests/test_request_links.py:41",
      "claim": "The real location of the `_done/` skip (`if \"_done\" not in p.parts`) — both upstream artifacts cite `:36`, which is the `def _scanned_files()` line. Hardening (c) is declined against this, since the skip is documented as deliberate at :19-20."
    },
    {
      "ref": ".claude/skills/update-docs/SKILL.md:131-135",
      "claim": "States invariant A only — 'the artifact's Status blockquote is the source of truth; the track README's Index Stage cell mirrors it' — and never that either word must be one the grammar declares. Phase 4 adds invariant B here."
    },
    {
      "ref": ".claude/skills/commit/SKILL.md:110-149",
      "claim": "Step 4 maintains ROADMAP.md's per-item Status against the diff, and :141 surfaces open ESCALATIONS.md entries bearing on a closing row. Phase 6 relies on its 'maps to no roadmap row' path — this is a process defect, not a numbered item."
    },
    {
      "ref": "ROADMAP.md:197",
      "claim": "`| H1 | escalation-queue | … | 1.3 | DONE |` — the harness row whose absence this bug is a worked example of, and which has now landed. It is why hardening (c) is declined rather than rebuilt."
    },
    {
      "ref": ".github/workflows/ci.yml:36-47",
      "claim": "The `Lint, types, tests` job runs `uv run ruff check`, `uv run ruff format --check`, `uv run mypy`, then `uv run pytest -m \"not network\"`. That is why the per-phase local gate includes `ruff format --check`, which the plan template's §3 boilerplate omits."
    },
    {
      "ref": "requests/README.md:76-87",
      "claim": "The three hard triggers. Trigger 1 fired on this bug (intake's Open Questions came out non-empty and question 1 was load-bearing), which is why the full track ran and this plan exists rather than a direct build."
    }
  ],
  "open_questions": [
    "Phase 4 decides NOT to create a shared prose home for the stage vocabulary, keeping six restatements each pointed at its track README. That is this plan's answer to the remainder of RCA Open Question 1, and it is a judgment call rather than a forced one — the counter-argument is that a seventh restatement will be added the next time a pipeline skill is written, and only the guard will catch it. If the user prefers a shared home, the cheapest shape is a single `> **Status:**` example block in requests/README.md that every SKILL.md links to while keeping its own copyable template; that is additive to this plan, not a replacement for any phase.",
    "Phase 5's `next:`-field work declares the vocabulary in prose but adds no guard, because the field's live values include a free-form `<feature-slug>` (diagnose-bug/SKILL.md:102) alongside stage names. If the user wants that field mechanically enforced, the field's shape has to change first — e.g. splitting `next:` into a stage token plus an optional target — and that is a separate request, not a hardening step.",
    "Should `_done/1.1-app-shell/reviews/preflight.md`'s `> **Status:** preflight` be brought into a declared vocabulary? It is green today only because the invariant-A guard globs non-recursively (tests/test_repo_structure.py:479) and the conformance guard scans only `.claude/skills/*/SKILL.md`. `preflight` names a panel working file, not a pipeline stage, so leaving it undeclared is defensible — but nothing currently says so in writing, which is the same shape of gap this whole bug is about.",
    "Phase 6 archives this item into `_done/`, which removes it from the link checker's scope (tests/test_request_links.py:41). Its BUGFIX_REQUEST.md and ROOT_CAUSE_ANALYSIS.md carry relative links four levels up into `.claude/skills/` that resolve today; after the move they will never be checked again. That is the documented convention, but it is worth confirming the links still resolve BEFORE the move rather than discovering later that the archived trail points nowhere.",
    "The bugfix track has never completed a full run before, so Phase 6 is the first exercise of its `_done/` archive path. If anything about the move surprises the implementer — the Index link shape, a guard reading through it — that is new information about the track contract itself and belongs in the implementation report, not silently worked around."
  ]
}
```

---

## Planner: 1

```json
{
  "planner": "sequencing",
  "ok": true,
  "onboarding_files": [
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\ROOT_CAUSE_ANALYSIS.md",
      "why": "The decided upstream artifact. Read in full first — it is CONSUMED, not re-opened. Its Verdict (confirmed-bug, four instances), the red repro table at :28-32, the four-instance evidence at :62-85, the answers to the four Open Questions at :95-116, and the tiered fix posture at :118-135 are the whole mandate. The one thing it explicitly leaves to this plan is at :126-129: shared prose home vs. guard-and-keep-the-restatements."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\tests\\test_repo_structure.py",
      "why": "The red reproduction lives here, already committed. Lines 32-60 are the module-level machinery (STATUS_GRAMMAR, SKILL_STATUS_TEMPLATE, STAGE_ADVANCING_SKILLS, ROLLS_A_SIBLING, TERMINAL_TOKENS, DERIVES_TERMINAL) and lines 270-353 are the three failing tests. Read the regexes literally — every prose edit in this fix is graded by them, and `_advance_status_section` at :74-80 defines the exact window an edit must land inside."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\README.md",
      "why": "The track contract. `:86` declares the bugfix grammar `intake → diagnosed → planned → fixed` — this is the authority the fix makes enforceable, and the terminal word this item's own report must open at. `:35-46` is the definition of done (red goes green + a regression test is left behind, and the repro must have failed first). `:48-57` says a CI/workflow-config defect's test belongs in tests/test_repo_structure.py, which is where it already is. `:98` is this item's Index row."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\create-implementation-plan\\SKILL.md",
      "why": "Defect 2 and half of defect 1 live here. Read `:50-61` (track resolution AND the stage-discovery reader at `:56`), and `:158-183` (Step 5, the advance-status region). Note `:167` is where `_advance_status_section` starts matching and `:184` (`## 1. Onboarding`, inside a code fence) is where it stops — the regex at tests/test_repo_structure.py:53 is fence-blind."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\implement-plan\\SKILL.md",
      "why": "Defect 3 and the other half of defect 1. Read `:51-65` (the two-track resolution that calibration falls through), `:86-95` (the disposition gate whose worked example quotes the bogus `plan` token), and `:251-275` (Step 7, the advance-status region bounded by `## 1. Acceptance ledger` at `:276`). Also `:29` and `:324`, two track-blind `implemented` restatements outside the guarded window."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\scope-feature\\SKILL.md",
      "why": "The reference implementation. `:136-146` is the pattern the fix copies: `:139` rolls the sibling ('Set the request's Status blockquote to `scoped`'), `:140-143` sets the Index cell, `:144` opens the new artifact. Do not invent a new shape — match this one, including its 'these are in-place edits, git is read-only here' framing at `:136-137`."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\diagnose-bug\\SKILL.md",
      "why": "Defect 4. `:107` is the template blockquote writing `root-cause`; `:97` and `:154` are its prose siblings; `:7` carries it in the skill's dispatch description. `:152` is the line that already gets sibling rollover right, and `:154`'s parenthetical 'or the terminal stage word' is the in-repo precedent the RCA names at `:107-108` for track-derived prose — preserve both."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\feature-requests\\README.md",
      "why": "`:104` declares the four-field Status blockquote shape and, critically, declares `next:` as `<stage or \"implement\">` — i.e. deliberately NOT a stage-grammar field. `:106` declares the feature grammar. Both are load-bearing for scoping the hardening decisions in Phase 4."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\tests\\test_request_links.py",
      "why": "The other guard the skill edits are exposed to: `_scanned_files` at `:35-56` sweeps `.claude/skills/**/*.md`. Read `_dead_links` at `:59-83` before writing any path into a skill — it only inspects markdown-link syntax `[text](target)`, so a backticked bare path is not checked and is the safer form. `:86-97` (`test_the_root_documents_are_actually_scanned`) is the guard-on-a-guard idiom Phase 4 copies."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\ESCALATIONS.md",
      "why": "Where any declined Phase 4 hardening item gets parked instead of forgotten. `:72-99` is the six-field entry format (every field guarded by tests/test_escalations.py), `:75` is the strict `Bears on:` rule, and `:101-103` warns that E-000 is a template, never a real entry. Highest existing id is E-009 at `:225`."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\CLAUDE.md",
      "why": "Project conventions the implementer must honor even on a docs-only fix: work on a branch and land through a PR, agents commit only through `/commit` (never `git commit` ad hoc), subagents get read-only git, amend/force-push/push-to-main stay the user's, and label epistemics. Also the source of the 'the panel is the default' framing (ADR 0010) that the skills being edited implement."
    }
  ],
  "architecture_notes": "SHAPE OF THE CHANGE. This is a documentation-and-guard fix with a zero-byte footprint under src/, app/, careers/, datasets/, or rulesets/. Everything it touches is prose inside four `.claude/skills/*/SKILL.md` files, plus (in the optional Phase 4) new assertions in tests/test_repo_structure.py. There is no Python behavior change, no HTTP surface, no event schema, no ruleset, and no dataset — so no data-contracts work and no source-verification phase is required (see UNCONFIRMED CLAIMS below for why that is a positive finding rather than an omission).\n\nSTARTING STATE, MEASURED TODAY (2026-08-21). Branch is `bugfix/pipeline-status-rollover` (the task's gitStatus snapshot showing `phase1/escalation-queue` is stale — H1 merged as PR #22 = commit 2f91ab5). Working tree is clean. Commit fb0406e (\"Diagnose the pipeline status drift and land its red repro\") landed the RCA and the three failing tests on this branch and is NOT on origin/main; `git show origin/main:tests/test_repo_structure.py` contains none of the three test functions, and origin/main carries only BUGFIX_REQUEST.md from this item's directory. So the branch is DELIBERATELY RED and its PR cannot merge under `enforce_admins: true` until this fix lands. `uv run pytest --tb=no -q` gives 3 failed, 79 passed (82 collected). `uv run ruff check` → all checks passed. `uv run mypy` → success, 16 source files.\n\nTHE TWO INVARIANTS (from ROOT_CAUSE_ANALYSIS.md:45-59). Invariant A — the Index cell agrees with every `*.md` in the item directory — is guarded by tests/test_repo_structure.py:454. Invariant B — the stage word is one the track's declared grammar contains — was guarded by nothing. A compares a directory against itself, so a skill writing an invented token *consistently* stays green forever. That asymmetry is why three of four defects were silent. The fix keeps A untouched (RCA Open Question 4 settles that it is exactly right) and closes B.\n\nTHE WRITER/READER COUPLING — the single most important sequencing fact, and one the RCA does not enumerate. Every stage word appears twice in the pipeline: once where a skill WRITES it, and once where a downstream skill READS it back to discover work. The writers are the six restatements the RCA counted. The readers are separate, unguarded, and they break if a writer is fixed alone:\n  - create-implementation-plan/SKILL.md:56 hunts for \"a confirmed-bug RCA at `root-cause`\" — the token defect 4 removes.\n  - implement-plan/SKILL.md:61 hunts for \"an item at the `plan` stage\" — the token defect 2 removes.\n  - implement-plan/SKILL.md:91-93 quotes `plan · … · decided · next: implement` as the worked example of a ready plan and says \"the word `plan` appearing is *expected*\" — that sentence becomes false the moment defect 2 is fixed.\nNo test covers any of them (guard B only inspects `> **Status:**` template lines via SKILL_STATUS_TEMPLATE at tests/test_repo_structure.py:41). Consequence for phasing: a writer and its readers must move in the SAME phase, or the next real pipeline run silently fails to find its own work item. Phase 1 is grouped on exactly this boundary.\n\nTHE THIRD TRACK IS MISSING FROM THE MACHINERY. RCA Open Question 2 says the terminal word can follow from the track resolution implement-plan already does. That resolution, read at implement-plan/SKILL.md:53-55, is binary: \"`bugfix` when the path is under `bugfix-requests/`, else `feature` (the default)\". Calibration resolves to `feature` and would be written `implemented` instead of `retuned`. Worse, the work-dir formula on the same line — `requests/<track>-requests/<slug>/` — does not compose for calibration at all, because the directory is `calibration-findings`, not `calibration-requests`. Deriving the terminal from a two-valued resolution therefore cannot fix defect 3 for the third track; the resolution has to become three-valued and state its three paths literally. This is why Phase 3 is not a one-word edit.\n\nHOW THE GUARDS GRADE PROSE — read before writing a single word.\n  - `_advance_status_section` (tests/test_repo_structure.py:74-80) slices from the literal \"advance status\" to the next line matching `^##\\s`. That regex is FENCE-BLIND, so the window ends at the first `##` inside the template code fence: create-implementation-plan :167→:184, implement-plan :254→:276. Prose added after the fence is invisible to both the rollover and terminal guards.\n  - `ROLLS_A_SIBLING` (:55) matches `Status blockquote|sibling|every artifact`, case-insensitive.\n  - `DERIVES_TERMINAL` (:60) matches `terminal (?:stage word|token)|track's terminal`, case-insensitive; the alternative pass condition is ≥2 of {implemented, fixed, retuned} appearing in the window.\n  - `SKILL_STATUS_TEMPLATE` (:41) is `^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)`. A placeholder like `> **Status:** <the terminal word> · …` does not match `[a-z-]+`, so it produces NO offender — the guard goes VACUOUS rather than green. This is the sharpest trap in the whole fix and Phase 3 step 4 exists to dispose of it deliberately.\n\nTHE DESIGN CALL THE RCA HANDED TO THE PLAN (RCA:126-129), RESOLVED. Weighed: a shared prose home (e.g. `.claude/skills/_shared/status-grammar.md`) versus guard-it-and-keep-the-restatements. Recommendation: NO new shared file. Three reasons, all grounded. (1) There is no single grammar to home — requests/feature-requests/README.md:106, requests/bugfix-requests/README.md:86 and requests/calibration-findings/README.md:88 declare three different ones, and every back-half skill resolves a track before it writes a word, so a shared home would have to be track-keyed and would therefore duplicate rather than replace the READMEs — a seventh restatement. (2) Skills are loaded one SKILL.md at a time with no include mechanism; a shared file is a document an agent must *choose* to open, which is the same failure mode as prose plus one more hop. (3) The mechanism that actually stops recurrence is the committed guard (RCA:99-104), and it is already written. What the fix adds beyond correctness is that each restatement now carries a backticked pointer to its authority instead of merely agreeing with it by luck. Duplication drops from six free-floating literals to six literals each naming their source, under a test.\n\nPER-PHASE GREEN, STATED HONESTLY. Three tests are red at the start and they partition cleanly across three fix phases, so an intermediate phase cannot show a fully green `uv run pytest`. The phase gate used throughout this plan is therefore: **the phase's named pytest selector passes, the failing set is EXACTLY the documented remainder with zero new failures, and `uv run ruff check` / `uv run ruff format --check` / `uv run mypy` are clean.** The full suite reaches 82 passed at the end of Phase 3. Because `/commit` pushes the branch, CI will run and be RED on this branch until Phase 3 completes; that is expected and is not a retry-loop trigger. Do not open the PR before Phase 3 is green. If the user would rather never push a red branch, Phases 1-3 can be squashed into a single `/commit` — that is Open Question 4 and costs the per-defect reviewability, not correctness.",
  "phases": [
    {
      "name": "Phase 1 — Pin the baseline, then retire the two invented tokens (defects 2 and 4) at every writer AND reader",
      "goal": "`plan` and `root-cause` — the two stage words no track grammar declares — are gone from every skill, both where a skill instructs you to write one and where a skill looks one up to find work. `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` goes green. Chosen first because it is the cheapest instance and it proves the authority pattern (grammar-declared token + a backticked pointer to the README that declares it) that Phases 2 and 3 then apply to harder cases.",
      "steps": [
        "Confirm the branch and the baseline before editing anything. `git rev-parse --abbrev-ref HEAD` must print `bugfix/pipeline-status-rollover`; `git status` must be clean. Then `uv run pytest --tb=no -q` must print exactly `3 failed, 79 passed` and the three failures must be exactly test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares, test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory, and test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token (tests/test_repo_structure.py:270, :299, :330).",
        "STOP CONDITION: if a FOURTH test fails — especially test_index_stage_cells_match_their_artifact_status_headers (tests/test_repo_structure.py:454) — the stage-3 run that produced this plan followed the still-broken skill and left this item's directory internally inconsistent. Repair it first: set the Status blockquote of requests/bugfix-requests/pipeline-status-rollover/BUGFIX_REQUEST.md:1, ROOT_CAUSE_ANALYSIS.md:1 and IMPLEMENTATION_PLAN.md:1 all to `planned`, and the Index Stage cell at requests/bugfix-requests/README.md:98 to `planned`. Record the repair in the eventual report — it is live evidence for defect 1.",
        "create-implementation-plan/SKILL.md — writer edits. Change `plan` to `planned` in three places, matching existing text exactly: `:172` (\"set this item's **Index** row Stage cell to `plan`\"), `:173` (\"opens at stage `plan`, `next: implement`\"), and the template blockquote `:176` (`> **Status:** plan · created <YYYY-MM-DD> · decided · next: implement`). Leave `next: implement` alone in all three — see Phase 4 step 3 for why the `next:` field is deliberately out of scope.",
        "create-implementation-plan/SKILL.md:177-178 — the HTML comment directly under the template cites \"this README status grammar\" as its authority in the same breath as violating it (RCA:72-74). Now that the token is correct, make the pointer concrete: name the two READMEs by backticked path (`requests/feature-requests/README.md` and `requests/bugfix-requests/README.md`) rather than saying \"this README\". Use backticks, not markdown links — tests/test_request_links.py:63-83 only resolves `[text](target)` syntax, so a backticked path carries no dead-link risk.",
        "create-implementation-plan/SKILL.md:56 — READER edit, not in the RCA's four-instance list and load-bearing. The Index-discovery sentence reads \"or `requests/bugfix-requests/README.md` for a confirmed-bug RCA at `root-cause`\". Change `root-cause` to `diagnosed`. Left alone, stage 3 hunts the bugfix Index for a token that no longer exists anywhere in the repo and silently finds nothing.",
        "diagnose-bug/SKILL.md — writer edits. Change `root-cause` to `diagnosed` at `:97` (the confirmed-bug verdict line, \"→ `root-cause · … · decided · next: plan`\"), `:107` (the template blockquote — this is the line guard B actually grades), and `:154` (\"header) to `root-cause` (or the terminal stage word)\"). PRESERVE two things verbatim while doing it: `:152`'s phrase \"Status blockquote\" (tests/test_repo_structure.py:55 keys on it, and diagnose-bug currently PASSES the rollover guard because of it) and `:154`'s parenthetical \"(or the terminal stage word)\" (RCA:107-108 names it as the in-repo precedent Phase 3 copies).",
        "diagnose-bug/SKILL.md:7 — the pipeline chain inside the skill's dispatch description reads \"intake -> root-cause -> reuse plan/implement\". Change the chain token to `diagnosed`. Keep the natural-language trigger phrases (\"find the root cause\", \"why is X producing the wrong output\") untouched — those drive skill selection and are not stage words. This is Open Question 3; if the user declines, skip this step and note it.",
        "implement-plan/SKILL.md — READER edits, the downstream consumers of defect 2. `:61`: \"for an item at the `plan` stage\" → `planned`. `:93`: the disposition-gate worked example reads \"a ready plan reads `plan · … · decided · next: implement`, so the word `plan` appearing is *expected*\" — rewrite as `planned · … · decided · next: implement` and adjust the trailing clause so it still reads true. Leaving `:93` produces a skill whose worked example contradicts the artifact it is describing.",
        "Sweep for stragglers: `Select-String -Path \".claude\\skills\\*\\SKILL.md\" -Pattern '`root-cause`|`plan`'` must return zero hits. (This exact grep found the readers at create-implementation-plan:56 and implement-plan:61,:93 during planning — run it, do not assume.)"
      ],
      "acceptance": [
        "`uv run pytest tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares -q` → 1 passed. Before this phase it failed with `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}`; after, no skill instructs a token outside the declared vocabulary `['diagnosed', 'fixed', 'implemented', 'intake', 'planned', 'retuned', 'scoped']`.",
        "`uv run pytest --tb=no -q` → exactly `2 failed, 80 passed`, and the two remaining failures are exactly test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory and test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token. Any other failure is a regression introduced by this phase.",
        "`Select-String -Path \".claude\\skills\\*\\SKILL.md\" -Pattern '`root-cause`|`plan`'` returns no matches — proving the readers moved with the writers, which no test checks.",
        "`uv run pytest tests/test_request_links.py -q` → all passed. The edits land in `.claude/skills/`, a tree that guard scans (tests/test_request_links.py:35-36), so a malformed pointer would red it.",
        "`uv run ruff check` → \"All checks passed!\"; `uv run ruff format --check` → clean; `uv run mypy` → \"Success: no issues found in 16 source files\". All three are expected to be unchanged from baseline — this phase edits only markdown, so any movement here means a stray file was touched.",
        "`git diff --stat` shows exactly three files changed, all under `.claude/skills/`, and none under `src/`, `app/`, `tests/`, `careers/`, or `requests/` (unless the Phase 1 STOP CONDITION fired, in which case the item directory and requests/bugfix-requests/README.md are also expected)."
      ],
      "commit_note": "Hand to `/commit`. Suggested message subject: \"Retire the two invented pipeline stage tokens\". Never run `git commit` ad hoc (CLAUDE.md). `/commit` stages deliberately, runs the doc checks, and asks before writing; on yes it commits AND pushes the branch. Expect CI on the pushed branch to be RED — two repro tests remain by design until Phase 3. Do not open the PR. This is a bugfix-track item and maps to no ROADMAP row, so `/commit`'s roadmap-status step should find nothing to move; requests/README.md:73-74 documents that path."
    },
    {
      "name": "Phase 2 — Make stage-advancing skills roll the artifacts already in the directory (defect 1, the blocking one)",
      "goal": "Following `/create-implementation-plan` Step 5 or `/implement-plan` Step 7 literally leaves the item directory internally consistent, so invariant A (tests/test_repo_structure.py:454) cannot go red as a consequence of obeying a skill. `test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory` goes green. This is the defect that actually breaks builds today (RCA:64-68), and it is second only because Phase 1 established the authority pattern its wording reuses.",
      "steps": [
        "Re-read the reference implementation at scope-feature/SKILL.md:136-146 before writing anything. It does three things in order: `:139` rolls the sibling, `:140-143` sets the Index cell, `:144` opens the new artifact. Copy that ORDER, not just the sentence — rolling the sibling first is what makes the Index edit the last thing that can disagree.",
        "create-implementation-plan/SKILL.md — insert a new first bullet in the advance-status list, immediately before the existing Index bullet at `:170`, so it lands inside the window `_advance_status_section` slices (starts at the literal \"advance status\" on `:167`, ends at `## 1. Onboarding` on `:184` — the regex at tests/test_repo_structure.py:53 is fence-blind, so anything after `:184` is invisible to the guard). Wording must contain BOTH the phrases \"Status blockquote\" and \"sibling\" so that a later reword of either one alone cannot silently re-red the guard (tests/test_repo_structure.py:55 matches `Status blockquote|sibling|every artifact`).",
        "Make that bullet say what to do and why, concretely: set every SIBLING artifact's Status blockquote in `<work-dir>` to `planned` — the `FEATURE_REQUEST.md` / `BUGFIX_REQUEST.md` and the `PROJECT_SCOPE.md` / `ROOT_CAUSE_ANALYSIS.md` already sitting there — because `tests/test_repo_structure.py::test_index_stage_cells_match_their_artifact_status_headers` compares the Index cell against EVERY `*.md` in the item directory. Write the test path in backticks, not as a markdown link (tests/test_request_links.py:63-83 resolves only `[text](target)`).",
        "implement-plan/SKILL.md — the identical insertion, as a new first bullet immediately before the Index bullet at `:257`, inside the window `:254`→`:276` (`## 1. Acceptance ledger`). Leave the terminal word itself as a placeholder phrase for now (\"the track's terminal stage word\") and let Phase 3 define it — do NOT hardcode `implemented` here, or Phase 3 has to unpick this edit.",
        "Do not touch diagnose-bug/SKILL.md:152 or scope-feature/SKILL.md:139. Both already satisfy the guard (RCA:68 confirms diagnose-bug gets this right), and STAGE_ADVANCING_SKILLS at tests/test_repo_structure.py:46-51 deliberately excludes the intake skills, which create the item and so have no sibling to roll.",
        "Verify placement mechanically rather than by eye. In a scratch Python REPL, import the helpers from tests/test_repo_structure.py and print `_advance_status_section(text)` for both edited files, confirming the new bullet appears in the returned slice. Placement outside the window is the single most likely way this phase looks done and is not."
      ],
      "acceptance": [
        "`uv run pytest tests/test_repo_structure.py::test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory -q` → 1 passed. Before this phase it failed with `['create-implementation-plan', 'implement-plan']`.",
        "`uv run pytest --tb=no -q` → exactly `1 failed, 81 passed`, the single remaining failure being test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token.",
        "`uv run pytest tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares -q` still passes — Phase 1 is not regressed by the new prose (a stray `> **Status:**` line in the new bullet would break it).",
        "`uv run pytest tests/test_repo_structure.py::test_index_stage_cells_match_their_artifact_status_headers -q` passes — the invariant this whole fix protects is still green and was never modified (RCA Open Question 4 settles that it stays unchanged).",
        "Placement proof: `_advance_status_section` on each edited file returns a slice containing the new bullet. Record the two slices in the eventual report as evidence, since the guard's window is not obvious from reading the file.",
        "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` all clean and unchanged; `uv run pytest tests/test_request_links.py -q` green.",
        "`git diff --stat` shows exactly two files changed, both `.claude/skills/*/SKILL.md`."
      ],
      "commit_note": "Hand to `/commit`. Suggested subject: \"Roll sibling artifact statuses in the back-half pipeline skills\". Branch CI stays RED (one repro test remains). Still no PR. If `/commit`'s doc-drift step flags CLAUDE.md, check whether its skills description needs no change — this fix alters skill prose, not the project map, so the expected answer is no drift."
    },
    {
      "name": "Phase 3 — Derive the terminal stage word from a three-valued track resolution (defect 3), and turn the repro fully green",
      "goal": "`/implement-plan` closes every track on that track's own terminal word — feature `implemented`, bugfix `fixed`, calibration `retuned` — instead of writing one unconditionally. `test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token` goes green and the full suite reaches 82 passed. Sequenced last of the three fixes because it is the only one whose fix SHAPE was genuinely open (RCA Open Question 2) and because it turns out to require repairing the track resolution itself, which the RCA did not anticipate.",
      "steps": [
        "Fix the track resolution first — everything downstream derives from it. implement-plan/SKILL.md:53-55 currently reads \"`<track>` = `bugfix` when the path is under `bugfix-requests/`, else `feature` (the default); `<work-dir>` = `requests/<track>-requests/<slug>/`\". That is two-valued, so a calibration finding resolves to `feature`. Make it three-valued: `bugfix` under `bugfix-requests/`, `calibration` under `calibration-findings/`, else `feature`. CRITICAL: the `requests/<track>-requests/<slug>/` template does NOT compose for calibration — the directory is `calibration-findings`, not `calibration-requests`. Replace the template with the three literal directory paths.",
        "Add the terminal table inside the advance-status window (`:254`→`:276`), immediately after the opening sentence at `:254-255`: a three-row table mapping feature → `implemented` (requests/feature-requests/README.md:106), bugfix → `fixed` (requests/bugfix-requests/README.md:86), calibration → `retuned` (requests/calibration-findings/README.md:88), each row naming its README in backticks as the authority. Introduce it with the phrase \"the track's terminal stage word\".",
        "That wording satisfies BOTH branches of the guard deliberately. tests/test_repo_structure.py:349 passes if `DERIVES_TERMINAL` (`terminal (?:stage word|token)|track's terminal`, :60) matches OR if ≥2 of {implemented, fixed, retuned} appear in the window. Naming all three tokens AND using the phrase means a later reword of either one alone cannot silently re-red it — the same belt-and-braces reasoning as Phase 2's wording.",
        "Replace the two hardcoded instructions inside the window: `:259` (\"set this item's **Index** row Stage cell to `implemented`\") and `:260` (\"The report opens at `implemented · created <today> · decided · next: commit`\") both become \"the track's terminal stage word (see the table above)\".",
        "DISPOSE THE TEMPLATE BLOCKQUOTE AT `:268` DELIBERATELY — this is Open Question 1 and the sharpest trap in the fix. `SKILL_STATUS_TEMPLATE` (tests/test_repo_structure.py:41) is `^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)`. Rewriting `:268` as `> **Status:** <the track's terminal stage word> · …` does not match `[a-z-]+`, so guard B stops seeing this line entirely — it goes VACUOUS, not green. RECOMMENDED disposition (a): keep a concrete, grammar-declared token in the blockquote and add a one-line note beside it (\"swap for your track's terminal — see the table above\"), which keeps guard B pointed at this line. Disposition (b) — the placeholder, accepting the coverage loss — is only acceptable if Phase 4 step 1 lands in the same run.",
        "Fix the two track-blind restatements OUTSIDE the guarded window, which no test will ever catch: `:29` (\"The feature ends at status `implemented`\") and `:324` (\"the report + `implemented` status\"). Reword both to speak of the item's track terminal. These are exactly the unguarded prose restatements this bug is about; leaving them is leaving the drift in place with nothing red.",
        "Re-run the Phase 1 sweep, widened: `Select-String -Path .claude\\skills\\implement-plan\\SKILL.md -Pattern 'implemented'` and read every hit. Hits at `:218`, `:280`, `:289` are ordinary English (\"symbols you implemented\", \"the phases implemented\", \"how each was fixed\") and must be left alone. Only unconditional INSTRUCTIONS to write the word are in scope."
      ],
      "acceptance": [
        "`uv run pytest tests/test_repo_structure.py::test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token -q` → 1 passed. Before this phase it failed with \"hardcodes ['implemented'] and serves all three tracks, whose terminals are ['fixed', 'implemented', 'retuned']\".",
        "`uv run pytest --tb=no -q` → **`82 passed`, 0 failed**. This is the red-to-green transition the bugfix track's definition of done requires (requests/bugfix-requests/README.md:35-46) — capture the exact output, it is the report's primary evidence.",
        "The whole repro moves together: all three of tests/test_repo_structure.py:270, :299, :330 pass, and the 79 tests that were green at baseline are still green. Compare against the baseline captured in Phase 1 step 1 — 79 + 3 = 82, no test added or removed in Phases 1-3.",
        "Three-track resolution proof by reading: implement-plan/SKILL.md:53-55 names `bugfix-requests/`, `calibration-findings/` and the feature default, and states three literal work-dir paths rather than a `<track>-requests` template. Confirm `requests/calibration-findings/` is the real directory name (it is — requests/README.md:10 links it).",
        "Guard-B coverage did not go vacuous: re-run the module-level regex against implement-plan/SKILL.md in a REPL — `SKILL_STATUS_TEMPLATE.findall(text)` must still return at least one token, and every token returned must be in `_declared_stage_tokens()`. If it returns an empty list, disposition (b) was taken and Phase 4 step 1 is now mandatory rather than optional.",
        "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` clean; `uv run pytest tests/test_request_links.py -q` green.",
        "`git diff --stat` shows exactly one file changed: `.claude/skills/implement-plan/SKILL.md`."
      ],
      "commit_note": "Hand to `/commit`. Suggested subject: \"Derive the terminal stage word from the resolved track\". Branch CI should now be GREEN for the first time since fb0406e — verify that before anything else. This is the natural point to open the PR (the user's job, not the agent's — CLAUDE.md), or to continue to Phase 4 first and open one PR for the whole fix. Recommend continuing: Phase 4 is small and the hardening decisions read better reviewed alongside the fix they harden."
    },
    {
      "name": "Phase 4 — Close the two ways the new guard can go quietly vacuous, and park what is declined (gated)",
      "goal": "The mechanism the RCA calls the root fix (RCA:126-128) cannot be silently disabled by a future edit, and each of the RCA's three named hardening candidates is either landed or explicitly declined in writing rather than forgotten. Every item here is independently droppable — the user disposes which land. Sequenced last because it is additive: the repro is already green and every step is reversible on its own.",
      "steps": [
        "ITEM 1 (recommended — and MANDATORY if Phase 3 took disposition (b)). Add `test_the_stage_token_guard_is_not_vacuous` to tests/test_repo_structure.py, beside test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares at `:270`. Assert that `SKILL_STATUS_TEMPLATE` still parses at least one declared token from each of the four skills that write a concrete one — `make-feature-request` (:176), `make-bugfix-request` (:130), `scope-feature` (:149), `create-implementation-plan` (:176). Reason, put in the docstring: guard B only reports a skill it can PARSE, so a future rewrite to a `<placeholder>` blockquote empties the guard with nothing red. This is the same guard-on-a-guard idiom as tests/test_request_links.py:86-97, which exists for exactly this reason — cite it.",
        "ITEM 2 (recommended — Phase 1 proved these exist). The stage-DISCOVERY literals are guarded by nothing: create-implementation-plan/SKILL.md:56, implement-plan/SKILL.md:61, scope-feature/SKILL.md:48, diagnose-bug/SKILL.md:46 each look an item up by a backticked stage word in a sentence of the shape \"for an item at the `X` stage\". Add a narrow guard anchored on that phrasing (e.g. `at (?:the )?`(?P<stage>[a-z-]+)` stage`) asserting every captured word is in `_declared_stage_tokens()`. Keep the regex narrow and state in the docstring that it is deliberately more brittle than guard B — if it starts producing false reds, delete it rather than loosening it into noise. If the user declines, record explicitly that these four sites stay unguarded.",
        "ITEM 3 (recommended: DECLINE, with the reason written down). RCA hardening (a) proposes guarding the `next:` field, citing make-bugfix-request/SKILL.md:130 writing `next: root-cause`. Decline it here: `next:` is not a stage field. requests/feature-requests/README.md:104 declares it as `next: <stage or \"implement\">`, and every skill today writes an ACTION there — `scope` (make-feature-request:176), `plan` (scope-feature:144), `implement` (create-implementation-plan:176), `commit` (implement-plan:268). Guarding it against the stage grammar would red five skills that are not wrong. Tightening `next:` means changing the three track READMEs first, which is a separate request, not this fix. Update make-bugfix-request:130's `next: root-cause` to `next: diagnose` or `next: diagnosed` for consistency with Phase 1 — a one-word prose fix, not a guard.",
        "ITEM 4 (cheap and safe — recommended). RCA hardening (b): the Index cell is only ever checked against artifacts, never against the grammar, so a hand-edited Index could carry an invented word as long as every artifact matched it. Add a sibling to test_index_stage_cells_match_their_artifact_status_headers (tests/test_repo_structure.py:454) asserting each Index Stage cell is in ITS OWN track's declared grammar — note `_declared_stage_tokens()` at `:63` unions all three, so this needs a per-track variant, not the existing helper. Vacuous today for calibration (its Index at requests/calibration-findings/README.md is empty) and it fires on one row for bugfix and several for feature.",
        "ITEM 5 (recommended: OUT OF SCOPE). RCA hardening (c) measures the cost of tests/test_request_links.py:36 skipping `_done/` — the skip is why the 1.1 panel's original catch of this defect (`_done/1.1-app-shell/reviews/plan-adversarial.md:217`) became unreachable. The skip is documented as deliberate at tests/test_request_links.py:45-53, and the archived-finding failure mode is what harness row H1 `escalation-queue` (ROADMAP.md:197, DONE) was built to prevent. Record the measured cost in the report; do not change the skip in a bugfix about stage tokens.",
        "For every item declined with a real alternative and a nameable moment, park an ESCALATIONS.md entry rather than losing it — that file exists for exactly this (ESCALATIONS.md:10-13). Follow the six-field format at `:72-99` exactly (tests/test_escalations.py guards every field); the next free id is E-010 (highest existing is E-009 at `:225`). `Bears on:` must resolve to a roadmap item, phase, or `post-v1` with nothing else on the line (`:75`) — H2 `domain-engineer` (ROADMAP.md:198, NOT STARTED, the next harness row) is the plausible moment for further pipeline-guard work. Do NOT renumber anything to E-000, which is a template (`:101-103`).",
        "PROVE EACH NEW GUARD RED-FIRST before keeping it. For every test added in this phase: temporarily break the thing it guards (e.g. change create-implementation-plan:176's token to `<placeholder>` for item 1), run the new selector, confirm it FAILS with a readable message, then revert the temporary edit and confirm it passes. The track README is explicit that a repro which never failed is not a repro (requests/bugfix-requests/README.md:43-46) — the same standard applies to a regression guard. Revert by editing the file back, never by `git checkout`/`restore`/`stash` (CLAUDE.md: those are destructive-git and stay the user's)."
      ],
      "acceptance": [
        "`uv run pytest --tb=no -q` → all passed, with a collected count of 82 + (number of guards landed). State the new total explicitly in the report.",
        "Red-first evidence for every added guard: for each, the captured failing output from the temporary break plus the passing output after revert. A guard shipped without that pair is not accepted.",
        "`uv run pytest tests/test_escalations.py -q` → passes, including any newly parked E-010+ entry. That guard checks all six fields and the `Bears on:` resolution, so a malformed entry reds here rather than rotting.",
        "Every declined item is recorded — in the report, and in ESCALATIONS.md where it has a real alternative and a nameable moment. \"Considered and declined, because X\" is an acceptable outcome; silence is not.",
        "`git status` is clean of any temporary red-first edit — grep the four skills for the placeholder strings used during the break/revert cycle to confirm none survived.",
        "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` clean — this is the first phase that touches Python, so these three are load-bearing here rather than merely unchanged. mypy runs strict; new test functions need `-> None` annotations to match the existing style throughout tests/test_repo_structure.py."
      ],
      "commit_note": "Hand to `/commit`. Suggested subject: \"Guard the stage-token guard against going vacuous\". `/commit` also surfaces parked escalation entries against a row it is closing — expect it to surface any E-010 added here, which is the intended behavior, not a warning. Branch CI must stay green."
    },
    {
      "name": "Phase 5 — Close this item's own paperwork under the rule it just made enforceable, and hand off",
      "goal": "The item's artifacts and Index row reach the bugfix track's terminal stage correctly — which is the first live exercise of all three fixes on themselves. If any step here feels like fighting the skill, a fix is incomplete and the phase is diagnostic rather than clerical.",
      "steps": [
        "Write `requests/bugfix-requests/pipeline-status-rollover/IMPLEMENTATION_REPORT.md` from the template at implement-plan/SKILL.md:267-300, opening at `fixed` — the BUGFIX track's terminal word (requests/bugfix-requests/README.md:86) — NOT `implemented`. This is the Phase 3 fix exercised on itself: if the skill still pushes you toward `implemented`, Phase 3 did not land and you must go back.",
        "Make the acceptance ledger (report section 1) carry the red-to-green evidence verbatim: the baseline `3 failed, 79 passed` from Phase 1 step 1, and the final `82 passed` from Phase 3. That pair IS the bugfix track's definition of done (requests/bugfix-requests/README.md:35-46), and the regression test left behind is the three-test repro that was already committed in fb0406e — say so explicitly, since a reader may otherwise look for a newly added test.",
        "Roll the siblings — the Phase 2 fix exercised on itself. Set the Status blockquote to `fixed` in all of BUGFIX_REQUEST.md:1, ROOT_CAUSE_ANALYSIS.md:1, and IMPLEMENTATION_PLAN.md:1, and set the Index Stage cell at requests/bugfix-requests/README.md:98 to `fixed`. Four edits; missing any one reds test_index_stage_cells_match_their_artifact_status_headers, which is the original symptom.",
        "Archive per the track convention at requests/bugfix-requests/README.md:83 and :91-93 — one move into `_done/<slug>/` at the terminal stage, Index row stays with its link updated. ORDER MATTERS, for two independently verified reasons. (1) tests/test_request_links.py:36 skips `_done/`, so run the link checker on the LIVE tree before moving, or its coverage of these artifacts evaporates silently. (2) tests/test_repo_structure.py:475-477 resolves `track_dir / row[\"link\"]` and `continue`s when the directory does not exist — so if the Index link is not updated to `_done/<slug>/` in the SAME edit as the move, the stage guard stops firing on this row rather than failing. A stale link makes the guard vacuous, not red.",
        "Confirm no ROADMAP.md edit is owed. This is a bugfix-track item with no roadmap row; H1 `escalation-queue` (ROADMAP.md:197) is already DONE and unrelated. requests/README.md:73-74 documents `/commit`'s \"maps to no roadmap row\" path.",
        "Hand off. Per CLAUDE.md the agent may push the feature branch and open/merge its PR, but amend, force-push and any push to `main` stay the user's. Do not open the PR until `uv run pytest --tb=no -q` is fully green locally AND branch CI is green — `enforce_admins: true` means nobody merges past a red check anyway."
      ],
      "acceptance": [
        "`uv run pytest --tb=no -q` → all passed, including test_index_stage_cells_match_their_artifact_status_headers, with the item's four Status lines and its Index cell all reading `fixed`.",
        "`uv run pytest tests/test_request_links.py -q` → passes, run BEFORE the `_done/` move. Record that it ran on the live tree.",
        "After the move: the Index row at requests/bugfix-requests/README.md points at `_done/pipeline-status-rollover/` and that directory exists on disk. Verify by hand that tests/test_repo_structure.py:475's `item_dir.is_dir()` would be True — a passing test proves nothing here, because a broken link passes by `continue`.",
        "IMPLEMENTATION_REPORT.md's Status blockquote reads `fixed`, and `uv run pytest tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares -q` still passes (the report is an artifact, not a skill, so it is not graded by that guard — but a stray `> **Status:**` line copied into a SKILL.md would be).",
        "Self-check recorded: the report states, in one line, whether following the just-fixed skills produced a green repo with no manual patching. That sentence is the real acceptance for the whole bug — the original symptom was \"following a pipeline skill literally produces a red build\" (BUGFIX_REQUEST.md:6).",
        "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` clean."
      ],
      "commit_note": "Hand to `/commit`. Suggested subject: \"Close pipeline-status-rollover at the bugfix track's terminal stage\". `/commit` will run the fuller `/update-docs` sweep on a change of this shape — expect it to check whether CLAUDE.md's map and the requests/ Index rows still match, which is precisely what this phase edited. Then the PR is the user's to open and merge."
    }
  ],
  "testing": "THE REPRO IS ALREADY COMMITTED — DO NOT WRITE A NEW ONE. Commit fb0406e landed all three failing tests on this branch (tests/test_repo_structure.py:270, :299, :330). They are the regression test the bugfix track's definition of done requires (requests/bugfix-requests/README.md:35-46), and they are correctly placed: that README's table at :48-57 routes a \"CI or workflow config\" defect to \"a structural assertion in tests/test_repo_structure.py\". Phases 1-3 are graded by moving them red→green; only Phase 4 adds new tests.\n\nTHE SELECTORS, PHASE BY PHASE.\n  Baseline (Phase 1 step 1): `uv run pytest --tb=no -q` → must be exactly `3 failed, 79 passed` (82 collected). Capture this output; it is the report's before-half.\n  Phase 1: `uv run pytest tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares -q` → 1 passed. Full suite → `2 failed, 80 passed`.\n  Phase 2: `uv run pytest tests/test_repo_structure.py::test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory -q` → 1 passed. Full suite → `1 failed, 81 passed`.\n  Phase 3: `uv run pytest tests/test_repo_structure.py::test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token -q` → 1 passed. Full suite → `82 passed`, zero failed. This is the red-to-green transition.\n  Phase 4: full suite green at 82 + N, where N is the number of guards landed.\n  Phase 5: full suite green, and `uv run pytest tests/test_request_links.py -q` run explicitly BEFORE the `_done/` move.\n\nTHE PER-PHASE GATE, STATED PRECISELY. Because three tests are red at the start, an intermediate phase cannot show a fully green suite. The gate is therefore: the phase's named selector passes, the failing set is EXACTLY the documented remainder with zero new failures, and `uv run ruff check` + `uv run ruff format --check` + `uv run mypy` are all clean. Ruff-format is in the list because CI runs it (.github/workflows/ci.yml:40) and a locally-green `ruff check` does not imply it.\n\nREGRESSION SAFETY — WHAT COULD BREAK AND WHAT CATCHES IT.\n  1. Invariant A itself. tests/test_repo_structure.py:454 (test_index_stage_cells_match_their_artifact_status_headers) is the guard the whole bug is about, and RCA Open Question 4 settles that it stays unchanged. It must pass at every checkpoint. It is also the guard most likely to red from Phase 5's paperwork — which is intentional, that is it doing its job.\n  2. Dead pointers in skill prose. Every phase edits files inside `.claude/skills/`, a tree tests/test_request_links.py:35-36 sweeps. Mitigation baked into the plan: write paths in backticks, not as markdown links — `_dead_links` at :59-83 only resolves `[text](target)` syntax, so a backticked path carries zero dead-link risk while a link to a non-existent file reds the build.\n  3. Guard B going VACUOUS instead of green. `SKILL_STATUS_TEMPLATE` (:41) is `[a-z-]+` and does not match a `<placeholder>`, so replacing a template token with a placeholder produces no offender and no failure — coverage silently disappears. Phase 3 step 5 disposes this deliberately and Phase 4 item 1 adds the guard-on-a-guard that makes it impossible to do by accident.\n  4. Prose edits landing outside the guards' windows. `_advance_status_section` (:74-80) is fence-blind and stops at the first `^##` after the literal \"advance status\" — :167→:184 for create-implementation-plan, :254→:276 for implement-plan. Phase 2 verifies placement by calling the helper in a REPL rather than by eye.\n  5. Python-side regressions. Zero risk in Phases 1-3 (markdown only) — which is exactly why ruff/mypy staying byte-identical to baseline is a useful signal that no stray file was touched. Phase 4 is the only phase where they are load-bearing; mypy runs strict, so new test functions need `-> None` to match the existing module.\n  6. The 79 baseline-green tests. Every phase re-runs the full suite, so the arithmetic (79 + 3 = 82, no test added or removed in Phases 1-3) is itself an assertion that nothing else moved.\n\nRED-FIRST FOR ANYTHING NEW (Phase 4 only). Each added guard must be shown failing against a temporarily broken repo, then passing after the break is reverted, with both outputs captured. The track README's rule — \"a repro that passes against the broken code is not a repro\" (requests/bugfix-requests/README.md:43-46) — applies to regression guards too. Revert by editing the file back; `git checkout`/`restore`/`stash` are destructive-git and stay the user's (CLAUDE.md).\n\nWHAT IS NOT TESTED, AND SAID PLAINLY. No test covers the stage-DISCOVERY readers (create-implementation-plan:56, implement-plan:61, :93, scope-feature:48, diagnose-bug:46) unless Phase 4 item 2 lands. Phase 1's acceptance therefore includes a grep — `Select-String -Path \".claude\\skills\\*\\SKILL.md\" -Pattern '`root-cause`|`plan`'` returning zero hits — as a manual stand-in. It is a weaker check than a test and should be named as such in the report.\n\nCI. .github/workflows/ci.yml runs ruff check (:37), ruff format --check (:40), mypy (:43), pytest with coverage (:47), plus the Node and smoke jobs which this change cannot touch. The local gate above is the same set. Branch CI is expected RED from Phase 1 through Phase 2 and green from Phase 3 onward; a red check after Phase 3 is stop-and-fix, never a retry loop.",
  "risks": [
    "THE HIGHEST-PROBABILITY FAILURE: an edit lands outside the guard's window and the phase looks done while the test still fails. `_advance_status_section` (tests/test_repo_structure.py:74-80) slices from the literal \"advance status\" to the next `^##\\s` line, and NEXT_SECTION (:53) is fence-blind — so the window ends at `## 1. Onboarding` (create-implementation-plan:184) and `## 1. Acceptance ledger` (implement-plan:276), both of which sit INSIDE a markdown code fence. Prose added below the fence is invisible. Mitigation: Phase 2 verifies placement by calling the helper in a REPL, not by reading.",
    "GUARD B CAN GO VACUOUS RATHER THAN GREEN. `SKILL_STATUS_TEMPLATE` (tests/test_repo_structure.py:41) captures `[a-z-]+`, so a template rewritten as `> **Status:** <the terminal word> · …` matches nothing, reports no offender, and passes — while silently removing that skill from the guard's coverage. This is the exact class of silence the bug is about, recreated by its own fix. Phase 3 step 5 forces an explicit disposition and Phase 4 item 1 is the structural answer.",
    "FIXING A WRITER WITHOUT ITS READER BREAKS STAGE DISCOVERY, AND NO TEST NOTICES. create-implementation-plan:56 looks for a bugfix RCA at `root-cause` and implement-plan:61 looks for an item at the `plan` stage — both tokens Phase 1 removes. Land Phase 1's writer edits alone and the next real pipeline run finds no work item and either stops or guesses. The RCA does not enumerate these three sites (create-implementation-plan:56, implement-plan:61, implement-plan:93); they were found by grep during planning and are grouped into Phase 1 for exactly this reason.",
    "DERIVING THE TERMINAL FROM A TWO-VALUED RESOLUTION DOES NOT ACTUALLY FIX THE THIRD TRACK. implement-plan/SKILL.md:53-55 resolves only `bugfix` vs `feature`; calibration falls through to `feature` and its work-dir template `requests/<track>-requests/<slug>/` does not even compose for `calibration-findings`. An implementer who reads RCA Open Question 2 as \"the machinery already exists\" and writes one sentence will ship defect 3 half-fixed with the guard green — because the guard only inspects the advance-status window, not the resolution at :53.",
    "PUSHING A KNOWINGLY RED BRANCH. `/commit` pushes on approval, so Phases 1 and 2 leave branch CI red by design. The risk is that a red check is mistaken for a real failure and triggers a retry loop, or that the PR is opened early and cannot merge under `enforce_admins: true`. Mitigation: each commit note states the expected remaining failure by name, and no PR is opened before Phase 3. Open Question 4 offers squashing Phases 1-3 if the user prefers never to push red.",
    "THE `_done/` MOVE CAN MAKE A GUARD VACUOUS INSTEAD OF RED. tests/test_repo_structure.py:475-477 resolves `track_dir / row[\"link\"]` and `continue`s when the directory is absent — so archiving into `_done/<slug>/` without updating the Index link in the same edit silently switches the stage check off for that row rather than failing. And tests/test_request_links.py:36 skips `_done/` entirely, so the artifacts' links stop being checked the moment they move. Phase 5 sequences the link run before the move for this reason.",
    "SCOPE CREEP INTO THE `next:` FIELD. RCA hardening (a) points at make-bugfix-request:130's `next: root-cause` and it is tempting to guard the field. Doing so would red five skills that are not wrong: requests/feature-requests/README.md:104 declares `next:` as `<stage or \"implement\">` and every skill writes an ACTION there (`scope`, `plan`, `implement`, `commit`). Tightening it requires changing three track READMEs first — a separate request. Phase 4 item 3 declines it in writing so the next reader does not re-open it.",
    "OVER-EDITING THE ORDINARY ENGLISH WORD \"implemented\". implement-plan/SKILL.md:218, :280 and :289 use it as plain prose (\"symbols you implemented\", \"the phases implemented\"). A blind find-and-replace corrupts them. Only unconditional INSTRUCTIONS to write the word are in scope, and Phase 3's last step says to read every hit rather than replace them.",
    "THE FIX IS GRADED BY REGEXES, SO CLEVER WORDING CAN PASS WHILE BEING WRONG FOR A HUMAN. Both Phase 2 and Phase 3 could satisfy their guards with a single keyword-bearing sentence that a cold agent cannot act on. The plan mitigates by requiring the added prose to say WHAT to do, WHY (naming the guard it protects), and WHICH files — and by requiring two independent matching phrases so a later reword of one cannot silently re-red the guard.",
    "DIAGNOSE-BUG'S FOUR TERMINAL EXIT WORDS ARE NOT IN ANY GRAMMAR. diagnose-bug/SKILL.md:99-102 uses `closed-works-as-intended`, `cannot-reproduce` and `redirected-to-feature` as verdict-driven statuses. They escape guard B only because they appear in prose rather than in a `> **Status:**` line. A future edit that promotes any of them into a template blockquote reds guard B immediately — which is correct behavior, but will look like a regression from this fix. Note it in the report so the next reader is not surprised.",
    "TOUCHING A SKILL'S DISPATCH DESCRIPTION. diagnose-bug/SKILL.md:7 carries the stage chain inside the frontmatter description that drives skill selection. Changing the chain token is right; stripping the natural-language trigger phrase \"root cause\" would degrade dispatch. Phase 1 separates the two explicitly, and Open Question 3 lets the user decline the whole step."
  ],
  "files_to_touch": [
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\create-implementation-plan\\SKILL.md",
      "change": "Phase 1: `plan` → `planned` at :172, :173, :176 (defect 2); make the authority pointer at :177-178 name the two track READMEs by backticked path instead of \"this README\"; :56 reader — \"a confirmed-bug RCA at `root-cause`\" → `diagnosed`. Phase 2: insert a sibling-rollover bullet before the Index bullet at :170, inside the :167→:184 advance-status window, containing both \"Status blockquote\" and \"sibling\" (defect 1)."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\implement-plan\\SKILL.md",
      "change": "Phase 1: readers only — :61 \"an item at the `plan` stage\" → `planned`, and :93's worked example `plan · … · decided · next: implement` → `planned` with its trailing clause adjusted. Phase 2: sibling-rollover bullet before the Index bullet at :257, inside the :254→:276 window, terminal word left as a placeholder phrase. Phase 3: make :53-55 track resolution three-valued with three literal work-dir paths; add the per-track terminal table plus the phrase \"the track's terminal stage word\" inside the window; de-hardcode :259 and :260; dispose the :268 template blockquote per Open Question 1; reword the unguarded track-blind restatements at :29 and :324. Leave the ordinary-English uses at :218, :280, :289 alone."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\diagnose-bug\\SKILL.md",
      "change": "Phase 1 only (defect 4): `root-cause` → `diagnosed` at :97 (verdict line), :107 (the template blockquote guard B grades), and :154 (Step 5 Index instruction); and the stage chain inside the dispatch description at :7, keeping its natural-language trigger phrases intact. PRESERVE verbatim: :152's \"Status blockquote\" phrase (it is why this skill already passes the rollover guard) and :154's \"(or the terminal stage word)\" parenthetical (the in-repo precedent Phase 3 copies)."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\tests\\test_repo_structure.py",
      "change": "Phase 4 ONLY — untouched in Phases 1-3, since the three repro tests at :270, :299 and :330 are the grader and must not move under the thing they grade. Additions, each gated on user disposition: a guard-on-the-guard asserting SKILL_STATUS_TEMPLATE still parses a declared token from the four concrete-token skills; a narrow guard on the \"at the `X` stage\" discovery literals; and a per-track Index-cell-vs-grammar assertion beside :454. Note `_declared_stage_tokens()` at :63 unions all three grammars, so the per-track check needs its own variant. mypy is strict — annotate new tests `-> None`."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\make-bugfix-request\\SKILL.md",
      "change": "Phase 4 item 3, one word: :130's `next: root-cause` → a token consistent with the Phase 1 rename. The stage field there (`intake`) is already correct and guard B already passes on this file; this is prose consistency, not a guard fix, and is explicitly NOT an argument for guarding the `next:` field."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\ESCALATIONS.md",
      "change": "Phase 4, only if something is declined with a real alternative and a nameable moment. Append under `## Open` following the six-field format at :72-99 (all six guarded by tests/test_escalations.py). Next free id is E-010 (highest existing is E-009 at :225). `Bears on:` must be a bare roadmap item / phase / `post-v1` with nothing else on the line per :75 — H2 (ROADMAP.md:198) is the plausible moment. Never renumber to E-000 (:101-103)."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\IMPLEMENTATION_REPORT.md",
      "change": "Phase 5, new file, from the template at implement-plan/SKILL.md:267-300. Opens at `fixed` — the bugfix terminal per requests/bugfix-requests/README.md:86, NOT `implemented`. Its acceptance ledger carries the baseline `3 failed, 79 passed` and the final `82 passed` as the red-to-green evidence, and names fb0406e's three tests as the regression guard left behind."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\BUGFIX_REQUEST.md",
      "change": "Status blockquote at :1 rolls `diagnosed` → `planned` (when this plan lands) → `fixed` (Phase 5). No other edit — the intake artifact is decided and is consumed, not revised."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\ROOT_CAUSE_ANALYSIS.md",
      "change": "Status blockquote at :1 rolls `diagnosed` → `planned` → `fixed` (Phase 5). Its body is DECIDED and must not be edited — the verdict, the evidence, and the four Open Question answers are the prior stage's output."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\README.md",
      "change": "Phase 5: Index Stage cell at :98 → `fixed`, and the row's link updated to `_done/pipeline-status-rollover/` in the SAME edit as the archive move — tests/test_repo_structure.py:475-477 `continue`s on a missing directory, so a stale link switches the stage guard off rather than failing it. The grammar declaration at :86 is the authority this fix enforces and must NOT change."
    }
  ],
  "code_references": [
    {
      "ref": "tests/test_repo_structure.py:270 test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares",
      "claim": "Phase 1's grader. Verified RED today with `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}` against declared vocabulary `['diagnosed', 'fixed', 'implemented', 'intake', 'planned', 'retuned', 'scoped']`. Globs `.claude/skills/*/SKILL.md` and inspects only `> **Status:**` template lines."
    },
    {
      "ref": "tests/test_repo_structure.py:299 test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory",
      "claim": "Phase 2's grader. Verified RED with `['create-implementation-plan', 'implement-plan']`. Iterates STAGE_ADVANCING_SKILLS (:46-51) and requires ROLLS_A_SIBLING (:55) to match inside `_advance_status_section`."
    },
    {
      "ref": "tests/test_repo_structure.py:330 test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token",
      "claim": "Phase 3's grader. Verified RED: \"implement-plan's advance-status section hardcodes ['implemented'] and serves all three tracks, whose terminals are ['fixed', 'implemented', 'retuned']\". Passes if DERIVES_TERMINAL matches OR ≥2 terminal tokens appear in the window."
    },
    {
      "ref": "tests/test_repo_structure.py:74-80 _advance_status_section",
      "claim": "Defines the window every Phase 2 and Phase 3 prose edit must land inside: from the literal 'advance status' to the next `^##\\s` line. NEXT_SECTION (:53) is fence-blind, so the window ends at a `##` heading inside the template code fence — :167→:184 for create-implementation-plan, :254→:276 for implement-plan."
    },
    {
      "ref": "tests/test_repo_structure.py:41 SKILL_STATUS_TEMPLATE",
      "claim": "`^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)` — captures `[a-z-]+`, so a `<placeholder>` blockquote matches nothing and produces no offender. This is how guard B can go vacuous rather than green, and is the reason Phase 3 step 5 and Phase 4 item 1 exist."
    },
    {
      "ref": "tests/test_repo_structure.py:454 test_index_stage_cells_match_their_artifact_status_headers",
      "claim": "Invariant A — the guard that is currently GREEN and must stay green at every checkpoint. RCA Open Question 4 settles that it is exactly right and is not modified by this fix. Its every-artifact loop at :479 is what makes stale siblings load-bearing."
    },
    {
      "ref": "tests/test_repo_structure.py:475-477",
      "claim": "`item_dir = track_dir / row[\"link\"]` followed by `if not item_dir.is_dir(): continue` — a stale Index link makes the stage guard VACUOUS rather than red. Drives Phase 5's requirement that the `_done/` move and the link update happen in one edit."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:172",
      "claim": "Defect 2, site 1: \"cell to `plan` (match the row by its `[<slug>]` link)\". Verified by reading. → `planned` in Phase 1."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:176",
      "claim": "Defect 2, site 3 and the line guard B actually grades: `> **Status:** plan · created <YYYY-MM-DD> · decided · next: implement`. The HTML comment immediately below at :177-178 cites 'this README status grammar' as its authority in the same breath as violating it."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:56",
      "claim": "A stage-discovery READER the RCA does not enumerate: 'or `requests/bugfix-requests/README.md` for a confirmed-bug RCA at `root-cause`'. Unguarded. Must move with defect 4 in Phase 1 or stage 3 hunts a token that no longer exists."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:53-55",
      "claim": "The track resolution RCA Open Question 2 says the terminal word can follow from. Verified two-valued: '`bugfix` when the path is under `bugfix-requests/`, else `feature` (the default)', with work-dir `requests/<track>-requests/<slug>/` — a template that does not compose for `calibration-findings`. Phase 3 makes it three-valued."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:61",
      "claim": "A second unenumerated READER: 'for an item at the `plan` stage'. Breaks the moment defect 2 is fixed; grouped into Phase 1."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:91-93",
      "claim": "The disposition gate's worked example: 'a ready plan reads `plan · … · decided · next: implement`, so the word `plan` appearing is *expected*'. Becomes false after Phase 1 and must be updated in the same phase."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:259-260",
      "claim": "Defect 3's hardcoded instructions inside the guarded window: set the Index Stage cell to `implemented`, and 'The report opens at `implemented · created <today> · decided · next: commit`'. Both become track-derived in Phase 3."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:268",
      "claim": "The terminal template blockquote `> **Status:** implemented · …`. Sits inside the :254→:276 window and is simultaneously graded by guard B — which is why rewriting it as a placeholder trades a green for a silence. Open Question 1."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:29 and :324",
      "claim": "Two track-blind restatements OUTSIDE the guarded window: 'The feature ends at status `implemented`' and 'the report + `implemented` status'. No test will ever catch these; Phase 3 fixes them because they are exactly the unguarded prose drift this bug is about."
    },
    {
      "ref": ".claude/skills/diagnose-bug/SKILL.md:107",
      "claim": "Defect 4, the graded line: `> **Status:** root-cause · created <YYYY-MM-DD> · decided · next: <plan | fix | none | <feature-slug>>`. Its prose siblings are :97 and :154, and the stage chain also appears in the dispatch description at :7."
    },
    {
      "ref": ".claude/skills/diagnose-bug/SKILL.md:152-154",
      "claim": "The line that already gets rollover right ('Update the `BUGFIX_REQUEST.md` Status blockquote and the **Index** row … to `root-cause` (or the terminal stage word)'). The phrase 'Status blockquote' is why this skill passes the rollover guard, and '(or the terminal stage word)' is the precedent RCA:107-108 names for Phase 3. Preserve both while changing the token."
    },
    {
      "ref": ".claude/skills/scope-feature/SKILL.md:136-146",
      "claim": "The reference implementation Phase 2 copies. :139 rolls the sibling, :140-143 sets the Index cell, :144 opens the new artifact, and :136-137 frames them as in-place edits under a read-only-git rule."
    },
    {
      "ref": "requests/bugfix-requests/README.md:86",
      "claim": "The bugfix grammar `intake → diagnosed → planned → fixed` — the authority for this item's own Status words and for the `fixed` terminal in Phase 5. Also :35-46, the definition of done (red goes green + a regression test left behind, repro must have failed first), and :48-57 which routes a CI/workflow-config defect to tests/test_repo_structure.py."
    },
    {
      "ref": "requests/feature-requests/README.md:104 and :106",
      "claim": ":106 declares the feature grammar. :104 declares the blockquote shape and, load-bearingly, declares `next:` as `<stage or \"implement\">` — i.e. NOT a stage-grammar field. This is the grounded reason Phase 4 item 3 declines the `next:` hardening."
    },
    {
      "ref": "requests/calibration-findings/README.md:88",
      "claim": "The third grammar, `intake → diagnosed → planned → retuned`. Verified present. Its Index is empty and the track has never been run — RCA Open Question 3 leaves that `unconfirmed` deliberately and covers it by guarding rather than observing."
    },
    {
      "ref": "tests/test_request_links.py:59-83 _dead_links",
      "claim": "Only resolves markdown-link syntax `[text](target)`; backticked bare paths are not checked. This is why every path written into a skill by this fix should be backticked rather than linked. :35-36 confirms `.claude/skills/` is a scanned tree; :86-97 is the guard-on-a-guard idiom Phase 4 item 1 copies."
    },
    {
      "ref": "ESCALATIONS.md:72-99",
      "claim": "The six-field entry format for parking a declined hardening item, every field guarded by tests/test_escalations.py. :75 is the strict bare-moment `Bears on:` rule, :101-103 warns E-000 is a template, and :225 (E-009) is the highest existing id, so the next free one is E-010."
    },
    {
      "ref": "ROADMAP.md:197-198",
      "claim": "H1 `escalation-queue` is DONE (merged as PR #22 = 2f91ab5) and H2 `domain-engineer` is NOT STARTED. This bugfix maps to no roadmap row — requests/README.md:73-74 documents `/commit`'s path for that — and H2 is the plausible `Bears on:` moment for any parked pipeline-guard work."
    },
    {
      "ref": ".github/workflows/ci.yml:37,:40,:43,:47",
      "claim": "The CI gates the local per-phase gate mirrors: `ruff check`, `ruff format --check`, `mypy`, `pytest`. Note `ruff format --check` is a separate step, so a green `ruff check` locally does not imply CI green."
    },
    {
      "ref": "git commit fb0406e",
      "claim": "'Diagnose the pipeline status drift and land its red repro' — the commit that landed the RCA and the three failing tests on branch `bugfix/pipeline-status-rollover`. Verified NOT on origin/main: `git show origin/main:tests/test_repo_structure.py` contains none of the three test functions, and origin/main carries only BUGFIX_REQUEST.md from this item's directory. The branch is deliberately red and its PR cannot merge until Phase 3."
    }
  ],
  "open_questions": [
    "PHASE 3, THE ONE REAL DESIGN CALL. How should implement-plan/SKILL.md:268's terminal template blockquote read? (a) Keep a concrete grammar-declared token plus a one-line 'swap for your track's terminal' note — guard B stays pointed at this line. (b) Use `> **Status:** <the track's terminal stage word> · …` — cleaner prose, but SKILL_STATUS_TEMPLATE (tests/test_repo_structure.py:41) then matches nothing and this skill silently leaves guard B's coverage. RECOMMEND (a). If (b) is chosen, Phase 4 item 1 becomes mandatory rather than optional.",
    "PHASE 4 DISPOSITION — which hardening items land? Item 1 (guard-on-the-guard, recommended and mandatory under Open Question 1(b)); item 2 (guard the four stage-discovery reader literals, recommended); item 4 (Index-cell-vs-grammar, RCA hardening (b), cheap and recommended). Declined with reasons written down: item 3 (the `next:` field, RCA hardening (a)) and item 5 (the `_done/` skip, RCA hardening (c)). Anything declined that has a real alternative and a nameable moment gets an E-010 entry rather than silence.",
    "Should diagnose-bug/SKILL.md:7's dispatch-description stage chain ('intake -> root-cause -> reuse plan/implement') be updated to `diagnosed`? RECOMMEND yes — it is the same prose restatement the bug is about — but it lives inside the description that drives skill selection, so the natural-language trigger phrases around it must be left untouched. Declining costs only consistency, not correctness.",
    "COMMIT GRANULARITY. Phases 1-3 as three commits gives per-defect reviewability at the cost of a branch whose CI is RED until Phase 3 (`/commit` pushes on approval). Squashing them into one commit means the branch is never pushed red. RECOMMEND three commits with the expected remaining failure named in each commit note — the red is informative here, and `enforce_admins: true` prevents anything merging past it anyway. The user's call.",
    "BRANCH NAMING, noted rather than fixed. The live branch is `bugfix/pipeline-status-rollover`, while implement-plan/SKILL.md:272's report template prescribes `**Branch:** implement/<slug>` and the last merged feature branch was `phase1/escalation-queue`. Three conventions, none written down anywhere authoritative — the same restatement-drift shape as the bug being fixed, one level up. RECOMMEND keeping the existing branch, recording the mismatch in the report, and NOT widening this fix to cover it.",
    "RCA Open Question 3 stays `unconfirmed` and this plan deliberately does not resolve it: whether the calibration track routes through the shared back half in practice. Its Index at requests/calibration-findings/README.md is empty and nobody has run it. Phase 3 covers it in principle by making the resolution three-valued and the terminal table complete; confirming it against a real calibration run is a task for whenever Phase 2 of the roadmap produces one. Flagged because it is the only `unconfirmed` claim this plan touches — and note it is a claim about an internal track, not about an external data source, so no source-verification phase is owed (docs/data-sources.md does not exist in this repo; the data catalogue is docs/data-access.md and this change touches nothing in it)."
  ]
}
```

---

## Planner: 2

```json
{
  "planner": "domain-convention",
  "ok": true,
  "architecture_notes": "## What is actually broken, in one sentence\n\nSix pipeline skills each restate the request-track status vocabulary as a hand-typed literal in their own prose, and nothing mechanically links those literals to the three track READMEs that declare the grammar — so three of the six drifted. The RCA is decided: the cause is the missing link, not the individual typos.\n\n**This change touches NO data.** No dataset, no `datasets/manifest.json`, no ledger, no ruleset, no economy, no cloud money, no `src/`, no `app/`. `docs/data-access.md` is untouched and no unconfirmed source claim is load-bearing. Per the stage-3 section menu (`.claude/skills/create-implementation-plan/SKILL.md:218-221`), the plan carries **no §9 data-contracts section** — that is a deliberate omission, not a gap. The one unconfirmed claim in play (RCA Open Question 3: whether the calibration track routes through the shared back half — `unconfirmed`, its Index at `requests/calibration-findings/README.md:94` is empty) is handled by *guarding* rather than by *assuming*: no phase below depends on calibration behaving any particular way, and the fix makes `implement-plan` correct for it in principle without waiting for the track to be exercised.\n\n## The two invariants (the shape the fix must respect)\n\n| | Invariant | Guarded by | Status |\n|---|---|---|---|\n| **A** | The Index Stage cell agrees with **every** `*.md` in the item directory | `tests/test_repo_structure.py:454-487`, whose per-artifact loop is at `:479` | already green, unchanged by this fix |\n| **B** | The stage word is one the **track's declared grammar** contains | `tests/test_repo_structure.py:270-296` (new, RED) | this is what the fix delivers |\n\nInvariant A compares a directory **against itself**, which is exactly why three of the four defects were silent: a skill that writes an invented token *consistently* into both the Index and its artifact satisfies A forever. The RCA settled that A is correct and stays untouched; only B is added.\n\n## The test machinery the fix must satisfy (read this before editing a single word)\n\nThe three red tests are **prose-shape assertions over `.claude/skills/*/SKILL.md`**, so the fix is edits to markdown that must land in specific *regions* matched by specific *regexes*. Getting the wording right is the whole job.\n\n- `_declared_stage_tokens()` (`tests/test_repo_structure.py:63-71`) parses `STATUS_GRAMMAR` (`:38`, `**Status grammar:** …`) out of all three track READMEs and unions the backticked words → `{intake, scoped, planned, implemented, diagnosed, fixed, retuned}`. **The three track READMEs are the source of truth. Do not move the grammar lines** (`requests/feature-requests/README.md:106`, `requests/bugfix-requests/README.md:86`, `requests/calibration-findings/README.md:88`) — the parser reads them from exactly there.\n- `SKILL_STATUS_TEMPLATE` (`:41`) = `^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)`. It matches the six template blockquotes and **only** those. A placeholder starting with `<` does not match at all — which means it silently removes that skill from test-1 coverage. Prefer a real, declared token plus a prose note.\n- `_advance_status_section()` (`:74-80`) slices from the first case-insensitive `advance status` (`:52`) to the next `^## ` (`:53`). **The regex is fence-blind** — it does not know about ```` ``` ```` — so in `implement-plan` the slice runs from `:254` to just before `## 1. Acceptance ledger` at `:276`, and therefore *includes* the template blockquote at `:268`. Verified by reading the assertion's own printed section text. Anything you add for tests 2 and 3 must fall inside that window: **`create-implementation-plan` :167→:183**, **`implement-plan` :254→:275**.\n- `ROLLS_A_SIBLING` (`:55`) = `Status blockquote|sibling|every artifact`, case-insensitive.\n- `DERIVES_TERMINAL` (`:60`) = `terminal (?:stage word|token)|track's terminal`, and test 3 (`:349`) passes if that matches **or** more than one of `{implemented, fixed, retuned}` (`:59`) appears in the section. The recommended wording satisfies both, so the test cannot be gamed by accident.\n\n## The six restatements, enumerated (verified by grep)\n\n| Skill | Line | Token written | Correct? |\n|---|---|---|---|\n| `make-feature-request` | `:176` | `intake` | ✅ |\n| `make-bugfix-request` | `:130` | `intake` (but `next: root-cause`) | ✅ stage / ⚠️ `next:` |\n| `scope-feature` | `:149` | `scoped` | ✅ — and `:136-146` is the **correct rollover pattern** |\n| `create-implementation-plan` | `:176` | `plan` | ❌ defect 2 |\n| `diagnose-bug` | `:107` | `root-cause` | ❌ defect 4 |\n| `implement-plan` | `:268` | `implemented` (track-blind) | ❌ defect 3 |\n\n## Branch state — read this first, it is not what the stale git snapshot says\n\nThe working branch is **`bugfix/pipeline-status-rollover`** (not `phase1/escalation-queue`). Commit `fb0406e` \"Diagnose the pipeline status drift and land its red repro\" is **on this branch and pushed to origin, but NOT merged to main** — `git diff HEAD origin/main --stat` shows `ROOT_CAUSE_ANALYSIS.md` (+143) and `tests/test_repo_structure.py` (+136) as additions this branch carries. **Do not create a new branch and do not branch off main** — the red repro only exists here. Continue on `bugfix/pipeline-status-rollover`.\n\n## Baseline, measured just now (not inferred)\n\n- `uv run pytest -q` → **3 failed, 79 passed** (82 total). The three failures are exactly the RCA's three repro tests; every other test is green, so the repro isolates this defect and nothing else.\n- `uv run ruff check` → `All checks passed!`\n- `uv run mypy` → `Success: no issues found in 16 source files`\n- CI runs the same four gates plus `ruff format --check`: `.github/workflows/ci.yml:37, :40, :43, :47`.\n\n## Definition of done (the bugfix track's, not a feature's)\n\n`requests/bugfix-requests/README.md:35-46`: **the red reproduction goes green and a regression test is left behind.** The regression test is already written — it *is* the repro (`fb0406e`), which is the ideal case. `:57` also names the right home for a CI/config-shaped defect: \"a structural assertion in `tests/test_repo_structure.py`\" — which is where every guard this plan adds belongs.\n\n## Roadmap mapping\n\nThere is **no roadmap row for this bug**. `ROADMAP.md:197` (H1 `escalation-queue`) is `DONE`; nothing in the H-series or Phase 1 covers pipeline-skill hygiene. `/commit` has an explicit path for this — `.claude/skills/commit/SKILL.md:146`, \"say 'no roadmap row'\". Expect and use it; do not invent a row.",
  "onboarding_files": [
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\ROOT_CAUSE_ANALYSIS.md",
      "why": "The decided upstream artifact. Read in full and CONSUME it — its verdict (confirmed-bug, four instances across three skills), its evidence file:lines, and its tiered fix posture are settled. Do not re-open the cause. Its 'Answers to the request's Open Questions' section is where the fix's shape comes from."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\BUGFIX_REQUEST.md",
      "why": "Context only. Its 'Affected Area & Pointers' (:69-83) is the fastest index of every file this touches, and its Reproduction section (:27-40) explains why the two defect classes fail independently."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\tests\\test_repo_structure.py",
      "why": "The repro AND the regression guard, in one file. Read :30-80 (the constants and the two helpers) before editing any skill — the fix is prose that must satisfy specific regexes over specific line windows. Then :270-353 (the three red tests) and :454-487 (the green invariant-A guard the fix must not disturb)."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\scope-feature\\SKILL.md",
      "why": "Lines 136-149 are THE correct pattern the fix copies: :139 rolls the sibling, :140-143 sets the Index cell, :144 opens the new artifact at a grammar-legal token, :149 is the template blockquote. Whatever you write into the other two skills should look like this."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\create-implementation-plan\\SKILL.md",
      "why": "Defect 1 (Step 5, :167-173 — no sibling rollover) and defect 2 (:176 writes `plan`). Also :49-51 and :56/:65, the track-resolution prose that the token rename ripples into. Note the irony at :177-178: it cites 'this README status grammar' as authority in the same breath as violating it."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\implement-plan\\SKILL.md",
      "why": "Defect 1 again (Step 7, :257-260) and defect 3 (:259 and :268 hardcode `implemented` while the skill explicitly serves all three tracks). Step 1 (:56-105) is where the track is already resolved from the artifact path — RCA Open Question 2's answer is that the terminal word can follow from that same resolution."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\diagnose-bug\\SKILL.md",
      "why": "Defect 4, found by the diagnosis itself: :107 writes `root-cause`, a token no grammar declares. :154 already shows the tolerated derived-terminal shape ('or the terminal stage word') that test 3's DERIVES_TERMINAL regex was written around."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\README.md",
      "why": "The track contract this bug runs under: the grammar at :86 (`intake → diagnosed → planned → fixed`), the definition of done at :35-46, the where-does-the-test-live table at :50-57, and the `_done/` archive convention at :83 and :91-92 that the final phase executes."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\README.md",
      "why": "Line 16 is load-bearing for the design call: 'Each track's README is the contract — layout, status grammar…'. That is why the fix makes the track READMEs authoritative rather than relocating the grammar somewhere shared."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\commit\\SKILL.md",
      "why": "The only sanctioned commit path. :110-149 is the roadmap-status step (this change hits the :146 'no roadmap row' branch), :141 surfaces parked escalation entries, :216-238 covers the push and the never-force/never-main rules. Every phase below ends here."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\ESCALATIONS.md",
      "why": "Only if Phase 5 runs. :73-79 is the six-field entry format, every field of which tests/test_escalations.py checks; :24 states that no agent resolves an entry — agents park, the user disposes."
    }
  ],
  "phases": [
    {
      "name": "Phase 1 — Minimal fix: four prose edits, red repro to green",
      "goal": "Turn all three RCA repro tests GREEN by making the four drifted skill restatements grammar-legal and by adding the sibling-rollover instruction to stages 3 and 4. This is the RCA's Minimal tier and the whole build-greening unit — the suite cannot be green partway through, so all four edits land together.",
      "steps": [
        "Confirm the starting state before touching anything. Run `uv run pytest -q` and record the output: it must be `3 failed, 79 passed`, and the three failures must be exactly `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares`, `test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory`, `test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token`. Confirm `git branch --show-current` reads `bugfix/pipeline-status-rollover`. If either differs, STOP and report — you are not on the branch that carries the repro.",
        "Read `tests/test_repo_structure.py:30-80` in full first. The four edits below must land inside the regex windows described there; `_advance_status_section` is fence-blind, so the addressable window is `create-implementation-plan` :167→:183 and `implement-plan` :254→:275.",
        "EDIT A (defect 2, `create-implementation-plan/SKILL.md`) — change every stage literal `plan` to `planned`: the Index instruction at :171-172 ('set this item's **Index** row Stage cell to `plan`' → `` `planned` ``), the artifact line at :173 ('opens at stage `plan`' → 'opens at stage `planned`'), and the template blockquote at :176 (`> **Status:** plan · …` → `> **Status:** planned · …`). Leave `next: implement` alone — that field is an action word, not a stage word. Leave the comment at :177-178 intact; it is now telling the truth.",
        "EDIT B (defect 1, `create-implementation-plan/SKILL.md`) — insert a rollover bullet into the Step 5 bullet list between :172 and :173, modeled verbatim in shape on `scope-feature/SKILL.md:139`. Required wording, because it is what ROLLS_A_SIBLING (`tests/test_repo_structure.py:55`) matches AND what an agent actually needs to do: `- Roll **every artifact already in the directory** — the intake doc (`FEATURE_REQUEST.md` / `BUGFIX_REQUEST.md`) and the upstream artifact (`PROJECT_SCOPE.md` / `ROOT_CAUSE_ANALYSIS.md`) — by setting each one's Status blockquote to `planned` as well. The Index cell and every artifact in the directory must agree, or `tests/test_repo_structure.py::test_index_stage_cells_match_their_artifact_status_headers` reds the build.`",
        "EDIT C (defects 1 + 3, `implement-plan/SKILL.md` Step 7) — rewrite the :257-260 bullets so the terminal word is DERIVED from the track already resolved in Step 1, and so siblings roll. Set the Index bullet to name the derivation and all three terminals: '…set this item's **Index** row Stage cell to the **track's terminal stage word** — `implemented` (feature), `fixed` (bugfix), `retuned` (calibration) — read off the resolved track README's **Status grammar** line, never from memory.' Then add the rollover bullet: '- Roll **every artifact already in the directory** — the intake doc, the upstream `PROJECT_SCOPE.md` / `ROOT_CAUSE_ANALYSIS.md`, and the `IMPLEMENTATION_PLAN.md` — by setting each one's Status blockquote to that same terminal word.' Then change :260 to 'The report opens at the same terminal word · `created <today>` · `decided` · `next: commit`.'",
        "EDIT C2 (keep test-1 coverage on `implement-plan`) — leave the template blockquote at :268 as a real declared token (`> **Status:** implemented · created <YYYY-MM-DD> · decided · next: commit`) and add ONE prose line immediately BEFORE the ```markdown fence at :267: '`implemented` below is the **feature** track's terminal; write the resolved track's own — `fixed` for a bugfix, `retuned` for a calibration finding.' Do NOT replace the token with a `<placeholder>`: SKILL_STATUS_TEMPLATE (`tests/test_repo_structure.py:41`) is anchored on `[a-z-]+` and a leading `<` makes the line invisible to the conformance test, silently dropping this skill from coverage.",
        "EDIT D (defect 4, `diagnose-bug/SKILL.md`) — change the template blockquote at :107 from `root-cause` to `diagnosed`; change the verdict prose at :97 from '`root-cause · … · decided · next: plan`' to '`diagnosed · … · decided · next: plan`'; change the Step 5 instruction at :154 from 'to `root-cause` (or the terminal stage word)' to 'to `diagnosed` (or the terminal stage word)'. Keep the parenthetical — it is the in-repo precedent DERIVES_TERMINAL was written around. Do NOT touch :5-7 or `make-bugfix-request/SKILL.md:5-6`, where 'root-cause' is English prose describing the analysis, not a stage token.",
        "Re-run the three repro tests specifically: `uv run pytest tests/test_repo_structure.py -q`. All 82 assertions in that module must pass. If test 3 still fails, re-read the printed section text in the assertion output — it prints the exact slice `_advance_status_section` produced, which tells you whether your edit landed inside the window."
      ],
      "acceptance": [
        "`uv run pytest -q` reports 82 passed, 0 failed — the three RCA repro tests are GREEN and none of the 79 previously-passing tests regressed.",
        "`uv run ruff check`, `uv run ruff format --check`, and `uv run mypy` are all clean (they were clean at baseline; this phase touches only markdown, so any new failure means something unintended was edited).",
        "`grep -n 'Status:\\*\\* ' .claude/skills/*/SKILL.md` shows six template blockquotes and every stage word is one of `intake` / `scoped` / `planned` / `diagnosed` / `implemented` — no `plan`, no `root-cause`.",
        "`.claude/skills/implement-plan/SKILL.md` Step 7 names all three terminal words and the phrase 'track's terminal stage word'; it no longer instructs `implemented` unconditionally.",
        "Both `create-implementation-plan` Step 5 and `implement-plan` Step 7 contain an explicit instruction to roll the artifacts already in the directory, phrased as an action an agent can follow — not a keyword inserted to satisfy a regex."
      ],
      "commit_note": "Fix the four drifted stage restatements: `plan`→`planned`, `root-cause`→`diagnosed`, a track-derived terminal in `implement-plan`, and the sibling-rollover instruction in stages 3 and 4. Turns the RCA's three red repro tests green; the repro stays as the regression guard. No roadmap row (bugfix)."
    },
    {
      "name": "Phase 2 — Close the ripple the rename leaves behind, and cite the authority",
      "goal": "Fix the restatements that no test can see but that Phase 1 just invalidated, and resolve the RCA's one genuinely open design call ('a shared prose home vs. guard it and keep the restatements') in the cheapest correct direction: keep the six restatements where they are, but make each advance-status step name the track README as its authority.",
      "steps": [
        "Fix the stage-word references Phase 1 made stale. These are prose, not blockquotes, so the conformance test cannot see them — but leaving them makes the skills self-contradictory (stage 3 would go looking for an Index row reading `root-cause` that now reads `diagnosed`): `.claude/skills/create-implementation-plan/SKILL.md:56` ('for a confirmed-bug RCA at `root-cause`' → `` `diagnosed` ``) and `:65` ('a ready bugfix RCA reads `root-cause · … · decided · next: plan`' → `` `diagnosed · …` ``).",
        "Fix the same class in `implement-plan/SKILL.md` Step 1: the Index-lookup sentence that says to look 'for an item at the `plan` stage' → '`planned`', and the disposition-gate sentence 'a ready plan reads `plan · … · decided · next: implement`, so the word `plan` appearing is *expected*' → '`planned` · …', keeping the surrounding point that the gate is on the 3rd field, not the stage word.",
        "Fix `make-bugfix-request/SKILL.md:130`: `next: root-cause` → `next: diagnose`. Rationale to record in the plan's Decisions: across the other five templates the `next:` field is an imperative ACTION (`scope`, `plan`, `implement`, `commit`), never a stage noun — `root-cause` was the only noun, and it named a stage word that no longer exists. This is RCA hardening item (a), applied at its cheapest point.",
        "Add one authority sentence to each of the four stage-advancing skills' advance-status steps (`scope-feature` :136, `diagnose-bug` :150, `create-implementation-plan` :167, `implement-plan` :254) pointing at the track README's **Status grammar** line as the source of the word — e.g. 'The word comes from the resolved track README's **Status grammar** line (`requests/<track>/README.md`), which is the contract; a token that line does not declare fails `tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares`.' Phase 1's Edit C already carries this for `implement-plan`; add it to the other three.",
        "Do NOT move the grammar lines out of the three track READMEs. `_declared_stage_tokens()` (`tests/test_repo_structure.py:63-71`) reads `**Status grammar:**` from exactly `requests/<track>/README.md`, and `requests/README.md:16` already declares that each track's README is the contract. Relocating the grammar to a shared file would break the parser and contradict the documented ownership — the deduplication is achieved by citation, not by relocation.",
        "Verify the links you write resolve: `tests/test_request_links.py` scans `.claude/skills/` (`:29`) and fails on a dead relative link. Note the fence exemption at `:31` if you need to show an example path."
      ],
      "acceptance": [
        "`grep -rn 'root-cause' .claude/skills/*/SKILL.md` returns only English-prose occurrences (the skill descriptions at `diagnose-bug:5-7` and `make-bugfix-request:5-6`) — no stage tokens and no `next:` value.",
        "`grep -rn '`plan`' .claude/skills/create-implementation-plan/SKILL.md .claude/skills/implement-plan/SKILL.md` returns no occurrence used as a STAGE word (occurrences of the word 'plan' meaning the document or the action are fine and expected).",
        "All four stage-advancing skills' advance-status steps name the track README's Status grammar line as the authority for the token.",
        "`uv run pytest -q` still 82 passed; `uv run ruff check`, `ruff format --check`, `mypy` clean.",
        "`uv run pytest tests/test_request_links.py -q` passes — every relative link added in this phase resolves on disk."
      ],
      "commit_note": "Close the restatement ripple: the non-blockquote stage references stages 3 and 4 use for lookup, and `next: root-cause` → `next: diagnose`. Each advance-status step now cites its track README's Status grammar as the authority instead of only restating it."
    },
    {
      "name": "Phase 3 — Guard the `next:` field against the same drift (RCA hardening (a))",
      "goal": "The repro only inspects the STAGE field of a status blockquote. The `next:` field is unchecked, which is how `next: root-cause` survived. Declare the next-action vocabulary alongside each grammar and assert it, so the field that just drifted cannot drift again.",
      "steps": [
        "GATED — this phase is the RCA's hardening tier ('gated, not assumed'). Confirm with the user before building it; if declined, skip to Phase 4 and record the skip in the implementation report.",
        "Add a `**Next-action vocabulary:**` line immediately under each `**Status grammar:**` line — `requests/feature-requests/README.md:106`, `requests/bugfix-requests/README.md:86`, `requests/calibration-findings/README.md:88`. Feature: `` `scope` → `plan` → `implement` → `commit` ``. Bugfix: `` `diagnose` → `plan` → `implement` → `commit` ``, plus the exit values `` `fix` `` and `` `none` ``. Calibration: mirror the bugfix shape. Keep the exact `**Bold:**` + backticked-token format — the parser in the next step reuses `BACKTICKED` (`tests/test_repo_structure.py:39`).",
        "Add `NEXT_ACTION = re.compile(r\"^>\\s*\\*\\*Status:\\*\\*[^\\n]*next:\\s*(?P<next>[a-z-]+)\", re.MULTILINE)` and a `_declared_next_actions()` helper beside `_declared_stage_tokens()` (`tests/test_repo_structure.py:63-71`), parsing the new line the same way.",
        "Add `test_every_pipeline_skill_writes_a_next_action_some_track_declares()` next to the existing conformance test at `:270`. Same shape: glob `SKILLS_DIR.glob(\"*/SKILL.md\")`, collect the `next:` value from each template blockquote, assert the set difference against the declared union is empty. The regex must tolerate a `<a | b | c>` placeholder (`diagnose-bug:107` writes one) — those start with `<` and simply will not match `[a-z-]+`, which is the intended behaviour: a placeholder is not a claim.",
        "Write the failure message in the house style — say what broke, name the source of truth, and say why it matters (copy the tone of `:291-296`).",
        "Sanity-check the guard actually bites: temporarily set one skill's `next:` to a nonsense word, confirm the new test goes red, then revert it. Do this with an in-memory edit-and-undo, never with `git checkout`/`restore`."
      ],
      "acceptance": [
        "All three track READMEs carry a `**Next-action vocabulary:**` line parseable by the same `BACKTICKED` regex as the grammar line.",
        "`tests/test_repo_structure.py::test_every_pipeline_skill_writes_a_next_action_some_track_declares` exists and passes against the current six skills.",
        "The new guard demonstrably fails when a skill's `next:` is set to an undeclared word (verified by a temporary edit, then reverted).",
        "`uv run pytest -q` passes with the count up by one (83); ruff, ruff format, mypy clean."
      ],
      "commit_note": "Declare each track's next-action vocabulary beside its status grammar and guard it. RCA hardening (a): the `next:` field was the unchecked half of the status blockquote, and it had already drifted."
    },
    {
      "name": "Phase 4 — Check the Index cell against its own track's grammar (RCA hardening (b))",
      "goal": "Invariant A only proves the Index and the artifacts agree with EACH OTHER. A hand-edited Index carrying an invented word passes if every artifact matches it. Assert the Index cell is a word its OWN track declares — note this is per-track, stricter than the union the conformance test uses.",
      "steps": [
        "GATED — hardening tier. Confirm with the user before building.",
        "Refactor `_declared_stage_tokens()` (`tests/test_repo_structure.py:63-71`) into a per-track form (e.g. `_declared_stage_tokens(track: str | None = None)` returning one track's set, or a `dict[str, set[str]]`) and keep the unioned call site at `:280` working. Preserve the existing behaviour exactly — the conformance test must stay union-based, because a skill legitimately serves several tracks.",
        "Add `test_index_stage_cells_are_words_their_own_track_declares()` beside the existing Index guard at `:454`. Reuse its `stage_cell` regex (`:465`) to walk each track README's Index rows, and assert each captured `stage` is in THAT track's declared set. Watch the `\\w+` capture group: it does not match hyphens, so a hypothetical `root-cause` cell would capture as `root` — mention this in the docstring so the next reader is not misled by the failure text.",
        "Skip rows whose Stage cell is empty — `requests/calibration-findings/README.md:94` is a placeholder row (`_(none yet …)_`) with no stage, and the guard must tolerate an empty track rather than assuming calibration has been exercised. This is where RCA Open Question 3 stays honestly `unconfirmed`: the guard covers the track without requiring anyone to have run it.",
        "Confirm the current Index rows pass: feature `_done/H1-escalation-queue` at `implemented` (`requests/feature-requests/README.md:116`) and bugfix `pipeline-status-rollover` at whatever stage the directory currently sits (`requests/bugfix-requests/README.md:98`)."
      ],
      "acceptance": [
        "`tests/test_repo_structure.py::test_index_stage_cells_are_words_their_own_track_declares` exists and passes.",
        "The pre-existing `test_index_stage_cells_match_their_artifact_status_headers` and `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` still pass unchanged — the per-track refactor did not narrow the conformance test to one track.",
        "The guard tolerates the empty calibration Index without erroring or vacuously passing on a populated one.",
        "`uv run pytest -q` green; ruff, ruff format, mypy clean."
      ],
      "commit_note": "Assert every Index Stage cell is a word its own track's grammar declares. RCA hardening (b): invariant A only ever proved the Index and the artifacts agreed with each other, never that either agreed with the contract."
    },
    {
      "name": "Phase 5 — Park the `_done/` decision, then close the item out on its own fixed rules",
      "goal": "Record the one adjacent gap this fix deliberately does NOT close (hardening (c)) as a parked decision rather than a silent choice, then roll the item to its terminal stage — which is the fix dogfooding itself, since doing so correctly is exactly what defects 1 and 3 made impossible.",
      "steps": [
        "Hardening (c) is a DECISION, not a task, so it goes to the queue rather than into the code. `tests/test_request_links.py:41` (`p for p in tree.rglob(\"*.md\") if \"_done\" not in p.parts`) is the skip that made the 1.1 panel's original catch of this defect unreachable — the finding is real and still sits at `requests/feature-requests/_done/1.1-app-shell/reviews/plan-adversarial.md:217` (verified: an `E2-08` finding naming the grammar mismatch directly). The skip is deliberate and documented at `:15-21`; narrowing it is a genuine call with alternatives.",
        "Park it in `ESCALATIONS.md` using the six-field format at `:73-79`, which `tests/test_escalations.py` checks field by field. `Bears on:` must resolve to a roadmap item id, a phase name, or `post-v1` — with H1 already `DONE` (`ROADMAP.md:197`) and no pipeline-hygiene row existing, `post-v1` is the honest moment. `Assumed:` records what was actually done: 'left the skip as-is; the new conformance guard now catches this defect class mechanically, so an unreachable archived finding is no longer the only line of defence — *inferred*.' `Source:` is `tests/test_request_links.py:41`, written as code, not a link. `Status:` is `open`.",
        "Do not resolve any entry — `ESCALATIONS.md:24`: agents park and read, disposition is the user's. Note that `/commit` surfaces parked entries against a row it closes (`.claude/skills/commit/SKILL.md:141`); since this change maps to no roadmap row, expect nothing to be surfaced.",
        "Roll the item to its terminal stage using the rules Phase 1 just wrote — this is the acceptance test for the fix, executed by hand. The bugfix terminal is `fixed` (`requests/bugfix-requests/README.md:86`). Set the Status blockquote of ALL artifacts in the directory — `BUGFIX_REQUEST.md`, `ROOT_CAUSE_ANALYSIS.md`, `IMPLEMENTATION_PLAN.md`, and the `IMPLEMENTATION_REPORT.md` you write — to `fixed`, and set the Index Stage cell at `requests/bugfix-requests/README.md:98` to `fixed`. Not `implemented`.",
        "Archive per `requests/bugfix-requests/README.md:83` and `:91-92`: one move of the directory into `requests/bugfix-requests/_done/pipeline-status-rollover/`, with the Index row staying put and only its link updated to `_done/pipeline-status-rollover/`. Verify afterwards that `test_index_stage_cells_match_their_artifact_status_headers` still resolves the row — it does `track_dir / row[\"link\"]` (`tests/test_repo_structure.py:475`), so a `_done/…/` link resolves fine and every artifact inside is still checked.",
        "Hand off to `/commit`. Do not run `git commit`, `git merge`, or `git commit --amend` under any circumstances; `/commit` stages by path, runs the doc gate, asks, then commits and pushes the branch (`.claude/skills/commit/SKILL.md:216-224`). Opening and merging the PR is the user's."
      ],
      "acceptance": [
        "`ESCALATIONS.md` carries one new open entry with all six fields; `uv run pytest tests/test_escalations.py -q` passes.",
        "All four `*.md` files in the item directory and the bugfix Index cell read `fixed` — the track's own terminal, not `implemented`. This is the direct behavioural proof that defect 3 is fixed.",
        "The Index row link points at `_done/pipeline-status-rollover/` and `uv run pytest tests/test_request_links.py tests/test_repo_structure.py -q` is green after the move.",
        "Full `uv run pytest -q` green, `uv run ruff check` / `ruff format --check` / `uv run mypy` clean, and the branch is pushed by `/commit` — with the PR left for the user to open."
      ],
      "commit_note": "Park the `_done/` link-scan trade-off as an escalation entry, then close pipeline-status-rollover at `fixed` and archive it — rolled by the very rules this fix put in place."
    }
  ],
  "testing": "**The regression test already exists and is committed.** `fb0406e` landed the three repro assertions in `tests/test_repo_structure.py` (`:270-296`, `:299-327`, `:330-353`) together with the RCA. That satisfies both halves of the bugfix track's definition of done (`requests/bugfix-requests/README.md:35-46`) and puts the guard in the home that README's table names for a CI/config-shaped defect (`:57`, \"a structural assertion in `tests/test_repo_structure.py`\"). **Do not rewrite the repro to make it pass** — a repro edited to accommodate the fix is not a repro. The only sanctioned change to those three tests is the per-track refactor of `_declared_stage_tokens()` in Phase 4, and that phase's acceptance explicitly requires the conformance test's union semantics to survive it.\n\n**Measured baseline (run at plan time, not inferred):** `uv run pytest -q` → `3 failed, 79 passed`; `uv run ruff check` → `All checks passed!`; `uv run mypy` → `Success: no issues found in 16 source files`. The three failures are exactly the repro; the other 79 confirm the repro isolates this defect and nothing else. If your first run does not reproduce those numbers, stop — you are on the wrong branch (see the branch note; the repro exists only on `bugfix/pipeline-status-rollover`, unmerged).\n\n**Per-phase gate, run locally before every `/commit`:**\n```\nuv run pytest -q\nuv run ruff check\nuv run ruff format --check\nuv run mypy\n```\nAll four must be clean. CI re-runs the same four on the PR — `.github/workflows/ci.yml:37, :40, :43, :47` — plus the web job and a secret scan, neither of which this change can affect (no `app/` file is touched). A red CI check is stop-and-fix, never a retry loop; `enforce_admins: true` means nobody merges past one anyway.\n\n**Why the phase boundaries fall where they do.** The three repro tests fail against three different edits, but a phase must end GREEN, and the suite is red until *all four* prose fixes land. So Phase 1 is deliberately one atomic unit rather than three tidy ones. Phases 2-5 are each independently green and independently committable.\n\n**Verifying the fix rather than the keyword.** Two of the three tests are satisfiable by inserting a matching phrase without changing the instruction — `ROLLS_A_SIBLING` (`:55`) matches on `Status blockquote|sibling|every artifact`, and `DERIVES_TERMINAL` (`:60`) on `terminal stage word`. The recommended wording in Phase 1 satisfies each test *twice over* (the rollover bullet is a genuine, followable instruction that happens to contain both trigger phrases; the terminal bullet both names the derivation AND lists all three terminal words, so `len(named) > 1` holds independently). Phase 1's last acceptance criterion is stated in exactly those terms because a keyword-only fix would pass the suite and leave the bug in place — which is how this defect got lost the first four times.\n\n**The end-to-end test is Phase 5, executed by hand.** Rolling this item to `fixed` — the bugfix terminal, not `implemented` — across all four artifacts plus the Index, and archiving it into `_done/` with only the link changed, is the fix running against itself. If Phase 5 can be completed by following the newly-edited Step 7 literally and the suite stays green, defects 1 and 3 are demonstrably closed. If it can't, they aren't.\n\n**Negative check worth running once (cheap, high value).** After Phase 1, temporarily revert one edit in memory (e.g. put `plan` back at `create-implementation-plan:176`), confirm the conformance test goes red with a message naming that skill, then restore. Do this by editing and re-editing the file — **never** with `git checkout`, `git restore`, `git stash`, or `git clean`.",
  "risks": [
    "**Keyword-satisfaction instead of a real fix.** `ROOT_CAUSE_ANALYSIS.md` is explicit that this defect was found and lost four times. Two of the three tests match on prose phrases, so a fix that inserts `Status blockquote` and `terminal stage word` without writing a followable instruction goes green and leaves the bug. Mitigation: Phase 1's wording is prescribed verbatim, and its final acceptance criterion is judged on whether an agent could follow the sentence, not on whether the regex matched.",
    "**Editing the repro to make it pass.** The three assertions are the regression guard AND the acceptance contract. Loosening a regex, deleting an assertion, or narrowing `STAGE_ADVANCING_SKILLS` (`tests/test_repo_structure.py:46-51`) would produce a green suite and no fix. The only sanctioned change is Phase 4's per-track refactor, whose acceptance requires the conformance test's union semantics to survive.",
    "**`_advance_status_section` is fence-blind.** It slices to the next `^## ` (`:53`) with no awareness of ```` ``` ```` fences, so in `implement-plan` the window runs :254→:275 and *includes* the template blockquote at :268 — while in `create-implementation-plan` the window ends at :183 because `## 1. Onboarding` at :184 sits inside the fence. An edit placed one line outside its window silently does nothing. Mitigation: the exact windows are stated in every relevant step, and the assertion prints the slice it actually took.",
    "**Replacing `implement-plan`'s template token with a `<placeholder>` quietly drops it from test-1 coverage.** `SKILL_STATUS_TEMPLATE` (`:41`) is anchored on `[a-z-]+`; a leading `<` means no match, no offender, no coverage. Phase 1 Edit C2 keeps a real declared token plus a prose note precisely to avoid trading one silent gap for another.",
    "**Relocating the grammar to a 'shared home' would break the parser.** `_declared_stage_tokens()` (`:63-71`) reads `**Status grammar:**` from exactly the three track READMEs, and `requests/README.md:16` names each track README as the contract. The RCA left this design call open; the plan closes it as guard-plus-citation. Moving the grammar lines is the one shape that reds the very guard being installed.",
    "**Wrong branch = phantom baseline.** The repro and the RCA live only in `fb0406e` on `bugfix/pipeline-status-rollover`, unmerged (`git diff HEAD origin/main --stat` shows both as this branch's additions). An implementer who branches off `main` sees 79 passed / 0 failed and concludes there is nothing to fix. Phase 1 step 1 checks the branch name and the exact 3-failed/79-passed counts before any edit.",
    "**The `_done/` move can strand a link.** Archiving the directory takes it out of `tests/test_request_links.py`'s scan (`:41`) but the Index row's link must be updated in the same commit, and `test_index_stage_cells_match_their_artifact_status_headers` still resolves and checks artifacts under `_done/` (`:475`) — so every file in the moved directory must read `fixed`, not just the ones you remember.",
    "**Calibration remains unconfirmed and must stay that way.** RCA Open Question 3 records that nobody has run that track and its Index (`requests/calibration-findings/README.md:94`) is empty. No phase may assume calibration routes through the shared back half; Phase 4 explicitly tolerates an empty Index rather than treating the absence as evidence either way.",
    "**Convention violations are the cheapest way to fail this change.** Every phase ends at `/commit` — never an ad-hoc `git commit`, never `--amend`, never a push to `main`, never a force-push. Any subagent spawned for grounding gets **read-only git** and must not `checkout`/`reset`/`restore`/`clean`/`stash`. `/commit` pushes the feature branch; opening and merging the PR stays the user's.",
    "**Scope creep into the RCA's decided territory.** The verdict, the cause, and the four instances are settled. `diagnose-bug`'s non-blockquote exit words (`closed-works-as-intended`, `cannot-reproduce`, `redirected-to-feature` at `:99-102`) are a real adjacent gap the RCA did not enumerate — it is raised as an open question below, not folded into a phase, because deciding it here would be re-opening stage 2."
  ],
  "files_to_touch": [
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\create-implementation-plan\\SKILL.md",
      "change": "Phase 1: `plan` → `planned` at :171-172 (Index instruction), :173 (artifact stage line), :176 (template blockquote); insert the sibling-rollover bullet into the Step 5 list between :172 and :173, inside the :167→:183 window. Phase 2: `root-cause` → `diagnosed` at :56 and :65; add the 'authority is the track README's Status grammar line' sentence to Step 5."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\implement-plan\\SKILL.md",
      "change": "Phase 1: rewrite Step 7 bullets :257-260 so the Index word is the **track's terminal stage word** naming all three (`implemented`/`fixed`/`retuned`), add the sibling-rollover bullet, and change :260 to the derived word; add one prose note immediately before the ```markdown fence at :267 while KEEPING the real token at :268. Phase 2: Step 1's `plan` → `planned` in the Index-lookup sentence and the disposition-gate sentence."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\diagnose-bug\\SKILL.md",
      "change": "Phase 1: `root-cause` → `diagnosed` at :107 (template blockquote), :97 (verdict prose), and :154 (Step 5 Index instruction — keep the 'or the terminal stage word' parenthetical, it is the precedent test 3 was written around). Leave :5-7 alone: 'root-cause analysis' there is English, not a token. Phase 2: add the authority sentence to Step 5."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\make-bugfix-request\\SKILL.md",
      "change": "Phase 2: :130, `next: root-cause` → `next: diagnose` — the `next:` field is an imperative action everywhere else (`scope`/`plan`/`implement`/`commit`), and `root-cause` was both a noun and a retired stage word. RCA hardening (a)."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\.claude\\skills\\scope-feature\\SKILL.md",
      "change": "Phase 2 ONLY, and only the added authority sentence at Step 5 (:136). Its stage word and rollover pattern (:139, :149) are already correct — this file is the template the others copy. Do not otherwise edit it."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\tests\\test_repo_structure.py",
      "change": "Phase 3: add `NEXT_ACTION` regex + `_declared_next_actions()` beside `_declared_stage_tokens()` (:63-71) and a `test_every_pipeline_skill_writes_a_next_action_some_track_declares` beside :270. Phase 4: refactor `_declared_stage_tokens()` to a per-track form (union call site at :280 preserved) and add `test_index_stage_cells_are_words_their_own_track_declares` beside :454. **Phases 1-2 must not touch this file at all** — it is the repro."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\README.md",
      "change": "Phase 3 (gated): add a `**Next-action vocabulary:**` line under the grammar at :86. Phase 5: set the `pipeline-status-rollover` Index Stage cell (:98) to `fixed` and repoint its link to `_done/pipeline-status-rollover/`. The grammar line at :86 itself is never edited."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\feature-requests\\README.md",
      "change": "Phase 3 (gated) only: add a `**Next-action vocabulary:**` line under the grammar at :106. The grammar line itself is never edited — `_declared_stage_tokens()` parses it from exactly there."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\calibration-findings\\README.md",
      "change": "Phase 3 (gated) only: add a `**Next-action vocabulary:**` line under the grammar at :88. Nothing else — the track is unexercised and its Index (:94) is an empty placeholder; do not populate or infer anything from it."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\ESCALATIONS.md",
      "change": "Phase 5: one new `open` entry parking the `_done/` link-scan trade-off (RCA hardening (c)), six fields per the format at :73-79, `Bears on: post-v1`, `Source: tests/test_request_links.py:41`. Never resolve an entry (:24)."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\BUGFIX_REQUEST.md",
      "change": "Status blockquote only. Rolls to `planned` when the plan artifact is written (stage 3), then to `fixed` in Phase 5. Never edit its body — it is a decided upstream artifact."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\ROOT_CAUSE_ANALYSIS.md",
      "change": "Status blockquote only (currently `diagnosed`, already grammar-correct). Rolls to `planned`, then to `fixed` in Phase 5. Its verdict, evidence, and fix posture are decided — consume, never re-open."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\IMPLEMENTATION_PLAN.md",
      "change": "Written by stage 3 (this artifact). Opens at `planned · created <today> · decided · next: implement` — `planned`, not `plan`, since the plan must not inject the defect it fixes. Rolls to `fixed` in Phase 5."
    },
    {
      "path": "D:\\projects\\nba2k-rpg\\requests\\bugfix-requests\\pipeline-status-rollover\\IMPLEMENTATION_REPORT.md",
      "change": "Written by stage 4 in Phase 5. Opens at `fixed` — the bugfix track's terminal per `requests/bugfix-requests/README.md:86`, NOT `implemented`. Writing this file correctly is itself the acceptance evidence for defect 3."
    }
  ],
  "code_references": [
    {
      "ref": "tests/test_repo_structure.py:270-296 — test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares",
      "claim": "RED today. Reports `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}` against declared vocabulary `['diagnosed', 'fixed', 'implemented', 'intake', 'planned', 'retuned', 'scoped']`. Catches defects 2 and 4. Verified by running `uv run pytest tests/test_repo_structure.py -q`."
    },
    {
      "ref": "tests/test_repo_structure.py:299-327 — test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory",
      "claim": "RED today, reporting `['create-implementation-plan', 'implement-plan']`. Catches defect 1, the blocking one."
    },
    {
      "ref": "tests/test_repo_structure.py:330-353 — test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token",
      "claim": "RED today: 'implement-plan's advance-status section hardcodes ['implemented'] and serves all three tracks, whose terminals are ['fixed', 'implemented', 'retuned']'. Catches defect 3."
    },
    {
      "ref": "tests/test_repo_structure.py:74-80 — _advance_status_section",
      "claim": "Slices from the first case-insensitive `advance status` to the next `^## `. FENCE-BLIND: it includes the fenced template blockquote at implement-plan:268 in the section it returns. Verified from the assertion's own printed section text."
    },
    {
      "ref": "tests/test_repo_structure.py:41 — SKILL_STATUS_TEMPLATE",
      "claim": "`^>\\s*\\*\\*Status:\\*\\*\\s*(?P<stage>[a-z-]+)` — anchored on a lowercase word, so a `<placeholder>` token is invisible to the conformance test. This is why Phase 1 Edit C2 keeps a real token at implement-plan:268."
    },
    {
      "ref": "tests/test_repo_structure.py:55 and :60 — ROLLS_A_SIBLING, DERIVES_TERMINAL",
      "claim": "`Status blockquote|sibling|every artifact` and `terminal (?:stage word|token)|track's terminal`. These are the exact phrases the Phase 1 wording must contain — and the reason a keyword-only fix would pass while leaving the bug in place."
    },
    {
      "ref": "tests/test_repo_structure.py:63-71 — _declared_stage_tokens",
      "claim": "Parses `**Status grammar:**` from `requests/<track>/README.md` for all three tracks and unions the backticked words. This is why the grammar lines must NOT be relocated to a shared file."
    },
    {
      "ref": "tests/test_repo_structure.py:454-487 — test_index_stage_cells_match_their_artifact_status_headers",
      "claim": "Invariant A, green and unchanged by this fix. Its per-artifact loop at :479 is what makes a stale sibling load-bearing; :475 resolves `track_dir / row[\"link\"]`, so a `_done/…/` link still gets checked after Phase 5's archive move."
    },
    {
      "ref": ".claude/skills/scope-feature/SKILL.md:136-149",
      "claim": "The correct pattern the fix copies: :136 opens the advance-status section, :139 rolls the sibling ('Set the request's Status blockquote to `scoped`'), :140-143 sets the Index cell, :144 opens the new artifact, :149 is the grammar-legal template blockquote."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:167-178",
      "claim": "Defects 1 and 2 together. :167 opens the advance-status section (window ends at :183); :171-172 and :173 write `plan`; :176 is the template blockquote writing `plan`; :177-178 cites 'this README status grammar' as authority in the same breath as violating it. No bullet mentions the siblings."
    },
    {
      "ref": ".claude/skills/create-implementation-plan/SKILL.md:49-51, :56, :65",
      "claim": "Track resolution (`<track>` from the upstream path, `<work-dir>`, the track README) already works and is untouched. But :56 and :65 restate `root-cause` as the stage to look for — prose no test sees, invalidated by the Phase 1 rename, fixed in Phase 2."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md:251-260, :268",
      "claim": "Defects 1 and 3. Step 7's advance-status window is :254→:275 (next `^## ` is `## 1. Acceptance ledger` at :276). :258-259 writes `implemented` unconditionally, :260 repeats it, :268 is the template blockquote. No bullet mentions the siblings."
    },
    {
      "ref": ".claude/skills/implement-plan/SKILL.md Step 1 (:56-105)",
      "claim": "The track is ALREADY resolved from the artifact path here, which is RCA Open Question 2's answer — the terminal word can follow from the same resolution rather than being a literal. This step also restates `plan` as the stage to look for; Phase 2 fixes that to `planned`."
    },
    {
      "ref": ".claude/skills/diagnose-bug/SKILL.md:107",
      "claim": "Defect 4, found by the diagnosis running on itself: the template blockquote writes `root-cause`, which no track grammar declares. :97 restates it in prose and :154 in the Step 5 Index instruction."
    },
    {
      "ref": ".claude/skills/diagnose-bug/SKILL.md:154",
      "claim": "'…to `root-cause` (or the terminal stage word)' — the parenthetical is the in-repo precedent DERIVES_TERMINAL was written around, and the shape implement-plan should copy. Keep it when fixing the token."
    },
    {
      "ref": ".claude/skills/make-bugfix-request/SKILL.md:130",
      "claim": "`> **Status:** intake · created <YYYY-MM-DD> · open · next: root-cause` — the stage word is correct; the `next:` value is a noun naming a retired stage. RCA hardening (a); Phase 2 changes it to `next: diagnose`."
    },
    {
      "ref": "requests/feature-requests/README.md:106 / requests/bugfix-requests/README.md:86 / requests/calibration-findings/README.md:88",
      "claim": "The three declared grammars, verified verbatim: `intake → scoped → planned → implemented`, `intake → diagnosed → planned → fixed`, `intake → diagnosed → planned → retuned`. The source of truth the fix makes authoritative rather than advisory."
    },
    {
      "ref": "requests/README.md:16",
      "claim": "'Each track's README is the contract — layout, status grammar, the live Index, and the `_done/` archive convention.' The documented ownership that settles the RCA's shared-prose-home question in favour of guard-plus-citation."
    },
    {
      "ref": "requests/bugfix-requests/README.md:35-46 and :50-57",
      "claim": "Definition of done — 'a red reproduction goes green, and a regression test is left behind' — and the table naming `tests/test_repo_structure.py` as the right home for a CI/config-shaped defect's guard. Both already satisfied by the committed repro."
    },
    {
      "ref": "requests/bugfix-requests/README.md:83, :91-92, :98",
      "claim": "The `_done/` archive convention Phase 5 executes: one move at the terminal stage, Index row stays with its link updated. :98 is the live `pipeline-status-rollover` row, currently `diagnosed`."
    },
    {
      "ref": "tests/test_request_links.py:41",
      "claim": "`p for p in tree.rglob(\"*.md\") if \"_done\" not in p.parts` — the deliberate skip that made the 1.1 panel's catch unreachable. RCA hardening (c). NOTE: the RCA cites `:36`, which is the `_scanned_files` def line; the skip itself is at :41. Phase 5 parks this as a decision rather than changing it."
    },
    {
      "ref": "requests/feature-requests/_done/1.1-app-shell/reviews/plan-adversarial.md:217",
      "claim": "Verified present: an `E2-08` high-confidence 'convention' finding whose location line names the grammar mismatch against `requests/feature-requests/README.md` directly. Found, recorded, archived, and lost — the measured cost the RCA records."
    },
    {
      "ref": ".claude/skills/commit/SKILL.md:110-149, :216-238",
      "claim": "Step 4 keeps ROADMAP statuses in step and :146 gives the explicit 'no roadmap row' path this bugfix takes; :141 surfaces parked escalation entries; :216-224 pushes the feature branch; :229-234 never pushes `main` and never force-pushes; :234 leaves opening the PR to the user."
    },
    {
      "ref": "ROADMAP.md:197",
      "claim": "`H1 | escalation-queue | … | Blocks 1.3 | DONE` — H1 has landed, so ESCALATIONS.md is live and usable, and there is no open harness row this bug maps to."
    },
    {
      "ref": "ESCALATIONS.md:73-79",
      "claim": "The six required entry fields (id+title, `Bears on:` which must resolve to a roadmap id / phase / `post-v1` with no backticks, `Parked:`, `Assumed:` with an epistemic label, `Source:` as code, `Status: open|resolved`), each checked by tests/test_escalations.py."
    },
    {
      "ref": ".github/workflows/ci.yml:37, :40, :43, :47",
      "claim": "CI's Python job runs `ruff check`, `ruff format --check`, `mypy`, and `pytest` — the same four gates each phase must pass locally before `/commit`."
    },
    {
      "ref": "git: branch `bugfix/pipeline-status-rollover`, commit fb0406e",
      "claim": "The repro and the RCA are on this branch and pushed to origin but UNMERGED — `git diff HEAD origin/main --stat` shows `ROOT_CAUSE_ANALYSIS.md` and `tests/test_repo_structure.py` as this branch's additions. Do not create a new branch; branching off main loses the red repro."
    }
  ],
  "open_questions": [
    "**`/diagnose-bug`'s non-terminal exit words are undeclared, and the RCA did not enumerate them.** `diagnose-bug/SKILL.md:99-102` instructs `closed-works-as-intended`, `cannot-reproduce`, and `redirected-to-feature` as Status stage words for the three non-confirmed verdicts. None appears in the bugfix grammar at `requests/bugfix-requests/README.md:86`, and none is caught by the conformance test — they are written as inline prose (`` `cannot-reproduce` · … ``) rather than in the `> **Status:**` blockquote form `SKILL_STATUS_TEMPLATE` (`tests/test_repo_structure.py:41`) matches. This is defect 2's exact shape in a place nobody has looked. **Recommendation:** declare them on the bugfix grammar line as terminal exits (e.g. `… → `fixed` · exits: `cannot-reproduce` | `closed-works-as-intended` | `redirected-to-feature``) and let `_declared_stage_tokens()` pick them up unchanged. Deliberately NOT folded into a phase — enumerating a fifth instance is adjacent to re-opening a decided RCA, so it needs the user's call: fix it here, or open a follow-up BUGFIX_REQUEST.",
    "**Are hardening phases 3 and 4 in scope for this fix, or a separate item?** The RCA states the hardening tier is 'gated, not assumed'. Phases 3 and 4 are each ~30 lines of test plus three one-line README additions, and both close gaps this exact defect walked through. But they are strictly beyond 'the red repro goes green'. Recommendation: run both — they are cheap, and the measured cost of this bug (four independent discoveries, none of which fixed it) is an argument for guarding rather than observing. The user decides at the Phase 3 gate.",
    "**Is `post-v1` the right `Bears on:` for the `_done/` escalation entry?** `ESCALATIONS.md:75` requires a roadmap item id, a phase name, or `post-v1`, with no `unscheduled` hatch. H1 is `DONE` (`ROADMAP.md:197`) and no row covers pipeline-skill hygiene, so `post-v1` is the only honest resolvable moment — but an entry parked at `post-v1` is also the one least likely to be reopened, which is the failure mode the queue exists to prevent. If the user would rather bind it to a nearer moment, `H2` (`domain-engineer`, `NOT STARTED`) is the next harness row that will re-read the skill corpus.",
    "**Should `next:` values be treated as a vocabulary at all?** Phase 3 assumes yes and declares one. The counter-argument: `requests/feature-requests/README.md:104` types the field loosely as `next: <stage or \"implement\">`, i.e. it was never meant to be closed. If the user prefers to leave the field free-form, Phase 2's `next: root-cause` → `next: diagnose` edit still stands on consistency grounds alone and Phase 3 drops entirely."
  ]
}
```
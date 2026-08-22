# Planning Panel — Adversarial & Meta-Audit Findings

> Verbatim panel output, with exactly two mechanical transformations: machine-absolute
> path prefixes stripped (these files are tracked and this repo is public), and markdown
> link syntax neutralized so repo-relative citations do not read as broken links from
> this directory. No other content altered.


## Convergence map

- - **theme:** The scope mis-cites the third recovered stray: `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` is the `.gitignore:63` blanket-`build/` shadowing at moment **2.1**, not a 'client-side router seam' at 1.10.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** All three opened the cited lines and got the same text; I re-read them plus the duplicate at `PROJECT_SCOPE.md:442-444` and confirmed. The failure mode is nasty because the wrong version STILL PASSES the guard (1.10 is a real id), so CI cannot catch it — only reading can. It also explains the confusion: `PROJECT_SCOPE.md:319` does mention 1.10's router, and finding F-02 already ruled that line a shipped fold rather than a stray.
- - **theme:** AC 18 must be a non-recursive `REPO_ROOT.glob("*.md")`, never `REPO_ROOT` appended to `SCANNED_TREES`.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** Three independent readings of `_scanned_files` (`tests/test_request_links.py:31-37`) reached the same conclusion: the loop rglobs each tree, so the literal reading of the criterion would sweep node_modules/, .venv/, var/, and the deliberately-exempt `_done/` archive whose links describe the repo as it was. A criterion whose literal reading is a trap is exactly what a cold implementer needs warned about.
- - **theme:** The fenced worked example must be stripped from the document-level parse and parsed separately, with a reserved id, or AC 11 collides with AC 8 and AC 9.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** Three planners independently derived the same constraint conflict from criteria written in different sections of the scope, and independently proposed the same resolution (fence-strip + separate template parse + `E-000`). That is a genuine structural coupling, not a style preference — and the likely 'fix' when hit blind is to weaken AC 11, which deletes the only mechanical proof goal 1 has.
- - **theme:** The parser discriminator is an id-pattern match, and it measures out at exactly 38 ids with 57 non-item leading cells rejected.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** All three prototyped the regex against the real `ROADMAP.md` and got identical numbers; I re-ran it a fourth time and got 38/57 again with all four AC-2 probes present. AC 3's correction of findings F-27/F-06 is therefore verified rather than inherited, and AC 2's `>= 30` floor is confirmed to have eight rows of headroom.
- - **theme:** `test_index_stage_cells_match_their_artifact_status_headers` (`tests/test_repo_structure.py:286-319`) is a latent red the moment this plan's own artifact lands, and the stage-3 skill does not warn about it.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** Three planners each traced the test to the same consequence — the Index cell and every sibling artifact header must move in one commit, twice (at `planned` and at `implemented`) — and each found the same precedent in `_done/1.1-app-shell/`. It is the single most likely spurious red in the whole build, and its failure message points at the Index rather than at the token, so it reads as a phantom bug.
- - **theme:** The CLAUDE.md budget is +1 line total against a measured 221, and must be measured with `(Get-Content).Count`, not `Measure-Object -Line`.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** Three independent measurements returned 221, matching AC 23's stated baseline exactly, and all three named the same over-run trap (adding a prose bullet under 'Important locations' as well as the map line). The measurement-command divergence is itself a recorded defect (scope risk 15) that would silently under-report and let the criterion pass while red.
- - **theme:** Inertness is the feature-killing risk, and the three read seams are the whole mitigation — nothing writes entries automatically.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** This reproduces the scoping panel's own 3/3 convergence one stage later, from three different lenses, all anchored on the same named precedent (`ops/README.md:30-37`, branch-protection.json inert until re-applied). It is why Phase 4 must not be trimmed under time pressure, and why the substring tests must be proven to bite rather than merely written.
- - **theme:** `tests/test_no_leaks.py` scans `git ls-files`, so AC 22's coverage of the new document is vacuous until `/commit` stages it.
  - **planners:** - sequencing
    - domain-convention
  - **why_high_signal:** Two planners traced the same ordering trap to the same lines (`:61-74`) and reached the same remedy — a manual sweep before the commit, a re-run after — without proposing the obvious wrong fix (`git add`), which the agents-commit-only-through-/commit rule forbids. On a public repo where entries record real assumptions, a vacuously-green leak guard is the worst kind of green.
- - **theme:** AC 24's observable signal is not automatically satisfied — none of the seven seeds names moment `1.3`.
  - **planners:** - code-grounded
    - sequencing
  - **why_high_signal:** Two planners independently checked the seed moments (`Phase 3`, `Phase 3`, `H2`, `1.8`, `1.8`, `2.1`, `post-v1`) against scope risk 2's claim that 'the seven seeds make this true on day one' and found the claim does not hold for 1.3 specifically. Both refused to fabricate an entry to make the criterion green. That is the right instinct and it is a user call, not a planner call.
- - **theme:** Moment comparison must be casefolded, because the heading reads `Post-v1` while AC 5's fixture names `post-v1`.
  - **planners:** - code-grounded
    - domain-convention
  - **why_high_signal:** Two planners caught the same one-character trap from the same measured heading list, and both noted the same symptom: only the green fixture fails, which reads as a fixture bug rather than a parser bug and costs disproportionate debugging time.
- - **theme:** Two of the scope's Affected-Area line citations are off by one — 'Why H1 exists' is :200-204 and 'Parked, not scheduled' is :217-222.
  - **planners:** - code-grounded
    - sequencing
    - domain-convention
  - **why_high_signal:** Three independent re-verifications produced the same corrections, and one noted that the scope's own Problem section (line 51) already cites :217-222 correctly while its pointer section (line 316) does not. A cold implementer trusts line numbers literally, so an off-by-one on the exact paragraph being edited is worth correcting explicitly rather than silently.

---

## Reviewer summaries


### Reviewer 1

- **reviewer:** code-grounded
- **kind:** adversary
- **summary:** Code-grounded verification of every reference the merged plan cites. I read or grepped all of them. VERDICT: the plan's factual grounding is unusually strong — I could not find a single fabricated file, function, or line number. Every measurement it claims re-measured correctly on my run: the roadmap discriminator yields exactly 38 unique ids with 57 non-item leading cells rejected and all four AC-2 probes (`0.1`, `1.3`, `H2`, `4.6`) present; `(Get-Content CLAUDE.md).Count` == 221; `uv run pytest -q` == 55 passed across 8 modules; `_dead_links()` returns `[]` for all five root docs; `datasets/`, `careers/`, `rulesets/`, `lib/`, `build/`, `ESCALATIONS.md`, and `docs/data-sources.md` are all absent and `src/rpg_core/` holds only `__init__.py`. Every function name it claims to reuse exists with the claimed signature: `web_imports_under(root)` at test_layering.py:38, `violation_message` at :70, `_scanned_files()` at test_request_links.py:31 (rglob-per-tree, confirming the AC-18 trap is real), `_dead_links` at :40, `_read` at test_repo_structure.py:256, `test_core_documents_exist` at :243 with the false "three documents" docstring over a five-name tuple, `test_index_stage_cells_match_their_artifact_status_headers` at :286 with a non-recursive `item_dir.glob("*.md")`, `_tracked_text_files()` reading `git ls-files` at test_no_leaks.py:61. The plan's two corrections to the scope's pointers are both correct: `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` really is the `.gitignore:63` blanket-`build/` item at moment 2.1 (and `.gitignore:63` really is `build/`), not a router seam at 1.10; and `requests/feature-requests/README.md:106` really does say `planned`, not `plan`. What I DID find are executable defects — one of them fatal on the very first `/commit`, plus three vacuous-assertion traps of exactly the class AC 4 was written to prevent, and one API misuse of a regex the plan tells the implementer to copy. Ten findings below, all grounded in commands I actually ran.

### Reviewer 2

- **reviewer:** executability
- **kind:** adversary
- **summary:** ADVERSARY 2 — EXECUTABILITY & SEQUENCING. I read the decided scope in full, then verified the plan's load-bearing claims against the real tree rather than trusting them. The plan's *measurements* hold up: `(Get-Content CLAUDE.md).Count` = 221; the id discriminator yields exactly 38 unique ids (`0.1`…`4.6`, `H1`, `H2`) with `1.10` included; `^###\s+(Phase \d+|Post-v1)` yields exactly six names (`### Post-v1` is at ROADMAP.md:277, capitalized, so the casefold warning is real); `_dead_links()` returns `[]` for all five root docs; `uv run pytest -q` = 55 passed on `phase1/escalation-queue` with a clean tree. Its two pointer corrections are also correct and important — `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` really is the `.gitignore:63` blanket-`build/` item at moment 2.1 (duplicated at `PROJECT_SCOPE.md:442-444`), not a router seam at 1.10; and `requests/feature-requests/README.md:106` really does say `planned`, not `plan`. Phase ORDER is sound: no phase depends on later work (Phase 2's AC 6/AC 13 assertions need Phase 1's file and roadmap edit; Phase 3's link-checker widening needs Phase 1's file to exist; Phase 4's seam tests need Phase 2's module). Conventions are baked in well — `/commit`-only, read-only git, `/commit` owns ROADMAP statuses, the N/A-by-probe treatment of resolve-by-name / ADR 0003 / 0004 / 0008 is honest rather than omitted. Where it fails is at the seams the plan itself could not see: (1) it asserts a GREEN Phase-0 baseline that is already RED, because `.claude/skills/create-implementation-plan/SKILL.md:170-173` flips the Index cell when the plan artifact lands while `FEATURE_REQUEST.md`/`PROJECT_SCOPE.md` stay `scoped`, and `tests/test_repo_structure.py:286-319` compares all three — and the plan then tells the agent "any red here is pre-existing"; (2) the plan document itself carries `…` absolute paths in `files_to_touch`, which `tests/test_no_leaks.py:26` will fail the build on the moment `/commit` stages it (zero such paths exist under `requests/` today); (3) several acceptance criteria are un-anchored — "prove the guard bites" never says whether that is a committed test or a manual one-off, and `len(parse_entries(...)) == 7` reintroduces exactly the exact-count brittleness the plan rejects for AC 2. Eighteen findings below, each grounded in a file I opened.

### Reviewer 3

- **reviewer:** meta-audit
- **kind:** meta_audit
- **summary:** META-AUDIT OF THE MERGE (not the repo). I independently re-ran the merge's headline measurements before judging convergence: `uv run pytest -q` = 55 passed on `phase1/escalation-queue` with a clean tree; the id discriminator over the real ROADMAP.md accepts exactly 38 leading cells and rejects exactly 57; the phase-heading regex returns 6 headings (lines 144/163/224/246/261/277); `(Get-Content CLAUDE.md).Count` = 221; `_dead_links()` returns `[]` for all five root documents; `.gitignore:63` is `build/`; and `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` is the gitignore/builder item at moment 2.1, not a router seam at 1.10. Every CI (ci.yml:3-7, 19, 36-47), pyproject (54, 58-75, 82, 84, 88, 93), skill (commit:109-144, make-feature-request:74-95, diagnose-bug:132-142 and 161-162) and test_layering citation in the merged plan checks out verbatim. The merge is largely faithful and its 3/3 convergence themes are real, not manufactured.

SCOPE-CREEP: essentially clean. No deferred item (skills that WRITE entries, the [OPEN-N] mirror guard, ADR 0011) and no dropped item (ops/escalations.py, `Supersedes:`, resolved-entry archive, `Surfaced by:`, the /update-docs drift check) was smuggled back in; the plan names all eight and forbids them. The [G]-tagged ACs 14-16 were already promoted to core scope items 10-12 by Decisions 1/3/5, so Phase 4 is in-scope rather than a silent promotion. The only additions beyond the tiered scope are process rigor (extra tmp_path "prove it bites" procedures elevated to blocking acceptance, plus an API-shaping refactor constraint) and DC's stage-4 report + `_done/` archive move, adopted 1-of-3 with no dissent recorded.

COMPLETENESS: one material drop. All 24 ACs map to phases and all three planners' distinctive code references survive — except that the merge kept SEQ's *risk* about the Index/status latent red while dropping SEQ's *remedial step*, leaving the `planned` rollover owned by no phase and Phase 0's "all four gates exit 0" acceptance unachievable (F1). Two scope risks (11, format designed from retrospective examples; 16, permanent maintenance) were dropped by all three planners and not recovered. One planner-raised regex tolerance (`[em-dash or hyphen]`) was silently narrowed to em-dash-only, opening a per-entry silent-skip hole (F2). Duplication is the other side of the coin: the third-stray correction is restated about ten times across summary/onboarding/phases/risks/decisions/convergence_map/code_references, and the AC-18 rglob trap about seven.

COST-UNREALISM: the merge's "cheap"/"reuse" claims hold up under measurement — AC 18 really does cost zero cleanup, the 38/57 discriminator really works, the FENCED_BLOCK reuse really is a one-line copy. The unrealism is in framing and load distribution: the summary calls this "pure process/docs work" while Phase 2 is a ~19-step, six-function, ten-regex, thirteen-assertion module under mypy strict — the exact split SEQ separated into two phases and the merge collapsed into one.

---

## Adversary findings (code-grounded + executability)


### F-01

- **id:** F-01
- **title:** The plan artifact's own absolute Windows paths will fail test_no_leaks.py on the first /commit
- **severity:** blocker
- **confidence:** high
- **category:** correctness
- **location:** tests/test_no_leaks.py:26
- **problem:** Every path in the draft's `onboarding.files_to_read[].path` and `files_to_touch[].path` is written as an absolute drive-letter path (`ESCALATIONS.md`, `tests\test_escalations.py`, and 15 more). `IMPLEMENTATION_PLAN.md` is a tracked `.md`, `.md` is in `TEXT_SUFFIXES` (tests/test_no_leaks.py:41-58), and `_tracked_text_files()` (:61-74) scans everything in `git ls-files`. I ran the actual `WINDOWS_PATH` regex from :26 against the plan's own strings and it matches: `p.findall(r'see ESCALATIONS.md ...')` returns `['ESCALATIONS.md and D']`. So the moment `/commit` stages the plan, `test_no_leaks.py::test_no_windows_absolute_paths` goes RED — before Phase 0 has even run its baseline. This is also a direct violation of CLAUDE.md's public-repo rule ('No machine-specific absolute paths ... in tracked files'), which the plan's own `conventions` list quotes.
- **proposed_fix:** Write every path in the rendered IMPLEMENTATION_PLAN.md repo-relative (`ESCALATIONS.md`, `tests/test_escalations.py`, `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md`). The draft's `code_references` block already uses repo-relative form correctly — apply the same convention to `files_to_read` and `files_to_touch`. Add an explicit line to Phase 0 or the conventions list: 'this plan document is itself scanned by tests/test_no_leaks.py once staged — no drive-letter paths anywhere in it.'
- **reviewer:** code-grounded

### F-02

- **id:** F-02
- **title:** Phase 0's '55 passed on a clean tree' baseline is unreachable as sequenced — the plan's own landing turns test_index_stage_cells red
- **severity:** major
- **confidence:** high
- **category:** sequencing
- **location:** tests/test_repo_structure.py:286
- **problem:** `test_index_stage_cells_match_their_artifact_status_headers` matches the Index row with `^\|\s*\[(?P<slug>[^\]]+)\]\((?P<link>[^)]+)\)\s*\|\s*(?P<stage>\w+)` and compares that word against `^>\s*\*\*Status:\*\*\s*(?P<stage>\w+)` for EVERY `*.md` in the item dir. Today the Index cell (requests/feature-requests/README.md:116), FEATURE_REQUEST.md:1, and PROJECT_SCOPE.md:1 all read `scoped` — green, and I measured 55 passed. The instant `IMPLEMENTATION_PLAN.md` lands opening `> **Status:** planned`, three files disagree and the suite is red. Phase 0's first two acceptance bullets ('git status --short is empty', 'uv run pytest -q reports 55 passed') therefore describe a state that cannot exist once the plan is in the tree. The plan flags the invariant in `risks` and lists the roll in `files_to_touch`, but never sequences it as a step, so a cold implementer starting at Phase 0 sees a red baseline and concludes something is broken.
- **proposed_fix:** Add an explicit pre-Phase-0 step (or a Phase 0 step 0): 'The commit that lands this plan must roll FEATURE_REQUEST.md:1, PROJECT_SCOPE.md:1, IMPLEMENTATION_PLAN.md:1 AND requests/feature-requests/README.md:116 to `planned` together — four files, one /commit. The 55-passed baseline is measured AFTER that commit, not before it.' Precedent to cite: all four `_done/1.1-app-shell/*.md` read `implemented` against an `implemented` Index cell (verified).
- **reviewer:** code-grounded

### F-03

- **id:** F-03
- **title:** AC 10's register-boundary guard is vacuous twice over — 'DESIGN.md' is a substring of 'GAME_DESIGN.md', and 'Escalation' is a substring of the queue's own prose
- **severity:** major
- **confidence:** high
- **category:** test-vacuity
- **location:** requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md:148
- **problem:** The Phase 2 step for AC 10 prescribes: 'assert the queue body contains `GAME_DESIGN.md`, `DESIGN.md`, `Stage plan`, and `Escalation`.' Two of those four prove nothing. (a) `"DESIGN.md" in body` is satisfied by the `GAME_DESIGN.md` mention alone — plain substring containment — so the DESIGN.md §2/§4 register rows can be deleted entirely and the assertion still passes. (b) `"Escalation"` is satisfied by the queue's own title/prose: the plan itself mandates a name-disambiguation line saying "'escalation' now means two things in this repo", and the document is named ESCALATIONS.md. So the `/diagnose-bug` register row can vanish with the guard still green. The scope wrote AC 10 to prove the boundary header names all five competing registers; as prescribed it proves at most two of them. This is the same failure class AC 4 exists for, applied to the criterion that guards the load-bearing deliverable.
- **proposed_fix:** Assert on anchors that cannot be produced by anything else in the document: `"GAME_DESIGN.md"`, `"DESIGN.md §2"`, `"DESIGN.md §4"`, `"Stage plan"`, and `"diagnose-bug"` (the skill directory name — I verified `ESCALATIONS` appears in none of the three skill files and `diagnose-bug` appears nowhere in the current root docs, so both are clean anchors). Scope the check to the header region above `## Open`, and add a comment naming the substring-shadowing trap so the next agent does not 'simplify' it back.
- **reviewer:** code-grounded

### F-04

- **id:** F-04
- **title:** AC 3's heading-anchor slices have no non-vacuity guard, and the anchors contain em dashes
- **severity:** major
- **confidence:** high
- **category:** test-vacuity
- **location:** ROADMAP.md:21
- **problem:** The plan (Phase 2 step for AC 3, and gated_decision 5) prescribes slicing the real ROADMAP.md by heading anchor: `### In scope — the engine` (:21), `### In scope — the application` (:37), `### Out of scope` (:73), `## Open questions, by the phase that answers them` (:322). I verified all four headings exist verbatim — but three of them contain U+2014 EM DASH. If the implementer types a hyphen, or a heading is later reworded, `text.split(anchor)` finds nothing, the slice is empty, `_item_ids("")` returns `set()`, and the test asserts `== set()` — PASSING while proving nothing about the four tables it was written to prove empty. The plan correctly rejected hardcoded line offsets as brittle (finding F-28's logic) but replaced them with a substitute that fails SILENTLY rather than loudly, which is strictly worse. AC 4 gave the entry parser a non-vacuity guard; the roadmap parser's negative assertion got none.
- **proposed_fix:** Two changes. (1) Anchor on the em-dash-free prefixes — `"### In scope"` (take both occurrences), `"### Out of scope"`, `"## Open questions"` — or match with a compiled regex on the heading line rather than a literal split. (2) Before asserting zero ids, assert each slice is non-empty AND contains at least one `|`-leading row, with a message like 'the ROADMAP heading anchors moved — this negative assertion is proving nothing'. Same shape as AC 4, applied to the other half of the parser.
- **reviewer:** code-grounded

### F-05

- **id:** F-05
- **title:** `FENCED_BLOCK.findall()` returns group tuples, not block content — the AC 11 template extraction as described does not work
- **severity:** minor
- **confidence:** high
- **category:** correctness
- **location:** tests/test_request_links.py:26
- **problem:** The plan tells the implementer to 'copy the shape at tests/test_request_links.py:26' and 'Expose `_fenced_blocks(text: str) -> list[str]` for the AC 11 test'. `FENCED_BLOCK = re.compile(r"^([ \t>]*)(`{3,}|~{3,}).*?^\1\2.*?$", re.DOTALL | re.MULTILINE)` has TWO capture groups (indent, fence chars), so the obvious implementation — `return FENCED_BLOCK.findall(text)` — returns the groups, not the block. I measured it: on a document with one fenced example, `findall` returns `[('', '```')]` while `[m.group(0) for m in finditer(...)]` returns the real block `'```markdown\n### E-000 - x\n- **Status:** open\n```'`. (`FENCED_BLOCK.sub("", ...)` for the body-side fence strip works correctly — that half of the plan is fine.) The mis-implementation fails loudly (AC 11 asserts exactly one entry, gets zero), but the plan itself warns that the likely reaction when AC 11 misbehaves is to weaken it, which would delete the only mechanical proof goal 1 has.
- **proposed_fix:** Spell the implementation out in the plan rather than saying 'copy the shape': `def _fenced_blocks(text: str) -> list[str]: return [m.group(0) for m in FENCED_BLOCK.finditer(text)]`, and note that `group(0)` includes the opening ```` ```markdown ```` and closing ```` ``` ```` delimiter lines — harmless for the MULTILINE `ENTRY`/`FIELD` regexes, but say so explicitly so nobody strips them wrong.
- **reviewer:** code-grounded

### F-06

- **id:** F-06
- **title:** Phase 1's `Select-String ROADMAP.md -Pattern 'serviceable'` acceptance check cannot fail
- **severity:** minor
- **confidence:** high
- **category:** test-vacuity
- **location:** ROADMAP.md:220
- **problem:** Phase 1's acceptance bullet reads: "`Select-String ROADMAP.md -Pattern 'serviceable'` still returns the preserved observation". I ran it: 'serviceable' occurs at ROADMAP.md:13, :39, :53, :220, and :248. Four of those five are nowhere near the paragraph being edited (the v1 blockquote, the application-scope intro, the 'real constraint in both directions' callout, and Phase 3's Proves line). So the check returns hits whether or not AC 13's required sentence at :220-222 survives — it proves nothing about the one thing it was written to prove, which is exactly the 'preserved, not dropped' half of AC 13.
- **proposed_fix:** Grep for a fragment unique to the sentence being preserved: `Select-String ROADMAP.md -Pattern 'nowhere defined or tested'` (I verified this phrase appears only at :221). Better still, fold it into the AC 13 pytest assertion in tests/test_escalations.py alongside the negative assertions for 'autonomous stage dispatcher' and 'design/UX specialist', so it is enforced rather than eyeballed once.
- **reviewer:** code-grounded

### F-07

- **id:** F-07
- **title:** The /update-docs CLAUDE.md budget uses a different command AND a different ceiling than AC 23 — both pass, but the plan never reconciles them
- **severity:** minor
- **confidence:** high
- **category:** process-friction
- **location:** .claude/skills/update-docs/SKILL.md:76
- **problem:** The plan's Phase 0 says 'Do NOT use `Measure-Object -Line` — `.claude/skills/update-docs/SKILL.md` prescribes it and it under-reports' but never gives the number or the other budget. Measured: `.claude/skills/update-docs/SKILL.md:76-77` says '`CLAUDE.md` stays **under 200 lines**. Check it: `(Get-Content CLAUDE.md | Measure-Object -Line).Lines`', and that command returns **181** today versus `(Get-Content CLAUDE.md).Count` == **221**. `/commit` Step 3 runs `/update-docs` at EVERY phase checkpoint in this plan, so the implementer will see 181/200 five times while the plan insists the baseline is 221/222. Both gates in fact pass (181→182 stays under 200), but nothing in the plan says so, and the natural reaction to two contradictory numbers is to stop and re-litigate scope risk 15 mid-build.
- **proposed_fix:** Record both measurements in Phase 0's acceptance: '`(Get-Content CLAUDE.md).Count` == 221 (AC 23's baseline, ceiling 222) and `(Get-Content CLAUDE.md | Measure-Object -Line).Lines` == 181 (the /update-docs budget at update-docs/SKILL.md:76, ceiling 200). Both are satisfied by a +1-line change; they are independent gates measuring different things, and reconciling them is scope risk 15's own bugfix request, not this item's work.'
- **reviewer:** code-grounded

### F-08

- **id:** F-08
- **title:** One files_to_touch entry carries a malformed, non-existent path in its `path` field
- **severity:** minor
- **confidence:** high
- **category:** cold-handoff
- **location:** requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md:1
- **problem:** The draft's `files_to_touch` contains an entry whose `path` is the string `"requests\feature-requests\PROJECT_SCOPE.md — actual path requests\feature-requests\H1-escalation-queue\PROJECT_SCOPE.md"` — a path concatenated with an English correction. `requests/feature-requests/PROJECT_SCOPE.md` does not exist (I listed the directory: it holds only README.md, the H1 item dir, and _done/). A cold implementer trusting the field literally opens nothing; one skimming it may create the file at the wrong level. The intended target is `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md`, whose line 1 I read: `> **Status:** scoped · created 2026-08-15 · decided · next: plan`.
- **proposed_fix:** Replace the `path` with the single correct repo-relative path `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md` and move the note ('body is DECIDED and consumed, never revised; status blockquote at :1 only') entirely into the `change` field.
- **reviewer:** code-grounded

### F-09

- **id:** F-09
- **title:** The stated reason for fence-stripping ROADMAP.md is wrong; the load-bearing fence strip is on the queue side only
- **severity:** nit
- **confidence:** high
- **category:** accuracy
- **location:** ROADMAP.md:289
- **problem:** The Phase 2 step for `known_moments` says 'Strip fenced blocks first (`ROADMAP.md` carries a fenced ASCII diagram).' I checked the diagram — it is ROADMAP.md:289-295, and its body lines are `Phase 0   Harness      ░     workbench ...`. None begins with `|` (so `TABLE_ROW` cannot match it) and none begins with `###` (so `PHASE_HEADING` cannot match it). Fence-stripping the roadmap is a genuine no-op. Stated as a requirement with a false justification, it invites a cold implementer to hunt for the fence-vs-table interaction that supposedly motivates it, and risks obscuring where the fence strip actually IS load-bearing: the queue body, where it is the only thing keeping the `E-000` worked example from colliding with AC 8's uniqueness guard and AC 9's section agreement.
- **proposed_fix:** Reword: 'Fence-stripping the roadmap is harmless and cheap, but it is NOT what makes this work — the ASCII diagram at ROADMAP.md:289-295 contains no `|`-leading rows and no `###` headings, so it contributes nothing either way. The fence strip that IS load-bearing is on the QUEUE side (see AC 11), and that one is not optional.'
- **reviewer:** code-grounded

### F-10

- **id:** F-10
- **title:** Should the seam substring tests also assert the surrounding instruction, given the plan's own inertness argument?
- **severity:** question
- **confidence:** medium
- **category:** test-strength
- **location:** .claude/skills/commit/SKILL.md:133
- **problem:** gated_decision 7 recommends anchoring the three seam tests on the bare filename `ESCALATIONS.md`, and I confirmed the anchor is clean — `Select-String` over make-feature-request/SKILL.md, commit/SKILL.md, and diagnose-bug/SKILL.md returns zero hits for 'ESCALATIONS' today. But the plan simultaneously names inertness as 'the dominant risk ... named independently by all three scopers and all three planners', and a bare-filename assertion passes if the bullet is rewritten into a sentence that no longer instructs anyone to read the queue. The plan states this weakness honestly and still recommends the weak anchor. Given that these three bullets ARE the entire inertness mitigation, and that the /commit drain bullet in particular is a third rail after commit/SKILL.md:133-138 where a rewrite is plausible, a two-part assertion may be worth the reflow brittleness.
- **proposed_fix:** Consider a two-part assertion per seam: the filename PLUS one verb-bearing token that survives reflow — e.g. `"ESCALATIONS.md" in body and "surface" in bullet` where `bullet` is the line containing the filename. That catches a filename left stranded in a non-instruction while breaking only on a genuine rewording. Flagging as a question rather than a finding: the plan's reasoning is sound and this is a judgment call the implementer is explicitly licensed to make ('the implementer may tighten it if they find a phrase worth the brittleness').
- **reviewer:** code-grounded

### F-11

- **id:** F-A2-01
- **title:** Phase 0 asserts a green baseline that is already red, and no phase performs the scoped→plan status rollover
- **severity:** blocker
- **confidence:** high
- **category:** sequencing
- **location:** plan Phase 0 steps 2 + acceptance 2; tests/test_repo_structure.py:286-319; .claude/skills/create-implementation-plan/SKILL.md:170-173; requests/feature-requests/README.md:116
- **problem:** The stage-3 skill that produces this plan explicitly sets two things when it writes IMPLEMENTATION_PLAN.md: `.claude/skills/create-implementation-plan/SKILL.md:172` — "set this item's **Index** row Stage cell to `plan`" — and `:173`/`:176` — the artifact opens at stage `plan`. It does NOT touch `FEATURE_REQUEST.md:1` or `PROJECT_SCOPE.md:1`, both of which currently read `scoped` (verified: `requests/feature-requests/README.md:116` reads `| [H1-escalation-queue] (H1-escalation-queue/) | scoped |` today, and the item directory holds only FEATURE_REQUEST.md, PROJECT_SCOPE.md and reviews/). `tests/test_repo_structure.py:286-319` matches the Index row's stage cell against EVERY `*.md` directly under the item directory, so the instant this plan lands there are two mismatches and the suite is RED. Phase 0's acceptance says "All four gates exit 0 on an unmodified tree; `uv run pytest -q` reports 55 passed", and Phase 0 step 2 says "Any red here is pre-existing, not caused by this work." A cold agent hits a red suite on its very first command, is told by the plan to ignore it, and proceeds through four `/commit`-gated phases with a known-red test — or burns an hour discovering the plan's own arrival caused it. The plan documents the invariant in its risks and lists the three files in `files_to_touch`, but no PHASE STEP anywhere performs the rollover, so it is a checklist item with no owner.
- **proposed_fix:** Add an explicit first step to Phase 0, before the baseline measurement: "Reconcile the stage lockstep that this plan's own arrival broke. Set `requests/feature-requests/H1-escalation-queue/FEATURE_REQUEST.md:1` and `PROJECT_SCOPE.md:1` to `> **Status:** planned …`, set this plan's own header to `planned`, and set the Index cell at `requests/feature-requests/README.md:116` to `planned` (the stage-3 skill wrote `plan`; the repo's grammar at `requests/feature-requests/README.md:106` is `intake → scoped → planned → implemented`, and the Index/artifact comparison is exact-word). Then run `uv run pytest tests/test_repo_structure.py::test_index_stage_cells_match_their_artifact_status_headers -q` and confirm green." Change Phase 0's acceptance bullet to: "After the lockstep rollover, all four gates exit 0 and `uv run pytest -q` reports 55 passed." Either land the rollover as its own `/commit` or fold it into Phase 1's commit, but say which.
- **reviewer:** executability

### F-12

- **id:** F-A2-02
- **title:** The plan's own files_to_touch paths will fail tests/test_no_leaks.py the moment /commit stages the plan
- **severity:** blocker
- **confidence:** high
- **category:** convention-violation
- **location:** plan files_to_touch (all 16 entries) and onboarding.files_to_read (all 10 entries); tests/test_no_leaks.py:26,41,61-74
- **problem:** Every path in the draft's `files_to_touch` and `files_to_read` is written machine-absolute — `ESCALATIONS.md`, `tests\test_escalations.py`, and so on. `tests/test_no_leaks.py:26` defines `WINDOWS_PATH = re.compile(r"\b[A-Za-z]:[\\/] (?:[\w .()-]+[\\/]){1,}[\w .()-]*")`, `.md` is in `TEXT_SUFFIXES` (`:41-58`), and `_tracked_text_files()` (`:61-74`) scans everything `git ls-files` reports. `IMPLEMENTATION_PLAN.md` is a tracked artifact under `requests/feature-requests/`. I grepped that whole tree for the pattern and found ZERO matches — no existing artifact does this, including the 989-line `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md`. So the first `/commit` that stages this plan turns `test_no_windows_absolute_paths` red, in a repo whose CLAUDE.md names that guard as a binding public-repo rule. Worse, the plan's own Phase 5 acceptance claims the leak guards pass — a claim its own body falsifies.
- **proposed_fix:** Rewrite every path in the plan document repo-relative before it is written to disk: `ESCALATIONS.md`, `tests/test_escalations.py`, `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md`, `.claude/skills/commit/SKILL.md`, etc. Add a line to Phase 0's steps: "Before the first `/commit`, run `uv run pytest tests/test_no_leaks.py -q` — the plan artifact is itself tracked and scanned, and machine-absolute paths in a plan are the most common way this guard fires."
- **reviewer:** executability

### F-13

- **id:** F-A2-03
- **title:** Phase 2's acceptance pins an exact entry count, reintroducing the brittleness the plan rejects for AC 2
- **severity:** major
- **confidence:** high
- **category:** acceptance-quality
- **location:** plan Phase 2 acceptance bullet 5 ("`len(parse_entries(...))` == 7"); plan gated_decisions #2
- **problem:** The plan argues at length — decisions entry 5, testing section failure-mode 3, code_references — that AC 2 must be `>= 30` rather than `== 38` because an exact count "fires in every unrelated PR that adds a row", and instructs the implementer to write the reason in a comment so nobody tightens it. It then does exactly the rejected thing one phase later: Phase 2's acceptance requires `len(parse_entries(...)) == 7`. The queue's entire purpose is that entries get added; the eighth parked decision — which may arrive during this very build, since the plan's own gated_decisions #2 offers to add one about superseding correction events — turns that check red for no defect. It also conflicts with Phase 4, which adds no entries but does add tests, and with Phase 5, whose full-suite run would inherit the pin.
- **proposed_fix:** Change the acceptance bullet to `len(parse_entries(...)) >= 7`, and note that the SEVEN-seed requirement is already proven the right way by AC 12's distinctive-substring assertions plus AC 4's non-vacuity guard — a count adds nothing they don't cover and adds a failure mode they don't have.
- **reviewer:** executability

### F-14

- **id:** F-A2-04
- **title:** "Prove the guard bites" is never resolved into a committed test or a manual check
- **severity:** major
- **confidence:** high
- **category:** acceptance-quality
- **location:** plan Phase 2 acceptance bullet 7; plan Phase 4 step 7 and acceptance bullet 2
- **problem:** Two of the plan's most valuable verification steps are stated without saying what artifact they produce. Phase 2: "Prove the non-vacuity guard bites WITHOUT touching a tracked file: copy the queue into `tmp_path`, mangle a field name in the COPY, and confirm `parse_entries` returns `[]` and the AC 4 assertion would fire." Phase 4: "copy the skill file to `tmp_path`, delete the bullet in the COPY, and confirm the assertion reports it" / acceptance: "each is demonstrated to FAIL when its bullet is removed from a `tmp_path` copy — proven, not asserted." A cold agent cannot tell whether to commit a red/green pair or run a throwaway command at the console. If it is manual, the proof evaporates the moment the shell closes, stage 4's acceptance panel cannot re-verify it, and the regression it guards against returns silently — which is the exact failure `tests/test_layering.py:85-100` was built to avoid by committing BOTH directions. Everything needed is already in place: the plan mandates that `parse_entries` and the seam checks take TEXT rather than a path, which makes each red case a three-line committed test.
- **proposed_fix:** Rewrite both as deliverables, not checks. Phase 2: "Write `test_a_drifted_entry_format_parses_to_nothing(tmp_path)` — fabricate a queue whose field label is `**Bears-on:**`, assert `parse_entries(text) == []`, and assert `NO_ENTRIES_MESSAGE` is what the non-vacuity guard raises." Phase 4: "Write one `tmp_path` red test per seam — pass the skill text with the bullet stripped to the pure checker and assert it reports the seam missing." Then the acceptance bullets read "these six tests exist and are green", which is mechanically verifiable.
- **reviewer:** executability

### F-15

- **id:** F-A2-05
- **title:** FENCED_BLOCK.findall() returns capture-group tuples, not fenced blocks — _fenced_blocks as specified will not work
- **severity:** major
- **confidence:** high
- **category:** correctness
- **location:** plan Phase 2 step 6 ("Expose `_fenced_blocks(text: str) -> list[str]`") and architecture_map ("reusing the `FENCED_BLOCK` regex shape at `tests/test_request_links.py:26`"); tests/test_request_links.py:26
- **problem:** `FENCED_BLOCK = re.compile(r"^([ \t>]*)(`{3,}|~{3,}).*?^\1\2.*?$", re.DOTALL | re.MULTILINE)` has two capture groups. The existing consumer only ever calls `.sub()` (`tests/test_request_links.py:41`), where that is harmless. The plan's new consumer needs the block CONTENT for AC 11, and the obvious call — `FENCED_BLOCK.findall(text)` — returns `[('', '```'), …]`: the indent and the fence delimiter, never the body. A cold agent gets an empty template, AC 11 fails with a message about zero entries, and the likely 'fix' is the one the plan itself warns is fatal — weakening AC 11, which deletes the only mechanical proof goal 1 has. The plan flags the AC 11 / AC 8 / AC 9 coupling in detail but says nothing about this mechanical trap in the regex it prescribes reusing.
- **proposed_fix:** Spell the implementation out in the step: "`_fenced_blocks` must use `FENCED_BLOCK.finditer(text)` and take `m.group(0)` — `findall` on this pattern returns `(indent, fence)` tuples because it has two capture groups, not the block body. Then drop the first and last line of each match (the fence delimiters) before handing the text to `parse_entries`." Add one assertion to the AC 11 test that the extracted template is non-empty, so this failure surfaces as "template not extracted" rather than as "template malformed".
- **reviewer:** executability

### F-16

- **id:** F-A2-06
- **title:** Casefolding known_moments makes the scope's AC 2 assertion literally false
- **severity:** major
- **confidence:** high
- **category:** acceptance-quality
- **location:** plan architecture_map ("Return the union CASEFOLDED"), Phase 2 step 5 and AC-2 step, Phase 2 acceptance bullet 3; PROJECT_SCOPE.md:120-123
- **problem:** The decided scope's AC 2 requires the returned set to contain "known-good ids (`0.1`, `1.3`, `H2`, `4.6`)". The plan makes `known_moments` return everything casefolded, so `H2` is never in the set — only `h2` — and then rewrites the acceptance to assert `h2`. The casefold NEED is real and well argued (`### Post-v1` at ROADMAP.md:277 versus AC 5's `post-v1` fixture — I verified both), but pushing it into the accessor silently rewrites a decided criterion and makes the returned set a lossy view of the roadmap. It also makes the AC 7 failure message harder to write well: the plan wants the message to name "the offending moment", and a casefolded vocabulary means any suggestion the message offers comes out lowercased and unlike what the roadmap actually reads.
- **proposed_fix:** Keep case in the data, fold at the comparison: `known_moments()` returns the ids and phase names verbatim (so `assert {"0.1", "1.3", "H2", "4.6"} <= known_moments(text)` satisfies AC 2 word-for-word), and `moment_violations` does the one-line fold — `known = {m.casefold() for m in known_moments(roadmap_text)}` — with an inline comment naming `### Post-v1` vs `post-v1` as the reason. One extra line, and the criterion stops needing a footnote.
- **reviewer:** executability

### F-17

- **id:** F-A2-07
- **title:** Entry.section is undefined for the fenced template, and the plan's "same field guards" wording invites a helper that makes AC 11 unsatisfiable
- **severity:** major
- **confidence:** high
- **category:** correctness
- **location:** plan Phase 2 step 6 ("Split the body on `## Open` / `## Resolved` so each entry carries its section") and AC 11 step ("run the SAME `parse_entries` and the SAME field guards over it"); PROJECT_SCOPE.md:144-147 (AC 9) and :151-154 (AC 11)
- **problem:** `parse_entries` is specified to take text and attach a `section` to each entry, and it is called twice — once on the fence-stripped body and once on the extracted `E-000` template. The template has no `## Open` / `## Resolved` heading above it, so its entry's `section` is whatever the implementation defaults to. The plan never says what that is, nor what should happen to an entry that appears outside both sections in the real queue. Meanwhile AC 11 is described as running "the SAME regex and field guards" and AC 9 as a per-entry section/Status agreement check. A cold agent's natural move is a single `_assert_entry_valid(entry)` helper covering fields + status vocabulary + section agreement, applied to both call sites — at which point AC 11 fails on the template and the agent starts weakening AC 11, the one outcome the plan flags as fatal. Separately, an entry accidentally written above `## Open` in the real file gets `section=None` and slips past AC 9 entirely, so the guard is quietly weaker than the criterion.
- **proposed_fix:** Split the guards explicitly in the step text: (a) a per-entry FIELD guard — six fields present, `^E-\d{3}$` id, `Status:` in `STATUS_VALUES` — applied to both real entries and the template; (b) a DOCUMENT-level guard applied only to the queue — ids unique, every entry's `section` is exactly `open` or `resolved` (a `None` section is itself a failure, message: "entry outside both sections"), and section agrees with `Status:`. State that `Entry.section` is `None` for a text with no section headings and that this is expected for the template.
- **reviewer:** executability

### F-18

- **id:** F-A2-08
- **title:** No step updates ROADMAP.md:168-170, the prose that says "Harness row H1 is in flight"
- **severity:** major
- **confidence:** high
- **category:** missing-step
- **location:** ROADMAP.md:168-170; .claude/skills/commit/SKILL.md:111-131; plan Phase 5 steps
- **problem:** ROADMAP.md's Phase 1 header carries a narrative status paragraph: "**Status:** **IN-PROGRESS** — 1.1 `app-shell` has landed the application skeleton. No domain logic yet. Harness row H1 is in flight; 1.2 `career-ledger` is the next numbered item." (verified at :168-170). `/commit` Step 4 owns the Status COLUMN and the phase-header aggregate word — `.claude/skills/commit/SKILL.md:111-114` says it owns "a **Status** column on every phase item … plus an aggregate on each phase header", and :128-131 covers the aggregate derivation. Nothing in that step covers this free prose. The plan's Phase 5 correctly says the Phase 1 aggregate stays IN-PROGRESS, but leaves the sentence claiming H1 is still in flight after H1 is DONE — stale text in the single document the plan calls "the spec of record", guarded by no test.
- **proposed_fix:** Add a Phase 5 step: "Update the Phase 1 status prose at `ROADMAP.md:168-170` — H1 has landed and no longer 'is in flight'; the sentence should read that H1 `escalation-queue` is DONE and 1.2 `career-ledger` is next. This is prose, not a Status cell, so `/commit` Step 4 will not do it for you." Note in the same step that `CLAUDE.md`'s Status paragraph does NOT mention H1 (verified) and so needs no edit — which also protects the +1 line budget.
- **reviewer:** executability

### F-19

- **id:** F-A2-09
- **title:** The plan describes the Index cell as moving scoped→planned, but the stage-3 skill already moved it to `plan`
- **severity:** major
- **confidence:** high
- **category:** stale-precondition
- **location:** plan architecture_map ("Today H1's Index cell … and both artifacts say `scoped` — green"), files_to_touch entry for requests/feature-requests/README.md; .claude/skills/create-implementation-plan/SKILL.md:170-173; requests/feature-requests/README.md:116
- **problem:** The plan states the starting state as "Today H1's Index cell (`requests/feature-requests/README.md:116`) and both artifacts say `scoped` — green" and instructs `Stage cell `scoped` → `planned` when this plan lands`. That snapshot expires at the instant the plan is written: `.claude/skills/create-implementation-plan/SKILL.md:172` directs the stage-3 skill to set the Index Stage cell to `plan` as part of producing this document. So the cold agent opens `README.md:116` looking for `scoped`, finds `plan`, and now has to reason from first principles about which of three tokens is right — while the suite is red (see F-A2-01). This is a distinct problem from the missing rollover step: it is a stated precondition that will be false when read.
- **proposed_fix:** Restate the precondition as a decision tree rather than a snapshot: "When you start, `requests/feature-requests/README.md:116` reads either `scoped` (the plan was not landed by `/create-implementation-plan`) or `plan` (it was — the skill sets that token at `SKILL.md:172`). Either way the correct value is `planned`, per the grammar at `requests/feature-requests/README.md:106`. Set the cell and all artifact headers to `planned` together."
- **reviewer:** executability

### F-20

- **id:** F-A2-10
- **title:** Phase 5 requires moving a directory but gives no mechanism, and the plan's own conventions tell the executor git is read-only
- **severity:** major
- **confidence:** medium
- **category:** missing-step
- **location:** plan Phase 5 step 6; plan conventions bullet 2; requests/feature-requests/README.md:96-100; tests/test_request_links.py:31-37
- **problem:** Phase 5 says "move the item directory ONCE into `requests/feature-requests/_done/H1-escalation-queue/` and repoint the Index link." The plan's conventions section, quoted verbatim from CLAUDE.md, says "Never `checkout`/`reset`/`restore`/`clean`/`stash` or anything that discards working-tree state", and Phase 0 step 1 tightens it to "Git is read-only for you beyond this." A cold agent has no sanctioned move command: `git mv` is a git write, and the plan never names `Move-Item`. Second-order risk the plan also omits: `requests/feature-requests/README.md` is inside `SCANNED_TREES` (`tests/test_request_links.py:24`) and is NOT `_done`-exempt, so if the directory moves without the Index link at `:116` being repointed in the SAME edit, `test_process_artifacts_have_no_dead_relative_links` goes red on a link that pointed at a directory that no longer exists.
- **proposed_fix:** Name the command and the coupling: "Move with `Move-Item requests/feature-requests/H1-escalation-queue requests/feature-requests/_done/` (a filesystem move, not `git mv` — `/commit` stages the rename). In the SAME edit, repoint the Index link at `requests/feature-requests/README.md:116` to `[H1-escalation-queue] (_done/H1-escalation-queue/)`; the README itself is link-checked (`tests/test_request_links.py:24`, no `_done` exemption for the file DOING the linking), so a move without the repoint is an immediate red." Also clarify whether the read-only-git rule binds the executor here or only spawned subagents.
- **reviewer:** executability

### F-21

- **id:** F-A2-11
- **title:** AC 3's heading-anchor slicing never defines its terminator, and two anchors share a prefix
- **severity:** minor
- **confidence:** high
- **category:** under-specification
- **location:** plan Phase 2 AC-3 step and decisions entry 5; ROADMAP.md:21, :37, :73, :86, :322
- **problem:** The plan replaces AC 3's hardcoded line ranges with heading anchors — `### In scope — the engine`, `### In scope — the application`, `### Out of scope`, `## Open questions, by the phase that answers them` — "each up to the next heading", but never says what counts as a heading. Verified against the file: `### Out of scope` at :73 must terminate at `### Why deferring the age multiplier is defensible` (:86), and `## Open questions…` at :322 runs to end of file with no following heading at all. A naive `text.split(anchor)[1].split('###')[0]` also breaks on the two `### In scope` anchors sharing a prefix, and on `#### Harness — Phase 1` (:193), which is a level-4 heading the phase regex correctly ignores but a naive splitter would not.
- **proposed_fix:** Specify the slice: "`_section(text, anchor)` returns the text from the line equal to `anchor` up to the next line matching `^#{2,6}\s`, or end of file. Anchor on the FULL heading line, not a prefix — `### In scope — the engine` and `### In scope — the application` share five characters. Verified terminators today: engine→application (:37), application→`### Out of scope` (:73), out-of-scope→`### Why deferring the age multiplier is defensible` (:86), open-questions→EOF."
- **reviewer:** executability

### F-22

- **id:** F-A2-12
- **title:** Phase 0's dead-link one-liner silently depends on the working directory
- **severity:** minor
- **confidence:** high
- **category:** environment-assumption
- **location:** plan Phase 0 step 7
- **problem:** The prescribed command is `uv run python -c "import sys; sys.path.insert(0,'tests'); … [print(p.name, t._dead_links(Path(p))) for p in Path('.').glob('*.md')]"`. Both `sys.path.insert(0,'tests')` and `Path('.')` are relative to the process CWD. Agent tool calls reset their working directory between invocations in this harness (stated in the environment notes), so run from anywhere but the repo root this prints nothing and the acceptance bullet "`_dead_links()` returns `[]` for all five root documents" passes VACUOUSLY on an empty iteration — the exact vacuity failure mode the plan spends AC 4 defending against elsewhere. I ran it from the repo root and it does return `[]` for all five, so the claim is true; the command is what is fragile.
- **proposed_fix:** Make the command root-anchored and non-vacuous: `uv run python -c "import sys,pathlib; r=pathlib.Path('.').resolve(); sys.path.insert(0,str(r/'tests')); import test_request_links as t; docs=sorted(r.glob('*.md')); assert len(docs)==5, docs; [print(p.name, t._dead_links(p)) for p in docs]"`, and prefix the step with an explicit "run from the repo root".
- **reviewer:** executability

### F-23

- **id:** F-A2-13
- **title:** No instruction for the case where the branch check fails
- **severity:** minor
- **confidence:** high
- **category:** missing-step
- **location:** plan Phase 0 step 1 and acceptance bullet 1
- **problem:** Phase 0 step 1 says `git branch --show-current` "must print `phase1/escalation-queue`" and warns that `git switch -c` would fork a duplicate — but says nothing about what to do if it prints something else. Combined with the same step's "Git is read-only for you beyond this", a cold agent that lands on `main` or a stale branch has no legal next move and will either improvise a forbidden git write or start editing `main`, which CLAUDE.md flags as one of the genuinely unrecoverable actions. (Verified the branch is correct today, so this is a robustness gap, not a live failure.)
- **proposed_fix:** Add the exit: "If it prints anything else — `main` especially — STOP and surface it to the user. Creating or switching branches is not this plan's to do, and `main` is protected; do not edit a file until the branch is confirmed."
- **reviewer:** executability

### F-24

- **id:** F-A2-14
- **title:** "55 passed" is used as an acceptance anchor across phases without stating the expected delta
- **severity:** minor
- **confidence:** high
- **category:** acceptance-quality
- **location:** plan Phase 0 acceptance bullet 2, testing section per-phase selectors
- **problem:** The plan measures and cites 55 passed (I re-ran it: 55 dots on `phase1/escalation-queue`, clean tree — correct). But every later phase adds tests: Phase 2 adds roughly a dozen to `tests/test_escalations.py`, Phase 3 adds `test_project_maps_list_the_escalation_queue`, Phase 4 adds three seam tests. The per-phase acceptance bullets only say "green", so the count is an anchor with no forward contract — a cold agent cannot notice that a test module silently failed to collect (a plausible outcome of an import error inside a `-q` run that still reports "green" for the selector it ran). The plan's own AC 4 non-vacuity reasoning is exactly this concern applied one level down.
- **proposed_fix:** Either drop the count from acceptance and rely on the selectors, or make it a forward contract: state the expected floor per phase ("Phase 2: ≥ 67 passed, at least 12 of them from `tests/test_escalations.py`; Phase 3: ≥ 68; Phase 4: ≥ 71") and tell the agent to confirm the new module actually collected with `uv run pytest tests/test_escalations.py --collect-only -q`.
- **reviewer:** executability

### F-25

- **id:** F-A2-15
- **title:** /commit's doc gate may propose CLAUDE.md edits that break the hard +1 line budget
- **severity:** minor
- **confidence:** medium
- **category:** convention-interaction
- **location:** plan Phase 3 last step (AC 23); .claude/skills/commit/SKILL.md:102-107; PROJECT_SCOPE.md:190-191
- **problem:** AC 23 is a hard numeric criterion — `(Get-Content CLAUDE.md).Count` may increase by at most 1 against the measured 221 (I verified 221). Phase 3 budgets exactly that: one line inside the project-map fence, plus a zero-delta word swap at `:216` (verified: `:216` says "Nine decisions are settled" while `:57`, `:90` and `:111` all say ten). But every phase ends at `/commit`, and `/commit` Step 3 runs the doc gate — `.claude/skills/commit/SKILL.md:102` explicitly includes "a read of `CLAUDE.md`'s project map against the tree", and `:105-107` says a flag means "stop and surface it." Landing a brand-new root document is precisely the signal that gate looks for, so it is likely to propose additional CLAUDE.md prose. The plan warns the implementer to resist adding a bullet themselves but never anticipates the gate proposing one, and a criterion that a sanctioned tool can push over the line deserves an explicit answer.
- **proposed_fix:** Add to Phase 3's commit note: "`/commit` Step 3's doc gate will notice a new root document and may propose more CLAUDE.md prose. Decline anything beyond the one project-map line and say why — AC 23 caps the delta at +1 against a measured 221, and the queue's own boundary header carries the content a CLAUDE.md bullet would duplicate. Re-measure `(Get-Content CLAUDE.md).Count` after the commit, not only before."
- **reviewer:** executability

### F-26

- **id:** F-A2-16
- **title:** Phase 4's "Grep confirms no seam instructs a skill to WRITE an entry" is not a runnable check
- **severity:** minor
- **confidence:** high
- **category:** acceptance-quality
- **location:** plan Phase 4 acceptance bullet 5; PROJECT_SCOPE.md Decision 2 (:357)
- **problem:** The bullet names no pattern and no files, so it cannot be executed or reproduced — and it guards a real boundary: scope Decision 2 defers "teach a skill to WRITE entries" to its own request specifically because `Blocks: 1.3` makes scope creep expensive. As written, an implementer whose `/commit` bullet grew from "surface open entries" into "surface open entries and append a resolution note" would tick this bullet honestly.
- **proposed_fix:** Replace with a concrete check plus a human read: "`Select-String -Path .claude/skills/*/SKILL.md -Pattern 'ESCALATIONS' -Context 2,2` — read every hit and confirm each verb is a READ (surface / open / check), never a write (add / append / record / park an entry). Confirm each seam is at most one bullet and that the three edits total under ten added lines across three files."
- **reviewer:** executability

### F-27

- **id:** F-A2-17
- **title:** The fence-strip on ROADMAP.md is justified by a condition that does not exist
- **severity:** nit
- **confidence:** high
- **category:** grounding
- **location:** plan Phase 2 step 5 ("Strip fenced blocks first (`ROADMAP.md` carries a fenced ASCII diagram)"); ROADMAP.md:289-295
- **problem:** ROADMAP.md has exactly one fenced block, at :289-295 — a five-line ASCII bar chart of the phases. I read it: it contains no `|`-delimited rows and no `###` headings, so it can contribute neither an id nor a phase name, and stripping it is a no-op. The instruction is harmless but its stated reason is wrong, and a cold agent who checks the claim and finds it false will start doubting the neighbouring instructions that ARE load-bearing (the id discriminator, the casefold).
- **proposed_fix:** Keep the strip, fix the rationale: "Strip fences before parsing as a defensive habit — today's only fence (`ROADMAP.md:289-295`, the phase bar chart) contributes nothing either way, but a future fenced example of a roadmap ROW would be picked up as a real id if the strip were absent."
- **reviewer:** executability

### F-28

- **id:** F-A2-18
- **title:** A files_to_touch entry carries a malformed, self-contradicting path
- **severity:** nit
- **confidence:** high
- **category:** grounding
- **location:** plan files_to_touch, entry 15
- **problem:** The entry reads `requests\feature-requests\PROJECT_SCOPE.md — actual path requests\feature-requests\H1-escalation-queue\PROJECT_SCOPE.md`. The `path` field is a location that does not exist, with the correction stuffed into the same string. A cold agent trusts these literally; `requests/feature-requests/PROJECT_SCOPE.md` is not a file, and there is no reason the field cannot simply be right.
- **proposed_fix:** Set the path to `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md` and move the note ("status blockquote at :1 only; the body is DECIDED and is consumed, never revised") into the `change` field where it belongs — see also F-A2-02 on making all of these repo-relative.
- **reviewer:** executability

---

## Meta-audit findings (did the merge converge faithfully?)


### M-01

- **id:** F1
- **title:** The `planned` status rollover is owned by no phase, and Phase 0's green-baseline acceptance is unachievable because of it
- **severity:** major
- **confidence:** high
- **category:** completeness-drop
- **location:** Merged plan phases[0] (Phase 0) steps + acceptance bullet 2; risks item 2; files_to_touch entries for FEATURE_REQUEST.md and requests/feature-requests/README.md
- **problem:** I verified the live state: requests/feature-requests/README.md:116 Index cell = `scoped`, FEATURE_REQUEST.md:1 = `scoped`, PROJECT_SCOPE.md:1 = `scoped` — green today. tests/test_repo_structure.py:286-319 iterates `item_dir.glob('*.md')` and asserts every artifact's Status word equals the Index cell. The stage-3 skill (.claude/skills/create-implementation-plan/SKILL.md:170-173) instructs setting ONLY the Index cell and the new plan's own header — it says nothing about the two siblings. So the moment this plan lands, three files disagree and that test goes RED. The merge kept the risk (risks item 2: 'Bump all of them plus the Index cell together') and kept the files_to_touch notes ('Rolled to `planned` when the plan lands'), but assigned the remediation to NO PHASE. Phase 0 then asserts as acceptance: 'All four gates exit 0 on an unmodified tree; uv run pytest -q reports 55 passed' and its step says 'Any red here is pre-existing, not caused by this work' — which is exactly wrong: this red IS caused by this plan landing. The sequencing planner handled it explicitly (Phase 0 step 2, with a conditional acceptance 'green at HEAD, or red only on test_index_stage_cells_match_their_artifact_status_headers and green after the status-header sync'). The merge dropped that step while keeping only the warning.
- **proposed_fix:** Add an explicit Phase 0 step: 'If `uv run pytest tests/test_repo_structure.py::test_index_stage_cells_match_their_artifact_status_headers` is red, sync FEATURE_REQUEST.md:1, PROJECT_SCOPE.md:1, IMPLEMENTATION_PLAN.md:1 and the Index cell at requests/feature-requests/README.md:116 all to `planned` — three one-line edits, bookkeeping not scope, carried into Phase 1's /commit rather than committed alone.' Then relax Phase 0's acceptance to SEQ's conditional form: 'All four gates green at HEAD, or red only on test_index_stage_cells_match_their_artifact_status_headers and green after the sync.'
- **reviewer:** meta-audit

### M-02

- **id:** F2
- **title:** Merge narrowed the entry-heading regex to em-dash-only, dropping the code-grounded planner's tolerant alternation and opening a per-entry silent skip
- **severity:** major
- **confidence:** medium
- **category:** signal-loss
- **location:** Merged plan phases[2] (Phase 2), step 3: `ENTRY = re.compile(r"^###\\s+(?P<id>E-\\d{3})\\s*—\\s*(?P<title>.+)$", re.MULTILINE)`
- **problem:** The code-grounded planner proposed `ENTRY_HEADING` matching `^###\\s+(?P<id>E-\\d{3})\\s*[em-dash or hyphen]\\s*(?P<title>.+)$` — i.e. an alternation tolerating a plain hyphen. The merge silently narrowed it to em-dash-only and recorded no rationale in `decisions`. Consequence: a worker who types `### E-008 - Should corrections carry a delta?` produces an entry the parser does not see at all. Every downstream guard the plan calls load-bearing then passes on that entry — AC 6 (moment must exist), AC 8 (six fields, unique id), AC 9 (section agrees with Status). AC 4's non-vacuity guard does NOT catch it, because AC 4 only fires when ZERO entries parse; with seven seeds already present it can never fire on a single malformed eighth. This is precisely the silent-pass failure mode the merged plan calls 'the single most valuable test in the module', reintroduced one level down at entry granularity.
- **proposed_fix:** Restore the tolerant alternation: `\\s*[—–-]\\s*`. Additionally add a per-entry count guard beside AC 4, which is the real fix: count `^###\\s+E-` headings in the fence-stripped body with a loose regex, and assert it equals `len(parse_entries(...))`, failing with 'N entry headings found but M parsed — one entry's heading does not match ENTRY'. That catches any future heading-shape drift, not just the dash.
- **reviewer:** meta-audit

### M-03

- **id:** F3
- **title:** Phase 2 is disproportionately loaded, and the summary understates it as 'pure process/docs work'
- **severity:** major
- **confidence:** medium
- **category:** cost-unrealism
- **location:** Merged plan summary ('Pure process/docs work'); phases[2] (Phase 2), 19 steps and 8 acceptance bullets
- **problem:** Phase 2 as merged asks for: six pure functions (`_item_ids`, `known_moments`, `parse_entries`, `_fenced_blocks`, `moment_violations`, `violation_message`), an `Entry` frozen dataclass/NamedTuple, roughly ten module-level regex/frozenset constants, and thirteen distinct AC assertions (AC 2-13) — all fully annotated under `mypy strict = true` over `files = ["src", "tests"]` (verified pyproject.toml:82-84) with `ruff format --check` as a real CI step (verified ci.yml:40). For calibration, the idiom it copies, tests/test_layering.py, is 124 lines with two functions and four tests. The sequencing planner split exactly this work into two phases (parser + roadmap-side assertions first; queue-side assertions second) precisely because the parser is the highest-uncertainty piece. The merge adopted the OPPOSITE ordering (queue first) — defensible, and recorded in decisions — but then also collapsed SEQ's two-phase split into one, taking the cost of both choices. Meanwhile the summary frames the whole item as 'Pure process/docs work: nothing under src/ or app/ moves', which is true of the deliverable's location and false of its effort.
- **proposed_fix:** Split Phase 2 into 2a and 2b while KEEPING the merge's queue-first ordering. 2a: the parser and the assertions that only need ROADMAP.md and tmp_path — AC 1, 2, 3, 5, 7 — ending at /commit. 2b: the assertions that read the queue — AC 4, 6, 8, 9, 10, 11, 12, 13 — ending at /commit. Each phase then has a plausible single-sitting size and a real rollback point. Also amend the summary from 'Pure process/docs work' to something like 'No runtime code — one root document, one strictly-typed parser test module, three skill bullets.'
- **reviewer:** meta-audit

### M-04

- **id:** F4
- **title:** A files_to_touch entry has prose jammed into its path field, producing a path that does not exist
- **severity:** minor
- **confidence:** high
- **category:** correctness
- **location:** Merged plan files_to_touch, entry 15: path = 'requests\\feature-requests\\PROJECT_SCOPE.md — actual path requests\\feature-requests\\H1-escalation-queue\\PROJECT_SCOPE.md'
- **problem:** The `path` field contains a wrong path followed by an em dash and a prose correction. A cold implementer consuming files_to_touch programmatically or literally gets `requests/feature-requests/PROJECT_SCOPE.md`, which does not exist (verified: the H1 directory contains exactly FEATURE_REQUEST.md, PROJECT_SCOPE.md, and reviews/). The plan's own onboarding section elsewhere cites the correct path, so this is a merge artifact, not a belief — but it is exactly the class of error the plan spends a whole risk warning about ('a cold implementer trusts them literally').
- **proposed_fix:** Set path to `requests\\feature-requests\\H1-escalation-queue\\PROJECT_SCOPE.md` and move the note ('body is DECIDED and is consumed, never revised') into the `change` field where it already partly lives.
- **reviewer:** meta-audit

### M-05

- **id:** F5
- **title:** The phase-heading code_reference omits ROADMAP.md:163 and so contradicts the plan's own architecture_map
- **severity:** minor
- **confidence:** high
- **category:** correctness
- **location:** Merged plan code_references, ref 'ROADMAP.md:144, :224, :246, :261, :277'; contradicted by architecture_map ('MEASURED: that regex returns exactly ['Phase 0','Phase 1','Phase 2','Phase 3','Phase 4','Post-v1']')
- **problem:** I measured the headings: 144 (Phase 0), 163 (Phase 1), 224 (Phase 2), 246 (Phase 3), 261 (Phase 4), 277 (Post-v1). The code_reference lists only five line numbers and its claim text enumerates only five headings, omitting Phase 1 entirely — while architecture_map and the Phase 2 steps both assert six. The sequencing planner's proposal listed ':144, :163, :224, :246, :261' correctly; the merge dropped :163 when consolidating. A cold implementer cross-checking the citation against the file will find a sixth heading the plan does not cite and will not know whether the omission is deliberate (it is not) — which matters because the total-vocabulary arithmetic (38 + 6 = 44) depends on all six.
- **proposed_fix:** Change the ref to 'ROADMAP.md:144, :163, :224, :246, :261, :277' and add `### Phase 1 — Skeleton — **IN-PROGRESS**` to the claim text.
- **reviewer:** meta-audit

### M-06

- **id:** F6
- **title:** AC 3's heading-anchor slicing can silently produce empty slices, making the negative assertion vacuous — the exact trap AC 4 exists to prevent
- **severity:** minor
- **confidence:** medium
- **category:** test-vacuity
- **location:** Merged plan phases[2] (Phase 2), the AC 3 step ('Slice the real file by HEADING ANCHOR rather than by hardcoded line number'); decisions item 5; gated_decisions item 5
- **problem:** The merge chose to slice ROADMAP.md by heading anchors (`### In scope — the engine`, `### In scope — the application`, `### Out of scope`, `## Open questions, by the phase that answers them`) and prove each slice contributes zero ids. That is a defensible faithful reading of AC 3 and it is disclosed. But it introduces a vacuity hole the merge does not close: if a heading is ever reworded, `text.split(anchor)` yields no slice (or an empty one), `_item_ids('')` returns `set()`, and the assertion `== set()` PASSES while proving nothing. The sequencing planner avoided this by using inline fixture strings mirroring the real rows; the merge dropped that alternative along with SEQ's caution that fixtures should mirror real row shapes, and kept only the anchor approach with no guard on the anchor itself. The plan elsewhere (AC 4, and its own testing section) treats exactly this shape of silent pass as the most valuable thing to defend against.
- **proposed_fix:** Add one line to the AC 3 step: assert each anchor was FOUND before asserting its slice is empty — e.g. `assert anchor in text, f'{anchor} no longer appears in ROADMAP.md; the AC 3 slice is proving nothing'` — and assert each slice is non-empty text containing at least one `|` row, so a renamed heading fails loudly instead of passing vacuously.
- **reviewer:** meta-audit

### M-07

- **id:** F7
- **title:** Heavy cross-section duplication of the same corrections and traps invites drift between the phases and the risks list
- **severity:** minor
- **confidence:** medium
- **category:** dedup
- **location:** Merged plan: the third-stray correction appears in summary, onboarding files_to_read (2 entries), phases[0] step 5, phases[1] step 8, decisions item 7, risks item 1, convergence_map item 1, code_references (3 entries), and files_to_touch. The AC-18 rglob trap appears in architecture_map, phases[3] step 2, decisions item 3, risks item 4, convergence_map item 2, code_references, and files_to_touch (2 entries).
- **problem:** The merge converged the planners by restating each high-signal item everywhere it could plausibly belong rather than once where it acts. The third-stray correction is stated roughly ten times and the link-checker trap roughly seven. This is not merely verbose: it creates ten places that must be edited in lockstep if the user disposes gated_decisions differently (e.g. redirects E-006's moment), and it inflates the document to the point where a cold implementer is more likely to skim than read — which is the failure mode the whole feature is about. Note the duplication is not contradictory anywhere I checked; the risk is future drift, not present error.
- **proposed_fix:** State each correction/trap once, in the phase step that acts on it, with the full evidence. Reduce the risks and convergence_map entries to one-line pointers ('E-006 subject/moment correction — see Phase 1 step 8'). Keep the code_references citations, since those are the verification ledger, but drop the restated rationale from them.
- **reviewer:** meta-audit

### M-08

- **id:** F8
- **title:** Two scope risks were dropped by all three planners and not recovered by the merge, one of which is load-bearing for Phase 1's format decision
- **severity:** minor
- **confidence:** high
- **category:** completeness-drop
- **location:** Merged plan risks (19 items); scope PROJECT_SCOPE.md:293-294 (risk 11) and :308-309 (risk 16)
- **problem:** Scope risk 11 — 'The format is pinned by every later entry and is being designed from retrospective examples rather than a real mid-build parking event. Mitigation is cheapness, not foresight' — is absent from the merged risks, from all three proposals, and from the plan's Phase 1 format step. It is the reason goal 2 says 'Keep the field set minimal so a revision at entry six is an edit, not a migration', and it is the argument a cold implementer needs when tempted to add a seventh field. Scope risk 16 (permanent maintenance: one more root document, one more test to keep green, one more file every doc sweep considers) is likewise absent. Because no planner raised either, this is a merge-completeness gap rather than a dedup failure — but the merged plan is the cold-handoff document, and the scope's risk list is part of what it consumes.
- **proposed_fix:** Add both to the merged risks list. Also add one sentence to the Phase 1 header step: state in ESCALATIONS.md's own header that the six-field format is deliberately minimal and was designed from retrospective examples, so revising it at entry six is expected and is an edit, not a migration — which is what makes the cheapness mitigation actually available to the next worker.
- **reviewer:** meta-audit

### M-09

- **id:** F9
- **title:** 'Six required fields' over five bullet names is restated without ever resolving the arithmetic in the constant
- **severity:** minor
- **confidence:** medium
- **category:** clarity
- **location:** Merged plan phases[1] step 3 ('PIN THE FORMAT, six required fields, exactly' followed by five bullets); phases[2] step 3 (`REQUIRED_FIELDS`, five names) and step for AC 8; phases[2] acceptance ('passing all six field guards')
- **problem:** The plan says 'six' throughout while listing five `- **Field:**` bullets. The sixth is the heading id, per AC 8 ('all six required fields — Bears on:, Parked:, Assumed:, Source:, Status:, and a title with an id matching ^E-d{3}$'). The merge inherits the scope's ambiguity and compounds it by naming the constant `REQUIRED_FIELDS` while it holds five bullet names, then asserting 'all six field guards' against it. An implementer counting to six from the bullet list will invent a sixth bullet — precisely the F-26 class of error (a field required by the tests but absent from the pinned format) that the scope's blocker finding was raised about.
- **proposed_fix:** State it once, explicitly: 'six guards = one heading id + five bullet fields'. Rename the constant `REQUIRED_FIELD_BULLETS = frozenset({'Bears on','Parked','Assumed','Source','Status'})` and assert the id separately, so the count is unambiguous at the point of implementation.
- **reviewer:** meta-audit

### M-10

- **id:** F10
- **title:** Plan-added proof procedures and an API-shaping refactor constraint are presented as blocking acceptance rather than as plan-added rigor
- **severity:** minor
- **confidence:** medium
- **category:** scope-creep
- **location:** Merged plan phases[2] acceptance bullet 7 (copy queue to tmp_path and mangle a field); phases[3] acceptance bullet 2 and phases[3] step 6 (copy each skill file to tmp_path, delete the bullet, and 'Factor the check as a small pure function taking TEXT, not a path, so this is possible')
- **problem:** None of these appears in the scope's core, folded, or gated tiers. The scope's ACs 4, 14, 15 and 16 require the non-vacuity guard and three substring tests to EXIST and be green; they do not require a manual break-and-observe ceremony for each, nor do they dictate the seam check's signature. The procedures are cheap and defensible rigor, and the read-only-git rationale (test_layering.py:12-16, verified) is sound — but the merge states them as acceptance criteria, which makes them gating, and the Phase 4 refactor constraint additionally shapes the module's public API for a reason no criterion requires. This is the one place the merge adds work beyond the decided tiers.
- **proposed_fix:** Demote all three to a 'Recommended verification (plan-added, not scope)' note under each phase's steps, and remove them from the acceptance bullets so a phase cannot be blocked on rigor the scope did not buy. Keep the pure-function-taking-TEXT recommendation as a suggestion with its rationale, not as a constraint.
- **reviewer:** meta-audit

### M-11

- **id:** F11
- **title:** Seven code_references entries are measurements, not file:line citations, diluting the verification ledger
- **severity:** nit
- **confidence:** high
- **category:** clarity
- **location:** Merged plan code_references, refs: 'ROADMAP.md — id discriminator, MEASURED 2026-08-15', 'ROADMAP.md — phase headings, MEASURED 2026-08-15', 'requests/feature-requests/_done/1.1-app-shell/ — all four artifact headers', 'docs/decisions/README.md — index count, MEASURED', 'CLAUDE.md — line count, MEASURED 2026-08-15', 'pytest baseline, MEASURED 2026-08-15', 'filesystem probe, MEASURED 2026-08-15'
- **problem:** The code_references block is the plan's citation ledger — the thing a cold implementer spot-checks to decide whether to trust the rest. Mixing seven measurement results into it (all of which I independently reproduced and all of which are correct) means a reader cannot mechanically verify the block by opening files at line numbers; a third of the entries have no line number to open. The measurements are genuinely valuable and honestly labelled; they are simply in the wrong container.
- **proposed_fix:** Move the seven into a separate 'Measurements taken 2026-08-15' block (command run, result, re-run instruction), leaving code_references as pure file:line citations that can be checked one by one.
- **reviewer:** meta-audit

### M-12

- **id:** F12
- **title:** The plan implies `Source:` citations are covered by the link checker; they are not unless written as markdown links
- **severity:** nit
- **confidence:** medium
- **category:** correctness
- **location:** Merged plan architecture_map ('_dead_links strips a `:442-444` citation suffix at `:57`, so `Source:` citations with line numbers resolve')
- **problem:** Verified in tests/test_request_links.py: `MARKDOWN_LINK = re.compile(r"\\[[^\\]]*\\]\\(([^)]+)\\)")` at line 27 only matches `[text] (target)`. A plain-text field such as `- **Source:** requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:369` is never seen by `_dead_links` at all, so the LINE_SUFFIX strip at :57 is irrelevant to it. The plan's Phase 1 step prescribes `Source: <path with an optional :line suffix>` — plain text — so as written the seed provenance is entirely unchecked, contrary to the architecture note. The claim is harmless in effect but will mislead someone reasoning about how much of the queue is mechanically guarded.
- **proposed_fix:** Either (a) state plainly that `Source:` values are plain text and deliberately not link-checked, and note the tradeoff (they cannot rot loudly), or (b) require them written as markdown links so AC 18 actually covers them — the LINE_SUFFIX strip at :57 means `[PROJECT_SCOPE.md:369] (requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:369)` does resolve. Option (b) is one character of extra syntax per seed and makes the provenance trail self-checking.
- **reviewer:** meta-audit

### M-13

- **id:** F13
- **title:** Fence-stripping in `known_moments` is prescribed but was not part of the cited 38-id measurement
- **severity:** question
- **confidence:** high
- **category:** correctness
- **location:** Merged plan phases[2], the `known_moments` step ('Strip fenced blocks first (`ROADMAP.md` carries a fenced ASCII diagram)') vs architecture_map's 'RE-MEASURED during convergence: exactly 38 unique ids ... 57 non-item leading cells rejected'
- **problem:** I verified ROADMAP.md has exactly one fenced block, at lines 289-295, containing the ASCII phase bar ('Phase 0   Harness   ...'). It has no `|`-leading rows and no `###` headings, so fence-stripping cannot change either the 38/57 id count or the six-heading harvest. My reproduction — which does NOT strip fences — returns exactly 38 accepted and 57 rejected, matching the plan's numbers. So the prescribed implementation differs from the one that produced the cited measurement, even though the answers coincide today. A cold implementer who probes without stripping (as the plan's own Phase 0 one-liner instructs, which also does not strip) and gets 38 has no way to tell whether the parser is right.
- **proposed_fix:** Keep the strip for future-proofing but say so explicitly: 'ROADMAP.md's only fenced block today is the ASCII phase bar at :289-295, which contains no table rows and no headings, so the 38/57 measurement holds with or without stripping. The strip is defensive against a future fenced example.' That reconciles the Phase 0 probe (unstripped) with the Phase 2 implementation (stripped).
- **reviewer:** meta-audit

### M-14

- **id:** F14
- **title:** Phase 5's `_done/` archive move and stage-4 IMPLEMENTATION_REPORT.md were adopted 1-of-3 with no dissent recorded
- **severity:** nit
- **confidence:** medium
- **category:** scope-creep
- **location:** Merged plan phases[5] (Phase 5) steps 4 and 6; files_to_touch IMPLEMENTATION_REPORT.md entry; decisions (no entry covering this choice)
- **problem:** Only the domain-convention planner prescribed writing IMPLEMENTATION_REPORT.md and moving the item into `_done/H1-escalation-queue/`. The code-grounded planner's Phase 5 reconciled statuses but wrote no report; the sequencing planner's Phase 5 handed off to the user and did neither. Verified against the contract: requests/feature-requests/README.md:91 makes IMPLEMENTATION_REPORT.md the STAGE 4 deliverable (i.e. /implement-plan's), and :96-100 makes the archive move the terminal-stage lifecycle action. So a stage-3 plan prescribing both is defensible as hand-off instructions, but the merge presents 1-of-3 convergence as settled with no `decisions` entry and no note that two planners omitted it — the same standard the merge applies rigorously elsewhere (it records the queue-first ordering, the E-000 reservation, the seam-test placement, and the anchor slicing).
- **proposed_fix:** Keep both steps but add a `decisions` entry recording that this was 1-of-3 and why it was kept (the track contract names them), and re-title Phase 5 to make the boundary explicit — e.g. 'Phase 5 — Close out and hand off into stage 4' — so a cold implementer reads the report and the archive move as pipeline lifecycle rather than as additional in-scope build work.
- **reviewer:** meta-audit

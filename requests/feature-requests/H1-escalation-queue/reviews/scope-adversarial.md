# Scoping Panel — Adversarial Findings & Convergence

> Verbatim output of the two adversaries, plus the merge step's convergence
> map. Kept unfiltered — including findings later judged overstated.

## Convergence map

*Where two or more scopers independently agreed — the highest-signal material.*

- - **theme:** INERTNESS is the feature-killing risk, and it is the same shape as ops/README.md's 'inert until it is re-applied' failure for branch-protection.json
  - **scopers:** - fit
    - ambitious
    - minimalist
  - **why_high_signal:** Three independent lenses — including the minimalist, whose instinct is to cut wiring — all reached the same conclusion and all cited the same repo artifact for it. That unanimity plus a shared citation is the strongest signal in the panel. It is also the risk with no test: a structural guard proves entries are well-formed and can never prove anyone parked anything, which is why the wiring tier is the headline gated decision and why the request's own observable signal has to be written as user-run.
- - **theme:** Root ESCALATIONS.md, not docs/ — discoverability IS the mechanism
  - **scopers:** - fit
    - ambitious
    - minimalist
  - **why_high_signal:** Unanimous, with the same argument reached three ways: the three hypotheses failed precisely by living somewhere nobody looks, so a queue one directory deep is a queue nobody opens. ROADMAP.md:197 names the bare filename, which implies root. The only cost any scoper found is a sixth root document, and all three judged that acceptable. Effectively settled — gated only because the root-document count is a taste call this repo has been deliberate about.
- - **theme:** Resolved entries STAY with a resolution pointer, mirroring the ADR-immutability ethos
  - **scopers:** - fit
    - ambitious
    - minimalist
  - **why_high_signal:** The request explicitly offered this as an adjacent question scoping could fold in or reject, and all three folded it in, all three citing docs/decisions/README.md:26-31. Two independently proposed the `## Open` / `## Resolved` split as the mechanism that keeps the open list short without building the deferred archive. Convergence on both the rule AND its implementation is unusually strong.
- - **theme:** The boundary against the mechanisms that already exist is the load-bearing deliverable, and it must live in the queue's own header — not only in the scope
  - **scopers:** - fit
    - ambitious
    - minimalist
  - **why_high_signal:** All three identified the same failure (two overlapping places to look), all three rejected the widest option in Open Question 1, and all three concluded the header — not the file, not the test — is what prevents it. They differed only on the count of existing mechanisms (fit found five, ambitious three, minimalist two), which sharpens rather than weakens the point: the register landscape is already confusing enough that three careful readers enumerated it differently.
- - **theme:** Widen the moment vocabulary rather than adding an `unscheduled` escape hatch
  - **scopers:** - ambitious
    - minimalist
  - **why_high_signal:** The two scopers furthest apart on scope converged on the same middle answer to Open Question 3, for the same reason: hard-requiring an item id creates pressure to mis-file under whatever row is nearest, which corrupts the drain WHILE LOOKING CORRECT — a worse failure than an honest hatch. The minimalist arrived at it by trying to write the serviceability-gate seed and finding no honest row; the ambitious by reasoning about the failure mode. Agreement from opposite directions, with a concrete falsifying example.
- - **theme:** The parser is fiddlier than it looks — ROADMAP.md mixes table shapes and the guard can go silently vacuous
  - **scopers:** - fit
    - ambitious
    - minimalist
  - **why_high_signal:** All three flagged it and each found a different failure path: fit found the empty-leading-cell and [OPEN-N] tables that a loose regex would swallow; ambitious found the harness table's SIXTH Blocks column that a positional parser silently drops (quietly rejecting a legitimate H1 entry); the minimalist found that an empty parse result makes the whole guard `assert not []` and pass forever. Three distinct, real, non-overlapping bugs in one small parser — which is why the non-vacuity and exact-set criteria are non-negotiable.
- - **theme:** Skill-level write wiring is the real payoff and also the thing most likely to blow the scope behind a binding Blocks cell
  - **scopers:** - fit
    - ambitious
    - minimalist
  - **why_high_signal:** All three tiered it OUT of core despite the ambitious scoper calling it 'the real payoff'. The shared reasoning is strong: it edits decision logic across four-plus SKILL.md files, it pre-commits a write protocol before a single entry has been written by hand, and ROADMAP.md:197's Blocks: 1.3 means every hour spent on it is an hour the ledger's correction model waits. When the ambitious lens declines to fold its own headline enhancement, that is a real verdict rather than caution.
- - **theme:** CLAUDE.md's line budget is a constraint on this item, and the instrument that measures it is broken
  - **scopers:** - fit
    - minimalist
  - **why_high_signal:** Fit read the budget as 19 lines of headroom (181 against 200); the minimalist measured the file at 221 real lines and traced the discrepancy to update-docs/SKILL.md:76-77's prescribed command, which uses `Measure-Object -Line` and counts zero for blank lines. I verified both numbers. The disagreement itself is the finding: two careful agents read the same budget and got opposite answers because the documented instrument lies. It bounds this item's CLAUDE.md edit to one line and it is a separate bugfix request.

---

## Adversary summaries


### Adversary 1

- **adversary:** fit-ac
- **summary:** I resolved every integration point the merged scope cites. The repo-fit verdict is essentially sound and unusually well-grounded: ROADMAP.md:197 (H1 row, `Blocks: 1.3`, IN-PROGRESS), ROADMAP.md:200-204, ROADMAP.md:217-222, ADR 0010:63-66 and :125-128, docs/decisions/README.md:20/26-34, ops/README.md:30-37, diagnose-bug/SKILL.md:132-142 and :161-162, make-feature-request/SKILL.md:74-92, commit/SKILL.md:28-29, update-docs/SKILL.md:76-78 and :100-101, requests/README.md:6-12, requests/feature-requests/README.md:34-40 and :63-79, and every cited line in tests/test_repo_structure.py, tests/test_layering.py and tests/test_request_links.py all resolve exactly as claimed. The N/A contract findings are correct by filesystem probe: no `datasets/`, `careers/`, `rulesets/`, `lib/`; `src/rpg_core/` is `__init__.py` alone; ten ADRs. I independently reproduced three of the scope's measured claims: `_dead_links()` returns `[]` for all five root documents; `(Get-Content CLAUDE.md).Count` = 221 vs `Measure-Object -Line` = 181; `[OPEN-10]` is cited at ROADMAP.md:334 and defined nowhere (GAME_DESIGN.md §8 runs [OPEN-1]..[OPEN-9], and [OPEN-1] is struck through as SETTLED at :292).

Three things break. (1) FRAMING: the request's headline pain is that a worker mid-build has no third move; nothing in core creates that move. The only CLAUDE.md edit lands inside the project-map fence, which announces a file's existence, not a permission to park — so goal 1 is asserted, not delivered, and no acceptance criterion touches it. (2) EVIDENCE: one of the "four verified decisions already stranded in `_done/1.1-app-shell/`" is not a parked decision at all — PROJECT_SCOPE.md:319 sits under the header "**Folded in (all of them — Decision 7)**" at :316; it shipped. And the MEASURED claim that "CLAUDE.md and the FEATURE_REQUEST both claim §8 parks ten questions" is false for CLAUDE.md, whose three "ten" mentions (:57, :90, :111) all refer to ADRs, of which there are ten. In a repo where `measured` is a load-bearing word, a mislabelled claim is the finding. (3) ACCEPTANCE: the criteria are strong in shape — non-vacuity, red-and-green, failure-message-as-record are all genuinely testable — but four are not checkable as written. "The phase names" in an *exact-set* assertion is unenumerated and its normalization undefined; the negative assertion misses ROADMAP.md:41-51, a third table shape whose leading cells are bold surface names rather than empty or `**[OPEN-N]**`; the tmp_path proof fabricates a queue but not a roadmap, so the "green" case is coupled to live ids; and the criteria are not tier-tagged, so two of them assert cheap-fold deliverables the user may drop. The non-goals are mostly honest and the inertness risk is named without flinching — but non-goal 7 (no rationale in entries) is breached by a core deliverable, and the "REGISTER-BOUNDARY GUARD" name overclaims what `no "[OPEN-" in a title` can prove.


### Adversary 2

- **adversary:** scope-completeness
- **summary:** Adversary 2 — scope discipline and completeness. I verified the merged scope against the repo: every path, line citation, and measurement it leans on. Most of the grounding holds (H1 row at ROADMAP.md:197 with Blocks: 1.3; ADR 0010:125-128 naming H1; src/rpg_core containing only __init__.py; no datasets/, careers/, rulesets/; the four stranded 1.1 decisions at PROJECT_SCOPE.md:319/369/370 and IMPLEMENTATION_PLAN.md:859; the [OPEN-10] orphan; CLAUDE.md 221 real lines vs 181 by the skill's prescribed command; all five root docs returning [] from _dead_links). The fit verdict of "clean" is right and the two named frictions are real.

The problems are in the tiers and in what got left out. (A) OVER-REACH: the acceptance criteria have grown past the deliverable. AC 2's exact-38-id set assertion turns every future roadmap row into a red test in an unrelated PR, and it maximizes exactly the "weaken the assertion" pressure the scope's own renumbering risk warns about. The test_request_links.py root-wide extension permanently widens a shared guard's blast radius over five documents outside this feature, and it is folded in on a "measured clean today" argument while an equally adjacent measured defect (the broken Measure-Object -Line budget command) is pushed out to its own request — inconsistent standard. The summary silently promotes four cheap_fold recoveries into core by claiming "seven seed entries" when tiered_scope.core lists three.

(B) BLIND SPOTS, three of them load-bearing. The scope's own headline deliverable — the register boundary — misses a register: DESIGN.md §3 "Architecture notes not yet ADRs" (verified at DESIGN.md:99-113) is the closest overlap of all and appears in neither the header spec nor AC 9. The parser's negative assertion (AC 3) is factually wrong about the repo: the v1 scope tables' ROWS lead with `**Creation** — …`, not an empty cell — only the header row is empty — so the stated "leading-cell-anchored pattern separates all four shapes" is unverified, and there is a fifth table (the application table at :41-51) never enumerated. And the drain has an unnamed hole: an Open entry whose moment reaches DONE is permanently invisible, because both surfaces that could catch it (/commit, /update-docs) were dropped and the recommended read seam only fires when a NEW item enters intake.

Two internal contradictions block implementation as written: `Source:` is required by AC 8 but absent from the five-field format the core pins (and the "stay at five" rule is the stated mitigation for format churn), and above_and_beyond's core item edits GAME_DESIGN.md §8 while the non-goals and gated decision 5 both declare §8 off limits. I also found one measured doc-drift defect in a file this scope edits that the scope did not notice: CLAUDE.md:216 still says "Nine decisions are settled" while :57, :90, and :111 all say ten and ten exist on disk.

Net: the shape is right, the gating on the wiring question is honest and well-argued, and the recommendation to defer write-side skill wiring is correct. But the acceptance criteria need trimming in two places, three contradictions need resolving before a planner can act, and four completeness gaps need naming.


---

## Adversary findings (all 48, verbatim)


### F-01

- **id:** A1-01
- **title:** Goal 1 ("make the third move exist") has no core deliverable and no acceptance criterion
- **severity:** blocker
- **confidence:** high
- **category:** fit
- **location:** goals[0]; tiered_scope.core (CLAUDE.md bullet); acceptance_criteria (all 17)
- **problem:** The request's problem statement (FEATURE_REQUEST.md:15-18) is that a worker facing a judgment call has exactly two moves and the scope's first goal claims to create the third. But nothing in core creates it. Core delivers a file, a boundary header, a format, a guard, and retrospective seeds. The only CLAUDE.md edit is "one line in CLAUDE.md's project-map fenced block" — verified, that fence is CLAUDE.md:51-67, a directory map whose lines say what a path *is*, not what an agent may *do*. The behavioural rules live in a separate section (CLAUDE.md:129-160, "Project conventions"). A map line announces the file exists; it never tells a worker mid-build that parking is permitted and non-blocking. Meanwhile the write side is explicitly out (the request's "Not a change to how the pipeline skills behave") and every wiring option is gated. So goal 1 is achieved by no deliverable in any tier, and none of the 17 acceptance criteria mentions it. That is the exact shape of the INERTNESS risk the scope itself names — but stated as an achieved goal rather than an open one.
- **proposed_fix:** Promote one line into CLAUDE.md's "Project conventions" section (not the map fence): "Hit a judgment call mid-build? Record it in ESCALATIONS.md with the assumption you took, and keep going — parking never blocks." This is a doc line, not a change to any skill's decision logic, so it does not breach the request's Explicitly-out. Add a core acceptance criterion asserting that string's presence, in the tests/test_repo_structure.py:276-284 substring idiom. If the user declines the extra CLAUDE.md line (see A1-15 on the budget), restate goal 1 honestly as "make the third move POSSIBLE and recorded — making it KNOWN is gated with the wiring".
- **adversary:** fit-ac


### F-02

- **id:** A1-02
- **title:** PROJECT_SCOPE.md:319 is a shipped fold, not a stranded parked decision — the "four recovered decisions" is three
- **severity:** major
- **confidence:** high
- **category:** fit
- **location:** tiered_scope.cheap_folds ("RECOVER THE FOUR STRANDED DECISIONS"); above_and_beyond[3]; grounding_pointers[5]; summary
- **problem:** I read the cited lines. requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:316 is the header "**Folded in (all of them — Decision 7)**", and :318-319 is a bullet under it: "SPA history fallback for unmatched non-`/api` paths, paired with the AC 7 JSON-404 guard. It is what stops item 1.10's router from being a breaking change." That is a decision MADE and SHIPPED, whose forward reference to 1.10 explains why 1.10 will have nothing to decide. The scope records it as "the client-side router seam (:319, moment 1.10)" — a parked decision. Parking it would put a non-question in the queue on day one, which is precisely the "shadow backlog" failure non-goal 6 warns about, and it inflates the evidence base the scope leans on hardest ("four decisions with explicitly named moments", "moves the feature from plausible to proven"). The other three check out: :369 and :370 are `drop`-tier rows carrying explicit future moments ("right moment is 1.8", "the seam it slots into at 1.8"), and IMPLEMENTATION_PLAN.md:859-861 is the `.gitignore:63` `build/` item, verified — .gitignore line 63 is literally `build/`.
- **proposed_fix:** Drop the :319 item. Restate the recovery as THREE entries (PROJECT_SCOPE.md:369, :370, IMPLEMENTATION_PLAN.md:859-861) and correct the count everywhere it appears. If a fourth is wanted, PROJECT_SCOPE.md:373 ("Three-way version parity test — `app/package.json`'s version is meaningless for a private SPA. Mark it private, fix the version at a placeholder") is a genuine parked call with an unstated moment, and naming its moment would be an honest exercise of the format. Note separately that IMPLEMENTATION_PLAN.md:861 already prescribes its own disposition — "Should become an intake item rather than being rediscovered at 2.1" — so the queue entry should point at that, not replace it.
- **adversary:** fit-ac


### F-03

- **id:** A1-03
- **title:** A MEASURED claim is false: CLAUDE.md nowhere says §8 parks ten questions
- **severity:** major
- **confidence:** high
- **category:** framing
- **location:** tiered_scope.cheap_folds ("RECORD [OPEN-10] AS A SEED ENTRY"); gated_decisions[4]
- **problem:** The scope states, under the label MEASURED, that "`CLAUDE.md` and the FEATURE_REQUEST both claim §8 parks ten" questions. I grepped CLAUDE.md: its only reference to the mechanism is line 80, "`[OPEN-N]` items are parked deliberately; each has a phase that answers it" — no count. Its three "ten" occurrences are :57 ("ADRs — ten settled calls"), :90 ("Ten ADRs cover save decryption...") and :111 ("All ten are ADRs"), all correct, since docs/decisions/ holds 0001-0010. Only FEATURE_REQUEST.md:52-53 makes the ten-questions claim. Separately, the scope's counter-claim "It parks nine" is right on id count but omits that [OPEN-1] is SETTLED and struck through (GAME_DESIGN.md:292), so §8 defines nine ids of which eight are live, and ROADMAP.md's table lists nine rows ([OPEN-2]..[OPEN-10]) of which one has no definition. This repo treats measured/verified/inferred as different claims (CLAUDE.md:161-165); a false statement carrying the strongest label is a bigger problem than the fact it gets wrong.
- **proposed_fix:** Restate: "MEASURED — ROADMAP.md:334 cites [OPEN-10]; GAME_DESIGN.md §8 defines [OPEN-1] through [OPEN-9] ([OPEN-1] settled at :292, so eight live); a grep over tracked *.md finds no [OPEN-10] definition. FEATURE_REQUEST.md:52-53 asserts §8 parks ten. CLAUDE.md makes no count." Then note the seed entry should record BOTH the orphan and the stale count in the request, since fixing the request's prose is also not this item's job.
- **adversary:** fit-ac


### F-04

- **id:** A1-04
- **title:** Acceptance criteria are not tier-tagged; at least two assert cheap-fold deliverables
- **severity:** major
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[11] (test_core_documents_exist) and [12] (test_request_links root extension), against tiered_scope.cheap_folds
- **problem:** The 17 criteria read as one flat contract, but they mix tiers. Criterion 12 requires `test_core_documents_exist` (tests/test_repo_structure.py:243-247) to include ESCALATIONS.md — that is tiered as a cheap_fold and is a live dissent in the scope's own text. Criterion 13 requires tests/test_request_links.py's SCANNED_TREES (:24) extended to root-level `*.md` — also a cheap_fold, and it is the ONLY thing that makes criterion 13's stated purpose ("every relative pointer an entry carries is verified to resolve") true. If the user drops either fold, the acceptance panel in stage 4 has criteria it cannot satisfy and no way to tell they were optional. The panel's contract is exactly "a cold agent can run one command and get a pass or fail" (requests/feature-requests/README.md:65-66) — that requires knowing which commands are in scope.
- **proposed_fix:** Tag every criterion with the tier that produces it: `[CORE]`, `[FOLD: root-link-check]`, `[FOLD: core-documents]`, `[GATE: read-seam]`. State once, above the list, that FOLD/GATE criteria bind only if the user adopts that item, and that dropping a fold drops its criterion rather than failing it.
- **adversary:** fit-ac


### F-05

- **id:** A1-05
- **title:** "Exact expected set" is not exact: "the phase names" is unenumerated and its normalization undefined
- **severity:** major
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[1] (ROADMAP-PARSER EXACTNESS)
- **problem:** The criterion says the parsed set must equal an exact expected set, then enumerates only the 38 item ids (which I verified: 0.1-0.6, 1.1-1.11, H1-H2, 2.1-2.8, 3.1-3.5, 4.1-4.6 = 38) and appends "plus the phase names and the literal `post-v1`". "The phase names" is undefined in every dimension that matters for an equality assertion. ROADMAP.md's headers read `### Phase 0 — Harness — **DONE**` (:144), `### Phase 4 — Career → **v1** — **NOT STARTED**` (:261), and `### Post-v1` (:277). Is the moment "Phase 0", "Phase 0 — Harness", or "Harness"? Is it case-sensitive? Is `post-v1` normalized from the `### Post-v1` heading or from the four table cells at :328/:330/:333/:334? And there is a fifth header, `#### Harness — Phase 1` at :193, which a header regex keyed on "Phase" would either swallow or must explicitly exclude. An exact-set criterion whose set cannot be written down is not testable.
- **proposed_fix:** Write the set literally in the criterion: the 38 ids as strings, plus exactly `{"Phase 0","Phase 1","Phase 2","Phase 3","Phase 4","post-v1"}`, matched case-insensitively after stripping the em-dash suffix, and add an explicit sub-assertion that `#### Harness — Phase 1` (ROADMAP.md:193) contributes nothing.
- **adversary:** fit-ac


### F-06

- **id:** A1-06
- **title:** The negative assertion misses a third non-item table shape — ROADMAP.md:41-51
- **severity:** major
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[2] (PARSER NEGATIVE ASSERTION); risks ("PARSER BRITTLENESS", which enumerates four shapes)
- **problem:** The criterion proves that exactly two non-item shapes contribute zero ids: rows with an empty leading cell (ROADMAP.md:25-35, :77-84) and rows leading with `**[OPEN-N]**` (:326-334). Both verified. But ROADMAP.md:41-51 is a third shape the criterion does not name: the in-scope application table, whose leading cells are non-empty, non-bracketed bold labels — `| **Career management** | Create, list, view, archive...`, `| **Player state** | ...`, `| **Game log** | ...`. A regex that rejects empty cells and `[OPEN-` but accepts bold leading cells satisfies the criterion as written while admitting "Career management" as a valid moment. The scope's own risk entry lists four shapes and still misses this one (it counts the harness table's sixth column as the fourth). Since the scope calls the negative assertion "non-negotiable" precisely because a loosened regex would widen silently, the omission defeats the purpose.
- **proposed_fix:** Add to the criterion: "and rows whose leading cell is a bold prose label (the application-surface table at ROADMAP.md:41-51) contribute ZERO ids — assert `parse(ROADMAP.md)` contains none of `Career management`, `Player state`, `Game log`, `Box-score entry`, `Spend flow`, `Badge loadout`, `Progression history`, `Milestone tracker`, `Career comparison`."
- **adversary:** fit-ac


### F-07

- **id:** A1-07
- **title:** The tmp_path proof fabricates the queue but not the roadmap, so the "green" case is not hermetic
- **severity:** major
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[4] (PROVEN RED AND GREEN AGAINST tmp_path)
- **problem:** The criterion specifies "a fabricated queue naming moment `9.9` returns exactly that one violation; a fabricated queue naming `1.3`, `H2`, `Phase 3`, and `post-v1` returns none." Only the queue is fabricated. For the green case to pass, the parser must be reading the REAL ROADMAP.md — which means the hermetic proof is coupled to live roadmap ids, and the day 1.3 or H2 is renamed the *proof* goes red alongside the *real assertion*. That is the ROADMAP RENUMBERING TAX the scope names as a risk, landing in the one test that was supposed to be insulated from it. It also breaks the tests/test_layering.py idiom the criterion invokes: `web_imports_under(root)` (:38) takes the tree as an argument precisely so the proofs at :85-100 touch nothing real.
- **proposed_fix:** Specify the guard as a two-argument pure function — `violations(queue_path: Path, roadmap_path: Path) -> list[...]` — and require both files fabricated under tmp_path in the red and green proofs, with a small fake roadmap table containing `1.3`, `H2`, `### Phase 3 — Season`, and `post-v1`. The real assertion (criterion 5) then calls it with REPO_ROOT paths, which is the only place live ids appear.
- **adversary:** fit-ac


### F-08

- **id:** A1-08
- **title:** The format encodes state twice — `Status:` field and `## Open`/`## Resolved` sections — which the scope's own reasoning rejects elsewhere
- **severity:** major
- **confidence:** high
- **category:** scope-creep
- **location:** tiered_scope.core (entry format, "RESOLVED ENTRIES STAY"); acceptance_criteria[7] (FIELD AND VOCABULARY GUARDS)
- **problem:** Core pins five fields including `Status:` with "a closed vocabulary", AND a `## Resolved` section at the foot that resolved entries move into. Those are two representations of the same fact that can disagree — an entry marked `Status: resolved` sitting under `## Open`, or vice versa. The scope drops the `Surfaced by:` field for exactly this reason: "Two fields that must agree is a pure drift source with no new information." The same argument applies here and is not made. Compounding it, the criterion requires "every `Status:` value is drawn from a closed vocabulary declared in the test" without ever naming the vocabulary, so the criterion cannot be checked without a decision the scope has not taken.
- **proposed_fix:** Pick one representation. Recommended: sections are the truth (an entry's state is where it lives), and `Status:` is replaced by an optional `Resolved by:` pointer carried only in the `## Resolved` section — which also drops the format to four fields on an open entry, reinforcing the stated five-field ceiling. If both are kept, enumerate the vocabulary literally in the criterion (e.g. exactly `{open, resolved}`) and add a criterion asserting section membership and `Status:` agree for every entry.
- **adversary:** fit-ac


### F-09

- **id:** A1-09
- **title:** Non-goal 7 ("entries do NOT carry a decision's rationale") is breached by a core deliverable
- **severity:** major
- **confidence:** high
- **category:** scope-creep
- **location:** non_goals[6] vs goals[4] and tiered_scope.core ("SEED MIGRATION")
- **problem:** Non-goal 7 says an entry "names the question, the assumption, and where the answer will be recorded; the rationale lives in the ADR, request, or commit it points at", and attributes it to the request (FEATURE_REQUEST.md:61-62 does park it). But goal 5 and the core seed-migration bullet both require that ROADMAP.md:220-222's substantive observation — that "serviceable" is already a v1 constraint in both directions (ROADMAP.md:53-55) and is nowhere defined or tested — move INTO the serviceability-gate entry, explicitly so a "mechanical copy of three titles" doesn't drop it. That observation is the argument for why the gate might be needed: it is rationale, and it is the whole reason the entry is interesting. The scope therefore has a non-goal its core violates, with no reconciliation.
- **proposed_fix:** Loosen non-goal 7 to what is actually intended: "Entries carry no ADR-length argumentation. One sentence of context is permitted and expected — the assumption's justification, the constraint that makes the question live. The full argument belongs in the ADR, request, or commit the entry points at." Then the serviceability observation fits inside the rule instead of against it. Alternatively leave the observation in ROADMAP.md §v1 where it is already true, and have the entry cite `ROADMAP.md:53-55` — but that leaves ROADMAP.md carrying half the content, which criterion 11 forbids.
- **adversary:** fit-ac


### F-10

- **id:** A1-10
- **title:** Seed count is internally inconsistent — the summary says seven, the tiering implies three or eight
- **severity:** major
- **confidence:** high
- **category:** completeness
- **location:** summary ("seven seed entries") vs tiered_scope.core (three hypotheses) vs tiered_scope.cheap_folds (four strays + [OPEN-10])
- **problem:** The summary states "Core is therefore the file plus its boundary header, the format, the guard, and seven seed entries — the three ROADMAP.md:217-222 hypotheses plus four verified decisions already stranded in _done/1.1-app-shell/". But the tiering puts only the three hypotheses in core; the four strays are a cheap_fold and the [OPEN-10] orphan is a separate cheap_fold. So core contains three seeds, not seven, and the full adopted set would be eight, not seven — and per finding A1-02 one of the four strays is not a parked decision, so the true numbers are three in core and seven total. The risks section then leans on "the seven seed entries" as the mitigation for the request's observable signal not firing, attributing to core a mitigation core does not contain. Acceptance criterion 10 proves only the three.
- **proposed_fix:** State the seed inventory once, as a table with a tier column: three hypotheses [CORE]; two recovered `drop`-row decisions from PROJECT_SCOPE.md:369/:370 [FOLD]; the `.gitignore` item from IMPLEMENTATION_PLAN.md:859-861 [FOLD]; the [OPEN-10] orphan [FOLD]. Fix the summary and the risk mitigation to reference the CORE count, and add a fold-tagged acceptance criterion for each fold's entries.
- **adversary:** fit-ac


### F-11

- **id:** A1-11
- **title:** "REGISTER-BOUNDARY GUARD" overclaims — it guards id reuse, not the boundary
- **severity:** minor
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[8]
- **problem:** The criterion is named as the mechanical guard for the boundary the fit section calls "the most expensive failure available here", but what it asserts is that no entry title contains the literal `[OPEN-`. An entry titled "Does the affinity table replace the other anti-convergence levers?" — a verbatim duplicate of [OPEN-2] (GAME_DESIGN.md:296, ROADMAP.md:326) — passes it. The scope elsewhere states plainly that "nothing mechanical can distinguish a build-time decision from an engineering question", so the criterion's name contradicts the fit section's own analysis. The second half of the criterion (the header must name GAME_DESIGN.md, DESIGN.md, the Stage plan, and /diagnose-bug's Escalation) is a clean substring test and is fine.
- **proposed_fix:** Split and rename. "[CORE] ID-REUSE GUARD: no entry title contains `[OPEN-` — an entry must not re-badge a GAME_DESIGN.md §8 question under a second id." and "[CORE] BOUNDARY HEADER PRESENT: ESCALATIONS.md contains the strings `GAME_DESIGN.md`, `DESIGN.md`, `Stage plan`, and `diagnose-bug`." State explicitly that the boundary itself is enforced by human reading of the header, not by a test — the scope already believes this and should say it in the criteria rather than only in the risks.
- **adversary:** fit-ac


### F-12

- **id:** A1-12
- **title:** Criterion 11 ("no duplicate source") is a negative assertion with no strings named
- **severity:** minor
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[10]
- **problem:** "a test asserts `ROADMAP.md` no longer enumerates the three hypotheses inline — the 'Parked, not scheduled' paragraph is reduced to a pointer line containing `ESCALATIONS.md`." "No longer enumerates" cannot be turned into an assertion without knowing which strings must be absent, and "reduced to a pointer line" cannot be checked without knowing what the pointer line says. This is the criterion the scope calls "the one that stops the migration leaving two sources that drift" — the load-bearing one is the vaguest.
- **proposed_fix:** Name the strings. "[CORE] a test asserts `ESCALATIONS.md` appears in ROADMAP.md, and that the literals `design/UX specialist` and `autonomous stage dispatcher` (present today at ROADMAP.md:217-218) do NOT. Failure message: 'ROADMAP.md still enumerates a migrated hypothesis — the queue is now the source, and two sources drift.'" Note that `serviceability gate` cannot be asserted absent if the §v1 constraint text at ROADMAP.md:53-55 is retained, so choose the two unambiguous strings.
- **adversary:** fit-ac


### F-13

- **id:** A1-13
- **title:** The exact-set assertion fights the roadmap's own documented growth convention
- **severity:** minor
- **confidence:** medium
- **category:** risk
- **location:** acceptance_criteria[1]; ROADMAP.md:130-137
- **problem:** ROADMAP.md:130-137 states that H rows are "infrastructure ... added when it's needed rather than up front", and H2 already exists. An exact-set assertion over 38 ids means the next added row — H3, or a new 1.x — turns CI red inside an unrelated PR, with a failure that reads as an escalation-queue defect. The scope's stated justification ("fails loudly on a table reformat instead of silently narrowing") is real but one-sided: it does not distinguish a reformat that breaks the parser from a legitimate row addition, and the obvious fix under time pressure is to loosen the assertion — the exact degradation the scope warns about in the renumbering-tax risk. Status-cell edits are safe (they don't touch the leading cell), so the trigger is row add/remove/rename only, which is infrequent but expected.
- **proposed_fix:** Split the exactness across two targets. Against a FROZEN fixture copy of a roadmap table under `tests/fixtures/`, assert exact-set equality — that catches parser regressions with zero coupling to the live document. Against the live ROADMAP.md, assert (a) the anchors `1.3`, `H1`, `H2` are present, (b) the three negative shapes contribute zero (A1-06), and (c) `len(ids) >= 38`, so narrowing fails loudly while a new row does not.
- **adversary:** fit-ac


### F-14

- **id:** A1-14
- **title:** The `Blocks: 1.3` urgency is over-weighted and is used to justify three separate deferrals
- **severity:** minor
- **confidence:** high
- **category:** framing
- **location:** risks ("SCOPE CREEP HAS A BINDING COST HERE"); gated_decisions[1]; summary
- **problem:** The scope invokes ROADMAP.md:197's `Blocks: 1.3` as the closing argument against the write-side wiring, against the mirror guard, and in the summary ("every gated item adopted delays the ledger's correction model"). But ROADMAP.md:179-180 shows 1.2 `career-ledger` is NOT STARTED and 1.3 `correction-by-append` Needs 1.2. So H1 is not on the critical path today — 1.2 is, and H1 could take a week without moving 1.3's start date by a day. The scope does concede this once ("there is genuine slack — but slack is not a licence"), then continues to use the binding cell as the primary cost argument. The effect is to pressure the reader toward option (a) with a cost that is currently zero, when the scope's own headline risk says option (a) produces an inert file.
- **proposed_fix:** Quantify the slack once, plainly, in the risk entry and in gated_decision 1: "H1 gates 1.3 only after 1.2 lands. 1.2 is NOT STARTED (ROADMAP.md:179) and is a substantial item, so the schedule cost of an extra day on H1 is currently zero. The argument against the write-side wiring must stand on its own merits — the write protocol is being designed from imagination — not on the Blocks cell."
- **adversary:** fit-ac


### F-15

- **id:** A1-15
- **title:** The CLAUDE.md budget criterion is ambiguous ("versus HEAD") and misdescribes an already-blown budget as unworsened
- **severity:** minor
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[16]
- **problem:** Two problems. (1) "increases by at most 1 versus HEAD" is not a single runnable check on a branch with more than one commit — HEAD moves as the branch grows, so a per-commit +1 satisfies it indefinitely. (2) The framing "BUDGET NOT WORSENED BY MORE THAN ONE LINE" implies a budget being respected. The documented budget is `CLAUDE.md` stays **under 200 lines** (.claude/skills/update-docs/SKILL.md:76), and I confirmed the file is 221 real lines. So the criterion sanctions adding to a file already 21 lines over, and does so in the same scope that identifies the measuring instrument as broken. That is a defensible call, but the criterion's wording hides it.
- **proposed_fix:** Make it absolute and honest: "[CORE] `(Get-Content CLAUDE.md).Count` is at most 222. NOTE: the documented budget (.claude/skills/update-docs/SKILL.md:76) is under 200 lines and the file is already at 221 real lines; the prescribed measuring command reports 181 because `Measure-Object -Line` discounts blank lines. This item accepts +1 knowingly and does not attempt the cut, which belongs with the bugfix request for the measuring command." If finding A1-01's rules line is adopted, this becomes at most 223 and should say so.
- **adversary:** fit-ac


### F-16

- **id:** A1-16
- **title:** Inconsistent handling of the "no skill behaviour changes" non-goal — one skill edit gated, another folded silently
- **severity:** minor
- **confidence:** high
- **category:** framing
- **location:** tiered_scope.cheap_folds (diagnose-bug disambiguation line) vs gated_decisions[0] (make-feature-request read bullet)
- **problem:** The request's Explicitly-out says "Not a change to how the pipeline skills behave." The scope routes the make-feature-request/SKILL.md read bullet to the human specifically because "it does edit a skill file, which brushes the request's Explicitly-out" — correct and commendable. But it simultaneously folds, as a cheap_fold requiring no approval, "a one-line disambiguation in ... .claude/skills/diagnose-bug/SKILL.md". That is also an edit to a skill file. The scope's defence ("DISAMBIGUATION ONLY — the functional change of giving the hand-off a destination is gated below") is sound, but it is buried inside the fold's own text rather than stated as the rule that separates the two cases.
- **proposed_fix:** State the distinction once, in non_goals: "A skill edit that changes what an agent DOES is gated. A skill edit that is purely descriptive prose — a name disambiguation, a cross-reference — is folded. The diagnose-bug line is the second kind; the make-feature-request bullet is the first, because it adds a step to a checklist an agent follows." Then both dispositions are readable from one rule rather than from two separate justifications.
- **adversary:** fit-ac


### F-17

- **id:** A1-17
- **title:** Goal 9 promises "one file with one section"; the proposed format has no per-moment sectioning
- **severity:** nit
- **confidence:** high
- **category:** framing
- **location:** goals[8] vs tiered_scope.core (entry format, `## Open` / `## Resolved`)
- **problem:** Goal 9: "Leave a cold agent picking up any roadmap item able to answer 'what was parked against this?' from one file with one section." The format core actually specifies is heading-blocks with a `Bears on:` field, grouped into `## Open` and `## Resolved`. There is no section per moment. A cold agent answers the question by scanning or grepping `Bears on: 1.3` across the whole `## Open` section — which is fine and cheap, but it is not what the goal says, and the goal's phrasing could be read as requiring a per-item index the scope never scopes.
- **proposed_fix:** Reword: "...able to answer 'what was parked against this?' from one file with one grep — `Bears on: 1.3`." Optionally add to the boundary header a one-line instruction naming that grep, and sort `## Open` by moment so the scan is also visually grouped.
- **adversary:** fit-ac


### F-18

- **id:** A1-18
- **title:** Criterion 1's docstring half is a human judgment presented as a test
- **severity:** nit
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[0]
- **problem:** "`uv run pytest tests/test_escalations.py -q` is green, AND the module carries a docstring in the idiom of tests/test_repo_structure.py:1-9 / tests/test_layering.py:1-17 explaining why the guard exists." The first clause is a command with a pass/fail. The second is a review judgment — "in the idiom of" and "explaining why" have no mechanical check — bundled into the same bullet, so an acceptance panel would mark the whole criterion green on the pytest run alone. requests/feature-requests/README.md:76-79 requires human-only criteria to be marked user-run so the panel does not claim them.
- **proposed_fix:** Split. "[CORE] `uv run pytest tests/test_escalations.py -q` is green." and "[CORE, mechanical proxy] the module docstring is non-empty and names both `ROADMAP.md` and `ESCALATIONS.md` — asserted by the module's own test." Leave any judgment about idiom quality to the /commit doc gate rather than the acceptance ledger.
- **adversary:** fit-ac


### F-19

- **id:** A1-19
- **title:** Criterion 10 asserts "distinctive strings" without naming them
- **severity:** nit
- **confidence:** high
- **category:** acceptance
- **location:** acceptance_criteria[9]
- **problem:** "`ESCALATIONS.md` contains distinctive strings for all three ROADMAP.md:217-222 hypotheses (serviceability gate, design/UX specialist, autonomous stage dispatcher)." The parenthetical names the concepts, not the literals the test asserts, and the source text at ROADMAP.md:217-218 reads "A serviceability gate for the web UI, a design/UX specialist, and an autonomous stage dispatcher" — the migrated entry titles may legitimately be reworded, at which point the test's strings and the entries diverge and nobody knows which is authoritative. This is the same substring idiom as tests/test_repo_structure.py:260-273, which does name its literal (`"no application code yet"`).
- **proposed_fix:** Name the three literals in the criterion and require the entries to contain them verbatim: `serviceability gate`, `design/UX specialist`, `autonomous stage dispatcher`. Pair with criterion 11's absence assertion on the same strings in ROADMAP.md so the pair reads as one migration proof.
- **adversary:** fit-ac


### F-20

- **id:** A1-20
- **title:** No acceptance criterion covers the recovered strays or the [OPEN-10] seed
- **severity:** minor
- **confidence:** high
- **category:** completeness
- **location:** acceptance_criteria (all) vs tiered_scope.cheap_folds; above_and_beyond[3]
- **problem:** above_and_beyond calls the recovery of the stranded decisions "the enhancement that moves the feature from plausible to proven", and the [OPEN-10] seed "the cleanest possible demonstration of why H1's test matters". Neither has a criterion. If both folds are adopted, an acceptance panel has nothing to run against them; their entries could be omitted, malformed in a way the field guard tolerates, or cite a `Source:` that does not resolve, and every criterion stays green.
- **proposed_fix:** Add fold-tagged criteria: "[FOLD: stray-recovery] ESCALATIONS.md contains entries whose `Source:` fields cite `requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:369`, `:370`, and `IMPLEMENTATION_PLAN.md:859-861`, and `uv run pytest tests/test_request_links.py -q` proves each resolves." and "[FOLD: open-10] ESCALATIONS.md contains an entry whose title includes `[OPEN-10]`" — noting this last one requires the id-reuse guard (A1-11) to exempt a title that is ABOUT the orphan rather than re-badging a live question, which is a real interaction the scope has not spotted.
- **adversary:** fit-ac


### F-21

- **id:** A1-21
- **title:** Choosing a new test module diverges from a bullet the request lists under Non-negotiables
- **severity:** question
- **confidence:** medium
- **category:** fit
- **location:** tiered_scope.core ("tests/test_escalations.py — a NEW module"); FEATURE_REQUEST.md:98-99
- **problem:** FEATURE_REQUEST.md:98-99, under "Constraints / Non-negotiables", reads: "The structural test matches the existing idiom in `tests/test_repo_structure.py`: parse a document, assert against the filesystem, fail with a message that explains the why." The scope reads this as binding the idiom rather than the file, records a minimalist dissent parenthetically, and chooses a new module. I think the scope is right — tests/test_layering.py, tests/test_request_links.py and tests/test_ci_contexts.py are all standalone parser guards, and a pure function proven against tmp_path does not fit test_repo_structure.py, which has no tmp_path fixtures anywhere. But the divergence is from a bullet the request itself filed under Non-negotiables, and it is currently argued in a parenthetical inside a core bullet.
- **proposed_fix:** Promote the reading to an explicit line in the fit verdict or non_goals: "We read FEATURE_REQUEST.md:98's non-negotiable as binding the IDIOM, not the FILE, on the evidence that three of the repo's four parser guards already live in their own modules. If the user reads it as binding the file, the guard collapses into test_repo_structure.py and the tmp_path proofs go with it." That way the user can overturn it in one read rather than finding it in a parenthesis.
- **adversary:** fit-ac


### F-22

- **id:** A1-22
- **title:** The dispatcher seed's proposed moment ("post-v1 or H2") is itself the mis-filing failure the scope warns about
- **severity:** question
- **confidence:** medium
- **category:** scope-creep
- **location:** risks ("INFERRED, NOT VERIFIED — THE SEED MOMENTS"); tiered_scope.core (seed migration)
- **problem:** The scope proposes moments for the three hypotheses and offers, for the autonomous stage dispatcher, "post-v1 or H2". H2 is `domain-engineer` (ROADMAP.md:198) — a write-capable subagent for `src/`, Needs 1.2, Blocks 1.4. An autonomous stage dispatcher is orchestration of the request pipeline, not domain delegation; attaching it to H2 because H2 is the nearest harness row is exactly the "MIS-FILING UNDER THE NEAREST MOMENT" risk the scope names, committed in the scope's own seed proposal. Leaving it as "or" also hands the implementer an unmade decision inside a core deliverable.
- **proposed_fix:** Settle it here: `post-v1`, on the grounds that ROADMAP.md's harness convention (:130-137) sequences H rows by Needs/Blocks and no existing row needs a dispatcher, and that `post-v1` is the honest answer when no moment exists. Say so in one line so the entry's author does not re-open it. Same treatment for the other two: state the proposed moment and the one-line argument, and label the whole set INFERRED as the scope already does.
- **adversary:** fit-ac


### F-23

- **id:** A1-23
- **title:** No rule for what happens to an entry whose moment is deleted rather than renamed
- **severity:** question
- **confidence:** medium
- **category:** completeness
- **location:** acceptance_criteria[6] (failure message names two candidate causes); non_goals ("No agent ever RESOLVES an entry")
- **problem:** The failure message is required to name both candidate causes — the entry is wrong, or a roadmap row moved. But the scope never states the DISPOSITION rule for the second case. If ROADMAP.md deletes a row (the roadmap has already lost columns once — ADR 0010:120-123 removed `Size` and `★`), an entry pointing at it turns CI red and no agent may resolve it, because "disposition is the user's". So a routine roadmap edit produces a red build only the user can clear, in an unrelated PR. That is a live blocking interaction inside a mechanism whose defining property is that it never blocks.
- **proposed_fix:** Add one line to the boundary header and one non-goal: "If an entry's moment disappears from ROADMAP.md, an agent MAY re-point it to the successor row or to `post-v1` and note the change in the entry — this is a pointer repair, not a resolution. Resolving the underlying question stays the user's." Then the guard's red state is always clearable by the person hitting it, and the non-blocking property survives contact with roadmap edits.
- **adversary:** fit-ac


### F-24

- **id:** A1-24
- **title:** The document-count question is gated but never argued against Phase 0's exit condition
- **severity:** question
- **confidence:** low
- **category:** fit
- **location:** gated_decisions[5]; ROADMAP.md:147
- **problem:** Phase 0's exit condition is "a green CI run on an empty repo, and every document doing one job" (ROADMAP.md:147), and Phase 0 is DONE on that basis. The scope argues the file's location on discoverability grounds and defers the taste call to the user, but never tests the proposal against that exit condition — which is the repo's own standard for whether a new root document is justified. The answer is probably yes (a queue does exactly one job, and it is a job no existing document does — DESIGN.md §4 at :115 comes closest and has no moments), but the argument is not made where a user weighing gated_decision 6 would read it.
- **proposed_fix:** One sentence in the fit verdict: "ROADMAP.md:147's Phase 0 exit — 'every document doing one job' — is satisfied rather than strained: the queue does one job no root document does, and the nearest overlap (DESIGN.md §4, open engineering questions, :115) is explicitly out of scope. A sixth root document is added under that standard, not around it."
- **adversary:** fit-ac


### F-25

- **id:** A1-25
- **title:** Minor mischaracterisation of test_repo_structure.py's contents
- **severity:** nit
- **confidence:** high
- **category:** fit
- **location:** tiered_scope.core (new-module bullet: "no pure functions and no tmp_path fixtures")
- **problem:** The claim is used to justify a separate module and the load-bearing half is correct — I confirmed tests/test_repo_structure.py has no tmp_path fixture and no parser proven red-and-green. But it does contain module-level functions: `_git_check_ignore` at :33 and `_read` at :256. "No pure functions" is wrong as stated; `_read` is one.
- **proposed_fix:** Reword to the accurate and equally strong claim: "test_repo_structure.py's helpers (`_git_check_ignore` :33, `_read` :256) are I/O shims, not parsers; the module contains no pure parse function proven red-and-green and no tmp_path fixture anywhere. tests/test_layering.py is where that idiom lives."
- **adversary:** fit-ac


### F-26

- **id:** A2-01
- **title:** Format contradiction: `Source:` is required by the tests but absent from the pinned five-field format
- **severity:** blocker
- **confidence:** high
- **category:** completeness
- **location:** merged scope — tiered_scope.core ("THE ENTRY FORMAT, pinned deliberately. Five fields, no more…") vs acceptance_criteria[7] ("every entry carries all required fields (`Bears on:`, `Parked:`, `Assumed:`, `Source:`, `Status:`)") and cheap_folds ("each with a `Source:` citation")
- **problem:** The core bullet pins the format at an id plus five keys and never lists `Source:`. AC 8 then makes `Source:` a REQUIRED field the guard enforces on every entry. A planner cannot build both. Worse, the contradiction poisons two of the scope's own arguments: the stated mitigation for designing a format from retrospective examples is "keep the field set to five so a format revision at entry six is an edit rather than a migration," and the `Supersedes:` field is dropped explicitly because it would be "a sixth field." If `Source:` is required, the format is already six and both arguments are spent. It also breaks the three ROADMAP-hypothesis seeds, which have no source citation to give beyond `ROADMAP.md:217-222`.
- **proposed_fix:** Decide it once and state it in one place. Recommended: make `Source:` OPTIONAL — required only when the entry is recovered from an existing artifact — and have AC 8 assert the four mandatory keys (`Bears on:`, `Parked:`, `Assumed:`, `Status:`) plus "`Source:` if present, must be a resolvable relative link" (which the extended link checker already gives for free). Then restate the core bullet as "four required keys plus an optional `Source:`" and drop the "five fields, no more" phrasing, replacing the churn mitigation with an honest "four required keys." Re-check the `Supersedes:` drop rationale against whatever number survives.
- **adversary:** scope-completeness


### F-27

- **id:** A2-02
- **title:** The parser's negative assertion is mis-grounded: the v1 scope tables' rows do NOT have empty leading cells
- **severity:** blocker
- **confidence:** high
- **category:** risk
- **location:** merged scope — acceptance_criteria[2] ("rows whose leading cell is empty (the v1 scope tables at `:25-35` and `:77-84`)") and risks ("a leading-cell-anchored pattern separates all four today (verified by reading each)"); actual repo: ROADMAP.md:23-35, :41-51, :75-84
- **problem:** MEASURED. At ROADMAP.md:23 the header row is `| | Why it can't be cut |` — the empty leading cell is the HEADER. Every data row leads with content: `:25` is `| **Creation** — vitals, position, archetype, draft tier → starting vector | … |`, `:77` is `| **Age/development multiplier** — XP income decaying with age | … |`. So the negative assertion as specified would test a property those rows do not have, and the risk section's claim that a leading-cell anchor "separates all four today (verified by reading each)" is not supported for two of the four. A naive leading-cell-non-empty parser would extract `**Creation** — vitals, position, archetype, draft tier → starting vector` as a valid moment. The guard's whole value is that it rejects a bad moment; a parser built to this spec would accept eleven bogus ones.
- **proposed_fix:** Restate the negative assertion in terms of the property that actually separates the shapes: the leading cell must match an ID SHAPE (`^(?:\d+\.\d+|H\d+)$`) after stripping markdown emphasis, not merely be non-empty. Then the criterion becomes: the parser yields zero ids from the three prose tables (`:23-35`, `:41-51`, `:75-84`) and zero from the open-questions table (`:326-334`), asserted by name against each table's line range. Keep the negative assertion — it is the right idea — but ground it on the shape test rather than on emptiness.
- **adversary:** scope-completeness


### F-28

- **id:** A2-03
- **title:** SCOPE-CREEP: the exact-38-id set assertion is a maintenance trap that fires in unrelated PRs
- **severity:** major
- **confidence:** high
- **category:** scope-creep
- **location:** merged scope — acceptance_criteria[1] ("a test asserts the result equals an exact expected set, not a count. Today that set is the 38 item ids…"); ROADMAP.md:130-137 ("`H` rows are infrastructure … added when it's needed rather than up front")
- **problem:** Hardcoding all 38 ids in tests/test_escalations.py couples an escalation-queue guard to every future roadmap edit. ROADMAP.md explicitly plans to grow H rows on demand, and Phase 2-4 rows may split. The next agent adding H3 gets a red test in a PR about something else, with a fix that is pure ceremony — pasting a new id into a test list. The scope's own risk entry ("ROADMAP RENUMBERING TAX … the obvious 'fix' is to weaken the assertion") describes exactly the pressure this criterion maximizes: an assertion that goes red for a legitimate, unrelated reason is the assertion that gets loosened. The stated benefit — failing loudly on a table reformat rather than silently narrowing — is achievable at a fraction of the cost.
- **proposed_fix:** Replace exact equality with three cheaper assertions that catch the same failure: (1) a small pinned SENTINEL SUBSET must be present — `{"0.1", "1.1", "1.3", "1.11", "H1", "H2", "2.1", "4.6"}` (spans every table shape including the two-digit minor and the harness table's extra `Blocks` column); (2) a LOWER BOUND on count (`>= 38`) so a reformat that narrows the parse fails loudly while a legitimate addition does not; (3) the shape-based negative assertions from A2-02. This keeps every failure mode the exact set was buying and removes the false-red on roadmap growth.
- **adversary:** scope-completeness


### F-29

- **id:** A2-04
- **title:** Core is inconsistent with itself: the summary says seven seed entries, tiered_scope.core says three
- **severity:** major
- **confidence:** high
- **category:** scope-creep
- **location:** merged scope — summary ("Core is therefore the file plus its boundary header, the format, the guard, and seven seed entries — the three `ROADMAP.md:217-222` hypotheses plus four verified decisions already stranded in `_done/1.1-app-shell/`") vs tiered_scope.core (only "SEED MIGRATION — the three `ROADMAP.md:217-222` hypotheses") and tiered_scope.cheap_folds ("RECOVER THE FOUR STRANDED DECISIONS", "RECORD `[OPEN-10]` AS A SEED ENTRY")
- **problem:** The summary silently promotes four cheap_fold items into core, and drops the fifth ([OPEN-10], which would make eight). This is the exact laundering the tiering exists to prevent: the acceptance panel holds the build to whatever `core` says, and the user reads the summary. It also matters substantively — the four recoveries carry a caveat the scope itself labels INFERRED ("the moments are the 1.1 panel's judgment, not re-verified"), which is a reason to keep them foldable rather than mandatory, and one of them ([OPEN-10]) is explicitly flagged as touching ADR 0005's carve-out.
- **proposed_fix:** Pick one and make the summary match. Recommended: keep the three ROADMAP hypotheses in core (they are the request's stated In scope at FEATURE_REQUEST.md:49-50) and leave the four recoveries plus [OPEN-10] as cheap folds. Rewrite the summary sentence to "…the format, the guard, and the three migrated hypotheses, with four recovered strays and the [OPEN-10] orphan folded in cheaply." If instead the panel wants all seven mandatory, move them into tiered_scope.core explicitly and add an acceptance criterion asserting the distinctive strings for all seven, not just the three that AC 10 covers today.
- **adversary:** scope-completeness


### F-30

- **id:** A2-05
- **title:** Contradiction: a core deliverable edits GAME_DESIGN.md §8, which the non-goals and gate 5 both declare off limits
- **severity:** major
- **confidence:** high
- **category:** scope-creep
- **location:** merged scope — above_and_beyond[0] tier `core` ("In the header, plus a reciprocal cross-reference line in GAME_DESIGN.md §8") vs non_goals[0] ("`GAME_DESIGN.md` §8 and its phase index at `ROADMAP.md:324-334` stay exactly as they are") and gated_decisions[4] ("it edits GAME_DESIGN.md, which the non-goals put off limits")
- **problem:** One core item proposes a reciprocal cross-reference line in GAME_DESIGN.md §8; the non-goals say §8 stays exactly as it is; gated decision 5 uses "it edits GAME_DESIGN.md" as a reason to withhold the mirror guard. A planner reading all three cannot tell whether §8 is touchable. Compounding it, no acceptance criterion covers the reciprocal line, so it would silently not happen and nothing would notice — which is the same class of failure (an unenforced pointer) that the measured [OPEN-10] orphan demonstrates.
- **proposed_fix:** Resolve in favour of the cross-reference and narrow the non-goal: change non_goals[0] to "NOT a replacement for `[OPEN-N]` — no migration, no restructuring, no change to any `[OPEN-N]` entry's content. One cross-reference line pointing readers at ESCALATIONS.md is in scope." Add a matching acceptance criterion (substring test: GAME_DESIGN.md contains `ESCALATIONS.md`). Restate gate 5's argument on its actual grounds — that disposing the [OPEN-10] orphan means DECIDING a design question that touches ADR 0005 — rather than on "edits GAME_DESIGN.md," which is now permitted.
- **adversary:** scope-completeness


### F-31

- **id:** A2-06
- **title:** MISSING REGISTER: `DESIGN.md` §3 "Architecture notes not yet ADRs" is a sixth parking place and the closest overlap of all
- **severity:** major
- **confidence:** high
- **category:** completeness
- **location:** DESIGN.md:99-113 (verified: `## 3. Architecture notes not yet ADRs`, three bullets including "Two packages, one repo" and "The read-model is disposable"); merged scope — fit_verdict FRICTION 1 enumerates five registers and omits it; acceptance_criteria[8] requires the header to name only four things
- **problem:** The scope's own load-bearing deliverable is the register boundary, and its enumeration is incomplete. `DESIGN.md` §3 is literally "decisions taken but not yet recorded as ADRs" — semantically nearer to a parked build-time decision than §2 (unsettled mechanism math) or §4 (open engineering questions), and it is the section a worker who has just made a judgment call would most plausibly reach for. The convergence map even treats the scopers' disagreement on register COUNT (five/three/two) as sharpening the point; the merged count is still wrong. Separately, AC 9 collapses `DESIGN.md` §2 and §4 into a single `DESIGN.md` substring, so the header could name §2 alone and pass while leaving the sharpest overlap (§4) undisambiguated.
- **proposed_fix:** Add `DESIGN.md` §3 to the register map as a sixth row, with the distinguishing test stated plainly: §3 holds decisions ALREADY MADE that have not earned an ADR; the queue holds decisions NOT YET MADE. Strengthen AC 9 to assert the header contains all three DESIGN.md section references as distinct strings (`§2`, `§3`, `§4`) rather than the bare filename, so the boundary cannot pass by naming one of three. Update fit_verdict FRICTION 1 to say six registers, since the count is part of the argument for why the header is the deliverable.
- **adversary:** scope-completeness


### F-32

- **id:** A2-07
- **title:** MISSING: an Open entry whose moment reaches DONE becomes permanently invisible — the drain has a hole no tier addresses
- **severity:** major
- **confidence:** medium
- **category:** completeness
- **location:** merged scope — non_goals ("NOT a blocking mechanism"), gated_decisions[0] recommendation (b) (read seam at `/make-feature-request` Step 2), above_and_beyond "One-line /commit surface" tier `gated` / recommended NO, and "An /update-docs check for queue drift" tier `drop`
- **problem:** The drain fires when a NEW item enters intake and someone reads what was parked against it. Nothing fires when an item COMPLETES. If item 1.3 lands with two of its entries still Open, those entries now name a DONE moment, the read seam will never surface them again (no future request names 1.3), and they sit in the file forever looking live. This is distinct from the INERTNESS risk the scope does name — inertness is "nobody parks anything"; this is "things were parked correctly and still fall off the end." Both candidate remedies were disposed independently (the /commit surface recommended NO as "the second-best read point"; the /update-docs check dropped), and neither disposition mentions this failure — they were both argued only against inertness.
- **proposed_fix:** Name it as a distinct risk, then dispose it deliberately. Cheapest honest remedy that respects the non-blocking rule: add a `Status:` value of `lapsed` to the closed vocabulary plus one header sentence ("an entry whose moment shipped without an answer is marked `lapsed` and either re-pointed at a later moment or resolved as 'decided by default'"), so the state at least has a name. Do NOT make it a test — a guard asserting "no Open entry names a DONE item" would turn a live queue entry into a red build, which violates the user-settled non-blocking constraint (see A2-08). If the user takes gate 1(b), note in that gate's rationale that the read seam does not close this hole, so gate 1(a) carries this cost too.
- **adversary:** scope-completeness


### F-33

- **id:** A2-08
- **title:** The guard makes the ACT of parking capable of blocking a merge, in tension with the user-settled "parking never blocks"
- **severity:** major
- **confidence:** medium
- **category:** risk
- **location:** merged scope — acceptance_criteria[5] ("THE REAL ASSERTION: the parser run over the actual `ESCALATIONS.md` finds zero violations") and [7] (field/vocabulary guards) vs non_goals[2] ("NOT a blocking mechanism… no test fails because an entry is unresolved… nothing in the format or the wiring may halt a stage") and FEATURE_REQUEST.md:55-56
- **problem:** The non-goal is scoped to UNRESOLVED entries, which is correct as far as it goes. But the guard means a MALFORMED entry — a typo'd status, a missing `Assumed:`, a moment that was valid last week and got renamed — turns CI red and blocks the PR that is carrying unrelated work. A worker who has just been burned by that once has a strong incentive to take the old second move (guess silently) rather than park, because parking now carries merge risk that guessing does not. That is the precise behaviour the feature exists to eliminate. The scope's risk list covers parser brittleness and the renumbering tax as CORRECTNESS concerns; it never connects them to the non-blocking constraint as an INCENTIVE concern.
- **proposed_fix:** Name the tension explicitly in risks, and mitigate it in the format rather than by weakening the guard: (1) keep the worked example in the header (already a cheap fold) — it is the main defence; (2) make the failure message actionable enough to fix in under a minute (AC 7 already requires naming the entry, the moment, and both candidate causes — keep that); (3) state in the header that a malformed entry is a build failure so the worker knows the shape matters before writing, and that the fix is always a one-line edit, never deleting the entry. Add a non-goal clarifier: "parking never blocks WORK; a malformed entry does block the MERGE, and that is the price of a mechanical pointer."
- **adversary:** scope-completeness


### F-34

- **id:** A2-09
- **title:** Inconsistent standard: the root-wide link-checker extension is folded in while an equally adjacent measured defect is pushed to its own request
- **severity:** major
- **confidence:** medium
- **category:** scope-creep
- **location:** merged scope — cheap_folds ("EXTEND `tests/test_request_links.py`'s scanned set to root-level `*.md`") vs risks ("MEASURED DEFECT, ADJACENT AND WORTH ITS OWN BUGFIX REQUEST — NOT FIXED HERE" re `update-docs/SKILL.md:76-77`); tests/test_request_links.py:24 `SCANNED_TREES`
- **problem:** Both are pre-existing defects in shared tooling, adjacent to this item, and cheap. One is folded into a harness item that holds a binding `Blocks: 1.3`; the other is pushed out on the grounds that "it is a defect in an existing skill." The distinguishing principle is never stated. The measurement the scope uses to justify folding (all five root docs return `[]` today) proves there is no CLEANUP today — it does not bound the ONGOING cost: after this lands, every future edit to README.md, CLAUDE.md, ROADMAP.md, GAME_DESIGN.md and DESIGN.md is link-gated, including edits made by `/commit`'s doc pass and `/update-docs`, by five documents' worth of surface that H1 has no stake in. That is a permanent widening of a shared guard introduced by a queue feature.
- **proposed_fix:** Narrow it to what H1 actually needs: add `ESCALATIONS.md` alone to `SCANNED_TREES` (a one-file addition, e.g. an explicit `SCANNED_FILES` tuple alongside the trees), and raise "extend the checker to all root-level `*.md`" as its own follow-up request alongside the `Measure-Object -Line` bugfix. That keeps the queue's dense relative pointers checked — which is the real motivation — applies one consistent standard to both adjacent defects, and leaves the shared guard's blast radius unchanged. If the panel prefers the wide version, state the distinguishing principle ("defects in tests we are already editing get folded; defects in skills do not") so the next item can apply it.
- **adversary:** scope-completeness


### F-35

- **id:** A2-10
- **title:** Missed measured doc-drift in a file this scope edits: CLAUDE.md still says nine ADRs in one place and ten in three others
- **severity:** major
- **confidence:** high
- **category:** completeness
- **location:** CLAUDE.md:216 ("**Check the ADRs before proposing anything structural.** Nine decisions are") vs CLAUDE.md:57 ("decisions/          ADRs — ten settled calls"), :90 ("Ten ADRs cover save decryption, ingestion, the ledger, rulesets,"), :111 ("All ten are ADRs."); docs/decisions/ contains 0001–0010 (verified by listing)
- **problem:** MEASURED. CLAUDE.md is internally inconsistent about the ADR count, and the scope — which explicitly verified "Ten ADRs exist (`docs/decisions/0001`–`0010`, verified by listing)", edits CLAUDE.md, pins a CLAUDE.md line budget, and spends a gated decision (gate 4) on whether to add ADR 0011 — never noticed. This is directly load-bearing on gate 4: approving ADR 0011 requires updating an ADR count that is already wrong in one of four places, and the scope's discoverability acceptance criteria are substring assertions, which by construction cannot catch a count. It is also a live instance of exactly the rot H1 exists to make mechanical, sitting in the onboarding document.
- **proposed_fix:** Fold the one-word fix (`Nine` → `Ten` at CLAUDE.md:216) into this branch — it is a word change, not a line, so it does not touch the budget constraint in AC 17. Note it in gate 4's rationale as a second small cost of approving ADR 0011 (four call-sites to keep in step, none of them tested). Optionally raise a follow-up: the ADR count appears in CLAUDE.md four times and README.md:63 once, all untested — a candidate for a one-line structural assertion in the same idiom as `test_adr_numbers_are_unique_and_contiguous`.
- **adversary:** scope-completeness


### F-36

- **id:** A2-11
- **title:** The scope proves CLAUDE.md's budget is blown, then spends a line of it anyway
- **severity:** major
- **confidence:** medium
- **category:** acceptance
- **location:** merged scope — acceptance_criteria[16] ("CLAUDE.md BUDGET NOT WORSENED BY MORE THAN ONE LINE… MEASURED BASELINE: 221 lines") and risks ("the budget reads as met with 19 to spare while the file is 21 OVER"); tiered_scope.core ("one line in `CLAUDE.md`'s project-map fenced block"); `.claude/skills/update-docs/SKILL.md:76-78` ("`CLAUDE.md` stays **under 200 lines**"); measured: `(Get-Content CLAUDE.md).Count` = 221, `Measure-Object -Line` = 181
- **problem:** The scope establishes that the real file is 21 lines over a 200-line hard budget and that the instrument reporting compliance is defective — then writes an acceptance criterion permitting the file to grow by one more, and puts that growth in `core`. "Not worsened by more than one line" is the wrong bar for a file already over budget; the honest bars are net-zero or a reduction. This also weakens the case for raising the measurement defect as a separate bugfix request: the scope discovered the budget is being violated and its response was to violate it slightly more.
- **proposed_fix:** Change AC 17 to NET-ZERO: `(Get-Content CLAUDE.md).Count` must not exceed 221. The project-map fence at CLAUDE.md:51-67 has an easy trade — the fence already carries a comment line per entry, so add `ESCALATIONS.md` and merge or trim one adjacent line. Alternatively drop the CLAUDE.md pointer from core entirely: `README.md`'s project map plus `requests/README.md` already give two discoverable locations, and `requests/README.md` is the only one covered by the link checker today. If CLAUDE.md keeps the pointer, say in the scope that it is being paid for from a budget already overdrawn, so the decision is visible.
- **adversary:** scope-completeness


### F-37

- **id:** A2-12
- **title:** No gated item carries a conditional acceptance criterion — if a gate is approved, nothing proves it landed
- **severity:** major
- **confidence:** medium
- **category:** acceptance
- **location:** merged scope — gated_decisions[0]–[5] and tiered_scope.gated; acceptance_criteria (17 criteria, all written against the roadmap-literal core plus folded cheap items)
- **problem:** Every acceptance criterion is written for core-plus-folds. The six gated decisions — including gate 1, which the scope calls "the headline gate" and recommends taking — have no criteria attached. If the user approves gate 1(b) (a READ bullet in `/make-feature-request` Step 2), the build has no test, no substring assertion, and no user-run criterion proving it happened, in a repo whose intake README defines testable as "a cold agent can run one command and get a pass or fail" (`requests/feature-requests/README.md:65-67`). The same applies to gate 3 (the `/diagnose-bug` pointer line) and gate 4 (ADR 0011, which would need an index row and would hit `test_adr_numbers_are_unique_and_contiguous`).
- **proposed_fix:** Attach one conditional criterion per gate, marked "applies only if approved." Gate 1(b): a substring test asserting `.claude/skills/make-feature-request/SKILL.md` contains `ESCALATIONS.md` — the same idiom as `test_both_intake_templates_carry_a_stage_plan_section` (tests/test_repo_structure.py:159). Gate 3: the same substring assertion against `.claude/skills/diagnose-bug/SKILL.md`. Gate 4: `test_every_adr_is_listed_in_the_index` and `test_adr_numbers_are_unique_and_contiguous` stay green with 0011 present, plus the ADR count call-sites in CLAUDE.md and README.md updated (see A2-10). Gate 5: the mirror guard is green, i.e. the orphan is disposed first.
- **adversary:** scope-completeness


### F-38

- **id:** A2-13
- **title:** Entry-id collisions across branches are unaddressed: sequential `E-NNN` in one file merges cleanly into duplicates
- **severity:** major
- **confidence:** medium
- **category:** risk
- **location:** merged scope — tiered_scope.core ("a stable entry id (`E-NNN`)") and acceptance_criteria[7] ("entry ids match `^E-\d{3}$` and are unique"); CLAUDE.md conventions ("Work on a branch; land it through a PR")
- **problem:** Every substantial change here happens on a feature branch. Two branches that each park an entry both pick the next free `E-NNN`, and git merges two additions to different regions of one markdown file without a conflict. The uniqueness assertion then fails on `main` AFTER both merged, and the repair is renumbering — which breaks any pointer already written to the old id (a resolution pointer, an ADR, a request, a commit message). The ADR set avoids this because it is one file per decision, so git conflicts loudly; a single append-only markdown file with a monotonic counter has the opposite property. Nothing in the risks, non-goals, or format addresses id assignment.
- **proposed_fix:** Either accept and name it (single-author repo, branches are short-lived, likelihood genuinely low) as a one-line risk with the repair stated — "renumber the later entry and leave a `superseded id` note rather than silently reusing" — or remove the failure mode by construction: date-scoped ids (`E-2026-08-15-a`) never collide, are still stable, still sort, and cost one regex change (`^E-\d{4}-\d{2}-\d{2}-[a-z]$`). The date form also makes `Parked:` partially redundant, which slightly offsets the format-size pressure from A2-01.
- **adversary:** scope-completeness


### F-39

- **id:** A2-14
- **title:** AC 10 and AC 11 can both pass while the substantive observation the migration was told to preserve is dropped
- **severity:** minor
- **confidence:** high
- **category:** acceptance
- **location:** merged scope — goals[4] ("preserving the substantive observation embedded there (that 'serviceable' is a v1 constraint in both directions per `ROADMAP.md:53-56`)"), tiered_scope.core ("moves INTO the serviceability-gate entry"), vs acceptance_criteria[9] (three hypothesis names present) and [10] (ROADMAP no longer enumerates them)
- **problem:** The scope names this as the thing a mechanical copy of three titles would drop, and then writes acceptance criteria that check exactly a mechanical copy of three titles plus a deletion. AC 10 asserts three distinctive strings appear in ESCALATIONS.md; AC 11 asserts ROADMAP.md's paragraph is reduced to a pointer. Both are satisfied by an implementation that deletes ROADMAP.md:220-222's observation and never rewrites it anywhere. The information — that "serviceable" is a v1 constraint in both directions (ROADMAP.md:53-56) and is nowhere defined or tested — would be lost from the repo entirely, in the very migration that exists to stop losing things.
- **proposed_fix:** Add one substring criterion in the AC-10 idiom: `ESCALATIONS.md` contains a distinctive fragment of the preserved observation (e.g. `nowhere defined or tested`) and a link or citation to `ROADMAP.md`'s v1 section. One assertion, and it converts the goal from an intention into a check.
- **adversary:** scope-completeness


### F-40

- **id:** A2-15
- **title:** `Status:` vocabulary is declared in the test, not in the document the worker reads — a built-in drift source
- **severity:** minor
- **confidence:** high
- **category:** completeness
- **location:** merged scope — acceptance_criteria[7] ("every `Status:` value is drawn from a closed vocabulary declared in the test"); contrast tests/test_layering.py:26 `DESIGN_CITATION` and :112-123, where the test asserts the failure message carries the rule
- **problem:** The source of truth for a field a human writes by hand would live in a pytest module. A worker reads `ESCALATIONS.md`'s header, writes a status the header does not enumerate (or enumerates loosely), and finds out at CI. Worse, the two can drift in the other direction: the header lists four statuses, the test knows three, and the fourth silently never validates. This is the same class of failure as the register boundary living only in the scope document rather than in the file — a mistake the scope correctly identifies and fixes for the boundary, then reintroduces for the vocabulary.
- **proposed_fix:** Declare the vocabulary in `ESCALATIONS.md`'s header (a one-line list) and have the test PARSE it from there, or — simpler and in the repo's existing idiom — keep the tuple in the test but add an assertion that every value in it appears verbatim in the header, mirroring `test_the_failure_message_cites_the_architecture_record` (tests/test_layering.py:112). Either way the document a human reads and the check that binds them cannot drift apart.
- **adversary:** scope-completeness


### F-41

- **id:** A2-16
- **title:** New test module diverges from a stated non-negotiable and is placed in core with the dissent buried, while smaller unanimous questions got gates
- **severity:** minor
- **confidence:** medium
- **category:** framing
- **location:** FEATURE_REQUEST.md:98-99 ("**The structural test matches the existing idiom** in `tests/test_repo_structure.py`", under *Constraints / Non-negotiables*); merged scope — tiered_scope.core ("`tests/test_escalations.py` — a NEW module… (Minimalist dissent recorded: it reads the constraint as naming the file.)") vs gated_decisions[5] (file location, all three scopers agreed, still gated)
- **problem:** The scope's reading — that the constraint binds the idiom, not the file — is defensible and well argued (test_layering.py, test_request_links.py and test_ci_contexts.py are all standalone parser guards). But it is a divergence from something the request filed under *Non-negotiables*, disposed inside a core bullet with the dissent parenthesised, while a question all three scopers agreed on (root vs docs/) was elevated to a gated decision. The gating is inconsistent in the direction that matters: the contested call was folded, the uncontested one was escalated.
- **proposed_fix:** Either surface it as a short gated decision — "the request names `tests/test_repo_structure.py`; we read that as the idiom, not the file. Confirm or redirect. Cost of redirecting: the pure-function/`tmp_path` red-green proofs land in a module with no fixtures and no pure functions, which is the one thing that module currently isn't" — or, at minimum, add an explicit line to fit_verdict recording that a stated non-negotiable was reinterpreted, so it is not discovered at acceptance. Given gate 6 already exists for the file's location, a two-line addition there is the cheapest home.
- **adversary:** scope-completeness


### F-42

- **id:** A2-17
- **title:** Dependency gap: panel subagents are read-only by convention, so much of the pipeline structurally cannot park an entry
- **severity:** minor
- **confidence:** medium
- **category:** risk
- **location:** CLAUDE.md ("**Subagents get read-only git.**"); scope-feature / create-implementation-plan panel subagents run under explicit read-only instructions (this very scoping task included); merged scope — gated_decisions[1] recommendation (defer write wiring), goals[0] ("A worker hitting a judgment call can record it")
- **problem:** The scope's central goal is that "a worker" hitting a judgment call parks it. But the workers who hit the most judgment calls are panel subagents in stages 2 and 3, and those are launched read-only — they return findings as text, they do not write tracked files. With write-side wiring deferred (gate 2, recommended NO), the pipeline's own gated calls can only reach the queue if the ORCHESTRATING agent transcribes them, and nothing in core, cheap_folds, or the accepted gates asks it to. So the realistic population of parkers in the near term is: the main agent, and the user. That is smaller than the goals imply, and it strengthens the inertness risk in a way the risk entry does not capture.
- **proposed_fix:** Name the constraint in risks and adjust one expectation: state that in the near term the parker is the main-thread agent or the user, and that panel subagents surface a parkable decision in their RETURN, which the orchestrator transcribes. If gate 1(b) is approved, the natural symmetric addition is one line telling `/scope-feature`'s merge step to transcribe any gated call the user declines to decide — but that is write-side wiring and belongs with gate 2, so note it as the first candidate for the deferred follow-up rather than folding it here.
- **adversary:** scope-completeness


### F-43

- **id:** A2-18
- **title:** The ROADMAP table-shape enumeration undercounts: the in-scope application table at :41-51 is never named
- **severity:** minor
- **confidence:** high
- **category:** completeness
- **location:** ROADMAP.md:41-51 (`| Surface | Contents |` header, rows leading `| **Career management** | …`); merged scope — risks ("`ROADMAP.md` mixes four table shapes in one file") and acceptance_criteria[2], which names three tables
- **problem:** MEASURED. ROADMAP.md contains at least eight markdown tables in five distinct shapes: the in-scope engine table (:23-35), the in-scope APPLICATION table (:41-51) — never mentioned anywhere in the scope — the out-of-scope table (:75-84), five phase item tables, the harness table with its extra `Blocks` column (:195-198), and the open-questions table (:324-334). The application table's rows lead with `**Career management**`, `**Player state**`, etc., so it is a live false-positive source for any leading-cell parser and it is not covered by the negative assertion. Combined with A2-02, the negative-assertion criterion is grounded on an inventory that is both miscounted and mischaracterised.
- **proposed_fix:** Restate the inventory as five shapes and list all three prose tables by line range in the negative assertion: `:23-35`, `:41-51`, `:75-84`, plus `:324-334`. With the id-shape anchor from A2-02 in place, all four fall out for free — but they should be asserted by name, because the point of a negative assertion is that a future loosening fails loudly.
- **adversary:** scope-completeness


### F-44

- **id:** A2-19
- **title:** `post-v1` as a moment: provenance and casing unspecified
- **severity:** minor
- **confidence:** high
- **category:** acceptance
- **location:** merged scope — acceptance_criteria[1] ("plus the phase names and the literal `post-v1`") and [4] (fabricated queue naming `post-v1` returns none); ROADMAP.md:277 (`### Post-v1`) and :328/:330/:333/:334 (`post-v1` in Phase cells)
- **problem:** The valid-moment set is supposed to be parsed out of ROADMAP.md, but `post-v1` appears there in two forms: a heading `### Post-v1` (capital P) and lowercase inside open-questions Phase cells that the negative assertion says must contribute zero ids. So either the parser special-cases the literal (in which case it is not derived from the document, and the exact-set criterion is partly a hardcode), or it derives it from the `### Post-v1` heading (in which case casing must be normalised or the red/green fixture in AC 5 fails). The scope's precedent citation points at :328-334, which is precisely the table it also forbids the parser from reading.
- **proposed_fix:** Specify one source and one normalisation: derive phase-shaped moments from `^###\s+(Phase \d+|Post-v1)` headings and compare case-insensitively, so both `post-v1` and `Post-v1` validate. Restate the precedent citation as ROADMAP.md:277 (the heading) rather than :328-334 (the forbidden table), and adjust AC 5's fixture to exercise both casings.
- **adversary:** scope-completeness


### F-45

- **id:** A2-20
- **title:** Two citation slips in otherwise well-grounded evidence
- **severity:** nit
- **confidence:** high
- **category:** framing
- **location:** merged scope — cheap_folds/above_and_beyond ("`Phase 3` — whose Exit at `ROADMAP.md:248-249` is literally 'the app is genuinely serviceable'") vs ROADMAP.md:248 (`**Proves:**`) / :249 (`**Exit:**`); grounding_pointers ("`requests/README.md:6-12` (the three-track tie-break)") vs the tie-break actually living at `requests/feature-requests/README.md:8-12` — `requests/README.md:6-10` is the three-track TABLE
- **problem:** Both are small, and I verified every other line citation in the scope resolves. But the Phase-3 one is load-bearing for a cheap fold: the argument for widening the moment vocabulary rests on Phase 3's own text saying "genuinely serviceable," and it says that in the **Proves** line, not the **Exit** line. A planner quoting the scope into an implementation plan would propagate the misattribution into the seed entry itself.
- **proposed_fix:** Change to "whose **Proves** line at `ROADMAP.md:248` is literally 'and the app is genuinely serviceable'", and change the tie-break pointer to `requests/feature-requests/README.md:8-12` (or cite `requests/README.md:6-10` as the track table, which is what it is).
- **adversary:** scope-completeness


### F-46

- **id:** A2-21
- **title:** `test_no_leaks.py` scans the git index, so "a new tracked .md is scanned" only holds after staging
- **severity:** nit
- **confidence:** high
- **category:** acceptance
- **location:** tests/test_no_leaks.py:12-13 ("Scanned files are the git index") and :61-74 (`git ls-files -z`); merged scope — acceptance_criteria[15] ("in particular `tests/test_no_leaks.py` (a new tracked `.md` is scanned; the repo is PUBLIC…)")
- **problem:** A locally-created, unstaged `ESCALATIONS.md` is invisible to `_tracked_text_files()`. Running `uv run pytest` before `/commit` stages the file would report green while the leak guard has never looked at it. The criterion is true on CI (the branch is pushed, so the file is tracked) but false at the moment a builder would most naturally check it, and the scope states it without that qualifier.
- **proposed_fix:** Add the qualifier: "…scanned once `ESCALATIONS.md` is staged — `test_no_leaks.py` reads `git ls-files`, so verify AFTER `/commit` stages, or with an explicit `git add -N ESCALATIONS.md` first." One clause, and it removes a false-green window on a public-repo guard.
- **adversary:** scope-completeness


### F-47

- **id:** A2-22
- **title:** No stop rule or cut line for a build that holds a binding `Blocks: 1.3`
- **severity:** question
- **confidence:** medium
- **category:** scope-creep
- **location:** merged scope — tiered_scope (9 core bullets, 8 cheap folds), acceptance_criteria (17 criteria), gated_decisions (6); ROADMAP.md:197 (`Blocks: 1.3`), risks ("SCOPE CREEP HAS A BINDING COST HERE")
- **problem:** The scope names the binding cost and then proposes a build with nine core items, eight folds, seventeen acceptance criteria and six decisions for the user — for a markdown file, a format, and one parser. Every one is individually defensible; collectively they are a substantial branch sitting on the ledger's correction model. The scope's own partial relief (1.2 is not blocked by H1 and 1.3 needs 1.2 anyway) is correctly labelled "slack is not a licence," but no licence limit is proposed either. There is no stated minimum viable landing, so if the branch runs long there is no defined thing to cut to.
- **proposed_fix:** State an explicit MVP and a cut order. Suggested MVP: `ESCALATIONS.md` with its boundary header and worked example, the four-key format, `tests/test_escalations.py` with the moment guard plus non-vacuity, the three ROADMAP hypotheses migrated with ROADMAP.md reduced to a pointer, and the `requests/README.md` line. Suggested cut order if the branch runs long, in this sequence: the root-wide link-checker extension (A2-09 narrows it anyway), the [OPEN-10] seed entry, the four `_done/` recoveries, the `test_core_documents_exist` extension. Each is independently landable as a two-line follow-up, which is what makes them safe to cut.
- **adversary:** scope-completeness


### F-48

- **id:** A2-23
- **title:** Open question: what happens to a parked decision answered after the ruleset it bears on is pinned?
- **severity:** question
- **confidence:** low
- **category:** risk
- **location:** merged scope — fit_verdict ("no ruleset version changes, no career replays, no recorded history shifts — ADR 0003's append-only rule and ADR 0004's pinned-version immutability are not engaged"); docs/decisions/0004-rulesets-as-versioned-config.md; ROADMAP.md:179-183 (items 1.2, 1.3, 1.4)
- **problem:** The contract analysis is correct TODAY — nothing here touches a ledger or a ruleset, verified by filesystem probe. But the queue's first real users will be items 1.2 `career-ledger`, 1.3 `correction-by-append` and 1.4 `ruleset-loader`, and the entries parked against them will be ledger-schema and ruleset-shape decisions. Once ruleset v1 is pinned by a recorded event (ADR 0004 makes a pinned version immutable), an entry answered afterwards cannot be applied by editing v1 — it has to become v2. Nothing in the queue's header or format tells a worker that, and "the queue records decisions that the repo's own rules may make unapplyable by the time they are answered" is a genuinely new interaction.
- **proposed_fix:** Probably not a v1 build item, but worth one sentence in the header once 1.4 exists: "an entry answered after the thing it bears on has shipped is resolved forward — a new ruleset version, a superseding event, a new ADR — never by editing what was recorded." For now, record it in the scope's risks as a forward-looking note so the first ledger entry does not discover it, and so gate 4's ADR-0011 argument can weigh it (this is the kind of interaction an ADR is actually for).
- **adversary:** scope-completeness


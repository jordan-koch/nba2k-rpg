> **Status:** implemented · created 2026-08-21 · decided · next: commit

# Implementation Report — Escalation Queue (Harness H1)

> **One-line outcome:** a decision can be parked against the moment that reopens it, with a parser
> guard proving every entry names a real roadmap moment and three seams that actually read it ·
> **Acceptance:** 23/24 criteria met by execution, AC 24 handed to the user unclaimed ·
> **Branch:** `phase1/escalation-queue`

## 1. Acceptance ledger

Every row was verified by **running** the command named, not by inspection. Counted row by row for
this report rather than carried over from the panel's headline — its own meta-audit caught that
headline ("21 of 24") contradicting its ledger, so the arithmetic here is independent.

**Totals: 23 met · 0 partial · 0 unmet · 1 USER-RUN (not claimable).**

| # | Tier | Criterion | Verdict | Evidence |
|---|---|---|---|---|
| 1 | C | `pytest tests/test_escalations.py -q` green; docstring in the house idiom | **met** | 22 tests, exit 0. Docstring `tests/test_escalations.py:1-26` names the motivating failure and the vacuity risk |
| 2 | C | Parser positive: non-empty, contains `0.1`/`1.3`/`H2`/`4.6`, size ≥ 30 | **met** | `known_moments()` over the real `ROADMAP.md` returns **44** = 38 item ids + 5 phase names + `post-v1`. Matches Phase 0's measured 38 exactly |
| 3 | C | Parser negative: leading cell must **match** an id pattern; all three non-item tables plus open-questions contribute zero | **met** | Ran per anchor: 13 / 11 / 10 / 11 table rows, `_item_ids` = `set()` for each. Slices asserted non-empty first, so the check cannot go vacuous |
| 4 | C | Non-vacuity: entry regex matched ≥ 1, with a drift message | **met** | `test_the_entry_regex_matched_something`. **Strengthened past the criterion:** the floor alone cannot see a malformed entry (the count fails to *grow*, it never shrinks) — `malformed_headings()` closes that, see §5 C-01 |
| 5 | C | Proven red **and** green against `tmp_path`; both fixtures fabricate the roadmap | **met** | Red returns exactly `[('E-001','9.9')]`; green returns `[]` across `1.3` / `H2` / `Phase 3` / `post-v1`. Both write their own `FAKE_ROADMAP`; no tracked file is mutated |
| 6 | C | The real assertion: zero violations over the actual queue | **met** | `unknown_moments(QUEUE, ROADMAP)` → `[]` over 9 entries |
| 7 | C | The failure message is the record — names file, entry id, moment, rule | **met** | `violation_message()` emits all four. **Was `partial` at panel time**: under a malformed neighbour it named an innocent entry. C-01's fix makes the id reliably the offending one |
| 8 | C | Field and vocabulary guards; six fields; id `^E-\d{3}$`, unique; closed `Status:` vocabulary | **met** | Guards proven by mutation (deleted field → reported; `Status: deferred` → reported; duplicate id → reported). **Was `partial`**: the id-shape clause was enforced only by construction, since a malformed heading was never examined. C-01's fix makes it real. Non-emptiness added beyond the criterion |
| 9 | C | State stored once — section agrees with `Status:` | **met** | `test_each_entry_sits_in_the_section_its_status_claims`; all 9 entries `open` under `## Open` |
| 10 | C | Register-boundary guard; no entry title contains `[OPEN-` | **met** | Asserted against the register-map **table rows** (7 rows), anchored on `GAME_DESIGN.md` / `§2` / `§4` / `Stage plan` / `diagnose-bug` — chosen to dodge two vacuity traps (§4) |
| 11 | C | The fenced worked example parses green under the *same* guards | **met** | E-000 parses as exactly one entry, all five field bullets, `Status: open`, moment `post-v1` resolves. Retargeted off `1.3` — see §5 C-05 |
| 12 | C | Seed migration proven by distinctive substrings | **met, as twice amended** | Scope said **seven**; plan decision G2 amended to **eight** (E-008); the user approved a **ninth** (E-009) during this stage. All nine substring-asserted |
| 13 | C | No duplicate source: `ROADMAP.md` no longer enumerates the three hypotheses; the observation is preserved | **met** | The three phrases are absent from `ROADMAP.md`; `ESCALATIONS.md` is referenced; `serviceable` still present — all three asserted |
| 14 | G | The read seam exists in `/make-feature-request`, substring-tested | **met** | Bullet in Step 2; `test_intake_reads_the_queue_when_grounding_an_item`. Widened to phase names — §5 C-04 |
| 15 | G | The `/commit` drain-hole check exists, substring-tested | **met** | Third rail in Step 4; `test_commit_surfaces_open_entries_before_closing_a_row`. Widened to phase headers — §5 C-04 |
| 16 | G | The `/diagnose-bug` pointer exists, substring-tested | **met** | One line in the Escalation block; `test_diagnose_bug_has_somewhere_to_hand_a_murky_cause` |
| 17 | F | `test_repo_structure.py` green, `test_core_documents_exist` extended, docstring corrected | **met** | Queue added to the tuple; the docstring that said "the three documents" over a five-name tuple now states the rule instead |
| 18 | F | `test_request_links.py` green, extended to root-level `*.md` | **met** | 25 files scanned, 6 root docs, 0 dead links. Non-recursive glob, deduped. Anti-vacuity test added beyond the criterion (§5 M-07) |
| 19 | F | Discoverability proven **mechanically** — both maps, each substring-tested | **met** | **Was `unmet` at panel time** — the two map lines landed with nothing asserting them. `test_both_project_maps_name_the_escalation_queue` added; proven to bite (removing either line makes the substring absent) |
| 20 | F | `CLAUDE.md`'s "Nine decisions" → "Ten" | **met** | One word, zero line delta |
| 21 | C | `ruff check`, `ruff format --check`, `mypy` all exit 0; zero new `# type: ignore` | **met** | All three exit 0 — 64 files formatted, 16 source files type-checked under strict. Zero `# type: ignore` anywhere in `tests/` or `src/` |
| 22 | C | `uv run pytest` green overall, including `test_no_leaks.py` with the queue **tracked** | **met** | **79 passed.** `test_no_leaks` enumerates `git ls-files` — the *index* — so the eleven paths were staged first; re-run after every later edit |
| 23 | C | `CLAUDE.md` budget worsened by at most one line vs HEAD | **met** | `(Get-Content CLAUDE.md).Count` = **222**, HEAD = 221. Exactly at cap |
| 24 | C | **USER-RUN** — the 1.3 pickup surfaces entries unprompted; an entry is answerable by editing the queue alone; parked context reads as useful | **HANDED TO THE USER — not claimed** | Mechanical precondition holds: E-008 and E-009 both bear on `1.3`, and `/make-feature-request` Step 2 instructs intake to surface them. Whether it *feels* useful is a human judgment and is not claimable here |

## 2. What shipped

All five plan phases. Against the plan's §7 checklist — 16 rows, all accounted for:

| File | Change |
|---|---|
| `ESCALATIONS.md` | **New**, 245 lines. Header, register map, ADR-0011 trigger, both halves of the F-33 carve-out, name disambiguation, pinned six-field format, worked example, **nine** seeds |
| `tests/test_escalations.py` | **New**, 22 tests. Parser + guards + the three seam tests (decision G6) |
| `ROADMAP.md` | `Parked, not scheduled` reduced to a pointer; Phase 1 status prose updated. H1 row left for `/commit` |
| `tests/test_repo_structure.py` | `test_core_documents_exist` extended + docstring corrected; project-map test added |
| `tests/test_request_links.py` | Non-recursive root glob + docstring; anti-vacuity test added |
| `CLAUDE.md` | Project-map line; "Nine" → "Ten"; `[OPEN-N]` bullet folded to name the queue |
| `README.md` | Project-map row |
| `requests/README.md` | One line beside the three-track table |
| `.claude/skills/make-feature-request/SKILL.md` | One bullet, Step 2 |
| `.claude/skills/commit/SKILL.md` | Third rail, Step 4 + frontmatter description clause |
| `.claude/skills/diagnose-bug/SKILL.md` | One line, Escalation block |
| The four request artifacts + Index | Status rolled to `implemented`; this report added |

## 3. Deviations from the plan

1. **AC 12's seed count moved 8 → 9.** The plan's G2 amended the scope's seven to eight; the panel
   proposed a ninth (E-009, ruleset-version pinning on a correction event at moment `1.3`) and the
   user approved it. It doubles AC 24's day-one signal at the item H1 blocks.
2. **Three guards added beyond the criteria**, each closing a hole the panel confirmed by
   execution: `malformed_headings()`, `unresolved_sources()`, and the link-checker anti-vacuity
   assertion. §5 has the reasoning.
3. **`CLAUDE.md` gained a fourth edit** — the `[OPEN-N]` bullet now names the queue. Above the
   contract (AC 19 asked only for the map line), user-approved, and rewritten to fit two lines so
   AC 23's cap still holds at 222.
4. **The worked example's subject changed.** It was a ledger-fold question bearing on `1.3` with a
   `Source:` pointing at a file that does not exist. Both were defects — see §5 C-05.
5. **No phase was deferred.** Phase 0's seven pre-flight steps were all discharged, including the
   two by-eye verifications that caught the upstream scope's mis-citation (§4).

## 4. Verification & edge cases

**The scope's third stray was mis-cited, and the plan was right to correct it.** Verified by
opening the source: `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` is the `.gitignore:63`
blanket-`build/` shadowing at moment **2.1** — not the "client-side router seam at 1.10" the scope
names. `PROJECT_SCOPE.md:319` is a shipped fold, confirming finding F-02. E-006 carries the
corrected subject and moment.

**The `[OPEN-10]` orphan is real.** `GAME_DESIGN.md` §8 runs `[OPEN-1]` through `[OPEN-9]` and
stops; `ROADMAP.md:334` cites a tenth. Recorded as E-007, not answered (non-goal 13).

**Anti-vacuity, which is the class of failure this repo has hit before.** Three traps were
avoided deliberately and are commented in place: `FENCED_BLOCK.findall()` returns capture-group
tuples rather than blocks (`.sub()`/`.finditer()` used instead); casefolding the moment *set*
would make AC 2's `H2` assertion literally false (case-insensitivity applied at the comparison
site); and AC 10's register assertions would pass on substrings twice over — `DESIGN.md` inside
`GAME_DESIGN.md`, and `Escalation` in the queue's own prose — so they assert against table rows
using distinctive anchors.

**Regression posture.** Additive apart from three one-line skill bullets and two test extensions.
The extension most likely to bite later is AC 18: any bad relative link in a root document is now
a build failure. Measured clean today (0 dead links across 25 scanned files), so the cost lands on
future edits, which is the intended effect.

**One self-inflicted defect, caught and repaired.** Using PowerShell `Set-Content -Encoding utf8`
to rewrite three `Source:` citations double-encoded every em dash and added a BOM — exactly what
the plan's §8 conventions forbid ("Windows dev, Linux CI. Don't write files with PowerShell
`Set-Content`/`Out-File`"). Reversed via the cp1252 round-trip and verified: no BOM, 49 em dashes,
6 section signs, 0 mojibake, LF endings throughout.

**Measurement note.** `Measure-Object -Line` reports `CLAUDE.md` at HEAD as **181** where
`(Get-Content).Count` reports **221** — a 40-line under-report, concretely confirming the defect
the scope logged as risk 15 (`update-docs/SKILL.md` prescribes the wrong command). Out of scope
here; worth its own bugfix request.

## 5. Findings resolved

The acceptance panel ran 13 agents — 6/6 reviewers, 5/5 verifiers, meta-audit ran, **0 findings
unverified**, 0 degraded lenses. 21 confirmed findings; the independent verifier refuted none.
Verdict `fix`. All 21 are resolved below.

| # | Sev | Finding | Resolution |
|---|---|---|---|
| C-01 | **blocker** | A malformed entry heading is invisible to every guard **and** its field bullets bleed into the preceding entry, overwriting its parsed `Source:`/`Assumed:` | **Fixed, both halves.** Reproduced first: an intruder made `unknown_moments` report `[('E-008','9.9')]` — indicting an innocent entry — and replaced E-008's `Source:` with `` `INTRUDER.md` ``. Bodies are now bounded by the next `###` heading of *any* kind, and `malformed_headings()` rejects any non-entry `###` in the entry sections. This also makes `ESCALATIONS.md`'s own carve-out true, which it was not |
| C-02 | major | AC 19 unmet — both map lines landed with nothing asserting them | **Fixed.** `test_both_project_maps_name_the_escalation_queue`; proven to bite |
| C-03 | major | Phase 5 close-out had not run | **Fixed** — this report, the status rollover, and the `_done/` move |
| C-04 | major | The `/commit` rail closed the drain hole for item rows but not phase headers, where two seeds live | **Fixed.** Both the rail and the intake bullet widened to the phase half of the moment vocabulary. Faithful to AC 15's wording, so a scope gap rather than a deviation |
| C-05 | major | The worked example was an `open` entry bearing on `1.3` — the first live drain at the item H1 blocks would return a fabricated hit | **Fixed.** Retargeted to `post-v1`, subject changed, dead `Source:` replaced, and one line added saying E-000 is a template and must never be answered |
| M-01 | minor | `ROADMAP.md`'s Phase 1 prose marks H1 landed while the H1 row still reads `IN-PROGRESS` | **Handed to `/commit`** — it flips the row in the same commit, which is the intended sequence and the only sanctioned path. Flagged in §7 so it cannot be missed |
| M-02 | minor | `test_every_status_comes_from_the_closed_vocabulary` raised `KeyError` instead of its diagnostic | **Fixed** — `.get()` on both sides |
| M-03 | minor | `FIELD`'s `\s*` crossed newlines, so a blank value swallowed the next line and indicted two innocent fields | **Fixed** — `[ \t]*`, plus a non-emptiness assertion since `Assumed:` is the load-bearing field |
| M-04 | minor | A backticked `Bears on:` failed with a message asserting the moment doesn't exist | **Fixed** — backticks tolerated at the comparison site, and the format table now states the canonical form |
| M-05 | minor | Three seeds cited `ROADMAP.md:217-222` — the very lines this change rewrote into a pointer back at them | **Fixed** — pinned to `@ a408d4f`, verified to carry the pre-migration text |
| M-06 | minor | `Source:` was the one pointer in a pointer-guarding feature that nothing checked | **Fixed** — `unresolved_sources()` asserts the path exists (line numbers deliberately unchecked) |
| M-07 | minor | The widened root-document scan had no anti-vacuity assertion | **Fixed** — `test_the_root_documents_are_actually_scanned` |
| N-01…N-06 | nit | Filesystem-vs-index glob undocumented; a false `_done/` clause in a new comment; E-001 citing `:248` as an "exit condition" when it is the *Proves* line; E-003 anchored on the bare word "autonomous"; `section_body` matching by substring rather than line boundary; `/commit`'s frontmatter under-describing its own inventory | **All six fixed.** The `_done/` clause was factually wrong and I wrote it; the E-003 anchor is now `stage dispatch be autonomous`, verified unique |
| Q-01 | question | The change was staged before review, mooting `/commit`'s staging guard | **Explained, not silently accepted** — staging was *required* for AC 22, since `test_no_leaks` reads `git ls-files`. Flagged in §7 for `/commit` to re-derive |
| Q-02 | question | `CLAUDE.md` named the queue but never said when to read it | **User approved** the fold into the existing `[OPEN-N]` bullet; rewritten to two lines so AC 23 holds |
| Q-03 | question | The only `1.3` entry omitted the correction-event question that actually threatens the ledger | **User approved** — added as E-009 |

**Meta-audit findings.** Four, all accepted: the panel's headline arithmetic contradicted its own
ledger (this report counts independently); `requests/README.md` landed with no ledger row and no
lens examining it (recorded in §2 as checklist row 16, covered by no numbered AC); the seam tests'
self-declared vacuity weakness was unrecorded (stated in §6); and a severity-provenance nit.

## 6. Manual gates & user-run steps

- **AC 24 is yours and is not claimed.** At item 1.3's pickup, check that E-008 and E-009 surface
  without you asking; that you can answer one by editing `ESCALATIONS.md` alone with no build
  running; and that the parked context reads as useful rather than as noise.
- **The three seam tests assert the bare filename** (decision G7). Stated weakness, unchanged: they
  also pass if `ESCALATIONS.md` survives in a sentence that no longer instructs anyone. The seam is
  a read rather than a gate, so a substring is proportionate — but it is not proof the instruction
  still makes sense.
- **`unconfirmed`: whether the drain cadence actually fires.** It assumes every item boundary passes
  through `/make-feature-request`, which ADR 0010's entry condition does not guarantee for doc
  edits. The whole cadence rests on it, and nothing here tests it.
- **`inferred`, not verified: the seed moments** for E-001/E-002/E-003, and the 1.8/2.1 moments on
  the recovered strays (the 1.1 panel's judgment as of 2026-08-14). Labelled as such in each entry.

## 7. Hand-off

Ready for `/commit`. Three things it must know:

1. **The eleven paths were staged deliberately, before review** — AC 22 required it, because
   `test_no_leaks.py` scans the git index rather than the working tree. Re-derive the staged set so
   the secrets/bulk-data refusal runs for real rather than accepting a pre-populated index.
2. **`ROADMAP.md`'s H1 row must flip to `DONE` in this same commit.** The Phase 1 status prose
   already reads as though H1 landed, so the document contradicts itself until the row moves. Not
   hand-edited here on purpose — `/commit` owns that column, against the diff.
3. **Its own Step 4 now has a third rail**, added by this change: when flipping a row to `DONE`,
   surface open entries naming it. Nothing in this commit's diff is blocked by one.

After the commit: the branch is 3 commits behind `main` (dependency config, a bugfix intake, a
lockfile bump — none touching `ROADMAP.md` or `CLAUDE.md`), so its PR will need the same
`gh pr update-branch` the last two did. Opening and landing the PR stays the user's call.

**Follow-up surfaced by this build, not fixed here:** `update-docs/SKILL.md`'s `Measure-Object
-Line` under-reports line counts by 40 on `CLAUDE.md` (§4). It already has a written bugfix
request in the tree from a prior session's sibling defect; this is a second instance worth
attaching to it.

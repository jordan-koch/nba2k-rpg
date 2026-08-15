> **Status:** planned · created 2026-08-15 · decided · next: implement

# Implementation Plan — Escalation Queue (Harness H1)

> **One-line goal:** a root `ESCALATIONS.md` where a decision can be parked instead of interrupting,
> with a parser guard proving every entry names a real roadmap moment and three one-line seams that
> actually read it · **Target component:** `ESCALATIONS.md`, `tests/test_escalations.py`, and
> one-line edits to three skills and four documents.

**Every path in this document is repo-relative, deliberately.** This artifact is itself tracked and
scanned by `tests/test_no_leaks.py`, which fails the build on drive-letter paths — the repo is
public. Both adversaries independently flagged the draft's machine-absolute paths as a blocker.

## 1. Onboarding — read these first

A worker mid-build hits a judgment call and has exactly two moves: interrupt, or guess silently.
The second leaves no trace — a decision made by default is indistinguishable from one nobody
noticed. H1 builds the third move: record the question, the alternatives, and the assumption
actually taken; name the roadmap moment it bears on; keep going. A pytest guard makes the pointer
mechanical. Three one-line seams give the queue something that reads it. It ships with **eight**
real seed entries, so it is an artifact with content on day one rather than an empty schema.

`ROADMAP.md`'s H1 row carries `Blocks: 1.3` — binding. Item 1.3 `correction-by-append` cannot start
until this lands.

| Read | Why |
|---|---|
| `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md` | The decided contract — **consume it, do not re-open**. 24 tier-tagged acceptance criteria, seven Decisions, the F-33 carve-out. Two of its pointers are corrected below; its decisions are not |
| `ROADMAP.md` | Both the spec of record **and** the parser's input. H1 row at `:197`; *Why H1 exists* `:200-204`; *Parked, not scheduled* `:217-222` (the paragraph AC 13 reduces to a pointer); the "/commit maintains this table" blockquote `:139-142`; six table shapes the parser must discriminate |
| `tests/test_layering.py` | The idiom `tests/test_escalations.py` copies near-exactly. Docstring `:1-17` states **why** the guard is a pure function proven against `tmp_path` — subagents have read-only git, so you cannot prove a guard red by breaking a tracked file and reverting. Pure guard `:38-67`, red/green pair `:85-100`, failure-message test `:112-123` |
| `tests/test_repo_structure.py` | Two edits land here. Module docstring `:1-9`, module-level regex constants `:21`/`:30`, `test_core_documents_exist` `:243-246`, the `_read` helper `:256-257` and substring idiom `:260-283`, and `test_index_stage_cells_match_their_artifact_status_headers` `:286-319` — the landmine every phase must respect |
| `tests/test_request_links.py` | AC 18 extends this. `SCANNED_TREES` `:24`, `FENCED_BLOCK` `:26`, `_scanned_files` `:31-37` (calls `rglob` **per directory** — the reason AC 18 needs a non-recursive root glob, not a new tree entry), the `_done/` skip `:36`, `_dead_links` `:40-64` |
| `requests/feature-requests/README.md` | The pipeline contract. Status blockquote form `:104`, and the grammar at `:106` — `intake → scoped → planned → implemented`. **The token is `planned`, not `plan`.** Index at `:112-117`; H1's row is `:116` |
| `requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md` | Source of two recovered strays: `:369` (OpenAPI snapshot test, moment 1.8) and `:370` (OpenAPI→TypeScript codegen, moment 1.8). Its `:319` router line is **not** a stray — finding F-02 ruled it a shipped fold |
| `requests/feature-requests/_done/1.1-app-shell/IMPLEMENTATION_PLAN.md` | The gold-standard plan to imitate, **and** the source the scope mis-cites. Read `:859-861` yourself — it is the `.gitignore:63` blanket-`build/` shadowing at moment **2.1**, not a router seam at 1.10 |
| `.claude/skills/commit/SKILL.md` | Step 4 "Roadmap status" `:109-144` — the diff→status table `:118-122` and the two rails `:133-138` where the drain-hole bullet joins as a third. Also the only sanctioned commit path: every phase ends here |
| `pyproject.toml` | The gates AC 21 names. ruff `line-length = 100` `:54` and the lint select block `:58-75` (PTH forbids bare `open()`); mypy `strict = true` `:82` with `files = ["src", "tests"]` `:84` — the new module is fully type-checked, zero new `# type: ignore` |

## 2. Architecture map

Process/docs work with exactly one Python artifact. Nothing under `src/` or `app/` moves (non-goal
9), no CI job is added (non-goal 11 — the tests join the existing "Lint, types, tests" job), and
nothing reads the queue at runtime (non-goal 10).

**Data contracts: N/A, verified by probe rather than assumed** (2026-08-15). `datasets/manifest.json`,
`careers/`, `rulesets/`, `lib/`, and `build/` are all absent; `src/rpg_core/` contains only
`__init__.py`. There is no logical dataset name to register, no grain to prove, no ledger or ruleset
to pin. ADR 0003's append-only rule and ADR 0004's version immutability are genuinely not engaged —
recorded so a cold implementer does not go hunting for a seam to honor them at. This plan therefore
carries **no** data-contracts section.

**The root today:** five tracked `*.md` — `CLAUDE.md` (221 lines, measured), `DESIGN.md`,
`GAME_DESIGN.md`, `README.md`, `ROADMAP.md`. `ESCALATIONS.md` becomes the sixth, and the first one
covered by the link checker once AC 18 lands.

## 3. Phased implementation

Each phase ends green on `uv run pytest` · `ruff check` · `ruff format --check` · `mypy`, then lands
through `/commit`. CI re-runs the same gates on the PR.

### Phase 0 — Pre-flight: verify inherited beliefs, measure the baseline (no commit)

**Goal.** Start from a measured baseline and discharge by measurement every belief a later phase
builds on.

**Steps**

1. **Confirm the branch — do not create one.** `git branch --show-current` must print
   `phase1/escalation-queue`. Git is read-only beyond this: never
   `checkout`/`reset`/`restore`/`clean`/`stash`.
2. **Reconcile the status lockstep this plan's own arrival broke.** `test_index_stage_cells_match_their_artifact_status_headers`
   compares **every** `*.md` directly under the request directory against the Index cell. This plan
   opens at `planned` while `FEATURE_REQUEST.md` and `PROJECT_SCOPE.md` still read `scoped`, so the
   suite is red until all four agree. Set both artifacts' blockquotes and the Index cell at
   `requests/feature-requests/README.md:116` to `planned`. *(`reviews/` is exempt — the glob is
   non-recursive.)*
3. **Record the baseline green**, after step 2: `uv run pytest -q` (expect 55 passed), `ruff check`,
   `ruff format --check`, `mypy`. Any red is pre-existing, not caused by this work.
4. **Measure the `CLAUDE.md` budget with the command AC 23 names:** `(Get-Content CLAUDE.md).Count`.
   Expect 221. Do **not** use `Measure-Object -Line` — `.claude/skills/update-docs/SKILL.md`
   prescribes it and it under-reports (scope risk 15; its own bugfix request, out of scope here).
5. **Verify the parser's input rather than trusting it.** Count unique leading cells in `ROADMAP.md`
   matching `^(\d+\.\d+|H\d+)$`. Expect **38**. If it is not 38, the roadmap moved under this plan
   and AC 2's `>= 30` floor must be re-checked before the test is written.
6. **Verify the recovered strays by opening them** — one scope pointer is wrong and a cold agent
   would otherwise copy it verbatim. `_done/1.1-app-shell/PROJECT_SCOPE.md:369` = OpenAPI snapshot
   test (moment 1.8); `:370` = OpenAPI→TypeScript codegen (moment 1.8);
   `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` = the `.gitignore:63` blanket-`build/`
   shadowing, moment **2.1** — *not* the "client-side router seam at 1.10" the scope calls it. The
   count of three strays is unaffected; only the third one's subject and moment change.
7. **Verify the `[OPEN-10]` orphan** — `ROADMAP.md:334` cites it; `GAME_DESIGN.md` §8 ends at
   `[OPEN-9]`.

**Acceptance.** Branch confirmed; four status tokens agree at `planned`; four gates green; 221
measured; 38 ids measured; three strays and the orphan read with your own eyes.

**Commit note.** No commit — except step 2's lockstep fix, which rides with Phase 1.

### Phase 1 — `ESCALATIONS.md`: header, pinned format, eight seeds

**Goal.** Land the queue and stop `ROADMAP.md` being a second source of truth for three entries.
Satisfies core items 1–4, 6, 7 and folds 1, 2, 3, 6, 8.

**Steps**

1. **Create `ESCALATIONS.md` at the repo root** (core item 1, Decision 7).
2. **Write the boundary header first** — the load-bearing deliverable, written for a worker about to
   add an entry. In order: (a) what the queue is for; (b) a **register map** disambiguating it from
   the five existing parking places — `GAME_DESIGN.md` §8 `[OPEN-N]`, `DESIGN.md` §2, `DESIGN.md` §4
   (the sharpest overlap — bullets with no ids and no named moment), ADR 0010's Stage plan, and
   `/diagnose-bug`'s Escalation; (c) the **ADR-0011 trigger** verbatim from Decision 6 — the first
   time someone proposes absorbing `[OPEN-N]` or `DESIGN.md` §4, that is the second litigation and
   ADR 0011 gets written then; (d) one line recording that a `ROADMAP.md` `Blocks` cell stops work
   while a queue entry **never** does; (e) the **F-33 carve-out in both halves** — no open entry
   stops a stage, fails a build, or gates a merge, *and* the file is not exempt from ordinary CI: a
   malformed entry fails `tests/test_escalations.py` exactly as malformed markdown fails any other
   guard; (f) the name disambiguation (fold 8).
3. **Pin the format — six required fields, exactly.** Phase 2's regexes are written against this
   shape, so change one and change both. Heading `### E-NNN — <question title>`; body one bullet
   each: `- **Bears on:** <moment>` · `- **Parked:** <YYYY-MM-DD>` · `- **Assumed:** <what was
   actually done, or the literal "none — not hit yet">` · `- **Source:** <path, optional :line>` ·
   `- **Status:** open`. **Six, not five** — finding F-26 caught `Source:` being required by the
   tests while absent from the pinned format.
4. **`Status:` vocabulary is exactly `open` | `resolved`** (Decision G4). A resolved entry's
   resolution pointer lives in the **body**, not as a seventh field.
5. **Add the worked example** inside a fenced block (fold 6). It must parse green under the same
   regex and field guards as real entries — that is AC 11, and it is how goal 1 becomes mechanical.
6. **Write the eight seeds** under `## Open`:
   - **E-001** serviceability gate → `Phase 3` *(grounded: `ROADMAP.md:248`)*
   - **E-002** design/UX specialist → `Phase 3` *(inferred)*
   - **E-003** autonomous stage dispatcher → `H2` *(inferred)*
   - **E-004** OpenAPI snapshot test → `1.8` · Source `_done/1.1-app-shell/PROJECT_SCOPE.md:369`
   - **E-005** OpenAPI→TypeScript codegen → `1.8` · Source `…/PROJECT_SCOPE.md:370`
   - **E-006** `.gitignore:63` blanket `build/` shadows the Phase 2 builder pattern → `2.1` ·
     Source `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861`
   - **E-007** the `[OPEN-10]` orphan → `post-v1` · recorded, **not** answered (non-goal 13)
   - **E-008** does a superseding correction event carry the full replacement box score or a delta?
     → `1.3` · a real open question under ADR 0003 *(added by decision G2 so AC 24's first check has
     something to surface — not fabricated to turn a criterion green)*

   E-001/002/003 carry `inferred` in `Assumed:`, per decision G1.
7. **Reduce `ROADMAP.md:217-222` to a pointer** (AC 13). Preserve the paragraph's substantive
   observation — that "serviceable" is a v1 constraint in both directions and is nowhere defined or
   tested. Also update `ROADMAP.md:168-170`'s prose, which says "Harness row H1 is in flight."

**Acceptance.** Queue exists at root with header, register map, trigger, carve-out, worked example,
and eight entries; `ROADMAP.md` no longer enumerates the three hypotheses; `uv run pytest` green.

### Phase 2 — `tests/test_escalations.py`: the parser guard

**Goal.** Make the pointer mechanical. Satisfies AC 1–13 and core item 5.

**Steps**

1. **New module** (core item 5), opening `from __future__ import annotations`.
2. **Module docstring in the house idiom** (AC 1), explaining *why*: the three hypotheses failed by
   sitting in prose with their moments named only in the prose describing them. State, as
   `test_layering.py:12-16` does, that the parser is proven both ways against `tmp_path` because
   subagents have read-only git.
3. **Module-level constants** in the `test_repo_structure.py:21`/`:30` convention: `REPO_ROOT`,
   queue/roadmap paths, `FENCED_BLOCK`, `TABLE_ROW`, `ITEM_ID` (`^(?:\d+\.\d+|H\d+)$`),
   `PHASE_HEADING`, `ENTRY`, `FIELD`, `REQUIRED_FIELDS`, `STATUS_VALUES = frozenset({"open",
   "resolved"})`.
4. **`_item_ids(text) -> set[str]`** — first cell of every table row, kept only on
   `ITEM_ID.fullmatch`. **Comment the F-27/F-06 correction inline:** emptiness is *not* the
   discriminator; the v1 scope tables lead with `**Creation**`-style bold text.
5. **`known_moments(roadmap_text) -> frozenset[str]`** — `_item_ids` plus every `PHASE_HEADING`
   capture plus `post-v1`. Strip fenced blocks first (`ROADMAP.md` carries a fenced ASCII diagram).
   **Compare case-insensitively at the comparison site, not by casefolding the returned set** —
   finding [16] showed casefolding the set makes the scope's AC 2 assertion (`H2` present) literally
   false.
6. **`parse_entries(text) -> list[Entry]`** — strip the fenced worked example for the *entry* pass,
   then parse it separately for AC 11.
7. **The guard tests**, per AC 2–13. Three traps the adversaries found, each to be avoided
   explicitly:
   - **`FENCED_BLOCK.findall()` returns capture-group tuples, not blocks** (finding [15]) — the
     existing regex has groups. Use `.sub()` to strip, or `.finditer()` with `.group(0)`.
   - **AC 3 locates the non-item tables by heading anchor**, not hardcoded offsets (decision G5) —
     `### In scope — the engine`, `### In scope — the application`, `### Out of scope`, and
     `## Open questions, by the phase that answers them`, each up to the next heading. Hardcoded
     offsets are the brittleness F-28 rejected for the id set. **Assert each slice is non-empty**
     (finding [4]) — the anchors contain em dashes and a silent miss makes the test vacuous.
   - **AC 10's register guard is vacuous twice over as written** (finding [3]): `"DESIGN.md"` is a
     substring of `"GAME_DESIGN.md"`, and `"Escalation"` appears in the queue's own prose. Assert
     against the register-map **table rows** specifically, and use `GAME_DESIGN.md` and
     `diagnose-bug` as the distinctive anchors.
8. **Prove red and green against `tmp_path`** (AC 5), fabricating **both** the queue and the roadmap
   so the green case is hermetic (finding F-07).
9. **The three seam substring tests live in this module** (decision G6) and assert the bare filename
   `ESCALATIONS.md` (decision G7).

**Acceptance.** `uv run pytest tests/test_escalations.py -q` green; the red fixture produces exactly
one violation naming entry id and moment; `mypy` clean with full annotations and zero new
`# type: ignore`. **Do not pin an exact entry count** (finding [13]) — assert `>= 8`.

### Phase 3 — Discoverability and the folded doc fixes

**Goal.** Satisfies AC 17–20, 23 and folds 4, 5, 7, 9.

**Steps**

1. **AC 17 / fold 4** — extend `test_core_documents_exist` (`tests/test_repo_structure.py:243-246`)
   to include the queue, **and fix its docstring in the same edit**: it says "The three documents
   that carry the design" over a five-name tuple, so it already lied before this change.
2. **AC 18 / fold 5** — extend `tests/test_request_links.py` to root-level `*.md`. **Do not add
   `REPO_ROOT` to `SCANNED_TREES`** — `_scanned_files` (`:31-37`) calls `rglob` per entry and would
   sweep `app/node_modules/`, `.venv/`, `var/`, and the deliberately-exempt `_done/` tree. Add a
   separate **non-recursive** `REPO_ROOT.glob("*.md")` and dedupe. Update the module docstring.
3. **AC 19 / core item 8** — exactly one line inside `CLAUDE.md`'s project-map fenced block
   (`:51-67`), and one row in `README.md`'s (`:55-73`). Inside the fences deliberately, so they add
   no link-check surface now that AC 18 has landed.
4. **AC 20 / fold 9** — fix `CLAUDE.md:216`: "Nine decisions are settled" → "Ten". One word, zero
   line delta.
5. **Fold 7** — one line in `requests/README.md` beside the three-track table linking the queue.
   `requests/` is already in `SCANNED_TREES`, so this is the one pointer that cannot silently rot.

**Acceptance.** Both project maps name the queue (substring-tested); deletion fails the build;
`(Get-Content CLAUDE.md).Count` ≤ 222; link checker green over root documents.

### Phase 4 — The three read seams

**Goal.** Kill the inertness risk all three scopers named independently. Satisfies AC 14–16 and core
items 10–12. **One bullet each** — the constraint that keeps this inside the "no skill behavior
changes" non-goal.

**Steps**

1. **AC 14 / Decision 1** — one bullet in `.claude/skills/make-feature-request/SKILL.md` Step 2:
   when grounding a roadmap item, open the queue and surface any open entry whose `Bears on:` names
   this item's moment. Adds a **read** to a checklist; changes no decision logic.
2. **AC 15 / Decision 5** — one bullet in `.claude/skills/commit/SKILL.md` Step 4, as a third rail
   after the two at `:133-138`: when flipping a roadmap row to `DONE`, surface open entries naming
   it. Closes the F-32 drain hole. Keep it to one bullet — that skill's keep-it-lightweight posture
   is explicit, and a gate people route around is worse than no gate.
3. **AC 16 / Decision 3** — one line in `.claude/skills/diagnose-bug/SKILL.md`'s Escalation block
   (`:132-142`): also park a queue entry naming the moment the bug bears on. **Pointer only** — the
   RCA keeps its structure and the evidence trail is not duplicated. Preserves the non-blocking
   property exactly: the bug still waits; the queue only remembers that it is waiting.
4. **Links must resolve.** `.claude/skills/` is in `SCANNED_TREES`, so any markdown link in these
   three files resolves relative to the skill file: `../../../ESCALATIONS.md`.

**Acceptance.** Three substring tests green; `uv run pytest tests/test_request_links.py -q` green.

### Phase 5 — Close out

**Goal.** Prove the acceptance contract, reconcile the status lockstep, let `/commit` advance H1.

**Steps**

1. Full local gate from a clean shell — all four exit 0, zero new `# type: ignore` (AC 21).
2. **AC 22** — `tests/test_no_leaks.py` green on a run where the queue is **tracked**. Re-read all
   eight entries by eye: the repo is public, and the guards catch drive-letter paths, home
   directories, and emails — not indiscretion.
3. **AC 23** — re-measure `(Get-Content CLAUDE.md).Count` ≤ 222.
4. Write `IMPLEMENTATION_REPORT.md` as an acceptance ledger over all 24 criteria, each with the
   command run and its result. **Mark AC 24 USER-RUN and do not claim it.**
5. **Reconcile the status headers again** — roll all four artifact blockquotes *and* the Index cell
   to `implemented` in the same commit. Precedent: all four `_done/1.1-app-shell/*.md` read
   `implemented` against an `implemented` cell.
6. Move the item directory once into `requests/feature-requests/_done/H1-escalation-queue/` and
   repoint the Index link. **This is a directory move, and your git is read-only** — use file tools,
   or hand the `git mv` to the user (finding [20]).
7. **Let `/commit` advance `ROADMAP.md`'s H1 row against the diff** — never hand-edit it.

**Acceptance.** 23 of 24 criteria met with evidence; AC 24 handed to the user; H1 `DONE`.

## 4. Testing & verification

The guard is the deliverable's proof, and its own failure modes are the risk. Three levels:

- **Unit, against `tmp_path`** — the parser proven red *and* green on fabricated queue+roadmap
  pairs, never by mutating a tracked file (subagents have read-only git).
- **Integration, against the real files** — every entry's moment resolves; the non-item tables
  contribute zero ids; the worked example parses like a real entry.
- **Anti-vacuity, which is the one that matters** — the entry regex must have matched something
  (AC 4), each heading-anchor slice must be non-empty (finding [4]), and the register assertions
  must not pass on substrings (finding [3]). A guard that passes over an empty list is worse than no
  guard, and this repo has hit that failure before.

**Regression posture.** The change is additive apart from three one-line skill bullets and two test
extensions. The extension most likely to bite is AC 18 — widening the link checker to root documents
turns any bad relative link in a root `*.md` into a build failure. Measured clean today, so the risk
is future edits, which is exactly the intended effect.

## 5. Decisions

Carried from the scope (1–7) plus the panel's (G1–G7):

| # | Decision | Rationale |
|---|---|---|
| 1–7 | *(the scope's seven)* | See `PROJECT_SCOPE.md` §Decisions — read seam, no writes, `/diagnose-bug` pointer, orphan recorded not answered, `/commit` drain check, no ADR 0011 yet, root + deletion guard |
| G1 | Seed moments: `Phase 3` / `Phase 3` / `H2` | Only the first is grounded in text (`ROADMAP.md:248`); the others are a reading. All three labelled `inferred`. Changing one later is a one-line edit with no migration |
| G2 | **Add an eighth seed (E-008) for moment 1.3** | AC 24's first check had nothing to surface — none of the seven seeds named 1.3. E-008 is a real open question under ADR 0003, not a fabrication to turn a criterion green. The panel explicitly refused the fabrication route. **Reconciliation for stage 4:** the scope's AC 12 says "all **seven** seeds"; under this decision it reads as **eight**, and the additional entry is E-008. Verify eight, not seven — and treat AC 12's count as amended here rather than as a failed criterion |
| G3 | Leave `ROADMAP.md:334`'s `[OPEN-10]` row in place | Non-goal 13: recorded, not answered. Differs from the three hypotheses — those were *duplicated* by the migration, `[OPEN-10]` is an orphan the queue merely indexes |
| G4 | `Status:` is `open` \| `resolved`; resolution pointer in the body | A third value is unwarranted when the scope dropped `Supersedes:`. Body not a seventh field — F-26 exists precisely because a field appeared in the tests but not the format |
| G5 | AC 3 locates tables by **heading anchor**, not line offsets | Faithful-intent reading, recorded rather than substituted silently. Hardcoded offsets are the brittleness F-28 rejected, and ADR 0010 just rewrote that region of `ROADMAP.md` |
| G6 | Seam tests live in `tests/test_escalations.py` | One module is the single place a cold agent reads to see what holds the queue up. Purely legibility; recorded so it is not re-argued mid-build |
| G7 | Seam tests assert the bare filename | It appears in none of the three skill files today, so it is a clean anchor that survives rewording. Weakness stated: it also passes if the filename survives in a sentence that no longer instructs anyone |

**Disposed en bloc:** G3, G6, G7 — recorded here individually so the trail survives the batching.

## 6. Risks & gotchas

1. **The guard going silently vacuous** — the dominant risk, and this repo has hit it before. AC 4
   and the non-empty slice assertions are the answer.
2. **`FENCED_BLOCK.findall()` returns tuples**, not blocks. The obvious reuse is wrong.
3. **Casefolding the moment set** makes AC 2 literally false. Compare case-insensitively at the
   comparison site instead.
4. **The status lockstep is a latent red** at both ends — when this plan lands (Phase 0 step 2) and
   when the report lands (Phase 5 step 5). Every `*.md` directly under the request dir must match
   the Index cell.
5. **Roadmap renumbering tax.** Item ids are hand-edited cells, and ADR 0010 just deleted two columns
   from every table. A renumbering silently orphans entries.
6. **Scope creep has a binding cost** — `Blocks: 1.3` is binding, and 1.3 is the append-only
   correction model ADR 0003 treats as load-bearing.
7. **Public repo.** Entries record assumptions taken when nobody was sure, world-readable forever.
   The guards catch paths and emails, not indiscretion.
8. **`unconfirmed`: whether the drain cadence actually fires.** It assumes every item boundary passes
   through `/make-feature-request`, which ADR 0010's entry condition does not guarantee for doc
   edits. The whole cadence rests on it.
9. **`inferred`, not verified: the seed moments** for E-001/002/003 and the 1.8/2.1 moments on the
   recovered strays — the latter were the 1.1 panel's judgment as of 2026-08-14.
10. **Phase 1 is the heaviest phase** and the summary's "pure process/docs work" understates it
    (finding [31]). Budget accordingly; it is eight entries plus the header plus a roadmap edit.

## 7. Files to touch (checklist)

- [ ] `ESCALATIONS.md` — **new**, root
- [ ] `tests/test_escalations.py` — **new**
- [ ] `ROADMAP.md` — `:217-222` reduced to a pointer; `:168-170` prose; H1 row via `/commit` only
- [ ] `tests/test_repo_structure.py` — `test_core_documents_exist` + its docstring
- [ ] `tests/test_request_links.py` — non-recursive root glob + docstring
- [ ] `CLAUDE.md` — one project-map line; `:216` "Nine" → "Ten"
- [ ] `README.md` — one project-map row
- [ ] `requests/README.md` — one line beside the three-track table
- [ ] `.claude/skills/make-feature-request/SKILL.md` — one bullet, Step 2
- [ ] `.claude/skills/commit/SKILL.md` — one bullet, Step 4
- [ ] `.claude/skills/diagnose-bug/SKILL.md` — one line, Escalation block
- [ ] `requests/feature-requests/H1-escalation-queue/FEATURE_REQUEST.md` — status
- [ ] `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md` — status
- [ ] `requests/feature-requests/H1-escalation-queue/IMPLEMENTATION_PLAN.md` — status
- [ ] `requests/feature-requests/H1-escalation-queue/IMPLEMENTATION_REPORT.md` — **new**, stage 4
- [ ] `requests/feature-requests/README.md` — Index cell `:116`

## 8. Conventions (bake these in)

- **Commits go through `/commit` only.** Never `git commit` ad hoc.
- **Subagent git is read-only** — no `checkout`/`reset`/`restore`/`clean`/`stash`. Bubble a
  destructive-git *need* upward.
- **`ROADMAP.md` statuses are advanced by `/commit` against the diff**, never hand-edited.
- **Label epistemics** — `measured` / `verified` / `inferred` / `assumed` / `unconfirmed` mean
  different things, and entries carry them.
- **The repo is public.** No machine-specific paths, ids, or personal identifiers in tracked files —
  including this plan and the `reviews/` trail.
- **Windows dev, Linux CI.** Don't write files with PowerShell `Set-Content`/`Out-File`; use the
  file-editing tools.
- **mypy is strict over `src` and `tests`.** Full annotations, zero new `# type: ignore`.
- **ruff `line-length = 100`**, and PTH forbids bare `open()`.
- *Not applicable here, stated so nobody reaches for them:* resolve-by-name (no datasets),
  append-only ledger (no `careers/`), ruleset immutability (no `rulesets/`), cost-side-only pricing
  (no economy). Verified absent by probe.

## 9. Code-grounding verification

**67 code references emitted; 64 parseable file/line refs independently re-checked against the
working tree; 0 unresolvable.** Panel health: 3/3 planners, 2/2 adversaries, 1/1 meta-audit, 0
degraded lenses, 42 findings (3 blockers, 14 majors).

Two references in the **upstream scope** were corrected by the panel and verified by hand here:

| Cited | Verified |
|---|---|
| Third stray = "client-side router seam", moment 1.10 | **Corrected** — `_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` is the `.gitignore:63` blanket-`build/` shadowing, moment **2.1**. The router text at `PROJECT_SCOPE.md:319` was already ruled a shipped fold by F-02 |
| Artifact stage token `plan` | **Corrected** — `requests/feature-requests/README.md:106` grammar is `planned`. The stage-3 skill template says `plan`; the repo's own grammar and the exact-word Index comparison win |

Three blockers were applied rather than asked, all objective: machine-absolute paths throughout the
draft (both adversaries, independently — this artifact is scanned by `tests/test_no_leaks.py`), and
the status lockstep this plan's own arrival breaks.

## References

- `requests/feature-requests/H1-escalation-queue/PROJECT_SCOPE.md` — the decided contract
- `requests/feature-requests/H1-escalation-queue/FEATURE_REQUEST.md` — the intake
- `reviews/plan-proposals.md` · `reviews/plan-adversarial.md` — this panel's raw trail
- `reviews/scope-proposals.md` · `reviews/scope-adversarial.md` — stage 2's trail
- `docs/decisions/0010-panels-by-default.md` — why this item runs the full pipeline
- `ROADMAP.md` · `tests/test_layering.py` · `tests/test_repo_structure.py` ·
  `tests/test_request_links.py` · `.claude/skills/commit/SKILL.md`

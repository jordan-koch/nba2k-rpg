# Acceptance Panel Trail — Escalation Queue (Harness H1)

Stage 4 adversarial acceptance panel, run 2026-08-21 against the completed working tree.
Raw, unfiltered. The disposition of each finding is in
[`../IMPLEMENTATION_REPORT.md`](../IMPLEMENTATION_REPORT.md) §5.

## Panel health

| Metric | Value |
|---|---|
| Agents | 13 — 13 done, 0 errored, 0 skipped, 0 empty |
| Reviewers | **6 / 6** — `acceptance`, `fidelity`, `correctness`, `edgecases`, `ledger`, `skill-quality` |
| Verifiers | **5 / 5** — 4 location-grouped batches (cap 4) + the standalone acceptance-ledger verifier |
| `findings_unverified` | **0** |
| Meta-audit | ran (`meta_ok: 1`) |
| Degraded lenses | **none** |
| Blocker/major raw → deduped | 19 → 19 (no cross-lens duplicates merged) |
| Confirmed findings | 21 — 1 blocker, 4 majors, 7 minors, 6 nits, 3 questions |
| Refuted by the verifier | **none** — all 17 blocker/major submissions came back confirmed |
| Tokens / tool calls | 1,462,097 / 321 |
| Duration | ~29 min |

**Verdict: `fix`** — not `go` (one criterion outright unmet, one confirmed blocker) and nowhere
near `no-go` (on-plan, all gates green, every seed citation verified line-exact, no convention
violated).

## Roster and why it scaled that way

The diff bucketed into three areas — `tests`, `skills`, `docs` — with nothing under `src/`,
`app/`, `datasets/`, `rulesets/`, CI, or config. That drew the four core reviewers plus the
`ledger` and `skill-quality` specialists. The `ledger` lens verified **by inspection rather than
assumption** that the append-only rule, ruleset pinning, dataset-resolve-by-name and ADR 0008 are
genuinely not engaged: `src/rpg_core/` holds only `__init__.py`, no `careers/` exists, and no test
reads a real career.

## The blocker, reproduced independently before it was fixed

C-01 was filed `major` by four of five lenses and `blocker` by `edgecases`; the merge carried it at
blocker and disclosed the escalation rather than editing silently. I reproduced both halves myself
rather than accepting either reading.

Injecting `### E-9999 - Intruder` (four digits, hyphen instead of the pinned em dash) at the real
`## Resolved` offset:

```
entries counted : 8            <- intruder not counted; the seed-count floor cannot notice
unknown moments : [('E-008', '9.9')]   <- names an INNOCENT entry
bad statuses    : {'E-008': 'bogus'}   <- same
E-008 Assumed   : INTRUDER-ASSUMED     <- real entry's provenance overwritten
E-008 Source    : `INTRUDER.md`
```

Two distinct defects. The malformed entry is **invisible** — the count fails to grow rather than
shrinking, so no floor can see it. And because entry bodies were bounded by the next *valid* entry,
the intruder's field bullets bled into the preceding entry, and last-key-wins in the field dict
**overwrote a real entry's `Source:` and `Assumed:`** — provenance, in a world-readable permanent
record. Had the intruder used plausible values, nothing would have fired at all.

This also falsified a claim the shipped artifact printed about itself, at `ESCALATIONS.md:54-56`:
"a *malformed* entry fails `tests/test_escalations.py` exactly as malformed markdown fails any
other guard." Fixing it made that sentence true.

**Note on the first reproduction attempt:** it injected at the *prose* mention of `` `## Resolved` ``
in the header rather than the section heading, and so reproduced only the invisibility half. The
offset was re-derived from the `SECTION` regex before the finding was accepted.

## Confirmed findings

| # | Sev | Confidence | Finding |
|---|---|---|---|
| C-01 | blocker | high | Malformed entry heading invisible + overwrites the preceding entry's fields |
| C-02 | major | high | AC 19 unmet — both project-map lines shipped unguarded |
| C-03 | major | high | Phase 5 close-out had not run |
| C-04 | major | high | `/commit` drain rail item-scoped while Step 4 also flips phase headers, where two seeds live |
| C-05 | major | high | The fenced worked example was an `open` entry bearing on `1.3` — the first live drain at the item H1 blocks returns a fabricated hit |
| M-01 | minor | high | `ROADMAP.md` Phase 1 prose marks H1 landed while the H1 row reads `IN-PROGRESS` |
| M-02 | minor | high | Status-vocabulary test raises `KeyError` instead of emitting its diagnostic |
| M-03 | minor | high | `FIELD`'s trailing `\s*` crosses newlines; a blank value swallows the next line |
| M-04 | minor | high | A backticked `Bears on:` fails with a message asserting the moment doesn't exist |
| M-05 | minor | high | Three seeds cite `ROADMAP.md:217-222` — the lines this change rewrote into a pointer back at them |
| M-06 | minor | high | `Source:` is the one pointer in a pointer-guarding feature that nothing checks |
| M-07 | minor | high | The widened root-document link scan has no anti-vacuity assertion |
| N-01 | nit | high | Root glob is filesystem-based, diverging from the sibling guard's git-index idiom |
| N-02 | nit | high | The new `_scanned_files` comment misstates why `REPO_ROOT` is kept out of `SCANNED_TREES` |
| N-03 | nit | high | E-001 cites `ROADMAP.md:248` as an "exit condition"; `:248` is the *Proves* line |
| N-04 | nit | high | E-003's seed anchor is the bare word "autonomous", looser than the roadmap-side assertion |
| N-05 | nit | medium | `section_body` matches its anchor by substring, not at a line boundary |
| N-06 | nit | medium | `/commit`'s frontmatter description under-describes its own inventory |
| Q-01 | question | medium | The change was staged before review, mooting `/commit`'s staging guard |
| Q-02 | question | medium | `CLAUDE.md` names the queue but never says when to read it |
| Q-03 | question | medium | The only `1.3` entry omits the correction-event question that actually threatens the ledger |

Two verifier qualifications were carried forward rather than laundered:

- **V9** — C-04's implementation is *literally faithful* to scope AC 15's wording, so it is a gap
  the scope left open rather than a deviation; AC 15 stayed `met`. V9 also noted the intake bullet
  is item-scoped too, so fixing only the commit rail under-covers. Both were widened.
- **V16** — softened "contradicts ADR 0003" to "tension with" on the E-009 question. Adopted.
- **V6** — corrected the fidelity lens's count of untouched checklist rows from four to five.

## Meta-audit

Four findings, all accepted.

1. **major — synthesis arithmetic.** The merged report's headline claimed "21 of 24 criteria met"
   while its own ledger scored 20, and PLAN-P5's reconciliation summed to 25 of 24. The
   `IMPLEMENTATION_REPORT.md` ledger was therefore counted independently, row by row, rather than
   carried over.
2. **minor — coverage gap.** `requests/README.md` (fold 7) landed but has no ledger row and no lens
   examined it: no numbered AC covers it and Phase 3's acceptance list omits it, so it fell through
   the whole verification net. Recorded as checklist row 16 in the report.
3. **minor — dropped signal.** The module's own written admission that the three seam tests can go
   vacuous was unrecorded while AC 14/15/16 shipped as clean `met`. Now stated in the report's
   manual-gates section.
4. **nit — severity provenance.** C-01's escalation to blocker was disclosed against the lenses but
   not against the verify pass, where all six verdicts on it returned `major`.

## Gated decisions

Six surfaced. Four were dispositioned as objective and fixed without asking (C-04, C-05, the AC
7/AC 8 rescoring — which dissolved once C-01 was fixed — and the Q-01 staging question, explained
rather than silently accepted). Two went to the user:

- **Q-02** — spend the `CLAUDE.md` budget on a "when to read it" clause. **User: yes**, folded into
  the existing `[OPEN-N]` bullet, rewritten to two lines so AC 23's 222 cap still holds.
- **Q-03** — add E-009 (does a correction event pin the ruleset version live, or inherit the
  corrected event's?). **User: yes.** Bears on `1.3`, doubling AC 24's day-one signal at the item
  H1 blocks.

## What the panel verified positively

Worth recording, because a trail that lists only defects misrepresents the review.

- All four gates re-run independently by the panel: 72 passed at review time, `ruff check` clean,
  `ruff format --check` clean over 64 files, `mypy` clean over 16 files, `CLAUDE.md` 222 vs 221.
- **Both the auditor and the independent verifier opened every seed's `Source:` citation** and
  found them line-exact — including the plan's correction of the scope's mis-cited third stray
  (`_done/1.1-app-shell/IMPLEMENTATION_PLAN.md:859-861` really is the blanket-`build/` item at
  moment **2.1**, not a router seam at 1.10).
- Every named parser trap was avoided: `FENCED_BLOCK` via `.sub()`/`.finditer()` rather than
  `.findall()`; case-folding at the comparison site rather than on the returned set; AC 3 located
  by heading anchor with non-empty-slice assertions; register anchors chosen to dodge the
  `DESIGN.md`-inside-`GAME_DESIGN.md` substring trap.
- The `edgecases` lens's mutation testing proved the field guards genuinely fire: deleting E-007's
  `Source:` reported it; `Status: deferred` reported it; a duplicated id reported it.

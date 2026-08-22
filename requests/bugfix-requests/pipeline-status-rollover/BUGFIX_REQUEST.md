> **Status:** planned · created 2026-08-15 · decided · next: implement

# Bug Report — Stage-3 and stage-4 skills leave sibling artifact statuses stale, and write a token the grammar doesn't have

## Symptom

Following `/create-implementation-plan` literally produces a **red build**. Its Step 5 advances the
Index row and opens the new artifact, but says nothing about the artifacts already in the directory,
which keep their previous stage word. `tests/test_repo_structure.py::test_index_stage_cells_match_their_artifact_status_headers`
compares **every** `*.md` directly under a request directory against that item's Index Stage cell by
exact word, so the stale siblings fail it.

Three defects, in descending order of severity:

1. **No sibling rollover instruction** (the blocking one). `scope-feature/SKILL.md:139` says *"Set the
   request's Status blockquote to `scoped`"* — it rolls the sibling. `create-implementation-plan`
   Step 5 and `implement-plan` Step 7 have **no equivalent line**.
2. **A token the grammar doesn't contain.** `create-implementation-plan/SKILL.md` writes `plan` in
   three places — the Index instruction (line-wrapped across `:172-173`), `:173`, and the template at
   `:176`. All three track grammars say **`planned`**.
3. **A track-blind terminal token.** `implement-plan/SKILL.md:258-260` writes `implemented`
   unconditionally. That is correct for the feature track only — bugfix terminates at `fixed`,
   calibration at `retuned` — and that skill explicitly serves both tracks.

## Reproduction attempt

**Deterministic. Observed live this session on `H1-escalation-queue`.**

1. Take any feature item at stage `scoped` — its directory holds `FEATURE_REQUEST.md` and
   `PROJECT_SCOPE.md`, both with `> **Status:** scoped …`, and an Index row reading `scoped`.
2. Follow `create-implementation-plan/SKILL.md` Step 5 literally: write `IMPLEMENTATION_PLAN.md`
   opening at `plan`, and set the Index Stage cell to `plan`. Change nothing else.
3. Run `uv run pytest tests/test_repo_structure.py -q`.

**Result:** `test_index_stage_cells_match_their_artifact_status_headers` fails, reporting that the
Index lists the item as `plan` while `FEATURE_REQUEST.md` declares `scoped`.

Note the two defects fail *independently*: even if step 2 used `planned` throughout — the
grammar-correct token — the test still fails, because the siblings are what go stale. Fixing the
token alone does not fix the build.

## Expected vs Actual

- **Expected:** following a pipeline skill's own instructions leaves the repo green. The stage-2
  skill achieves this; stage 3 and stage 4 should behave the same way. The status grammar in each
  track README is the source of truth for the token.
- **Actual:** stage 3 and stage 4 advance the Index and their own artifact while leaving every
  sibling behind, and stage 3 uses a token no track grammar defines.

## Severity

**Wrong-output-that-misleads, not data corruption.** No ledger, no career, no dataset, and no money
is touched — the failure is a red CI check on a process artifact, and the test catches it loudly.

What raises it above cosmetic is the **cost profile**: it fires on *every* feature and *every* bug
that reaches stage 3, it fires at the end of the most expensive stage in the pipeline, and the
failure message points at the artifact rather than at the skill that caused it. The natural response
is to patch the symptom locally and move on — which is precisely what happened this session, and
which leaves the defect in place for the next item.

## Triage

- **Verdict:** `needs-full-track` — but a light one. The cause is not in question; the fix's *shape*
  is (see Open Questions).
- **Obviousness hint (non-binding):** the cause is almost certainly a missing instruction rather than
  faulty logic — `scope-feature/SKILL.md:136-144` has the pattern the other two lack. What is *not*
  obvious is whether the fix belongs in three skill files or in one shared place.

## Affected Area & Pointers

Skills and process documentation. Nothing under `src/` or `app/`.

- [`.claude/skills/create-implementation-plan/SKILL.md`](../../../.claude/skills/create-implementation-plan/SKILL.md)
  — Step 5, `:170-177`. The Index instruction, the artifact stage line, and the template.
- [`.claude/skills/implement-plan/SKILL.md`](../../../.claude/skills/implement-plan/SKILL.md)
  — Step 7, `:255-260`, plus the report template's status line.
- [`.claude/skills/scope-feature/SKILL.md`](../../../.claude/skills/scope-feature/SKILL.md)
  — `:136-144`, **the correct pattern**. Whatever the fix is, this is what it should look like.
- [`tests/test_repo_structure.py`](../../../tests/test_repo_structure.py) — the guard at `:286`,
  and the every-artifact loop at `:311` that makes siblings load-bearing.
- The three grammars: [`requests/feature-requests/README.md`](../../feature-requests/README.md)
  `:106`, [`requests/bugfix-requests/README.md`](../README.md) `:86`, and
  [`requests/calibration-findings/README.md`](../../calibration-findings/README.md) `:88`.

## Reporter's cause-hunch (non-binding)

The stage-2 skill was written with the rollover and the later two were not, so the rule lives in one
skill's prose rather than anywhere shared. Each skill restates the status vocabulary independently,
which is exactly the shape that drifts. Diagnosis is free to find something else.

## Open Questions for Diagnosis

1. **Instruction or mechanism?** Three skills each restating the grammar is the condition that
   produced the drift. A fix that adds a fourth restatement may just reset the clock. Is there a
   shared home for the rule — the track READMEs already state the grammar — and is the existing test
   sufficient enforcement, or does the *skill* need its own guard?
2. **Should the terminal token be derived rather than hardcoded?** `implement-plan` already resolves
   the track from the artifact path; the terminal word could follow from that same resolution instead
   of being a literal.
3. **Is the calibration track actually affected in practice?** It has a grammar with a `planned`
   stage and a `retuned` terminal, but whether it routes through the shared back half at all is
   `unconfirmed` — nobody has run that track yet, and its Index is empty.
4. **Is the guard itself too strict, or exactly right?** Requiring every artifact in the directory to
   agree is what makes a stale sibling fail. That is arguably the correct invariant — the alternative
   is a directory that disagrees with itself — but it should be an explicit call rather than an
   assumption the fix inherits.

## Stage plan

**Full pipeline.** Trigger 1 fired: Open Questions came out non-empty, and question 1 is load-bearing
— whether this is three doc edits or a shared mechanism changes what gets built, and getting it wrong
reproduces the same drift on the next skill added.

Trigger 2 did not fire: the reproduction is deterministic and was observed live. Trigger 3 did not
fire: no ADR, pillar, event schema, or dataset contract is touched.

## A note on how this was found

The 1.1 planning panel **already caught this defect** — see
[`_done/1.1-app-shell/reviews/plan-adversarial.md`](../../feature-requests/_done/1.1-app-shell/reviews/plan-adversarial.md)
`:217`, which flags the grammar mismatch against `requests/feature-requests/README.md` directly. The
finding was then archived into `_done/`, a tree `tests/test_request_links.py:36` deliberately skips
and nobody reopens. It was found, recorded, and lost — and then rediscovered from scratch by a second
panel roughly a day later.

That is the exact failure roadmap item **H1 `escalation-queue`** exists to prevent, and this bug is a
worked example of its absence. Recorded here because it is evidence for that item, not because it
changes this fix.

> **Status:** diagnosed · created 2026-08-21 · decided · next: plan

# Root Cause Analysis — Pipeline skills write stage words nothing checks

> **A note on this artifact's own Status line.** The grammar in
> [`../README.md`](../README.md) is `intake → diagnosed → planned → fixed`, so this opens at
> `diagnosed`. `/diagnose-bug`'s template says to write `root-cause`, which no track grammar
> declares — that is **defect 4 below**, found while running the skill on itself. Following the
> template literally would have injected the defect into the artifact diagnosing it.

## Verdict

**`confirmed-bug`** — and broader than intake found: **four instances across three skills**, not
three. It needs the full track, as the request's Stage plan argues: the cause is settled, the fix's
*shape* is not, and Open Question 1 is load-bearing.

## Reproduction (red)

Three assertions in `tests/test_repo_structure.py`, run with:

```
uv run pytest tests/test_repo_structure.py -q
```

**Currently RED — `3 failed, 79 passed`.** All 79 pre-existing tests stay green, so the repro
isolates this defect and nothing else. `ruff check`, `ruff format --check` and `mypy` are clean on it.

| Test | Red output today | Catches |
|---|---|---|
| `test_every_pipeline_skill_writes_a_stage_token_some_grammar_declares` | `{'create-implementation-plan': ['plan'], 'diagnose-bug': ['root-cause']}` against declared vocabulary `['diagnosed', 'fixed', 'implemented', 'intake', 'planned', 'retuned', 'scoped']` | defects **2** and **4** |
| `test_stage_advancing_skills_roll_the_artifacts_already_in_the_directory` | `['create-implementation-plan', 'implement-plan']` | defect **1** (the blocking one) |
| `test_the_terminal_stage_skill_does_not_hardcode_one_track_s_terminal_token` | `implement-plan` hardcodes `['implemented']` while serving all three tracks | defect **3** |

**Not yet committed** — it lands together with this RCA through `/commit`, since agents don't commit.

Defect 3 needed its own assertion: `implemented` *is* in the union of declared grammars, so the
conformance test cannot see it. It is wrong only *relative to the track*, which is a different
claim and needed a different check. Without it a fix could land leaving defect 3 in place with
nothing red — the exact way this bug was lost once already.

## Evidence (the cause)

### The symptom is one defect; the cause explains why the other three are silent

Two different invariants govern a stage word, and only one of them was ever guarded:

| | Invariant | Guarded by |
|---|---|---|
| **A** | The Index cell agrees with **every** `*.md` in the item directory | `test_index_stage_cells_match_their_artifact_status_headers` (`tests/test_repo_structure.py`) |
| **B** | The stage word is one the **track's declared grammar** actually contains | **nothing, anywhere** |

That asymmetry is the root cause of the reporting pattern. Invariant A compares a directory
**against itself**. So a skill that writes a made-up token *consistently* — into the Index and into
its own artifact — satisfies A perfectly and stays green forever. Only a skill that leaves a sibling
behind breaks A, and that is the single instance anyone noticed.

Underneath both: **the stage vocabulary is restated as a literal in each skill's prose, with no
mechanical link to the track README that declares it.** Six restatements across six skills; three of
them wrong. That is the reporter's hunch, and the evidence confirms it.

### The four instances

**Defect 1 — no sibling rollover** (breaks invariant A → loud red). The correct pattern is
`.claude/skills/scope-feature/SKILL.md:136-146`, which does three things: `:139` rolls the sibling
("Set **the request's** Status blockquote to `scoped`"), `:140-143` sets the Index cell, `:144`
opens the new artifact. `create-implementation-plan/SKILL.md:167-173` does only the last two —
the two siblings sitting at `scoped` are never mentioned. `implement-plan/SKILL.md:254-260` is the
same shape. `diagnose-bug/SKILL.md:152` gets it right, so this defect is **2 of 4 skills**, not all.

**Defect 2 — a token no grammar declares** (breaks B → silent).
`create-implementation-plan/SKILL.md:176` writes `plan`; all three grammars say `planned`. The irony
is load-bearing rather than decorative: `:177-178` cites *"this README status grammar"* as its
authority **in the same breath as violating it**, which is what a rule restated by hand looks like
when it drifts.

**Defect 3 — a track-blind terminal** (breaks B for two tracks → silent).
`implement-plan/SKILL.md:254-260` writes `implemented` unconditionally while explicitly serving both
tracks. Feature ends at `implemented`, bugfix at `fixed`, calibration at `retuned`. It is the *last*
stage, so nothing downstream remains to notice.

**Defect 4 — `/diagnose-bug` has it too** (breaks B → silent). **Found by this diagnosis, not by
intake.** `diagnose-bug/SKILL.md:107` writes `root-cause`; the bugfix grammar says `diagnosed`. This
is the strongest available evidence for Open Question 1: the defect was present in the very skill
being used to diagnose it, and neither intake nor a human reading three skills spotted it. A rule
that lives in prose is not enforced by anyone noticing.

### The grammars, for the record

| Track | Declared at | Grammar |
|---|---|---|
| feature | `requests/feature-requests/README.md:106` | `intake → scoped → planned → implemented` |
| bugfix | `requests/bugfix-requests/README.md:86` | `intake → diagnosed → planned → fixed` |
| calibration | `requests/calibration-findings/README.md:88` | `intake → diagnosed → planned → retuned` |

## Answers to the request's Open Questions

These were flagged load-bearing for the plan, and the diagnosis produced evidence on all four.

1. **Instruction or mechanism?** *A fourth restatement would reset the clock* — that is now
   demonstrated, not argued. This diagnosis found defect 4 in a skill nobody suspected, in a repo
   where the rule had already been written down correctly twice. The recommendation is a
   **mechanism**: the conformance guard above is what makes the track READMEs authoritative rather
   than advisory. Whether the skills *also* get a shared prose home is a genuine design call and
   belongs to the plan — but the guard is what stops recurrence, and it is cheap.
2. **Should the terminal token be derived?** **Yes, and the machinery already exists.**
   `implement-plan` resolves the track from the artifact path in its Step 1; the terminal word can
   follow from that same resolution. `diagnose-bug/SKILL.md:152` already shows the tolerated prose
   shape — *"or the terminal stage word"* — so there is an in-repo precedent to copy.
3. **Is calibration affected in practice?** Still **`unconfirmed`**, and deliberately left so: its
   Index is empty and nobody has run the track. But its grammar declares `retuned`, so
   `implement-plan` is wrong for it *in principle* today. The guard covers it without waiting for
   the track to be exercised, which is the point of guarding rather than observing.
4. **Is the guard too strict?** **No — it is exactly right, and it is the only reason any of this
   surfaced.** Requiring every artifact in a directory to agree is the correct invariant; the
   alternative is a directory that contradicts itself. The gap was never strictness, it was
   **scope**: A was guarded and B was not. Keep A unchanged; the fix adds B.

## Fix posture (tiered)

- **Minimal** — four prose edits, turning all three repro tests green: add the sibling-rollover line
  to `create-implementation-plan` Step 5 and `implement-plan` Step 7 (copy `scope-feature:139`);
  change `plan` → `planned` at `create-implementation-plan:172-173,176`; change `root-cause` →
  `diagnosed` at `diagnose-bug:107` and its Step 5 instruction; make `implement-plan`'s terminal
  token track-derived.
- **Root** — the conformance guard *is* the root fix, and it is already written as the repro. It
  converts the track READMEs from advisory prose into the enforced source of truth. **What stays
  open, stated plainly:** the six restatements remain six. The guard prevents drift; it does not
  remove the duplication that causes it. A single shared prose home for the vocabulary is the
  alternative the plan should weigh against "guard it and keep the restatements."
- **Hardening** — three adjacent gaps, gated not assumed. (a) The `next:` field is unchecked:
  `make-bugfix-request/SKILL.md:130` writes `next: root-cause`, a non-grammar token, and the repro
  only inspects the *stage* field. (b) The Index cell itself is only checked against artifacts, never
  against the grammar — a hand-edited Index could carry an invented word if every artifact matched
  it. (c) `tests/test_request_links.py:36` skips `_done/`, which is how the 1.1 panel's original
  catch of this defect became unreachable; that skip is deliberate, but its cost is now measured.

## What this bug cost, measured

Recorded because it bears on the fix's priority rather than its shape. The 1.1 planning panel
already caught defect 2 — `_done/1.1-app-shell/reviews/plan-adversarial.md:217` flags the grammar
mismatch directly — and the finding was archived into a tree nothing reopens. It was found,
recorded, and lost, then rediscovered by a second panel a day later, and worked around by hand twice
more during H1. Four independent discoveries of one defect, none of which fixed it.

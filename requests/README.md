# Requests

The project's work intake — three parallel tracks under one inbox. Every
substantial change enters here.

| Track | For | Start with |
|---|---|---|
| **[feature-requests/](feature-requests/)** | New capability — an engine mechanic, an app surface, a dataset, a skill | `/make-feature-request` |
| **[bugfix-requests/](bugfix-requests/)** | A defect in existing code, config, or tooling | `/make-bugfix-request` |
| **[calibration-findings/](calibration-findings/)** | Everything ran green and the **economy is wrong** | see that track's README |

Each track's **README is the contract** — layout, status grammar, the live Index,
and the `_done/` archive convention. The back half
(`/create-implementation-plan` → `/implement-plan`) is shared and auto-detects
the track from the artifact's path.

## Why three tracks and not two

A code defect and an economy defect look similar and triage completely
differently.

A career that reaches 90 OVR in two seasons is not a crash. The code did exactly
what it was told; the ledger replays; every test is green. The question is *which*
of several things is wrong: the **expectation model** is too easy to beat, the
**cost curve** is too shallow, the **affinity table** doesn't bite, or the
**milestone windfalls** are doing more work than intended. Each has a different
investigation and a different fix.

Calibration findings also carry a second obligation a code bug doesn't: **fixing
forward is only half the work.** The careers already played were played under the
old ruleset. Every finding owes a **replay plan** alongside the fix — which
ruleset version changes, which careers replay, and whether a player's recorded
history shifts underneath them.

See [calibration-findings/README.md](calibration-findings/README.md).

## Principles

Two rules run through every panel in every track:

- **Greedy, but gated.** Agents propose *everything* — generating options is
  cheap, so be ambitious. Scope-growing or expensive ideas get **tiered and
  deferred for your decision**, never silently folded into the build.
- **Generate → converge → triage → you decide.** Adversarial agents record *all*
  findings with severity and confidence and never self-censor. The merge step
  builds the convergence map and surfaces the gated calls. **You** dispose them —
  the panel proposes, you decide.

And one that matters more here than in a typical repo:

- **Label your epistemics.** *Measured*, *verified*, *inferred*, *assumed*,
  *unconfirmed* are different words and mean different things. Much of this
  project rests on beliefs about a game's file formats and a league's
  statistics — a request that says "2K ratings history is available by season"
  when nobody has checked is a liability. Say `unconfirmed` and it becomes a task.

## Weight

Not every change needs every stage. A one-line fix does not need a scoping panel.

> Skip stages when the work is small; lean on the full pipeline when the work is
> big, risky, or hard to hand off cold.

[`ROADMAP.md`](../ROADMAP.md) marks the items that earn the full panel with ★ —
nine of thirty-six. The panels cost real tokens and several minutes. They earn it
on decisions that are expensive to reverse — the ledger's event schema, the
expectation model's parameterization, the affinity combination rule — and waste
it on work whose shape is already obvious.

See [CLAUDE.md](../CLAUDE.md) for where this sits in the repo.

# 0004 — Economy rules are versioned config, not code

**Status:** accepted · 2026-08-12

## Context

The economy is expected to be wrong at first. The whole calibration track exists
on that premise, and [`ROADMAP.md`](../../ROADMAP.md) Phase 2 plans to *replace*
Phase 1's placeholder economy wholesale once real data exists.

If the XP formula, cost curves, and affinity tables live in Python, then "which
rules were live when this game was recorded" is answerable only by git archaeology
against the commit date — and replaying an old career under its original rules
means checking out an old commit.

## Decision

XP formula parameters, cost curves, affinity tables, badge budgets, and milestone
definitions live in **versioned configuration files** under `rulesets/`, not in
code. Code interprets a ruleset; it does not embed one.

**Every event pins the ruleset version live at the time it was recorded.** A
replay resolves each event against its pinned version.

Rulesets are *not* datasets and are deliberately not registered in
`datasets/manifest.json` — they have a version axis and replay semantics that the
dataset layer has no notion of.

## Consequences

**Buys:** a career can be replayed under the rules it was played by, or
deliberately re-run under new ones, and the difference is visible. Retuning
becomes a diff of numbers rather than a diff of logic. Phase 2's economy swap is
a config change plus a replay — item 2.8 exists specifically to prove that claim
while only one throwaway career is at stake.

**Costs:** an indirection layer, and a real discipline problem — the temptation to
put "just this one" special case in code is constant, and each one silently
breaks the replay guarantee for careers that predate it. Config also loses type
checking at the boundary, so the loader has to validate what the type system
would otherwise have caught.

**Forecloses:** rules that can't be expressed as data. If a mechanic genuinely
needs branching logic, it belongs in code *and* needs a version-gated switch, which
is worse than either. Prefer to reshape the mechanic.

**Obligation:** a ruleset version, once any recorded event pins it, is
**immutable**. Changing it rewrites history silently. Retuning creates a new
version; only unreleased versions may be edited in place.

## Alternatives considered

**Formula in code, tuned by editing Python.** Simplest and type-checked
end-to-end. Rejected: it makes "what were the rules in season 2" unanswerable
without git archaeology, and it makes replay require a checkout.

**Config, but unversioned — one live ruleset.** Most of the benefit for none of
the bookkeeping. Rejected because it is exactly the version that silently
rewrites history: retune once and every past game re-scores under rules it was
never played under.

**Store the resolved rules inside every event.** Fully self-describing and
immune to drift, but enormous, unreadable, and it makes a deliberate global
retune impossible. Pinning a version reference gets the same guarantee.

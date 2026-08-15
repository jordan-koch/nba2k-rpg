# 0010 — Panels are the default; skipping them is an argued exception

**Status:** accepted · 2026-08-15

## Context

[`ROADMAP.md`](../../ROADMAP.md) carried two advisory columns on every work item:
**Size** (`S`/`M`/`L`) and **Panel** (★). Both were assigned in a single sitting
while sequencing thirty-six items, **none of which existed yet**.

The ★ legend was binding in effect — *"Unmarked items should skip straight to a
plan or straight to work."* So a prediction made at the point of **minimum**
information was encoded as an instruction, then consumed later at the point of
**maximum** information, by a worker who had just ground the item in the repo and
knew considerably more than the legend did.

Worse, it was self-confirming in the wrong direction: an unmarked item skips the
stage that would have discovered it needed a panel. Nothing could falsify it.

**It was consulted exactly once, and overridden.** Item 1.1 `app-shell` was
unmarked and sized `M`. The full panel ran anyway; the scoping adversary raised
the mismatch as a MAJOR finding against the scope's own size; the user disposed
the question by making the estimate advisory. The scope recorded it as *"one
honest friction, recorded not resolved"* — see
`requests/feature-requests/_done/1.1-app-shell/PROJECT_SCOPE.md:51-55`. A rule
whose only application was an override is not carrying its weight.

`Size` had it worse still: **nothing consumed it.** It gated no stage, set no
budget, and ordered no work. It existed to be wrong.

One thing ★ *was* answering, and which any replacement owes an answer to:
**pre-commitment.** Marks set while thinking about the whole shape resist the
in-the-moment bias to skip ceremony on the item you are itching to build. That
bias is real, and it is sharper here than in most repos because the agent writing
the justification is the one that benefits from skipping.

## Decision

**Delete the `Panel` and `Size` columns.** `Needs` and `Blocks` stay — those are
structural facts about ordering, not predictions about complexity. `Status` stays;
it is a record of what landed.

**The full pipeline is the default.** Anything that gets a request runs
intake → scope → plan → implement unless a skip is *argued in writing*, in a
required closing section of the intake artifact, surfaced at the intake handoff —
which is already human-gated, so this adds no new interruption.

**Three hard triggers. Any one means the panel runs, and no argument is
available:**

1. Intake's **Open Questions** section came out non-empty. That is the definition
   of a blurry edge, and it is mechanical — the agent already had to write it.
2. **Explicitly out** could not be filled. `/make-feature-request` already treats
   an empty one as a signal to interview further; still empty at the end means the
   edges are not known.
3. It touches something **expensive to reverse** — a settled ADR, a pillar from
   `GAME_DESIGN.md` §2, the event schema, a dataset contract, or anything another
   roadmap item pins.

Otherwise a skip is available, and costs a written argument naming which triggers
it cleared.

**Entry condition.** This governs work that gets a *request*. Typo fixes,
dependency bumps, and doc edits never enter the pipeline at all —
[`/commit`](../../.claude/skills/commit/SKILL.md)'s "maps to no roadmap row" path
already covers them. Panel-by-default applies to the already-filtered set.

**Skipped work is still adversarially reviewed.** `/implement-plan` gains a
**direct-build mode**: the intake artifact fills the `planPath` slot, `scopePath`
is omitted, and `touchedAreas` comes from the diff as it always did. The panel's
reviewers were never plan-bound — the roster is derived from what the change
touched — so they run at full strength on a diff with no plan behind it.

**No trim lever, deliberately.** Because the roster is diff-derived, a small
change spawns the four core reviewers and perhaps one specialist. The size of the
work already governs the size of the panel; a `--quick` flag would be a second,
worse control over the same variable.

## Consequences

**Buys:** the panel call is made when there is an artifact to read, by whoever
just ground it in the repo. The burden of proof sits on the cheap path, so
*"let's just build it"* costs an argument rather than being the silent default.
The user sees deviations only, never the routine call. Two columns that could
rot no longer exist to rot.

**Costs:** **more panels will run.** Nine items were marked ★; the trigger rule
will catch more than nine. That is the intended direction and it is real tokens
and real minutes. The skip argument is **written by the party that benefits from
it** — the triggers are mechanical to blunt exactly that, but it is not
eliminated, and the human-gated handoff is the backstop rather than a solution. A
direct-build item's acceptance ledger is derived from a Desired Outcome instead
of numbered criteria, which is **weaker evidence**; that is deliberate, since an
item needing numbered criteria trips trigger 1. Deleting `Size` removes the only
estimate of effort in the project, and nothing replaces it.

**Forecloses:** pre-registering ceremony on unwritten work. A future roadmap that
wants to flag an item as expensive-to-reverse does it in that item's request,
argued against evidence — not in a column filled in before the item exists.

**A note on [ADR 0003](0003-event-sourced-tracked-ledger.md).** Its closing line
cites *"which is why Phase 1 item 1.2 is marked ★"* as the reason the event schema
is the most expensive thing in the codebase to change. **The reasoning survives
intact** — the event schema *is* expensive to change, which is precisely trigger 3
above, so item 1.2 still runs the full panel. Only the ★ it points at is gone.
Per [the ADR rules](README.md), 0003 is not edited to reflect a later change of
mind; this note is the record.

**Enforced by:** a structural test in `tests/test_repo_structure.py` asserting
that every live intake artifact carries the stage-decision section. Archived
(`_done/`) artifacts predate this rule and are exempt, on the same reasoning that
exempts them from the link checker.

## Alternatives considered

**Keep ★ and re-mark the items with better judgment.** Rejected: the problem is
not *which* nine were marked, it is deciding before the evidence exists.
Re-marking is the same error committed with fresher guesses.

**Demote ★ and `Size` to explicitly non-binding hints.** Rejected: this repo is
read mostly by cold agents against documents treated as authoritative. A hint in a
table column is read as an instruction — and an instruction everyone is told to
ignore is worse than either having the rule or not.

**Require the user to approve a stage plan on every item.** Rejected: it makes the
human a gate on the routine path, which is precisely the synchronous-interruption
tax roadmap item H1 exists to remove. The exception deserves attention; the
default does not.

**Route directly-built work through the generic `/code-review` instead.**
Rejected: it is diff-native and needs no document, but it does not know this
repo's rules — append-only ledgers, resolve-by-name, labelled epistemics — and
`/implement-plan`'s specialists check exactly those. Fine for generic
correctness, a downgrade on the constraints that actually bite here.

**Trim the panel roster on the skip path to economize.** Rejected as unnecessary;
see the no-trim-lever note above.

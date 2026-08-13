# 0003 — Event-source the career, and track the ledger in git

**Status:** accepted · 2026-08-12

## Context

A career runs for real months across many seasons, and the economy that governs
it is explicitly expected to change — [ADR 0004](0004-rulesets-as-versioned-config.md)
makes rules versioned config precisely so they can be retuned. A design that
stores *current state* has to migrate that state every time a rule changes, and
migrations of a subjective economy are guesswork.

Second, and more sharply: [ADR 0001](0001-no-save-decryption.md) means there is
**no upstream**. A career cannot be re-derived from the game, from an API, or
from anywhere else. Whatever the app stores is the only copy that will ever
exist.

## Decision

**Event-source the career.** Two append-only streams — game results and currency
spends, plus corrections and accolades — with current player state as a fold over
them. Every event pins the ruleset version live when it was recorded.

**Track `careers/<slug>/events.jsonl` in git.** The SQLite read-model lives in
`var/` and is regenerable by replay.

**Corrections are appends.** Editing a mis-entered box score writes a superseding
event; it never mutates the recorded one.

## Consequences

**Buys:** retuning the economy is a replay rather than a migration. Free
counterfactuals — "what if I'd gone Playmaker" is a replay under a different
spend stream. Version control on the single most irreplaceable artifact in the
project, with clean diffs, because append-only JSONL is exactly what git is good
at. A 20-season career is on the order of 1,600 events.

**Costs:** every read goes through a fold, so naive implementations get slow and
need a cached projection — which is what `var/` is for. Correction-by-append is
genuinely harder to implement than `UPDATE`, and a developer who forgets is not
warned by anything except the replay test. The event schema becomes the most
expensive thing in the codebase to change, which is why Phase 1 item 1.2 is
marked ★.

**Forecloses:** any "just fix the row" repair. A ledger bug is repaired by
appending, never by editing history — see
[`requests/bugfix-requests/README.md`](../../requests/bugfix-requests/README.md).

**Enforced by:** a replay-determinism test (folding twice yields identical state)
and a structural test asserting `careers/**` is not gitignored.

## Alternatives considered

**Store current state in SQLite, migrate on rule change.** Simpler to write and
much faster to read. Rejected because it makes every retune a data migration of
subjective numbers, and because a corrupted or mis-migrated row has no upstream
to recover from.

**Event-source, but keep the log in `var/` with a backup script.** This is what
both reference projects do with local state, and it is correct *there* because
both have an upstream to re-ingest from. Here it would put the only copy of the
career behind a backup script someone has to remember to run.

**Track the SQLite file in git instead.** Binary, doesn't diff, and merge
conflicts are unresolvable. The log is the source of truth precisely because it
is text.

# 0001 — Do not decrypt the 2K save files

**Status:** accepted · 2026-08-12

## Context

The save tree at `<steam>\userdata\<account-id>\3472040\remote\` contains exactly
the files this project would most like to read — `MyLEAGUE0001`,
`CreatedPlayers`, `DraftClassNBA0006`, `CareerModeBuilds`. Reading them would
make box-score ingestion and roster state automatic.

They are encrypted. This is `verified`, not inferred:

- Header `EBNH` + 4 zero bytes + 8 bytes unique per file (nonce) + 8 bytes shared
  across same-epoch saves (probably a key version)
- Whole-file Shannon entropy **8.0000 bits/byte**
- Byte histogram flat to ±3% (26,681–28,141 against 27,189 expected uniform)
- Zero plaintext strings, zero `BNH` markers after the header

The install bundles use `BNH`; the leading **E** is almost certainly "Encrypted".
The key lives in `NBA2K26.exe`, behind EasyAntiCheat.

## Decision

Do not pursue save decryption, for reading or writing.

The install data — which is *not* encrypted and is fully accessible — remains in
scope. See [`docs/data-access.md`](../data-access.md).

## Consequences

**Buys:** no fight with anti-cheat, nothing that breaks on every patch, no legal
or ToS grey area, and a project that keeps working when 2K27 ships.

**Costs:** box-score ingestion is manual, permanently. Roster state cannot be
read back, so the app can never verify that a worksheet was actually applied —
the human step is trusted by construction. Both are real and neither has a
workaround under this decision.

**Forecloses:** automatic ingestion. The nearest available substitute is OCR over
the post-game box-score screen, which requires no save access at all and is
tracked as post-v1 in [`ROADMAP.md`](../../ROADMAP.md).

**Note:** "just reading" is not a lesser ask. Reading requires the key, the key
requires getting inside a process behind EasyAntiCheat, and that is the same
fight as writing.

## Alternatives considered

**Extract the key from `NBA2K26.exe`.** Rejected. Anti-cheat makes it adversarial,
every patch potentially moves it, and the payoff is convenience on a step that
takes about thirty seconds by hand.

**Read `local\tmp\replay.bin` (3.5 GB).** It sits outside the encrypted `remote`
tree and might carry play-by-play. Cheap to check, probably only the last game,
and not on the critical path. Left as an unresolved lead in
[`docs/data-access.md`](../data-access.md) rather than a plan.

**Community save editors.** Same anti-cheat surface, plus a dependency on someone
else's reverse engineering keeping pace with patches.

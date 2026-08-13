# Data Access

What can be read, from where, and how confident we are. Reconnaissance performed
**2026-08-12** against the local install and save data.

**Epistemic labels are load-bearing.** `verified` means someone ran it and saw
the result. `inferred` means it follows from something verified. `unconfirmed`
means it is a belief nobody has tested — and an unconfirmed claim is a task, not
a fact.

---

## 1. Install data — fully accessible · `verified`

`<steam>\steamapps\common\NBA 2K26` — resolved at runtime by
`research/tools/iff.ps1` from `NBA2K26_INSTALL` or a Steam registry probe. Never
hardcode it; `tests/test_no_leaks.py` will fail the build.

- **`manifest`** is a plaintext CSV index of **589,895 files**:
  `name,blob,offset,length`. No index reversing needed.
- Payload lives in 58 opaque blobs (`0A`–`4F`), ~100 GB total.
- **`oo2core_9_win64.dll` ships with the game** at `data\oodle\`. P/Invoking
  `OodleLZ_Decompress` works directly — verified with exact size matches
  (`gamedata.iff` 3.3 MB → 27.6 MB).

### The `.iff` container format · `verified`

```
gzip-style 16-byte header (magic 1F 8B, CM=0x21, extra field "VCZ")
  └─ Oodle Kraken stream      (uncompressed size = last 4 bytes, gzip ISIZE convention)
       └─ standard ZIP archive
            └─ typed entries: .RDAT, .SCNE, .TXTR, .VCLOCALIZEDATA, .SLUG
```

A working toolkit is preserved at [`research/tools/`](../research/tools/):

| File | Purpose |
|---|---|
| `iff.ps1` | `Get-IffManifest`, `Get-IffBytes`, `Expand-Iff`, `Get-IffEntries`, `Get-IffEntryBytes` |
| `find_grid.ps1` | Statistical record-stride detection in a decompressed `.RDAT` |
| `dump_grid.ps1` | Phase-locks the player grid, dumps names + record hexdump |

### Roster payloads · `verified`

All contain a `roster.RDAT` entry:

| IFF | `roster.RDAT` size |
|---|---|
| `playnow_online_roster.iff` | 15.4 MB |
| `learn2k_roster.iff` | 15.4 MB |
| `metrics_roster.iff` | 12.6 MB |
| `wnba_metrics_roster.iff` | 7.7 MB |

### Player record layout · partially decoded

| Offset | Contents | Confidence |
|---|---|---|
| `+0` | Last name, UTF-16LE | `verified` |
| `+40` | First name, UTF-16LE | `verified` |
| `+80` onward | Packed binary — attributes, tendencies, badges | **`not decoded`** |

- Flat array of **~918 slots × 17,234 bytes** · `verified` — the stride is
  confirmed by consecutive offsets in
  [`research/sample_players.csv`](../research/sample_players.csv)
  (28128 − 10894 = 17234), and 918 × 17,234 ≈ 15.8 MB matches the payload size.
- A separate 366-byte-stride alphabetical **surname pool** — the CAP name
  generator table · `verified`.

Names extracted cleanly: Jokić, LeBron, Giannis, Wembanyama, DeRozan, Anunoby,
plus legends (Erving, Gilmore) and generated filler players.
`research/sample_players.csv` holds 250 of them — a floor, not the true count;
name validation was strict and rejected accented characters and empty slots.

### Also accessible, unused so far · `verified`

`TEXT.VCLOCALIZEDATA` (16 MB string table, likely holds display names for every
attribute and badge), 5,642 player portraits, 3,708 roster textures, 2,270 team
logos.

---

## 2. Save data — encrypted, out of scope · `verified`

`<steam>\userdata\<account-id>\3472040\remote\`

Contains exactly the files this project would want — `MyLEAGUE0001` (6.6 MB),
`CreatedPlayers`, `DraftClassNBA0006`, `CareerModeBuilds` — and all are
encrypted.

Header: `EBNH` + 4 zero bytes + 8 bytes unique per file (nonce) + 8 bytes shared
across same-epoch saves (probably a key version — the Oct-2025 files differ from
the Aug-2026 ones). Install bundles use `BNH`; the leading **E** is `inferred` to
mean "Encrypted".

Evidence, unambiguous:

- Whole-file Shannon entropy **8.0000 bits/byte**
- Byte histogram flat to ±3% (26,681–28,141 against 27,189 expected uniform)
- Zero plaintext strings
- Zero `BNH` markers after the header

The key lives in `NBA2K26.exe`, behind EasyAntiCheat.
**Not pursued** — see [ADR 0001](decisions/0001-no-save-decryption.md).

### Unresolved lead · `unconfirmed`

`local\tmp\replay.bin` (3.5 GB) sits **outside** the encrypted `remote` tree. If
unencrypted it might carry play-by-play. Long shot, probably just the last game.
Cheap to check, not on the critical path, nobody has looked.

---

## 3. External sources · `unconfirmed`

Nothing below has been pulled from this repo. Every row is a belief.

| Source | Wanted for | Status |
|---|---|---|
| Real NBA box scores | The expectation model (Phase 2, item 2.3) | `unconfirmed` — no endpoint chosen, no pull attempted |
| Real NBA draft data | Draft tier → OVR band ([ADR 0006](decisions/0006-decompose-draft-tier.md)) | `unconfirmed` |
| 2K ratings cross-section, with height/weight/wingspan | The vitals affinity layer (Phase 2, item 2.5) | `unconfirmed` |
| 2K ratings **history** by year | Longitudinal trajectories — the falsifiability harness | `unconfirmed`, and **availability itself is in doubt** |

**The one that matters most.** Whether historical 2K rosters are available from
prior years is an open question in `DESIGN.md`, and it gates any fitted aging
work. It is deliberately **not** on v1's critical path — the age multiplier is
deferred and regression is rejected
([ADR 0009](decisions/0009-no-athletic-regression.md)) — but the falsifiability
harness depends on it entirely.

Confirming these is the first task of Phase 2.

---

## 4. What this means for the design

- **Box-score ingestion is manual, permanently.** Not a shortcut — the only
  tractable path. See [ADR 0002](decisions/0002-manual-ingestion-dto-boundary.md).
- **Roster state cannot be read back.** The app cannot verify a worksheet was
  applied; the human step is trusted by construction.
- **The career ledger has no upstream.** This is why it is tracked in git rather
  than left in `var/` — see [ADR 0003](decisions/0003-event-sourced-tracked-ledger.md).
- **The install roster is a calibration corpus, not a source of truth to import.**
  Its value is ~918 real attribute vectors to check archetypes and caps against.
- **External ratings probably outrank the struct decode.** The decode yields one
  cross-section; external ratings yield the same cross-section *plus* vitals,
  without touching the install. The decode is post-v1 and may never be needed.

### Struct decode approach, when and if · `inferred`

Differential analysis is **blocked**: it needs a write-then-diff loop, and the
only writable surface is the encrypted save tree.

The available approach is **known-plaintext correlation**. ~918 player names sit
at known offsets, and their true ratings are obtainable externally — so correlate
candidate byte offsets across all records against a known vector (OVR, height,
age) and the encoding falls out. Slower per field than a diff, but it needs
nothing but read access.

Scope is roughly 60 attributes, 80 badges (0–4 each), 70 tendencies, 15 hot zones.

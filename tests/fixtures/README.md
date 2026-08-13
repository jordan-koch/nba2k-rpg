# Test fixtures

Committed inputs that let tests run offline and deterministically. This is the
one carve-out to the "no data in git" rule — everything here is small, hand-
checked, and pinned on purpose.

## What belongs here

| Kind | Why it's a fixture |
|---|---|
| **Career event logs** | Reproducing a ledger or fold bug. **Never** reproduce against a live career — copy the events here and work on the copy. |
| **Cached source payloads** | A trimmed response from an external source, so builder tests never hit the network. |
| **Pinned economy outputs** | A known (build, box score) → (XP, price) mapping, so a retune can't silently undo a previous calibration decision. |
| **Ruleset snapshots** | The exact ruleset a fixture career was recorded under, so replay tests are self-contained. |

## Rules

**Small and trimmed.** A fixture is the *minimum* input that exercises the case.
A full-season pull belongs in `var/cache/`, not here.

**Pinned, not regenerated.** A fixture that gets rewritten whenever the code
changes proves nothing. If output changes, that's a decision to review — update
the fixture deliberately, in the same commit as the change that justified it.

**Fixtures accumulate; they don't get replaced.** A better real-world case is a
*new* fixture. Old ones stay, because they encode what was true when someone
decided it mattered.

**Never a real career, in place.** Copy it. See
[`requests/bugfix-requests/README.md`](../../requests/bugfix-requests/README.md)
— the ledger has no upstream, and a test that writes to a real career destroys
the only copy that exists.

## Layout

Nothing here yet. Fixtures arrive with the code that needs them, from Phase 1.

```
fixtures/
  careers/<slug>/events.jsonl    ledger + replay cases
  sources/<source>/*.json        trimmed external payloads
  economy/*.json                 pinned price and XP expectations
```

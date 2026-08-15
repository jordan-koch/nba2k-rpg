# CLAUDE.md — nba2k-rpg

## What this project is

A self-directed RPG progression layer for a specific way of playing NBA 2K26:
create a player, insert them into a draft class, then play **MyNBA player-locked**
as that player — i.e. rebuilding MyCareer inside the franchise mode.

That mode has no progression system. Attributes, badges, hot zones, and animation
packages are all hand-editable in-game, so growth is possible — but with no earned
currency, every upgrade is arbitrary. This project supplies the currency and the
rules that make upgrades feel earned.

Inspired by **Synergy2K**. The user subscribes to it and likes it; this exists
because of five specific disagreements with its implementation, listed in
[`README.md`](README.md).

## Status

**Phase 0 — harness — complete. Phase 1 — skeleton — in progress.** Item 1.1
`app-shell` has landed the seam: `src/rpg_api/` (health endpoint, SPA serving)
and `app/` (React + Vite). **No domain logic yet** — no ledger, no economy, no
careers; `src/rpg_core/` is still a version string. Next is 1.2 `career-ledger`.
Per-item status lives in [`ROADMAP.md`](ROADMAP.md).

## Stack

Python 3.12, uv, ruff, mypy strict, pytest. The app is a **localhost web app:
FastAPI + a React SPA**, with local storage — SQLite as a rebuildable read-model
over the tracked event ledger. No cloud, no credentials, no hosting.

## The repo is PUBLIC

GitHub Free requires a public repo for branch protection, and that trade was
taken deliberately. Consequences that bind every change:

- **Everything tracked is world-readable, forever** — including `careers/`, which
  is tracked on purpose (see below).
- **No machine-specific absolute paths, account ids, tokens, or personal
  identifiers in tracked files.** `tests/test_no_leaks.py` fails the build on
  drive-letter paths, home directories, and email addresses.
- **Machine-specific values resolve from the environment.** `.env.example` lists
  the keys; `.env` is gitignored. `research/tools/iff.ps1` is the worked
  example — it reads `NBA2K26_INSTALL` or probes the Steam registry, and hardcodes
  nothing.
- Roster data extracted from the game install is **2K's**, not ours. Keep the
  tracked footprint to what calibration actually needs.

## Project map

```
GAME_DESIGN.md      What the game is — read FIRST for intent
ROADMAP.md          v1 boundary, five phases, 36 work items
DESIGN.md           Open engineering work — unsettled mechanism math only
docs/
  data-access.md      What can be read, from where, with epistemic labels
  decisions/          ADRs — ten settled calls
requests/           Intake — feature-requests / bugfix-requests / calibration-findings
.claude/skills/     Pipeline stages + /commit
src/rpg_core/       Domain core — I/O-free, web-free. Empty until item 1.2
src/rpg_api/        HTTP seam — routing, serialization, serving the built SPA
app/                React + Vite SPA. Every config file scoped to app/
research/           IFF extraction toolkit + roster sample
ops/                Branch protection, local toolchain
tests/              Structural guards
var/                GITIGNORED — read-model, caches, scratch
```

Directories appear when their phase does. `careers/`, `datasets/`, `rulesets/`,
and `lib/` don't exist yet — don't create them speculatively.

**Two run modes**, both in `ops/README.md`: `uv run rpg-serve` for the built app
on one origin, or uvicorn + `npm run dev` in two terminals. The Vite proxy is the
entire CORS story — there is no CORS middleware, deliberately.

## Important locations

- **[GAME_DESIGN.md](GAME_DESIGN.md)** — the four pillars, the player's decisions,
  the failure modes. Every proposed mechanic gets tested against the pillars.
  `[OPEN-N]` items are parked deliberately; each has a phase that answers it.
- **[ROADMAP.md](ROADMAP.md)** — the work breakdown. **Every row is one intake
  item and one feature branch.** It does **not** say how much ceremony a row gets;
  that is decided against the written request, never in advance (ADR 0010).
  Each row and phase header carries a **Status** — `NOT STARTED` / `IN-PROGRESS` /
  `DONE` — maintained by `/commit` against the diff, not edited ad hoc.
  **`H` rows are harness work** — outside the numbered items, same Status rules,
  ordered by `Needs`/`Blocks` rather than position. A `Blocks` cell is binding:
  it names the item that may not start until the harness row lands.
- **[docs/decisions/](docs/decisions/)** — read before proposing anything
  substantive. Ten ADRs cover save decryption, ingestion, the ledger, rulesets,
  the training subsystem, draft tiers, repo scope, cost-side-only builds,
  regression, and when the pipeline's panels run.
- **[docs/data-access.md](docs/data-access.md)** — everything about the game's
  files. **Every external source in §3 is `unconfirmed`** — nothing has been
  pulled from this repo yet.

## Established facts — do not re-investigate

Verified 2026-08-12. Full detail in [`docs/data-access.md`](docs/data-access.md).

- **Save files are encrypted.** `EBNH` magic, entropy 8.0000 bits/byte, flat byte
  histogram, zero plaintext. Key is in `NBA2K26.exe` behind EasyAntiCheat.
- **Install data is fully accessible.** `manifest` is a plaintext CSV index of
  589,895 files. `.iff` = gzip-style header → Oodle Kraken → ZIP → typed entries.
  `research/tools/iff.ps1` already does all of this.
- **Player records are ~918 slots × 17,234 bytes.** Names decode at `+0` and
  `+40`; everything past `+80` is packed binary and **not decoded**.

## Decisions already made — do not re-propose

All ten are ADRs. The ones most often re-proposed:

- **No save decryption** (0001). Reading is not a lesser ask than writing — both
  need the key from behind anti-cheat.
- **Corrections are appends** (0003). Never mutate a recorded event. A ledger bug
  is repaired by appending, never by editing history.
- **Rules are versioned config, not code** (0004). A ruleset version that any
  recorded event pins is immutable.
- **No practice/film/training subsystem** (0005). The Phase 4 offseason block is
  explicitly *not* this — read the carve-out before touching it.
- **The build prices upgrades; it never scores production** (0008). Archetype
  must not enter the scoring model, including sympathetic versions.
- **No athletic regression** (0009). Rejected, not deferred.
- **The panel is the default** (0010). Ceremony is never pre-registered on
  unwritten work. Skipping a stage costs a written argument in the request, and
  three hard triggers foreclose it outright.

## Project conventions

- **Work on a branch; land it through a PR.** `main` is protected. Never commit
  to `main` directly.
- **Agents commit only through `/commit`.** Never run `git commit` ad hoc — not
  for a one-line change, not for an "obviously safe" one.
- **Agents may push a feature branch, open and merge its PR, and prune it after.**
  All are recoverable, and making the user type them buys nothing. The real gate
  is on GitHub's side, not here: `enforce_admins: true` means **nobody** merges
  past a red check, so opening and merging a PR cannot bypass CI. Still theirs
  alone, and these are the genuinely unrecoverable ones: **amend, force-push, and
  any push to `main`.** `gh api` also stays prompted — it is the whole REST
  surface, and re-applying branch protection is rare enough to be worth a human.
- **Prune only against a verified-merged check — and `-d` is not that check.**
  PRs here land as **squash merges**, so the branch tip is never an ancestor of
  `main` and `git branch -d` refuses every already-merged branch. The check that
  actually works is content equality:

  ```powershell
  git fetch origin
  git diff <branch> origin/main --stat    # empty output = fully merged
  ```

  Empty means safe, and only then is `-D` appropriate. Reaching for `-D` because
  `-d` complained, *without* running that diff, is how unmerged work gets thrown
  away. The commit stays in the reflog for ~90 days either way.
- **Subagents get read-only git.** When spawning any subagent, tell it git is
  read-only — never `checkout`/`reset`/`restore`/`clean`/`stash` or anything that
  discards working-tree state. Bubble a destructive-git *need* back up. The push
  and prune allowances above are the main agent's, not a subagent's.
- **Label your epistemics.** *Measured*, *verified*, *inferred*, *assumed*,
  *unconfirmed* mean different things. Most of this repo rests on beliefs about a
  game's file formats and a league's statistics; an unconfirmed claim is a task,
  not a fact.
- **Every roadmap item is a request.** Nothing substantial gets built without an
  intake artifact behind it. **The full pipeline is the default** — a skipped
  stage is an exception you argue for in writing, in the request's **Stage plan**
  section, and three hard triggers foreclose the argument entirely
  ([ADR 0010](docs/decisions/0010-panels-by-default.md), rubric in
  [requests/README.md](requests/README.md)). The burden of proof is on the cheap
  path, not on the panel.

## The one inverted convention

**`careers/**/events.jsonl` is TRACKED in git.** Everywhere else in this repo,
and in both reference projects, local state is disposable and gitignored. Here it
is the opposite, because the encrypted save means there is **no upstream to
re-ingest a career from** — the ledger is the only copy that will ever exist.

`tests/test_repo_structure.py` enforces this. If you add a `.gitignore` rule that
shadows the carve-out, that test fails and it is not being pedantic.

Its mirror: `var/` holds **only** regenerable things — the SQLite read-model
(rebuilt by replay) and caches (re-pulled with `--fetch`).

## Related repos — references, not dependencies

Neither is upstream. Nothing here consumes anything from either. See
[ADR 0007](docs/decisions/0007-repo-location-no-upstream.md).

Local checkouts, paths not recorded here — this repo is public. `.env.example`
lists the keys (`NBA_ANALYSIS_PATH`, `POKEMON_LAB_PATH`); ask the user for the
actual locations if you need to read either.

- **`nba-analysis`** — NBA lakehouse, portfolio work, Phase 0. The **style
  template**: toolchain, ADR format, request tracks, structural tests, CI. Same
  domain by coincidence; *not* a source of box scores.
- **`pokemon-lab`** — Gen 3 Pokémon tooling. The **structural sibling**:
  hobby-domain project with a `build/build-*.py` → `datasets/` builder pattern
  resolved by logical name. That data-layer pattern is the one to follow in
  Phase 2.

## Context on the user

Data engineer. Thinks in systems and pushes back well on design. Prefers thin
mechanisms over subsystems. Wants the economy to be **falsifiable** — calibrated
against real player development rather than tuned by taste.

**This is a fun side project**, not portfolio work. That governs scope: size it
for sustained enjoyment, not completeness. It does *not* mean light process —
`pokemon-lab` is also a hobby project and runs the full request pipeline.

## How to help

- **Check any proposed mechanic against the four pillars** in `GAME_DESIGN.md` §2
  and the seven failure modes in §7. Most naive progression designs hit at least
  one of: low-minute dead ends, backwards curves, convergence to uniform, or a
  cosmetic class.
- **Check the ADRs before proposing anything structural.** Nine decisions are
  settled and re-litigating them is the most expensive thing that can happen here.
- **Don't answer `[OPEN-N]` questions ad hoc.** Each is parked against a phase and
  gets a scoping panel with the loop already in hand to argue against.
- **`unconfirmed` beliefs are tasks.** If a plan depends on an external source
  nobody has pulled, say so rather than assuming its shape.

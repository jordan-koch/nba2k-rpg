# nba2k-rpg

A self-directed RPG progression layer for a specific way of playing NBA 2K26:
create a player, insert them into a draft class, then play **MyNBA
player-locked** as that player — rebuilding MyCareer inside the franchise mode.

That mode has no progression system. Attributes, badges, hot zones, and animation
packages are all hand-editable in-game, so growth is *possible* — but with no
earned currency, every upgrade is arbitrary. This project supplies the currency
and the rules that make upgrades feel earned.

> **Phase 1, in progress.** The harness is done and the application skeleton now
> runs: a FastAPI seam, a one-page React SPA that crosses it, and two honest run
> modes. There is no game logic yet — no ledger, no economy, no careers. Those
> are items 1.2 onward in [ROADMAP.md](ROADMAP.md).

## The loop

```
play a game
  └─> enter the box score          (~30s, keyboard-driven)
       └─> see the grade           — what you produced vs. what was expected
            └─> XP accrues
                 └─> spend when you want to
                      └─> worksheet: a diff to apply by hand in-game
```

Two steps touch the game and both are human: **entering the box score** and
**applying the worksheet**. Everything between them is the engine's. The save
files are encrypted and deliberately not decrypted
([ADR 0001](docs/decisions/0001-no-save-decryption.md)), so this is the only
tractable shape.

## What makes it different

Inspired by Synergy2K, which does the same box-score → XP → upgrade loop well.
This exists because of five specific disagreements with its implementation:

1. No starting badges — most real draft-class players already have them.
2. Only six fixed archetypes.
3. Low-minute players have no realistic path to improve.
4. The progression curve runs backwards relative to real NBA development.
5. Builds converge toward uniformly-high ratings over a long career.

The answers, in short: **score against expectation rather than against zero**, so
opportunity normalizes out and a better player has to beat a higher bar;
**price upgrades by vitals × archetype**, so specialization falls out of the cost
structure instead of needing a cap; and **make the class pick a career-long
commitment** rather than a label.

Full treatment in [GAME_DESIGN.md](GAME_DESIGN.md).

## Project map

```
nba2k-rpg/
├── GAME_DESIGN.md     What the game is — fantasy, pillars, the player's decisions
├── ROADMAP.md         v1 boundary, five phases, 36 work items
├── DESIGN.md          Open engineering work — unsettled mechanism math
├── CLAUDE.md          Onboarding map + the rules to work by
├── docs/
│   ├── data-access.md   What can be read, from where, how confident we are
│   └── decisions/       ADRs — ten settled calls and what each cost
├── requests/          Work intake — three tracks (feature / bugfix / calibration)
├── .claude/skills/    The pipeline stages, plus /commit
├── src/rpg_core/      Domain core — I/O-free, web-free. Empty until item 1.2
├── src/rpg_api/       HTTP seam — routing, serialization, serving the SPA
├── app/               React + Vite SPA. All of its config is scoped to app/
├── research/          IFF extraction toolkit + the roster sample
├── ops/               Branch protection, local toolchain setup
├── tests/             Structural guards
└── var/               GITIGNORED — read-model, caches, scratch
```

Directories appear when their phase does. `careers/`, `datasets/`, `rulesets/`,
and `lib/` don't exist yet.

## Setup

```powershell
winget install --id=astral-sh.uv -e        # once; open a new shell afterwards for PATH
winget install --id=OpenJS.NodeJS.LTS -e   # once
uv sync                                    # from the tracked uv.lock
npm ci                                     # from app/, using the tracked lockfile
```

Then run it, either way:

```powershell
npm run build          # from app/
uv run rpg-serve       # one origin, http://127.0.0.1:8000
```

```powershell
# or, for development, in two terminals:
uv run uvicorn rpg_api.app:create_app --factory --reload --host 127.0.0.1 --port 8000
npm run dev            # from app/
```

See [ops/README.md](ops/README.md) for branch protection, both toolchains, the
full local check list, and the lockfile rules.

## Status

| Phase | | |
|---|---|---|
| 0 — Harness | workbench | **done** |
| **1 — Skeleton** | is it fun? | in progress |
| 2 — Economy | do the numbers mean anything? | |
| 3 — Season | does it survive 82 games? | |
| 4 — Career | is a career more than a long season? | **← v1** |

## A note on scope

This is a side project, built for enjoyment rather than as portfolio work. That
governs scope — it is sized for sustained play, not completeness — but not
process: the request pipeline, ADRs, and CI gates are here because a project
written mostly by agents needs its decisions written down or it re-litigates them
every month.

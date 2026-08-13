# nba2k-rpg

A self-directed RPG progression layer for a specific way of playing NBA 2K26:
create a player, insert them into a draft class, then play **MyNBA
player-locked** as that player — rebuilding MyCareer inside the franchise mode.

That mode has no progression system. Attributes, badges, hot zones, and animation
packages are all hand-editable in-game, so growth is *possible* — but with no
earned currency, every upgrade is arbitrary. This project supplies the currency
and the rules that make upgrades feel earned.

> **Phase 0.** Repo, process, and CI harness exist. **No application code yet.**
> The first work item is Phase 1's `app-shell` — see [ROADMAP.md](ROADMAP.md).

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
│   └── decisions/       ADRs — nine settled calls and what each cost
├── requests/          Work intake — three tracks (feature / bugfix / calibration)
├── .claude/skills/    The pipeline stages, plus /commit
├── src/rpg_core/      Domain core — I/O-free, web-free. Empty until Phase 1
├── research/          IFF extraction toolkit + the roster sample
├── ops/               Branch protection, local toolchain setup
├── tests/             Structural guards
└── var/               GITIGNORED — read-model, caches, scratch
```

Directories appear when their phase does. `careers/`, `datasets/`, `rulesets/`,
`lib/`, and the web app don't exist yet.

## Setup

```powershell
winget install --id=astral-sh.uv -e   # not yet installed on the dev machine
uv lock
uv sync
uv run pytest
```

See [ops/README.md](ops/README.md) for branch protection and the CI lockfile note.

## Status

| Phase | | |
|---|---|---|
| **0 — Harness** | workbench | in progress |
| 1 — Skeleton | is it fun? | |
| 2 — Economy | do the numbers mean anything? | |
| 3 — Season | does it survive 82 games? | |
| 4 — Career | is a career more than a long season? | **← v1** |

## A note on scope

This is a side project, built for enjoyment rather than as portfolio work. That
governs scope — it is sized for sustained play, not completeness — but not
process: the request pipeline, ADRs, and CI gates are here because a project
written mostly by agents needs its decisions written down or it re-litigates them
every month.

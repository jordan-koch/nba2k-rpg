# 0007 — Repo outside OneDrive; this project has no upstream repo

**Status:** accepted · 2026-08-12 · *paths redacted 2026-08-13 when the repo went public; the decision is unchanged*

## Context

Two location questions, settled together because they were originally confused
with each other.

**Where the repo lives.** The obvious home was
`OneDrive\Documents\Portfolio\`, alongside other work. This repo will carry a
SQLite read-model, cached stat pulls, and extracted game payloads — files that
change constantly and are large.

**What it depends on.** There is another NBA repo on the same machine
(`nba-analysis`), and an older superseded one in OneDrive. Early
notes recorded the older one as "an upstream source, not a parent," which was
wrong in a way worth recording: it implied this project would consume data
produced by another repo.

## Decision

**The repo lives on a local drive, deliberately not under OneDrive.**

**This project has no upstream repo.** It pulls its own NBA box scores, draft
data, and 2K ratings directly into `datasets/spoke/` via its own builders.

`nba-analysis` is a **style reference** — toolchain, ADR format,
request tracks, structural tests, CI shape. `pokemon-lab`
is a **structural reference** — the resolve-by-name data layer and the builder
pattern. Neither is a dependency. Nothing here imports, reads, or waits on
either.

## Consequences

**Buys:** no OneDrive sync thrash on a database and a cache. No cross-repo
coupling, no waiting on another project's roadmap, and no shared schema to keep
in step. This project can be deleted or rewritten without touching anything else.

**Costs:** the NBA data acquisition work is duplicated between this repo and
`nba-analysis`, which does the same kind of pull for different reasons. That
duplication is accepted deliberately — the coupling cost of sharing exceeds the
cost of writing a second pull, especially since the two want different grains.

**Forecloses:** treating `nba-analysis` as a warehouse this app queries. If that
ever becomes attractive, it needs a superseding ADR and a real interface, not an
ad-hoc file read across the filesystem.

**Consequence for backups:** OneDrive is not backing this up. The git remote is
the backup — which is a large part of why
[ADR 0003](0003-event-sourced-tracked-ledger.md) tracks the career ledger rather
than leaving it in `var/`.

## Alternatives considered

**Under `OneDrive\Documents\Portfolio\`.** Free offsite backup. Rejected: sync on
a live SQLite file and a multi-gigabyte cache is misery, and the cache is
regenerable so syncing it is pure waste.

**Consume `nba-analysis` as an upstream.** Architecturally tidier and avoids
duplicate extraction. Rejected: that repo is portfolio work with its own goals
and its own pace, it currently has no pipeline code at all, and coupling a hobby
project's critical path to another project's roadmap is a good way to stall both.

**A shared local data directory outside both repos.** Avoids duplication without
coupling the repos. Rejected as premature — one consumer does not need a shared
substrate, and `datasets/manifest.json` makes relocating cheap if a second ever
appears.

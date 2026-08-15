# Architecture Decision Records

Why each choice was made, written down at the time it was made.

These exist because this project is mostly written by agents against documents
treated as authoritative. A decision that lives only in a chat log gets
re-proposed every few weeks, and re-litigating a settled call is the single most
expensive thing that can happen to a small project.

## Format

One file per decision, numbered and immutable once accepted:

```
NNNN-short-slug.md
```

Each carries:

- **Status** — proposed / accepted / superseded by NNNN
- **Context** — what forced a decision; the constraints in play at the time
- **Decision** — what was chosen, stated plainly
- **Consequences** — what this buys, what it costs, and what it forecloses
- **Alternatives considered** — and why they lost

## Rules

**Don't edit an accepted ADR to reflect a change of mind.** Write a new one that
supersedes it, and update the old one's status line to point at it. The value
here is the record of what was believed *at the time*; rewriting it destroys
exactly what makes it useful.

**Record the cost honestly.** An ADR that lists only benefits is marketing. The
consequences section should be uncomfortable to write.

**Numbers are contiguous.** `tests/test_repo_structure.py` enforces that they run
1..N with no gaps and that every one appears in the index below.

## Index

| # | Decision | Status |
|---|---|---|
| [0001](0001-no-save-decryption.md) | Do not decrypt the 2K save files | accepted |
| [0002](0002-manual-ingestion-dto-boundary.md) | Manual box-score entry behind a DTO boundary | accepted |
| [0003](0003-event-sourced-tracked-ledger.md) | Event-source the career, and track the ledger in git | accepted |
| [0004](0004-rulesets-as-versioned-config.md) | Economy rules are versioned config, not code | accepted |
| [0005](0005-no-training-subsystem.md) | No practice/film/training subsystem | accepted |
| [0006](0006-decompose-draft-tier.md) | Decompose draft tier rather than model it directly | accepted |
| [0007](0007-repo-location-no-upstream.md) | Repo outside OneDrive; this project has no upstream repo | accepted |
| [0008](0008-build-is-cost-side-only.md) | The build prices upgrades; it never scores production | accepted |
| [0009](0009-no-athletic-regression.md) | Do not model athletic regression | accepted |
| [0010](0010-panels-by-default.md) | Panels are the default; skipping them is an argued exception | accepted |

# 0002 — Manual box-score entry behind a DTO boundary

**Status:** accepted · 2026-08-12

## Context

[ADR 0001](0001-no-save-decryption.md) rules out reading game state from the save
files, so the only way a box score reaches the engine is a human typing it. That
is the same constraint Synergy2K operates under — and now we know it was the only
tractable path rather than a shortcut somebody took.

The risk is that "manual entry" leaks into the design as an assumption. If
parsing, validation, and the earn model are written against a web form's request
payload, then a future OCR path is a rewrite rather than an addition.

## Decision

Box-score entry is manual, and ingestion is a **DTO boundary**: a single
`BoxScore` type that every source constructs and every consumer accepts.

The web form is one producer of that type. OCR, a paste-a-line parser, a test
fixture, and a bulk backfill are others. Nothing downstream of the DTO knows or
cares which produced it.

## Consequences

**Buys:** OCR becomes a v2 swap-in behind an existing seam rather than a rewrite.
Test fixtures construct the DTO directly, so the entire economy is testable with
no HTTP and no UI. Validation lives in one place.

**Costs:** an indirection that looks like ceremony while there is exactly one
producer. It will look like over-engineering until the second producer arrives,
and it is legitimate to point that out.

**Forecloses:** nothing meaningful. The boundary can be collapsed later far more
cheaply than it can be introduced later.

**Obligation:** the DTO must carry what the *economy* needs, not what the 2K
post-game screen happens to show. If a field is in the box score but no rule
consumes it, it is still worth capturing — an event log is only as good as what
was recorded at the time, and re-entering 82 games because a formula changed is
not an option.

## Alternatives considered

**Write the earn model against the HTTP request payload.** Simpler today. Makes
the API shape and the domain model the same thing, so an API change becomes an
economy change, and testing the economy requires standing up a web app.

**Defer the boundary until OCR is actually built.** Plausible, but the boundary
is nearly free now and expensive once three consumers have grown against the
concrete shape.

**Design for OCR from the start.** Rejected as scope. OCR is explicitly post-v1
in [`ROADMAP.md`](../../ROADMAP.md); the point here is only to leave the door
open, not to walk through it.

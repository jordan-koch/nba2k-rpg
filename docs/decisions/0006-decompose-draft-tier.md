# 0006 — Decompose draft tier rather than model it directly

**Status:** accepted · 2026-08-12

## Context

Projected draft position is a creation input and the game's difficulty lever — a
projected top-3 pick starts stronger than an undrafted free agent. The natural
implementation is to learn the mapping directly: draft tier → starting attribute
and badge vector.

The sample does not support it. One roster carries roughly sixty rookies spread
across five tiers (top-3, lottery, late first, second round, undrafted). Twelve
players per tier is thin for a sixty-dimensional attribute vector, and it
collapses entirely once badges are involved — badges are ordinal 0–4 and sparse,
so a per-tier conditional distribution over eighty of them has nothing to stand
on.

## Decision

Do not model draft slot → ratings directly. Decompose into three independent
estimates, each fitted where the sample is adequate:

1. **Draft tier → overall rating band**, from real draft data. This is the *only*
   place draft tier enters the model.
2. **Archetype**, from clustering attribute vectors across a full roster (~918
   players — a healthy sample) or authored by hand until that exists.
3. **Badges**, as a conditional distribution given (archetype, OVR band) — not
   given tier.

Creation then samples: pick tier and archetype → draw a starting attribute and
badge vector.

## Consequences

**Buys:** each estimate is fitted against a sample that can support it. Tier is
reduced to a single scalar (an OVR band), which sixty rookies *can* inform.
Archetype gets the full roster rather than the rookie slice. Badges condition on
things that actually predict them.

**Costs:** three models instead of one, and the composition can be wrong even
when each part is right — a tier/archetype combination that never occurs in
reality (an undrafted 7'0" playmaker) is sampleable here, because the pieces were
fitted independently.

**Forecloses:** capturing genuine tier-specific texture. If top-3 picks are
distinctive in some way that isn't just "higher OVR", this decomposition cannot
see it.

## Notes for when clustering happens

Carried from `DESIGN.md` §5.4 so they aren't rediscovered:

- **PCA first.** 2K attributes are heavily collinear — shooting and athleticism
  move in blocks — so cluster in reduced space.
- **Choose k by silhouette, then override for nameability.** Six to ten
  archetypes a human recognizes beats the statistically optimal seventeen.
- **Cluster on attributes only.** Badges are ordinal and sparse; mixing them into
  the distance metric distorts more than it informs.
- **The interesting output is the archetypes that don't map cleanly** onto 2K's
  own six. Those are real player types the existing tooling can't express.

## Alternatives considered

**Model draft slot → ratings directly.** Rejected on sample size, as above.

**Hand-author a starting vector per (tier, archetype) pair.** Roughly fifty
combinations, each a sixty-dimensional vector. Tedious but tractable, and it is
effectively what v1 does for the archetype layer. Rejected as the *general*
answer because it is taste rather than data, which is what **P4** exists to
avoid.

**Drop draft tier entirely; let the player pick a starting OVR.** Honest and much
simpler. Rejected because the draft-tier framing is part of the fantasy — being
a second-round flier is a different story than being a number-one pick, even at
the same rating.

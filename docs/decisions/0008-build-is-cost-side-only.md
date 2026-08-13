# 0008 — The build prices upgrades; it never scores production

**Status:** accepted · 2026-08-12

## Context

The build — vitals plus archetype — is the central decision of the game
(`GAME_DESIGN.md` §3.1). It shapes starting attributes and what upgrades cost. The
open question was whether it should also shape **what production is worth**.

The intuition for "yes" is strong: a rim-running big is *supposed* to finish
inside, so measure them against that. But it composes badly with the cost layer.
If out-of-class attributes cost more *and* out-of-class production earns less,
the two penalties compound. A big who develops a jumper pays a premium to acquire
it and then earns less when it works — so building toward it also slows the
income funding it.

That turns the class pick from a commitment into a cage. The stated design goal
is that an off-archetype build reads as *a choice with a price*, never as a
mistake the system punishes. Under compounding penalties it isn't merely
expensive, it's dominated.

## Decision

**Neither vitals nor archetype appear anywhere in the scoring model.**

Two players who post identical box scores earn identical currency, whatever they
were built as. A slasher who develops a three is rewarded for made threes exactly
as a sharpshooter is.

The build shapes **what things cost**. It never shapes **what production is
worth**. One lever, not two.

Expectation remains relative — production is still scored against what *should*
have been produced — but it is conditioned on **rating, position, and minutes**.
Position stays in the model; archetype does not.

## Consequences

**Buys:** off-archetype builds are expensive to reach and fully rewarding once
reached, which is the intended shape. The scoring model gets simpler and has one
fewer axis to calibrate. Anti-convergence pressure lives entirely in pricing,
where [ADR 0006](0006-decompose-draft-tier.md)'s affinity structure already puts
it.

**Costs:** the engine cannot express "this player is doing their job well" in
archetype terms. A defensive specialist and a scorer at the same position and
minutes are held to the same bar, and only one of them has a box score that
reflects their job — see the known bias below.

**Forecloses:** archetype-specific grading of any kind, including sympathetic
versions like "credit a rim protector for blocks." Reintroducing archetype on the
scoring side reopens the cage problem regardless of intent.

## Known bias

An archetype-blind model is still **data**-biased. Box scores measure offense far
better than defense. Conditioning on position absorbs part of it — centers are
expected to block and rebound — but a rim protector and a post scorer at the same
position, minutes, and rating are graded by the same yardstick.

This is tracked as **[OPEN-8]** in `GAME_DESIGN.md` and is measurable once the
expectation model is fitted (Phase 2). It is a known risk, not a solved problem.
The tempting fix — an archetype term in scoring — is precisely what this ADR
forbids; a legitimate fix would adjust how defensive counting stats are weighted
for *everyone*.

## Alternatives considered

**Archetype shapes the expectation bar, not the payout.** The first proposal: a
big is *expected* to rebound, so threes read as above-expectation and earn more.
This avoids the double penalty and was nearly adopted. Rejected as strictly more
complex than blindness for the same outcome — if surprising production already
beats a rating-based bar, the archetype term adds calibration surface without
changing the sign.

**Archetype shapes both cost and payout.** The compounding version. Rejected on
the cage argument above.

**No expectation at all — score raw production.** Rejected long before this ADR:
it rewards opportunity over performance and makes XP grow with skill, which is
the backwards-progression problem this project exists to fix.

# 0009 — Do not model athletic regression

**Status:** accepted · 2026-08-12

## Context

Real players decline. Vertical, speed, and lateral quickness fade through the
late twenties and thirties while skill and feel hold up or keep improving. 2K
models this in its own progression, and an early working position for this
project was to model it too: age should *cost* athletic attributes while skill
stays improvable, creating real late-career decisions about spending to hold off
decline in some areas while still growing in others.

**P4** says real careers are the reference and curves should be fitted rather
than invented. Regression is the most obviously real thing a career does.

## Decision

**Athletic regression is not in the design.** Nothing takes back attributes the
player earned.

This is a **rejection, not a deferral** — distinct from the age/development
multiplier, which is deferred and may yet be adopted.

## Consequences

**Buys:** the late career stays about building someone rather than about holding
a line. A player's ending is chosen rather than scripted — the engine has no
opinion about when you are finished, and a career ends when you decide it ends.

**Costs:** this is unrealistic, and knowingly so. It is the one place the design
picks the enjoyable model over the accurate one. A thirty-six-year-old will keep
whatever athleticism they bought at twenty-two, which is wrong.

It also softens the long-run difficulty curve: with nothing eroding, late-career
XP has no maintenance burden to fund, so it all goes to growth.

**Forecloses:** the late-career tradeoff that was originally seen as a feature —
spending to slow decline in one area while growing another. That was a genuinely
interesting decision and this ADR gives it up on purpose.

**Constrains P4:** real careers are the reference for *how growth behaves*, not
for how careers end. Any future falsifiability harness compares growth
trajectories, and must not flag the absence of decline as a calibration failure.

## Reasoning

A career that ends with the player spending currency to replace what age took —
buying back speed every season and losing ground anyway — is an accurate model of
aging and a bad ending to a game. It converts the last third of a career from
*building someone* into *fighting a battle you are scripted to lose*.

Deceleration is already handled without it. Flat expectation-relative income
means a better player has to beat a higher bar to earn anything, and superlinear
cost means each point is dearer than the last. The curve already flattens; it
simply never turns down.

## Alternatives considered

**Model regression faithfully.** Realistic, matches 2K, creates late-career
decisions. Rejected on the experience argument above.

**Model regression but grant a maintenance stipend that covers most of it.**
Keeps the shape while removing the sting. Rejected as the worst of both — the
player still watches numbers fall, still spends on maintenance, and the stipend
is a fudge factor with no principled value.

**Soft-cap athleticism by age instead of decaying it** — no loss, but growth in
athletic attributes gets very expensive after thirty. Rejected *for now* as
scope, not as a bad idea; it preserves "nothing is taken away" while adding age
texture, and is the natural candidate if this ADR is ever revisited alongside the
deferred age multiplier.

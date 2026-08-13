# Engineering Notes

> **What lives where.** This document holds **open engineering work** — mechanism
> math that isn't settled and architecture notes that haven't earned an ADR.
>
> - **What the game is** → [`GAME_DESIGN.md`](GAME_DESIGN.md)
> - **What gets built, in what order** → [`ROADMAP.md`](ROADMAP.md)
> - **Settled decisions** → [`docs/decisions/`](docs/decisions/)
> - **What can be read and how sure we are** → [`docs/data-access.md`](docs/data-access.md)
>
> Split out of the original idea-capture document on 2026-08-12. Anything that
> became a decision is now an ADR; anything that became a verified fact is now in
> `data-access.md`. What's left is genuinely unfinished.

---

## 1. The convergence analysis

Preserved in full because it is the load-bearing argument behind the affinity
cost model, and both [ADR 0008](docs/decisions/0008-build-is-cost-side-only.md)
and `GAME_DESIGN.md` §9 reference it.

**The problem.** With a convex per-attribute cost curve, the cheapest marginal
point is *always* your worst attribute. Spend rationally for long enough and you
converge on a flat 90-everything player. The curve isn't failing — it is a
gradient pointing straight at homogenization.

**This is structural, not a tuning issue.** If every attribute shares the same
convex cost curve and you are maximizing total ability, the optimum sits where
marginal costs are equal — i.e. **all attributes equal**. No purely per-attribute
cost function can produce specialization. Tuning steepness only changes how long
convergence takes.

Badge thresholds *do* create concentration pressure, because they are a
non-linear payoff. But they are **one-shot**: hit the thresholds for the tiers you
want and the incentive is satisfied and gone, after which the convex curve
resumes flattening you. That is exactly the observed arc in prior art.

**Where the argument breaks — and why the design works.** The conclusion holds
only while the curve is *identical across attributes*. A per-(vitals, archetype)
affinity multiplier breaks that symmetry: marginal costs still equalize, but they
now equalize at **different attribute levels** depending on affinity.
Specialization falls out of the cost structure itself rather than needing an
external correction.

This is why the build is priced rather than capped. A multiplier steep enough to
be prohibitive is strictly better than a wall — it says *if you really want it*
instead of *no*.

## 2. Open mechanism work

None of this is settled. Each gets a scoping panel in the phase that owns it —
see [`ROADMAP.md`](ROADMAP.md).

### 2.1 Expectation model — Phase 2, item 2.3

Production is scored against what a player of your **rating, position, and
minutes** should produce ([ADR 0008](docs/decisions/0008-build-is-cost-side-only.md)
settles that archetype is not a term). Unsettled:

- Functional form. Per-36 rates conditioned on an OVR band? A fitted regression?
  Separate models per counting stat, or a joint one?
- How rating enters — banded or continuous. Banded is easier to fit and creates
  cliffs at band edges.
- Which box-score fields participate. Efficiency (FG%, 3P%, FT%) behaves very
  differently from volume at low minutes.

### 2.2 Small-sample shrinkage — Phase 2, item 2.3

Naive per-36 explodes at low minutes: one turnover in five minutes shouldn't nuke
you, 2-for-2 shouldn't be a jackpot. Empirical-Bayes shrinkage toward the prior,
with weight falling as minutes accumulate. Bounds both upside and downside and
caps what a single bad game costs.

Unsettled: what the prior *is* (league average at that rating? the player's own
season-to-date?), and how fast weight decays.

### 2.3 Affinity layer combination — Phase 2, item 2.6 · **[OPEN-7]**

Two multiplicative layers (vitals, archetype) compound badly at the edges — an
unclamped 5'10" post scorer comes out as cheap to build as an average one.
Proposed shape is asymmetric clamping: vitals get a wide band, archetype a narrow
one, so a class pick bends physical reality without cancelling it. Numbers in
`GAME_DESIGN.md` §3.1.3 are illustrative.

### 2.4 Cost curve shape — Phase 2, item 2.7

Superlinear in current rating: 60→61 trivial, 87→88 punishing. Unsettled whether
that is exponential, polynomial, or a lookup table, and whether the exponent is
global or per-attribute-family.

### 2.5 Baseline XP floor — Phase 2

Full at garbage-time minutes, decaying **smoothly** toward zero at starter
minutes ([ADR 0005](docs/decisions/0005-no-training-subsystem.md)). A hard cutoff
at ~20 minutes means 19 vs 21 produces an earnings cliff — arbitrary, and invites
gaming. Unsettled: the decay function and where it effectively reaches zero.

## 3. Architecture notes not yet ADRs

- **Output a worksheet, not a state.** Since changes are applied by hand, each
  cycle's artifact is a diff: *Driving Dunk 78→81, Close Shot 71→74, equip
  Posterizer (Silver)*. Optimize for foolproof transcription — that is where app
  state desyncs from the game, and there is no way to detect the desync
  ([ADR 0001](docs/decisions/0001-no-save-decryption.md)).
- **Two packages, one repo.** `src/rpg_core/` is the I/O-free domain; the API and
  web app depend on it and it depends on neither. A research/modeling layer
  (notebook-shaped, different lifecycle) sits separately under `research/`.
  Separating now beats untangling later.
- **The read-model is disposable.** SQLite in `var/`, rebuilt by replaying
  `careers/`. If rebuilding it is ever inconvenient enough to tempt a migration,
  something has gone wrong with
  [ADR 0003](docs/decisions/0003-event-sourced-tracked-ledger.md).

## 4. Open engineering questions

- **Where does the read-model boundary sit?** Fold-on-read is simplest and gets
  slow; a materialized projection is faster and can drift. Probably fold-on-read
  until it hurts, with the replay test as the safety net.
- **How are hot zones and animation packages represented,** if they enter scope
  at all? Hand-editable in-game and part of the mode, but currently post-v1.
- **Does the worksheet need to be printable/exportable,** or is on-screen enough?
  Bears on whether a second monitor is assumed.
- **What is the minimum viable box-score field set?** Every field not captured is
  a field no future ruleset can ever use — the log only remembers what was
  recorded. Argues for over-capturing at entry even when nothing consumes it yet.

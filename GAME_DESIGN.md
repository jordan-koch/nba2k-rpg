# NBA 2K26 RPG — Game Design

> **Status: first draft, 2026-08-12.** This document states *what the game is*.
> `DESIGN.md` holds the engineering notes and the mechanism work; where the two
> disagree, this one wins and `DESIGN.md` gets corrected.
>
> Sections marked **[OPEN]** need a ruling before they can be built.

---

## 1. The fantasy

You created a player, dropped them into a draft class, and you're playing MyNBA
locked to them. Every game produces a box score, and that box score is the only
thing that makes your player better.

> **A career that develops the way a real one does, driven by what you actually
> did on the floor, inside the limits of who you chose to be.**

Three feelings it chases:

- **Earned.** When Driving Dunk goes 78→81, you know which games paid for it.
- **Constrained.** You're a rim-running big. You *can* learn to shoot threes. It
  will cost you, and that cost is what makes it a decision instead of a menu.
- **Believable.** The trajectory looks like a real player's — fast early,
  plateauing, and declining in the legs long before the hands.

---

## 2. Pillars

Every mechanic gets tested against these four. A mechanic that serves none of
them is cut, however clever.

**P1 — Nothing is arbitrary.** Every point of currency traces to a game you
played. Every price traces to a rule you can read. If you can't explain why an
upgrade cost what it cost, the system has failed at its only job.

**P2 — The class is a commitment, not a label.** Your archetype changes what's
cheap, what's expensive, and what counts as doing your job. Going against it is
always possible and always costly.

**P3 — You're graded against yourself, not against zero.** Production is measured
against what a player of your rating, role, and minutes *should* produce.
Improving raises your own bar.

**P4 — Real careers are the reference.** Curves are fitted to real NBA
development, not tuned by taste. When the model and reality disagree, the model
is wrong.

---

## 3. The player's decisions

The engine computes the currency and sets the prices. What's left for the player
*is* the game. In descending order of weight:

### 3.1 Creation — the build, decided once

Creation takes seven inputs. All but the name shape the starting vector:

| Input | Role |
|---|---|
| **Name** | Cosmetic only |
| **Height / weight / wingspan** | *Vitals* — the physical layer (§3.1.1) |
| **Primary position** | Depth-chart role and expectation baseline. **Not** the build. |
| **Archetype** | *Skill orientation* — the class layer (§3.1.2). Enumerated later. |
| **Projected draft position** | Difficulty lever — sets the starting OVR band. Enumerated later. |

**Position and archetype are separate axes.** A slasher can be any height. This
matters because the modern NBA has largely dissolved positional prescription
while leaving physical reality intact — the best shooters still skew small, the
best rim protectors still skew tall, and that's a fact about bodies rather than
about position labels.

Everything except the badge loadout is decided here and lived with. A build you
can switch is a label; the commitment is the mechanic.

#### 3.1.1 Layer one — vitals

Height, weight, and wingspan set per-attribute cost multipliers on their own,
before archetype is considered. A 7'0" build pays more for speed, agility, and
ball handling and less for strength, rebounding, and interior finishing. A 5'10"
build pays the inverse.

This layer is **empirical, not authored** — the real relationship between size and
each attribute is measurable across a full roster of real players (§3.1.4).

#### 3.1.2 Layer two — archetype

Skill orientation, independent of size. A *slasher* gets cheaper driving dunk,
speed, and finishing regardless of whether they're 6'2" or 7'0"; they pay more for
three-point shooting either way.

This is the RPG class. An axe-swinging mage is buildable, slow, and expensive —
never forbidden. An out-of-class build should read as *a choice with a price*,
never as a mistake the system punishes.

#### 3.1.3 How the two layers combine — **[OPEN-7]**

The layers multiply, but **archetype must not be able to fully cancel vitals.**
Unclamped multiplication makes a 5'10" post scorer as cheap to build as an
average one, which is wrong: a body is a harder constraint than a class pick.

Proposed shape — archetype gets a narrow band, vitals get a wide one:

```
cost = base(rating) × vitals_mult × archetype_mult
       vitals_mult    ∈ [0.5, 3.0]     wide — physical reality
       archetype_mult ∈ [0.6, 1.6]     narrow — orientation, not transcendence
```

The test case is the tall playmaker. A 7'0" playmaker pays `2.5 × 0.6 = 1.5×` for
ball handling — meaningfully cheaper than a 7'0" non-playmaker at `2.5×`, and
still far dearer than a 6'2" playmaker at `0.7 × 0.6 = 0.42×`. That's the right
answer: Jokić is a real, buildable, expensive build, not a free one.

#### 3.1.4 Where the multipliers come from

The vitals layer is a regression, not a taste judgment: fit each attribute against
height / weight / wingspan across a full roster of real rated players. This is
**P4** applied to character creation.

Two notes:

- **Use the wingspan residual, not raw wingspan.** Wingspan is nearly collinear
  with height; the informative feature is *plus-wingspan* (wingspan − height).
  Feeding both raw values into the same fit mostly measures height twice.
- **The archetype layer is hand-authored initially** and validated against the
  corpus later (see `DESIGN.md` §5.4 and **[OPEN-4]**).

#### 3.1.5 One structure, two jobs

The same (vitals × archetype) affinity table that prices upgrades also **generates
the starting vector**: high-affinity attributes start higher. Draft tier scales
the whole vector to an OVR band.

That's one mechanism serving creation and progression both, rather than a
generator and a cost model that can silently disagree with each other.

### 3.2 Where XP goes — continuous

Constrained by the affinity table. Note that the interesting version of this
decision is *not* "what's cheapest" — the affinity table already answers that.
It's **how far to push in-class before paying the out-of-class premium**, which
is a genuine tradeoff at every stage of a career.

### 3.3 Badge loadout — revisable

Earn any badge you qualify for; equip a limited number, with higher tiers
consuming more budget. This is the **only decision you can take back**, and it's
what lets a player adapt to a changing role without betraying the class pick.

### 3.4 Milestone timing — occasional

When to cash a once-per-career windfall (see §5).

### 3.5 What the build does *not* do — *(settled)*

**Neither vitals nor archetype appear anywhere in the scoring model.** Two players
who post identical box scores earn identical currency, whatever they were built
as. A slasher who develops a three is rewarded for made threes exactly as a
sharpshooter is.

The build shapes **what things cost**, never **what production is worth**. One
lever, not two.

This is what keeps the class a commitment rather than a cage. Under the rejected
alternative — out-of-class attributes cost more *and* out-of-class production
earns less — the axe-swinging mage isn't merely expensive, it's self-defeating,
because building toward it also slows the income funding it.

**Expectation (P3) is still relative**, but it's conditioned on rating, position,
and minutes — never on archetype. Position stays in the model; archetype does
not.

> **Known bias — [OPEN-8].** Box scores measure offense far better than defense.
> An archetype-blind scoring model is still *data*-biased: a rim protector and a
> post scorer at the same position, minutes, and rating are measured by the same
> yardstick, and only one of them has a box score that reflects their job.
> Conditioning on position absorbs part of this. The residual is real and needs
> measuring rather than assuming.

---

## 4. The loop

The ceremony is **per game**.

```
play a game
  └─> enter the box score          (~30s, keyboard-driven)
       └─> see THE GRADE           ← the emotional payload
            └─> XP accrues         (usually modest)
                 └─> spend when you want to
                      └─> worksheet: a diff to apply by hand in-game
```

**The per-game beat is "how did I do," not "what did I buy."** Expectation-relative
XP with small-sample shrinkage produces modest, noisy per-game numbers by design
(§P3) — so if the per-game payload were the XP, most games would feel like
nothing happened. It isn't. The payload is the **grade**: what you produced
against what was expected of you, legible immediately, every game.

XP accumulates quietly underneath. Spending is a separate act, taken when the
player wants a decision rather than on a schedule.

Two human steps remain, and always will: **entering the box score** and
**applying the worksheet**. Everything between them is the engine's.

---

## 5. Milestones

A second income stream, deliberately kept small and punctuating.

**Box-score-derived** — cheap to build, since the engine already has every box
score. "Score 2,000 points in a season." "500 career blocks." Achievement-shaped.

**Non-box-score** — All-Star selections, awards, championships, contract
signings. These are *not* derivable from anything the engine sees, so they need a
manual entry surface: the player asserts them, the engine records them. In ledger
terms this is a second event type alongside `GamePlayed`.

**The constraint that makes this safe:** milestone thresholds scale with counting
stats, and counting stats scale with skill — so a naive milestone system
reintroduces exactly the positive feedback loop §P3 exists to kill. Better
players hit more thresholds and earn more windfalls, and the curve bends back the
wrong way.

Two rules hold it:

1. **Each milestone fires once per career.** Never repeatable, never per-season
   for the same achievement.
2. **Total milestone income is capped as a share of career XP.** The number is
   **[OPEN-3]**.

Milestones are punctuation. If they become a meaningful fraction of income, the
economy is no longer governed by the expectation model and §P4 is unfalsifiable.

---

## 6. What this is not

- **Not a simulator.** You play the games. This never decides an outcome.
- **Not a stat tracker.** Tracking is a side effect of the economy, not a goal.
- **Not a roster editor.** It tells you what to change; you change it in-game.
- **Not a replacement for 2K's progression system.** There isn't one in this
  mode. That absence is the entire reason this exists.

---

## 7. Failure modes

Checked against every proposed mechanic.

| Mode | Description |
|---|---|
| **Arbitrary** | The root failure. Every other mode is a species of it. |
| **Low-minute dead end** | A bench player has no path to improve, so the mode only works from a starting role. |
| **Backwards curve** | Improving faster at 28 than at 21. |
| **Convergence** | Long careers flatten toward 90-everything and builds stop being distinct. |
| **Cosmetic class** | *(new)* Affinity multipliers too gentle — the class becomes flavor text and **P2** fails. |
| **Milestone inflation** | *(new)* Windfalls grow into real income and stop the expectation model from governing the curve. |
| **Class as cage** | *(new)* Out-of-class play penalized on both cost and earning, so the only viable build is the one the class prescribes. See §3.5. |
| **Losing battle** | *(new)* Late career becomes spending to stand still. See §7.1. |

### 7.1 On modeling decline — *(settled: no)*

Athletic regression is realistic and it is **not** in the design.

A career that ends with the player spending currency to replace what age took —
buying back speed each season, losing ground anyway — is an accurate model of
aging and a bad ending to a game. It converts the last third of a career from
*building someone* into *fighting a battle you're scripted to lose*. The realism
is real; so is the fact that it feels awful.

The stance instead: **a career ends when you decide it ends.** The engine has no
opinion about when you're finished. Growth slows naturally — flat
expectation-relative income plus superlinear cost already decelerate the curve
without anyone modeling decay — but nothing takes back what you earned.

This is the one place the design deliberately chooses the enjoyable model over
the accurate one, which is worth stating plainly rather than discovering later
and mistaking it for an oversight. It also constrains **P4**: real careers are the
reference for *how growth behaves*, not for how careers end.

---

## 8. Open questions

**[OPEN-1] — ~~Does the build shape the bar or the payout?~~ SETTLED.**
Neither. The build is cost-side only; the scoring model is blind to vitals and
archetype alike. See §3.5.

**[OPEN-2] — Does the affinity table replace `DESIGN.md` §5.3's other levers?**
§5.3 proposed three anti-convergence levers: a badge equip budget, an elite tax
on total investment, and hard caps from the roster corpus. Per-archetype affinity
multipliers may do most of that work alone — see §9. Current leaning: **keep the
badge budget** (different axis — active loadout, not acquisition), **drop the
elite tax** (redundant), **replace hard caps with pricing** (an affinity
multiplier steep enough to be prohibitive is better than a wall, and matches the
axe-mage framing).

**[OPEN-3] — What share of career XP may come from milestones?**
Needs a number, and it should be small.

**[OPEN-4] — How many archetypes, and where do they come from?**
For a first version they can be hand-authored with hand-authored affinity tables.
`DESIGN.md` §5.4's clustering work then *validates or replaces* them empirically
rather than being a prerequisite.

**[OPEN-5] — Is the badge equip budget fixed or growing over a career?**
Carried over from `DESIGN.md` §7. Fixed makes every season a real tradeoff;
growing feels good late but reopens the convergence problem.

**[OPEN-6] — Does the generalist build exist in the real NBA?**
Carried over. Under the class frame this softens considerably: a generalist is
now just an archetype with a flat affinity table, competing against specialists
whose steep tables buy them more depth for the same XP. It stops being a question
about whether the design *permits* generalists and becomes one about how to price
the flat table.

**[OPEN-7] — How do the vitals and archetype layers combine?**
§3.1.3 proposes clamped multiplication — wide band for vitals, narrow for
archetype, so a class pick bends physical reality without cancelling it. The
bands are guesses; the *shape* is the thing to agree on first.

**[OPEN-8] — How much does box-score bias penalize defensive archetypes?**
See §3.5. Archetype-blind scoring is still data-biased toward offense.
Measurable once there's a fitted expectation model — until then, a known risk
rather than a solved problem. Resist fixing it by reintroducing archetype into
scoring; that reopens **[OPEN-1]**.

**[OPEN-9] — Is the vitals layer static or does it evolve?**
A 22-year-old adds weight and strength; a 34-year-old loses lift. Vitals are
currently modeled as fixed at creation. Whether weight (and therefore its cost
multipliers) drifts over a career interacts with the aging work in
`DESIGN.md` §5.2.

---

## 9. What the class frame changes about `DESIGN.md` §5.3

Worth recording, because it partially resolves the sharpest analysis in that
document.

§5.3 argued — correctly — that convergence is **structural**: if every attribute
shares the same convex cost curve and you're maximizing total ability, the
optimum sits where marginal costs are equal, which is all attributes equal. It
concluded that no purely per-attribute cost function can produce specialization.

That conclusion holds only while the curve is **identical across attributes**.
A per-(archetype, attribute) affinity multiplier breaks the symmetry the argument
depends on: marginal costs still equalize, but they now equalize at *different
attribute levels* depending on affinity. Specialization falls out of the cost
structure itself rather than needing an external correction.

The class pick was proposed as an agency mechanic. It also happens to be the
cleanest available answer to §5.3 — and unlike a hard cap, it prices the
out-of-class build instead of forbidding it.

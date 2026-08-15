# Roadmap

> **10,000-foot view, 2026-08-12.** Deliberately handwaves detail. The point is a
> concrete v1 boundary and the milestones to reach it — not a spec.
>
> `GAME_DESIGN.md` says what the game is. This says what gets built, in what
> order, and what each step proves.

---

## v1

> **A serviceable web app in which you can run a multi-season career from draft
> onward, on more than one build at a time, where every attribute and badge change
> you applied in-game was issued by the engine.**

It fails loudly. The moment you hand-wave an upgrade because the engine couldn't
price it — or reach for a spreadsheet because the app couldn't show you something
— v1 isn't done.

### In scope — the engine

| | Why it can't be cut |
|---|---|
| **Creation** — vitals, position, archetype, draft tier → starting vector | The class pick is the game's central decision (`GAME_DESIGN.md` §3.1) |
| **Affinity cost model** — vitals × archetype | Without it the archetype is cosmetic and **P2** fails |
| **Expectation-relative XP** — fitted to real NBA production | Without it every number is arbitrary and **P1** fails |
| **Superlinear cost in current rating** | The other half of the anti-convergence pressure |
| **Event log + fold + replay test** | The ledger is the only copy of a career; replay is what makes retuning safe |
| **Versioned rulesets** | Phase 2 replaces the whole economy in place — this is what makes that a config change |
| **Badge unlock + equip budget** | The one revisable decision in the game |
| **Concurrent careers** | The test instrument for the central design claim — see below |
| **Multi-season structure** — seasons roll over, age tracked, career totals accumulate | A career that only runs one season isn't a career |
| **Season transition** — a thin offseason training block paying out currency | The once-a-year ceremony |
| **Milestones** — box-score-derived thresholds and manually-entered accolades | Punctuation; gives a season shape beyond the per-game drip |

### In scope — the application

Not a form and a worksheet. A serviceable web app you actually manage a player in.

| Surface | Contents |
|---|---|
| **Career management** | Create, list, view, archive. Switch between concurrent careers |
| **Player state** | Attributes, badges, vitals, age, current OVR, XP balance |
| **Game log** | Browse every game entered; **correct a mis-entered box score** |
| **Box-score entry** | Fast, keyboard-driven |
| **Spend flow** | Browse prices under your affinity table, purchase, generate the worksheet |
| **Badge loadout** | Equip and re-equip within budget |
| **Progression history** | Attributes and XP over time — the thing that makes a career legible |
| **Milestone tracker** | What's hit, what's close, what's unclaimed |
| **Career comparison** | Light. Concurrent careers are pointless if you can't hold them side by side |

**"Serviceable" is a real constraint in both directions.** It must genuinely do
the job — no reaching for a spreadsheet. It does not need to be beautiful, and
design polish is not a v1 gate.

> **Note on CRUD over an append-only log.** Correcting a box score cannot mutate
> the event that recorded it — that would silently rewrite history and break the
> replay guarantee. Updates and deletes are *appends*: a correction event that
> supersedes the original, with the fold resolving it. A naive CRUD layer over
> the ledger is the single easiest way to destroy the architecture's main payoff,
> so this belongs in Phase 1, not as a later fix.

**Concurrent careers earn their place on a stronger argument than convenience.**
**P2** claims the build is a commitment that produces genuinely distinct players.
That claim is *untestable at n = 1* — you cannot tell whether a slasher and a
sharpshooter feel different without running both. It measures the design's
central promise.

It's also **cheap in Phase 1 and expensive retrofitted**: a directory per career
and a career id on every event, versus unpicking a singleton later.

### Out of scope

| | Status |
|---|---|
| **Age/development multiplier** — XP income decaying with age | **Deferred by decision.** Needs care; revisit as an update once the base economy has been observed |
| **Regression** — athletic attributes decaying with age | **Rejected, not deferred.** Late career becomes spending to stand still. `GAME_DESIGN.md` §7.1 |
| Empirically-derived archetypes | Post-v1 — hand-authored works for v1 |
| Hard caps from a roster corpus | Post-v1 — pricing may make them unnecessary |
| Roster struct decode | Post-v1, possibly never — external ratings give the same cross-section |
| **Falsifiability harness** — career arc vs. real players | Post-v1. See the honesty note |
| OCR box-score capture | Post-v1. **Confirmed out.** Manual entry is fine |
| Hot zones, animation packages | Post-v1 |

### Why deferring the age multiplier is defensible

Worth recording, because it looks like a gap and isn't quite one.

`DESIGN.md` §5.2 stacks three levers against the backwards-progression problem:
flat income (expectation-relative), a decaying age multiplier, and superlinear
cost. **Two of the three ship in v1.** Flat income means outperforming your own
rating is the only way to bank XP; superlinear cost means each point costs more
than the last. Together they already produce a decelerating curve.

What's missing without the third lever is *decline*, and age-independence: a
21-year-old and a 31-year-old at identical ratings progress identically. Wrong,
but not broken — and three compounding brakes is a real overshoot risk. Watching
two levers behave before adding a third is the right order.

### The honesty note

v1 has a **fitted** economy — XP tracks real production norms. It does not have a
**falsified** one: nothing checks a finished career's trajectory against real
players who entered at the same tier. Until that exists, **P4** is design intent
rather than a demonstrated property.

"Calibrated" is not "falsifiable." Worth keeping the words apart.

---

## Phases

Each phase is a **vertical slice** — end to end, shipping usable software, rather
than completing a horizontal layer. The application is a first-class deliverable
in every one of them, not a wrapper added at the end.

Every row below is intended to be one intake item and one feature branch.

**Size:** `S` a sitting · `M` a day or so · `L` multi-day.
**Panel:** ★ means the decision is expensive to reverse — run the full scoping
panel. Unmarked items should skip straight to a plan or straight to work.
**Status:** `NOT STARTED` · `IN-PROGRESS` · `DONE`. Every item row carries one,
and every phase header carries the aggregate. A phase is `DONE` only when all of
its items are and its **Exit** condition has actually been met.

> **This table is maintained by [`/commit`](.claude/skills/commit/SKILL.md).**
> The commit gate checks the staged diff against these rows and advances the
> statuses in the same commit as the work. Statuses are a record of what landed,
> not a plan — don't mark an item `DONE` ahead of its commit.

### Phase 0 — Harness — **DONE**

**Proves:** nothing. It's the workbench.
**Exit:** a green CI run on an empty repo, and every document doing one job.
**Status:** **DONE** — 2026-08-12. Exit met: CI green, branch protection on,
documents split to one job each.

| # | Item | Deliverable | Size | Needs | Status |
|---|---|---|---|---|---|
| 0.1 | `repo-init` | git init, GitHub remote, `.gitignore`, `.gitattributes`, README skeleton | S | — | DONE |
| 0.2 | `python-toolchain` | `pyproject.toml` (uv/ruff/mypy strict/pytest), `src/` package, first structural test | S | 0.1 | DONE |
| 0.3 | `ci-harness` | GitHub Actions, branch protection, dependabot, secret scan | S | 0.2 | DONE |
| 0.4 | `request-tracks` | `requests/` three tracks, READMEs, Index convention | S | 0.1 | DONE |
| 0.5 | `skills-port` | `.claude/skills/` ported from `nba-analysis` + `settings.json` | M | 0.4 | DONE |
| 0.6 | `docs-split` | 7 ADRs extracted, `docs/data-access.md` written, `DESIGN.md` shrunk to open work | M | 0.1 | DONE |

*Note on 0.6:* the offseason-training ADR must state explicitly why it is not the
practice subsystem `DESIGN.md` rejected.

### Phase 1 — Skeleton — **IN-PROGRESS**

**Proves:** the architecture, and whether the loop is any fun.
**Exit:** two careers, ten box scores each, one correction, a spend, a worksheet
applied in-game.
**Status:** **IN-PROGRESS** — 1.1 `app-shell` has landed the application
skeleton. No domain logic yet; 1.2 `career-ledger` is next.

The economy here is **deliberately fake** — placeholder XP, invented expectation,
guessed affinity numbers. Finding out whether the loop is satisfying comes before
calibrating it.

| # | Item | Deliverable | Size | Needs | Status |
|---|---|---|---|---|---|
| 1.1 | `app-shell` | FastAPI + React/Vite wiring, dev server, health endpoint, frontend build in CI | M | 0.3 | DONE |
| 1.2 | `career-ledger` ★ | Event schema, JSONL append, career directory layout, the fold, replay-determinism test | L | 0.2 | NOT STARTED |
| 1.3 | `correction-by-append` ★ | Superseding-event model so edits and deletes never mutate history | M | 1.2 | NOT STARTED |
| 1.4 | `ruleset-loader` | Versioned ruleset config; every event pins the version live at the time | M | 1.2 | NOT STARTED |
| 1.5 | `player-model` | Attributes, badges, vitals, position — the state the fold produces | M | 1.2 | NOT STARTED |
| 1.6 | `placeholder-economy` | Fake XP formula, fake expectation, guessed affinity table, behind the ruleset interface | M | 1.4, 1.5 | NOT STARTED |
| 1.7 | `player-creation` | Creation inputs → starting vector. API + UI | M | 1.6 | NOT STARTED |
| 1.8 | `box-score-entry` | `BoxScore` DTO, validation, submit endpoint, entry form | M | 1.6 | NOT STARTED |
| 1.9 | `spend-and-worksheet` | Price browse, purchase, worksheet diff output. API + UI | M | 1.6 | NOT STARTED |
| 1.10 | `career-switching` | Career list, create, switch, archive. Multi-career UI | S | 1.7 | NOT STARTED |
| 1.11 | `game-correction-ui` | Edit a mis-entered box score through the append path | S | 1.3, 1.8 | NOT STARTED |

*Multi-career is a structural constraint across all of Phase 1, not item 1.10.*
*Every event carries a career id from 1.2 onward; 1.10 is only its UI.*

### Phase 2 — Economy — **NOT STARTED**

**Proves:** the numbers mean something, and a ruleset swap is a config change
rather than a migration.
**Exit:** a Phase 1 career replays under the real ruleset with no data migration.
**Resolves:** **[OPEN-2]**, **[OPEN-7]**, **[OPEN-8]**, authored half of **[OPEN-4]**.
**Status:** **NOT STARTED**.

| # | Item | Deliverable | Size | Needs | Status |
|---|---|---|---|---|---|
| 2.1 | `datasets-layer` | `datasets/manifest.json`, `lib/paths.py`, resolve-by-name, `hub`/`spoke`/`curated`/`report` | M | 0.2 | NOT STARTED |
| 2.2 | `nba-boxscore-source` | Builder pulling real NBA box scores to `datasets/spoke/`, cached, `--fetch` | L | 2.1 | NOT STARTED |
| 2.3 | `expectation-model` ★ | Expected production given rating, position, minutes, with small-sample shrinkage | L | 2.2 | NOT STARTED |
| 2.4 | `ratings-cross-section` | Builder pulling external 2K ratings with height/weight/wingspan | M | 2.1 | NOT STARTED |
| 2.5 | `vitals-affinity-fit` ★ | Regress attributes on height/weight/plus-wingspan → the vitals multiplier layer | L | 2.4 | NOT STARTED |
| 2.6 | `archetype-tables` ★ | Enumerate archetypes, author the archetype layer, settle the combination rule | L | 2.5 | NOT STARTED |
| 2.7 | `attribute-cost-curve` ★ | Superlinear cost in current rating | M | 1.6 | NOT STARTED |
| 2.8 | `economy-swap` ★ | Assemble ruleset v2, swap it in, replay Phase 1 careers, prove no migration | M | 2.3, 2.6, 2.7 | NOT STARTED |

*Item 2.8 is the architecture's exam. If it needs a migration, the event-sourcing*
*claim in `DESIGN.md` §6 was never true, and better to learn it here.*

### Phase 3 — Season — **NOT STARTED**

**Proves:** it works over 82 games, not 10 — and the app is genuinely serviceable.
**Exit:** a full season played end to end, every upgrade earned, no spreadsheets.
**Resolves:** **[OPEN-5]**.
**Status:** **NOT STARTED**.

| # | Item | Deliverable | Size | Needs | Status |
|---|---|---|---|---|---|
| 3.1 | `badge-system` ★ | Unlock thresholds, equip budget, loadout management. API + UI | L | 2.8 | NOT STARTED |
| 3.2 | `player-dashboard` | The full player state view — attributes, badges, vitals, OVR, XP | M | 2.8 | NOT STARTED |
| 3.3 | `game-log` | Browse, filter, and inspect every game entered | M | 2.8 | NOT STARTED |
| 3.4 | `progression-history` | Attributes and XP over time — what makes a career legible | M | 3.2 | NOT STARTED |
| 3.5 | `fast-entry` | Keyboard-driven entry tuned to survive 82 repetitions | M | 3.3 | NOT STARTED |

### Phase 4 — Career → **v1** — **NOT STARTED**

**Proves:** a career is more than a long season.
**Exit:** **v1.**
**Resolves:** **[OPEN-3]**.
**Status:** **NOT STARTED**.

| # | Item | Deliverable | Size | Needs | Status |
|---|---|---|---|---|---|
| 4.1 | `season-rollover` | Season boundary event, age increment, per-season and career totals | M | 3.5 | NOT STARTED |
| 4.2 | `offseason-training` | The training block and its payout; straight into the next season | M | 4.1 | NOT STARTED |
| 4.3 | `milestones-derived` | Threshold definitions and detection folded from the event log | M | 4.1 | NOT STARTED |
| 4.4 | `accolade-entry` | Manual accolade event type + entry UI for what the engine can't see | M | 4.1 | NOT STARTED |
| 4.5 | `milestone-tracker` | Hit, close, and unclaimed — plus the windfall spend | M | 4.3, 4.4 | NOT STARTED |
| 4.6 | `career-comparison` | Two careers side by side. The instrument **P2** is measured with | M | 4.1 | NOT STARTED |

### Post-v1

Age/development multiplier, if ever. Derived archetypes from clustering. The
falsifiability harness. Hard caps if pricing proved insufficient. The struct
decode, only if external ratings prove inadequate. OCR. Hot zones.

**Not deferred — rejected:** athletic regression. See `GAME_DESIGN.md` §7.1.

---

## Shape of it

```
Phase 0   Harness      ░     workbench                                  ← done
Phase 1   Skeleton     ███   is it fun?                                 ← here
Phase 2   Economy      ████  do the numbers mean anything?
Phase 3   Season       ███   does it survive 82 games?
Phase 4   Career       ███   is a career more than a long season?     ← v1
```

Phase 2 is the heavy one and it's mostly data engineering. Phase 1 is
deliberately the cheapest of the four because its job is to fail fast if the loop
isn't enjoyable.

---

## Risks

**v1 is large.** Real economy, full application, multi-season, milestones,
concurrent careers. The load-bearing mitigation is Phase 1: if the loop isn't
enjoyable on a fake economy, that's known before Phases 2–4 are built. Keep that
phase cheap and keep it honest.

**Event-sourced CRUD is easy to get wrong.** See the note in the application
scope. Correction-by-append lands in Phase 1 or the replay guarantee is
decorative.

**The offseason block sits next to a settled rejection.** `DESIGN.md` rejects a
practice/film/training subsystem as too much machinery. The offseason block is
*not* that — a once-a-year ceremony rather than a repeatable in-season grind —
but the distinction should be written into the ADR explicitly in Phase 0, or it
reads later as a decision quietly reversed.

---

## Open questions, by the phase that answers them

| | Question | Phase |
|---|---|---|
| **[OPEN-2]** | Does affinity replace the other anti-convergence levers? | 2 |
| **[OPEN-3]** | What share of career XP may come from milestones? | 4 |
| **[OPEN-4]** | How many archetypes, and derived or authored? | 2 authored · post-v1 derived |
| **[OPEN-5]** | Badge equip budget fixed or growing? | 3 |
| **[OPEN-6]** | Does the generalist build exist in the real NBA? | post-v1 |
| **[OPEN-7]** | How do the vitals and archetype layers combine? | 2 |
| **[OPEN-8]** | How badly does box-score bias penalize defensive builds? | 2 |
| **[OPEN-9]** | Do vitals drift over a career? | post-v1, with aging |
| **[OPEN-10]** | Does the offseason training payout scale with age? | post-v1, with aging |

None block Phase 0 or Phase 1. Each gets a scoping panel when its phase arrives,
with the loop already in hand to argue against.

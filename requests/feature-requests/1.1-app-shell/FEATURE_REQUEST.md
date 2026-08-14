> **Status:** scoped · created 2026-08-13 · decided · next: plan

# Feature Request — App Shell (Phase 1, item 1.1)

## Problem / Motivation

There is no application. Phase 0 built the workbench — CI, branch protection, the
request pipeline, structural tests — and deliberately stopped there:
[`pyproject.toml`](../../../pyproject.toml) has an empty `dependencies` list with a
comment reserving FastAPI's arrival for this exact item, and
[`src/rpg_core/__init__.py`](../../../src/rpg_core/__init__.py) contains only a version
string.

Phase 1's whole purpose is to find out whether the loop is fun before the economy
is calibrated, and every remaining Phase 1 item — player creation, box-score entry,
the spend flow, career switching — is a *surface*. None of them can be built, run,
or judged without something to attach to. Right now there is no way to serve an
HTTP response, no way to render a page, and no answer to the question "how do I run
this thing." That's what's felt today: the next eleven items are all blocked on the
same missing seam.

Secondarily, the frontend is currently unproven ground in a repo that is otherwise
tightly guarded. Python has ruff, mypy strict, pytest, and a green CI job; a
JavaScript build has none of that yet, and CI does not know it exists. Introducing
the SPA without extending the same posture to it would leave half the codebase
unchecked from its first commit.

## Desired Outcome

A running application skeleton with nothing in it, and a repo that knows how to
check it.

- The user can start the app locally and reach a page in a browser that shows a
  live status fetched from the backend — proving the request actually crossed the
  seam rather than being mocked in the frontend.
- There are two honest ways to run it: a **development** mode with hot reload for
  building the Phase 1 surfaces, and a **serve the built app** mode where the
  backend hands out the compiled SPA, so "run the app" has a real answer that does
  not involve two dev servers.
- CI fails on a broken frontend the same way it fails on a broken backend — a type
  error, a lint violation, or a build failure in the SPA turns the PR red.
- A cold agent picking up item 1.2 can add an endpoint and a page without deciding
  any structural questions this item should have answered.

Explicitly *not* part of "done": the page being nice to look at. `ROADMAP.md`'s
"serviceable" constraint cuts both ways, and design polish is not a v1 gate.

## Rough Ideas (non-binding)

The roadmap row already names the shape: FastAPI + React/Vite wiring, dev server,
health endpoint, frontend build in CI. Beyond that, hunches only — scoping is free
to propose better:

- The SPA likely lives in a top-level `app/`. Not chosen here, but
  [`.gitignore`](../../../.gitignore) already carries `node_modules/`, `.vite/`, and
  `app/dist/` rules from Phase 0, and `CLAUDE.md`'s project map lists serving under
  `app/` — so that convention was anticipated and should probably be honored rather
  than re-litigated.
- The API cannot live in `src/rpg_core/`, which is I/O-free and web-free by rule.
  It probably wants its own package (`src/rpg_api/` or similar) so the domain core
  stays importable without pulling in a web framework. Naming and layout are
  scoping's call.
- Vite's dev-server proxy is the conventional answer to CORS in development, and
  avoids the backend needing CORS middleware at all in local dev.
- The health endpoint is the natural place to report the package version, which
  `tests/test_repo_structure.py` already pins against `pyproject.toml`.

## Scope Signals

- **In:**
  - FastAPI application, a health/status endpoint, and its test.
  - React + TypeScript SPA on Vite, in **strict** mode, with a linter — matching
    the Python side's mypy-strict/ruff posture rather than being the loose half of
    the repo.
  - A development mode (Vite dev server → FastAPI, hot reload) *and* a mode where
    FastAPI serves the built SPA. Both are in.
  - One page: it calls the health endpoint and renders the result. That is the
    entire UI.
  - A **separate CI job** for the web app — Node setup, install, typecheck, lint,
    build — running in parallel with the existing Python job so a red frontend is
    legible on its own.
  - Whatever documentation makes the run story discoverable (`ops/README.md` and/or
    `README.md`), since a launch path nobody can find is not a launch path.
  - Dependency declaration done properly: FastAPI added to
    [`pyproject.toml`](../../../pyproject.toml) with `uv.lock` regenerated, because
    CI runs `uv sync --locked` and a stale lock is a hard failure.

- **Explicitly out:**
  - **Any domain logic.** No player model, no events, no ledger, no economy — those
    are items 1.2–1.6 and each has its own request. `src/rpg_core/` should stay
    empty or near-empty when this lands.
  - **Any career-related endpoint or page.** No career list, no creation form, no
    box-score entry. The status page is the only surface.
  - **Persistence of any kind.** No SQLite, no read-model, no `careers/` directory,
    no migrations. The shell is stateless.
  - **Auth, users, sessions, HTTPS, CORS for non-local origins.** This is a
    localhost app with no credentials and no hosting, per `CLAUDE.md`.
  - **Visual design.** No component library, no theme system, no styling beyond
    what makes the status page legible.
  - **Packaging and distribution.** No Docker, no installer, no `pyinstaller`, no
    deployment target. It runs from a checkout.
  - **A component-test harness for the frontend** (Vitest, Testing Library, etc.).
    There is one page and nothing to test; adding a second test framework before
    there is a second component is machinery ahead of need. Scoping may disagree —
    see Open Questions.

- **Not now / later:**
  - A shared type contract between the API's DTOs and the frontend (generated
    client, OpenAPI codegen, or hand-mirrored types). Genuinely valuable once
    `BoxScore` exists in 1.8 — premature when the only payload is a health check.
  - Routing and app chrome (nav, layout shell). Deferred deliberately: structuring
    an app before it has surfaces pre-decides the structure blind. The first item
    that needs a second page brings it.
  - Frontend test tooling, per above.
  - Any production-grade server story (workers, process supervision).

## Affected Area & Pointers

This item is almost entirely **new** ground — its main risk is not breaking things
but choosing conventions the next eleven items inherit.

A cold scoping agent should read, in order:

- [`ROADMAP.md`](../../../ROADMAP.md) — Phase 1 table for the item row, its
  dependencies (0.3, done), and the eleven items that build on this one.
- [`CLAUDE.md`](../../../CLAUDE.md) — the project map (which directories exist and
  the instruction not to create the others speculatively), the public-repo rules,
  and the stack statement.
- [`pyproject.toml`](../../../pyproject.toml) — empty `dependencies` (line 9) with
  the comment reserving FastAPI for this item; `[tool.mypy] files = ["src", "tests"]`
  (line 65), which will need to cover a new API package; ruff config; the
  `[tool.hatch.build.targets.wheel] packages = ["src/rpg_core"]` line, which a second
  source package changes.
- [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) — the existing
  `python` and `secrets` jobs. Note `uv sync --locked` (line 34) and
  `--cov=rpg_core` (line 47); a new job goes alongside these.
- [`ops/branch-protection.json`](../../../ops/branch-protection.json) — *verified:*
  `required_status_checks.contexts` is `["Lint, types, tests", "Secret scan"]`, the
  jobs' **display names**. A new CI job is therefore not a required check until its
  `name:` is added here *and* the config is re-applied to GitHub. Easy to miss, and
  the symptom is a PR that merges green while the frontend job was failing.
- [`.gitignore`](../../../.gitignore) — the Node/web-app block already present, and
  the careers carve-out warning about blanket rules.
- [`tests/test_repo_structure.py`](../../../tests/test_repo_structure.py) — the
  structural-guard idiom this repo uses; a new top-level directory and a new source
  package are the kind of thing that gets a guard here.
- [`src/rpg_core/__init__.py`](../../../src/rpg_core/__init__.py) — currently the
  whole domain core; establishes that it holds a version and nothing else.
- [`ops/README.md`](../../../ops/README.md) — where the local toolchain is
  documented; the Node toolchain likely joins it.

**No dataset is involved**, so the five data contracts do not apply here.

## Constraints / Non-negotiables

- **The domain core stays web-free.** `src/rpg_core/` is I/O-free and web-free per
  `CLAUDE.md`. FastAPI must not become an import dependency of it, in either
  direction that would couple them.
- **The repo is public.** No absolute paths, no machine identifiers, no ports or
  hostnames baked to one machine's setup in a way that leaks anything.
  `tests/test_no_leaks.py` is a blocking check.
- **Machine-specific values resolve from the environment**, with keys listed in
  `.env.example` and `.env` gitignored.
- **CI runs `uv sync --locked`.** Adding FastAPI means running `uv lock` and
  committing `uv.lock` in the same change, or the build fails outright.
- **`var/` is the only scratch root** and is gitignored — build caches, `node_modules`
  aside, belong there or in an already-ignored path. Nothing regenerable gets
  tracked.
- **`main` is protected**; this lands on a branch through a PR, committed only via
  `/commit`.
- **Python 3.12**, uv, ruff, mypy strict, pytest — the existing toolchain is not
  up for renegotiation as part of this item.

## Open Questions for Scoping

1. **Where does the API package live, and what is it called?** `src/rpg_api/`,
   `src/rpg_app/`, or inside `app/`? This binds `[tool.mypy] files`, the hatch wheel
   `packages` list, and CI's `--cov` target — all three are currently
   `rpg_core`-only. Cheap now, annoying later.
2. **How does FastAPI serve the built SPA, and what happens when the build is
   absent?** A fresh clone has no `app/dist/`. Mounting a missing directory can fail
   at import time; a clear error beats a stack trace, and this is the first thing a
   cold agent will trip on.
3. **Is there a single command that runs both halves in development**, or does the
   user run two? A one-command launcher is nicer and is one more thing to maintain
   on Windows *and* in CI. (*Assumed:* the user's daily environment is Windows and
   PowerShell — `research/tools/iff.ps1` is PowerShell — so a bash-only launcher
   would be useless. Worth confirming.)
4. **Does the health endpoint report anything beyond liveness?** Version is the
   obvious candidate and is already pinned by a structural test. Anything more
   (ruleset version, career count) is a lie until the things it reports exist.
5. **Which linter for TypeScript** — eslint (conventional, heavy config) or oxlint
   (fast, fewer plugins)? Low stakes, but it is a dependency the repo carries from
   here on.
6. **Does `ops/branch-protection.json` need the new job added as a required check**,
   and is that a manual GitHub step the user has to take? If so it should be called
   out loudly rather than assumed applied.
7. **Should the frontend test framework be deferred at all?** Intake put it out of
   scope on "no components to test" grounds. The counter-argument is that adding a
   test harness later, once there are untested components, is how frontends end up
   untested permanently. Scoping should decide on purpose rather than by default.
8. **Does a structural guard get written for the new layout** — e.g. asserting the
   API package does not import from a web framework into `rpg_core`, or that `app/`
   exists with a lockfile? Consistent with the repo's habits; possibly premature.
9. **Node version and package manager** (npm/pnpm), and whether the version is
   pinned somewhere CI and the local machine both read. *Unconfirmed:* whether the
   user has a Node toolchain installed at all.

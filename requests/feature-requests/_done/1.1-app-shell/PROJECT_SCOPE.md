> **Status:** implemented · created 2026-08-14 · decided · next: —

# Project Scope — App Shell (Phase 1, item 1.1)

> **Authoring rule, load-bearing.** Every path this item *creates* — `src/rpg_api/`,
> `app/`, `app/dist/`, `tests/conftest.py` — is written as inline code or inside a
> fenced block, **never as a markdown link**. `tests/test_request_links.py` scans
> every `.md` under `requests/` and asserts each relative link resolves on disk, so a
> single markdown link pointing at `app/` turns CI red on the very PR that lands this
> scope. Only paths verified present today are linked.
>
> This is not hypothetical. It fired twice during this stage: once on the panel trail
> file, where an adversary *quoting* a bad link wrote a real one, and once on this
> document, where the sentence you are reading originally demonstrated the trap by
> falling into it. Note also that the finding which predicted this got its own
> reasoning wrong — it claimed inline backticks make such a quote safe. They do not;
> only fenced blocks (3+ backticks, blockquoted is fine) are stripped. Carry the rule
> into the plan.

## Fit Verdict

**`clean`** — unanimous across all three scoper lanes, and verified rather than asserted.

Phase 0 reserved this item's conventions **by name** in five tracked files:
[`pyproject.toml`](../../../../pyproject.toml) lines 9–13 (`dependencies = []` with
"FastAPI arrives with Phase 1 item 1.1 (app-shell)"),
[`.github/dependabot.yml`](../../../../.github/dependabot.yml) line 30 ("npm arrives with
Phase 1 item 1.1"), [`.gitignore`](../../../../.gitignore) lines 66–68 (`node_modules/`,
`.vite/`, `app/dist/`), [`.gitattributes`](../../../../.gitattributes) line 41
(`package-lock.json linguist-generated`), and
[`.claude/settings.json`](../../../../.claude/settings.json) (allow entries for
`PowerShell(node *)` / `PowerShell(npm *)`).

The architecture it instantiates is stated, not invented:
[`DESIGN.md`](../../../../DESIGN.md) §3 — "Two packages, one repo. `src/rpg_core/` is the
I/O-free domain; the API and web app depend on it and it depends on neither" — echoed
from the other side by
[`src/rpg_core/__init__.py`](../../../../src/rpg_core/__init__.py) lines 3–11.

**Contract applicability, verified.** No dataset: `datasets/manifest.json` does not
exist (it is item 2.1), so the five data contracts are N/A. No ledger or economy:
`careers/` and `rulesets/` do not exist, so nothing here touches ADR 0003's append-only
history or ADR 0004's pinned rulesets. None of the nine ADRs is contradicted or engaged.

**One correction to the request, verified.** `FEATURE_REQUEST.md`'s Rough Ideas claims
"CLAUDE.md's project map lists serving under `app/`". **False** — grep for `app/` in
[`CLAUDE.md`](../../../../CLAUDE.md) returns no matches. The real evidence for the `app/`
convention is `.gitignore` line 68 and `.gitattributes` line 41, which is still strong
enough to honor rather than re-litigate. A plan must not inherit the false reasoning.

**One honest friction, recorded not resolved.** [`ROADMAP.md`](../../../../ROADMAP.md)
sizes 1.1 as `M` and does **not** mark it ★ — its legend says unmarked items should skip
straight to a plan or straight to work. The full panel ran anyway. The user has
explicitly disposed the resulting size question (Decision 7): there is no budget, and
the item takes as long as it needs.

## Problem

There is no application. Phase 0 built the workbench and deliberately stopped: the
dependency list is empty with a comment reserving FastAPI for this exact item, and
`src/rpg_core/__init__.py` contains a docstring and a version string.

Every remaining Phase 1 item — career ledger, player model, creation, box-score entry,
spend-and-worksheet, career switching, correction UI — is a *surface*, and none can be
built, run, or judged without something to attach to. **Eleven roadmap rows are blocked
on the same missing seam.**

Separately, the frontend is unproven ground in a repo that is otherwise tightly guarded.
Python has ruff, mypy strict, pytest, and a green required CI job; a JavaScript build has
none of that and CI does not know it exists. Introducing the SPA without extending the
same posture would leave half the codebase unchecked from its first commit.

## Goals / Non-Goals

**Goals**

1. **Establish the HTTP seam** — a FastAPI application in `src/rpg_api/` exposing
   `GET /api/health`, so items 1.2–1.11 attach endpoints without re-deciding layout.
2. **Establish the browser seam** — one React + TypeScript page under `app/` that
   fetches the health endpoint across a real network boundary and renders it, proving the
   request crossed the seam rather than being mocked in the frontend.
3. **Prove and mechanically protect the dependency direction** `DESIGN.md` §3 asserts:
   `rpg_api` imports `rpg_core` (the health payload's version comes from
   `rpg_core.__version__`), and `rpg_core` imports no web framework — enforced by a guard
   test, not by convention.
4. **Give "run the app" two honest answers** — a hot-reload development mode (Vite dev
   server proxying `/api` to uvicorn, so no CORS middleware exists anywhere) and a
   single-process mode where uvicorn serves the built SPA out of `app/dist`.
5. **Extend the repo's check posture to the new half** — TypeScript strict mirroring
   mypy strict, a linter mirroring `ruff check`, a separate CI job so a red frontend is
   legible on its own, and — the part that is easy to skip — make that job an *actually
   required* check rather than an advisory one.
6. **Land the dependency bookkeeping correctly in one commit** — fastapi + uvicorn in
   `pyproject.toml` with `uv.lock` regenerated, `src/rpg_api` in the hatch wheel
   `packages` list, `--cov` extended past `rpg_core`, a committed `app/package-lock.json`,
   and the npm ecosystem entry `dependabot.yml` line 30 is holding a slot for.
7. **Stop the docs lying** — `ops/README.md` gains the Node toolchain and both run modes;
   `README.md`'s "No application code yet" banner, project map, and Setup block, and
   `CLAUDE.md`'s project map and its "the web app doesn't exist yet" line, all stop being
   false. **This goal carries its own acceptance criterion** (AC 17) rather than being
   delegated to `/commit`'s judgment gate.
8. **Leave a cold agent picking up item 1.2 with no structural questions open** — package
   name, route prefix, dev/serve split, and frontend toolchain are all decided here.

**Non-Goals**

- **Any domain logic.** No player model, event schema, fold, ledger, economy, `rulesets/`
  directory, or `BoxScore` DTO. `src/rpg_core/` still holds a docstring and `__version__`
  when this lands. *The single strongest failure mode for this item is deciding the status
  page would be more convincing with a career in it.*
- **Persistence of any kind.** No SQLite, no read-model, no `careers/`, no migrations.
  Nothing here creates a file under `var/` or `careers/`.
- **Any career-facing surface** — no career list, creation form, box-score entry, spend
  flow, or worksheet. The status page is the entire UI.
- **The dataset layer.** `datasets/manifest.json` and `lib/paths.py` are item 2.1.
- **Auth, users, sessions, HTTPS, multi-user, hosting, or CORS for non-local origins.**
  The Vite proxy makes dev same-origin and the built mode is same-origin by construction;
  permissive CORS "just in case" would be a posture eleven items inherit for nothing.
- **Visual design.** No component library, theme system, CSS framework, or design tokens.
  Legibility only.
- **A shared type contract between API DTOs and the frontend** — OpenAPI codegen, a
  generated client, or hand-mirrored DTO types. Valuable once `BoxScore` exists at item
  1.8 ([ADR 0002](../../../../docs/decisions/0002-manual-ingestion-dto-boundary.md)); today
  it would generate types for a two-field payload. *(A hand-written `Health` interface in
  a small typed fetch wrapper is NOT this — it is the seam codegen later slots into.)*
- **Client-side routing and app chrome.** One page; structuring an app before it has
  surfaces pre-decides the structure blind.
- **Global state management** (Redux, Zustand, TanStack Query).
- **Packaging and distribution** — no Docker, installer, PyInstaller, deployment target,
  process supervisor, or worker model. It runs from a checkout.
- **End-to-end browser automation** (Playwright/Cypress).
- **Path-filtered CI jobs** (`paths-ignore`). With `required_status_checks.strict: true`
  and named contexts, a filtered job that never reports makes PRs wait forever — the exact
  silent-hang failure `ops/README.md`'s rename warning describes.
- **Telemetry, analytics, error reporting, or any outbound network call** from either half.
- **Changing the Python toolchain.** In particular mypy strict is **not** relaxed — no
  blanket per-module override carving `rpg_api` out of strict on its first day.
- **The existing `.claude/skills/` JavaScript.** Thousands of lines of `.js`/`.mjs` already
  live there, unlinted and unchecked, and several skills document `node <guard>.mjs` as a
  manual check. Those guards do **not** join CI in this item. **Consequence for the
  implementation:** the eslint config and `tsconfig.json` live *inside* `app/` with file
  scope limited to `app/`, **never** a repo-root config — a root config would immediately
  start reporting on `.claude/skills/**/*.js` and force an ignore list nobody scoped.
- **Committing or merging.** This lands on a branch through a PR via `/commit`; the merge
  and the `gh api -X PUT` re-apply of branch protection stay the user's.

## Acceptance Criteria

Testable per [`requests/feature-requests/README.md`](../../README.md): a cold agent runs one
command and gets a pass or fail. Criteria only a human can prove are marked **USER-RUN**
so the acceptance panel does not claim them. Every criterion below describes the single
agreed deliverable — there is no tier-dependent hedging, because Decision 7 lands the
full scope.

1. `uv sync --locked` exits 0 from a clean checkout, with `fastapi` and `uvicorn` in
   `[project].dependencies` and resolved in the tracked `uv.lock`. This is verbatim what
   [`ci.yml`](../../../../.github/workflows/ci.yml) line 34 runs, and it hard-fails on a
   stale lock.
2. `uv run pytest -m "not network"` is green, including a test using
   `fastapi.testclient.TestClient` to `GET /api/health` asserting status 200, content-type
   `application/json`, `body["status"] == "ok"`, `body["version"] == rpg_core.__version__`,
   and a boolean `body["spa_built"]`. No live server, no socket.
   ([`tests/test_repo_structure.py`](../../../../tests/test_repo_structure.py) lines 46–54
   already pins `rpg_core.__version__` to `pyproject.toml`, so the payload inherits it.)
3. **Layering guard, self-testing — no source mutation.** The guard is a pure function
   taking a directory root and returning violations. It is unit-tested twice against
   `tmp_path`: a fake module containing `import fastapi` reports exactly that file, and a
   clean tree reports none. The real assertion points at `src/rpg_core/` and expects zero.
   One `uv run pytest` proves red-and-green without editing tracked source.
   (`pydantic` is deliberately **not** in the deny-list — see Decisions.)
4. **CI-jobs guard, set equality.** The test parses
   [`.github/workflows/ci.yml`](../../../../.github/workflows/ci.yml) with `yaml.safe_load`,
   collects `jobs.*.name`, and asserts that set **equals**
   `required_status_checks.contexts` in
   [`ops/branch-protection.json`](../../../../ops/branch-protection.json). Equality, not
   containment: containment passes while a typo'd context name ("Web app" vs "Web App")
   makes every PR hang forever on a check that never reports — the failure
   [`ops/README.md`](../../../../ops/README.md) actually warns about. The failure message
   names which side carries the extra entry. A negative assertion proves the parser is
   structure-aware: a *step*-level name (e.g. "Gitleaks", "Install") does not enter the
   set. **This requires `pyyaml` and `types-PyYAML` in the dev group** (mypy strict needs
   the stubs) with `uv.lock` regenerated — an explicit core deliverable, not an
   undeclared test dependency.
5. **Missing-build branch**, no listener required: with the SPA dist location pointed at a
   `tmp_path` that does not exist, constructing the application raises no exception,
   `GET /api/health` returns 200, and `GET /` returns 503 whose body contains the literal
   build command. *(This forces the dist path to be an injectable factory argument; a
   module-level constant makes this criterion untestable — and a fresh clone has no
   `app/dist/`, so this is the branch every cold agent hits first.)*
6. **Present-build branch**: with the dist location pointed at a `tmp_path` containing a
   known `index.html`, `GET /` returns 200, `text/html`, and that file's bytes.
7. `GET` on an unknown path under `/api` returns 404 with content-type `application/json`,
   not HTML — the guard that stops the SPA history fallback swallowing API 404s.
8. `uv run mypy` exits 0 with `src/rpg_api` present, under the **unchanged**
   `[tool.mypy]` block (strict, `warn_unreachable`, `files = ["src", "tests"]`), with zero
   new `# type: ignore` comments and zero new per-module overrides. *A green run achieved
   by loosening strict fails this criterion.*
9. `uv run ruff check` and `uv run ruff format --check` exit 0 over `src/rpg_api` and every
   new test file.
10. From `app/`: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run build` each exit 0,
    and `app/dist/index.html` exists afterwards. These are exactly the steps the new CI job
    runs, so a green local run predicts a green CI run.
11. **tsconfig strictness, proven without mutation.** A committed, deliberately ill-typed
    fixture excluded from `npm run build` is checked by a dedicated
    `npm run typecheck:negative` asserted to exit non-zero — proving `strict` is actually
    engaged rather than a default-generated config that checks nothing.
12. `npm run test` is green with exactly two Vitest tests: the status page renders the
    fetched version, and the unreachable panel renders on a rejected fetch.
13. `uv run pytest tests/test_no_leaks.py` is green with `app/package.json`,
    `app/package-lock.json`, `app/tsconfig.json`, and `app/vite.config.ts` tracked. A real
    gate: `.json`, `.ts`, `.tsx`, `.js`, `.mjs`, `.css`, `.html` are all in `TEXT_SUFFIXES`
    ([`tests/test_no_leaks.py`](../../../../tests/test_no_leaks.py) lines 38–55), and the
    file's docstring claim that lockfiles are skipped is **true** of `uv.lock` and **false**
    of `package-lock.json`. If a pattern trips, the fix is a narrowly-justified `ALLOWED`
    entry with a written reason — **never** a weakened regex or a removed suffix.
14. A structural test asserts `[tool.hatch.build.targets.wheel].packages` contains
    `src/rpg_api` and that `ci.yml`'s pytest step passes a `--cov` flag naming `rpg_api`.
    *Without this, an omitted `packages` entry passes every test locally —
    `pythonpath = ["src"]` puts the package on the path regardless — then fails with
    `ModuleNotFoundError` on an installed environment. The test suite structurally cannot
    otherwise see it.*
15. `.github/dependabot.yml` contains an entry with `package-ecosystem: "npm"` pointing at
    the SPA directory, carrying the same monthly / patch-ignore posture as the uv entry,
    and the line-30 placeholder comment is gone.
16. `uv run pytest tests/test_repo_structure.py tests/test_request_links.py` is green — the
    existing structural guards survive the new directories.
17. **Documentation, mechanically checked.** A structural test asserts: `README.md` no
    longer contains "No application code yet"; `CLAUDE.md`'s project map contains both
    `app/` and `src/rpg_api/` and no longer states the web app doesn't exist; `ops/README.md`
    contains a Node-toolchain heading and both run-mode commands. *This is the idiom
    `tests/test_repo_structure.py` already uses for "the repo and its documents agree", and
    it exists because Goal 7 otherwise has no pass/fail check at all.*
18. **Real-server CI smoke.** A CI step builds the SPA, boots uvicorn against the built
    `dist`, and curls both `/` (200, HTML) and `/api/health` (200, JSON) — green in CI.
    This is the only check that exercises uvicorn, the static mount against a real
    filesystem, and the built artifact; `TestClient` exercises none of them.
19. `uv run <console-script>` serves the built app — the `[project.scripts]` entrypoint
    resolves and starts the served-build mode.
20. **USER-RUN — the dev seam.** Two commands in two terminals (uvicorn with reload; `npm
    run dev` in `app/`). The Vite URL renders the version string, and the browser network
    tab shows `/api/health` served on the **Vite origin**, not a cross-origin call to the
    API port — which is what actually proves the proxy, and therefore the
    no-CORS-middleware decision.
21. **USER-RUN — the built seam.** `npm run build`, then uvicorn alone: the same page
    renders at the uvicorn origin with no Vite dev server running.
22. **USER-RUN — the failure state.** With the page open, stopping the backend makes the
    page render a legible "backend unreachable" panel naming the start command, rather than
    a blank screen or an uncaught console error.
23. **USER-RUN — required-check activation, as an ordered gate *before* merge.**
    (1) Push the branch and let the new job report once, confirming the context name
    verbatim; (2) run `gh api -X PUT repos/<owner>/nba2k-rpg/branches/main/protection
    --input ops/branch-protection.json`; (3) confirm the new check shows as **Required** on
    the open PR; (4) then merge. Put these steps in the PR description.
    *Sequencing matters: re-applying after merge guarantees that the PR introducing the job
    is exactly the one that can land with a red frontend. An agent cannot do step 2 —
    `gh api *` is in `.claude/settings.json`'s `ask` list — and editing the JSON alone never
    changes GitHub.* **Verify beforehand** that the owner/repo in `ops/README.md` still
    matches `git remote -v`.

## Scope (tiered)

Decision 7 removed the budget: **core and every cheap fold land**. The tiering below is
kept as the panel produced it, because it still records *why* each piece is here.

**Core (must)**

- `src/rpg_api/` — a second source package alongside `src/rpg_core/`, per `DESIGN.md` §3,
  holding the FastAPI application and its health route and nothing else. Under `src/`
  specifically, because `[tool.mypy] files = ["src", "tests"]` and
  `[tool.pytest.ini_options] pythonpath = ["src"]` both already reach there — zero config
  churn on those two.
- `GET /api/health` returning `{"status": "ok", "version": rpg_core.__version__,
  "spa_built": <bool>}`. Version read from the attribute, not re-typed, so the existing
  version pin transitively covers the payload — and so the app has one honest reason to
  import the domain core, proving the `rpg_api → rpg_core` direction from day one. All API
  routes live under `/api` so the serving boundary is unambiguous.
- `pyproject.toml` dependency work, one commit: fastapi + uvicorn into
  `[project].dependencies` (replacing the empty list and the reservation comment); httpx,
  pyyaml, and types-PyYAML into the dev group; `watchfiles` in the dev group rather than
  `uvicorn[standard]`; `src/rpg_api` appended to `[tool.hatch.build.targets.wheel].packages`;
  a `[project.scripts]` console entrypoint for the served-build mode; `uv lock` re-run and
  `uv.lock` committed alongside.
- `ci.yml`: a third job, parallel with `python` and `secrets`, running setup-node against a
  pinned major with npm caching, then `npm ci` / typecheck / lint / test / build with
  working-directory `app`; plus the real-server smoke step (Decision 8); plus one line
  changed in the existing job — `--cov=rpg_core` gains `rpg_api`.
- `ops/branch-protection.json`: the new job's display name appended to
  `required_status_checks.contexts`, in the **same commit** as the workflow change, plus a
  loud call-out in the PR description and `ops/README.md` that the file is inert until
  re-applied with `gh api -X PUT`.
- `app/` — Vite + React + TypeScript SPA at the repo root (the location `.gitignore` and
  `.gitattributes` already anticipate), `tsconfig` with `strict: true`, eslint, npm with a
  committed `package-lock.json`. One page: it calls `/api/health` and renders status and
  version. That page is the entire UI.
- A Vite dev-server proxy mapping `/api` to the backend on the **IPv4 literal
  127.0.0.1** (not `localhost`). This is the whole CORS story; no CORS middleware is added
  in either mode.
- Serving the built SPA from FastAPI with the dist location **injectable** (a factory
  argument), so both branches are unit-testable against `tmp_path` with no listening
  socket: present → `index.html` at `/`; absent → 503 naming the build command, never an
  import-time traceback.
- **Guard test:** no file under `src/rpg_core/` imports `fastapi`, `starlette`, `uvicorn`,
  or the API package. The one convention this item leaves behind that actually protects the
  next eleven items. Its failure message cites `DESIGN.md` §3 by name.
- **Guard test:** CI job display names ≡ `ops/branch-protection.json` contexts.
  `ops/README.md` guards this in prose; prose does not fail a build.
- `.github/dependabot.yml`: the npm ecosystem entry line 30 reserves, matching the uv
  entry's monthly + patch-ignore posture.
- **Documentation:** `ops/README.md` gains a Node-toolchain section beside the uv one and
  both run modes; `README.md`'s banner, project map, and Setup block are corrected;
  `CLAUDE.md`'s project map gains `app/` and `src/rpg_api/` and its "web app doesn't exist
  yet" line stops being true. `CLAUDE.md` has a hard line budget — this is an edit, not an
  append.
- `ROADMAP.md` row 1.1 advanced by `/commit` against the diff, not hand-edited.

**Folded in (all of them — Decision 7)**

- SPA history fallback for unmatched non-`/api` paths, paired with the AC 7 JSON-404 guard.
  It is what stops item 1.10's router from being a breaking change.
- A legible backend-unreachable state naming the start command. Not polish: "I opened the
  page and it's blank" is the top cold-start confusion in a two-process app.
- A reusable `TestClient` fixture in `tests/conftest.py`, parameterized on the injectable
  dist location. Items 1.7–1.11 each need it; writing it once beats five agents inventing
  five variants.
- A small typed fetch wrapper (`app/src/api/client.ts`) with a hand-written `Health`
  interface — one place the frontend talks to the backend. Explicitly **not** the deferred
  codegen contract; it is the seam codegen would later slot into.
- TypeScript strictness beyond `strict: true` — `noUncheckedIndexedAccess`,
  `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch` — bringing the two
  halves to comparable severity with mypy strict + `warn_unreachable`. Free now, painful to
  retrofit.
- Node major pinned in the workflow plus one line in `ops/README.md`, rather than a
  `.nvmrc`/`engines` file. *Measured on this machine: node v24.15.0, npm 11.12.1.* A version
  file pins CI while the Windows developer silently drifts — a false sense of enforcement
  for one more tracked file.
- npm dependency caching on setup-node, mirroring the existing setup-uv caching. Matters
  because `concurrency: cancel-in-progress` means the job re-runs on every push.
- Guard test that `app/dist/` and `node_modules/` are gitignored, mirroring
  `test_scratch_root_is_gitignored` (which uses `git check-ignore --no-index` and therefore
  works on paths that do not exist yet). Asserts nobody later adds an `!app/**` carve-out.
- Correct the now-inaccurate docstring at `tests/test_no_leaks.py` line 37 ("Binary and
  lockfiles are skipped") — true of `uv.lock`, false of `package-lock.json`. This item is
  what makes the statement wrong, so this item fixes it.
- A real page title and favicon instead of the Vite template defaults. Identity, not design.
- An `.editorconfig`. Two toolchains, one Windows author, and a repo that forces `eol=lf`
  for everything except `.ps1`.

**Gated — resolved.** All nine disposed; see **Decisions**.

## Above & Beyond

Twenty-eight proposals were generated. With the budget removed, everything the panel
tiered as `core` or `cheap_fold` is in the build above. The rest:

| Proposal | Tier | Disposition |
|---|---|---|
| Import-layering guard test | core | **In** — promoted from enhancement; the only permanent artifact this content-free item leaves behind |
| CI-jobs ≡ contexts guard test | core | **In** — with set-equality and YAML parsing per adversary findings |
| Vitest + Testing Library, two tests | gated | **In** (Decision 1) |
| `spa_built` in the health payload | gated | **In** (Decision 6) |
| Real-server CI smoke step | gated | **In** (Decision 8) |
| Console-script entrypoint | gated | **In** (Decision 9) |
| eslint + typescript-eslint + react-hooks | gated | **In** (Decision 2) |
| One-command dev launcher | gated | **Out** (Decision 4) |
| Environment-resolved settings | gated | **Out** (Decision 5) |
| ADR 0010 | gated | **Out** (Decision 3) |
| `ops/check.ps1` CI-parity command | gated | **Out** (Decision 10) |
| Frontend formatter gate (prettier) | gated | **Out** — panel recommendation, not separately disposed; see Decisions |
| OpenAPI snapshot test | drop | **Out** — asserts nothing the health test doesn't; right moment is 1.8. Record the pointer in 1.8's request |
| OpenAPI→TypeScript codegen | drop | **Out** — machinery for one two-field object; the typed fetch wrapper is the seam it slots into at 1.8 |
| Request-id / structured logging middleware | drop | **Out** — single-user localhost; uvicorn's access log already answers "did the request arrive" |
| Playwright E2E of the served build | drop | **Out** — a second test toolchain and browser downloads for one page |
| Three-way version parity test | drop | **Out** — `app/package.json`'s version is meaningless for a private SPA. Mark it private, fix the version at a placeholder |

## Risks & Unknowns

1. **HEADLINE — silent-green merges.** `ops/branch-protection.json` lists contexts by CI
   job **display name**, and the file is inert until re-applied with `gh api -X PUT`.
   Symptom: a PR merges with a red frontend job and nothing complains, indefinitely.
   Mitigation is split — the guard test (AC 4) covers the tracked half; the ordered
   user-run gate (AC 23) covers the applied half. **UNCONFIRMED, check before planning:**
   whether GitHub's protection API accepts the current JSON unchanged (not re-applied since
   Phase 0), and whether the owner/repo in `ops/README.md` still matches the remote.
   *(The panel verified the remote is `jordan-koch/nba2k-rpg`, matching `ops/README.md`.)*
2. **Omitting `src/rpg_api` from the hatch `packages` list fails only at runtime.**
   `pythonpath = ["src"]` puts the package on the path for tests regardless — every test
   passes, CI goes green, and `uv run uvicorn rpg_api...` fails with `ModuleNotFoundError`
   on the user's machine. The sneakiest failure in the item. Hence AC 14.
3. **Stale lockfiles, twice.** `uv sync --locked` hard-fails rather than re-resolving;
   `npm ci` fails when `package.json` and `package-lock.json` disagree. `ops/README.md`
   documents the uv rule sharply; the Node rule needs the same sharpness.
4. **`tests/test_no_leaks.py` now scans frontend files**, and it is a blocking public-repo
   guard. Two concrete tripwires: a `package.json` carrying an `author` email fails the
   email check, and any Windows-generated config writing an absolute path fails the
   drive-letter check. *Inferred, not measured:* npm lockfileVersion 3 entries carry
   registry URLs and integrity hashes rather than local paths, so it will probably pass —
   but **run it before committing the lock**.
5. **gitleaks — the other required check — is unassessed.** The `secrets` job runs
   gitleaks over full history (`fetch-depth: 0`) and blocks merge, and the repo has **no**
   `.gitleaks.toml` or `.gitleaksignore`. This item adds a `package-lock.json` full of
   high-entropy base64 sha512 integrity strings to that scan. *Judged lower-probability
   than the panel implied — integrity hashes do not usually match credential rules, and the
   finding was medium-confidence — but it is cheap to check and expensive to discover at PR
   time.* Run gitleaks locally once before pushing; if it trips, remediate with specific
   fingerprints in `.gitleaksignore` or a scoped path allowlist, each with a written reason,
   mirroring the `ALLOWED`-entry discipline.
6. **mypy strict over FastAPI.** `disallow_untyped_decorators` against route decorators is
   the classic friction point. FastAPI ships `py.typed`, so annotated handlers should pass;
   unconfirmed until run. **The failure mode to refuse is a per-module override quietly
   carving `rpg_api` out of strict on its first day** — the exact asymmetry this item exists
   to prevent on the frontend side. Pinned by AC 8.
7. **Mounting a missing `app/dist/`.** *Inferred:* Starlette's `StaticFiles` raises at
   construction when the directory is absent, so a fresh clone gets an import-time traceback
   instead of an app. Why the dist path must be injectable (AC 5).
8. **Windows/Linux parity in npm scripts.** Daily shell is PowerShell; CI is
   ubuntu-latest. Any `package.json` script using `&&`, `rm -rf`, `cp`, or POSIX inline
   env-var prefixes works in CI and **fails locally** — Windows PowerShell 5.1 has no `&&`
   at all. Keep every script to a single command invocation with no shell operators.
9. **Windows/Node IPv6 resolution.** A Vite proxy targeting `http://localhost:PORT` can
   resolve to `::1` on Windows while uvicorn binds `127.0.0.1`, producing an
   `ECONNREFUSED` that looks exactly like the backend being down while it runs fine. Pin the
   proxy target to the IPv4 literal.
10. **Node toolchain drift.** Local is node v24.15.0 / npm 11.12.1 (measured); CI pins a
    major. A lockfileVersion difference between npm majors yields a lockfile that installs
    locally and fails `npm ci` in CI, with an error pointing at a package rather than at the
    version skew.
11. **Coverage silently stops meaning anything.** Left unchanged, `--cov=rpg_core` simply
    omits `rpg_api` — not a failure (no `fail-under` configured), just a number that quietly
    stops describing the codebase.
12. **Scope leakage into item 1.2.** The status page is boring by design, and the pull to
    make it show something — a career list, a stub player, a fake XP number — is the most
    likely way this item stops being a shell.
13. **npm supply chain in a public repo.** `npm ci` for a Vite/React toolchain runs install
    scripts (esbuild fetches a platform binary) and pulls a transitive tree orders of
    magnitude larger than the four-package Python dev group. Mitigations are the committed
    lockfile and the dependabot entry; no version of this item avoids the exposure, and the
    honest position is to note it rather than claim it is handled.
14. **The CI smoke step is a flake vector** (Decision 8, taken against the panel's
    recommendation). It needs Python and Node in one job or an artifact handoff between two,
    plus readiness-wait handling. Plan it with an explicit readiness poll and a bounded
    timeout, not a fixed sleep.
15. **Out of scope but worth recording before item 2.1:** `.gitignore` line 63 has a blanket
    `build/` rule matching a directory named `build` at **any** depth, which will silently
    shadow the `build/build-*.py` builder pattern `CLAUDE.md` says Phase 2 should follow.
    Not this item's problem; better found now.

## Affected Area & Pointers

**Target components:** a new source package `src/rpg_api/` (FastAPI app + health route,
imports `rpg_core`, imported by nothing in `rpg_core`), a new top-level `app/` (Vite +
React + TypeScript SPA, one page), and additions to `tests/` (three guard tests + the API
tests + `conftest.py`). No dataset, no manifest name.

Read first, in order:

- [`FEATURE_REQUEST.md`](FEATURE_REQUEST.md) — the intake and its nine Open Questions. This
  scope settles 1, 2, 4, 6, 8 and all gated ones; **9 is resolved** (node v24.15.0 / npm
  11.12.1 measured on this machine). Note its `CLAUDE.md`/`app/` claim is verified false.
- [`requests/feature-requests/README.md`](../../README.md) — the pipeline contract, the status
  blockquote grammar, the Index row, the definition of *testable*, and the user-run rule.
- [`pyproject.toml`](../../../../pyproject.toml) — line 9 empty `dependencies` and 11–13 the
  reservation comment; line 31 the hatch `packages` list; 61–65 `[tool.mypy]`; line 49 the
  DTZ rule; line 73 `pythonpath`; 15–21 the dev group.
- [`.github/workflows/ci.yml`](../../../../.github/workflows/ci.yml) — job display names at
  lines 19 and 50; setup-uv caching 24–28; `uv sync --locked` 34; ruff/mypy 36–43;
  `--cov=rpg_core` 47; `concurrency: cancel-in-progress` 9–12.
- [`ops/branch-protection.json`](../../../../ops/branch-protection.json) — line 4, the exact
  contexts array a third job must join.
- [`ops/README.md`](../../../../ops/README.md) — the `gh api -X PUT` apply and read-back
  commands, the job-rename warning this item generalizes to job *addition*, the uv section
  the Node section sits beside, and the "same four commands CI runs" block.
- [`tests/test_repo_structure.py`](../../../../tests/test_repo_structure.py) — the guard idiom
  to copy: `_git_check_ignore` (24–34), `test_package_version_matches_pyproject` (46–54)
  which pins the health payload transitively, `test_scratch_root_is_gitignored` (83–92) as
  the template, and the ADR index/contiguity tests (113–133).
- [`tests/test_no_leaks.py`](../../../../tests/test_no_leaks.py) — `TEXT_SUFFIXES` (38–55) now
  covering the frontend, `ALLOWED` (32–35) as the only sanctioned escape hatch, and the
  docstring at line 37 this item makes false.
- [`tests/test_request_links.py`](../../../../tests/test_request_links.py) — read the
  Authoring rule at the top of this document against lines 40–64 before writing the plan.
- [`src/rpg_core/__init__.py`](../../../../src/rpg_core/__init__.py) — the whole domain core
  today, and the docstring stating the dependency direction.
- [`DESIGN.md`](../../../../DESIGN.md) §3 — the "Two packages, one repo" note this instantiates.
- [`.gitignore`](../../../../.gitignore) — 66–68 (the Node block), 51–63 (Python, including the
  blanket `build/` at 63), 35–49 (the careers carve-out and its warning).
- [`.gitattributes`](../../../../.gitattributes) — line 3 (`* text=auto eol=lf`), the `*.ps1`
  CRLF exception, the `*.ts`/`*.tsx`/`*.css`/`*.html` entries, `*.ico binary`, and the
  `package-lock.json linguist-generated` line.
- [`.github/dependabot.yml`](../../../../.github/dependabot.yml) — the uv entry (16–28) whose
  posture the npm entry mirrors, and the line-30 placeholder this discharges.
- [`.claude/settings.json`](../../../../.claude/settings.json) — the `ask` list (git
  commit/push/merge, `gh api *`) determining what stays a user action, and the allow entries
  already covering `node *` / `npm *`.
- [`ROADMAP.md`](../../../../ROADMAP.md) — Phase 1 row 1.1 and the eleven rows downstream.
- [`CLAUDE.md`](../../../../CLAUDE.md) and [`README.md`](../../../../README.md) — both project
  maps and both "doesn't exist yet" sentences: the doc-drift surface AC 17 checks.
- [ADR 0002](../../../../docs/decisions/0002-manual-ingestion-dto-boundary.md) — read before
  writing the layering deny-list: it requires the DTO be constructible in tests "with no
  HTTP and no UI", which is why `pydantic` is deliberately **absent** from the deny-list
  (that is item 1.2's call, not this one's).

## Decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | **Vitest + Testing Library land now**, minimally — one dev dependency, one config block, one CI step, exactly two tests | The request's Open Question 7 asked scoping to decide on purpose, and the lanes split three ways. Repo precedent decides it: item 0.2 shipped the Python toolchain **and** the first structural test together. The backend-unreachable state is real branching logic and earns a test |
| 2 | **eslint + typescript-eslint + eslint-plugin-react-hooks** — *against* the panel's oxlint recommendation | The panel picked oxlint mainly on config-maintenance cost; Decision 7 removed cost as a constraint. `eslint-plugin-react-hooks` catches rules-of-hooks violations that are real runtime bugs, and that value grows sharply at items 1.7–1.11. Config lives **inside `app/`**, scoped to `app/` |
| 3 | **No ADR 0010** | `DESIGN.md` §3 already records the two-package split; the roadmap did not mark 1.1 ★; the existing nine ADRs govern game-design and data calls that were expensive to reverse. A guard test is a stronger record than prose because it fails a build — its message cites `DESIGN.md` §3 by name |
| 4 | **Two documented commands in two terminals**, no launcher | A supervisor spawning uvicorn + Vite with signal forwarding is real code with a known Windows failure: Ctrl+C in PowerShell against a Node process-runner can orphan the Python child holding the port, so the next run dies `EADDRINUSE`. Also untestable in CI |
| 5 | **No env keys** — no `RPG_API_PORT` / `RPG_SPA_DIST` in `.env.example`. **Recorded as a divergence:** `FEATURE_REQUEST.md` files env-resolved config under *Non-negotiables* | The constraint targets *machine-specific values*; a documented loopback default is not one — the three keys in `.env.example` today (`NBA2K26_INSTALL`, `NBA_ANALYSIS_PATH`, `POKEMON_LAB_PATH`) are all real machine paths. Testability is met by the injectable factory argument, and an `RPG_API_PORT` key adds a second place for the Vite proxy target to drift |
| 6 | **`spa_built` added to the health payload**; nothing else | It answers "which of the two modes am I in", the one question a cold agent actually has. `started_at`/`uptime`/python-version have no consumer and carry a DTZ lint tax; ruleset version and career count would be *lies* until items 1.4 and 1.2 land. **Rule for later items: the payload gains a field only when the thing it reports exists.** *(Panel recommendation — not separately disposed by the user; say so if you want it dropped.)* |
| 7 | **No budget.** The full core plus every cheap fold lands; the work takes as long as it needs | The user's explicit call, overriding the panel's "make the tiering a budget" and the adversary's M-vs-L complaint. **Consequence:** `ROADMAP.md` sizes 1.1 as `M` (a day or so) and that is now advisory rather than descriptive — flagged, not changed, since `/commit` maintains status and not size |
| 8 | **Real-server CI smoke step is IN** — *against* the panel's recommendation | The panel's objection was cost and flake risk; Decision 7 removed the cost half. `TestClient` never exercises uvicorn, the static mount against a real filesystem, or the built artifact — a real gap. Flake risk is now risk 14, to be planned with a bounded readiness poll |
| 9 | **Console-script entrypoint (`[project.scripts]`) is IN** | Matches the repo's documented `uv run ruff` / `uv run mypy` / `uv run pytest` idiom and requires nothing core isn't already doing. **Caveat to honor:** only one canonical way to run the served build gets documented — the console script, not a raw uvicorn incantation |
| 10 | **No `ops/check.ps1`** | `ops/README.md` stays the single place the command list lives. A parity script becomes a second copy that goes stale exactly like `ops/branch-protection.json` does |
| — | **No frontend formatter gate** (prettier or equivalent) | Panel recommendation, bundled inside the linter question and **not separately disposed**. Enforcing format on one component file is a dependency and a CI step bought for nothing. Flagged here so it is a visible default rather than a silent one |

**Adversary findings applied to this scope** (all raised by both adversaries independently,
except where noted): the artifact authoring rule (blocker — it fired during this stage);
ACs 3 and 11 restructured so no tracked source is mutated; AC 4 given set-equality
semantics, a named YAML parser, its declared dev dependencies, and a negative
step-name assertion; AC 17 added so Goal 7 is no longer delegated to a judgment gate;
AC 7's "if folded in" hedge removed; AC 23 resequenced *before* merge; the
`.claude/skills/` JS non-goal and the app-scoped-config constraint added. The gitleaks
finding is recorded as risk 5 with its confidence stated rather than treated as
established.

## Panel Trail

Raw, unfiltered panel output: [`reviews/scope-proposals.md`](reviews/scope-proposals.md)
(the three scopers' proposals) and
[`reviews/scope-adversarial.md`](reviews/scope-adversarial.md) (44 adversary findings, the
two adversary summaries, and the convergence map). Panel health: 3/3 scopers, 2/2
adversaries, no degraded lenses.

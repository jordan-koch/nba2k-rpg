> **Status:** planned · created 2026-08-14 · decided · next: implement

<!-- Status token is `planned`, per the grammar at requests/feature-requests/README.md:100
     (intake → scoped → planned → implemented). The create-implementation-plan SKILL.md
     template says `plan`; the repo's own contract wins, and /update-docs checks Index rows
     against these headers. -->

# Implementation Plan — App Shell (Phase 1, item 1.1)

> **One-line goal:** a running application skeleton with nothing in it — a FastAPI seam, a
> one-page SPA that crosses it, two honest run modes, and a check posture on the frontend that
> matches the Python half. · **Target component:** a new `src/rpg_api/` package, a new top-level
> `app/`, six new test modules, and the CI/branch-protection pair.

> **AUTHORING RAIL — read before writing any `.md` under `requests/`.** Every path this item
> *creates* — `src/rpg_api/`, `app/`, `app/dist/`, `tests/conftest.py` — is written as inline code
> or inside a fenced block, **never as a markdown link**. `tests/test_request_links.py` strips only
> 3+ backtick/tilde fences; inline backticks are **not** exempt. This trap fired three times across
> stages 2 and 3, including once inside the sentence warning about it. Also: **no absolute paths**
> anywhere — `tests/test_no_leaks.py` fails the build on a drive-letter path, and the panel's own
> output had to be rewritten repo-relative before the trail could be tracked.

---

## 1. Onboarding — read these first

There is no application yet. Phase 0 built the workbench and deliberately stopped:
`pyproject.toml` line 9 is `dependencies = []` with a comment at 11–13 reserving FastAPI for this
exact item, and `src/rpg_core/__init__.py` is a docstring plus `__version__ = "0.1.0"` — 16 lines
total. The **ten downstream Phase 1 rows, 1.2 through 1.11** (`ROADMAP.md:166-175`), are surfaces
blocked on the same missing seam.

This item builds that seam and **adds zero domain logic**. No player model, no event schema, no
ledger, no economy, no persistence. `src/rpg_core/__init__.py` must be **byte-identical** when this
lands — `git diff src/rpg_core/` being empty is the cheapest proof the non-goal held. The scope
names *"deciding the status page would be more convincing with a career in it"* as the single
strongest failure mode here.

| Read | Why |
|---|---|
| [`PROJECT_SCOPE.md`](PROJECT_SCOPE.md) | **The decided contract — consume it, do not re-open it.** Its Authoring rule first, then the 23 acceptance criteria, the non-goals, the 15 risks, and the 10 decisions. |
| [`FEATURE_REQUEST.md`](FEATURE_REQUEST.md) | Context only; every Open Question is disposed by the scope. **Its claim that CLAUDE.md's project map lists serving under `app/` is verified FALSE** — grep returns nothing. Don't inherit that reasoning; the real evidence is `.gitignore:68` and `.gitattributes:41`. |
| [`requests/feature-requests/README.md`](../README.md) | The pipeline contract: line 59–61 defines *testable* (one command, pass or fail), 71–73 the USER-RUN carve-out, 100 the status grammar, 106 the Index row. |
| [`pyproject.toml`](../../../pyproject.toml) | The file this changes most: 9 empty deps, 11–13 the comment to delete, 15–21 the dev group, 30–31 the hatch `packages` list, 49 DTZ, 50 PTH, 61–65 `[tool.mypy]` (must stay textually unchanged), 73 `pythonpath`. |
| [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) | Two jobs today: `Lint, types, tests` (19) and `Secret scan` (50). Line 34 `uv sync --locked`, 47 `--cov=rpg_core`, 10–12 `cancel-in-progress`, 22/25 the action majors already pinned. **Lines 3–7 are load-bearing — see the CI-trigger note below.** |
| [`ops/branch-protection.json`](../../../ops/branch-protection.json) | Line 4, the exact contexts array the new job's **display name** must join. Line 3's `strict: true` is why a path-filtered job would hang PRs forever. |
| [`ops/README.md`](../../../ops/README.md) | Line 12 the `gh api -X PUT` apply command, 20–24 the rename warning this item generalizes to job *addition*, 32–62 the uv section the Node section sits beside, 64–73 the four-command green gate. |
| [`tests/test_repo_structure.py`](../../../tests/test_repo_structure.py) | The guard idiom to copy: `_git_check_ignore` (24–34, works on paths that don't exist), the version pin (46–54), `test_scratch_root_is_gitignored` (83–92) as the template, the substring idiom (107–110) AC 17 extends. |
| [`tests/test_no_leaks.py`](../../../tests/test_no_leaks.py) | A blocking public-repo gate that now scans frontend files. **Its docstring at 12–13 says it reads the git INDEX** — stage before running or the result is a false green. Patterns at 26–29, `ALLOWED` at 32–35, the now-false docstring at 37, `TEXT_SUFFIXES` at 38–55. |
| [`tests/test_request_links.py`](../../../tests/test_request_links.py) | `FENCED_BLOCK` (26) and `_dead_links` (40–64). Read before writing any artifact. |
| [`src/rpg_core/__init__.py`](../../../src/rpg_core/__init__.py) | The whole domain core, 16 lines. Lines 3–6 state the dependency direction from the core's side. |
| [`DESIGN.md`](../../../DESIGN.md) | §3 at line 99; line 106 "Two packages, one repo." The layering guard's failure message cites this by name — Decision 3 chose a guard over an ADR, so **that citation is the record**. |
| [`.gitignore`](../../../.gitignore) | 66–68 the Node block; 62–63 blanket `dist/` and `build/` matching at **any** depth; 43–44 the careers carve-out; 18 `var/`. |
| [`.gitattributes`](../../../.gitattributes) | 3 `* text=auto eol=lf`, 7–10 the CRLF exception, 20–25 the ts/tsx/css/html entries, 35 `*.ico binary`, 41 `package-lock.json linguist-generated`. |
| [`.claude/settings.json`](../../../.claude/settings.json) | Lines 3–12 the `ask` list — `gh api *` at line 8 is why AC 23 step 2 is structurally impossible for an agent. **Lines 32–35 allow `gh pr view/list` and `gh run list/view` unprompted** — the agent can watch its own CI. |

**Verified absent by listing:** `app/`, `src/rpg_api/`, `tests/conftest.py`, `careers/`,
`datasets/`, `rulesets/`, `lib/`, `.gitleaks.toml`, `.gitleaksignore`. **Measured on this machine
2026-08-14:** node v24.15.0, npm 11.12.1; `gitleaks` **not** installed; ports **8000 and 5173 free**;
remote is `jordan-koch/nba2k-rpg`, matching `ops/README.md` lines 12 and 29.

> **CRITICAL — CI does not run on a feature-branch push.** `ci.yml` lines 3–7 trigger on
> `push: branches: [main]`, `pull_request`, and `workflow_dispatch` only. `/commit` pushes the
> branch and deliberately does **not** open the PR. So until a PR exists, **zero workflow runs
> exist** and AC 18 is unobservable. Phase 1's checkpoint therefore includes a **user action: open
> a draft PR**. Every later phase's CI evidence depends on it.

---

## 2. Architecture map

**Current structure** — one Python package holding a docstring and a version, three test modules,
no frontend.

```
src/rpg_core/__init__.py   16 lines. Docstring 3-6 declares it I/O-free and web-free.
                           __version__ = "0.1.0". No py.typed.
tests/                     Exactly three modules. There is NO tests/conftest.py.
pyproject.toml             deps empty (9); dev group (15-21); hatch packages (31);
                           mypy strict + files=["src","tests"] (61-65); pythonpath (73).
.github/workflows/ci.yml   Two jobs. Line 47 is the only occurrence of rpg_core.
ops/branch-protection.json Line 4 contexts; strict:true at line 3.
```

**Five seams, all pre-cut by Phase 0.**

1. **Package seam.** `files = ["src","tests"]` and `pythonpath = ["src"]` already reach anything
   under `src/`, so `src/rpg_api/` costs zero config churn on typing and test imports. The two
   places *not* automatic are the hatch `packages` list and `--cov=rpg_core` — which is exactly why
   AC 14 exists.
2. **Dependency-direction seam.** The health payload's `version` is `rpg_api`'s one honest reason to
   import `rpg_core`, exercising the arrow in the allowed direction — and
   `tests/test_repo_structure.py:46-54` already pins that value, so the payload inherits the pin free.
3. **CI-context seam.** `ops/branch-protection.json:4` lists **display names**; `ops/README.md:20-24`
   warns in prose. Prose does not fail a build. The guard closes the tracked half; the applied half
   can't be closed by any test, hence AC 23's ordered gate.
4. **Ignore seam.** `_git_check_ignore` shells `git check-ignore --no-index`, which works on paths
   that don't exist — so the guard can be written before `app/` does. The assertion that matters is
   the **negative** one: `app/src/main.tsx` must **not** be ignored.
5. **Leak seam.** `TEXT_SUFFIXES` already contains `.json`/`.ts`/`.tsx`/`.js`/`.mjs`/`.css`/`.html`.
   The moment they're tracked, the frontend configs are scanned.

**Target structure**

```
src/rpg_api/
  __init__.py   docstring mirroring rpg_core's from the API side; re-exports create_app
  app.py        create_app(spa_dist: Path | None = None) -> FastAPI  — the injectable factory
  health.py     APIRouter, GET /health, included under prefix "/api"
  spa.py        attach_spa(app, dist) — /api JSON-404 guard, traversal-safe resolve,
                history fallback, missing-build 503. No StaticFiles.
  serve.py      main() -> None — the [project.scripts] target

app/            Vite + React + TypeScript SPA, one page, ALL config scoped inside app/

tests/
  conftest.py         client factories parameterized on the injectable dist
  test_api_health.py  AC 2
  test_api_spa.py     ACs 5, 6, 7 + history fallback + traversal
  test_layering.py    AC 3
  test_ci_contexts.py AC 4
  test_packaging.py   AC 14
```

**The one non-obvious design call: no `StaticFiles` mount.** The obvious
`app.mount("/", StaticFiles(directory=dist, html=True))` breaks two criteria at once. It raises at
**construction** when the directory is absent (scope risk 7), so a fresh clone gets an import-time
traceback — AC 5 forbids that. And a mount at `/` still matches `/api/unknown` and answers with a
non-JSON 404 — AC 7 forbids that. So `spa.py` hand-rolls one catch-all, registered **last**, deciding
per request. **Leave both reasons in a source comment** or a future agent will "simplify" it straight
back into two bugs.

Deciding per request has a payoff: `spa_built` reads `(dist / "index.html").is_file()` at request
time too, so building the SPA while uvicorn runs flips both in the same instant — no "restart the
server" caveat to document, and no way for flag and route to disagree.

**No data surface, stated affirmatively.** `datasets/manifest.json`, `careers/`, and `rulesets/` do
not exist. Section 9 of the template is **omitted by decision, not oversight** — and the plan must
not invent a placeholder manifest entry to look complete.

---

## 3. Phased implementation

Eight phases. Each ends green locally on **`uv run ruff check` · `uv run ruff format --check` ·
`uv run mypy` · `uv run pytest -m "not network"`** (the order `ops/README.md:64-73` documents), then
lands through `/commit`. Run each as a separate invocation — PowerShell 5.1 has no `&&`.

### Phase 0 — Preflight: turn six beliefs into measurements

**Goal.** Six beliefs gate the shape of everything downstream. Measure them in a gitignored scratch
tree **before** a single tracked dependency lands, so the first surprise costs a probe rather than a
rewrite. Writes no application code and changes no tracked config.

**Steps**

1. **Confirm the branch — do NOT create one.** `git branch --show-current` must print
   `phase1/app-shell`, the branch already carrying this item's `FEATURE_REQUEST` and `PROJECT_SCOPE`
   commits. `git switch -c` here would fork a duplicate branch off the same tip. If you are on
   `main`, run `git switch phase1/app-shell`. *(Naming note: `ROADMAP.md` rows are `1.1`, but repo
   history uses slash-prefixed phase names — `phase0/public repo hardening`. The live branch wins;
   do not rename.)*
2. Work under `var/spike/` — gitignored at `.gitignore:18`, so nothing here can be committed by
   accident. **Every probe command must be non-interactive**: this harness runs PowerShell with
   stdin at the null device, so a console prompt reads EOF and the step hangs or errors.
3. **BELIEF 1** *(scope risk 7, inferred)* — does Starlette's `StaticFiles(directory=<absent path>)`
   raise at **construction**? Use `uv run --with fastapi --with starlette python <probe>`; `--with`
   builds an ephemeral overlay env and does **not** touch `uv.lock`. Record exception type and message.
4. **BELIEF 2** *(scope risk 6, unconfirmed)* — mypy strict over FastAPI. Write a ~15-line fully
   annotated app and run `uv run --with fastapi --with mypy mypy --strict --warn-unreachable <probe.py>`.
   Pass the flags **explicitly**: `var/` is outside `[tool.mypy] files`, so a bare `uv run mypy` won't
   see it. **Probe all three shapes this design may use**, not just the decorator: (a) `@app.get(...)`
   on an annotated handler, (b) reading `request.app.state.<attr>` into an annotated local, (c) a
   `Depends(...)`-injected value. Starlette's `State.__getattr__` returns `Any`, which trips
   `warn_return_any` if returned straight from a `-> Path` helper — and AC 8 bans the `# type: ignore`
   that would paper over it. **Record which shape is clean and have Phase 1 use it.**
5. **BELIEF 3** *(scope risk 10)* — scaffold non-interactively:
   `npm create vite@latest vite-probe -- --template react-ts` from `var/spike/`. Naming the target
   directory suppresses the name prompt and `--template` suppresses framework/variant. **If any
   prompt still appears the command is wrong — do not answer it, fix the invocation.** Then
   `npm install`, `npm run build`. Record `lockfileVersion` and the exact `dist/` layout. Also record
   the resolved majors for react, react-dom, vite, vitest, `@testing-library/react`,
   `typescript-eslint`, `eslint-plugin-react-hooks` — and check two boundaries explicitly:
   `@testing-library/react` **≥ 16** when React is 19 (earlier majors declare a React 18 peer), and
   that `eslint-plugin-react-hooks` exports a **flat config** object (≥ 5.2; fall back to manual
   `plugins`/`rules` wiring if not).
6. **BELIEF 4** *(scope risk 4, inferred)* — run the three regexes from `tests/test_no_leaks.py:26-29`
   directly against the probe's `package-lock.json` and `package.json`. The npm `author` field is the
   known EMAIL tripwire. For each hit record the remedy: a narrowly-justified `ALLOWED` entry with a
   written reason — **never** a weakened regex or a removed suffix.
7. **BELIEF 5** *(scope risk 5)* — **you chose to install gitleaks locally.** It is measured as not
   installed and `winget` is not in the allow list, so this is **your** command:
   `winget install gitleaks.gitleaks`. Then run it over the tree and record the result. If it trips on
   the lockfile's high-entropy sha512 integrity strings, remediate with specific fingerprints in a new
   `.gitleaksignore`, each with a written reason, mirroring the `ALLOWED` discipline — never a
   wholesale rule disable.
8. **BELIEF 6** *(scope risk 1)* — `git remote -v` is **measured** as `jordan-koch/nba2k-rpg`, matching
   `ops/README.md` lines 12 and 29: record as verified. Do **not** run `gh api` (ask list, line 8).
   Whether GitHub's protection API still accepts the current JSON stays **unconfirmed** and is your
   step in Phase 7.
9. Write results to `requests/feature-requests/1.1-app-shell/reviews/preflight.md`, one row per
   belief, each labelled with CLAUDE.md's vocabulary — *measured / verified / inferred / refuted*.
   **No belief may remain `unconfirmed`.** That file is scanned by `tests/test_request_links.py`.
10. Leave `var/spike/` in place — gitignored and useful for the rest of the build.

**Acceptance**

- `reviews/preflight.md` exists and carries a labelled result for all six beliefs, none left
  `unconfirmed`.
- `git status --porcelain` is empty except the new `reviews/preflight.md`, **and**
  `git diff --stat HEAD -- pyproject.toml uv.lock` is empty — proving `uv run --with` did not touch
  the lock. *(Do not use `--untracked-files=all` to check `var/`: that flag expands untracked
  directories, it does not display ignored paths, so the check would pass unconditionally.
  `git status --porcelain --ignored var/` is the informational form.)*
- All four Python commands exit 0 — the probe phase changed nothing a check can see.

**Commit.** CHECKPOINT — `/commit`. Stages only the preflight file. Suggested subject:
`docs(1.1): preflight — measure the app-shell's unconfirmed tooling beliefs`. Row 1.1 stays
`IN-PROGRESS`; nothing has been delivered.

### Phase 1 — The HTTP seam and all Python dependency bookkeeping

**Goal.** Land the seam and **all** dependency work in one commit, so `uv lock` runs exactly once for
the item and `uv sync --locked` is green from a clean checkout.

**Steps**

1. `pyproject.toml`, one pass: replace `dependencies = []` with fastapi + uvicorn and **delete the
   discharged reservation comment at 11–13** — leaving it makes the file lie. Take version floors from
   what `uv lock` actually resolves. **Declare `pydantic` explicitly** alongside fastapi if `health.py`
   imports it: it arrives only transitively today, nothing in the toolchain complains, and a future
   fastapi major that changes its pydantic pin becomes an unrelated-looking breakage. *(Alternative:
   return a `TypedDict` and import only what you declare.)*
2. Dev group gains `httpx` (TestClient raises at import without it), `pyyaml` + `types-PyYAML`
   (AC 4's parser plus the stubs mypy strict requires — **an explicit core deliverable**, not an
   undeclared test dependency), and `watchfiles`.
3. Line 31: `packages = ["src/rpg_core", "src/rpg_api"]`. **Scope risk 2** — the omission passes every
   local test because `pythonpath = ["src"]` masks it, and fails only at runtime.
4. Add `[project.scripts]` with exactly one entry: **`rpg-serve = "rpg_api.serve:main"`**
   *(your Decision A)*. This name is hardcoded in five places that must agree — `ops/README.md`,
   `README.md`'s Setup block, the CI smoke step, AC 19, and AC 22's panel copy.
5. Run `uv lock`, then `uv sync --locked`. **Commit `uv.lock` in this same commit.**
6. Edit `ci.yml` line 47 to `--cov=rpg_core --cov=rpg_api` (scope risk 11). One line, independent of
   the new job, so AC 14's second half is assertable from the start.
7. Create `src/rpg_api/__init__.py` — docstring mirroring the core's from the API side,
   `from __future__ import annotations`, re-export `create_app`.
8. Create `src/rpg_api/health.py` — `router = APIRouter()`, a fully annotated `GET /health` returning
   `{status, version, spa_built}`. **Read the version as `rpg_core.__version__`** — never re-type the
   literal. Pass the resolved dist in using **the shape BELIEF 2 measured clean**; bind through an
   annotated local (`dist: Path = request.app.state.spa_dist`), never an ignore.
9. Record Decision 6's standing rule in a code comment: *the payload gains a field only when the thing
   it reports exists.* No `career_count`, no `ruleset_version` (lies until 1.2/1.4), no
   `started_at`/`uptime` (no consumer, and DTZ taxes naive datetimes).
10. Create `src/rpg_api/app.py` — `create_app(spa_dist: Path | None = None) -> FastAPI`. Resolve the
    default from `Path(__file__).resolve()`, **never a literal path**. Use pathlib throughout (PTH).
    *Note the assumption:* the repo-relative default lands inside the tree only because uv installs the
    project **editable** from a checkout — which is exactly the scope's "it runs from a checkout"
    non-goal. A non-editable wheel gets the 503 branch, which is the designed fallback, not a bug. The
    Phase 5 smoke step is what would catch a wrong `parents[N]`.
11. Create `src/rpg_api/serve.py` — `main() -> None` calling
    `uvicorn.run("rpg_api.app:create_app", factory=True, host="127.0.0.1", port=8000)`. **IPv4 literal**,
    matching the Vite proxy (scope risk 9). Port 8000 measured free 2026-08-14. **No `__main__.py`** —
    Decision 9 permits one canonical incantation for the served build.
12. Create `tests/conftest.py` with three fully-annotated fixtures: `client_factory` returning
    `Callable[[Path], TestClient]`; `client` over a dist that does **not** exist (the fresh-clone state);
    `built_spa_dist(tmp_path)` writing a known `index.html` plus an assets file.
13. Create `tests/test_api_health.py` (AC 2) and `tests/test_packaging.py` (AC 14). The latter
    `tomllib`-loads pyproject (the idiom at `test_repo_structure.py:49-50`), asserts the hatch packages
    list contains both, then `yaml.safe_load`s `ci.yml` and asserts `--cov=rpg_api` appears in the
    Pytest step's `run` string. Give both a message explaining the runtime-only failure they prevent.
14. Confirm `git diff src/rpg_core/` is empty.

**Acceptance**

- `uv sync --locked` exits 0 with fastapi and uvicorn resolved in the tracked lock (AC 1).
- `uv run pytest tests/test_api_health.py` green — 200, `application/json`, status ok,
  `version == rpg_core.__version__`, `spa_built` is a bool (AC 2).
- `uv run pytest tests/test_packaging.py` green (AC 14).
- `uv run mypy` exits 0 under a **textually unchanged** `[tool.mypy]` block. Grep the diff for
  `type: ignore` and `[[tool.mypy.overrides]]`: zero new occurrences (AC 8).
- `uv run ruff check` and `uv run ruff format --check` green (AC 9).
- `git diff src/rpg_core/` is empty.

**Commit.** CHECKPOINT — `/commit`. The item's **only** dependency-and-lockfile commit. Suggested
subject: `feat(1.1): FastAPI seam — src/rpg_api, GET /api/health, packaging guard`.

> **USER ACTION at this checkpoint — open a draft PR** from `phase1/app-shell` to `main`.
> `ci.yml:3-7` gives a feature branch no push trigger, so `pull_request` is the only way any job ever
> reports. Every later phase's CI evidence depends on this. *(Fallback if you'd rather not open it
> early: `gh workflow run` — not in the allow list, so it prompts.)*

### Phase 2 — Serving the built SPA: both dist branches

**Goal.** Make the two dist states behave correctly and provably, with no listening socket and no
import-time traceback on a fresh clone.

**Steps**

1. Create `src/rpg_api/spa.py` with `attach_spa(app: FastAPI, dist: Path) -> None` registering one
   catch-all `@app.get("/{full_path:path}")`. Wire it as the **last** statement of `create_app`, after
   `include_router(..., prefix="/api")`. **Registration order is a correctness constraint, not style** —
   get it wrong and `/api/health` returns `index.html`, a failure that presents as a frontend bug.
2. Inside the handler, in this exact order: (a) if `full_path == "api"` or starts with `api/` →
   `raise HTTPException(404)`; FastAPI renders that as `application/json`, which **is** AC 7.
   (b) resolve `candidate = (dist / full_path).resolve()`; return `FileResponse` only if it `is_file()`
   **and** `candidate.is_relative_to(dist.resolve())` — *implementation note, not an acceptance
   criterion: this traversal check is two lines inside a branch the scope already requires. It is not a
   new criterion (see Decisions).* (c) else `index = dist / "index.html"`; if it `is_file()` →
   `FileResponse` — the history fallback. (d) else `PlainTextResponse(status_code=503)` whose body
   contains the literal `npm run build`.
3. **Do not use `StaticFiles`.** Leave a comment recording **both** reasons.
4. Make `spa_built` read `(dist / "index.html").is_file()` at **request** time, computed the same way
   the route decides.
5. Create `tests/test_api_spa.py`: AC 5 (absent dist — construction raises nothing, `/api/health` 200,
   `/` is 503 containing `npm run build`); AC 6 (present dist — `/` is 200, `text/html`, exact bytes);
   history fallback; AC 7 asserted on **both** branches; and a traversal case.

**Acceptance**

- `uv run pytest tests/test_api_spa.py` green on all five cases (ACs 5, 6, 7).
- `uv run pytest tests/test_api_health.py` still green — the catch-all did not shadow the health route.
- All four Python commands green.

**Commit.** CHECKPOINT — `/commit`. Independently shippable: the backend is complete and fully tested
with no frontend in the repo at all. Suggested subject:
`feat(1.1): serve the built SPA — both dist branches, JSON-404 boundary, history fallback`.

### Phase 3 — The three structural guards

**Goal.** Leave behind the conventions that protect the next ten items.

**Steps**

1. Create `tests/test_layering.py` with the guard as a **pure function** —
   `web_imports_under(root: Path) -> list[tuple[str, str]]`. Parse each `root.rglob("*.py")` with
   `ast.parse` and walk `ast.Import` / `ast.ImportFrom` — **AST, not regex**, so a docstring mentioning
   fastapi doesn't trip it. Guard `ast.ImportFrom` where `node.module is None` (relative import).
   Compare the first dotted segment.
2. Deny-list: `fastapi`, `starlette`, `uvicorn`, `rpg_api`. **`pydantic` deliberately absent** —
   [ADR 0002](../../../docs/decisions/0002-manual-ingestion-dto-boundary.md) requires the DTO be
   constructible with no HTTP and no UI, so that's item 1.2's call. Do not add it "for completeness".
3. Unit-test the function twice against `tmp_path` (**AC 3, no source mutation**): a fake module
   containing `import fastapi` reports exactly that file; a clean tree reports none. Then the real
   assertion over `src/rpg_core`, with a failure message **citing DESIGN.md §3 by name** — Decision 3
   made this test the record instead of an ADR, so the citation *is* the record.
4. Create `tests/test_ci_contexts.py` (AC 4) **with the same purity as the layering guard**, so its
   honesty check is runnable. Module-level helpers: `job_display_names(workflow: Path) -> set[str]`
   using `yaml.safe_load` and `{job.get("name", key) for key, job in doc["jobs"].items()}` — the `.get`
   fallback matters because a job may legally omit `name` — and
   `required_contexts(protection: Path) -> set[str]`, plus a `_diff_message(ci, protection) -> str`.
   The real assertion calls them on the tracked paths and asserts **set equality**: containment passes
   while a typo'd context ("Web app" vs "Web App") hangs every PR forever on a check that never
   reports. Compute `only_in_ci` and `only_in_protection` separately so the message names which side
   carries the extra.
5. **The honesty proof is a `tmp_path` unit test in the same module** — write a two-job workflow and a
   contexts array with one name typo'd, assert the comparison fails and the message names the side.
   *(Do not "mutate a scratch copy" ad hoc, and never edit the tracked `ci.yml` to watch a test go
   red — that is exactly what the pure-function shape exists to avoid.)*
6. Add AC 4's negative assertion: a **step**-level name — `Gitleaks` (`ci.yml:58`), `Install` (30),
   `Mypy` (42) — is **not** in the collected job-name set, proving the parser is structure-aware rather
   than grepping quoted strings. *(Aside for whoever debugs this: PyYAML parses a workflow's `on:` key
   as boolean `True` under YAML 1.1. Harmless — the guard reads only `doc["jobs"]`.)*
7. Add the app-ignore guard to `tests/test_repo_structure.py`, immediately after
   `test_scratch_root_is_gitignored` (83–92) so it **reuses** the module-private `_git_check_ignore`
   (24–34) including its `RuntimeError → pytest.skip` pattern. Assert `app/dist/index.html` and
   `app/node_modules/react/index.js` **are** ignored, and — the assertion that actually protects
   anything — `app/src/main.tsx` is **not**. Note in the docstring that `app/dist/` is covered twice
   (`.gitignore:62`'s blanket `dist/` and line 68), so a passing test does not prove line 68 survives.

**Acceptance**

- `uv run pytest tests/test_layering.py` green: tmp_path dirty case reported, tmp_path clean case
  empty, `src/rpg_core` empty — all in one run, no tracked source mutated (AC 3).
- The layering failure message contains the literal string identifying DESIGN.md §3.
- `uv run pytest tests/test_ci_contexts.py` green at today's two jobs and two contexts, **including
  the tmp_path honesty test and the negative step-name assertion** (AC 4).
- `uv run pytest tests/test_repo_structure.py` green including the app-ignore guard (AC 16).

**Commit.** CHECKPOINT — `/commit`. Suggested subject:
`test(1.1): layering, CI-contexts, and app-ignore structural guards`. These are the durable artifacts
of a content-free item.

### Phase 4 — `app/`: toolchain, the one page, and the leak gate

**Goal.** Stand up `app/` with a check posture matching the Python half from its first commit. Prove
the tracked frontend files clear the blocking leak guard **before** they enter history.

**Steps**

1. Scaffold **non-interactively**: `npm create vite@latest app -- --template react-ts` from the repo
   root. **Every config file lives inside `app/`** with scope limited to `app/` — `git ls-files .claude`
   returns 8 tracked `.js`/`.mjs` files, so a repo-root eslint or tsconfig would immediately start
   reporting on them and force an ignore list nobody scoped (an explicit non-goal).
2. `app/package.json`: `"private": true`, `"type": "module"`, version fixed at a placeholder. **No
   `author` field** — an email there fails `tests/test_no_leaks.py:29`, a blocking check.
3. Scripts — **every one a single command invocation, no shell operators.** PowerShell 5.1 has no `&&`
   at all. `dev`=`vite`, `build`=`vite build`, `typecheck`=`tsc --noEmit -p tsconfig.json`,
   `typecheck:negative`=`tsc --noEmit -p tsconfig.negative.json`,
   `check:negative`=`node scripts/check-negative.mjs`, `lint`=`eslint .`, `test`=`vitest run`.
   **`vite build` does not typecheck** — esbuild strips types — which is precisely why typecheck is a
   separate script and a separate CI step. Do not let a later simplification fold them together, and
   never ship `"build": "tsc && vite build"`.
4. Deps: react, react-dom. Dev: typescript, vite, `@vitejs/plugin-react`, `@types/react`,
   `@types/react-dom`, `@types/node`, vitest, jsdom, `@testing-library/react`,
   `@testing-library/jest-dom`, eslint, `@eslint/js`, typescript-eslint, `eslint-plugin-react-hooks`,
   globals. **Honor the two major boundaries BELIEF 3 recorded.**
5. **`app/tsconfig.json`** — a **single** config plus `@types/node` *(your Decision H)*: `strict: true`
   plus `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`,
   `noFallthroughCasesInSwitch`; target ES2022, module ESNext, moduleResolution bundler, jsx react-jsx,
   lib [ES2022, DOM, DOM.Iterable], noEmit, skipLibCheck, verbatimModuleSyntax.
   `include: ["src", "vite.config.ts"]`, `exclude: ["typecheck-fixtures", "dist", "node_modules"]`.
   **If `vite.config.ts`'s Node globals fight the browser DOM lib, switch to the template's app/node
   split — never loosen a strictness flag.** AC 8's spirit applies to the frontend half.
6. `app/typecheck-fixtures/bad.ts` — AC 11's committed fixture. Its errors **must be strict-specific**:
   one `strictNullChecks` error (`function len(s?: string) { return s.length }`) and one
   `noUncheckedIndexedAccess` error (`function first(xs: string[]): string { return xs[0] }`). A plain
   `const n: number = "x"` errors with strict **off** and would prove only that the compiler ran.
7. **`app/tsconfig.negative.json` — override BOTH keys:**
   `{"extends": "./tsconfig.json", "include": ["typecheck-fixtures"], "exclude": []}`.
   > **This is the false-green the panel caught.** A child config **inherits** the parent's `exclude`;
   > it does not reset it. Without `"exclude": []` the negative project resolves to **zero files**,
   > `tsc` exits non-zero with **TS18003** ("No inputs were found"), and the wrapper reports success —
   > so AC 11 passes because the config found nothing, not because `strict` caught the fixture. That is
   > exactly the failure AC 11 exists to rule out.
8. `app/scripts/check-negative.mjs` *(your Decision D)* — spawns the negative tsc run and exits 0 iff
   the inner run **failed**. Harden it so it cannot be fooled: capture stdout and assert (a) exit code
   non-zero, (b) output does **not** contain `TS18003`, (c) output contains the strict-family codes the
   fixture targets (TS18048/TS2532 for the `strictNullChecks` case, TS2322 for
   `noUncheckedIndexedAccess`). **Spawn portably:** on Windows `npm`/`tsc` are `.cmd` shims and
   `spawnSync("npm", …)` without `shell: true` fails ENOENT — invoke tsc's JS entry through
   `process.execPath` instead, which sidesteps the shim on both platforms.
9. `app/eslint.config.js` (flat config): `@eslint/js` recommended + typescript-eslint recommended +
   `eslint-plugin-react-hooks` *(Decision 2, taken against the panel's oxlint recommendation)*.
   `ignores`: `dist`, `typecheck-fixtures`. **Keep `scripts/` linted — and wire its globals**, or
   `npm run lint` fails on the very file that makes AC 11 runnable: add a config object with
   `files: ["scripts/**/*.mjs"]` and `languageOptions: { globals: globals.node, sourceType: "module" }`.
   That is what the `globals` dependency is for. **No prettier gate** — a visible default, not an
   oversight.
10. `app/vite.config.ts` importing `defineConfig` from `vitest/config` (it re-exports vite's and adds
    the test block, so no second config file). React plugin; `server.proxy` mapping `/api` to
    `http://127.0.0.1:8000` — **the IPv4 literal**, because Node on Windows can resolve `localhost` to
    `::1` while uvicorn binds 127.0.0.1, producing an ECONNREFUSED indistinguishable from a dead
    backend (scope risk 9). This proxy is the **entire** CORS story; no CORS middleware exists in
    either mode. `test: { environment: "jsdom", setupFiles: "./src/setupTests.ts", globals: false }`.
11. **`app/src/setupTests.ts` — exactly this, because `globals: false` breaks the defaults:**
    `import "@testing-library/jest-dom/vitest";` — the **vitest-specific entry**, not the bare package,
    which has no global `expect` to extend — plus
    `import { afterEach } from "vitest"; import { cleanup } from "@testing-library/react"; afterEach(cleanup);`.
    > Without the first, `toBeInTheDocument()` is simply absent and the obvious "fix" is to flip
    > `globals: true`, silently diverging from the plan. Without the second, RTL's auto-cleanup never
    > registers, the first test's DOM leaks into the second, and `getByText` on the version string
    > throws "found multiple elements" — in exactly the two-test suite AC 12 pins.
12. `app/src/api/client.ts` — `export interface Health { status: string; version: string; spa_built: boolean }`
    and an async `fetchHealth()` against the **relative** path `/api/health`. Relative is what makes
    both modes same-origin. Explicitly **not** the deferred codegen contract — the seam it slots into
    at item 1.8.
13. `app/src/App.tsx` with exactly three states — loading, ok (status + version), unreachable. **The
    unreachable panel must name the start command** (AC 22). Plus `app/src/main.tsx`, `app/index.html`
    (real title + favicon link, not Vite defaults), `app/public/favicon.svg` (prefer `.svg` —
    `.gitattributes:35` marks `*.ico binary`, which makes it undiffable for no benefit).
14. `app/src/App.test.tsx` — **exactly two** Vitest tests (AC 12): the page renders the fetched version;
    the unreachable panel renders on a rejected fetch. **Under `globals: false`, import `describe`,
    `it`, `expect`, `vi` explicitly from `vitest`.** Stub with `vi.stubGlobal("fetch", vi.fn())` so
    `client.ts` is exercised too, rather than mocking the module and testing nothing.
15. Repo-root `.editorconfig`: `root = true`, utf-8, final newline, `end_of_line = lf` globally with
    `crlf` for `{ps1,psm1,bat,cmd}` — it must **agree** with `.gitattributes` lines 3 and 7–10, not
    fight them. Indent 4 default, 2 for `{ts,tsx,js,mjs,json,css,html,yml,yaml}`.
16. **GUARD AGAINST THE ITEM'S MOST LIKELY FAILURE** (scope risk 12): no career, no stub player, no
    fake XP number, no router, no state library, no second page. Run `git status --short` and
    `git diff --stat`: no `careers/`, `rulesets/`, `datasets/`, or `var/` paths, and
    `src/rpg_core/__init__.py` byte-identical to HEAD.
17. Run `npm install` (generates the lock), then `npm ci`, `npm run typecheck`, `npm run check:negative`,
    `npm run lint`, `npm run test`, `npm run build`. Confirm `app/dist/index.html` exists.
18. **PRE-STAGING GATE, and the order is load-bearing.** Stage first with
    `git add --intent-to-add app/`, **then** run `uv run pytest tests/test_no_leaks.py` (AC 13). The
    scanner reads `git ls-files` — the **index**, per its docstring at 12–13 — so a run against
    untracked files is a **false green**. This is the single most likely way this item's public-repo
    guard gets bypassed by accident.
19. **SILENT-IGNORE CHECK:** cross-check `git status --porcelain --untracked-files=all app/` against
    `git check-ignore --no-index` per source file. `.gitignore` 62–63's blanket `dist/` and `build/`
    match at **any** depth, so a source file landing in a directory of either name under `app/` would be
    silently untracked with nothing complaining.

**Acceptance**

- From `app/`: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run test`, `npm run build` each exit
  0, and `app/dist/index.html` exists (AC 10).
- `npm run check:negative` exits 0 — meaning the inner run exited **non-zero** — **and its output
  contains no `TS18003` and does contain the strict-family codes** (AC 11).
- `npm run test` green with **exactly two** tests; count the reported total — the criterion is a count,
  not a floor (AC 12).
- With `app/` staged via `--intent-to-add`, `uv run pytest tests/test_no_leaks.py` green (AC 13).
- `uv run pytest tests/test_repo_structure.py tests/test_request_links.py` still green (AC 16).
- No eslint or tsconfig file at the repo root; both inside `app/`, scoped to `app/`.
- No npm script contains `&&`, `rm`, `cp`, or a POSIX inline env prefix.
- `git diff src/rpg_core/` empty; the diff contains no `careers/`, `rulesets/`, `datasets/`, `var/` paths.

**Commit.** CHECKPOINT — `/commit`. This is the commit that introduces `package-lock.json` to a public
repo, so the leak test must have been run against the **staged** tree. Stage `app/` by path — never
`git add -A` — and confirm the staged list contains no `node_modules/` and no `app/dist/`. Suggested
subject: `feat(1.1): app/ — Vite + React + strict TS, eslint, two Vitest tests, dev proxy`.

### Phase 5 — CI job, required context, dependabot, real-server smoke

**Goal.** Make a broken frontend turn a PR red the same way a broken backend does, and land the
workflow change and the branch-protection change in **one** commit. This phase addresses the item's
headline risk.

**Steps**

1. Choose the display name once — **`Web app`** — and type it **character-identically** in `ci.yml`'s
   `name:` and `ops/branch-protection.json` line 4.
2. Add a third job parallel with `python` and `secrets`, with
   `defaults: { run: { working-directory: app } }`. Steps: `actions/checkout@v5` (matching line 22),
   `actions/setup-node` **pinned to the current major — confirm it on the marketplace before this
   commit; this is the one claim the panel could not close offline** — with `node-version: 24`
   (matching measured local v24.15.0), `cache: npm`, `cache-dependency-path: app/package-lock.json`.
   > **GOTCHA:** `defaults.run.working-directory` applies only to `run:` steps, **never** to `uses:`
   > inputs — so that cache path is repo-root-relative. A wrong value does not fail; it **silently
   > disables caching**, and `cancel-in-progress` means the job re-runs on every push.
3. Then `npm ci`, `npm run typecheck`, `npm run check:negative`, `npm run lint`, `npm run test`,
   `npm run build`, and `test -f dist/index.html`.
4. Add the **real-server smoke step** to the same job (AC 18, **Decision 8, taken against the panel's
   recommendation — do not quietly drop it**). It needs both toolchains: add `astral-sh/setup-uv@v6`
   (matching line 25) and `uv sync --locked` with working-directory `.`. Start `rpg-serve` in the
   background, then poll readiness with a **bounded** loop — `curl --retry-connrefused --retry 30
   --retry-delay 1 --max-time 60`, or an explicit loop that `exit 1`s on exhaustion. **Never a fixed
   sleep** (scope risk 14). Assert `GET /` is 200 `text/html` and `GET /api/health` is 200 JSON
   containing `"status":"ok"`. Use `set -euo pipefail`.
5. Edit `ops/branch-protection.json` line 4 to
   `["Lint, types, tests", "Secret scan", "Web app"]` — **in the same commit** as the workflow change.
   The Phase 3 guard fails the build if they drift, which is the point.
6. **Do not add `paths-ignore` or any path filter to any job.** With `strict: true` and named contexts,
   a filtered job that never reports makes PRs wait forever — the silent hang `ops/README.md:20-24`
   warns about, and an explicit non-goal.
7. Edit `.github/dependabot.yml`: **delete the line-30 placeholder** and add a
   `package-ecosystem: "npm"` entry with `directory: "/app"`, monthly schedule,
   `commit-message.prefix: "deps"`, `labels: ["dependencies"]`, and the same semver-patch ignore block
   the uv entry carries at 26–28 (AC 15).
8. `uv run pytest tests/test_ci_contexts.py` must be green at **three** contexts. If red, the two files
   disagree and the guard is doing its job.

**Acceptance (pre-commit, all locally checkable)**

- `uv run pytest tests/test_ci_contexts.py` green at three jobs and three contexts, including the
  honesty test and the negative step-name assertion (AC 4).
- Cross-read once by eye: the `name:` string and the new contexts entry are character-identical.
- `uv run pytest tests/test_packaging.py` still green with the workflow restructured (AC 14).
- `.github/dependabot.yml` carries the npm entry and the placeholder is gone (AC 15).
- `ci.yml` contains no `paths`/`paths-ignore` filter; the smoke step uses a bounded poll with an
  explicit exhaustion failure, not a fixed sleep.
- `uv run pytest -m "not network"` green; `uv run mypy` green with types-PyYAML satisfying the stubs.

**Phase 5b — post-push verification (after `/commit` pushes, against the open PR)**

- `gh run list --branch phase1/app-shell --limit 1` shows a completed run whose **`Web app`** job is
  green; `gh run view <id> --log` shows the smoke step's two curls (AC 18). **Both commands are
  allowlisted at `.claude/settings.json:32-35` and need no prompt** — reading a run is not applying
  protection. On failure read the log rather than re-pushing blind.

> Split out because Phase 5's CI evidence can only exist **after** the push that `/commit` performs —
> as one acceptance list it was a circular gate.

**Commit.** CHECKPOINT — `/commit`. The workflow change and the contexts change **must** be in this one
commit; splitting them defeats the guard. Note in the PR description that
`ops/branch-protection.json` is inert until re-applied. Suggested subject:
`ci(1.1): Web app job, required context, npm dependabot, real-server smoke`.

### Phase 6 — Make the docs describe the application that now exists

**Goal.** Goal 7 has no pass/fail check unless one is written. Bring four documents back into
agreement with reality and land AC 17's structural test so drift becomes a test failure.

**Steps**

1. `ops/README.md`: add a `## Node toolchain` section beside the uv one (32–62) — node 24 / npm 11 as
   measured, `npm ci` from `app/`, and **the npm stale-lock rule stated with the same sharpness lines
   54–57 give the uv rule** (`npm ci` fails when `package.json` and `package-lock.json` disagree, so any
   script rename or dependency bump means re-running `npm install` and committing the regenerated lock
   in the same commit). Add the PowerShell form of the negative-typecheck assertion.
2. Document **both run modes**, and note the scoping precisely:
   - **Dev** — two terminals *(Decision 4)*:
     `uv run uvicorn rpg_api.app:create_app --factory --reload --host 127.0.0.1 --port 8000` in one,
     `npm run dev` from `app/` in the other. A launcher was rejected because a Node process-runner
     receiving Ctrl+C in PowerShell can orphan the Python child holding the port, so the next run dies
     `EADDRINUSE`. **`watchfiles` in the dev group is what makes `--reload` fast** — that is its stated
     purpose.
   - **Served** — `uv run rpg-serve`, **alone**.
   > **Decision 9's caveat binds the SERVED build only**: do not document a second way to run the
   > served build. The dev-mode uvicorn command is perfectly legal and must be written down.
3. `ops/README.md`: generalize the rename warning at 20–24 to cover job **addition**, and state loudly
   that the protection file is inert until re-applied with `gh api -X PUT`.
4. `README.md`: delete the `**No application code yet.**` banner (12–13); add `app/` and `src/rpg_api/`
   to the project map (53–69, where line 64 says rpg_core is "Empty until Phase 1"); remove the web app
   from the "don't exist yet" sentence (71–72); extend Setup (74–83) with the Node steps and both run
   commands.
5. `CLAUDE.md`: fix the Status section (20–21), add `app/` and `src/rpg_api/` to the project map (the
   rpg_core line is 58), and correct line 66's "and the web app don't exist yet". **CLAUDE.md has a
   hard line budget — this is an EDIT, not an append.**
6. `ROADMAP.md` line 156: the phase-header prose reads "**IN-PROGRESS** — 1.1 `app-shell` is at intake.
   No application code has landed yet." **Both sentences are false.** This is *prose* — `/commit`'s
   Step 4 owns the Status **column** and the `**Status:**` markers, not the surrounding sentence. Raise
   it inside the `/commit` run and correct it in the same commit; never as a separate ad-hoc edit.
   **The Size cell on row 1.1 stays `M`** — Decision 7 made it advisory and deliberately did not change
   it; `/commit`'s mandate covers Status cells only, so editing Size is exactly the ad-hoc table edit
   CLAUDE.md forbids.
7. Fix `tests/test_no_leaks.py` line 37: "Binary and lockfiles are skipped." is **true** of `uv.lock`
   (`.lock` is not in `TEXT_SUFFIXES`) and **false** of `package-lock.json` (**`.json` is, at line 42**).
   This item makes it wrong, so this item fixes it. **Change nothing else in that file** — no regex, no
   suffix.
8. Add AC 17's doc-agreement tests to `tests/test_repo_structure.py` in a new
   `# ─── Documentation ───` section, in the read-and-assert-substring idiom at 107–110. Assert:
   `README.md` does not contain `no application code yet` **compared lowercased**; `CLAUDE.md` contains
   both `app/` and `src/rpg_api/`; `CLAUDE.md` does not contain `no application code yet` (also
   lowercased); `ops/README.md` contains a Node-toolchain heading and both run-mode commands.
   > **The case trap, and your Decision C.** `README.md:12` capitalizes the N; `CLAUDE.md:21` does not.
   > A case-sensitive check silently passes on one of the two. You chose to fix **both** documents and
   > assert both lowercased — a small, deliberate widening of AC 17's literal text.
9. **Verify AC 19 end to end — PowerShell-native, no new permissions.** Start `uv run rpg-serve`
   backgrounded, then poll with
   `uv run python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health').status==200 else 1)"`
   — covered by the existing `PowerShell(uv *)` allow entry. **Do not use `curl`**: in PowerShell 5.1
   it is an alias for `Invoke-WebRequest`, which rejects curl's flags, and neither is allowlisted.
   **Then stop the backgrounded server before moving on** — Phase 7's ACs 20 and 21 both bind
   127.0.0.1:8000 and will die `EADDRINUSE` if it is still running, with a symptom that points at the
   frontend.
10. **MARKDOWN RAIL** for every document written in this phase: `app/`, `src/rpg_api/`, `app/dist/`,
    `tests/conftest.py` appear as inline code or inside fences, **never as a markdown link**.
11. Full green sweep in one sitting: all four Python commands, plus from `app/`: typecheck,
    check:negative, lint, test, build.
12. Grep the final diff for `type: ignore`, `[[tool.mypy.overrides]]`, `# noqa`, `eslint-disable`: zero
    new occurrences, or each individually justified in the commit message. **A green run bought by
    loosening a gate fails ACs 8 and 11 retroactively.**
13. Run gitleaks over the tree (installed in Phase 0 per your decision) before the final push.

**Acceptance**

- `uv run pytest tests/test_repo_structure.py` green including the Documentation section (AC 17).
- `Select-String -Path README.md -Pattern "No application code yet"` returns nothing;
  `Select-String -Path ROADMAP.md -Pattern "at intake"` returns nothing.
- `ops/README.md` documents exactly **one** canonical way to run the served build, and both run modes
  appear.
- `uv run rpg-serve` starts the served mode and both `/` and `/api/health` answer 200 (**AC 19 — this
  is agent-provable and must be claimed, not handed over**).
- `uv run pytest tests/test_request_links.py` green (AC 16).
- All four Python commands and all five frontend commands green in one sitting.
- `tests/test_no_leaks.py` line 37 is accurate about `package-lock.json`, and no regex or suffix changed.

**Commit.** CHECKPOINT — `/commit`, and **this is the one to let the full doc sweep run on** (a new
directory, a new convention, a changed setup step, and an advanced request status all fire). `/commit`
advances `ROADMAP.md` row 1.1 to `DONE` by matching the Deliverable cell against the tree, not the
branch name. Suggested subject:
`docs(1.1): describe the application that now exists, and test that the docs agree`.

### Phase 7 — Hand over the four user-run criteria and the merge gate

**Goal.** Prove the four things no agent can prove, in an order that does not let this exact PR be the
one that lands with a red frontend.

**Steps**

1. The agent's work stops at the push. `/commit` pushes the branch; it does **not** open the PR, never
   pushes `main`, never force-pushes, never amends.
2. **Write AC 23's ordered gate into the PR description as four numbered steps**, because the
   sequencing is the whole point:
   1. Let the **`Web app`** job report **once** on the open PR, confirming the context name verbatim
      against `ops/branch-protection.json:4`.
   2. **You run**
      `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json`
      *(owner/repo verified against `git remote -v`, 2026-08-14)*.
   3. Confirm the new check shows as **Required** on the open PR.
   4. **Then** merge.
3. State plainly that an agent **cannot** do step 2 — `gh api *` is in the ask list at line 8 — and that
   editing the JSON alone never changes GitHub. **Re-applying after merge would guarantee the PR
   introducing the job is exactly the one that could land with a red frontend.**
4. **AC 20 — the dev seam.** Two terminals. The Vite URL renders the version string **and the browser
   network tab shows `/api/health` served on the Vite origin**, not a cross-origin call to the API port.
   That second half is what actually proves the proxy, and therefore the no-CORS-middleware decision; a
   rendered version string alone does not.
5. **AC 21 — the built seam.** `npm run build`, then `uv run rpg-serve` alone with no Vite dev server:
   the same page renders at the uvicorn origin.
6. **AC 22 — the failure state.** With the page open, stop the backend. The page renders the legible
   "backend unreachable" panel naming the start command — not a blank screen, not an uncaught console
   error.
7. If the implementer spawns **any** subagent (plausible for SPA scaffolding), tell it git is
   **read-only**: no `checkout`/`reset`/`restore`/`clean`/`stash` or anything that discards working-tree
   state.
8. Post-merge pruning stays yours, and `-d` is **not** the check: PRs land as squash merges, so the
   branch tip is never an ancestor of `main`. The check that works is
   `git fetch origin; git diff phase1/app-shell origin/main --stat` — empty output means fully merged,
   and only then is `-D` appropriate.

**Acceptance** — exactly four USER-RUN criteria:

- **AC 20:** the version string renders at the Vite origin **and** the network tab shows `/api/health`
  on that same origin.
- **AC 21:** the same page renders at the uvicorn origin with no Vite process running.
- **AC 22:** stopping the backend produces a legible panel naming the start command.
- **AC 23:** the `Web app` check shows as **Required** on the open PR **before** the merge button is
  used, and all three contexts report green.
- The PR description contains the ordered four-step gate verbatim, step 2 marked as yours, so the
  sequence survives being done tomorrow instead of today.
- No agent invoked `gh api`, `git merge`, or `git push origin main` at any point.

> **AC 19 is NOT user-run.** The scope marks exactly four (20–23). AC 19 was proven in Phase 6 and the
> acceptance panel **must** claim it — it is the one check that catches a missing hatch `packages`
> entry independently of AC 14's structural test.

**Commit.** NO CODE COMMIT — this phase is verification and the merge gate. If a user-run check fails,
the fix goes back through the phase that owns it (AC 20/22 → Phase 4 or the proxy config; AC 21 →
Phase 2; AC 23 → Phase 5) and returns through `/commit` as a **new commit** on the same branch — never
`--amend`.

---

## 4. Testing & verification

**The per-phase green gate**, unchanged from `ops/README.md:64-73`:

```
uv run ruff check
uv run ruff format --check
uv run mypy
uv run pytest -m "not network"
```

From Phase 4 onward add, from `app/`: `npm ci`, `npm run typecheck`, `npm run check:negative`,
`npm run lint`, `npm run test`, `npm run build`. These **are** the new CI job's steps, so a green local
run predicts a green CI run.

**Per-criterion selectors** — the cold agent's map:

| AC | Command |
|---|---|
| 1 | `uv sync --locked` |
| 2 | `uv run pytest tests/test_api_health.py` |
| 3 | `uv run pytest tests/test_layering.py` |
| 4 | `uv run pytest tests/test_ci_contexts.py` |
| 5, 6, 7 | `uv run pytest tests/test_api_spa.py` |
| 8 | `uv run mypy` **plus** a diff grep for `type: ignore` and `[[tool.mypy.overrides]]` |
| 9 | `uv run ruff check` and `uv run ruff format --check` |
| 10 | from `app/`: `npm ci` / typecheck / lint / test / build, then confirm `app/dist/index.html` |
| 11 | `npm run check:negative` — exits 0 iff the inner tsc exited non-zero, with no `TS18003` |
| 12 | `npm run test`, and **count** the reported total — a count, not a floor |
| 13 | `git add --intent-to-add app/` **then** `uv run pytest tests/test_no_leaks.py` |
| 14 | `uv run pytest tests/test_packaging.py` |
| 15 | read `.github/dependabot.yml`; the line-30 placeholder must be gone |
| 16 | `uv run pytest tests/test_repo_structure.py tests/test_request_links.py` |
| 17 | `uv run pytest tests/test_repo_structure.py` (Documentation section) |
| 18 | `gh run list --branch phase1/app-shell --limit 1` then `gh run view <id> --log` (Phase 5b) |
| 19 | `uv run rpg-serve` plus the urllib poll of both routes — **agent-provable** |
| 20–23 | **USER-RUN**, Phase 7. The acceptance panel must **not** claim them. |

**Why the two red-before-green proofs are structured as they are.** ACs 3 and 11 both demand evidence
that a guard actually fails when it should, and both are built to prove it **without editing tracked
source**: the layering guard is a pure function fed a `tmp_path` fake, and the tsconfig proof is a
committed fixture with the non-zero assertion living in a caller. The original plan asked the
implementer to add `import fastapi` to the domain core and revert it — in a repo where agents have
read-only git, and in the PR whose entire point is that the import must not be there.

**The two testing subtleties that will bite.**

1. `tests/test_no_leaks.py` scans the **git index**, not the working tree. A brand-new untracked
   `app/package-lock.json` is invisible, so a pre-staging run is a false green.
2. `tests/test_request_links.py` strips **only** fenced blocks. Inline backticks are not exempt.

**Regression safety.** This item creates ground rather than changing behavior, so risk concentrates in
the guards it newly exposes: `test_no_leaks` now scans frontend files, `test_request_links` now scans
this plan, the version pin now transitively covers the health payload, and `test_ci_contexts` turns any
future job rename or addition into a build failure instead of a silently forever-pending PR. Coverage
is extended rather than left to rot — `ci.yml:47` gains `--cov=rpg_api`, without which the number
quietly stops describing the codebase (no `fail-under` is configured, so nothing else would complain).

**The strongest regression check here is a non-goal check**, worth running at Phase 4 and again at
Phase 6: `git diff src/rpg_core/` must be **empty**, and the diff must show no `careers/`, `rulesets/`,
`datasets/`, or `var/` paths.

---

## 5. Decisions

**Carried from the scope** (all ten, already disposed at stage 2): Vitest lands now with exactly two
tests; eslint + typescript-eslint + react-hooks over oxlint; no ADR 0010; two dev commands, no
launcher; no env keys; `spa_built` in the payload; no budget — full core plus every fold; the CI smoke
step is in; a console entrypoint; no `ops/check.ps1`.

**Disposed at this stage (stage 3):**

| # | Decision | Rationale |
|---|---|---|
| A | Console script is **`rpg-serve = "rpg_api.serve:main"`** | Matches the `uv run <tool>` idiom, says what it does, and is short enough to read inside AC 22's error panel. Hardcoded in five places that must agree. |
| B | **gitleaks installed locally** before the push — *against the panel's recommendation* | The panel recommended accepting CI as the gate on cost grounds. You chose the answer before the push rather than on the PR. `winget install gitleaks.gitleaks` is **your** command; `winget` is not allowlisted. |
| C | **AC 17 fixes both `README.md` and `CLAUDE.md`**, asserted lowercased | `README.md:12` capitalizes the N, `CLAUDE.md:21` does not — a case-sensitive test silently passes on one. A deliberate, small widening of AC 17's literal text; leaving a doc saying "no application code yet" next to a running application is what Goal 7 exists to prevent. |
| D | **`app/scripts/check-negative.mjs`** carries AC 11's assertion | An npm script cannot assert its own exit code and PowerShell 5.1 cannot negate one inline. One command invocation, identical on both platforms, keeping every script free of shell operators. One file the scope did not enumerate — flagged, not smuggled. |
| E | **`actions/setup-node` pinned to the current major**, confirmed on the marketplace before Phase 5; Node pinned to 24 | The repo pins `checkout@v5` and `setup-uv@v6`, so the current setup-node major is plausibly ahead of the v4 most examples show. **This is the one claim that stays UNCONFIRMED until someone with network access checks it.** |
| F | **No `py.typed`** in either package | Irrelevant to in-repo mypy (`files` checks sources directly) and there are no wheel consumers. Adding it to `rpg_api` alone would be the wrong asymmetry; adding it to both touches `rpg_core`, which the no-domain-logic non-goal makes awkward. Worth an intake item if the wheel is ever consumed. |
| G | **Port 8000** (API) and 5173 (Vite) | uvicorn's default, hardcoded identically in exactly two places — `serve.py` and the Vite proxy target — with `ops/README.md` naming those as the places that must stay in step. Decision 5 rejected an env key precisely to avoid a *second* place for the target to drift. **Both measured free on this machine, 2026-08-14.** |
| H | **Single `app/tsconfig.json`** plus `@types/node`, not the template's split | One fewer thing to reason about and one fewer file for the negative project to extend. Fallback recorded: if `vite.config.ts`'s Node globals fight the browser DOM lib, switch to the split — **never** loosen a strictness flag. |
| I | **No `StaticFiles` mount**; hand-rolled catch-all registered last, deciding per request | The obvious mount breaks two criteria at once: construction-time failure on a missing directory (AC 5) and a non-JSON 404 for unknown `/api` paths (AC 7). The reason must live in a source comment. |
| J | **`spa_built` evaluated per request**, not at construction | With no mount to stay consistent with, per-request is strictly better: flag and route read the same predicate and cannot disagree, and building while uvicorn runs flips both in the same instant — no "restart the server" caveat to document. |
| K | **The dist location is a factory argument** with a repo-relative default and no env key | AC 5 requires constructing against a nonexistent path with no exception, which a module constant makes untestable. The default is correct only under an editable install — which *is* the scope's "runs from a checkout" non-goal, stated rather than assumed. |
| L | **The traversal check is an implementation note, not an acceptance criterion** | One planner proposed it; the merge promoted it to an acceptance line with no decision entry. The two lines are cheap and correct and stay — but the acceptance panel measures the **23 criteria the scope decided**, not a 24th nobody agreed. |
| M | **`reviews/preflight.md` is a tracked artifact with its own commit** | Two of the item's design-shaping claims are labelled *inferred* or *unconfirmed*, and CLAUDE.md's rule is that an unconfirmed claim is a task. The tracked-file form (over a commit-message record) is justified because **items 1.2–1.11 inherit these measurements** — the node/npm majors, the Starlette behavior, and the mypy-strict shape are not re-measured per item. |
| N | **Layering guard parses with `ast`**, deny-list excludes `pydantic` | AST means a docstring mentioning fastapi does not trip it, and first-segment comparison catches `from fastapi.testclient import …`. Pydantic's absence is the scope's call, grounded in ADR 0002: that is item 1.2's decision. |
| O | **Template section 9 (Data contracts) omitted by decision** | Conditional in the skill's menu, and verified inapplicable: no dataset, no source, no network call. The plan must not invent a placeholder manifest entry to look complete. |

---

## 6. Risks & gotchas

1. **HEADLINE — silent-green merges.** The protection file lists contexts by **display name** and is
   inert until re-applied with `gh api -X PUT`. A PR merges with a red frontend job and nothing
   complains, indefinitely. Mitigation is split by construction: AC 4's guard covers the tracked half,
   AC 23's ordered gate covers the applied half. **Still unconfirmed:** whether GitHub's API accepts the
   current JSON unchanged — not re-applied since Phase 0, and only you can test it.
2. **The artifact-authoring trap, and it fires on this very PR.** Write `app/`, `src/rpg_api/`,
   `tests/conftest.py`, `app/dist/` as inline code or fenced, never as a link, until they exist.
3. **Omitting `src/rpg_api` from the hatch `packages` list fails only at runtime.** `pythonpath`
   masks it from every test. The sneakiest failure in the item.
4. **`test_no_leaks` scans the git index.** A pre-staging run is a false green — the single most likely
   way this item's blocking public-repo guard gets bypassed by accident.
5. **`test_no_leaks` now scans frontend files.** A `package.json` `author` email hits EMAIL; a
   Windows-generated absolute path hits WINDOWS_PATH. *Inferred, not measured* — Phase 0 BELIEF 4
   measures it.
6. **npm stale lock.** `npm ci` fails when `package.json` and `package-lock.json` disagree, exactly as
   `uv sync --locked` does. Any edit to `app/package.json` — a script rename, a dependency bump —
   requires re-running `npm install` and committing the regenerated lock **in the same commit**, or the
   new CI job goes red with an error naming a package rather than the skew.
7. **`StaticFiles` at `/` breaks two ACs at once**, and it is the obvious implementation.
8. **Route registration order is load-bearing.** The catch-all must be registered **after** the router,
   and the api-prefix 404 must be the **first** branch inside it. Get either wrong and `/api/health`
   returns `index.html` — a failure that presents as a frontend bug, inherited by items 1.7–1.11.
9. **mypy strict over FastAPI.** `disallow_untyped_decorators` is the classic friction point, and
   `request.app.state` returns `Any`, which trips `warn_return_any`. **The failure mode to refuse is a
   per-module override** carving `rpg_api` out of strict on its first day. Remedy: annotated signatures
   and annotated locals.
10. **npm scripts with shell operators work in CI and fail locally.** `"build": "tsc && vite build"` —
    the shape half the Vite templates ship — is broken on your daily shell.
11. **Windows/Node IPv6 resolution.** A proxy targeting `localhost` can resolve to `::1` while uvicorn
    binds 127.0.0.1, producing an ECONNREFUSED that looks exactly like a dead backend. Burns an hour
    unpinned, because the symptom points at the wrong process.
12. **setup-node cache path is repo-root-relative** even under `defaults.run.working-directory`. A wrong
    value doesn't fail — it silently disables caching.
13. **Node major skew.** A lockfileVersion difference between npm majors yields a lock that installs
    locally and fails `npm ci` in CI.
14. **`vite build` does not typecheck.** A green build proves nothing about types.
15. **The ill-typed fixture must fail for a strict-specific reason**, and the negative project must
    override the inherited `exclude` — see Phase 4 step 7.
16. **The CI smoke step is a flake vector** (Decision 8, taken against the panel). Bounded poll, explicit
    exhaustion failure. **If it flakes twice, tighten the poll — do not delete the only check that
    exercises uvicorn and the real filesystem serve.**
17. **npm supply chain in a public repo.** `npm ci` runs install scripts (esbuild fetches a platform
    binary) and pulls a tree orders of magnitude larger than the four-package Python dev group. The
    honest position is to record the exposure, not claim it is handled.
18. **Silent gitignore shadowing.** Blanket `dist/` and `build/` match at any depth. Line 62 already
    covers `app/dist/` independently of 68, so a passing ignore guard does not prove line 68 survives.
19. **Scope leakage into item 1.2** — the highest-probability way this item fails on its own terms.
20. **Subagent git is read-only.** No `checkout`/`reset`/`restore`/`clean`/`stash`.
21. **Out of scope but worth recording before item 2.1:** `.gitignore:63`'s blanket `build/` will
    silently shadow the `build/build-*.py` builder pattern CLAUDE.md prescribes for Phase 2. Should
    become an intake item rather than being rediscovered at 2.1.

---

## 7. Files to touch (checklist)

**Create — backend**
- [ ] `src/rpg_api/__init__.py` — docstring mirroring the core's from the API side; re-export `create_app`
- [ ] `src/rpg_api/app.py` — the injectable factory
- [ ] `src/rpg_api/health.py` — `GET /health`, version from `rpg_core.__version__`
- [ ] `src/rpg_api/spa.py` — JSON-404 guard, traversal-safe resolve, history fallback, 503
- [ ] `src/rpg_api/serve.py` — `main()`, the `rpg-serve` target

**Create — tests**
- [ ] `tests/conftest.py` · `tests/test_api_health.py` · `tests/test_api_spa.py`
- [ ] `tests/test_layering.py` · `tests/test_ci_contexts.py` · `tests/test_packaging.py`

**Create — frontend**
- [ ] `app/package.json` (no `author`) · `app/package-lock.json` (commit it)
- [ ] `app/tsconfig.json` · `app/tsconfig.negative.json` (**`"exclude": []`**) · `app/typecheck-fixtures/bad.ts`
- [ ] `app/scripts/check-negative.mjs` · `app/eslint.config.js` · `app/vite.config.ts`
- [ ] `app/index.html` · `app/public/favicon.svg` · `app/src/main.tsx` · `app/src/App.tsx`
- [ ] `app/src/api/client.ts` · `app/src/setupTests.ts` · `app/src/App.test.tsx`
- [ ] `.editorconfig` (repo root; must agree with `.gitattributes`)

**Edit**
- [ ] `pyproject.toml` — deps, dev group, hatch packages, `[project.scripts]`; `[tool.mypy]` **unchanged**
- [ ] `uv.lock` — regenerate, same commit
- [ ] `.github/workflows/ci.yml` — `--cov=rpg_api`; the `Web app` job; the smoke step
- [ ] `ops/branch-protection.json` — contexts, **same commit as the workflow**
- [ ] `.github/dependabot.yml` — npm entry; delete the line-30 placeholder
- [ ] `tests/test_repo_structure.py` — app-ignore guard; Documentation section
- [ ] `tests/test_no_leaks.py` — **one docstring line only**
- [ ] `ops/README.md` · `README.md` · `CLAUDE.md` · `ROADMAP.md` (line 156 prose; **Size cell stays `M`**)

**Artifacts**
- [ ] `requests/feature-requests/1.1-app-shell/reviews/preflight.md` — Phase 0's only tracked deliverable
- [ ] `requests/feature-requests/README.md` — Index Stage cell. **Advances to `planned` when this plan
      lands (stage 3, now), and to `implemented` in stage 4's commit — not during implementation.**

---

## 8. Conventions (bake these in)

- **Work on a branch, land through a PR.** `main` is protected. **The branch already exists:
  `phase1/app-shell`** — confirm it, never `git switch -c` a duplicate.
- **Agents commit only through `/commit`** — never `git commit` ad hoc, not for a one-line change.
  Every phase ends at a `/commit` checkpoint. It stages by path, never `git add -A`, pushes the feature
  branch, and never opens the PR, pushes `main`, force-pushes, or amends.
- **Subagents get read-only git.** No `checkout`/`reset`/`restore`/`clean`/`stash`. The push and prune
  allowances are the main agent's alone, and prune requires the content-equality check
  (`git diff <branch> origin/main --stat` empty) because PRs land as squash merges and `-d` refuses
  every already-merged branch here.
- **Anything outward-facing is user-run.** `gh api -X PUT` is structurally impossible for an agent, and
  editing the protection file alone never changes GitHub. The merge is yours.
- **The repo is public** — no machine-specific absolute paths, account ids, tokens, or personal
  identifiers in tracked files. The dist default resolves relative to the repo root; `app/package.json`
  carries no `author` email. `ALLOWED` with a written reason is the **only** sanctioned escape hatch —
  never a weakened regex, never a removed suffix.
- **Resolve by name, never a literal path.** There is no `datasets/manifest.json` yet, so this item
  expresses the convention in its pre-dataset form: the consumer never hardcodes a location, it
  **receives** one — `create_app(spa_dist=...)`. The next ten items copy whatever this one does, so
  **the injection point is the convention.**
- **Do not create domain or data surface speculatively.** `careers/`, `datasets/`, `rulesets/`, `lib/`
  do not exist and this item creates none of them. ADR 0003's append-only ledger, ADR 0004's immutable
  pinned rulesets, and ADR 0008's the-build-prices-but-never-scores have **zero surface here** — the
  plan's job is to make sure this item doesn't accidentally create that surface. Decision 6's standing
  rule is the operative rail: **the health payload gains a field only when the thing it reports
  exists.**
- **`careers/**/events.jsonl` is tracked** — the one inverted convention. This item adds ignore rules
  for `app/dist/` and `node_modules/` and **must not disturb that carve-out block**.
- **`var/` holds only regenerable things.** Phase 0's probes live under `var/spike/` and nothing there
  is ever staged.
- **Label your epistemics.** *Measured / verified / inferred / assumed / unconfirmed* mean different
  things, and an unconfirmed claim is a task. This plan states which of its own claims are measured
  (node/npm versions, gitleaks absence, the remote, both ports) versus still unconfirmed (the protection
  API accepting the JSON; the setup-node action major).
- **Every roadmap item is a request**, and its Status is maintained by `/commit` against the diff —
  never edited ad hoc. The one hand edit this plan sanctions is line 156's stale trailing **prose**,
  which `/commit`'s Step-4 mandate does not cover, and it rides in the same commit. **The Size cell
  stays `M`.**
- **Don't re-litigate the nine ADRs or answer `[OPEN-N]` ad hoc.** This item engages none: ADR 0002 is
  cited only to explain why `pydantic` stays out of the layering deny-list, and Decision 3 deliberately
  chose a guard test over a tenth ADR.
- **Consume the scope; do not re-open it.** Fit, goals, non-goals, and acceptance were decided at
  stage 2.

---

## 10. Code-grounding verification

Two code-grounded adversaries and one meta-audit read the repo and checked every cited reference.
**45 findings — 3 blockers, 13 majors.** I independently spot-checked seven citations; six resolved
exactly as claimed, and the two the meta-audit flagged as wrong I confirmed wrong.

| Cited reference | Verdict |
|---|---|
| Plan's `git switch -c 1.1-app-shell` | **CORRECTED** — the branch already exists as `phase1/app-shell` with both artifact commits. Replaced with a state check; propagated to Phase 7's prune command. |
| Plan's "Phase 5 CI is green on the pushed branch" | **CORRECTED** — `ci.yml:3-7` gives a feature branch no push trigger. Added a draft-PR user action at Phase 1 and split Phase 5b. |
| `tests/test_no_leaks.py:41` for `.json` | **CORRECTED** → line **42**; line 41 is `.toml`. Verified by reading. |
| `ROADMAP.md:166-175` = "eleven rows" | **CORRECTED** → **ten** rows (1.2–1.11). Verified: 165 is 1.1, 166 is 1.2, 175 is 1.11. |
| `app/tsconfig.negative.json` extend-and-narrow | **CORRECTED** — a child inherits the parent's `exclude`; without `"exclude": []` the project resolves zero files and AC 11 false-greens on TS18003. |
| AC 19 marked USER-RUN | **CORRECTED** — the scope marks exactly four (20–23). Moved to Phase 6, agent-provable. |
| Status token `plan` | **CORRECTED** → `planned`, per `requests/feature-requests/README.md:100`. Overrides the skill template. |
| Vitest `globals: false` + bare jest-dom import | **CORRECTED** — matchers never register and RTL cleanup never installs. Pinned the exact `setupTests.ts`. |
| `.claude/settings.json:32-35` allow `gh run list`/`gh run view` | **VERIFIED** by reading — the agent can watch its own CI; `gh api *` at line 8 stays yours. |
| `DESIGN.md:99` §3, line 106 "Two packages, one repo" | **VERIFIED** by reading. |
| `.gitignore` 62 `dist/`, 63 `build/`, 66 `node_modules/`, 68 `app/dist/` | **VERIFIED** by reading. |
| `src/rpg_core/__init__.py` 16 lines, direction at 3–6 | **VERIFIED** by reading. |
| `ops/README.md:12` owner/repo `jordan-koch/nba2k-rpg` | **VERIFIED** against `git remote -v`. |
| `pyproject.toml` 9 / 11–13 / 30–31 / 61–65 / 73 | **VERIFIED** by reading. |
| Ports 8000, 5173 free | **MEASURED** 2026-08-14. |
| `actions/setup-node` current major | **UNCONFIRMED** — needs network. Confirm before Phase 5 commits (Decision E). |

**Findings judged overstated and not applied:** the gitleaks/`package-lock.json` exposure is recorded
as risk 5 with its medium confidence stated rather than treated as established — and you resolved it by
installing gitleaks anyway (Decision B), which closes it by measurement.

---

## References

- [`PROJECT_SCOPE.md`](PROJECT_SCOPE.md) — the decided contract, 23 acceptance criteria
- [`FEATURE_REQUEST.md`](FEATURE_REQUEST.md) — intake (its `app/` claim about CLAUDE.md is false)
- [`reviews/plan-proposals.md`](reviews/plan-proposals.md) — the three planner lenses, verbatim
- [`reviews/plan-adversarial.md`](reviews/plan-adversarial.md) — 45 adversary + 18 meta-audit findings
- [`reviews/scope-proposals.md`](reviews/scope-proposals.md) · [`reviews/scope-adversarial.md`](reviews/scope-adversarial.md) — stage 2's trail
- [`ROADMAP.md`](../../../ROADMAP.md) · [`DESIGN.md`](../../../DESIGN.md) · [`CLAUDE.md`](../../../CLAUDE.md) · [`ops/README.md`](../../../ops/README.md)
- [ADR 0002](../../../docs/decisions/0002-manual-ingestion-dto-boundary.md) — why `pydantic` stays out of the deny-list

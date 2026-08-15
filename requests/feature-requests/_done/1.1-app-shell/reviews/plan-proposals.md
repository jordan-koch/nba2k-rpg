# Plan Panel - Raw Proposals

> Provenance trail for `/create-implementation-plan` on `1.1-app-shell`, run 2026-08-14.
> Panel health: 3/3 planners, 2/2 adversaries, 1/1 meta-audit, no degraded lenses.
>
> Three mechanical edits, applied so this file can be tracked in a public repo:
> absolute repo paths are rewritten repo-relative and local user paths redacted
> (tests/test_no_leaks.py blocks drive-letter paths outright); placeholder emails
> become `<email-redacted>`; and any passage quoting a markdown link to a
> not-yet-existing path is wrapped in a fenced block, the exemption
> tests/test_request_links.py documents. Text is otherwise verbatim.

Verbatim output of the three divergent planner lenses, before the merge stage
converged them. Kept unfiltered: what was proposed and cut is as informative
as what survived.

---

## Lens: `code-grounded`

### ok

true

### onboarding_files

{
    "path":  "requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md",
    "why":  "The decided upstream artifact. 23 numbered Acceptance Criteria (lines 147-258), 10 Decisions (502-516), 15 Risks (377-445), the Affected Area pointer list (447-500). CONSUME it — fit, goals, non-goals and ACs are settled. Read its Authoring rule (lines 5-18) FIRST: it binds how you write every .md under requests/."
}

{
    "path":  "requests/feature-requests/1.1-app-shell/FEATURE_REQUEST.md",
    "why":  "Context only. Its nine Open Questions (174-208) are all disposed by the scope. NOTE its Rough-Ideas claim that CLAUDE.md\u0027s project map lists serving under app/ is verified FALSE (grep for `app/` in CLAUDE.md returns nothing) — do not inherit that reasoning."
}

{
    "path":  "pyproject.toml",
    "why":  "Every backend config this item edits: line 9 empty `dependencies`, 11-13 the FastAPI reservation comment to delete, 15-21 the dev group, 30-31 the hatch wheel `packages` list, 61-65 `[tool.mypy]` (strict, warn_unreachable, files=[\"src\",\"tests\"]) which must NOT be relaxed, 68-74 pytest ini with `pythonpath = [\"src\"]`."
}

{
    "path":  ".github/workflows/ci.yml",
    "why":  "Two jobs today. Line 19 `name: Lint, types, tests`, 34 `uv sync --locked`, 47 `--cov=rpg_core`, 50 `name: Secret scan`, 10-12 `concurrency: cancel-in-progress: true`, 53-56 gitleaks with `fetch-depth: 0`. The third job goes alongside; line 47 gains `--cov=rpg_api`."
}

{
    "path":  "ops/branch-protection.json",
    "why":  "Line 4 is the exact contexts array: [\"Lint, types, tests\", \"Secret scan\"] — CI job DISPLAY names. The new job\u0027s name joins it in the same commit as the workflow change, and the file is inert on GitHub until the user re-applies it."
}

{
    "path":  "ops/README.md",
    "why":  "Line 12 the `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection` command (verified to match `git remote -v`), 21-24 the job-rename warning this item generalizes to job addition, 32-62 the uv section the Node section sits beside, 64-73 the \u0027same four commands CI runs\u0027 block."
}

{
    "path":  "tests/test_repo_structure.py",
    "why":  "The guard idiom to copy verbatim. `_git_check_ignore` 24-34 (works on paths that do not exist — why the app-ignore guard can be written before app/ does), `test_package_version_matches_pyproject` 46-54 (transitively pins the health payload\u0027s version), `test_scratch_root_is_gitignored` 83-92 as the template, ADR tests 113-133. AC 17\u0027s doc-agreement tests are added here."
}

{
    "path":  "tests/test_no_leaks.py",
    "why":  "A blocking public-repo gate that will now scan frontend files. ALLOWED at 32-35 is the only sanctioned escape hatch. TEXT_SUFFIXES at 38-55 already contains .json/.ts/.tsx/.js/.mjs/.css/.html, so app/package.json, app/package-lock.json, app/tsconfig.json and app/vite.config.ts all become scanned. Line 37\u0027s docstring becomes false and this item fixes it."
}

{
    "path":  "tests/test_request_links.py",
    "why":  "Read FENCED_BLOCK at line 26 and _dead_links at 40-64 before writing ANY .md under requests/. Only 3+ backtick fences are stripped; inline backticks are NOT exempt, and a markdown link to a path this item creates turns CI red on the very PR that lands it."
}

{
    "path":  "src/rpg_core/__init__.py",
    "why":  "The entire domain core today — a 12-line docstring plus `__version__ = \"0.1.0\"` at line 16. Lines 3-6 state the dependency direction from the core\u0027s side. This file is UNCHANGED when the item lands."
}

{
    "path":  "DESIGN.md",
    "why":  "Lines 106-109, \u0027Two packages, one repo. src/rpg_core/ is the I/O-free domain; the API and web app depend on it and it depends on neither.\u0027 The layering guard\u0027s failure message cites this section by name (Decision 3: a guard test instead of an ADR)."
}

{
    "path":  ".gitignore",
    "why":  "Lines 66-68 the Node block reserved in Phase 0, and 62-63 the blanket `dist/`/`build/` rules — `dist/` at 62 ALREADY ignores app/dist/ independently of 68, which the ignore guard must not be fooled by. Lines 35-49 are the careers carve-out; do not disturb it."
}

{
    "path":  ".gitattributes",
    "why":  "Line 3 `* text=auto eol=lf` (npm-generated files normalize to LF), lines 20-25 the already-present *.ts/*.tsx/*.css/*.html entries, line 35 `*.ico binary`, line 41 `package-lock.json linguist-generated=true -diff`. Phase 0 reserved all of it by name."
}

{
    "path":  ".github/dependabot.yml",
    "why":  "Lines 16-28 the uv entry whose monthly + patch-ignore posture the npm entry mirrors; line 30 the placeholder comment `# npm arrives with Phase 1 item 1.1 (app-shell).` this item discharges."
}

{
    "path":  ".claude/settings.json",
    "why":  "Lines 3-12 the `ask` list — git commit/push/merge and `gh api *` all require the user, which is why AC 23 is USER-RUN. Lines 13-17 confirm `PowerShell(node *)` and `PowerShell(npm *)` are already allowed, so the frontend work needs no permission changes."
}

{
    "path":  "requests/feature-requests/README.md",
    "why":  "The pipeline contract. Lines 57-73 define \u0027testable\u0027 (one command, pass or fail) and the USER-RUN rule; 96-100 the status blockquote grammar; line 106 the Index row whose Stage cell advances to `plan`."
}

{
    "path":  "CLAUDE.md",
    "why":  "Lines 20-21 the Status section (\u0027no application code yet\u0027), 49-63 the project map fenced block that gains app/ and src/rpg_api/, line 66 \u0027and the web app don\u0027t exist yet\u0027 — AC 17\u0027s target surface. 158 lines total: this is an edit, not an append."
}

{
    "path":  "README.md",
    "why":  "Line 12 the `**No application code yet.**` banner AC 17 asserts is gone, 53-69 the project map block, 71-72 \u0027and the web app don\u0027t exist yet\u0027, 74-83 the Setup block that gains the Node steps and both run commands."
}

{
    "path":  "ROADMAP.md",
    "why":  "Line 165 is row 1.1 (M, needs 0.3, IN-PROGRESS) — advanced by /commit against the diff, never hand-edited. Line 156 still says \u00271.1 app-shell is at intake\u0027, already stale. Lines 121-123 the ★/Status legend."
}

### architecture_notes

CURRENT STRUCTURE (verified by reading, 2026-08-14)

The repo is a Phase-0 harness with exactly one source package and zero runtime dependencies.

  src/rpg_core/__init__.py   — 17 lines total: a docstring (1-12) declaring the package
                               "I/O-free and web-free", `from __future__ import annotations`,
                               and `__version__ = "0.1.0"` at line 16. Nothing else. No py.typed.
  tests/                     — three files, NO conftest.py: test_repo_structure.py,
                               test_no_leaks.py, test_request_links.py (plus tests/fixtures/).
  pyproject.toml             — `dependencies = []` (9); dev group pytest/pytest-cov/ruff/mypy
                               (15-21); hatch wheel `packages = ["src/rpg_core"]` (31); mypy
                               strict + warn_unreachable + files=["src","tests"] (61-65); pytest
                               `pythonpath = ["src"]` (73).
  .github/workflows/ci.yml   — two jobs: `python` (display name "Lint, types, tests", line 19)
                               and `secrets` ("Secret scan", line 50). Line 47 runs
                               `uv run pytest -m "not network" --cov=rpg_core --cov-report=term-missing`.
  ops/branch-protection.json — line 4: contexts == ["Lint, types, tests", "Secret scan"].

There is no `app/`, no `src/rpg_api/`, no `tests/conftest.py`, no `datasets/manifest.json`, no
`careers/`, no `rulesets/`. Phase 0 RESERVED the frontend conventions by name in five tracked
files without creating anything: .gitignore 66-68, .gitattributes 41, dependabot.yml line 30,
pyproject.toml 11-13, and .claude/settings.json's node/npm allow entries.

THE SEAMS THIS CHANGE HOOKS INTO — five, all pre-cut by Phase 0

  1. PACKAGE SEAM. `[tool.mypy] files = ["src","tests"]` (pyproject.toml:65) and
     `[tool.pytest.ini_options] pythonpath = ["src"]` (73) both already reach any directory under
     src/. Putting the API at `src/rpg_api/` therefore costs ZERO config churn on type-checking
     and test imports. The two places that are NOT automatic are
     `[tool.hatch.build.targets.wheel].packages` (31) and ci.yml's `--cov=rpg_core` (47) — which
     is exactly why the scope demands a structural test for both (AC 14): omitting the hatch entry
     passes every local test (pythonpath covers it) and fails only with ModuleNotFoundError on an
     installed environment.

  2. DEPENDENCY-DIRECTION SEAM. DESIGN.md:106-109 and src/rpg_core/__init__.py:3-6 assert the same
     rule from both sides in prose. The health payload's `version` field is the item's one honest
     reason for rpg_api to import rpg_core, exercising the arrow in the allowed direction; the
     layering guard forbids the reverse. The arrow is already pinned on the VALUE side:
     tests/test_repo_structure.py:46-54 asserts `rpg_core.__version__ == pyproject["project"]
     ["version"]`, so a health test asserting `body["version"] == rpg_core.__version__` inherits
     that pin for free.

  3. CI-CONTEXT SEAM. ops/branch-protection.json:4 lists job DISPLAY names, and ops/README.md:21-24
     warns in prose that renaming a job silently breaks it. Prose does not fail a build. The new
     guard closes exactly the tracked half (set equality between ci.yml `jobs.*.name` and the
     contexts array). The applied half — GitHub only learns of a context when the user re-runs
     `gh api -X PUT` — cannot be closed by any test, which is why AC 23 is an ORDERED user-run
     gate that must complete BEFORE merge.

  4. IGNORE SEAM. .gitignore:66-68 already ignores node_modules/, .vite/, app/dist/ — and line 62's
     blanket `dist/` covers app/dist/ a second time. tests/test_repo_structure.py:24-34
     `_git_check_ignore` shells `git check-ignore -q --no-index`, which works on paths that do not
     exist, so the guard can be written before app/ does. The assertion that actually matters is
     the NEGATIVE one: `app/src/main.tsx` must NOT be ignored, i.e. nobody may later add an
     over-broad rule that swallows the SPA source.

  5. LEAK SEAM. tests/test_no_leaks.py:58-71 scans `git ls-files` filtered by TEXT_SUFFIXES (38-55).
     .json, .ts, .tsx, .js, .mjs, .css, .html are all in that set, so app/package.json,
     app/package-lock.json, app/tsconfig.json and app/vite.config.ts become scanned the moment they
     are tracked. Two concrete tripwires: an `author` field carrying an email fails EMAIL (line 29),
     and any Windows-generated absolute path fails WINDOWS_PATH (26). Run it BEFORE staging the lock.

TARGET STRUCTURE — the shape the item leaves behind

  src/rpg_api/
    __init__.py    docstring stating the direction (mirrors rpg_core's); re-exports create_app
    app.py         `create_app(spa_dist: Path | None = None) -> FastAPI` — the injectable factory
    health.py      APIRouter carrying GET /health, included under prefix "/api"
    spa.py         `attach_spa(app, dist)` — index route, history fallback, /api JSON-404 guard,
                   missing-build 503. No StaticFiles mount (see below).
    serve.py       `main() -> None` — the [project.scripts] console entrypoint; uvicorn.run

  app/             Vite + React + TypeScript SPA, one page, ALL config scoped inside app/

  tests/
    conftest.py         app/client factories parameterized on the injectable dist
    test_api_health.py  ACs 2, 7
    test_api_spa.py     ACs 5, 6 + history fallback + a path-traversal guard
    test_layering.py    AC 3 — pure function + tmp_path red/green + the real assertion
    test_ci_contexts.py AC 4 — yaml.safe_load, set equality, negative step-name assertion
    test_packaging.py   AC 14 — hatch packages + the --cov flag

THE ONE NON-OBVIOUS DESIGN CALL: no StaticFiles mount.

The obvious implementation — `app.mount("/", StaticFiles(directory=dist, html=True))` — fails two
of the scope's criteria at once, and both failures are named in the scope's own risks.
(a) Starlette's StaticFiles raises at CONSTRUCTION when the directory is absent (scope risk 7,
labeled inferred), so a fresh clone with no app/dist/ gets an import-time traceback instead of an
app — AC 5 forbids that. (b) A mount at "/" registered last still matches `/api/unknown`, and
StaticFiles answers with a non-JSON 404 — AC 7 forbids that.

So spa.py hand-rolls it, and the branch is decided PER REQUEST rather than at construction:

  * `GET /{full_path:path}` is registered LAST, after the /api router.
  * If `full_path == "api"` or `full_path.startswith("api/")` -> raise HTTPException(404).
    FastAPI's default handler renders that as application/json, satisfying AC 7 directly.
  * Else resolve `candidate = (dist / full_path).resolve()`; serve FileResponse only if it
    `is_file()` AND is inside `dist.resolve()` — a real path-traversal guard.
  * Else fall back to `dist / "index.html"` -> FileResponse. That is the SPA history fallback
    that stops item 1.10's router from being a breaking change.
  * If index.html does not exist -> PlainTextResponse(status_code=503) whose body contains the
    literal `npm run build`.

Deciding per request has a payoff the scope did not name: building the SPA while uvicorn runs makes
`/` start working and `spa_built` flip true in the same instant, instead of the two disagreeing
until a restart. `spa_built` in the health payload is computed the same way,
`(dist / "index.html").is_file()`, at request time.

Because the factory takes `spa_dist` as an argument, both branches are unit-testable against
tmp_path with no listening socket and no source mutation — which is what makes ACs 5 and 6
cold-runnable. `create_app()` with no argument resolves the default (repo root walked up from
`Path(__file__).resolve()`, then `app/dist`), exercised only by the console script and the CI
smoke step, never by a unit test.

### phases

{
    "name":  "Phase 1 — Backend dependencies, the rpg_api package, and GET /api/health",
    "goal":  "Land the HTTP seam and all Python dependency bookkeeping in one commit, so `uv sync --locked` is green from a clean checkout and rpg_api imports rpg_core in the one allowed direction. Scope Goals 1, 3 (half), 6.",
    "steps":  [
                  "Edit pyproject.toml line 9: replace `dependencies = []` with fastapi + uvicorn, and DELETE the discharged reservation comment at lines 11-13. Take the version floors from what `uv lock` actually resolves — do not commit a floor nobody has seen resolve.",
                  "Edit the dev group (lines 15-21): add `httpx` (starlette\u0027s TestClient requires it — without it `fastapi.testclient.TestClient` raises at import), `pyyaml` + `types-PyYAML` (AC 4\u0027s parser plus the stubs mypy strict needs), and `watchfiles` (for uvicorn --reload, chosen over `uvicorn[standard]` per the scope\u0027s Core list).",
                  "Edit pyproject.toml line 31: `packages = [\"src/rpg_core\", \"src/rpg_api\"]`. This is the line that fails only at runtime if forgotten (scope risk 2).",
                  "Add a `[project.scripts]` table with ONE entry — proposed `nba2k-rpg-serve = \"rpg_api.serve:main\"` (name is an open question). Decision 9\u0027s caveat binds: this becomes the only documented way to run the served build.",
                  "Run `uv lock`, then `uv sync --locked`. Commit uv.lock in this same commit — ops/README.md lines 54-57 make that a hard rule and ci.yml:34 hard-fails on a stale lock.",
                  "Edit .github/workflows/ci.yml line 47 to `--cov=rpg_core --cov=rpg_api` (scope risk 11). A one-line change independent of the new job, so it lands here rather than in Phase 5.",
                  "Create src/rpg_api/__init__.py: a docstring mirroring src/rpg_core/__init__.py lines 3-6 from the API side, `from __future__ import annotations`, and a re-export of create_app.",
                  "Create src/rpg_api/health.py: `router = APIRouter()` with a fully annotated `GET /health` handler returning a pydantic `Health` model (`status: str`, `version: str`, `spa_built: bool`). Read the version as `rpg_core.__version__`, never re-typed, so tests/test_repo_structure.py:46-54\u0027s pin covers the payload transitively. Pass the resolved dist to the handler via a dependency or `request.app.state` — whichever keeps mypy strict green with no ignore.",
                  "Create src/rpg_api/app.py with `def create_app(spa_dist: Path | None = None) -\u003e FastAPI`: resolve the default dist from the repo root (derived from `Path(__file__).resolve()`, never a literal path), store it, `include_router(health.router, prefix=\"/api\")`, and — in Phase 2 — call attach_spa LAST. Every handler and helper carries a return annotation (scope risk 6).",
                  "Create src/rpg_api/serve.py with `def main() -\u003e None` calling `uvicorn.run(\"rpg_api.app:create_app\", factory=True, host=\"127.0.0.1\", port=8000)`. IPv4 literal, matching the Vite proxy target (scope risk 9).",
                  "Create tests/conftest.py with three fixtures, parameterized on the injectable dist as the scope\u0027s fold-in requires: `client_factory` returning `Callable[[Path], TestClient]`; `client` over a dist path that does NOT exist (the fresh-clone state every cold agent hits first); and `built_spa_dist(tmp_path)` writing a known index.html plus assets/app.js. Fully annotated — mypy strict covers tests/.",
                  "Create tests/test_api_health.py for AC 2: status 200, content-type application/json, `body[\"status\"] == \"ok\"`, `body[\"version\"] == rpg_core.__version__`, `isinstance(body[\"spa_built\"], bool)`. No live server, no socket.",
                  "Create tests/test_packaging.py for AC 14: tomllib-load pyproject and assert the hatch wheel packages list contains both src/rpg_core and src/rpg_api; then yaml.safe_load ci.yml, find the python job\u0027s step named \u0027Pytest\u0027, and assert `--cov=rpg_api` appears in its `run` string. Give both a message explaining the runtime-only failure they prevent."
              ],
    "acceptance":  [
                       "`uv sync --locked` exits 0 from a clean checkout with fastapi and uvicorn resolved in the tracked uv.lock (AC 1)",
                       "`uv run pytest -m \"not network\"` is green, including the TestClient health test asserting 200 / application/json / status ok / version == rpg_core.__version__ / spa_built is a bool (AC 2)",
                       "`uv run mypy` exits 0 with src/rpg_api present under the UNCHANGED [tool.mypy] block, zero new `# type: ignore`, zero new per-module overrides (AC 8)",
                       "`uv run ruff check` and `uv run ruff format --check` exit 0 over src/rpg_api and every new test file (AC 9)",
                       "`uv run pytest tests/test_packaging.py` is green — hatch packages contains src/rpg_api and the Pytest step names rpg_api in --cov (AC 14)",
                       "`uv run pytest tests/test_repo_structure.py tests/test_request_links.py` still green (AC 16)"
                   ],
    "commit_note":  "feat(api): FastAPI app shell with GET /api/health. Adds fastapi+uvicorn to [project].dependencies with uv.lock regenerated, httpx/pyyaml/types-PyYAML/watchfiles to the dev group, src/rpg_api to the hatch wheel packages list, a [project].scripts entrypoint, and --cov=rpg_api to CI. Discharges the pyproject.toml reservation comment. src/rpg_core is untouched."
}

{
    "name":  "Phase 2 — SPA serving: both branches, the history fallback, and the JSON /api 404",
    "goal":  "Make the backend able to serve a built SPA and to fail legibly when there is no build — both branches unit-testable against tmp_path with no listening socket, and no import-time traceback on a fresh clone. Scope Goal 4 (backend half).",
    "steps":  [
                  "Create src/rpg_api/spa.py with `def attach_spa(app: FastAPI, dist: Path) -\u003e None` registering ONE catch-all `@app.get(\"/{full_path:path}\")`. Registration order is load-bearing: it must run AFTER `include_router(..., prefix=\"/api\")` in create_app, or it shadows the health route.",
                  "Inside the handler, in this order: (1) if `full_path == \"api\" or full_path.startswith(\"api/\")` -\u003e `raise HTTPException(status_code=404)`, which FastAPI renders as application/json — that IS AC 7, and it is what stops the history fallback swallowing API 404s. (2) resolve `candidate = (dist / full_path).resolve()`; return `FileResponse(candidate)` only if `candidate.is_file()` AND `candidate.is_relative_to(dist.resolve())`. (3) else `index = dist / \"index.html\"`; if `index.is_file()` -\u003e FileResponse(index); else -\u003e PlainTextResponse(status_code=503) whose body contains the literal `npm run build`.",
                  "Do NOT use StaticFiles. Leave a comment in spa.py recording both reasons — it raises at construction on a missing directory (scope risk 7) and a mount at / answers unknown /api paths with a non-JSON 404 (AC 7). A future agent will otherwise \u0027simplify\u0027 this straight back into two bugs.",
                  "Wire `attach_spa(app, dist)` as the LAST statement of create_app, and make the health payload\u0027s `spa_built` read `(dist / \"index.html\").is_file()` at request time so the two answers can never disagree.",
                  "Create tests/test_api_spa.py: (a) AC 5 — `client_factory(tmp_path / \"does-not-exist\")`: construction raises nothing, GET /api/health is 200, GET / is 503, `\"npm run build\" in response.text`. (b) AC 6 — over the built_spa_dist fixture: GET / is 200, content-type starts with text/html, body equals the fixture file\u0027s bytes. (c) history fallback — GET /careers/anything over a built dist returns index.html\u0027s bytes. (d) AC 7 — GET /api/nope is 404 with content-type application/json, asserted on BOTH branches. (e) traversal — a path escaping the dist root does not return a file from outside it.",
                  "Run all four Python commands. Fix any mypy strict friction by ANNOTATING, never by adding an ignore or a per-module override — AC 8 explicitly fails a green run achieved by loosening strict."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_api_spa.py` is green: with the dist pointed at a nonexistent tmp_path, constructing the app raises nothing, /api/health is 200, and GET / is 503 containing the literal build command (AC 5)",
                       "With the dist pointed at a tmp_path containing a known index.html, GET / is 200, text/html, and returns that file\u0027s bytes (AC 6)",
                       "GET on an unknown path under /api returns 404 with content-type application/json, not HTML — proven on both the built and unbuilt branches (AC 7)",
                       "A traversal attempt cannot return a file from outside the dist root",
                       "All four commands green: `uv run ruff check`, `uv run ruff format --check`, `uv run mypy`, `uv run pytest -m \"not network\"` (ACs 8, 9)"
                   ],
    "commit_note":  "feat(api): serve the built SPA with an injectable dist path. Adds the history fallback for unmatched non-/api paths, a JSON 404 guard so API misses never return HTML, a traversal-safe file resolve, and a 503 naming `npm run build` when no build exists. Deliberately not StaticFiles — reason recorded in spa.py."
}

{
    "name":  "Phase 3 — The three structural guards",
    "goal":  "Leave behind the conventions that protect the next eleven items: the domain core stays web-free, CI job names and required contexts cannot drift apart, and nobody later ignores the SPA source. Scope Goal 3 (enforcement half).",
    "steps":  [
                  "Create tests/test_layering.py with a PURE function `web_imports_under(root: Path) -\u003e list[tuple[str, str]]` returning (relative file, offending module) pairs. Parse each `root.rglob(\"*.py\")` with `ast.parse` and walk `ast.Import`/`ast.ImportFrom` — AST, not regex, so a docstring mentioning fastapi does not trip it. Guard `ast.ImportFrom` where `node.module is None` (a relative import). Deny-list: fastapi, starlette, uvicorn, rpg_api; compare the FIRST dotted segment. `pydantic` is deliberately ABSENT — ADR 0002 makes that item 1.2\u0027s call.",
                  "Unit-test the function twice against tmp_path (AC 3, no source mutation): a fake module containing `import fastapi` reports exactly that one file; a clean tree reports none. Then the real assertion: `web_imports_under(REPO_ROOT / \"src\" / \"rpg_core\")` is empty, with a failure message naming DESIGN.md §3 verbatim — Decision 3 makes this test the record instead of an ADR, so the citation IS the record.",
                  "Create tests/test_ci_contexts.py (AC 4). yaml.safe_load .github/workflows/ci.yml; collect `{job.get(\"name\", key) for key, job in doc[\"jobs\"].items()}` — the `.get` fallback matters because a job may legally omit `name`, in which case the key is the display name. Load ops/branch-protection.json and take required_status_checks[\"contexts\"]. Assert SET EQUALITY, not containment: containment passes while a typo\u0027d context hangs every PR forever on a check that never reports. Compute `only_in_ci` and `only_in_protection` separately so the message names which side carries the extra.",
                  "Add AC 4\u0027s negative assertion in the same file: a step-level name (\"Gitleaks\" from ci.yml:58, \"Install\" from line 30, \"Mypy\" from line 42) is NOT in the collected job-name set — proving the parser is structure-aware rather than grepping for quoted strings.",
                  "Add the ignore guard to tests/test_repo_structure.py, reusing `_git_check_ignore` (24-34) exactly as test_scratch_root_is_gitignored (83-92) does: `app/dist/index.html` and `app/node_modules/react/index.js` ARE ignored, and — the assertion that actually protects anything — `app/src/main.tsx` is NOT. Note in the docstring that app/dist/ is covered twice (.gitignore line 62\u0027s blanket `dist/` and line 68), so a passing test does not prove line 68 still exists."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_layering.py` is green: the fake tmp_path module importing fastapi is reported, a clean tmp_path tree reports nothing, and src/rpg_core reports zero — all in one run, with no tracked source mutated (AC 3)",
                       "`uv run pytest tests/test_ci_contexts.py` is green with today\u0027s two jobs and two contexts, and the negative assertion proves step-level names never enter the job-name set (AC 4)",
                       "Deliberately mutating a job\u0027s display name in a scratch copy makes test_ci_contexts fail with a message naming which side has the extra entry",
                       "`uv run pytest tests/test_repo_structure.py` is green including the new app-ignore guard — app/dist/ and app/node_modules/ ignored, app/src/main.tsx not (AC 16)",
                       "`uv run mypy` and `uv run ruff check` green over all three new/edited test files"
                   ],
    "commit_note":  "test: structural guards for the two-package layout. Adds an AST-based layering guard (src/rpg_core imports no web framework, failure message cites DESIGN.md §3), a set-equality guard tying CI job display names to ops/branch-protection.json contexts, and an app/ ignore guard asserting the SPA source is never shadowed."
}

{
    "name":  "Phase 4 — The SPA under app/",
    "goal":  "One React + TypeScript page that fetches the health endpoint across a real network boundary, with TypeScript strictness proven rather than assumed, a linter, and two Vitest tests. Scope Goals 2 and 5 (local half).",
    "steps":  [
                  "Create app/package.json: `private: true`, `type: module`, `version: \"0.0.0\"` as a deliberate placeholder (the version-parity proposal was dropped — a private SPA\u0027s version means nothing). NO `author` field: an email there fails tests/test_no_leaks.py:29 (scope risk 4).",
                  "Scripts — every one a SINGLE command, no shell operators, because Windows PowerShell 5.1 has no `\u0026\u0026` at all (scope risk 8): dev=`vite`, build=`vite build`, typecheck=`tsc --noEmit -p tsconfig.json`, typecheck:negative=`tsc --noEmit -p tsconfig.negative.json`, lint=`eslint .`, test=`vitest run`. Note `vite build` does NOT typecheck (esbuild strips types) — that is exactly why typecheck is a separate script and a separate CI step.",
                  "Dependencies: react, react-dom. Dev: typescript, vite, @vitejs/plugin-react, @types/react, @types/react-dom, @types/node, vitest, jsdom, @testing-library/react, @testing-library/jest-dom, eslint, @eslint/js, typescript-eslint, eslint-plugin-react-hooks, globals.",
                  "Create app/tsconfig.json with `strict: true` PLUS the four extras Decision 7 folded in — noUncheckedIndexedAccess, noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch — along with target ES2022, module ESNext, moduleResolution bundler, jsx react-jsx, lib [ES2022, DOM, DOM.Iterable], noEmit, skipLibCheck, verbatimModuleSyntax. include [\"src\", \"vite.config.ts\"]; exclude [\"typecheck-fixtures\", \"dist\", \"node_modules\"].",
                  "Create app/typecheck-fixtures/bad.ts — AC 11\u0027s committed ill-typed fixture. Its errors must be strict-SPECIFIC: a strictNullChecks error (`function len(s?: string) { return s.length }`) and a noUncheckedIndexedAccess error (`function first(xs: string[]): string { return xs[0] }`). A plain `const n: number = \"x\"` would fail with strict OFF and prove nothing.",
                  "Create app/tsconfig.negative.json extending tsconfig.json and including only typecheck-fixtures. An npm script cannot assert its own non-zero exit, so the assertion lives in the caller: CI (Phase 5) uses `if npm run typecheck:negative; then exit 1; fi` and ops/README.md documents the PowerShell form. Do NOT add a third Vitest test for it — AC 12 pins the count at exactly two.",
                  "Create app/eslint.config.js (flat config): @eslint/js recommended + typescript-eslint recommended + eslint-plugin-react-hooks (Decision 2, against the panel\u0027s oxlint recommendation), with typecheck-fixtures and dist in `ignores`. The config MUST live inside app/, never at the repo root — a root config would immediately start reporting on the thousands of unlinted .js/.mjs lines under .claude/skills/ and force an ignore list nobody scoped (an explicit non-goal).",
                  "Create app/vite.config.ts importing defineConfig from `vitest/config` (it re-exports vite\u0027s and adds the test block, so no second config file). React plugin; `server.proxy` mapping /api to `http://127.0.0.1:8000` — the IPv4 LITERAL, because Node on Windows can resolve localhost to ::1 while uvicorn binds 127.0.0.1, producing an ECONNREFUSED that looks exactly like the backend being down (scope risk 9). test: { environment: jsdom, setupFiles: ./src/setupTests.ts, globals: false }.",
                  "Create app/index.html with a real \u003ctitle\u003e and favicon link (not the Vite template defaults), plus the favicon asset under app/public/. Prefer .svg — .gitattributes line 35 marks *.ico binary, correctly, which makes it undiffable for no benefit here.",
                  "Create app/src/api/client.ts — the typed fetch wrapper: `export interface Health { status: string; version: string; spa_built: boolean }` and an async `fetchHealth()` against the RELATIVE path /api/health. Relative is what makes both modes same-origin, which is why no CORS middleware exists anywhere and no base-URL env key exists (Decision 5). Explicitly NOT the deferred codegen contract — it is the seam codegen slots into at item 1.8.",
                  "Create app/src/App.tsx with exactly three states — loading, ok (renders status + version), unreachable. The unreachable panel MUST name the start command (AC 22): \u0027I opened the page and it\u0027s blank\u0027 is the top cold-start confusion in a two-process app. Plus app/src/main.tsx and app/src/setupTests.ts.",
                  "Create app/src/App.test.tsx with EXACTLY two tests (AC 12): the status page renders the fetched version, and the unreachable panel renders on a rejected fetch. Stub the global with `vi.stubGlobal(\"fetch\", vi.fn())` so client.ts is exercised too, rather than mocking the module and testing nothing.",
                  "Run npm install (to generate the lock), then npm ci, npm run typecheck, npm run lint, npm run test, npm run build. Confirm app/dist/index.html exists and that npm run typecheck:negative exits NON-zero.",
                  "BEFORE staging anything, run `uv run pytest tests/test_no_leaks.py` (AC 13). package-lock.json is scanned — .json is in TEXT_SUFFIXES. If a pattern trips, the fix is a narrowly-justified ALLOWED entry with a written reason, NEVER a weakened regex or a removed suffix."
              ],
    "acceptance":  [
                       "From app/: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run test`, `npm run build` each exit 0, and app/dist/index.html exists afterwards (AC 10)",
                       "`npm run typecheck:negative` exits NON-zero against the committed ill-typed fixture, and both of its errors are strict-flag-specific rather than baseline type errors (AC 11)",
                       "`npm run test` is green with exactly two Vitest tests — the status page renders the fetched version, and the unreachable panel renders on a rejected fetch (AC 12)",
                       "`uv run pytest tests/test_no_leaks.py` is green with app/package.json, app/package-lock.json, app/tsconfig.json and app/vite.config.ts tracked (AC 13)",
                       "`uv run pytest tests/test_repo_structure.py tests/test_request_links.py` still green with the new top-level directory present (AC 16)",
                       "No npm script contains `\u0026\u0026`, `rm -rf`, `cp`, or a POSIX inline env-var prefix"
                   ],
    "commit_note":  "feat(app): Vite + React + TypeScript SPA with one status page. tsconfig strict plus noUncheckedIndexedAccess/noUnusedLocals/noUnusedParameters/noFallthroughCasesInSwitch, proven by a committed ill-typed fixture and a negative typecheck script; eslint + typescript-eslint + react-hooks scoped to app/; two Vitest tests; a typed fetch wrapper with a hand-written Health interface; Vite dev proxy to 127.0.0.1 so no CORS middleware exists in either mode."
}

{
    "name":  "Phase 5 — CI: the Web app job, the required-context bookkeeping, dependabot, and the real-server smoke",
    "goal":  "Extend the repo\u0027s check posture to the new half so a red frontend turns the PR red, landing the workflow and the branch-protection change in one commit so the Phase-3 guard stays green. Scope Goal 5.",
    "steps":  [
                  "Add a third job to .github/workflows/ci.yml, parallel with python and secrets, `name: Web app`, with `defaults: { run: { working-directory: app } }`. Steps: actions/checkout@v5 (matching line 22\u0027s existing pin), setup-node pinned to major 24 (matching the measured local v24.15.0), `cache: npm` with `cache-dependency-path: app/package-lock.json`. GOTCHA: defaults.run.working-directory applies only to `run:` steps, never to `uses:` inputs, so that cache path is repo-root-relative — a wrong value does not fail, it silently disables caching, and `concurrency: cancel-in-progress` (lines 10-12) means the job re-runs on every push.",
                  "Then npm ci, npm run typecheck, the negative-typecheck step (`if npm run typecheck:negative; then echo \u0027tsconfig strictness is not engaged\u0027; exit 1; fi`), npm run lint, npm run test, npm run build, and `test -f dist/index.html`. These are exactly the steps AC 10 has the implementer run locally, so a green local run predicts a green CI run.",
                  "Add the real-server smoke step to the SAME job (Decision 8, scope risk 14) — it needs both toolchains, so add astral-sh/setup-uv@v6 (matching ci.yml:25) and `uv sync --locked` after the build, with working-directory `.`. Start the console script in the background, poll readiness with a BOUNDED loop (up to 60 one-second attempts against `curl -sf http://127.0.0.1:8000/api/health`, `exit 1` on exhaustion) — never a fixed sleep. Then assert GET / returns 200 text/html and GET /api/health returns 200 JSON containing \"status\":\"ok\". Use `set -euo pipefail`.",
                  "Edit ops/branch-protection.json line 4 to [\"Lint, types, tests\", \"Secret scan\", \"Web app\"] — IN THE SAME COMMIT as the workflow change. The Phase-3 guard fails the build if these drift, which is the point.",
                  "Edit .github/dependabot.yml: delete the line-30 placeholder comment and add an npm entry with `directory: \"/app\"`, monthly schedule, commit-message prefix `deps`, labels [dependencies], and the same semver-patch ignore block the uv entry carries at lines 26-28 (AC 15).",
                  "gitleaks (scope risk 5): the secrets job scans full history and blocks merge, and this branch adds a package-lock.json full of high-entropy base64 sha512 integrity strings. VERIFIED: gitleaks is NOT installed on this machine (`Get-Command gitleaks` fails). Either install it and run `gitleaks detect` over the tree, or record explicitly that CI\u0027s Secret scan is the gate and that remediation — if it trips — is specific fingerprints in .gitleaksignore with a written reason each, mirroring the ALLOWED-entry discipline. Do not assert it passes without running it."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_ci_contexts.py` is green at THREE contexts — if it is red, ci.yml and ops/branch-protection.json disagree and the guard is doing its job (AC 4)",
                       "`uv run pytest tests/test_packaging.py` still green with the workflow restructured (AC 14)",
                       "`.github/dependabot.yml` contains a package-ecosystem npm entry pointing at the SPA directory with the uv entry\u0027s monthly + patch-ignore posture, and the line-30 placeholder is gone (AC 15)",
                       "On the pushed branch, the `Web app` job reports and is green, and its smoke step curls both / (200, HTML) and /api/health (200, JSON) against a real uvicorn serving the real built dist (AC 18)",
                       "The smoke step uses a bounded readiness poll with an explicit exhaustion failure, not a fixed sleep",
                       "gitleaks status is recorded honestly — either a local run\u0027s result, or a written note that CI\u0027s Secret scan is the gate plus the remediation path"
                   ],
    "commit_note":  "ci: add the Web app job and make it a required check. Third job runs npm ci/typecheck/negative-typecheck/lint/test/build against pinned Node 24 with npm caching, plus a real-server smoke step booting uvicorn against the built dist behind a bounded readiness poll. ops/branch-protection.json gains the job\u0027s display name in the same commit — it stays inert on GitHub until re-applied with `gh api -X PUT`. dependabot gains the npm ecosystem entry line 30 was holding."
}

{
    "name":  "Phase 6 — Documentation, the doc-agreement guard, and hand-off",
    "goal":  "Stop the docs lying, and make that mechanically checked rather than delegated to a judgment gate. Scope Goal 7, plus the setup for the four USER-RUN criteria.",
    "steps":  [
                  "Edit ops/README.md: add a `## Node toolchain` section beside the uv one (32-62) — node 24 / npm 11 as measured, `npm ci` in app/, the npm stale-lock rule with the same sharpness lines 54-57 give the uv rule, and the PowerShell form of the negative-typecheck assertion. Add both run modes: dev (two commands, two terminals — uvicorn with reload, and `npm run dev` in app/) and served (the console script alone). Decision 9\u0027s caveat: document the console script as the ONE way to run the served build; do not also document a raw uvicorn incantation.",
                  "Edit README.md: delete the `**No application code yet.**` banner (12-13), add app/ and src/rpg_api/ to the project map fenced block (53-69), remove \u0027and the web app\u0027 from line 72, and extend the Setup block (74-83) with the Node steps and both run commands.",
                  "Edit CLAUDE.md: the Status section (20-21, \u0027no application code yet\u0027 is now false), the project map fenced block (49-63, gains app/ and src/rpg_api/), and line 66\u0027s \u0027and the web app don\u0027t exist yet\u0027. CLAUDE.md is 158 lines and has a hard budget — this is an EDIT, not an append.",
                  "Fix tests/test_no_leaks.py line 37: \u0027Binary and lockfiles are skipped.\u0027 is true of uv.lock (.lock is not in TEXT_SUFFIXES) and false of package-lock.json (.json is). This item makes it wrong, so this item fixes it — say plainly that package-lock.json IS scanned.",
                  "Add AC 17\u0027s doc-agreement tests to tests/test_repo_structure.py in a new `# ─── Documentation ───` section, in the idiom the file already uses. Assert: README.md\u0027s body does not contain \u0027no application code yet\u0027 compared LOWERCASED (README line 12 capitalizes the N, CLAUDE.md line 21 does not — a case-sensitive check silently passes on one of them); CLAUDE.md\u0027s project map contains both `app/` and `src/rpg_api/`; CLAUDE.md does not contain the substring `the web app don\u0027t exist yet`; ops/README.md contains a Node-toolchain heading and both run-mode commands.",
                  "Add a repo-root .editorconfig: root=true, LF + final newline + utf-8 globally, indent_size 4 default with 2 for {ts,tsx,js,mjs,json,css,html,yml,yaml}, and end_of_line=crlf for {ps1,psm1,bat,cmd} mirroring .gitattributes lines 7-10.",
                  "Verify AC 19 end to end: run the console script in one shell (backgrounded), curl / and /api/health from another. This proves the [project.scripts] entrypoint resolves against the installed environment — the check that would catch a missing hatch packages entry even if AC 14\u0027s test somehow did not.",
                  "Full green local run — `uv run ruff check`, `uv run ruff format --check`, `uv run mypy`, `uv run pytest -m \"not network\"`, in the order ops/README.md lines 64-73 documents — plus, from app/: npm run typecheck, npm run lint, npm run test, npm run build.",
                  "Write the PR description carrying AC 23\u0027s ORDERED gate, because an agent structurally cannot execute it (`gh api *` is in .claude/settings.json\u0027s ask list at line 8): (1) push and let the Web app job report once, confirming the context name verbatim; (2) the user runs `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json`; (3) confirm the check shows as Required on the open PR; (4) then merge. Sequencing matters — re-applying after merge guarantees this exact PR is the one that could land with a red frontend. VERIFIED: `git remote -v` returns https://github.com/jordan-koch/nba2k-rpg.git, matching ops/README.md line 12.",
                  "Hand the four USER-RUN criteria to the user as a checklist: AC 20 (dev seam — the browser network tab must show /api/health on the VITE origin, which is what actually proves the proxy and therefore the no-CORS decision), AC 21 (built seam, uvicorn alone, no Vite running), AC 22 (stop the backend, get the legible panel naming the start command), AC 23 (the ordered gate above). /commit advances ROADMAP.md row 1.1 against the diff; line 156\u0027s stale \u0027is at intake\u0027 gets corrected in the same pass."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_repo_structure.py` is green including the new documentation assertions: README no longer says \u0027no application code yet\u0027 (case-insensitively), CLAUDE.md\u0027s map carries both app/ and src/rpg_api/ and no longer says the web app doesn\u0027t exist, ops/README.md has a Node-toolchain heading and both run-mode commands (AC 17)",
                       "`uv run \u003cconsole-script\u003e` starts the served-build mode and both / and /api/health answer 200 (AC 19)",
                       "All four Python commands and all four frontend commands green in one sitting",
                       "The PR description contains AC 23\u0027s four ordered steps, with step 2 marked as the user\u0027s",
                       "USER-RUN, handed off not claimed: AC 20 (Vite-origin /api/health in the network tab), AC 21 (uvicorn alone renders the page), AC 22 (backend stopped → legible panel naming the start command), AC 23 (required-check activation before merge)"
                   ],
    "commit_note":  "docs: describe the application that now exists. ops/README.md gains the Node toolchain and both run modes; README.md\u0027s \u0027no application code yet\u0027 banner, project map and Setup block are corrected; CLAUDE.md\u0027s map gains app/ and src/rpg_api/ and its \u0027web app doesn\u0027t exist yet\u0027 line goes. Adds a structural test so the claim is checked rather than judged, an .editorconfig for the two-toolchain repo, and fixes test_no_leaks.py\u0027s now-false lockfile docstring."
}

### testing

VERIFICATION MODEL — four layers, matching the scope's definition of testable
(requests/feature-requests/README.md lines 57-73: a cold agent runs one command and gets a pass
or fail).

LAYER 1 — the four Python commands, exactly as ops/README.md lines 64-73 documents and ci.yml
lines 36-47 runs them:
    uv run ruff check
    uv run ruff format --check
    uv run mypy
    uv run pytest -m "not network"
Every phase ends on all four green before /commit. AC 8's teeth: mypy must be green under the
UNCHANGED [tool.mypy] block at pyproject.toml lines 61-65, with zero new `# type: ignore` and
zero new per-module overrides. A green run bought by loosening strict FAILS the criterion. The
predictable friction is `disallow_untyped_decorators` over FastAPI's route decorators (scope
risk 6, unconfirmed until run) — FastAPI ships py.typed so annotated handlers should pass; if one
does not, the fix is annotating the handler, never carving rpg_api out of strict.

LAYER 2 — the frontend commands from app/, which ARE the CI job's steps, so a green local run
predicts a green CI run (AC 10):
    npm ci ; npm run typecheck ; npm run lint ; npm run test ; npm run build
plus `npm run typecheck:negative` asserted NON-zero (AC 11). No npm script may contain `&&`,
`rm -rf`, `cp`, or a POSIX inline env-var prefix — those work in CI and fail on Windows
PowerShell 5.1, which has no `&&` at all (scope risk 8).

LAYER 3 — the test suite, six files, no live sockets anywhere in pytest:
  tests/conftest.py         client factories parameterized on the injectable dist. Written once
                            here because items 1.7-1.11 each need it (a scope fold-in); five
                            agents inventing five variants is the alternative.
  tests/test_api_health.py  AC 2 (200 / application/json / status ok / version ==
                            rpg_core.__version__ / spa_built is a bool) and AC 7's JSON 404.
  tests/test_api_spa.py     AC 5 (missing dist: constructs clean, health 200, / -> 503 naming
                            `npm run build`), AC 6 (present dist: / -> 200 text/html, exact
                            bytes), the history fallback, and the path-traversal guard.
  tests/test_layering.py    AC 3 — the guard is a PURE function over a directory root,
                            unit-tested red and green against tmp_path, then pointed at
                            src/rpg_core and expected empty. One `uv run pytest` proves both
                            polarities with no tracked source mutated. AST-based, not regex.
  tests/test_ci_contexts.py AC 4 — yaml.safe_load over ci.yml, SET EQUALITY against
                            ops/branch-protection.json's contexts, a failure message naming which
                            side carries the extra, and a negative assertion that step-level
                            names never enter the job-name set.
  tests/test_packaging.py   AC 14 — the hatch wheel packages list contains src/rpg_api, and the
                            Pytest step's run string contains --cov=rpg_api. The suite
                            structurally cannot otherwise see this: pythonpath=["src"] makes
                            every local test pass with the hatch entry missing.
Plus the pre-existing guards, which must stay green throughout: tests/test_repo_structure.py
(extended with the app-ignore guard and AC 17's doc-agreement assertions),
tests/test_no_leaks.py (AC 13 — run it BEFORE staging app/package-lock.json),
tests/test_request_links.py (AC 16).

LAYER 4 — CI-only, because it cannot run offline: AC 18's real-server smoke step. It builds the
SPA, boots uvicorn against the built dist, and curls both `/` (200 HTML) and `/api/health` (200
JSON). It is the ONLY check that exercises uvicorn, the filesystem-backed serve, and the built
artifact — TestClient exercises none of them. Planned with a bounded readiness poll (60 x 1s,
exit 1 on exhaustion), never a fixed sleep (scope risk 14).

WHAT NO TEST CAN COVER — four USER-RUN criteria, marked so the acceptance panel does not claim
them: AC 20 (dev seam — the Vite-origin network request is what actually proves the proxy and
therefore the no-CORS-middleware decision), AC 21 (built seam), AC 22 (backend-unreachable
panel), AC 23 (the ordered gate: let the job report → user runs `gh api -X PUT` → confirm
Required on the open PR → then merge; `gh api *` sits in .claude/settings.json's ask list at line
8, so an agent structurally cannot do step 2, and editing the JSON alone never changes GitHub).

REGRESSION SAFETY. This item creates ground rather than changing behavior, so regression risk is
concentrated in the four existing tracked guards it newly exposes: test_no_leaks now scans
frontend files, test_request_links now scans this plan and the scope, test_repo_structure's
version pin now transitively covers the health payload, and the new test_ci_contexts guard turns
any future job rename or addition into a build failure instead of a silently forever-pending PR.

### risks

ARTIFACT-AUTHORING TRAP, fires on this very PR. tests/test_request_links.py scans every .md under requests/ and asserts each relative markdown link resolves on disk. Only 3+ backtick FENCED blocks are stripped (FENCED_BLOCK, line 26) — inline backticks are NOT exempt, contrary to a finding the scope itself records as wrong. So in IMPLEMENTATION_PLAN.md and every review file, write app/, src/rpg_api/, tests/conftest.py, app/dist/ as inline code or inside a fence, NEVER as a markdown link, until they exist on disk. The scope records this trap firing twice during stage 2.

OMITTING src/rpg_api FROM THE HATCH packages LIST FAILS ONLY AT RUNTIME. pyproject.toml line 73's `pythonpath = ["src"]` puts the package on the path for pytest regardless, so every test passes, CI goes green, and the console script dies with ModuleNotFoundError on the user's machine. The sneakiest failure in the item and the entire reason AC 14 exists. Phase 1 lands the edit and the guard together.

SILENT-GREEN MERGES. ops/branch-protection.json is a tracked file with NO connection to GitHub until `gh api -X PUT` re-applies it. Symptom: a PR merges with a red Web app job and nothing complains, indefinitely. The guard test covers only the tracked half. Verified for this plan: the remote is https://github.com/jordan-koch/nba2k-rpg.git, matching ops/README.md line 12, so the AC 23 command is correct as written. Still UNCONFIRMED: whether GitHub's protection API accepts the current JSON unchanged — it has not been re-applied since Phase 0.

STATICFILES AT / BREAKS TWO ACs AT ONCE, and it is the obvious implementation. It raises at construction on a missing directory (breaking AC 5 on every fresh clone) and answers unknown /api paths with a non-JSON 404 (breaking AC 7). The plan hand-rolls the catch-all instead. Leave the reason in a source comment or a future agent will 'simplify' it straight back into both bugs.

ROUTE REGISTRATION ORDER IS LOAD-BEARING. The `/{full_path:path}` catch-all must be registered AFTER `include_router(health.router, prefix="/api")`, and the api-prefix 404 check must be the FIRST branch inside it. Get either wrong and the health endpoint returns index.html — a failure that presents as a frontend bug.

tests/test_no_leaks.py NOW SCANS FRONTEND FILES and is a blocking public-repo guard. Two concrete tripwires: a package.json `author` field carrying an email fails EMAIL (line 29), and any Windows-generated absolute path fails WINDOWS_PATH (line 26). Inferred, not measured: npm lockfileVersion 3 entries carry registry URLs and integrity hashes rather than local paths, so it will probably pass — but run it BEFORE staging the lock. If it trips, the fix is a narrowly-justified ALLOWED entry with a written reason, never a weakened regex or a removed suffix.

GITLEAKS IS NOT INSTALLED LOCALLY — verified (`Get-Command gitleaks` fails on this machine). The scope's mitigation for risk 5 assumes it can be run before pushing. Either install it (a user action — winget is not in the allow list) or record explicitly that CI's Secret scan job (ci.yml 49-61, full history, blocking) is the only gate, and pre-plan the .gitleaksignore remediation. The exposure is a package-lock.json full of high-entropy base64 sha512 integrity strings; judged lower-probability than alarming, but do not assert it passes without running it.

npm SCRIPTS WITH SHELL OPERATORS WORK IN CI AND FAIL LOCALLY. Windows PowerShell 5.1 has no `&&` at all, and no `rm -rf`/`cp`. Every script must be a single command invocation. In particular `"build": "tsc && vite build"` — the shape half the Vite templates ship — is broken on the author's daily shell.

WINDOWS/NODE IPv6 RESOLUTION. A Vite proxy targeting http://localhost:PORT can resolve to ::1 on Windows while uvicorn binds 127.0.0.1, producing an ECONNREFUSED that looks exactly like the backend being down while it is running fine. Both the proxy target and the console script's bind address use the IPv4 literal 127.0.0.1.

mypy STRICT OVER FASTAPI. `disallow_untyped_decorators` against route decorators is the classic friction point; FastAPI ships py.typed so annotated handlers should pass, but this is unconfirmed until run. The failure mode to REFUSE is a per-module override quietly carving rpg_api out of strict on its first day — the exact asymmetry this item exists to prevent on the frontend side. AC 8 pins it.

setup-node CACHE PATH IS REPO-ROOT-RELATIVE even under `defaults.run.working-directory: app`. That default applies only to `run:` steps, never to `uses:` inputs, so `cache-dependency-path` must be `app/package-lock.json`. A wrong value does not fail — it silently disables caching, and `concurrency: cancel-in-progress` (ci.yml 10-12) means the job re-runs on every push.

PyYAML PARSES A WORKFLOW'S `on:` KEY AS THE BOOLEAN True (YAML 1.1). Harmless here because the guard reads only doc["jobs"], but it will surprise anyone who prints the parsed document while debugging.

`vite build` DOES NOT TYPECHECK — esbuild strips types without checking them. A green build proves nothing about types, which is why `npm run typecheck` is a separate script and a separate CI step. Do not let a later simplification fold them together.

THE ILL-TYPED FIXTURE MUST FAIL FOR A STRICT-SPECIFIC REASON. `const n: number = "x"` errors with strict OFF, so it proves the compiler ran, not that the flags are engaged. Use a strictNullChecks error and a noUncheckedIndexedAccess error so AC 11 actually tests what it claims to.

SCOPE LEAKAGE INTO ITEM 1.2. The status page is boring by design, and the single strongest failure mode for this item is deciding it would be more convincing with a career, a stub player, or a fake XP number in it. src/rpg_core/__init__.py must still be a docstring and a version string when this lands.

THE CI SMOKE STEP IS A FLAKE VECTOR (Decision 8, taken against the panel's recommendation). It needs Python and Node in one job plus readiness handling. Bounded poll with an explicit exhaustion failure, never a fixed sleep — a fixed sleep either wastes time or flakes, and usually both.

AC 17's CASE TRAP. README.md line 12 writes '**No application code yet.**' with a capital N; CLAUDE.md line 21 writes '**no application code yet.**' lowercase. A case-sensitive doc-agreement test silently passes on one of the two. Lowercase both sides before comparing.

OUT OF SCOPE BUT WORTH RECORDING BEFORE ITEM 2.1: .gitignore line 63's blanket `build/` matches a directory named build at ANY depth, which will silently shadow the `build/build-*.py` builder pattern CLAUDE.md says Phase 2 should follow. Not this item's problem; better found now. Its neighbour at line 62, blanket `dist/`, already covers app/dist/ independently of line 68 — so a passing ignore guard does not prove line 68 still exists.

### files_to_touch

{
    "path":  "pyproject.toml",
    "change":  "EDIT. Line 9: dependencies gains fastapi + uvicorn. Delete the discharged reservation comment at 11-13. Dev group (15-21) gains httpx, pyyaml, types-PyYAML, watchfiles. Line 31: packages gains \"src/rpg_api\". New [project.scripts] table with one console entrypoint. [tool.mypy] (61-65) UNCHANGED — AC 8."
}

{
    "path":  "uv.lock",
    "change":  "REGENERATE via `uv lock`, commit in the SAME commit as the pyproject change. ci.yml line 34 runs `uv sync --locked`, which hard-fails on a stale lock (AC 1). Currently 447 lines; .gitattributes line 40 already marks it linguist-generated -diff."
}

{
    "path":  "src/rpg_api/__init__.py",
    "change":  "NEW. Docstring mirroring src/rpg_core/__init__.py lines 3-6 from the API side; re-export create_app."
}

{
    "path":  "src/rpg_api/app.py",
    "change":  "NEW. `create_app(spa_dist: Path | None = None) -\u003e FastAPI` — the injectable factory ACs 5 and 6 require. Resolves the default dist relative to the repo root (never a literal path), includes the health router at prefix \"/api\", then calls attach_spa LAST."
}

{
    "path":  "src/rpg_api/health.py",
    "change":  "NEW. APIRouter with a fully annotated GET /health returning {status, version, spa_built}. Version read from rpg_core.__version__ — the one honest rpg_api → rpg_core import, inheriting the version pin at tests/test_repo_structure.py:46-54."
}

{
    "path":  "src/rpg_api/spa.py",
    "change":  "NEW. `attach_spa(app, dist)` — the catch-all: /api JSON-404 guard first, then a traversal-safe FileResponse, then the index.html history fallback, then a 503 naming `npm run build`. No StaticFiles, with the reason recorded in a comment."
}

{
    "path":  "src/rpg_api/serve.py",
    "change":  "NEW. `main() -\u003e None` wrapping uvicorn.run against 127.0.0.1:8000 with factory=True. The [project.scripts] target and the one documented way to run the served build (Decision 9)."
}

{
    "path":  "tests/conftest.py",
    "change":  "NEW. client_factory / client / built_spa_dist fixtures parameterized on the injectable dist — a scope fold-in written once here because items 1.7-1.11 each need it. Fully annotated; mypy strict covers tests/."
}

{
    "path":  "tests/test_api_health.py",
    "change":  "NEW. AC 2 (200, application/json, status ok, version == rpg_core.__version__, spa_built is a bool) and AC 7 (unknown /api path → 404 application/json) on both dist branches."
}

{
    "path":  "tests/test_api_spa.py",
    "change":  "NEW. AC 5 (missing dist: no construction error, health 200, / → 503 containing `npm run build`), AC 6 (present dist: / → 200 text/html, exact bytes), the history fallback, and the path-traversal guard."
}

{
    "path":  "tests/test_layering.py",
    "change":  "NEW. AC 3. Pure AST-based `web_imports_under(root)` denying fastapi/starlette/uvicorn/rpg_api (NOT pydantic — ADR 0002 makes that item 1.2\u0027s call). Red and green against tmp_path, then the real assertion over src/rpg_core with a message citing DESIGN.md §3."
}

{
    "path":  "tests/test_ci_contexts.py",
    "change":  "NEW. AC 4. yaml.safe_load of ci.yml → {job.get(\u0027name\u0027, key)}; SET EQUALITY against ops/branch-protection.json contexts; a message naming which side has the extra; a negative assertion that step-level names never enter the set."
}

{
    "path":  "tests/test_packaging.py",
    "change":  "NEW. AC 14. The hatch wheel packages list contains src/rpg_api, and the Pytest step\u0027s run string contains --cov=rpg_api. Guards the one failure the suite structurally cannot otherwise see."
}

{
    "path":  "tests/test_repo_structure.py",
    "change":  "EDIT. Add the app-ignore guard reusing _git_check_ignore (24-34) in the idiom of test_scratch_root_is_gitignored (83-92) — app/dist/ and app/node_modules/ ignored, app/src/main.tsx NOT ignored. Add AC 17\u0027s Documentation section asserting README/CLAUDE/ops agree with the repo that now exists."
}

{
    "path":  "tests/test_no_leaks.py",
    "change":  "EDIT, one docstring only. Line 37\u0027s \u0027Binary and lockfiles are skipped.\u0027 is false of package-lock.json (.json is in TEXT_SUFFIXES at 38-55). This item makes it wrong, so this item fixes it. Do NOT weaken any regex or remove a suffix."
}

{
    "path":  ".github/workflows/ci.yml",
    "change":  "EDIT. Line 47 gains --cov=rpg_api (Phase 1). A third job `name: Web app` with setup-node major 24, npm cache keyed on app/package-lock.json, working-directory app, running ci/typecheck/negative-typecheck/lint/test/build, plus the real-server smoke step with a bounded readiness poll (Phase 5)."
}

{
    "path":  "ops/branch-protection.json",
    "change":  "EDIT line 4: contexts becomes [\"Lint, types, tests\", \"Secret scan\", \"Web app\"] — in the SAME commit as the workflow change, or tests/test_ci_contexts.py fails. Inert on GitHub until the user re-applies it (AC 23)."
}

{
    "path":  ".github/dependabot.yml",
    "change":  "EDIT. Delete the line-30 placeholder comment; add an npm ecosystem entry with directory \"/app\" carrying the uv entry\u0027s monthly + patch-ignore posture from lines 16-28 (AC 15)."
}

{
    "path":  "app/package.json",
    "change":  "NEW. private:true, type:module, version 0.0.0 placeholder, NO author field (an email there fails test_no_leaks). Six single-command scripts — dev, build, typecheck, typecheck:negative, lint, test — with no shell operators."
}

{
    "path":  "app/package-lock.json",
    "change":  "NEW, committed. .gitattributes line 41 already marks it linguist-generated -diff. Run tests/test_no_leaks.py BEFORE staging it (AC 13)."
}

{
    "path":  "app/tsconfig.json",
    "change":  "NEW. strict:true plus noUncheckedIndexedAccess, noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch. include [src, vite.config.ts]; exclude typecheck-fixtures. Scoped INSIDE app/, never a repo-root config."
}

{
    "path":  "app/tsconfig.negative.json",
    "change":  "NEW. Extends tsconfig.json, includes only typecheck-fixtures. Target of `npm run typecheck:negative`, asserted non-zero by the CI step and documented in PowerShell form in ops/README.md (AC 11)."
}

{
    "path":  "app/typecheck-fixtures/bad.ts",
    "change":  "NEW. Committed ill-typed fixture whose errors are strict-SPECIFIC (one strictNullChecks, one noUncheckedIndexedAccess), so it proves the flags rather than the compiler."
}

{
    "path":  "app/eslint.config.js",
    "change":  "NEW. Flat config: @eslint/js + typescript-eslint + eslint-plugin-react-hooks (Decision 2, against the panel\u0027s oxlint recommendation). Scope limited to app/; ignores dist and typecheck-fixtures. A root config would start reporting on .claude/skills/**/*.js — an explicit non-goal."
}

{
    "path":  "app/vite.config.ts",
    "change":  "NEW. defineConfig from vitest/config (one file, no separate vitest config). React plugin; server.proxy \u0027/api\u0027 → http://127.0.0.1:8000 on the IPv4 LITERAL; test block with jsdom, setupFiles, globals:false."
}

{
    "path":  "app/index.html",
    "change":  "NEW. Real page title and favicon link, not the Vite template defaults. Identity, not design."
}

{
    "path":  "app/public/favicon.svg",
    "change":  "NEW. Prefer .svg over .ico — .gitattributes line 35 marks *.ico binary, correctly, which makes it undiffable for no benefit here."
}

{
    "path":  "app/src/main.tsx",
    "change":  "NEW. React root mount. Nothing else."
}

{
    "path":  "app/src/App.tsx",
    "change":  "NEW. The entire UI: loading / ok (status + version) / unreachable. The unreachable panel NAMES the start command (AC 22). No router, no state library, no component library, no theme."
}

{
    "path":  "app/src/api/client.ts",
    "change":  "NEW. Hand-written `Health` interface + `fetchHealth()` against the RELATIVE path /api/health. The one place the frontend talks to the backend; explicitly not the deferred codegen contract, but the seam codegen slots into at item 1.8."
}

{
    "path":  "app/src/setupTests.ts",
    "change":  "NEW. Imports @testing-library/jest-dom. Referenced by vite.config.ts\u0027s test.setupFiles."
}

{
    "path":  "app/src/App.test.tsx",
    "change":  "NEW. EXACTLY two Vitest tests (AC 12): renders the fetched version; renders the unreachable panel on a rejected fetch. Stub global fetch so client.ts is exercised too."
}

{
    "path":  ".editorconfig",
    "change":  "NEW, repo root. LF + final newline + utf-8; indent 4 default, 2 for ts/tsx/js/mjs/json/css/html/yml/yaml; CRLF for ps1/psm1/bat/cmd mirroring .gitattributes lines 7-10."
}

{
    "path":  "ops/README.md",
    "change":  "EDIT. New `## Node toolchain` section beside the uv one (32-62): node 24 / npm 11 as measured, the npm ci stale-lock rule with the sharpness lines 54-57 give the uv rule, the PowerShell negative-typecheck form, and both run modes (dev: two terminals; served: the console script only, per Decision 9)."
}

{
    "path":  "README.md",
    "change":  "EDIT. Delete the \u0027No application code yet\u0027 banner (12-13); add app/ and src/rpg_api/ to the project map (53-69); drop \u0027and the web app\u0027 from line 72; extend Setup (74-83) with the Node steps and both run commands. AC 17."
}

{
    "path":  "CLAUDE.md",
    "change":  "EDIT, not append — 158 lines and a hard budget. Status section (20-21), project map block (49-63) gains app/ and src/rpg_api/, and line 66\u0027s \u0027and the web app don\u0027t exist yet\u0027. AC 17."
}

{
    "path":  "ROADMAP.md",
    "change":  "EDIT BY /commit ONLY, against the diff — never hand-edited. Row 1.1 at line 165 advances to DONE. Line 156\u0027s \u0027is at intake\u0027 is already stale and should be corrected in the same pass."
}

{
    "path":  "requests/feature-requests/README.md",
    "change":  "EDIT. The Index row at line 106 advances its Stage cell to `plan` when the plan lands (and to `implemented` after stage 4). Match the row by its [1.1-app-shell] link."
}

{
    "path":  "requests/feature-requests/1.1-app-shell/IMPLEMENTATION_PLAN.md",
    "change":  "NEW — the stage-3 deliverable this analysis feeds. Opens `\u003e **Status:** plan · created 2026-08-14 · decided · next: implement`. Every path it creates is written inline-code or fenced, NEVER as a markdown link."
}

### code_references

{
    "ref":  "pyproject.toml:9",
    "claim":  "`dependencies = []` — the empty runtime dependency list Phase 1 fills with fastapi + uvicorn. Verified by reading."
}

{
    "ref":  "pyproject.toml:11-13",
    "claim":  "The reservation comment \u0027FastAPI arrives with Phase 1 item 1.1 (app-shell)\u0027. Phase 1 deletes it as discharged. Verified."
}

{
    "ref":  "pyproject.toml:15-21",
    "claim":  "The dev group — pytest\u003e=8.0, pytest-cov\u003e=5.0, ruff\u003e=0.6, mypy\u003e=1.11 — which gains httpx, pyyaml, types-PyYAML and watchfiles. Verified."
}

{
    "ref":  "pyproject.toml:30-31",
    "claim":  "`[tool.hatch.build.targets.wheel] packages = [\"src/rpg_core\"]` — the line whose omission of src/rpg_api fails only at runtime (AC 14). Verified."
}

{
    "ref":  "pyproject.toml:49",
    "claim":  "The `\"DTZ\"` ruff rule, \u0027naive datetimes — every event timestamp is tz-aware or it is a bug\u0027. Part of why Decision 6 kept started_at/uptime out of the health payload. Verified."
}

{
    "ref":  "pyproject.toml:61-65",
    "claim":  "`[tool.mypy]` — python_version 3.12, strict = true, warn_unreachable = true, files = [\"src\", \"tests\"]. AC 8 requires this block be UNCHANGED, and `files` already reaches any new package under src/. Verified."
}

{
    "ref":  "pyproject.toml:73",
    "claim":  "`pythonpath = [\"src\"]` — why a missing hatch packages entry passes every local test and fails only on an installed environment. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:19",
    "claim":  "`name: Lint, types, tests` — the python job\u0027s display name, one of the two strings in the contexts array. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:34",
    "claim":  "`run: uv sync --locked` — hard-fails on a stale lock rather than re-resolving. Verbatim what AC 1 pins. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:47",
    "claim":  "`run: uv run pytest -m \"not network\" --cov=rpg_core --cov-report=term-missing` — the single line that gains --cov=rpg_api. Grep confirms it is the ONLY occurrence of rpg_core anywhere in the workflow."
}

{
    "ref":  ".github/workflows/ci.yml:50",
    "claim":  "`name: Secret scan` — the secrets job\u0027s display name, the second contexts entry. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:10-12",
    "claim":  "`concurrency: group: ci-${{ github.ref }}` with `cancel-in-progress: true` — the job re-runs on every push, which is why npm caching on setup-node earns its keep. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:53-56",
    "claim":  "The secrets job checks out with `fetch-depth: 0`, so gitleaks scans full history — the scan that will see the new package-lock.json (scope risk 5). Verified."
}

{
    "ref":  ".github/workflows/ci.yml:22",
    "claim":  "`uses: actions/checkout@v5`, and at line 25 `astral-sh/setup-uv@v6` — the action majors already pinned in this repo, which the new job and its smoke step should match. Verified."
}

{
    "ref":  "ops/branch-protection.json:4",
    "claim":  "`\"contexts\": [\"Lint, types, tests\", \"Secret scan\"]` — the exact array a third job must join, and the set AC 4\u0027s guard compares against. Verified."
}

{
    "ref":  "ops/README.md:11-14",
    "claim":  "The apply command `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json`. Owner/repo VERIFIED still current: `git remote -v` returns https://github.com/jordan-koch/nba2k-rpg.git."
}

{
    "ref":  "ops/README.md:21-24",
    "claim":  "The blockquote warning that renaming a CI job silently breaks the contexts array and makes PRs \u0027wait forever for a check that never reports\u0027. AC 4\u0027s guard is the mechanical version of this prose."
}

{
    "ref":  "ops/README.md:64-73",
    "claim":  "\u0027The same four commands CI runs, in the same order\u0027 — uv run ruff check / ruff format --check / mypy / pytest. The per-phase local gate. Verified."
}

{
    "ref":  "src/rpg_core/__init__.py:3-6",
    "claim":  "\u0027Deliberately I/O-free and web-free... The API and the web app depend on it; it depends on neither.\u0027 The layering guard\u0027s subject, stated from the core\u0027s side. Verified."
}

{
    "ref":  "src/rpg_core/__init__.py:16",
    "claim":  "`__version__ = \"0.1.0\"` — the value the health payload reads by attribute rather than re-typing. Verified; the file is 17 lines total and ships no py.typed marker."
}

{
    "ref":  "DESIGN.md:106-109",
    "claim":  "\u0027Two packages, one repo. src/rpg_core/ is the I/O-free domain; the API and web app depend on it and it depends on neither.\u0027 Cited by name in the layering guard\u0027s failure message (Decision 3: a guard test instead of an ADR). Verified."
}

{
    "ref":  "tests/test_repo_structure.py:24-34",
    "claim":  "`_git_check_ignore` shells `git check-ignore -q --no-index`, returns True on exit 0 and raises on 128 — works on paths that do not exist, which is why the app-ignore guard can be written before app/ does. Verified."
}

{
    "ref":  "tests/test_repo_structure.py:46-54",
    "claim":  "`test_package_version_matches_pyproject` asserts rpg_core.__version__ == pyproject[\u0027project\u0027][\u0027version\u0027], so a health test asserting body[\u0027version\u0027] == rpg_core.__version__ inherits the pin transitively. Verified."
}

{
    "ref":  "tests/test_repo_structure.py:83-92",
    "claim":  "`test_scratch_root_is_gitignored` — the exact template the app/dist + node_modules ignore guard copies, including the pytest.skip on \u0027git unavailable\u0027. Verified."
}

{
    "ref":  "tests/test_repo_structure.py:113-133",
    "claim":  "The ADR index and contiguity tests — the \u0027the repo and its documents agree\u0027 idiom AC 17\u0027s documentation assertions extend. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:26-29",
    "claim":  "WINDOWS_PATH, POSIX_HOME and EMAIL — the three patterns a frontend config file could trip. A package.json `author` email hits EMAIL directly. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:32-35",
    "claim":  "`ALLOWED` maps a path to a written reason — the only sanctioned escape hatch, currently two entries (this file itself and .env.example). Any new entry needs its reason. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:37",
    "claim":  "The docstring \u0027Extensions worth scanning. Binary and lockfiles are skipped.\u0027 — true of uv.lock, false of package-lock.json once tracked. This item makes it wrong and fixes it. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:38-55",
    "claim":  "TEXT_SUFFIXES contains .json, .ts, .tsx, .js, .mjs, .css and .html — so app/package.json, app/package-lock.json, app/tsconfig.json and app/vite.config.ts all become scanned. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:58-71",
    "claim":  "`_tracked_text_files` filters `git ls-files -z` by ALLOWED and suffix — scanned files are the git index, so anything gitignored (app/dist/, node_modules/) is out of scope by construction. Verified."
}

{
    "ref":  "tests/test_request_links.py:26",
    "claim":  "`FENCED_BLOCK = re.compile(r\"^([ \\t\u003e]*)(`{3,}|~{3,}).*?^\\1\\2.*?$\", re.DOTALL | re.MULTILINE)` — only 3+ backtick or tilde fences are stripped. Inline backticks are NOT exempt, confirming the scope\u0027s authoring rule and the correction it records. Verified."
}

```text
{
    "ref":  "tests/test_request_links.py:44-64",
    "claim":  "`_dead_links` resolves every markdown-link target relative to the file, exempting http(s)/mailto/# targets, \u003cplaceholder\u003e forms and var/ paths, and stripping a `file.py:123` suffix via LINE_SUFFIX. Bare path tokens are NOT checked — only `[text](target)` forms. Verified."
}
```

{
    "ref":  ".gitignore:62-63",
    "claim":  "Blanket `dist/` and `build/` rules matching at any depth. `dist/` already ignores app/dist/ independently of line 68; `build/` will shadow Phase 2\u0027s build/build-*.py pattern (scope risk 15). Verified."
}

{
    "ref":  ".gitignore:66-68",
    "claim":  "The \u0027─── Node / web app ───\u0027 block — node_modules/, .vite/, app/dist/ — reserved by Phase 0 without creating anything, and the strongest evidence for the app/ convention. Verified."
}

{
    "ref":  ".gitignore:43-44",
    "claim":  "`!careers/` and `!careers/**` — the tracked-ledger carve-out the new ignore rules must not disturb. Verified."
}

{
    "ref":  ".gitattributes:3",
    "claim":  "`* text=auto eol=lf` — npm-generated files normalize to LF, so a Windows-authored package-lock.json does not churn in Linux CI. Verified."
}

{
    "ref":  ".gitattributes:20-25",
    "claim":  "*.js, *.mjs, *.ts, *.tsx, *.css and *.html already declared text — Phase 0 reserved the frontend file types by name. Verified."
}

{
    "ref":  ".gitattributes:35",
    "claim":  "`*.ico binary` — correct, and the reason to prefer a .svg favicon so the asset stays diffable. Verified."
}

{
    "ref":  ".gitattributes:41",
    "claim":  "`package-lock.json linguist-generated=true -diff` — the third Phase-0 reservation naming this item\u0027s artifacts by name. Verified."
}

{
    "ref":  ".github/dependabot.yml:16-28",
    "claim":  "The uv entry — monthly interval, commit-message prefix \u0027deps\u0027, labels [\u0027dependencies\u0027], and an ignore block for version-update:semver-patch. The npm entry mirrors this posture exactly. Verified."
}

{
    "ref":  ".github/dependabot.yml:30",
    "claim":  "`# npm arrives with Phase 1 item 1.1 (app-shell). Add the ecosystem entry then.` — the placeholder AC 15 requires be gone. Verified."
}

{
    "ref":  ".claude/settings.json:3-12",
    "claim":  "The `ask` list — git commit/push/merge and `gh api *`. This is why AC 23 step 2 is structurally impossible for an agent, and why /commit is the only sanctioned commit path. Verified."
}

{
    "ref":  ".claude/settings.json:13-17",
    "claim":  "`PowerShell(node *)` and `PowerShell(npm *)` already in the allow list — the frontend work needs no permission changes. Verified."
}

{
    "ref":  "requests/feature-requests/README.md:57-73",
    "claim":  "The definition of testable — \u0027a cold agent can run one command and get a pass or fail\u0027 — and the rule that human-only criteria must be marked user-run so the acceptance panel does not claim them. Verified."
}

{
    "ref":  "requests/feature-requests/README.md:96-100",
    "claim":  "The status blockquote grammar and the intake → scoped → planned → implemented progression the new plan\u0027s header must follow. Verified."
}

```text
{
    "ref":  "requests/feature-requests/README.md:106",
    "claim":  "The Index row `| [1.1-app-shell](1.1-app-shell/) | scoped | ... |` whose Stage cell advances to `plan`. Verified."
}
```

{
    "ref":  "CLAUDE.md:20-22",
    "claim":  "\u0027**Phase 0 — harness — complete.** ... **no application code yet.**\u0027 — lowercase \u0027no\u0027, where README.md line 12 capitalizes it. AC 17\u0027s case trap. Verified."
}

{
    "ref":  "CLAUDE.md:49-63",
    "claim":  "The project map fenced block listing \u0027src/rpg_core/  Domain core — I/O-free, web-free. Empty until Phase 1\u0027 — gains app/ and src/rpg_api/. Verified; CLAUDE.md is 158 lines, so this is an edit, not an append."
}

{
    "ref":  "CLAUDE.md:65-66",
    "claim":  "\u0027`careers/`, `datasets/`, `rulesets/`, `lib/`, and the web app don\u0027t exist yet — don\u0027t create them speculatively.\u0027 The exact substring AC 17 asserts is gone. Verified — and grep confirms `app/` appears nowhere in CLAUDE.md, so the FEATURE_REQUEST\u0027s contrary claim is false, exactly as the scope says."
}

{
    "ref":  "README.md:12-13",
    "claim":  "\u0027\u003e **Phase 0.** Repo, process, and CI harness exist. **No application code yet.**\u0027 — capital N. The banner AC 17 asserts is gone. Verified."
}

{
    "ref":  "README.md:53-72",
    "claim":  "The project map fenced block and the sentence \u0027Directories appear when their phase does. `careers/`, `datasets/`, `rulesets/`, `lib/`, and the web app don\u0027t exist yet.\u0027 Both need editing. Verified."
}

{
    "ref":  "README.md:74-83",
    "claim":  "The Setup block — winget uv, uv sync, uv run pytest — that gains the Node steps and both run commands. Verified."
}

{
    "ref":  "ROADMAP.md:165",
    "claim":  "`| 1.1 | app-shell | FastAPI + React/Vite wiring, dev server, health endpoint, frontend build in CI | M | 0.3 | IN-PROGRESS |` — the row /commit advances to DONE. Verified."
}

{
    "ref":  "ROADMAP.md:156",
    "claim":  "\u0027**Status:** **IN-PROGRESS** — 1.1 app-shell is at intake.\u0027 Already stale (it is scoped) and should be corrected in this item\u0027s /commit doc pass. Verified."
}

{
    "ref":  "ROADMAP.md:121-123",
    "claim":  "The legend — ★ means run the full scoping panel, \u0027Unmarked items should skip straight to a plan or straight to work\u0027, and the three Status values. 1.1 is unmarked; the panel ran anyway, disposed by Decision 7. Verified."
}

{
    "ref":  ".claude/skills/create-implementation-plan/SKILL.md:175-230",
    "claim":  "The plan template\u0027s section MENU — sections 1-8 Always/Default, 9 (data contracts) and 10 (code-grounding) Conditional. Section 9 is OMITTED for this item: no dataset, no manifest, no source. Verified."
}

{
    "ref":  ".claude/skills/create-implementation-plan/SKILL.md:249-255",
    "claim":  "\u0027Every relative link and bare requests/... token you write must resolve on disk\u0027, plus the instruction to fence forward references — the plan-side statement of the scope\u0027s Authoring rule. Verified."
}

### open_questions

CONSOLE-SCRIPT NAME. Decision 9 puts a [project.scripts] entrypoint in scope but names neither the script nor its target. This plan proposes `nba2k-rpg-serve = "rpg_api.serve:main"`; `rpg-serve` is the shorter alternative. It matters beyond taste because the name is hardcoded into ops/README.md, the CI smoke step, AC 19, and the backend-unreachable panel's text (AC 22) — four places that must agree. Pick once, in Phase 1.

DEFAULT PORT. Nothing in the repo pins one. This plan assumes uvicorn's 8000, hardcoded identically in the Vite proxy target, the console script, the CI smoke step and ops/README.md. Decision 5 explicitly rules out an RPG_API_PORT env key ('a second place for the Vite proxy target to drift'), so the number is a documented constant with no override. Confirm 8000 is free on the user's machine before those four places are written.

actions/setup-node MAJOR VERSION — cannot be verified offline. The repo pins actions/checkout@v5 (ci.yml:22) and astral-sh/setup-uv@v6 (line 25), so the current setup-node major is probably ahead of the v4 this plan defaults to. UNCONFIRMED: check the action's marketplace page before committing Phase 5. Dependabot's github-actions entry (dependabot.yml 8-14) bumps it monthly either way, so a conservative pin is safe but noisy.

FASTAPI / UVICORN VERSION FLOORS. The plan writes fastapi>=0.115 and uvicorn>=0.30 as placeholders. Set the actual floors from what `uv lock` resolves on the day — do not commit a floor nobody has seen resolve. Same on the frontend: React 19 vs 18 changes the @testing-library/react major, and the Vite major changes the flat-eslint plugin set.

GITLEAKS LOCALLY. Verified NOT installed on this machine. Is installing it (winget, which is not in .claude/settings.json's allow list, so a user action) acceptable, or is CI's Secret scan job the accepted gate for scope risk 5? Either answer is fine; the plan must not pretend a local run happened.

AC 17's SCOPE ON CLAUDE.md. The criterion names README.md's 'No application code yet' string plus CLAUDE.md's map and 'web app doesn't exist' line — but CLAUDE.md line 21 carries its own 'no application code yet' that is equally false after this lands. This plan fixes it and asserts it lowercased on both files. Confirm that is wanted rather than a criterion-widening.

py.typed MARKERS. Neither src/rpg_core/ nor the planned src/rpg_api/ ships one, so the built wheel's types are invisible to downstream consumers. Irrelevant to in-repo mypy (files=["src","tests"] checks sources directly) and there are no downstream consumers, so this plan leaves both without one for consistency. Flagged rather than fixed — adding it to rpg_api alone would be the wrong kind of asymmetry.

SINGLE tsconfig VS PROJECT REFERENCES. This plan uses one app/tsconfig.json covering src/ and vite.config.ts, with @types/node, because it is one fewer thing for a cold agent to reason about. The Vite template ships a tsconfig.app.json / tsconfig.node.json split instead, which keeps DOM and Node lib types from mixing. If the single config produces friction between vite.config.ts and the browser code, switch to the split rather than loosening a strictness flag — AC 8's spirit applies to the frontend half too.

docs/data-sources.md DOES NOT EXIST — the planning brief names it; the repo has docs/data-access.md (verified). Either way it is N/A here: the scope confirms no dataset, no datasets/manifest.json and no external source, so no verification phase is owed and the plan carries no data-contracts section. Every unconfirmed claim in data-access.md concerns the game install and is untouched by this item.

---

## Lens: `sequencing`

### ok

true

### onboarding_files

{
    "path":  "requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md",
    "why":  "The decided upstream artifact. 23 acceptance criteria, 10 Decisions, 15 Risks, and a load-bearing Authoring rule at lines 5-18: every path this item CREATES (src/rpg_api/, app/, app/dist/, tests/conftest.py) must be written inline or fenced, NEVER as a markdown link, or tests/test_request_links.py turns CI red on this very PR."
}

{
    "path":  "requests/feature-requests/1.1-app-shell/FEATURE_REQUEST.md",
    "why":  "Context only. Its nine Open Questions are all settled by the scope. NOTE its Rough Ideas claim that CLAUDE.md\u0027s project map lists serving under app/ is VERIFIED FALSE (grep CLAUDE.md for app/ returns nothing) — do not inherit that reasoning."
}

{
    "path":  "requests/feature-requests/README.md",
    "why":  "Pipeline contract. Lines 57-73 define \u0027testable\u0027 (a cold agent runs ONE command and gets pass/fail) and the USER-RUN carve-out; lines 96-100 the status blockquote grammar; line 106 the Index row whose Stage cell advances to plan then implemented."
}

{
    "path":  "pyproject.toml",
    "why":  "The single file this item changes most. Line 9 `dependencies = []`; lines 11-13 the comment reserving FastAPI for this exact item; line 31 `packages = [\"src/rpg_core\"]`; line 49 the DTZ rule; lines 61-65 `[tool.mypy]` strict + warn_unreachable + files=[src,tests]; line 73 `pythonpath = [\"src\"]`; lines 15-21 the dev group."
}

{
    "path":  ".github/workflows/ci.yml",
    "why":  "Line 19 job display name `Lint, types, tests`; line 34 `uv sync --locked`; line 47 `--cov=rpg_core`; line 50 `Secret scan`; lines 10-12 concurrency cancel-in-progress (why npm caching matters). The third job goes alongside these."
}

{
    "path":  "ops/branch-protection.json",
    "why":  "Line 4: `contexts` is exactly [\"Lint, types, tests\", \"Secret scan\"] — CI job DISPLAY names. The new job\u0027s name joins this array in the same commit as the workflow change, and the file is inert until re-applied with `gh api -X PUT`."
}

{
    "path":  "ops/README.md",
    "why":  "Lines 12-14 the apply command (owner/repo `jordan-koch/nba2k-rpg` — VERIFIED against `git remote -v` on 2026-08-14); lines 20-24 the job-rename warning this item generalizes to job addition; lines 32-63 the uv toolchain section the Node section sits beside; lines 64-73 the \u0027same four commands CI runs\u0027 block."
}

{
    "path":  "tests/test_repo_structure.py",
    "why":  "The guard idiom to copy. `_git_check_ignore` (24-34) works on paths that do NOT exist yet; `test_package_version_matches_pyproject` (46-54) transitively pins the health payload\u0027s version; `test_scratch_root_is_gitignored` (83-92) is the template for the app/dist + node_modules guard."
}

{
    "path":  "tests/test_no_leaks.py",
    "why":  "Blocking public-repo guard that will now scan frontend files. TEXT_SUFFIXES (38-55) already covers .json/.ts/.tsx/.css/.html; ALLOWED (32-35) is the only sanctioned escape hatch; line 37\u0027s docstring claim \u0027lockfiles are skipped\u0027 becomes FALSE for package-lock.json and this item fixes it. CRITICAL: `_tracked_text_files` (58-71) reads `git ls-files` — the INDEX — so untracked new files are invisible to it until staged."
}

{
    "path":  "tests/test_request_links.py",
    "why":  "Why the Authoring rule exists. FENCED_BLOCK (line 26) strips 3+ backtick fences only — inline backticks are NOT stripped; `_dead_links` (40-64) resolves every relative markdown link against disk."
}

{
    "path":  "src/rpg_core/__init__.py",
    "why":  "The entire domain core today: a docstring stating the dependency direction (lines 3-11) and `__version__ = \"0.1.0\"` (line 16). It must still be exactly this when 1.1 lands."
}

{
    "path":  "DESIGN.md",
    "why":  "Lines 106-109, \u0027Two packages, one repo\u0027 — the architecture this item instantiates and the sentence the layering guard\u0027s failure message must cite by name (Decision 3 chose a guard test over ADR 0010)."
}

{
    "path":  ".gitignore",
    "why":  "Lines 66-68 the Node block (node_modules/, .vite/, app/dist/) reserved in Phase 0; line 62 a blanket `dist/` and line 63 a blanket `build/` matching at ANY depth — nothing this item needs may live under a directory named dist or build outside app/."
}

{
    "path":  ".gitattributes",
    "why":  "Line 3 `* text=auto eol=lf`, lines 20-25 the .js/.mjs/.ts/.tsx/.css/.html text entries, line 35 `*.ico binary` (the favicon), line 41 `package-lock.json linguist-generated=true -diff` — Phase 0 reserved all of this by name."
}

{
    "path":  ".github/dependabot.yml",
    "why":  "Lines 16-28 the uv entry whose monthly + patch-ignore posture the npm entry mirrors; line 30 the placeholder comment `# npm arrives with Phase 1 item 1.1 (app-shell)` that AC 15 requires be discharged and removed."
}

{
    "path":  ".claude/settings.json",
    "why":  "Line 8 puts `gh api *` in the ask list — the agent structurally cannot apply branch protection, which is why AC 23 is USER-RUN. Lines 16-17 already allow `node *` and `npm *`."
}

{
    "path":  "CLAUDE.md",
    "why":  "Lines 47-63 the project map that gains app/ and src/rpg_api/, and line 66 \u0027the web app don\u0027t exist yet\u0027 which stops being true. It has a hard line budget — this is an EDIT, not an append. AC 17 mechanically checks both."
}

{
    "path":  "README.md",
    "why":  "Line 12 the \u0027No application code yet\u0027 banner AC 17 asserts is gone; lines 51-72 the project map and its \u0027the web app don\u0027t exist yet\u0027 sentence; lines 74-80 the Setup block that must gain the Node half."
}

{
    "path":  "ROADMAP.md",
    "why":  "Line 165 row 1.1 (size M, needs 0.3) and lines 166-175 the eleven downstream rows this unblocks; line 156 the phase Status line still reading \u00271.1 app-shell is at intake\u0027. /commit maintains these against the diff — do NOT hand-edit."
}

{
    "path":  "docs/decisions/0002-manual-ingestion-dto-boundary.md",
    "why":  "Read before writing the layering deny-list. It requires the DTO be constructible in tests with no HTTP and no UI, which is exactly why `pydantic` is deliberately ABSENT from the deny-list — that call belongs to item 1.2, not this one."
}

### architecture_notes

SHAPE OF THE CHANGE. This item adds a second source package and a first frontend to a repo that today has exactly one Python package containing a docstring and a version string. It is content-free by design: the only durable artifacts it leaves behind are seams and guards.

DEPENDENCY DIRECTION (DESIGN.md:106-109). `src/rpg_api/` imports `rpg_core`; `src/rpg_core/` imports no web framework and nothing from `rpg_api`. The one honest import is the health payload's `version`, read from `rpg_core.__version__` rather than re-typed — which makes tests/test_repo_structure.py:46-54 transitively cover the payload. Enforcement is a guard test (Decision 3 rejected ADR 0010 on the grounds that a test fails a build and prose does not), and its failure message must cite DESIGN.md §3 by name.

WHY src/ AND NOT app/. `[tool.mypy] files = ["src", "tests"]` (pyproject.toml:65) and `[tool.pytest.ini_options] pythonpath = ["src"]` (pyproject.toml:73) both already reach `src/`. Putting the API there is zero config churn on both. The cost is a trap: `pythonpath = ["src"]` also means every test passes whether or not `src/rpg_api` is in `[tool.hatch.build.targets.wheel].packages` (pyproject.toml:31) — the omission fails ONLY on an installed environment, at runtime, with ModuleNotFoundError. AC 14 exists because the test suite structurally cannot otherwise see this.

THE INJECTABLE DIST PATH IS THE LOAD-BEARING API DECISION. `create_app(spa_dist: Path)` — a factory argument, never a module-level constant. Two reasons compound: (1) Starlette's `StaticFiles(directory=...)` raises at CONSTRUCTION when the directory is absent (scope risk 7, labelled inferred — Phase 0 verifies it), so a fresh clone with no `app/dist/` would get an import-time traceback instead of an app; (2) a module-level constant makes ACs 5 and 6 untestable without a real build. With a factory argument both branches are unit-testable against `tmp_path` with no listening socket.

ROUTE REGISTRATION ORDER IS A CORRECTNESS CONSTRAINT, NOT A STYLE CHOICE. Starlette matches routes in registration order. The order must be: (1) real API routes under `/api`; (2) an explicit `/api/{rest:path}` catch-all returning a JSON 404 — this is what makes AC 7 hold, and without it the SPA history fallback swallows API 404s into HTML; (3) the static mount for built assets; (4) the SPA history fallback for unmatched non-`/api` paths. The fallback (a folded-in item) is what stops item 1.10's router from being a breaking change.

spa_built IS EVALUATED ONCE, AT CONSTRUCTION. The same predicate — `(spa_dist / "index.html").is_file()` — decides whether the static mount is registered AND what `spa_built` reports. Evaluating the mount at construction and the flag per-request would let the payload claim `true` while `/` still 503s. One evaluation, one truth; the consequence ("restart the server after building the SPA") is documented in `ops/README.md` rather than papered over.

TWO RUN MODES, NO CORS ANYWHERE. Dev = Vite dev server proxying `/api` to uvicorn, making the browser's origin single. Built = uvicorn serving `app/dist` — same-origin by construction. No CORS middleware exists in either mode, and the proxy target is the IPv4 literal `127.0.0.1` because on Windows `localhost` can resolve to `::1` while uvicorn binds IPv4, producing an ECONNREFUSED indistinguishable from a dead backend (scope risk 9).

CHECK-POSTURE SYMMETRY IS THE SECOND HALF OF THE ITEM. Python has ruff + mypy strict + pytest + a required CI context. The frontend gets TypeScript `strict` plus `noUncheckedIndexedAccess` / `noUnusedLocals` / `noUnusedParameters` / `noFallthroughCasesInSwitch`, eslint with typescript-eslint and react-hooks, and vitest — in a THIRD CI job whose display name must equal a new entry in ops/branch-protection.json:4. Every frontend config file lives INSIDE `app/` with file scope limited to `app/`: a repo-root eslint or tsconfig would immediately start reporting on the thousands of unlinted lines of `.js`/`.mjs` under `.claude/skills/`, which the scope explicitly excludes.

TWO GUARDS THAT PROTECT PROCESS RATHER THAN CODE. (a) The CI-jobs guard parses ci.yml with `yaml.safe_load` and asserts `{jobs.*.name} == set(contexts)` — EQUALITY, because containment passes while a typo'd context name makes every PR hang forever on a check that never reports, the exact failure ops/README.md:20-24 warns about. It needs `pyyaml` and `types-PyYAML` in the dev group (mypy strict needs the stubs). (b) The docs guard (AC 17) is the only pass/fail check Goal 7 has; without it, "stop the docs lying" is delegated to /commit's judgment gate.

NO DATA LAYER IS TOUCHED. `datasets/manifest.json` does not exist (item 2.1), `careers/` does not exist (item 1.2), `rulesets/` does not exist (item 1.4). The resolve-by-logical-name convention, ADR 0003's append-only ledger, ADR 0004's immutable pinned rulesets, and ADR 0008's price-never-score rule all have zero surface here — and the plan's job is to make sure this item does not accidentally create that surface. docs/data-access.md §3's four unconfirmed external sources are likewise untouched: this item makes no outbound network call from either half, so no source-verification phase is owed. The unconfirmed claims this item DOES rest on are its own (Starlette's construction-time failure, mypy strict over FastAPI decorators, the leak scanners over package-lock.json, npm lockfileVersion skew), and Phase 0 exists to convert them from belief to measurement before anything is built on them.

### phases

{
    "name":  "Phase 0 — Preflight: convert the item\u0027s unconfirmed beliefs into measurements",
    "goal":  "Every downstream phase rests on a belief that has never been tested in this repo: that Starlette raises at construction on a missing dist dir, that mypy strict passes over FastAPI route decorators, that a Vite package-lock.json survives tests/test_no_leaks.py and gitleaks, and that the branch-protection JSON still matches the live remote. Measure all of them in a throwaway scratch tree BEFORE a single tracked dependency lands, so the first surprise costs a probe and not a rewrite.",
    "steps":  [
                  "Create a scratch dir under `var/spike/` (gitignored by .gitignore line 18 — nothing here is ever committed) and work there for the whole phase.",
                  "BELIEF 1 (scope risk 7, labelled inferred): write a probe using `uv run --with fastapi --with starlette python \u003cprobe\u003e` that constructs `StaticFiles(directory=\u003ca path that does not exist\u003e)` and records the exact exception type and message. `uv run --with` builds an ephemeral overlay env — it does NOT touch pyproject.toml or uv.lock, so this phase cannot break `uv sync --locked`.",
                  "BELIEF 2 (scope risk 6, unconfirmed): write a ~15-line annotated FastAPI app in the scratch dir and run `uv run --with fastapi --with mypy mypy --strict --warn-unreachable \u003cprobe.py\u003e`. Pass the flags explicitly — `var/` is outside `[tool.mypy] files` (pyproject.toml:65) so the config\u0027s own settings will not apply. Record whether `disallow_untyped_decorators` fires on `@app.get(...)`. If it does, the remedy to record is a correctly annotated handler signature — NOT a per-module override, which AC 8 forbids outright.",
                  "BELIEF 3 (scope risks 4 and 10): in the scratch dir run `npm create vite@latest` for the react-ts template and `npm install`, producing a throwaway package-lock.json. Record the `lockfileVersion` value and the actual `dist/` layout after `npm run build` (whether assets land in `dist/assets/`) — Phase 2\u0027s static-mount design depends on that layout. Local toolchain is MEASURED as node v24.15.0 / npm 11.12.1 (confirmed 2026-08-14).",
                  "BELIEF 4 (scope risk 4): run the three regexes from tests/test_no_leaks.py:26-29 (WINDOWS_PATH, POSIX_HOME, EMAIL) directly against that scratch package-lock.json and package.json. The npm `author` field is the known tripwire for the email check. Record hits, and for each the remedy — a narrowly-justified ALLOWED entry with a written reason, NEVER a weakened regex or a removed suffix.",
                  "BELIEF 5 (scope risk 5): `gitleaks` is MEASURED as NOT installed on this machine (Get-Command returned nothing on 2026-08-14). Either install it (`winget install gitleaks`) and scan the scratch lockfile, or record honestly that the check is deferred to CI\u0027s `secrets` job — which is a blocking required context and runs on the PR before merge, so the worst case is a red PR rather than a leak.",
                  "BELIEF 6 (scope risk 1): `git remote -v` is MEASURED as `https://github.com/jordan-koch/nba2k-rpg.git`, matching ops/README.md lines 12 and 29. Record this as verified. Do NOT run `gh api` — .claude/settings.json line 8 puts it in the ask list; whether GitHub still accepts the JSON unchanged is the user\u0027s step in Phase 7.",
                  "Write the findings into `requests/feature-requests/1.1-app-shell/reviews/preflight.md`, one row per belief, each labelled with the epistemic vocabulary CLAUDE.md requires (measured / verified / inferred / refuted). This file is the phase\u0027s only tracked deliverable.",
                  "Delete nothing from `var/spike/` — it is gitignored and useful for the rest of the build."
              ],
    "acceptance":  [
                       "`requests/feature-requests/1.1-app-shell/reviews/preflight.md` exists and carries a labelled result for all six beliefs, with no belief left at `unconfirmed`.",
                       "`git status --short` shows exactly one new tracked-candidate file (the preflight findings). pyproject.toml and uv.lock are byte-identical to HEAD.",
                       "`uv run pytest -m \"not network\"` is green, `uv run ruff check` and `uv run ruff format --check` exit 0, `uv run mypy` exits 0 — i.e. the probe phase changed nothing that a check can see.",
                       "`uv run pytest tests/test_request_links.py` is green — the new markdown file introduces no dead relative link (write forward-referenced paths like `app/` and `src/rpg_api/` inline or fenced, per the scope\u0027s Authoring rule)."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. Stages only the preflight findings file. Reversible by deletion; nothing depends on it except the plan\u0027s own honesty. Suggested message subject: `docs(1.1): preflight — measure the app-shell\u0027s unconfirmed beliefs`."
}

{
    "name":  "Phase 1 — The backend seam: dependencies, src/rpg_api, /api/health, and the layering guard",
    "goal":  "Land the HTTP seam and ALL of the item\u0027s Python dependency bookkeeping in one shot, so `uv lock` runs exactly once for the whole item. Ends with a FastAPI app whose health payload proves the rpg_api -\u003e rpg_core direction, and a guard test that makes the reverse direction fail a build.",
    "steps":  [
                  "pyproject.toml, one edit pass: replace `dependencies = []` (line 9) and the reservation comment (lines 11-13) with `fastapi` and `uvicorn`; add `httpx` (required by `fastapi.testclient.TestClient`), `pyyaml`, `types-PyYAML` (Phase 5\u0027s guard needs the stubs under mypy strict), and `watchfiles` (reload support without pulling `uvicorn[standard]`) to the dev group at lines 16-21; append `src/rpg_api` to `[tool.hatch.build.targets.wheel].packages` (line 31). Run `uv lock` and stage uv.lock in the same commit — ci.yml:34 runs `uv sync --locked`, which hard-fails on a stale lock.",
                  "Change ci.yml line 47 from `--cov=rpg_core` to add `--cov=rpg_api`. One line, harmless before the web job exists, and it is what makes AC 14\u0027s second half assertable now instead of in Phase 5.",
                  "Create the package: `src/rpg_api/__init__.py` (docstring stating the direction and that it holds no domain logic) and `src/rpg_api/app.py` exposing `create_app(spa_dist: Path) -\u003e FastAPI`. Use `pathlib` throughout — ruff\u0027s PTH rule (pyproject.toml:49) rejects `os.path`. Add NO timestamp fields; ruff\u0027s DTZ rule taxes naive datetimes and Decision 6 already ruled the payload closed.",
                  "Register `GET /api/health` returning `{\"status\": \"ok\", \"version\": rpg_core.__version__, \"spa_built\": \u003cbool\u003e}`. Read the version from the attribute — never re-type the literal — so tests/test_repo_structure.py:46-54 transitively pins the payload. Compute `spa_built` once at construction from `(spa_dist / \"index.html\").is_file()`.",
                  "Create `tests/conftest.py` with a reusable TestClient fixture parameterized on the dist location, so items 1.7-1.11 do not each invent a variant. It must be able to build a client against an arbitrary `tmp_path`.",
                  "Create `tests/test_api_health.py` covering AC 2: status 200, content-type `application/json`, `body[\"status\"] == \"ok\"`, `body[\"version\"] == rpg_core.__version__`, and `isinstance(body[\"spa_built\"], bool)`. No live server, no socket.",
                  "Create `tests/test_layering.py` covering AC 3 as a PURE FUNCTION over a directory root returning violations. Unit-test it twice against `tmp_path` — a fake module containing `import fastapi` must report exactly that file, a clean tree must report none — then assert the real run over `src/rpg_core/` returns zero. This is what proves red-and-green in one `uv run pytest` without mutating tracked source. Deny-list: `fastapi`, `starlette`, `uvicorn`, `rpg_api`. `pydantic` is deliberately ABSENT (ADR 0002 requires DTOs constructible with no HTTP and no UI; that call belongs to item 1.2). The assertion message must cite DESIGN.md §3 by name.",
                  "Append AC 14\u0027s structural test to tests/test_repo_structure.py, following the existing tomllib idiom at lines 46-54: parse pyproject.toml and assert `src/rpg_api` is in the hatch `packages` list, and parse ci.yml\u0027s pytest step to assert a `--cov` flag names `rpg_api`.",
                  "Apply the Phase 0 remedy for BELIEF 2 if it fired — an annotated handler signature, never a `[[tool.mypy.overrides]]` block carving rpg_api out of strict."
              ],
    "acceptance":  [
                       "`uv sync --locked` exits 0 from the tracked lock (AC 1), with `fastapi` and `uvicorn` resolved in uv.lock.",
                       "`uv run pytest tests/test_api_health.py tests/test_layering.py -q` is green (ACs 2 and 3).",
                       "`uv run pytest tests/test_repo_structure.py -q` is green, including the new packaging assertion (AC 14).",
                       "`uv run mypy` exits 0 under the UNCHANGED `[tool.mypy]` block, with zero new `# type: ignore` comments and zero new per-module overrides (AC 8). Verify by grepping the diff for `type: ignore` and for `[[tool.mypy.overrides]]` — a green run bought by loosening strict FAILS this criterion.",
                       "`uv run ruff check` and `uv run ruff format --check` exit 0 over `src/rpg_api` and every new test file (AC 9).",
                       "`uv run pytest -m \"not network\"` is green end to end. `src/rpg_core/__init__.py` is byte-identical to HEAD — the non-goal is that this phase adds no domain logic whatsoever."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. This is the item\u0027s only dependency-and-lockfile commit; pyproject.toml and uv.lock must land together or CI\u0027s `uv sync --locked` fails. Fully reversible: reverting restores an empty dependency list and an app-less repo. Suggested subject: `feat(1.1): FastAPI seam — src/rpg_api, /api/health, layering guard`."
}

{
    "name":  "Phase 2 — Serving the built SPA: both branches, the JSON-404 boundary, and the console script",
    "goal":  "Make the two dist states — absent and present — behave correctly and provably, without a listening socket, and give the served-build mode its one canonical entrypoint. This phase is deliberately separate from Phase 1 because it is where the inferred Starlette behavior from Phase 0 becomes real code.",
    "steps":  [
                  "Extend `create_app(spa_dist)` with the four-step registration order, which is a correctness constraint: (1) the `/api` routes from Phase 1; (2) an explicit `/api/{rest:path}` catch-all returning a JSON 404; (3) the static mount for built assets, registered ONLY when the build predicate is true; (4) the SPA history fallback for unmatched non-`/api` paths.",
                  "Absent branch: when `(spa_dist / \"index.html\")` is not a file, construct NO StaticFiles instance (Phase 0 BELIEF 1 measured what happens otherwise) and make `GET /` return 503 whose body contains the literal build command a cold agent can copy. A fresh clone has no `app/dist/`, so this is the branch every cold agent hits first.",
                  "Present branch: mount the built assets from the layout Phase 0 BELIEF 3 measured (expected `dist/assets/`), and serve `index.html` for `/` and for the history fallback via `FileResponse`.",
                  "Create `tests/test_api_spa.py`: AC 5 (dist pointed at a non-existent `tmp_path` — construction raises nothing, `/api/health` still 200, `/` returns 503 containing the build command), AC 6 (dist pointed at a `tmp_path` containing a known index.html — `/` returns 200, `text/html`, and that file\u0027s bytes), and AC 7 (`GET /api/\u003cunknown\u003e` returns 404 with content-type `application/json`, not HTML). Add a fallback test: an unmatched non-`/api` path returns index.html when the build is present.",
                  "Add `src/rpg_api/__main__.py` with a `main()` that resolves the repo-relative default dist location and runs uvicorn, plus a `[project.scripts]` entry in pyproject.toml pointing at it. Re-run `uv lock`; if the lock is unchanged, commit nothing extra — `uv sync --locked` is the check.",
                  "Document nothing yet — Decision 9 says exactly one canonical way to run the served build gets documented, and that documentation lands in Phase 6 so it lands once."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_api_spa.py -q` is green — all four behaviors (ACs 5, 6, 7 and the fallback) proven against `tmp_path` with no listening socket and no built SPA present.",
                       "`uv run pytest tests/test_api_health.py -q` still green — the new registration order did not shadow the health route.",
                       "`uv run mypy` exits 0 and `uv run ruff check` / `uv run ruff format --check` exit 0 (ACs 8, 9 hold cumulatively).",
                       "`uv sync --locked` exits 0 — the `[project.scripts]` addition did not invalidate the lock.",
                       "The console script resolves: `uv run \u003cscript\u003e --help` (or an equivalent non-blocking invocation) exits without ImportError. Full AC 19 — that it actually serves the built app — is proven by the CI smoke step in Phase 5 and by the user in Phase 7, because it needs a real build.",
                       "`uv run pytest -m \"not network\"` is green end to end."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. Reversible and independently shippable: the backend is complete and fully tested with no frontend in the repo at all. Suggested subject: `feat(1.1): serve the built SPA — both dist branches, JSON-404 boundary, console script`."
}

{
    "name":  "Phase 3 — The frontend toolchain: app/ scaffold, strict TypeScript, eslint, the Vite proxy",
    "goal":  "Stand up `app/` with a check posture that MATCHES the Python half from its first commit, and prove it with exactly the commands CI will run. No behavior yet — this phase is about the toolchain being real and strict, so Phase 4\u0027s code lands into a gate rather than beside one.",
    "steps":  [
                  "Scaffold Vite + React + TypeScript in `app/` at the repo root — the location .gitignore lines 66-68 and .gitattributes line 41 already anticipate. Use the layout Phase 0 BELIEF 3 measured.",
                  "`app/package.json`: mark it `\"private\": true` and fix the version at a placeholder (the panel dropped the three-way version parity test on the grounds that a private SPA\u0027s version is meaningless). REMOVE any `author` field carrying an email — tests/test_no_leaks.py:29 is a blocking check. Every script must be a SINGLE command invocation with NO shell operators: `\u0026\u0026`, `rm -rf`, `cp`, and POSIX inline env prefixes all work on ubuntu-latest CI and FAIL in Windows PowerShell 5.1, which has no `\u0026\u0026` at all (scope risk 8).",
                  "Scripts to define: `dev`, `build`, `typecheck`, `lint`, `test`, plus the negative-typecheck pair from AC 11.",
                  "`app/tsconfig.json`: `strict: true` PLUS `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch` — bringing the frontend to comparable severity with mypy strict + warn_unreachable. The config lives INSIDE `app/` with file scope limited to `app/`; a repo-root config would immediately start reporting on `.claude/skills/**/*.js`, which the scope excludes by name.",
                  "eslint + typescript-eslint + eslint-plugin-react-hooks (Decision 2, taken against the panel\u0027s oxlint recommendation because rules-of-hooks violations are real runtime bugs and that value grows sharply at items 1.7-1.11). Config inside `app/`, scoped to `app/`. NO prettier or other formatter gate — that is a visible default, not an oversight.",
                  "`app/vite.config.ts`: dev-server proxy mapping `/api` to the backend at the IPv4 LITERAL `127.0.0.1`, never `localhost` (scope risk 9 — on Windows `localhost` can resolve to `::1` while uvicorn binds IPv4, producing an ECONNREFUSED that looks exactly like a dead backend). This proxy is the entire CORS story; no CORS middleware is added anywhere.",
                  "Real page title and favicon instead of the Vite template defaults (identity, not design — `*.ico binary` is already reserved at .gitattributes line 35). Add a repo-root `.editorconfig`: two toolchains, one Windows author, and `* text=auto eol=lf` at .gitattributes line 3.",
                  "Commit `app/package-lock.json`. BEFORE running the leak test, stage the new tree — `git add --intent-to-add app/` — because tests/test_no_leaks.py:58-71 reads `git ls-files`, i.e. the INDEX, so untracked files are invisible to it and a clean run on unstaged files proves nothing.",
                  "Append the gitignore guard test to tests/test_repo_structure.py, mirroring `test_scratch_root_is_gitignored` (lines 83-92) and using `_git_check_ignore` (lines 24-34): assert `app/dist/` and `node_modules/` are ignored, so nobody later adds an `!app/**` carve-out."
              ],
    "acceptance":  [
                       "From `app/`: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run build` each exit 0, and `app/dist/index.html` exists afterwards (AC 10). These are exactly the steps Phase 5\u0027s CI job runs, so a green local run predicts a green CI run.",
                       "`npm run check:negative` (the AC 11 wrapper) exits 0, meaning the committed ill-typed fixture — excluded from `npm run build` — made `tsc` exit non-zero. This is what proves `strict` is actually engaged rather than a default-generated config that checks nothing.",
                       "With `app/` staged via `git add --intent-to-add`, `uv run pytest tests/test_no_leaks.py -q` is green (AC 13). If a pattern trips, the remedy is a narrowly-justified `ALLOWED` entry (tests/test_no_leaks.py:32-35) with a written reason — NEVER a weakened regex or a removed suffix.",
                       "`uv run pytest tests/test_repo_structure.py -q` is green, including the new app/dist + node_modules gitignore guard.",
                       "`git status --short` shows no `node_modules/` and no `app/dist/` as untracked candidates — the .gitignore rules are doing their job.",
                       "`uv run pytest -m \"not network\"` is green; `uv run ruff check` / `uv run ruff format --check` / `uv run mypy` all exit 0 (the Python half is untouched)."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. This is the commit that introduces package-lock.json to the public repo, so run the leak test against the STAGED tree first. Reversible by deleting `app/`. Suggested subject: `feat(1.1): app/ scaffold — Vite + React + strict TS, eslint, dev proxy`."
}

{
    "name":  "Phase 4 — The frontend behavior: typed client, status page, unreachable panel, two Vitest tests",
    "goal":  "Make the page actually cross the seam and prove the one piece of real branching logic it has. Separated from Phase 3 so that if the toolchain is fine and the behavior is wrong (or vice versa), exactly one of the two reverts.",
    "steps":  [
                  "Create `app/src/api/client.ts` — a small typed fetch wrapper with a HAND-WRITTEN `Health` interface, the one place the frontend talks to the backend. This is explicitly NOT the deferred OpenAPI codegen contract (a non-goal until item 1.8 / ADR 0002); it is the seam codegen would later slot into.",
                  "Build the single status page: it calls `/api/health` on the Vite origin (a relative path, so the proxy handles dev and same-origin handles the built mode) and renders status and version. That page is the ENTIRE UI. Legibility only — no component library, theme system, CSS framework, or design tokens.",
                  "Build the backend-unreachable state: on a rejected fetch, render a legible panel NAMING the start command. Not polish — \u0027I opened the page and it\u0027s blank\u0027 is the top cold-start confusion in a two-process app.",
                  "Add Vitest + Testing Library with exactly TWO tests (AC 12, Decision 1): the status page renders the fetched version, and the unreachable panel renders on a rejected fetch. Two, not more — the scope caps this deliberately.",
                  "GUARD AGAINST THE ITEM\u0027S MOST LIKELY FAILURE: scope risk 12. The pull to make the status page show something — a career list, a stub player, a fake XP number — is the single most likely way this item stops being a shell. `src/rpg_core/` must still be a docstring and a version string when this lands; there must be no `careers/`, no `rulesets/`, no `datasets/`, no SQLite, and no file written under `var/` by application code.",
                  "Add no client-side router, no global state library (Redux/Zustand/TanStack Query), and no second page — item 1.10 brings the router, and structuring an app before it has surfaces pre-decides the structure blind."
              ],
    "acceptance":  [
                       "From `app/`: `npm run test` is green with EXACTLY two Vitest tests (AC 12). Count them — the criterion is a count, not a floor.",
                       "From `app/`: `npm run typecheck`, `npm run lint`, `npm run build` still exit 0, and `npm run check:negative` still exits 0.",
                       "`uv run pytest -m \"not network\"` is green — the backend suite is unaffected.",
                       "NON-GOAL CHECK, run explicitly: `git status --short` and `git diff --stat` show no `careers/`, `rulesets/`, `datasets/`, or `var/` paths, and `src/rpg_core/__init__.py` is byte-identical to HEAD.",
                       "With `app/` staged, `uv run pytest tests/test_no_leaks.py -q` is green over the new .ts/.tsx files (they are in TEXT_SUFFIXES at tests/test_no_leaks.py:38-55)."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. Suggested subject: `feat(1.1): status page — typed health client, unreachable panel, two Vitest tests`."
}

{
    "name":  "Phase 5 — CI: the third job, the required-check contexts, the jobs-guard, dependabot, and the real-server smoke",
    "goal":  "Make a broken frontend turn a PR red the same way a broken backend does — and make the tracked half of the required-check wiring impossible to get silently wrong. This is the phase that addresses the item\u0027s HEADLINE risk.",
    "steps":  [
                  "Add a third job to ci.yml, parallel with `python` and `secrets`, with a stable display name (e.g. `Web app`). Steps: checkout, `actions/setup-node` pinned to major 24 (matching the MEASURED local v24.15.0 — a lockfileVersion difference between npm majors produces a lockfile that installs locally and fails `npm ci` in CI, with an error pointing at a package rather than at the version skew, scope risk 10) with npm dependency caching keyed on `app/package-lock.json`, then `npm ci` / typecheck / lint / test / build with `working-directory: app`. Caching matters because `concurrency: cancel-in-progress` (ci.yml:10-12) re-runs the job on every push.",
                  "Add the real-server smoke step to the SAME job (AC 18, Decision 8, taken against the panel\u0027s recommendation): after the build, add setup-uv + `uv sync --locked`, start the console script from Phase 2 in the background against the built dist, then curl `/` (expect 200 + HTML) and `/api/health` (expect 200 + JSON). Use a BOUNDED READINESS POLL, never a fixed sleep — `curl --retry-connrefused --retry \u003cn\u003e --retry-delay 1 --max-time \u003cs\u003e` is the mechanism (scope risk 14 flags this step as the item\u0027s flake vector). This step is the only check that exercises uvicorn, the static mount against a real filesystem, and the built artifact; TestClient exercises none of them. It also discharges AC 19.",
                  "Add the new job\u0027s DISPLAY NAME to `required_status_checks.contexts` in ops/branch-protection.json (line 4) IN THE SAME COMMIT as the workflow change. Note loudly in the PR description that the file is inert until re-applied with `gh api -X PUT`.",
                  "Create `tests/test_ci_contexts.py` (AC 4): parse ci.yml with `yaml.safe_load`, collect `jobs.*.name`, and assert that set EQUALS the contexts array. Equality, not containment — containment passes while a typo\u0027d context name (\u0027Web app\u0027 vs \u0027Web App\u0027) makes every PR hang forever on a check that never reports, the failure ops/README.md:20-24 warns about. The failure message must name WHICH SIDE carries the extra entry. Add a negative assertion proving the parser is structure-aware: a STEP-level name (e.g. \u0027Gitleaks\u0027 at ci.yml:58, or \u0027Install\u0027 at ci.yml:30) must NOT enter the set. `pyyaml` and `types-PyYAML` are already in the dev group from Phase 1.",
                  "Discharge .github/dependabot.yml line 30: add a `package-ecosystem: \"npm\"` entry pointing at the SPA directory, mirroring the uv entry\u0027s monthly schedule and patch-ignore posture (lines 16-28), and DELETE the placeholder comment (AC 15).",
                  "Do NOT add `paths-ignore` or any path filter to any job. With `required_status_checks.strict: true` and named contexts, a filtered job that never reports makes PRs wait forever — the exact silent-hang failure this phase exists to prevent."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_ci_contexts.py -q` is green, including the negative step-name assertion (AC 4).",
                       "Manually cross-read: the job `name:` string in ci.yml and the new entry in ops/branch-protection.json:4 are character-identical. The guard test proves it, but read them once anyway — this is the item\u0027s headline risk.",
                       "`uv run pytest -m \"not network\"` is green; `uv run mypy` exits 0 with `types-PyYAML` satisfying the strict-mode stub requirement for the new test.",
                       "`uv run pytest tests/test_no_leaks.py tests/test_repo_structure.py tests/test_request_links.py -q` is green (AC 16 — existing structural guards survive).",
                       "Every npm script the CI job invokes has already been run locally and exited 0 in Phases 3-4 — the local run is what predicts the CI run.",
                       "The dependabot npm entry exists and the line-30 placeholder comment is gone (AC 15)."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. The workflow change and the branch-protection contexts change MUST be in this one commit; splitting them is how the guard test\u0027s whole purpose gets defeated. Note in the PR description that ops/branch-protection.json is inert until the user re-applies it. Suggested subject: `ci(1.1): Web app job, required context, jobs-guard, npm dependabot, real-server smoke`."
}

{
    "name":  "Phase 6 — Stop the docs lying, and prove it mechanically",
    "goal":  "Goal 7 has no pass/fail check unless one is written, and delegating it to /commit\u0027s judgment gate is how a repo ends up with a README that says \u0027no application code yet\u0027 next to an application. This phase makes documentation drift a test failure.",
    "steps":  [
                  "ops/README.md: add a Node-toolchain section beside the uv one (lines 32-63), stating node major 24 / npm 11 as measured, and the `npm ci` lockfile rule with the SAME sharpness the uv section gives `uv sync --locked` at lines 54-57 — `npm ci` fails when package.json and package-lock.json disagree. Document BOTH run modes: dev (two commands in two terminals, per Decision 4 — no launcher, because a Node process-runner receiving Ctrl+C in PowerShell can orphan the Python child holding the port, so the next run dies EADDRINUSE) and served-build (the console script, and ONLY the console script — Decision 9 says exactly one canonical incantation gets documented). Add the note that `spa_built` is evaluated at construction, so a server started before `npm run build` must be restarted.",
                  "README.md: delete the \u0027No application code yet\u0027 banner (line 12), add `app/` and `src/rpg_api/` to the project map (lines 51-72), remove the web app from the \u0027don\u0027t exist yet\u0027 sentence at line 72, and extend the Setup block (lines 74-80) with the Node half.",
                  "CLAUDE.md: add `app/` and `src/rpg_api/` to the project map (lines 49-63) and correct line 66 so it no longer claims the web app doesn\u0027t exist. CLAUDE.md has a hard line budget — this is an EDIT, not an append. `src/rpg_core/` line 58 still correctly says \u0027Empty until Phase 1\u0027 only if it is still empty; it is, so leave it.",
                  "Fix tests/test_no_leaks.py line 37: the docstring claims \u0027Binary and lockfiles are skipped\u0027, which is TRUE of uv.lock (no scanned suffix) and FALSE of package-lock.json (`.json` is in TEXT_SUFFIXES at line 41). This item is what makes the statement wrong, so this item fixes it.",
                  "Add AC 17\u0027s structural test to tests/test_repo_structure.py, using the same file-content idiom the module already uses for \u0027the repo and its documents agree\u0027: assert README.md no longer contains \u0027No application code yet\u0027; assert CLAUDE.md\u0027s project map contains both `app/` and `src/rpg_api/` and no longer states the web app doesn\u0027t exist; assert ops/README.md contains a Node-toolchain heading and both run-mode commands.",
                  "Do NOT hand-edit ROADMAP.md row 1.1 or the Phase 1 Status line at 151-157. /commit maintains those against the diff (CLAUDE.md\u0027s convention, and the /commit skill\u0027s ROADMAP step) — hand-editing them is exactly the ad-hoc maintenance the convention forbids.",
                  "Run gitleaks locally once before the final push if it is available (Phase 0 BELIEF 5 measured it as absent on this machine). If it trips on package-lock.json\u0027s high-entropy sha512 integrity strings, remediate with specific fingerprints in `.gitleaksignore` or a scoped path allowlist, EACH with a written reason, mirroring the ALLOWED-entry discipline. Do not disable the rule wholesale."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_repo_structure.py -q` is green, including the new documentation assertions (AC 17).",
                       "`uv run pytest -m \"not network\"` is green — the FULL suite, which is now the union of the three pre-existing guard modules plus test_api_health, test_api_spa, test_layering, test_ci_contexts, and conftest.",
                       "`uv run ruff check`, `uv run ruff format --check`, `uv run mypy` all exit 0.",
                       "From `app/`: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run test`, `npm run build`, `npm run check:negative` all exit 0 — the complete CI-parity sweep, run once at the end.",
                       "`uv run pytest tests/test_request_links.py -q` is green: every relative link in every touched `.md` under `requests/` resolves. Newly-created paths (`app/`, `src/rpg_api/`, `tests/conftest.py`) are written inline or fenced, never as markdown links — and note that inline backticks do NOT exempt a link, only 3+ backtick fences do (tests/test_request_links.py:26).",
                       "Grep the final diff for `type: ignore`, `[[tool.mypy.overrides]]`, `# noqa`, and `eslint-disable`: zero new occurrences, or each one individually justified in the commit message. A green run bought by loosening a gate fails ACs 8 and 11 retroactively."
                   ],
    "commit_note":  "CHECKPOINT — hand to the user for `/commit`. This is the commit where /commit\u0027s ROADMAP step advances row 1.1 and the Phase 1 Status line; let the skill do it. Suggested subject: `docs(1.1): the repo has an application now — README, CLAUDE.md, ops/README.md, doc guard`."
}

{
    "name":  "Phase 7 — USER-RUN acceptance and the ordered merge gate",
    "goal":  "Prove the four things no agent can prove — the dev proxy, the built seam, the failure state, and the actual activation of the new required check — and do the last one in an order that does not let this exact PR be the one that lands with a red frontend. This phase is the user\u0027s; the agent\u0027s job is to have written it into the PR description.",
    "steps":  [
                  "AC 20 — THE DEV SEAM. Two commands in two terminals: uvicorn with reload (backend), and `npm run dev` from `app/`. Open the Vite URL. The page renders the version string, and the browser network tab shows `/api/health` served on the VITE ORIGIN — not a cross-origin call to the API port. The origin is what actually proves the proxy, and therefore the no-CORS-middleware decision; a rendered version string alone does not.",
                  "AC 21 — THE BUILT SEAM. `npm run build` from `app/`, then the console script alone with NO Vite dev server running. The same page renders at the uvicorn origin.",
                  "AC 22 — THE FAILURE STATE. With the page open, stop the backend. The page renders the legible \u0027backend unreachable\u0027 panel naming the start command — not a blank screen and not an uncaught console error.",
                  "AC 23 — REQUIRED-CHECK ACTIVATION, AS AN ORDERED GATE BEFORE MERGE. (1) Push the branch and open the PR; let the new job report ONCE and confirm the context name verbatim against ops/branch-protection.json:4. (2) Run `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json` — owner/repo VERIFIED against `git remote -v` on 2026-08-14 as `jordan-koch/nba2k-rpg`, matching ops/README.md lines 12 and 29. (3) Confirm the new check shows as REQUIRED on the open PR. (4) Only then merge.",
                  "SEQUENCING IS THE POINT: re-applying protection AFTER merge guarantees that the PR introducing the job is exactly the one that can land with a red frontend. An agent structurally cannot do step 2 — `gh api *` is in .claude/settings.json\u0027s ask list at line 8 — and editing the JSON alone never changes GitHub.",
                  "The agent\u0027s deliverable here is the PR description: it must carry these four checks as a checklist, with the ordered gate written out, plus the loud call-out that ops/branch-protection.json is inert until re-applied.",
                  "Merge, and the post-merge branch prune, stay the user\u0027s. If pruning later, the check that actually works in this repo is content equality (`git fetch origin; git diff \u003cbranch\u003e origin/main --stat` — empty output means merged), because PRs land as squash merges and `git branch -d` refuses every already-merged branch here."
              ],
    "acceptance":  [
                       "USER-RUN: the Vite-origin `/api/health` request is visible in the network tab (AC 20) — origin confirmed, not just the version string.",
                       "USER-RUN: the built mode renders at the uvicorn origin with no Vite process running (AC 21).",
                       "USER-RUN: stopping the backend produces the named-command unreachable panel (AC 22).",
                       "USER-RUN: the new job appears as a REQUIRED check on the open PR before the merge button is used (AC 23), and all three contexts report green.",
                       "The PR description contains the ordered four-step gate verbatim, so the sequence survives being done tomorrow instead of today."
                   ],
    "commit_note":  "NO COMMIT — this phase is verification and the merge gate. If a user-run check fails, the fix goes back through the phase that owns it (AC 20/22 -\u003e Phase 4 or Phase 3\u0027s proxy config; AC 21 -\u003e Phase 2; AC 23 -\u003e Phase 5) and comes back through `/commit`. The merge and the `gh api -X PUT` re-apply are the user\u0027s alone."
}

### testing

HOW THE WHOLE THING IS VERIFIED

Every phase ends on the same green local run before it is handed to `/commit`: `uv run pytest -m "not network"`, `uv run ruff check`, `uv run ruff format --check`, `uv run mypy` — the same four commands ops/README.md lines 64-73 documents CI running, in the same order. From Phase 3 onward the frontend sweep joins it, run from `app/`: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run test`, `npm run build`, `npm run check:negative`. Those are exactly the steps the new CI job runs, which is the whole reason a green local run predicts a green CI run.

PER-CRITERION SELECTORS (the cold agent's map from acceptance criterion to command)

- AC 1 (lock) -> `uv sync --locked`
- AC 2 (health payload) -> `uv run pytest tests/test_api_health.py`
- AC 3 (layering guard) -> `uv run pytest tests/test_layering.py`
- AC 4 (CI jobs == contexts, set equality + negative step-name) -> `uv run pytest tests/test_ci_contexts.py`
- ACs 5, 6, 7 (absent dist / present dist / JSON 404) -> `uv run pytest tests/test_api_spa.py`
- AC 8 (mypy strict, no escape hatches) -> `uv run mypy` PLUS a diff grep for `type: ignore` and `[[tool.mypy.overrides]]`
- AC 9 (ruff) -> `uv run ruff check` and `uv run ruff format --check`
- AC 10 (frontend toolchain) -> `npm ci && npm run typecheck && npm run lint && npm run build` run as four separate PowerShell invocations, because Windows PowerShell 5.1 has no `&&`
- AC 11 (strict actually engaged) -> `npm run check:negative`
- AC 12 (exactly two Vitest tests) -> `npm run test`, and count the reported test total
- AC 13 (leak guards over frontend files) -> `git add --intent-to-add app/` THEN `uv run pytest tests/test_no_leaks.py`
- ACs 14, 17 and the app-gitignore guard -> `uv run pytest tests/test_repo_structure.py`
- AC 15 (dependabot npm) -> read .github/dependabot.yml; the placeholder comment at line 30 must be gone
- AC 16 (existing guards survive) -> `uv run pytest tests/test_repo_structure.py tests/test_request_links.py`
- ACs 18, 19 (real server, console script) -> the CI smoke step in the Web app job, plus the user's Phase 7 run
- ACs 20-23 -> USER-RUN, Phase 7. The acceptance panel must not claim these.

THE TWO TESTING SUBTLETIES THAT WILL BITE

1. `tests/test_no_leaks.py` scans the GIT INDEX, not the working tree — `_tracked_text_files` at lines 58-71 shells out to `git ls-files`. A brand-new untracked `app/package-lock.json` is invisible to it, so running the leak test before staging produces a green that proves nothing. Stage with `git add --intent-to-add app/` first. This is the single most likely way this item's public-repo guard gets bypassed by accident.

2. `tests/test_request_links.py` strips only FENCED blocks (3+ backticks, blockquoted is fine) via FENCED_BLOCK at line 26. Inline backticks do NOT exempt a markdown link. Since this item CREATES `app/`, `src/rpg_api/`, `app/dist/`, and `tests/conftest.py`, any markdown link to one of them written before it exists turns CI red on the very PR that lands the work — which is why the scope's Authoring rule (PROJECT_SCOPE.md lines 5-18) is load-bearing and must be carried into every artifact this item produces.

RED-BEFORE-GREEN WITHOUT MUTATING SOURCE

Two criteria demand proof that a guard actually fails when it should, and both are structured to prove it WITHOUT editing tracked source. AC 3's layering guard is a pure function over a directory root, unit-tested against a `tmp_path` fake containing `import fastapi` (must report exactly that file) and a clean `tmp_path` (must report none), with the real assertion pointed at `src/rpg_core/`. AC 11's negative typecheck is a COMMITTED ill-typed fixture excluded from `npm run build`, checked by a dedicated script asserted to exit non-zero. One `uv run pytest` and one `npm run check:negative` prove red-and-green.

REGRESSION SAFETY

Three pre-existing guard modules must stay green at every checkpoint and none of them may be weakened to accommodate this item: tests/test_repo_structure.py (the version pin at 46-54 now transitively covers the health payload), tests/test_no_leaks.py (a tripping pattern gets a narrowly-justified ALLOWED entry with a written reason — never a weakened regex, never a removed suffix), and tests/test_request_links.py. Coverage is extended rather than left to rot: ci.yml line 47 gains `--cov=rpg_api`, without which the number quietly stops describing the codebase (no `fail-under` is configured, so it fails silently by definition).

The strongest regression check in this item is a NON-GOAL check, and it is worth running explicitly at Phase 4 and again at Phase 6: `git diff --stat` against the merge base must show no `careers/`, no `rulesets/`, no `datasets/`, no `var/`, and `src/rpg_core/__init__.py` byte-identical to HEAD. Scope risk 12 names it — the status page being boring is the deliverable, and the pull to make it show a career, a stub player, or a fake XP number is the most likely way this item stops being a shell.

### risks

HEADLINE — the silent-green merge. ops/branch-protection.json lists contexts by CI job DISPLAY NAME (line 4) and the file is inert until re-applied with `gh api -X PUT`. Symptom: a PR merges with a red frontend job and nothing complains, indefinitely. The mitigation is split by construction: the AC 4 guard test covers the tracked half (with set equality, because containment passes while a typo'd name makes every PR hang forever on a check that never reports), and the AC 23 ordered user-run gate covers the applied half. VERIFIED 2026-08-14: `git remote -v` returns `https://github.com/jordan-koch/nba2k-rpg.git`, matching ops/README.md lines 12 and 29. STILL UNCONFIRMED: whether GitHub's protection API accepts the current JSON unchanged — it has not been re-applied since Phase 0, and only the user can test that (`gh api *` is in .claude/settings.json's ask list at line 8).

Omitting `src/rpg_api` from the hatch packages list (pyproject.toml:31) fails ONLY at runtime. `pythonpath = ["src"]` (pyproject.toml:73) puts the package on the path for tests regardless — every test passes, CI goes green, and the console script fails with ModuleNotFoundError on an installed environment. The sneakiest failure in the item, and the test suite structurally cannot otherwise see it. Hence AC 14, landed in Phase 1 alongside the packages edit.

Stale lockfiles, twice over. `uv sync --locked` (ci.yml:34) hard-fails rather than re-resolving, and `npm ci` fails when package.json and package-lock.json disagree. Phase 1 does ALL Python dependency work in one commit specifically so `uv lock` runs once; any later pyproject edit must be followed by `uv lock` and a `uv sync --locked` check before the checkpoint.

tests/test_no_leaks.py now scans frontend files and is a blocking public-repo guard. Two concrete tripwires: a package.json carrying an `author` email fails the EMAIL check (line 29), and any Windows-generated config writing an absolute path fails WINDOWS_PATH (line 26). INFERRED, not measured: npm lockfileVersion 3 entries carry registry URLs and integrity hashes rather than local paths, so it will probably pass. Phase 0 measures this against a scratch lockfile before it becomes a tracked artifact. Compounding trap: the test reads the git INDEX, so an unstaged run is a false green.

gitleaks — the other required check — is unassessed, and MEASURED as not installed on this machine (Get-Command returned nothing, 2026-08-14). The `secrets` job scans full history with `fetch-depth: 0` (ci.yml:53-56) and blocks merge, and the repo has no .gitleaks.toml or .gitleaksignore. This item adds a package-lock.json full of high-entropy base64 sha512 integrity strings to that scan. Judged lower-probability than it sounds — integrity hashes do not usually match credential rules — and the honest fallback is that CI's blocking check catches it on the PR, so the worst case is a red PR rather than a leak.

mypy strict over FastAPI. `disallow_untyped_decorators` against route decorators is the classic friction point; FastAPI ships py.typed so annotated handlers should pass, but it is unconfirmed until run — which is Phase 0's BELIEF 2. THE FAILURE MODE TO REFUSE is a per-module override quietly carving rpg_api out of strict on its first day: it is the exact asymmetry this item exists to prevent on the frontend side, and AC 8 pins it. The correct remedy is an annotated handler signature.

Mounting a missing app/dist/. INFERRED: Starlette's StaticFiles raises at CONSTRUCTION when the directory is absent, so a fresh clone would get an import-time traceback instead of an app. This is why the dist path must be an injectable factory argument (AC 5) and why the mount is registered only when the build predicate holds. Phase 0 BELIEF 1 measures the exact exception before Phase 2 codes against it.

Windows/Linux parity in npm scripts. The daily shell is PowerShell 5.1, which has NO `&&` at all; CI is ubuntu-latest. Any package.json script using `&&`, `rm -rf`, `cp`, or a POSIX inline env-var prefix works in CI and fails locally. Keep every script to a single command invocation with no shell operators — including the AC 11 negative-typecheck wrapper, which is why it is a small Node script rather than a shell one-liner.

Windows/Node IPv6 resolution. A Vite proxy targeting `http://localhost:PORT` can resolve to `::1` on Windows while uvicorn binds 127.0.0.1, producing an ECONNREFUSED that looks EXACTLY like the backend being down while it is running fine. Pin the proxy target to the IPv4 literal. This will burn an hour if it is not pinned, because the symptom points at the wrong process.

Node toolchain drift. Local is MEASURED at node v24.15.0 / npm 11.12.1 (2026-08-14); CI pins a major. A lockfileVersion difference between npm majors yields a lockfile that installs locally and fails `npm ci` in CI, with an error naming a package rather than the version skew. Pin CI to major 24 to match. Decision: a pinned major in the workflow plus one line in ops/README.md, NOT a .nvmrc or engines field — a version file pins CI while the Windows developer silently drifts, which is a false sense of enforcement for one more tracked file.

Coverage silently stops meaning anything. Left unchanged, `--cov=rpg_core` (ci.yml:47) simply omits rpg_api. Not a failure — no fail-under is configured — just a number that quietly stops describing the codebase. The one-line edit lands in Phase 1 so AC 14's second half is assertable from the start.

SCOPE LEAKAGE INTO ITEM 1.2 — the highest-probability way this item fails on its own terms. The status page is boring by design, and the pull to make it show something (a career list, a stub player, a fake XP number) is the most likely way this stops being a shell. The explicit guard is the non-goal check in Phases 4 and 6: src/rpg_core/__init__.py byte-identical to HEAD, and no careers/, rulesets/, datasets/, or var/ paths in the diff.

npm supply chain in a public repo. `npm ci` for a Vite/React toolchain runs install scripts (esbuild fetches a platform binary) and pulls a transitive tree orders of magnitude larger than the four-package Python dev group. Mitigations are the committed lockfile and the dependabot entry; no version of this item avoids the exposure, and the honest position is to record it rather than claim it is handled.

The CI smoke step is a flake vector — Decision 8 took it against the panel's recommendation, with cost removed but flake risk retained. It needs Python and Node in one job plus readiness handling. Plan it with an explicit bounded readiness poll (`curl --retry-connrefused --retry <n> --retry-delay 1 --max-time <s>`), never a fixed sleep. If it flakes twice in a row, the correct response is to tighten the poll, not to delete the only check that exercises uvicorn and the real static mount.

Out of scope but worth recording before item 2.1: .gitignore line 63 has a blanket `build/` rule matching a directory named build at ANY depth, which will silently shadow the `build/build-*.py` builder pattern CLAUDE.md says Phase 2 should follow. Line 62's blanket `dist/` behaves the same way. Not this item's problem — but nothing this item needs may live under a directory named build or dist outside app/.

Route registration order is easy to get wrong and produces a confusing symptom. If the SPA history fallback is registered before the `/api/{rest:path}` JSON-404 handler, an unknown API path returns an HTML page with status 200 — AC 7 exists precisely to catch this, and a cold agent adding endpoints at items 1.7-1.11 will inherit whatever order this item establishes.

### files_to_touch

{
    "path":  "pyproject.toml",
    "change":  "MODIFY (Phase 1, plus a scripts entry in Phase 2). Replace line 9\u0027s `dependencies = []` and the reservation comment at 11-13 with fastapi + uvicorn; add httpx, pyyaml, types-PyYAML, watchfiles to the dev group (15-21); append `src/rpg_api` to the hatch packages list (line 31); add a `[project.scripts]` console entrypoint. Do NOT touch `[tool.mypy]` (61-65) — AC 8 forbids relaxing strict."
}

{
    "path":  "uv.lock",
    "change":  "MODIFY (regenerated by `uv lock`, Phase 1). Must land in the SAME commit as the pyproject dependency change or ci.yml:34\u0027s `uv sync --locked` hard-fails."
}

{
    "path":  "src/rpg_api/__init__.py",
    "change":  "CREATE (Phase 1). Package docstring stating the rpg_api -\u003e rpg_core direction and that it holds no domain logic."
}

{
    "path":  "src/rpg_api/app.py",
    "change":  "CREATE (Phase 1, extended Phase 2). `create_app(spa_dist: Path) -\u003e FastAPI` — the injectable dist location, `GET /api/health` returning status/version/spa_built, the `/api/{rest:path}` JSON-404 handler, the conditional static mount, and the SPA history fallback, in that registration order."
}

{
    "path":  "src/rpg_api/__main__.py",
    "change":  "CREATE (Phase 2). The `main()` behind `[project.scripts]` — the served-build mode\u0027s ONE canonical entrypoint (Decision 9)."
}

{
    "path":  "tests/conftest.py",
    "change":  "CREATE (Phase 1). The reusable TestClient fixture parameterized on the injectable dist location. Items 1.7-1.11 each need it; writing it once beats five agents inventing five variants."
}

{
    "path":  "tests/test_api_health.py",
    "change":  "CREATE (Phase 1). AC 2 — status 200, application/json, status/version/spa_built with version read from rpg_core.__version__."
}

{
    "path":  "tests/test_api_spa.py",
    "change":  "CREATE (Phase 2). ACs 5, 6, 7 plus the history-fallback case, all against tmp_path with no listening socket."
}

{
    "path":  "tests/test_layering.py",
    "change":  "CREATE (Phase 1). AC 3 — the pure-function import guard, unit-tested red and green against tmp_path, asserted zero over src/rpg_core/. Failure message cites DESIGN.md §3 by name. Deny-list: fastapi, starlette, uvicorn, rpg_api — NOT pydantic (ADR 0002; that is item 1.2\u0027s call)."
}

{
    "path":  "tests/test_ci_contexts.py",
    "change":  "CREATE (Phase 5). AC 4 — yaml.safe_load over ci.yml, set EQUALITY against ops/branch-protection.json contexts, a failure message naming which side has the extra entry, and a negative assertion that a step-level name does not enter the set."
}

{
    "path":  "tests/test_repo_structure.py",
    "change":  "MODIFY (Phases 1, 3, 6). Append: AC 14\u0027s hatch-packages + --cov assertion; the app/dist + node_modules gitignore guard using `_git_check_ignore` (24-34) in the style of `test_scratch_root_is_gitignored` (83-92); AC 17\u0027s documentation assertions. Change nothing existing."
}

{
    "path":  "tests/test_no_leaks.py",
    "change":  "MODIFY (Phase 6, docstring only). Line 37\u0027s \u0027Binary and lockfiles are skipped\u0027 is true of uv.lock and false of package-lock.json — this item makes it wrong, so this item fixes it. Only add an ALLOWED entry (32-35) if Phase 0 measured a real trip, and then with a written reason."
}

{
    "path":  ".github/workflows/ci.yml",
    "change":  "MODIFY (Phases 1 and 5). Line 47 gains `--cov=rpg_api`; a third job (setup-node pinned to major 24 with npm caching, npm ci/typecheck/lint/test/build at working-directory app, then the bounded-readiness-poll real-server smoke) joins `python` and `secrets`. NO paths-ignore filter on any job."
}

{
    "path":  "ops/branch-protection.json",
    "change":  "MODIFY (Phase 5). Append the new job\u0027s display name to `required_status_checks.contexts` (line 4), character-identical to ci.yml\u0027s `name:`, in the SAME commit as the workflow change. Inert until the user re-applies it with `gh api -X PUT`."
}

{
    "path":  ".github/dependabot.yml",
    "change":  "MODIFY (Phase 5). Add the npm ecosystem entry pointing at the SPA directory, mirroring the uv entry\u0027s monthly + patch-ignore posture (16-28), and DELETE the line-30 placeholder comment (AC 15)."
}

{
    "path":  "app/package.json",
    "change":  "CREATE (Phase 3). private: true, placeholder version, NO author email (tests/test_no_leaks.py:29), and every script a single command invocation with no shell operators (PowerShell 5.1 has no `\u0026\u0026`)."
}

{
    "path":  "app/package-lock.json",
    "change":  "CREATE (Phase 3). Committed — .gitattributes:41 already reserves it as linguist-generated. Stage with `git add --intent-to-add` before running the leak test, or the test scans nothing."
}

{
    "path":  "app/tsconfig.json",
    "change":  "CREATE (Phase 3). strict: true plus noUncheckedIndexedAccess, noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch. Lives INSIDE app/, scoped to app/ — a repo-root config would start reporting on .claude/skills/**/*.js."
}

{
    "path":  "app/vite.config.ts",
    "change":  "CREATE (Phase 3). Dev-server proxy mapping /api to the IPv4 LITERAL 127.0.0.1, never localhost (scope risk 9). This is the entire CORS story."
}

{
    "path":  "app/src/api/client.ts",
    "change":  "CREATE (Phase 4). Small typed fetch wrapper with a hand-written `Health` interface — the seam OpenAPI codegen would later slot into at item 1.8, explicitly not codegen itself."
}

{
    "path":  "app/index.html",
    "change":  "CREATE (Phase 3). Real page title instead of the Vite template default, plus the favicon reference (*.ico is already binary at .gitattributes:35)."
}

{
    "path":  ".editorconfig",
    "change":  "CREATE (Phase 3). Two toolchains, one Windows author, and .gitattributes:3 forcing eol=lf everywhere except .ps1."
}

{
    "path":  "ops/README.md",
    "change":  "MODIFY (Phase 6). A Node-toolchain section beside the uv one (32-63) with the `npm ci` lockfile rule stated as sharply as the uv rule at 54-57, both run modes documented (two terminals for dev per Decision 4; the console script and only the console script for the built mode per Decision 9), and the note that spa_built is evaluated at construction."
}

{
    "path":  "README.md",
    "change":  "MODIFY (Phase 6). Delete the \u0027No application code yet\u0027 banner (line 12); add app/ and src/rpg_api/ to the project map (51-72) and drop the web app from the \u0027don\u0027t exist yet\u0027 sentence; extend Setup (74-80) with the Node half. AC 17 checks the first of these mechanically."
}

{
    "path":  "CLAUDE.md",
    "change":  "MODIFY (Phase 6). Add app/ and src/rpg_api/ to the project map (49-63); correct line 66 so it no longer says the web app doesn\u0027t exist. Hard line budget — an EDIT, not an append."
}

{
    "path":  "ROADMAP.md",
    "change":  "MODIFY BY /commit ONLY (Phase 6 checkpoint). Row 1.1 (line 165) and the Phase 1 Status line (156, still reading \u00271.1 app-shell is at intake\u0027). Never hand-edit — /commit maintains status against the diff."
}

{
    "path":  "requests/feature-requests/1.1-app-shell/reviews/preflight.md",
    "change":  "CREATE (Phase 0). The six unconfirmed beliefs, each converted to measured/verified/refuted with the evidence. The phase\u0027s only tracked deliverable."
}

{
    "path":  "requests/feature-requests/README.md",
    "change":  "MODIFY (plan stage). Index row for 1.1-app-shell (line 106) advances its Stage cell to `plan`, then to `implemented` when stage 4 lands."
}

### code_references

{
    "ref":  "pyproject.toml:9",
    "claim":  "`dependencies = []` — Phase 1 replaces it with fastapi + uvicorn. Verified: the list is literally empty today."
}

{
    "ref":  "pyproject.toml:11-13",
    "claim":  "The comment reserving FastAPI\u0027s arrival for \u0027Phase 1 item 1.1 (app-shell)\u0027 by name. Verified verbatim; Phase 1 removes it along with the empty list."
}

{
    "ref":  "pyproject.toml:31",
    "claim":  "`packages = [\"src/rpg_core\"]` — the hatch wheel list that AC 14 requires gain `src/rpg_api`. Verified."
}

{
    "ref":  "pyproject.toml:61-65",
    "claim":  "`[tool.mypy]` with strict = true (63), warn_unreachable = true (64), files = [\"src\", \"tests\"] (65). AC 8 requires this block be UNCHANGED. Verified."
}

{
    "ref":  "pyproject.toml:73",
    "claim":  "`pythonpath = [\"src\"]` — why every test passes whether or not rpg_api is in the hatch packages list, and therefore why AC 14 is not redundant. Verified."
}

{
    "ref":  "pyproject.toml:49",
    "claim":  "The DTZ rule (\u0027naive datetimes — every event timestamp is tz-aware or it is a bug\u0027), which taxes any timestamp field added to the health payload. Verified; Decision 6 already closes the payload."
}

{
    "ref":  ".github/workflows/ci.yml:19",
    "claim":  "Job display name `Lint, types, tests` — one of the two strings AC 4\u0027s set-equality guard must match against branch protection. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:34",
    "claim":  "`run: uv sync --locked` — AC 1 is verbatim what CI runs, and it hard-fails on a stale lock. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:47",
    "claim":  "`uv run pytest -m \"not network\" --cov=rpg_core --cov-report=term-missing` — the line Phase 1 extends with rpg_api and that AC 14\u0027s second half asserts. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:50",
    "claim":  "Job display name `Secret scan`, the second required context. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:10-12",
    "claim":  "`concurrency: group / cancel-in-progress: true` — why npm dependency caching on the new job matters: it re-runs on every push. Verified."
}

{
    "ref":  ".github/workflows/ci.yml:58",
    "claim":  "`- name: Gitleaks` is a STEP-level name, not a job name — the exact negative case AC 4\u0027s parser-is-structure-aware assertion should use. Verified."
}

{
    "ref":  "ops/branch-protection.json:4",
    "claim":  "`\"contexts\": [\"Lint, types, tests\", \"Secret scan\"]` — the array a third job\u0027s display name must join, in the same commit as the workflow change. Verified."
}

{
    "ref":  "ops/README.md:12-14",
    "claim":  "The `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json` command AC 23 step 2 runs. Owner/repo VERIFIED against `git remote -v` on 2026-08-14."
}

{
    "ref":  "ops/README.md:20-24",
    "claim":  "The blockquote warning that renaming a CI job silently breaks branch protection and \u0027PRs wait forever for a check that never reports\u0027 — the prose AC 4 turns into a build failure. Verified."
}

{
    "ref":  "ops/README.md:54-57",
    "claim":  "\u0027uv.lock is tracked, and CI installs with uv sync --locked\u0027 — the sharpness the new Node section must match for `npm ci`. Verified."
}

{
    "ref":  "ops/README.md:64-73",
    "claim":  "\u0027The same four commands CI runs, in the same order\u0027 — ruff check, ruff format --check, mypy, pytest. This is the per-phase checkpoint gate. Verified."
}

{
    "ref":  "tests/test_repo_structure.py:24-34",
    "claim":  "`_git_check_ignore` runs `git check-ignore -q --no-index` and works on paths that do not exist yet — the mechanism the app/dist + node_modules guard reuses. Verified."
}

{
    "ref":  "tests/test_repo_structure.py:46-54",
    "claim":  "`test_package_version_matches_pyproject` pins rpg_core.__version__ to pyproject — which transitively covers the health payload\u0027s version, provided the payload READS the attribute rather than re-typing the literal. Verified."
}

{
    "ref":  "tests/test_repo_structure.py:83-92",
    "claim":  "`test_scratch_root_is_gitignored` — the template for the new app/dist + node_modules gitignore guard. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:58-71",
    "claim":  "`_tracked_text_files` shells out to `git ls-files`, i.e. the INDEX — so an unstaged app/package-lock.json is invisible to the leak scan and a green run before staging proves nothing. Verified; this is the plan\u0027s most operationally important citation."
}

{
    "ref":  "tests/test_no_leaks.py:37",
    "claim":  "The docstring \u0027Binary and lockfiles are skipped\u0027 — true of uv.lock (no scanned suffix), false of package-lock.json since `.json` is in TEXT_SUFFIXES at line 41. This item makes it wrong and Phase 6 fixes it. Verified."
}

{
    "ref":  "tests/test_no_leaks.py:32-35",
    "claim":  "`ALLOWED` is the only sanctioned escape hatch, keyed by path with a written reason. Verified — the remedy for a trip is an entry here, never a weakened regex."
}

{
    "ref":  "tests/test_no_leaks.py:29",
    "claim":  "The EMAIL regex — the concrete tripwire for an npm-generated package.json carrying an `author` field. Verified."
}

{
    "ref":  "tests/test_request_links.py:26",
    "claim":  "`FENCED_BLOCK` matches 3+ backticks or tildes only. Inline backticks are NOT stripped — which is precisely the trap the scope\u0027s Authoring rule (PROJECT_SCOPE.md:5-18) says fired twice during scoping. Verified."
}

{
    "ref":  "tests/test_request_links.py:40-64",
    "claim":  "`_dead_links` resolves every relative markdown link against disk, exempting only http(s)/mailto/#, `\u003cplaceholder\u003e` targets, `var/` paths, and `file.py:123` suffixes. Verified."
}

{
    "ref":  "src/rpg_core/__init__.py:3-11",
    "claim":  "The docstring stating \u0027Deliberately I/O-free and web-free... The API and the web app depend on it; it depends on neither\u0027 — the direction the layering guard enforces. Verified."
}

{
    "ref":  "src/rpg_core/__init__.py:16",
    "claim":  "`__version__ = \"0.1.0\"` — the entire mutable content of the domain core, and the value the health payload must read rather than re-type. Verified."
}

{
    "ref":  "DESIGN.md:106-109",
    "claim":  "\u0027Two packages, one repo. src/rpg_core/ is the I/O-free domain; the API and web app depend on it and it depends on neither.\u0027 The sentence the layering guard\u0027s failure message must cite by name (Decision 3 chose a guard over ADR 0010). Verified."
}

{
    "ref":  ".gitignore:66-68",
    "claim":  "The Node block — node_modules/, .vite/, app/dist/ — reserved in Phase 0, which is the strongest evidence for the app/ convention. Verified."
}

{
    "ref":  ".gitignore:62-63",
    "claim":  "Blanket `dist/` and `build/` rules matching at ANY depth. Nothing this item needs may live under a directory with either name outside app/; the `build/` one is scope risk 15\u0027s warning for item 2.1. Verified."
}

{
    "ref":  ".gitattributes:41",
    "claim":  "`package-lock.json linguist-generated=true -diff` — Phase 0 reserved the lockfile by name, confirming the intended location and that it is committed. Verified."
}

{
    "ref":  ".gitattributes:20-25",
    "claim":  "`.js`, `.mjs`, `.ts`, `.tsx`, `.css`, `.html` all declared text with eol=lf per line 3 — the frontend\u0027s line endings are already decided by the repo. Verified."
}

{
    "ref":  ".github/dependabot.yml:30",
    "claim":  "`# npm arrives with Phase 1 item 1.1 (app-shell). Add the ecosystem entry then.` — the placeholder AC 15 requires be discharged and removed. Verified verbatim."
}

{
    "ref":  ".github/dependabot.yml:16-28",
    "claim":  "The uv entry whose monthly schedule and semver-patch ignore posture the npm entry must mirror. Verified."
}

{
    "ref":  ".claude/settings.json:8",
    "claim":  "`\"PowerShell(gh api *)\"` sits in the `ask` list — the structural reason AC 23 step 2 is USER-RUN and an agent cannot apply branch protection. Verified."
}

{
    "ref":  ".claude/settings.json:16-17",
    "claim":  "`PowerShell(node *)` and `PowerShell(npm *)` are already in the allow list — Phase 0 anticipated this item\u0027s toolchain. Verified."
}

{
    "ref":  "CLAUDE.md:66",
    "claim":  "\u0027`lib/`, and the web app don\u0027t exist yet — don\u0027t create them speculatively\u0027 — the sentence AC 17 requires stop being true. Verified."
}

{
    "ref":  "CLAUDE.md:47-63",
    "claim":  "The project map fenced block that must gain `app/` and `src/rpg_api/`; line 58 currently reads \u0027src/rpg_core/  Domain core — I/O-free, web-free. Empty until Phase 1\u0027. Verified."
}

{
    "ref":  "README.md:12-13",
    "claim":  "The blockquote \u0027Phase 0. Repo, process, and CI harness exist. No application code yet.\u0027 — the exact string AC 17 asserts is gone. Verified."
}

{
    "ref":  "README.md:71-72",
    "claim":  "\u0027Directories appear when their phase does. careers/, datasets/, rulesets/, lib/, and the web app don\u0027t exist yet.\u0027 — README\u0027s half of the doc-drift surface. Verified."
}

{
    "ref":  "ROADMAP.md:165",
    "claim":  "Row `| 1.1 | app-shell | FastAPI + React/Vite wiring, dev server, health endpoint, frontend build in CI | M | 0.3 | IN-PROGRESS |` — status advanced by /commit, never hand-edited. Verified."
}

{
    "ref":  "ROADMAP.md:156",
    "claim":  "Phase 1\u0027s Status line reads \u0027IN-PROGRESS — 1.1 app-shell is at intake. No application code has landed yet.\u0027 — stale once this item lands; /commit\u0027s roadmap step owns it. Verified."
}

{
    "ref":  "ROADMAP.md:166-175",
    "claim":  "The eleven downstream Phase 1 rows (1.2 through 1.11) blocked on this seam, all NOT STARTED. Verified."
}

{
    "ref":  "requests/feature-requests/README.md:57-73",
    "claim":  "The definition of testable — \u0027a cold agent can run one command and get a pass or fail\u0027 — and the rule that human-only criteria must be marked user-run so the acceptance panel does not claim them. Verified."
}

{
    "ref":  "requests/feature-requests/README.md:96-100",
    "claim":  "The status blockquote grammar and the intake -\u003e scoped -\u003e planned -\u003e implemented progression the plan\u0027s own header must follow. Verified."
}

{
    "ref":  "requests/feature-requests/README.md:106",
    "claim":  "The Index row for 1.1-app-shell, Stage cell currently `scoped` — advanced to `plan` when the IMPLEMENTATION_PLAN lands. Verified."
}

{
    "ref":  "docs/data-access.md:113-122",
    "claim":  "§3 External sources — all four rows labelled `unconfirmed`, no endpoint chosen and no pull attempted. This item touches NONE of them and makes no outbound network call, so no source-verification phase is owed and no data-contracts section belongs in the plan. Verified."
}

{
    "ref":  "requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:5-18",
    "claim":  "The Authoring rule: paths this item creates are written inline or fenced, never as markdown links, because tests/test_request_links.py would turn CI red on this very PR. It explicitly instructs \u0027Carry the rule into the plan.\u0027 Verified."
}

### open_questions

CONSOLE SCRIPT NAME. `[project.scripts]` needs a name and the plan does not fix one — `rpg-api` pointing at `rpg_api.__main__:main` is the recommendation (matches the repo's `uv run <tool>` idiom, and Decision 9 requires exactly one documented incantation). Whatever is chosen gets written into ops/README.md once and never a second way.

AC 11'S MECHANISM. The criterion says a dedicated `npm run typecheck:negative` is 'asserted to exit non-zero'. Asserted by whom is unspecified, and PowerShell 5.1 cannot negate an exit code inline the way bash can. Recommendation: `typecheck:negative` runs tsc against the negative project (exits non-zero by design) and a wrapper script `check:negative` spawns it and exits 0 iff the inner run failed — one command invocation, identical on Windows and ubuntu-latest. Flagging because it adds one small .mjs file inside app/ that the scope did not enumerate.

NODE MAJOR IN CI. Local is measured at v24.15.0. Pinning CI to major 24 avoids the lockfileVersion skew of scope risk 10; pinning to the current LTS instead would be more conventional but reintroduces exactly that skew. Recommendation: 24. Worth one word from the user since it is the number that appears in ops/README.md.

STATIC MOUNT SHAPE. Phase 2's design assumes Vite emits `dist/index.html` plus `dist/assets/*`, so the mount is `StaticFiles` at /assets with index.html served by explicit routes. Phase 0 BELIEF 3 measures the actual layout; if Vite's output differs, Phase 2 adapts. Called out so the cold agent treats the layout as measured-then-coded rather than assumed.

WHERE THE PACKAGING AND DOC GUARDS LIVE. The plan appends ACs 14, 17 and the gitignore guard to tests/test_repo_structure.py on the grounds that AC 17 explicitly names 'the idiom tests/test_repo_structure.py already uses'. A separate tests/test_packaging.py would also satisfy the criteria. Recommendation: append, keeping one structural-guard module.

SCOPE RISK 15 IS RECORDED, NOT ACTIONED. .gitignore line 63's blanket `build/` will shadow the `build/build-*.py` builder pattern CLAUDE.md prescribes for Phase 2. It is explicitly not this item's problem, and this plan does not touch it — but it should become an intake item before item 2.1 rather than being rediscovered there.

---

## Lens: `domain-convention`

### ok

true

### onboarding_files

{
    "path":  "D:\\projects\\nba2k-rpg\\requests\\feature-requests\\1.1-app-shell\\PROJECT_SCOPE.md",
    "why":  "THE decided contract. Read in full, especially the Authoring rule (lines 5-18), the 23 Acceptance Criteria (lines 147-258), the Non-Goals (lines 106-145) and the 10 Decisions (lines 502-516). It is CONSUMED, not re-opened."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\CLAUDE.md",
    "why":  "The conventions that bind every change: /commit only, main protected, public-repo leak rules, the inverted careers/ tracking rule, \u0027don\u0027t create careers|datasets|rulesets|lib speculatively\u0027, epistemic labelling. This item must honor all of them while touching none of the domain ones."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\pyproject.toml",
    "why":  "Every Python-side edit lands here: line 9 empty dependencies, lines 11-13 the reservation comment to delete, lines 16-21 the dev group, line 31 the hatch wheel packages list, lines 61-65 the mypy strict block that must NOT be loosened, line 73 pythonpath."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.github\\workflows\\ci.yml",
    "why":  "The third job goes here. Job display names at lines 19 and 50 are the exact strings ops/branch-protection.json line 4 must match; line 34 is the verbatim `uv sync --locked` AC 1 quotes; line 47 is the --cov line to extend."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\ops\\branch-protection.json",
    "why":  "Line 4 `contexts` is the array the new job\u0027s display name joins. The file is inert until re-applied with `gh api -X PUT` — a user action (.claude/settings.json line 8)."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\ops\\README.md",
    "why":  "Lines 12/29 carry the owner/repo (verified matching `git remote -v` = jordan-koch/nba2k-rpg); lines 21-24 are the job-RENAME warning this item generalizes to job ADDITION; lines 32-62 the uv section the Node section sits beside; lines 66-73 \u0027the same four commands CI runs\u0027 — the per-phase green gate."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_repo_structure.py",
    "why":  "The guard idiom to copy. `_git_check_ignore` (lines 24-34) is the helper the new gitignore guard must REUSE, not reimplement; `test_scratch_root_is_gitignored` (83-92) is the literal template; `test_package_version_matches_pyproject` (46-54) is what makes the health payload\u0027s version transitively pinned."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_no_leaks.py",
    "why":  "The blocking public-repo guard that now starts scanning frontend files. TEXT_SUFFIXES (38-55) already includes .json/.ts/.tsx/.css/.html; EMAIL (line 29) will fail on a package.json `author` field; WINDOWS_PATH (line 26) on any absolute path in a generated config; ALLOWED (32-35) is the ONLY sanctioned escape hatch; line 37\u0027s docstring is the sentence this item makes false."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_request_links.py",
    "why":  "Read `_dead_links` (40-64) and FENCED_BLOCK (line 26) before writing ANY markdown in this item. Only fenced blocks are stripped — inline backticks are NOT. A markdown link to a path this item creates turns CI red on the PR that creates it."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.claude\\settings.json",
    "why":  "Decides what an agent may do unprompted. Lines 4-11 `ask`: git commit/push/merge and `gh api *` are user-gated. Lines 16-17 already allow `node *` and `npm *`. Line 60 `Edit(/**)` means file edits are free — only git and gh are gated."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.claude\\skills\\commit\\SKILL.md",
    "why":  "The ONLY sanctioned commit path, and every phase ends in it. Step 2 (49-78) deliberate staging; Step 4 (109-144) is what owns ROADMAP.md\u0027s Status CELLS — note it does NOT own ROADMAP prose; Steps 6-7 (175-233) the hard rails: no --amend, no --no-verify, no force-push, never push main, never open the PR."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.gitignore",
    "why":  "Lines 66-68 already anticipate `node_modules/`, `.vite/`, `app/dist/`. Line 62\u0027s blanket `dist/` and line 63\u0027s blanket `build/` match at ANY depth — the silent-swallow class of bug the scope\u0027s risk 15 names. Lines 35-49 are the careers carve-out this item must not disturb."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\src\\rpg_core\\__init__.py",
    "why":  "The entire domain core today: a docstring stating the dependency direction (lines 3-9) and `__version__ = \"0.1.0\"` (line 16). It must look IDENTICAL after this item lands — that is the sharpest test of Non-Goal #1."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\DESIGN.md",
    "why":  "§3 \u0027Architecture notes not yet ADRs\u0027 (heading line 99); the \u0027Two packages, one repo\u0027 bullet at lines 106-108 is the exact sentence the layering guard\u0027s failure message must cite by name (Decision 3 chose a guard test over ADR 0010)."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\ROADMAP.md",
    "why":  "Row 1.1 at line 165 (Status IN-PROGRESS, owned by /commit). Lines 127-130 declare /commit owns the table. Line 156\u0027s phase-header PROSE (\u00271.1 app-shell is at intake. No application code has landed yet\u0027) is stale and is NOT covered by /commit\u0027s Status-cell mandate nor by AC 17 — it needs a hand edit."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\requests\\feature-requests\\README.md",
    "why":  "The pipeline contract: the definition of \u0027testable\u0027 and the user-run rule (lines 57-73), the status blockquote grammar (lines 96-100), and the Index row at line 106 whose Stage cell advances to `plan`."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\docs\\data-access.md",
    "why":  "Read ONLY to confirm this item consumes nothing from it. §3 \u0027External sources\u0027 (line 113) is entirely `unconfirmed`; none of those rows is touched by 1.1. Confirms the data-contracts section is correctly absent rather than forgotten."
}

### architecture_notes

SHAPE OF THE CHANGE. This is a pure-seam item with ZERO data surface, so this lens runs as PROJECT-CONVENTION correctness, not data-contract correctness.

Verified by filesystem probe (measured, 2026-08-14): `datasets/`, `careers/`, `rulesets/`, `lib/`, `app/`, `src/rpg_api/`, `tests/conftest.py` do NOT exist. `src/` contains exactly one package, `rpg_core`, holding one file. `tests/` contains exactly three test modules and `tests/fixtures/README.md`.

THE SEAM BEING INSTANTIATED. DESIGN.md line 99 opens §3 "Architecture notes not yet ADRs"; lines 106-108 state "Two packages, one repo. `src/rpg_core/` is the I/O-free domain; the API and web app depend on it and it depends on neither." src/rpg_core/__init__.py lines 3-9 echo the same direction from the other side. This item creates the second package and, for the first time, gives that sentence a mechanical enforcer.

The dependency graph after this item: browser -> (dev: Vite proxy | built: uvicorn static mount) -> `rpg_api` -> `rpg_core`. Exactly one edge into `rpg_core`, and it is the health payload's `version` field reading `rpg_core.__version__`. That single edge is load-bearing twice over: it proves the direction is real, and it inherits the existing version pin at tests/test_repo_structure.py lines 46-54, so the payload is transitively pinned to pyproject.toml with no new test.

INJECTION, NOT PATH RESOLUTION. The one path this item resolves at runtime is the built-SPA directory. The scope forces it to be a factory argument (AC 5, Decision 5: no `RPG_SPA_DIST` env key). The plan must therefore prescribe a factory signature roughly `create_app(spa_dist: Path | None = None) -> FastAPI`, with the default computed relative to the repo/package root and NEVER a literal path — tests/test_no_leaks.py line 26's WINDOWS_PATH regex fails the build on any tracked drive-letter path, and CLAUDE.md's "machine-specific values resolve from the environment" is satisfied here by the injection point plus a repo-relative default, which Decision 5 records as the deliberate divergence from FEATURE_REQUEST.md's Non-negotiables.

THIS IS THE PROJECT'S resolve-by-name CONVENTION IN ITS PRE-DATASET FORM. There is no `datasets/manifest.json` to resolve against (item 2.1). The convention that generalizes to this item is the same one: a consumer never hardcodes a location; it receives it. The plan should say so explicitly, because the next eleven items copy whatever this one does.

WHY THE UNCONFIRMED-CLAIM RULE STILL BITES. docs/data-access.md §3 (line 113) is entirely `unconfirmed`, and this item consumes none of it — so no data phase is needed. But the same discipline applies to the four TOOLING beliefs the build's design depends on, all currently `inferred` or `unconfirmed` in the scope's Risks: (a) mypy strict passes over FastAPI route decorators (risk 6, unconfirmed); (b) Starlette's StaticFiles raises at construction on a missing directory (risk 7, explicitly labelled *Inferred*); (c) tests/test_no_leaks.py passes over a tracked package-lock.json (risk 4, explicitly labelled *Inferred, not measured*); (d) gitleaks does not flag sha512 integrity strings (risk 5, self-described as medium-confidence). (a) and (b) determine code shape and must be measured BEFORE the factory is designed around them; (c) and (d) must be measured BEFORE the lockfile is staged. Hence Phase 1 is a verify-then-declare phase and Phase 4 carries a pre-staging gate.

WHAT MUST NOT MOVE. `src/rpg_core/__init__.py` must be byte-identical after this item. `.gitignore` lines 35-49 (the careers carve-out) must not be touched. `[tool.mypy]` lines 61-65 must be unchanged — AC 8 fails a green run achieved by loosening strict. No file appears under `careers/`, `var/` (tracked), `datasets/`, or `rulesets/`.

CONFIG SCOPE IS A HARD BOUNDARY. `git ls-files .claude` returns 8 tracked `.js`/`.mjs` files (the three panel scripts plus five guard scripts). Any eslint/tsconfig at the repo root would immediately start reporting on them and force an ignore list nobody scoped. Both configs live INSIDE `app/` with file scope limited to `app/`.

### phases

{
    "name":  "Phase 1 — Dependency spine, with the two unconfirmed backend beliefs measured first",
    "goal":  "Land the Python dependency bookkeeping in one commit, and MEASURE the two tooling claims (mypy-strict-over-FastAPI, StaticFiles-on-missing-dir) whose answers determine the shape of Phase 2, before any application code exists to be designed around a guess.",
    "steps":  [
                  "Create the feature branch: `git switch -c 1.1-app-shell` (allowed unprompted — .claude/settings.json line 27; `git checkout -b *` at line 28 is the alternative). Do NOT work on main (CLAUDE.md: main is protected).",
                  "pyproject.toml: replace line 9 `dependencies = []` with fastapi + uvicorn, and DELETE the reservation comment at lines 11-13 — it has now been discharged and leaving it makes the file lie.",
                  "pyproject.toml lines 16-21 (`[dependency-groups].dev`): add `httpx` (TestClient\u0027s transport), `pyyaml` and `types-PyYAML` (AC 4\u0027s parser plus the stubs mypy strict requires), and `watchfiles` (reload, chosen over `uvicorn[standard]` per the scope\u0027s Core list).",
                  "pyproject.toml line 31: append `\"src/rpg_api\"` to `[tool.hatch.build.targets.wheel].packages`. This is scope risk 2 — omit it and every test still passes because line 73\u0027s `pythonpath = [\"src\"]` puts the package on the path regardless; it fails only at runtime on an installed environment.",
                  "pyproject.toml: add a `[project.scripts]` block with ONE console entrypoint for the served-build mode (Decision 9). Pick the name here and never document a raw uvicorn incantation as an alternative — Decision 9\u0027s caveat is that exactly one canonical way to run the served build gets documented.",
                  "Run `uv lock`, then `uv sync --locked` — the second is verbatim ci.yml line 34 and hard-fails on a stale lock, so a local pass predicts AC 1.",
                  "MEASURE (a): write a throwaway `var/probe_route.py` (var/ is gitignored — .gitignore line 18) containing a fully annotated FastAPI route, and run `uv run mypy var/probe_route.py`. `[tool.mypy] files = [\"src\", \"tests\"]` (line 65) means a bare `uv run mypy` will not see it, so pass the path explicitly. Record whether `disallow_untyped_decorators` fires.",
                  "MEASURE (b): write a throwaway `var/probe_static.py` constructing `starlette.staticfiles.StaticFiles(directory=\u003ca path that does not exist\u003e)` and record whether it raises at construction. This decides whether Phase 2\u0027s factory may mount unconditionally or must branch.",
                  "Record both measurements, labelled *measured* per CLAUDE.md\u0027s epistemics rule, in the commit-message body. Do not stage anything under var/ — /commit\u0027s Step 2 table (SKILL.md line 61) refuses it.",
                  "Green gate, ops/README.md lines 66-73 in order: `uv run ruff check`, `uv run ruff format --check`, `uv run mypy`, `uv run pytest`."
              ],
    "acceptance":  [
                       "`uv sync --locked` exits 0 with fastapi and uvicorn resolved in the tracked uv.lock (AC 1).",
                       "`uv run pytest` is still green — the three existing test modules are unaffected.",
                       "`git status --porcelain --untracked-files=all` shows nothing under var/ staged.",
                       "Both probe results are written down as *measured* statements in the commit body; the probe files themselves are gone or left in var/ untracked.",
                       "`[tool.mypy]` (pyproject.toml lines 61-65) is textually unchanged."
                   ],
    "commit_note":  "/commit. Subject: \"Add FastAPI and uvicorn dependencies, regenerate uv.lock\". Body records the two measurements. ROADMAP.md row 1.1 (line 165) stays IN-PROGRESS — the Deliverable cell is nowhere near satisfied, and /commit\u0027s Step 4 rail is \u0027never mark ahead\u0027."
}

{
    "name":  "Phase 2 — The rpg_api package: factory, health route, and the API tests",
    "goal":  "Create the HTTP seam with the SPA dist location injected, both serve branches unit-testable against tmp_path with no listening socket, and mypy strict green with zero ignores and zero per-module overrides.",
    "steps":  [
                  "Create `src/rpg_api/__init__.py` and the application module. Export a factory, e.g. `create_app(spa_dist: Path | None = None) -\u003e FastAPI`. The dist location is a FACTORY ARGUMENT, never a module-level constant (AC 5) and never an env key (Decision 5). Its default is computed relative to the package/repo root — a literal drive-letter path fails tests/test_no_leaks.py line 26.",
                  "Add `GET /api/health` returning `{\"status\": \"ok\", \"version\": rpg_core.__version__, \"spa_built\": \u003cbool\u003e}`. Read the version from the attribute, never re-type the string — that is what makes tests/test_repo_structure.py lines 46-54 transitively cover the payload. This import is the ONLY edge into rpg_core and it is deliberate.",
                  "Apply Decision 6\u0027s standing rule verbatim in a code comment: the payload gains a field only when the thing it reports exists. No `career_count`, no `ruleset_version`, no `started_at` (the last would also draw the DTZ lint rule at pyproject.toml line 49).",
                  "Implement the serve branches using Phase 1\u0027s measurement (b): absent dist -\u003e construction must NOT raise, `GET /api/health` still 200, `GET /` returns 503 whose body contains the literal build command (AC 5). Present dist -\u003e `GET /` returns 200, text/html, that file\u0027s bytes (AC 6).",
                  "Implement the JSON-404 rail: an unknown path UNDER `/api` returns 404 with content-type application/json, not HTML (AC 7). Implement the SPA history fallback for unmatched NON-`/api` paths. Order matters — the fallback must not swallow API 404s; that pairing is what stops item 1.10\u0027s router being a breaking change.",
                  "Create `tests/conftest.py` with a reusable TestClient fixture parameterized on the injectable dist location. Items 1.7-1.11 each need it; the scope folds it in so five agents don\u0027t invent five variants.",
                  "Create the API test module covering AC 2, 5, 6, 7. Use `fastapi.testclient.TestClient` only — no live server, no socket. Assert status 200, content-type application/json, `body[\"status\"] == \"ok\"`, `body[\"version\"] == rpg_core.__version__`, and that `body[\"spa_built\"]` is a bool.",
                  "HARD RAIL (AC 8): if mypy strict complains, fix the annotation. Adding a `# type: ignore` or a per-module override carving rpg_api out of strict FAILS the criterion. This is the exact asymmetry the whole item exists to prevent on the frontend side.",
                  "Confirm `src/rpg_core/__init__.py` is untouched — `git diff src/rpg_core/` must be empty. This is the sharpest single test of the \u0027no domain logic\u0027 non-goal.",
                  "Green gate: the four commands from ops/README.md lines 66-73."
              ],
    "acceptance":  [
                       "`uv run pytest -m \"not network\"` green, including the health test (AC 2) and both dist branches against tmp_path (AC 5, AC 6).",
                       "`GET` on an unknown `/api/...` path returns 404 with content-type application/json (AC 7).",
                       "`uv run mypy` exits 0 with src/rpg_api present, `[tool.mypy]` unchanged, `git diff pyproject.toml` showing no new mypy overrides, and `grep -rn \u0027type: ignore\u0027 src/ tests/` returning nothing new (AC 8).",
                       "`uv run ruff check` and `uv run ruff format --check` exit 0 over src/rpg_api and the new test files (AC 9).",
                       "`git diff src/rpg_core/` is empty."
                   ],
    "commit_note":  "/commit. Subject: \"Add rpg_api package with health route and injectable SPA dist\". ROADMAP.md 1.1 remains IN-PROGRESS."
}

{
    "name":  "Phase 3 — The two guards that are green on day one",
    "goal":  "Land the layering guard (the one permanent artifact this content-free item leaves behind) and the gitignore guard, both of which pass immediately against the tree as it now stands.",
    "steps":  [
                  "Create `tests/test_layering.py` with the guard as a PURE FUNCTION taking a directory root and returning violations — no source mutation anywhere (AC 3).",
                  "Unit-test it twice against `tmp_path`: a fake module containing `import fastapi` reports exactly that file; a clean tree reports none. Then the real assertion points at `src/rpg_core/` and expects zero. One `uv run pytest` proves red-and-green without editing tracked source.",
                  "Deny-list: `fastapi`, `starlette`, `uvicorn`, and the API package. `pydantic` is deliberately ABSENT — ADR 0002 requires the DTO be constructible in tests with no HTTP and no UI, so that is item 1.2\u0027s call, not this one\u0027s. Do not add it \u0027for completeness\u0027.",
                  "The failure message must cite DESIGN.md §3 by name (Decision 3 chose a guard test over ADR 0010 precisely because a test fails a build where prose does not). The sentence it defends is at DESIGN.md lines 106-108.",
                  "Add the gitignore guard INSIDE `tests/test_repo_structure.py`, immediately after `test_scratch_root_is_gitignored` (lines 83-92), so it REUSES the module-private `_git_check_ignore` helper (lines 24-34) rather than duplicating the subprocess call. Assert `app/dist/...` and `node_modules/...` are ignored — both verified True today by `git check-ignore --no-index`, and the helper works on paths that do not exist yet. Its purpose is to fail if anyone later adds an `!app/**` carve-out.",
                  "Green gate: the four commands."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_layering.py` green: two tmp_path cases plus the real zero-violation assertion against src/rpg_core/.",
                       "`git diff src/` shows no test-scaffolding edits to tracked source (AC 3\u0027s no-mutation clause).",
                       "`uv run pytest tests/test_repo_structure.py` green, including the new gitignore guard.",
                       "The layering guard\u0027s assertion message contains the literal string identifying DESIGN.md §3.",
                       "`pydantic` does not appear in the deny-list."
                   ],
    "commit_note":  "/commit. Subject: \"Add import-layering and gitignore structural guards\"."
}

{
    "name":  "Phase 4 — The SPA, with the public-repo gate run BEFORE the lockfile is staged",
    "goal":  "Land app/ — Vite + React + TypeScript, strict, linted, two Vitest tests, the negative typecheck fixture — and prove the tracked frontend files clear the blocking leak guard and gitleaks before they enter history.",
    "steps":  [
                  "Scaffold `app/` at the repo root — the location .gitignore lines 66-68 and .gitattributes line 41 already anticipate. Do NOT put anything at the repo root: eslint config and tsconfig.json live INSIDE app/ with file scope limited to app/ (8 tracked .js/.mjs files under .claude/skills would otherwise start getting linted).",
                  "`app/package.json`: set `\"private\": true` and a placeholder version (the three-way version parity test was dropped as meaningless for a private SPA). CRITICAL — do NOT include an `author` field carrying an email. tests/test_no_leaks.py line 70 scans every tracked `.json` (TEXT_SUFFIXES lines 38-55) and EMAIL at line 29 will fail the build.",
                  "Every npm script must be a SINGLE command invocation with no shell operators. No `\u0026\u0026`, no `rm -rf`, no `cp`, no POSIX inline env-var prefixes. Windows PowerShell 5.1 has no `\u0026\u0026` at all, so such a script works in ubuntu CI and fails on the author\u0027s daily machine (scope risk 8).",
                  "`app/tsconfig.json`: `strict: true` plus `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`. No absolute paths anywhere in it — WINDOWS_PATH (test_no_leaks.py line 26) scans `.json` and `.ts` alike.",
                  "`app/vite.config.ts`: dev-server proxy mapping `/api` to the IPv4 literal `127.0.0.1`, NOT `localhost` (scope risk 9 — Node on Windows can resolve localhost to ::1 while uvicorn binds 127.0.0.1, producing an ECONNREFUSED indistinguishable from the backend being down). No CORS middleware is added anywhere, in either mode.",
                  "`app/src/api/client.ts`: a small typed fetch wrapper with a HAND-WRITTEN `Health` interface. This is explicitly NOT the deferred OpenAPI codegen contract — it is the seam codegen slots into at item 1.8.",
                  "One page: fetch `/api/health`, render status and version, and render a legible backend-unreachable panel naming the start command on a rejected fetch. That page is the entire UI. Resist the single strongest failure mode named in the scope\u0027s Non-Goals: no career, no stub player, no fake XP number.",
                  "Two Vitest tests, exactly (AC 12): the status page renders the fetched version; the unreachable panel renders on a rejected fetch.",
                  "AC 11: commit a deliberately ill-typed fixture EXCLUDED from `npm run build`, and add a dedicated `npm run typecheck:negative` script asserted to exit non-zero — this proves `strict` is actually engaged rather than a default-generated config that checks nothing.",
                  "Real page title and favicon instead of the Vite template defaults. `.gitattributes` line 35 already declares `*.ico binary`.",
                  "Add `.editorconfig` at the repo root, and make it AGREE with `.gitattributes` line 3 (`* text=auto eol=lf`) — an .editorconfig specifying crlf would fight the repo\u0027s normalization.",
                  "PRE-STAGING GATE, before `git add` of anything under app/: run `uv run pytest tests/test_no_leaks.py` (AC 13, scope risk 4 — explicitly *inferred, not measured*). If a pattern trips, the fix is a narrowly-justified `ALLOWED` entry (test_no_leaks.py lines 32-35) with a written reason — NEVER a weakened regex and NEVER a removed suffix.",
                  "PRE-PUSH GATE: run gitleaks locally once over the tree (scope risk 5 — the repo has no .gitleaks.toml or .gitleaksignore, verified absent, and the secrets job at ci.yml lines 58-61 blocks merge). If it trips on package-lock.json integrity hashes, remediate with specific fingerprints in a .gitleaksignore or a scoped path allowlist, each with a written reason, mirroring the ALLOWED discipline.",
                  "SILENT-IGNORE CHECK: run `git status --porcelain --untracked-files=all app/` and cross-check against `git check-ignore --no-index` for each source file. .gitignore line 62\u0027s blanket `dist/` and line 63\u0027s blanket `build/` match at ANY depth — the same class of silent shadowing the scope\u0027s risk 15 records for item 2.1. Verified today: `app/package.json` and `app/src/main.tsx` are NOT ignored; `app/dist/index.html` and `app/node_modules/**` ARE.",
                  "Green gate: the four Python commands, plus from app/: `npm ci`, `npm run typecheck`, `npm run typecheck:negative`, `npm run lint`, `npm run test`, `npm run build`. `npm *` and `node *` need no permission prompt (.claude/settings.json lines 16-17)."
              ],
    "acceptance":  [
                       "From app/: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run build` each exit 0, and app/dist/index.html exists afterwards (AC 10).",
                       "`npm run typecheck:negative` exits NON-zero (AC 11).",
                       "`npm run test` green with exactly two Vitest tests (AC 12).",
                       "`uv run pytest tests/test_no_leaks.py` green with app/package.json, app/package-lock.json, app/tsconfig.json and app/vite.config.ts tracked (AC 13).",
                       "No eslint or tsconfig file exists at the repo root; both are inside app/ and scoped to app/.",
                       "No npm script contains `\u0026\u0026`, `rm`, `cp`, or a POSIX env-var prefix.",
                       "gitleaks run locally is clean, or every finding is remediated by a fingerprint/path entry carrying a written reason.",
                       "`uv run pytest tests/test_repo_structure.py tests/test_request_links.py` still green with the new directories present (AC 16)."
                   ],
    "commit_note":  "/commit. Subject: \"Add React/Vite SPA with strict TypeScript, eslint, and Vitest\". Stage app/ by path — never `git add -A` (commit SKILL.md line 51). Confirm the staged list contains no node_modules/ and no app/dist/."
}

{
    "name":  "Phase 5 — CI job, required-check bookkeeping, dependabot, and the guards that pin them",
    "goal":  "Add the third CI job and the real-server smoke step, extend coverage, register the npm ecosystem, and land the set-equality guard and the hatch/--cov guard in the SAME commit as the changes they assert — so the phase ends green.",
    "steps":  [
                  "Choose the new job\u0027s DISPLAY NAME once and use it verbatim in both places. ci.yml already carries `name: Lint, types, tests` (line 19) and `name: Secret scan` (line 50); ops/branch-protection.json line 4 carries those two strings exactly.",
                  "ci.yml: add a third job parallel with `python` and `secrets` — actions/setup-node against a pinned MAJOR (local is node v24.15.0 / npm 11.12.1, measured on this machine), npm caching with `cache-dependency-path` pointing at the SPA lockfile, `working-directory: app`, then npm ci / typecheck / typecheck:negative / lint / test / build. No `.nvmrc` and no `engines` field — the scope chose a workflow pin plus one line in ops/README.md, because a version file pins CI while the Windows developer silently drifts.",
                  "Add the real-server smoke step (AC 18, Decision 8 — taken AGAINST the panel\u0027s recommendation, so do not quietly drop it). It builds the SPA, boots uvicorn against the built dist, and curls both `/` (200, HTML) and `/api/health` (200, JSON). Use a BOUNDED READINESS POLL with a timeout, never a fixed sleep (scope risk 14). It needs Python and Node in one job — putting setup-uv alongside setup-node in the web job keeps it to one job and keeps the job-name set at exactly three.",
                  "ci.yml line 47: extend `--cov=rpg_core` to also cover rpg_api (scope risk 11 — left alone, the number quietly stops describing the codebase; there is no fail-under, so nothing else complains).",
                  "Do NOT add `paths-ignore` or any path filter (explicit Non-Goal). With `required_status_checks.strict: true` (branch-protection.json line 3) and named contexts, a filtered job that never reports makes PRs wait forever — exactly the silent hang ops/README.md lines 21-24 warn about.",
                  "ops/branch-protection.json line 4: append the new job\u0027s display name to `contexts`, IN THE SAME COMMIT as the ci.yml change.",
                  "Add the AC 4 guard test: parse .github/workflows/ci.yml with `yaml.safe_load`, collect `jobs.*.name`, and assert that set EQUALS `required_status_checks.contexts`. Equality, not containment — containment passes while a typo\u0027d name (\u0027Web app\u0027 vs \u0027Web App\u0027) hangs every PR forever. The failure message must name which side carries the extra entry. Add a NEGATIVE assertion proving the parser is structure-aware: a step-level name (e.g. \u0027Gitleaks\u0027 at ci.yml line 58, or \u0027Install\u0027 at line 30) must NOT enter the set.",
                  "Add the AC 14 guard test: assert `[tool.hatch.build.targets.wheel].packages` contains `src/rpg_api` and that ci.yml\u0027s pytest step passes a `--cov` flag naming rpg_api. Read pyproject.toml with `tomllib` (the idiom already at tests/test_repo_structure.py lines 49-50). Without this, the omission is invisible to every local test because pythonpath = [\"src\"] masks it.",
                  ".github/dependabot.yml: add a `package-ecosystem: \"npm\"` entry pointing at the SPA directory, mirroring the uv entry\u0027s posture (lines 16-28): monthly interval, `commit-message.prefix`, labels, and the semver-patch ignore block. DELETE the line-30 placeholder comment — it has been discharged (AC 15).",
                  "Green gate: the four commands. Note the AC 4 guard is the one that would have been red in Phase 3 and is green only now, which is why it lands here."
              ],
    "acceptance":  [
                       "`uv run pytest` green, including the set-equality guard and the hatch/--cov guard.",
                       "The set-equality guard is proven honest: temporarily changing one letter of the job name in a scratch copy makes it fail (verify by reasoning through the negative case, or with a tmp_path fixture pair).",
                       "`.github/dependabot.yml` contains an npm ecosystem entry with the same monthly + patch-ignore posture as the uv entry, and the line-30 placeholder is gone (AC 15).",
                       "ci.yml\u0027s pytest step names both rpg_core and rpg_api in --cov.",
                       "ci.yml contains no `paths-ignore` / `paths` filter on any job.",
                       "The smoke step uses a bounded readiness poll, not a fixed sleep."
                   ],
    "commit_note":  "/commit. Subject: \"Add web-app CI job, real-server smoke, and the checks-parity guard\". The workflow change and the branch-protection.json change MUST be in this one commit — that pairing is the mitigation for the headline risk."
}

{
    "name":  "Phase 6 — Stop the docs lying, and prove it mechanically",
    "goal":  "Bring README.md, CLAUDE.md, ops/README.md and ROADMAP.md\u0027s phase prose back into agreement with a repo that now has an application, and land AC 17\u0027s structural test so Goal 7 has a pass/fail check instead of a judgment gate.",
    "steps":  [
                  "README.md: remove the banner at line 12 (\"**No application code yet.**\"); add `app/` and `src/rpg_api/` to the project map (the fenced block at lines 53-69, where line 64 currently reads that rpg_core is \u0027Empty until Phase 1\u0027); fix lines 71-72 which still say the web app doesn\u0027t exist; extend the Setup block (lines 76-80) with the Node steps and both run modes.",
                  "CLAUDE.md: add `app/` and `src/rpg_api/` to the project map, and correct the sentence listing the web app among the things that don\u0027t exist yet, plus the Status section\u0027s \u0027no application code yet\u0027 claim. CLAUDE.md has a hard line budget — this is an EDIT, not an append.",
                  "ops/README.md: add a Node-toolchain section beside the uv one (which occupies lines 32-62), documenting the pinned node major and the npm-ci lockfile rule with the same sharpness the uv rule gets at lines 54-57 (`npm ci` fails when package.json and package-lock.json disagree). Add BOTH run modes: the two-terminal dev seam and the console-script served build. Per Decision 9, document the console script as the ONE canonical way to run the served build — do not also document a raw uvicorn incantation.",
                  "ops/README.md: generalize the rename warning at lines 21-24 to cover job ADDITION, and state loudly that branch-protection.json is inert until re-applied with `gh api -X PUT` (the command at line 12; owner/repo verified matching `git remote -v` = jordan-koch/nba2k-rpg).",
                  "ROADMAP.md line 156: the Phase 1 header prose reads \"**IN-PROGRESS** — 1.1 `app-shell` is at intake. No application code has landed yet.\" Both sentences are now false. This is PROSE, not a Status cell — /commit\u0027s Step 4 (SKILL.md lines 109-144) owns the Status column and the `**Status:**` marker, not the surrounding sentence. Fix it by hand in this phase.",
                  "tests/test_no_leaks.py line 37: correct the docstring \"Binary and lockfiles are skipped\" — true of uv.lock, false of app/package-lock.json. This item is what makes the statement wrong, so this item fixes it.",
                  "Add the AC 17 structural test to tests/test_repo_structure.py, using the idiom already there for \u0027the repo and its documents agree\u0027 (e.g. `test_request_tracks_readme_links_every_track` at lines 107-110 reads a file and asserts on substrings). Assert: README.md no longer contains \"No application code yet\"; CLAUDE.md\u0027s project map contains both `app/` and `src/rpg_api/` and no longer states the web app doesn\u0027t exist; ops/README.md contains a Node-toolchain heading and both run-mode commands.",
                  "Advance the pipeline artifacts: set requests/feature-requests/README.md\u0027s Index row (line 106) Stage cell to `plan` when the plan lands, and IMPLEMENTATION_PLAN.md\u0027s own status blockquote per the grammar at README.md lines 96-100.",
                  "MARKDOWN RAIL for every document written in this phase and for the plan itself: `app/`, `src/rpg_api/`, `app/dist/`, `tests/conftest.py`, `datasets/manifest.json` go in fenced blocks or inline code — NEVER a markdown link. tests/test_request_links.py `_dead_links` (lines 40-64) resolves every relative markdown link in every live `.md` under requests/ and .claude/skills/, and FENCED_BLOCK (line 26) strips ONLY fenced blocks — inline backticks are NOT stripped. This trap already fired twice during scoping.",
                  "Green gate: the four commands, with `uv run pytest tests/test_repo_structure.py tests/test_request_links.py` explicitly (AC 16, AC 17)."
              ],
    "acceptance":  [
                       "`uv run pytest tests/test_repo_structure.py` green including the new documentation test (AC 17).",
                       "`uv run pytest tests/test_request_links.py` green — no markdown link in any live requests/ artifact points at a path that does not resolve (AC 16).",
                       "`grep -n \"No application code yet\" README.md` returns nothing.",
                       "`grep -n \"at intake\" ROADMAP.md` returns nothing.",
                       "ops/README.md documents exactly one canonical way to run the served build.",
                       "tests/test_no_leaks.py line 37\u0027s docstring is accurate about package-lock.json."
                   ],
    "commit_note":  "/commit — this is the one to run the FULL /update-docs sweep on (commit SKILL.md lines 85-95: a new directory, a new convention, a changed setup step, and a request artifact whose status advanced all fire). Subject: \"Update docs for the app shell and add the doc-agreement test\". This is also where ROADMAP.md row 1.1 (line 165) becomes DONE — /commit decides that by matching the Deliverable cell against the tree, not by the branch name."
}

{
    "name":  "Phase 7 — User-run acceptance and the ordered required-check gate",
    "goal":  "Hand the four criteria only a human can prove back to the user, in the order that makes the required check actually take effect before the PR merges.",
    "steps":  [
                  "The agent\u0027s work stops at the push. /commit pushes the feature branch (SKILL.md Step 7, lines 210-233); it does NOT open the PR, never pushes main, never force-pushes. The PR and the merge are the user\u0027s.",
                  "Write the AC 23 ordered gate INTO the PR description, as four numbered steps, because sequencing is the whole point: (1) push the branch and let the new job report once, confirming the context name verbatim; (2) `gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json`; (3) confirm the new check shows as **Required** on the open PR; (4) then merge. Re-applying AFTER merge guarantees that the PR introducing the job is exactly the one that can land with a red frontend.",
                  "State plainly in the handoff that an agent CANNOT do step 2 — `gh api *` is in .claude/settings.json\u0027s `ask` list (line 8) — and that editing ops/branch-protection.json alone never changes anything on GitHub. Verified for the user beforehand: `git remote -v` returns jordan-koch/nba2k-rpg, matching ops/README.md lines 12 and 29.",
                  "Hand over AC 19: `uv run \u003cconsole-script\u003e` serves the built app.",
                  "Hand over AC 20 (dev seam): two commands in two terminals — the reload backend, and `npm run dev` in app/. The Vite URL renders the version string AND the browser network tab shows /api/health served on the VITE origin, not a cross-origin call to the API port. That second half is what actually proves the proxy, and therefore the no-CORS-middleware decision.",
                  "Hand over AC 21 (built seam): `npm run build`, then the console script alone — the same page renders at the uvicorn origin with no Vite dev server running.",
                  "Hand over AC 22 (failure state): with the page open, stop the backend; the page renders a legible \u0027backend unreachable\u0027 panel naming the start command, not a blank screen or an uncaught console error.",
                  "If the implementer spawns ANY subagent during this item, tell it git is read-only — no checkout/reset/restore/clean/stash and nothing that discards working-tree state. The push and prune allowances are the main agent\u0027s alone (CLAUDE.md)."
              ],
    "acceptance":  [
                       "USER-RUN AC 19: the console-script entrypoint resolves and starts the served-build mode.",
                       "USER-RUN AC 20: the version string renders at the Vite origin and the network tab shows /api/health on that same origin.",
                       "USER-RUN AC 21: the same page renders at the uvicorn origin with no Vite process running.",
                       "USER-RUN AC 22: stopping the backend produces a legible named-command panel.",
                       "USER-RUN AC 23: the new context shows as Required on the open PR BEFORE the merge button is used.",
                       "No agent invoked `gh api`, `git merge`, or `git push origin main` at any point."
                   ],
    "commit_note":  "No commit of code here. If the PR description or ops/README.md needs a wording fix as a result of what the user observes, that is one more /commit on the same branch — never an --amend (commit SKILL.md lines 205-207)."
}

### testing

THE PER-PHASE GREEN GATE, unchanged from ops/README.md lines 66-73 ("the same four commands CI runs, in the same order"), run before every /commit: `uv run ruff check`, `uv run ruff format --check`, `uv run mypy`, `uv run pytest`. From Phase 4 onward add, from app/: `npm ci`, `npm run typecheck`, `npm run typecheck:negative`, `npm run lint`, `npm run test`, `npm run build` — these are exactly the steps the new CI job runs, so a green local run predicts a green CI run (AC 10).

WHAT PROVES WHAT.
- Health payload and both dist branches (AC 2, 5, 6, 7): `fastapi.testclient.TestClient` only, parameterized on the injectable dist location via the new `tests/conftest.py` fixture. No live server, no socket. The absent-dist case is the branch every cold agent hits first, because a fresh clone has no built SPA — verified today: `app/dist/index.html` is gitignored (.gitignore lines 62 and 68, both confirmed by `git check-ignore --no-index`).
- Version correctness needs NO new test: tests/test_repo_structure.py lines 46-54 already pin `rpg_core.__version__` to pyproject.toml, and the payload reads the attribute rather than re-typing the string, so the pin transits.
- Layering (AC 3): a pure function + two tmp_path unit tests (a fake module with `import fastapi` -> reports exactly that file; a clean tree -> none) + the real assertion against `src/rpg_core/`. Red-and-green in one `uv run pytest` with zero tracked-source mutation.
- CI contexts (AC 4): `yaml.safe_load` over .github/workflows/ci.yml, `jobs.*.name` collected into a set, asserted EQUAL to ops/branch-protection.json line 4's `contexts`. Plus a negative assertion that a step-level name (ci.yml line 58 "Gitleaks", line 30 "Install") does not enter the set — that is what proves the parser is structure-aware rather than a substring grep.
- Packaging (AC 14): `tomllib` read of pyproject.toml asserting `src/rpg_api` in the hatch packages list, plus ci.yml's pytest step naming rpg_api in --cov. This is the ONLY thing that can see the packaging omission, because pythonpath = ["src"] (pyproject.toml line 73) masks it from every other test.
- Frontend strictness (AC 11): a committed ill-typed fixture excluded from the build, checked by `npm run typecheck:negative` asserted to exit NON-zero. A tsconfig that checks nothing passes a positive typecheck; only the negative case catches it.
- Frontend behavior (AC 12): exactly two Vitest tests — the status page renders the fetched version; the unreachable panel renders on a rejected fetch. The unreachable state is real branching logic, which is why Decision 1 gave it a test.
- Public-repo safety (AC 13): `uv run pytest tests/test_no_leaks.py` run BEFORE staging the lockfile, not after. Plus a local gitleaks run before pushing. Both are labelled *inferred* in the scope (risks 4 and 5) and are cheap to measure, expensive to discover at PR time.
- Documentation (AC 17): a structural test in tests/test_repo_structure.py using the same read-file-and-assert-substrings idiom as `test_request_tracks_readme_links_every_track` (lines 107-110). This exists because Goal 7 otherwise has no pass/fail check at all.
- Existing guards survive (AC 16): `uv run pytest tests/test_repo_structure.py tests/test_request_links.py` after every phase that adds a directory or writes markdown.
- Real-server behavior (AC 18): only the CI smoke step exercises uvicorn, the static mount against a real filesystem, and the built artifact. TestClient exercises none of them. Bounded readiness poll, never a fixed sleep.

REGRESSION SAFETY. The three existing test modules must stay green untouched through every phase; the only edit any of them receives is the docstring correction at tests/test_no_leaks.py line 37 and the two additions to tests/test_repo_structure.py. `git diff src/rpg_core/` must be empty at the end of the item — that single command is the cheapest proof that the no-domain-logic non-goal held.

WHAT IS NOT TESTED AND MUST NOT BE CLAIMED. AC 19-23 are USER-RUN per requests/feature-requests/README.md lines 71-73. The acceptance panel must not claim them. In particular the proxy-origin observation (AC 20) is only provable in a browser network tab, and the required-check activation (AC 23) is only provable on the live PR after a `gh api -X PUT` the agent is not permitted to run.

### risks

CONVENTION — the markdown-link trap, and it has already fired twice. tests/test_request_links.py `_dead_links` (lines 40-64) resolves every relative markdown link in every live `.md` under requests/ and .claude/skills/, and FENCED_BLOCK (line 26) strips ONLY fenced blocks — inline backticks are NOT stripped, despite a scoping finding that claimed otherwise. A single markdown link to `app/` or `src/rpg_api/` written in the plan turns CI red on the very PR that lands the plan. Mitigation: every path this item creates appears as inline code or inside a fenced block, never as a link target.

CONVENTION — /commit's mandate is narrower than it looks. commit SKILL.md Step 4 (lines 109-144) owns ROADMAP.md's Status CELLS and the phase `**Status:**` markers. It does NOT own surrounding prose. ROADMAP.md line 156 ('1.1 `app-shell` is at intake. No application code has landed yet') is prose, is now false, and is covered by neither /commit nor AC 17. It needs a hand edit in Phase 6 or it silently rots.

CONVENTION — an agent cannot finish this item. `gh api *`, `git commit *`, `git push *` and `git merge *` are all in .claude/settings.json's `ask` list (lines 4-11). Editing ops/branch-protection.json changes nothing on GitHub until the user runs the PUT. A plan that treats the required-check activation as done-when-the-JSON-is-edited ships the headline risk unmitigated.

CONVENTION — the pull to make the status page interesting. The scope names this as 'the single strongest failure mode for this item' and again as risk 12. `careers/`, `rulesets/`, `datasets/` and `lib/` are all verified absent, and CLAUDE.md says not to create them speculatively. Decision 6's standing rule is the operative rail: the health payload gains a field only when the thing it reports exists. No career_count, no ruleset_version, no stub player.

PACKAGING — the sneakiest failure in the item. Omitting `src/rpg_api` from pyproject.toml line 31's hatch packages list passes every local test, goes green in CI, and fails with ModuleNotFoundError on the user's installed environment — because line 73's `pythonpath = ["src"]` puts the package on the path for tests regardless. The test suite structurally cannot otherwise see it. AC 14's guard is the only mitigation.

PUBLIC REPO — the leak guard now scans frontend files, and this belief is *inferred, not measured*. tests/test_no_leaks.py TEXT_SUFFIXES (lines 38-55) already covers .json/.ts/.tsx/.css/.html, and line 70 filters tracked files by that set. Two concrete tripwires: a package.json `author` field trips EMAIL (line 29); a Windows-generated config writing an absolute path trips WINDOWS_PATH (line 26). Run it before staging the lock. If it trips, the ONLY sanctioned fix is a narrowly-justified ALLOWED entry (lines 32-35) with a written reason — never a weakened regex, never a removed suffix.

GITLEAKS — unassessed and blocking. The secrets job (ci.yml lines 49-61) runs gitleaks over full history with fetch-depth: 0 and blocks merge, and the repo has NO .gitleaks.toml and NO .gitleaksignore (verified absent). This item adds a lockfile full of high-entropy base64 sha512 integrity strings to that scan. Lower-probability than it sounds, but cheap to check locally and expensive to discover at PR time.

MYPY STRICT over FastAPI route decorators is *unconfirmed* until run (scope risk 6). The failure mode to REFUSE is a per-module override quietly carving rpg_api out of strict on its first day — the exact asymmetry this item exists to prevent on the frontend side. Pinned by AC 8; measured in Phase 1 before any route is written.

STARLETTE StaticFiles on a missing directory is labelled *Inferred* in the scope (risk 7), not measured. If it raises at construction, a fresh clone gets an import-time traceback instead of an app. This is why the dist path is an injectable factory argument and why Phase 1 measures the behavior before Phase 2 designs around it.

WINDOWS/CI SHELL PARITY. Daily shell is PowerShell 5.1, which has NO `&&` at all; CI is ubuntu-latest. Any package.json script using `&&`, `rm -rf`, `cp`, or a POSIX inline env-var prefix works in CI and fails locally, which is the worst direction for the failure to point. Keep every script to a single command invocation with no shell operators.

WINDOWS/NODE IPv6. A Vite proxy targeting http://localhost:PORT can resolve to ::1 on Windows while uvicorn binds 127.0.0.1, producing an ECONNREFUSED that looks exactly like the backend being down while it is running fine. Pin the proxy target to the IPv4 literal 127.0.0.1.

SILENT GITIGNORE SHADOWING. .gitignore line 62's blanket `dist/` and line 63's blanket `build/` match a directory of that name at ANY depth. Today that is benign (verified: app/package.json and app/src/main.tsx are not ignored; app/dist and node_modules are). But a source file that lands in a directory named build or dist under app/ would be silently untracked with nothing complaining. Cross-check `git status --untracked-files=all app/` against `git check-ignore` before staging. The scope records the same hazard as risk 15 for item 2.1.

ROOT-SCOPED FRONTEND CONFIG. `git ls-files .claude` returns 8 tracked .js/.mjs files. An eslint or tsconfig at the repo root would immediately start reporting on them and force an ignore list nobody scoped. Both configs live inside app/ with file scope limited to app/ — this is an explicit Non-Goal, not a style preference.

SUBAGENT GIT. If the implementer spawns any subagent — plausible for scaffolding the SPA — it must be told git is read-only: no checkout/reset/restore/clean/stash, nothing that discards working-tree state. The push and prune allowances belong to the main agent alone.

NODE MAJOR SKEW. Local is node v24.15.0 / npm 11.12.1 (measured on this machine, 2026-08-14); CI pins a major in the workflow with no .nvmrc and no engines field (a deliberate scope choice). A lockfileVersion difference between npm majors yields a lockfile that installs locally and fails `npm ci` in CI, with an error pointing at a package rather than at the version skew.

### files_to_touch

{
    "path":  "D:\\projects\\nba2k-rpg\\pyproject.toml",
    "change":  "MODIFY. Line 9: fastapi + uvicorn into `[project].dependencies`. Lines 11-13: DELETE the discharged reservation comment. Lines 16-21: httpx, pyyaml, types-PyYAML, watchfiles into the dev group. Line 31: append `src/rpg_api` to the hatch wheel packages. NEW `[project.scripts]` block for the served-build console entrypoint. Lines 61-65 `[tool.mypy]`: MUST remain textually unchanged."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\uv.lock",
    "change":  "REGENERATE via `uv lock` and commit in the SAME commit as the pyproject change — ci.yml line 34 runs `uv sync --locked`, which hard-fails on a stale lock rather than re-resolving."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\src\\rpg_api\\__init__.py",
    "change":  "CREATE. New package alongside rpg_core. Under src/ specifically so `[tool.mypy] files` (line 65) and `pythonpath` (line 73) both already reach it — zero config churn on those two."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\src\\rpg_api\\app.py",
    "change":  "CREATE. `create_app(spa_dist: Path | None = None) -\u003e FastAPI`. GET /api/health returning status/version/spa_built; version read from `rpg_core.__version__` (the one and only import of the domain core). JSON-404 for unknown /api paths; SPA history fallback for unmatched non-/api paths; 503 naming the build command when dist is absent, never an import-time traceback."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\src\\rpg_api\\__main__.py",
    "change":  "CREATE (or equivalent module named by `[project.scripts]`). The single canonical served-build entrypoint. Decision 9\u0027s caveat: only ONE way to run the served build gets documented."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\conftest.py",
    "change":  "CREATE. Reusable TestClient fixture parameterized on the injectable dist location. Items 1.7-1.11 each need it — writing it once beats five agents inventing five variants."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_api_health.py",
    "change":  "CREATE. AC 2, 5, 6, 7 — health payload, both dist branches against tmp_path, JSON-404 under /api. TestClient only; no live server, no socket."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_layering.py",
    "change":  "CREATE. AC 3 — pure violation-finding function + two tmp_path unit tests + the real zero assertion against src/rpg_core/. Deny-list: fastapi, starlette, uvicorn, the API package. pydantic deliberately ABSENT (ADR 0002; that is item 1.2\u0027s call). Failure message cites DESIGN.md §3 by name."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_repo_structure.py",
    "change":  "MODIFY, three additions. (1) The gitignore guard for app/dist and node_modules, placed right after `test_scratch_root_is_gitignored` (lines 83-92) so it REUSES `_git_check_ignore` (lines 24-34). (2) The AC 4 set-equality guard (yaml.safe_load over ci.yml vs branch-protection.json contexts, plus the negative step-name assertion) — or a sibling module, but reuse the existing tomllib/read-file idioms either way. (3) The AC 14 hatch-packages + --cov guard, and (4) the AC 17 documentation-agreement test."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\tests\\test_no_leaks.py",
    "change":  "MODIFY, one line. Line 37\u0027s docstring \u0027Binary and lockfiles are skipped\u0027 is true of uv.lock and false of app/package-lock.json. This item is what makes it wrong, so this item fixes it. Do NOT touch TEXT_SUFFIXES or the regexes."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\package.json",
    "change":  "CREATE. `\"private\": true`, placeholder version, NO author field carrying an email (tests/test_no_leaks.py line 29 would fail the build). Every script a single command invocation — no `\u0026\u0026`, no `rm -rf`, no `cp`, no POSIX env prefixes."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\package-lock.json",
    "change":  "CREATE and COMMIT. Run `uv run pytest tests/test_no_leaks.py` and gitleaks locally BEFORE staging it. .gitattributes line 41 already declares it linguist-generated with diffs collapsed."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\tsconfig.json",
    "change":  "CREATE. `strict: true` plus noUncheckedIndexedAccess, noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch. Scoped to app/ only. No absolute paths."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\vite.config.ts",
    "change":  "CREATE. Dev-server proxy /api -\u003e the IPv4 literal 127.0.0.1, NOT localhost. No CORS middleware anywhere in either mode. Vitest config block lives here or in a sibling — inside app/, never at the repo root."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\src\\api\\client.ts",
    "change":  "CREATE. Small typed fetch wrapper with a HAND-WRITTEN `Health` interface. Explicitly NOT the deferred OpenAPI codegen contract — it is the seam codegen slots into at item 1.8."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\src\\App.tsx",
    "change":  "CREATE. The entire UI: fetch /api/health, render status and version, render a legible backend-unreachable panel naming the start command on a rejected fetch. No career, no stub player, no fake XP number."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\app\\index.html",
    "change":  "CREATE. Real page title and favicon instead of the Vite template defaults. Identity, not design. .gitattributes line 35 already declares *.ico binary."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.github\\workflows\\ci.yml",
    "change":  "MODIFY. Add a third job parallel with python and secrets, with a display name chosen ONCE and reused verbatim in branch-protection.json. setup-node on a pinned major with npm caching; working-directory app; npm ci / typecheck / typecheck:negative / lint / test / build. Add the real-server smoke step with a bounded readiness poll. Line 47: extend --cov to name rpg_api. NO paths-ignore on any job."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\ops\\branch-protection.json",
    "change":  "MODIFY line 4 — append the new job\u0027s display name to `contexts`, in the SAME COMMIT as the ci.yml change. The file is inert until the user re-applies it with `gh api -X PUT`."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.github\\dependabot.yml",
    "change":  "MODIFY. Add the npm ecosystem entry mirroring the uv entry\u0027s posture (lines 16-28: monthly, commit-message prefix, labels, semver-patch ignore) and DELETE the line-30 placeholder comment."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\ops\\README.md",
    "change":  "MODIFY. New Node-toolchain section beside the uv one (lines 32-62), with the npm-ci lockfile rule stated as sharply as the uv rule at lines 54-57. Both run modes, with the console script as the single documented way to serve the built app. Generalize the job-rename warning (lines 21-24) to job ADDITION."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\README.md",
    "change":  "MODIFY. Remove the line-12 \u0027No application code yet\u0027 banner; add app/ and src/rpg_api/ to the project map block (lines 53-69, note line 64\u0027s \u0027Empty until Phase 1\u0027); fix lines 71-72\u0027s \u0027the web app don\u0027t exist yet\u0027; extend the Setup block (lines 76-80) with the Node steps and both run modes."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\CLAUDE.md",
    "change":  "MODIFY, as an EDIT not an append (hard line budget). Project map gains app/ and src/rpg_api/; the sentence listing the web app among things that don\u0027t exist yet, and the Status section\u0027s \u0027no application code yet\u0027, both stop being false."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\ROADMAP.md",
    "change":  "MODIFY. Line 156\u0027s phase-header PROSE (\u00271.1 `app-shell` is at intake. No application code has landed yet\u0027) is stale and is owned by neither /commit\u0027s Status-cell mandate nor AC 17 — fix it by hand. Row 1.1\u0027s Status cell (line 165) is /commit\u0027s to advance against the diff."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\.editorconfig",
    "change":  "CREATE. Must AGREE with .gitattributes line 3 (`* text=auto eol=lf`); an .editorconfig specifying crlf would fight the repo\u0027s normalization."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\requests\\feature-requests\\README.md",
    "change":  "MODIFY line 106 — advance the 1.1-app-shell Index row\u0027s Stage cell to `plan`, matching the row by its [1.1-app-shell] link."
}

{
    "path":  "D:\\projects\\nba2k-rpg\\requests\\feature-requests\\1.1-app-shell\\IMPLEMENTATION_PLAN.md",
    "change":  "CREATE. Opens `\u003e **Status:** plan · created 2026-08-14 · decided · next: implement`. Sections 1-8 and 10 of the stage-3 menu; section 9 (Data contracts) is OMITTED — see the open questions for the affirmative justification."
}

### code_references

{
    "ref":  "pyproject.toml:9",
    "claim":  "`dependencies = []` — the empty runtime list this item replaces with fastapi + uvicorn."
}

{
    "ref":  "pyproject.toml:11-13",
    "claim":  "The reservation comment \u0027FastAPI arrives with Phase 1 item 1.1 (app-shell)\u0027. This item discharges it, so the comment must be DELETED, not left in place."
}

{
    "ref":  "pyproject.toml:16-21",
    "claim":  "`[dependency-groups].dev` currently holds exactly pytest, pytest-cov, ruff, mypy. httpx, pyyaml, types-PyYAML and watchfiles join here."
}

{
    "ref":  "pyproject.toml:31",
    "claim":  "`packages = [\"src/rpg_core\"]` — the hatch wheel list that must gain src/rpg_api. Omitting it fails only at runtime (scope risk 2)."
}

{
    "ref":  "pyproject.toml:49",
    "claim":  "`\"DTZ\",` in the ruff select list — naive-datetime lint. This is the tax that made started_at/uptime unattractive in the health payload (Decision 6)."
}

{
    "ref":  "pyproject.toml:61-65",
    "claim":  "`[tool.mypy]` — python_version 3.12, strict = true, warn_unreachable = true, files = [\"src\", \"tests\"]. AC 8 requires this block be textually UNCHANGED; files already reaches src/rpg_api with no edit."
}

{
    "ref":  "pyproject.toml:73",
    "claim":  "`pythonpath = [\"src\"]` — the line that masks a missing hatch packages entry from every local test, which is why AC 14\u0027s structural guard is the only thing that can see it."
}

{
    "ref":  ".github/workflows/ci.yml:19",
    "claim":  "`name: Lint, types, tests` — the first job DISPLAY NAME, matched verbatim by ops/branch-protection.json line 4."
}

{
    "ref":  ".github/workflows/ci.yml:34",
    "claim":  "`run: uv sync --locked` — verbatim what AC 1 requires to exit 0; it hard-fails on a stale lock rather than re-resolving."
}

{
    "ref":  ".github/workflows/ci.yml:47",
    "claim":  "`uv run pytest -m \"not network\" --cov=rpg_core --cov-report=term-missing` — the one line that must gain rpg_api, and the flag AC 14\u0027s guard asserts on."
}

{
    "ref":  ".github/workflows/ci.yml:50",
    "claim":  "`name: Secret scan` — the second job display name; with a third job added, the name set becomes exactly three entries and must EQUAL the contexts array."
}

{
    "ref":  ".github/workflows/ci.yml:58",
    "claim":  "The `- name: Gitleaks` STEP name. AC 4\u0027s negative assertion proves a step-level name does not enter the jobs.*.name set — the check that the parser is structure-aware rather than a substring grep."
}

{
    "ref":  "ops/branch-protection.json:4",
    "claim":  "`\"contexts\": [\"Lint, types, tests\", \"Secret scan\"]` — the exact array the new job\u0027s display name joins, in the same commit as the workflow change."
}

{
    "ref":  "ops/README.md:12",
    "claim":  "`gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection --input ops/branch-protection.json` — the AC 23 step 2 command. VERIFIED: `git remote -v` returns jordan-koch/nba2k-rpg, so the owner/repo still matches (this was the scope\u0027s UNCONFIRMED item 1)."
}

{
    "ref":  "ops/README.md:21-24",
    "claim":  "The blockquote warning that renaming a CI job silently breaks branch protection — \u0027PRs wait forever for a check that never reports, with no error explaining why\u0027. This item generalizes it to job ADDITION."
}

{
    "ref":  "ops/README.md:66-73",
    "claim":  "\u0027The same four commands CI runs, in the same order\u0027 — ruff check, ruff format --check, mypy, pytest. This is the per-phase green gate the plan prescribes before every /commit."
}

{
    "ref":  "tests/test_repo_structure.py:24-34",
    "claim":  "`_git_check_ignore(relative_path)` using `git check-ignore -q --no-index` — works on paths that do not exist yet, which is why the new app/dist guard must be added to THIS module and reuse it rather than duplicating the subprocess call."
}

{
    "ref":  "tests/test_repo_structure.py:46-54",
    "claim":  "`test_package_version_matches_pyproject` pins rpg_core.__version__ to pyproject.toml. Because the health payload reads the attribute rather than re-typing the string, this existing test transitively covers the payload — no new version test needed."
}

{
    "ref":  "tests/test_repo_structure.py:83-92",
    "claim":  "`test_scratch_root_is_gitignored` — the literal template for the new app/dist + node_modules gitignore guard, including the RuntimeError -\u003e pytest.skip pattern for a machine without git."
}

{
    "ref":  "tests/test_no_leaks.py:26",
    "claim":  "`WINDOWS_PATH` regex — fails the build on any tracked drive-letter path. Why the SPA dist default must be repo-relative and why generated frontend configs must be checked before staging."
}

{
    "ref":  "tests/test_no_leaks.py:29",
    "claim":  "`EMAIL` regex — a package.json `author` field carrying an address fails this blocking check (scope risk 4)."
}

{
    "ref":  "tests/test_no_leaks.py:32-35",
    "claim":  "`ALLOWED` — exactly two entries today, each with a written reason. The ONLY sanctioned escape hatch if a frontend file trips a pattern; never a weakened regex, never a removed suffix."
}

{
    "ref":  "tests/test_no_leaks.py:37",
    "claim":  "The docstring \u0027Extensions worth scanning. Binary and lockfiles are skipped.\u0027 — true of uv.lock, false of app/package-lock.json. This item makes it wrong, so this item fixes it."
}

{
    "ref":  "tests/test_no_leaks.py:38-55",
    "claim":  "`TEXT_SUFFIXES` already contains .json, .ts, .tsx, .css, .html, .js, .mjs — so the leak guard starts scanning the frontend the moment it is tracked. AC 13 is a real gate, not a formality."
}

{
    "ref":  "tests/test_request_links.py:26",
    "claim":  "`FENCED_BLOCK` — strips ONLY 3+ backtick/tilde fences (blockquoted allowed). Inline backticks are NOT stripped, contradicting a scoping finding. This is why the plan writes app/ and src/rpg_api/ as inline code or fenced text but never as a markdown link."
}

{
    "ref":  "tests/test_request_links.py:40-64",
    "claim":  "`_dead_links` resolves every relative markdown link target against the file\u0027s own directory. A link to a path this item creates would turn CI red on the very PR that creates it."
}

{
    "ref":  ".gitignore:62",
    "claim":  "Blanket `dist/` — matches a directory named dist at ANY depth. Verified with `git check-ignore --no-index`: app/dist/index.html IS ignored. Same silent-shadowing class as line 63\u0027s `build/`, which the scope flags as risk 15 for item 2.1."
}

{
    "ref":  ".gitignore:66-68",
    "claim":  "The Node/web-app block — `node_modules/`, `.vite/`, `app/dist/` — reserved in Phase 0, which is the verified evidence for the app/ convention (NOT CLAUDE.md, whose claim to that effect the scope proved false)."
}

{
    "ref":  ".gitattributes:3",
    "claim":  "`* text=auto eol=lf` — the repo decides line endings, not the machine. The new .editorconfig must agree with this or the two fight."
}

{
    "ref":  ".gitattributes:41",
    "claim":  "`package-lock.json linguist-generated=true -diff` — Phase 0 already reserved the SPA lockfile by name, collapsing it in diffs and language stats."
}

{
    "ref":  ".github/dependabot.yml:16-28",
    "claim":  "The uv entry — monthly interval, commit-message prefix, labels, and the semver-patch ignore block. The posture the npm entry mirrors."
}

{
    "ref":  ".github/dependabot.yml:30",
    "claim":  "\u0027# npm arrives with Phase 1 item 1.1 (app-shell). Add the ecosystem entry then.\u0027 — the placeholder AC 15 requires be gone."
}

{
    "ref":  "src/rpg_core/__init__.py:3-9",
    "claim":  "\u0027Deliberately I/O-free and web-free... The API and the web app depend on it; it depends on neither.\u0027 The docstring the layering guard mechanizes. This file must be byte-identical after the item lands."
}

{
    "ref":  "src/rpg_core/__init__.py:16",
    "claim":  "`__version__ = \"0.1.0\"` — the single attribute the health payload reads, giving rpg_api exactly one honest reason to import the domain core."
}

{
    "ref":  "DESIGN.md:106-108",
    "claim":  "\u0027Two packages, one repo. `src/rpg_core/` is the I/O-free domain; the API and web app depend on it and it depends on neither.\u0027 Under the §3 heading at line 99. The layering guard\u0027s failure message must cite this by name (Decision 3: a guard test instead of ADR 0010)."
}

{
    "ref":  "ROADMAP.md:156",
    "claim":  "\u0027**Status:** **IN-PROGRESS** — 1.1 `app-shell` is at intake. No application code has landed yet.\u0027 Both sentences become false. This is PROSE, owned by neither /commit\u0027s Status-cell mandate nor AC 17 — it needs a hand edit."
}

{
    "ref":  "ROADMAP.md:165",
    "claim":  "Row 1.1 — Size M, Needs 0.3, Status IN-PROGRESS. Decision 7 makes the M advisory rather than descriptive; /commit maintains status, not size, so the M is flagged not changed."
}

{
    "ref":  "README.md:12",
    "claim":  "\u0027\u003e **Phase 0.** Repo, process, and CI harness exist. **No application code yet.**\u0027 — the exact string AC 17 asserts is gone."
}

{
    "ref":  "README.md:71-72",
    "claim":  "\u0027`careers/`, `datasets/`, `rulesets/`, `lib/`, and the web app don\u0027t exist yet.\u0027 — false once app/ lands; part of AC 17\u0027s doc-drift surface alongside the project map at lines 53-69."
}

{
    "ref":  ".claude/settings.json:4-11",
    "claim":  "The `ask` list: `git commit *`, `git push *`, `git merge *`, `gh api *`. This is the mechanism behind \u0027agents commit only through /commit\u0027 and behind AC 23 step 2 being unreachable for an agent."
}

{
    "ref":  ".claude/settings.json:16-17",
    "claim":  "`PowerShell(node *)` and `PowerShell(npm *)` already in the allow list — reserved in Phase 0 for this exact item, so npm ci / npm run build need no permission prompt."
}

{
    "ref":  ".claude/skills/commit/SKILL.md:109-144",
    "claim":  "Step 4 — /commit owns ROADMAP.md\u0027s per-item Status cells and phase headers, with the \u0027never mark ahead / never mark down silently\u0027 rails and \u0027match on the deliverable, not the branch name\u0027. Its mandate stops at the cells; prose is not covered."
}

{
    "ref":  ".claude/skills/commit/SKILL.md:210-233",
    "claim":  "Step 7 — /commit pushes the feature branch with `git push -u origin \u003cbranch\u003e`, never pushes main, never force-pushes, and never opens the PR. Phase 7\u0027s handoff boundary."
}

{
    "ref":  "docs/data-access.md:113",
    "claim":  "\u0027## 3. External sources · `unconfirmed`\u0027 — every row in this table is an untested belief. Item 1.1 consumes NONE of them, which is why the plan carries no data-contracts section and no source-verification phase for external data."
}

{
    "ref":  "requests/feature-requests/README.md:57-73",
    "claim":  "The definition of testable (\u0027a cold agent can run one command and get a pass or fail\u0027) and the rule that human-only criteria must be marked user-run so the acceptance panel does not claim them — which is what ACs 20-23 rely on."
}

```text
{
    "ref":  "requests/feature-requests/README.md:106",
    "claim":  "The Index row `| [1.1-app-shell](1.1-app-shell/) | scoped | ... |` — the Stage cell that advances to `plan`."
}
```

{
    "ref":  "requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:5-18",
    "claim":  "The load-bearing Authoring rule: every path this item CREATES is written inline or fenced, never as a markdown link — and the explicit correction that inline backticks do NOT make a quote safe, only fenced blocks do."
}

{
    "ref":  "requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:40-43",
    "claim":  "\u0027Contract applicability, verified. No dataset: datasets/manifest.json does not exist (it is item 2.1)... No ledger or economy: careers/ and rulesets/ do not exist.\u0027 Independently re-verified by filesystem probe on 2026-08-14."
}

{
    "ref":  "requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:511",
    "claim":  "Decision 6\u0027s standing rule for every later item: \u0027the payload gains a field only when the thing it reports exists\u0027 — the operative rail against risk 12\u0027s scope leakage."
}

### open_questions

WHY SECTION 9 (Data contracts touched) IS OMITTED — stated affirmatively so a reviewer knows it was decided, not forgotten. This item registers no source, declares no grain, defines no keys, pulls no seasons, and makes zero network requests (telemetry and outbound calls are an explicit Non-Goal). Verified by filesystem probe on 2026-08-14: `datasets/`, `careers/`, `rulesets/` and `lib/` do not exist; `datasets/manifest.json` is item 2.1. Nothing is written to `var/cache/`. The five contracts — grain, keys, coverage, update semantics, pull cost — have no subject. The plan must NOT invent a placeholder manifest entry to look complete; CLAUDE.md forbids creating those directories speculatively.

CONSOLE-SCRIPT NAME (needs a one-word answer before Phase 1). `[project.scripts]` gets exactly one entrypoint and Decision 9's caveat is that only ONE canonical way to run the served build gets documented. The name is baked into ops/README.md, README.md's Setup block, and AC 19. Candidates: `nba2k-rpg`, `rpg-serve`, `rpg`. Pick before writing the pyproject block, because renaming it later means editing four files.

CI JOB DISPLAY NAME (needs an answer before Phase 5, and it must be typed identically in two files). Suggested `Web app`. The exact string goes in ci.yml's `name:` and in ops/branch-protection.json line 4's contexts array. AC 4's set-equality guard exists precisely because a case difference ('Web app' vs 'Web App') passes a containment check while hanging every PR forever.

SMOKE-STEP JOB PLACEMENT. AC 18 needs both Python and Node. One job with setup-uv alongside setup-node is simplest and keeps the job-name set at exactly three, which keeps AC 4's set equality clean. The alternative — an artifact handoff between two jobs — adds a fourth job name that must also appear in contexts and doubles the flake surface (risk 14). Recommend one job; flagging it because it is a plan-shaping call the scope left open.

DEFAULT API PORT. Decision 5 rules out an `RPG_API_PORT` env key, so a loopback default is hardcoded in exactly two places: the console script and the Vite proxy target. Pick one number and note in ops/README.md that these two must stay in step — the scope's stated reason for rejecting the env key was avoiding a SECOND place for the target to drift, so the plan should name the one place of record.

`.editorconfig` vs `.gitattributes`. .gitattributes line 3 forces `eol=lf` repo-wide with a CRLF exception only for .ps1/.psm1/.bat/.cmd (lines 7-10). The new .editorconfig must specify `end_of_line = lf` and either omit the Windows-script types or match the CRLF exception. Getting this wrong makes two tools fight over the same files, and the symptom is diff churn nobody can localize.

FAVICON FORMAT. .gitattributes line 35 declares `*.ico binary`, which anticipates an .ico — but .ico is not in tests/test_no_leaks.py's TEXT_SUFFIXES, so it is never leak-scanned. An .svg favicon would be scanned but has no .gitattributes entry. Either is fine; the plan should pick one so the implementer does not add a third pattern to .gitattributes on a whim.

GITLEAKS REMEDIATION SHAPE, if it trips. The repo has neither .gitleaks.toml nor .gitleaksignore (verified absent). If the lockfile's sha512 integrity strings fire a rule, the choice is between a .gitleaksignore of specific fingerprints and a scoped path allowlist. Both are new tracked config the scope did not budget. Recommend fingerprints with a written reason each, mirroring the ALLOWED discipline at tests/test_no_leaks.py lines 32-35 — but flag it, because it is a new file in a repo that guards its tracked footprint.


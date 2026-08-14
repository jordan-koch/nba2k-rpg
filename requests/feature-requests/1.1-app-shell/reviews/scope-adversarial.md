# Scope Panel - Adversarial Findings & Convergence

> Provenance trail for `/scope-feature` on `1.1-app-shell`, run 2026-08-13/14.
> Verbatim output of the two adversary lenses plus the merge stage's convergence
> map. Not every finding here was accepted into PROJECT_SCOPE.md - the ones that
> were, and the ones judged overstated, are recorded in that document.
>
> Two mechanical edits, applied so this file can be tracked in a public repo:
> placeholder email addresses are replaced with `<email-redacted>`, and any
> passage quoting a markdown link to a not-yet-existing path is wrapped in a
> fenced block - the exemption tests/test_request_links.py documents, so a report
> can quote a dead target without turning CI red. Text is otherwise verbatim.

Totals: 44 findings (major=14, minor=18, nit=7, question=4, blocker=1). Panel health: scopers 3/3, adversaries 2/2, no degraded lenses.

---

## Convergence map

Where two or more scopers independently agreed - the panel's highest-signal output.

### Branch-protection context drift is the item's headline risk, and editing the JSON does not apply it

**Lenses:** fit, ambitious, minimalist

All three independently ranked this first or near-first, and all three landed on the same two-part mitigation: a guard test for the tracked half (ci.yml job names ⊆ ops/branch-protection.json:4 contexts) plus a user-run criterion for the applied half, because `gh api *` sits in .claude/settings.json's ask list. The failure is silent — a PR merges green while the frontend job was red — and it is the only failure here that is invisible until broken code is already on main.

### A guard test making 'rpg_core stays web-free' mechanical rather than aspirational

**Lenses:** fit, ambitious, minimalist

Unanimous, and unanimous on the reasoning: this is the exact commit that introduces the thing the domain core must stay free of, the constraint is asserted in three documents (src/rpg_core/__init__.py:3-4, CLAUDE.md, DESIGN.md §3) and enforced by nothing, and it protects items 1.2-1.11. Convergence strong enough to promote it from enhancement to core. The lanes differed only on whether pydantic belongs in the deny-list — resolved against, on ADR 0002 grounds.

### Missing app/dist/ must not crash at import, and the dist location must be injectable to make both branches testable

**Lenses:** fit, ambitious, minimalist

All three reached the same non-obvious consequence from the request's Open Question 2: the acceptance criterion ('app starts with dist absent') is only satisfiable if the path is a factory argument rather than a module constant. That is a design constraint falling out of testability, arrived at independently three times — and it also dissolves the env-var question, since injectability does not require .env keys.

### Three configuration sites bind to a second source package, and one of them fails invisibly

**Lenses:** fit, ambitious, minimalist

All three flagged [tool.hatch.build.targets.wheel].packages (pyproject.toml:31), ci.yml's --cov=rpg_core (line 47), and [tool.mypy].files (line 65, which already covers src/ so needs no edit). The minimalist added the sharpest observation: pythonpath = ["src"] (line 73) means an omitted packages entry passes every test and CI while breaking the installed environment — a failure the test suite structurally cannot see, which is why it earns its own acceptance criterion.

### The frontend enters tests/test_no_leaks.py's blast radius for the first time

**Lenses:** fit, ambitious, minimalist

All three checked TEXT_SUFFIXES (lines 38-55) and independently caught that the file's own docstring claim about lockfiles is true for uv.lock and false for package-lock.json. All three also converged on the correct remedy if it trips: an ALLOWED entry with a written reason, never a weakened regex — which is the right instinct for a blocking guard on a public repo.

### Package name src/rpg_api/ and route prefix /api, decided deliberately because eleven items inherit them

**Lenses:** fit, ambitious, minimalist

Three independent lanes proposed the identical name and prefix, for the same reason: it names the layer's job, pairs symmetrically with rpg_core, and the /api prefix gives the serving boundary an unambiguous rule. Unanimity on a naming call with six binding sites (mypy files, hatch packages, --cov, the layering deny-list, the proxy rule, every downstream import) is about as strong a signal as this stage produces.

### mypy strict + FastAPI decorators is the likeliest source of implementation friction, and the wrong fix is a per-module override

**Lenses:** fit, ambitious, minimalist

All three named disallow_untyped_decorators specifically and all three refused the easy escape hatch on the same grounds — carving rpg_api out of strict on its first day would make the API half permanently weaker than the domain half, which is precisely the asymmetry this item exists to prevent on the frontend. Converted into an acceptance criterion that names the escape hatch and forbids it.

### The frontend test harness is a genuine judgment call, not a default — and the lanes split

**Lenses:** fit, ambitious, minimalist

High signal precisely because it did NOT converge. Intake put Vitest out on 'nothing to test' grounds and explicitly invited disagreement; ambitious said in (citing item 0.2 shipping toolchain and first test together), minimalist said out (citing a harness whose only subject is its own fixture), fit called it cheap-but-deliberate. Three lanes, three positions, all defensible — the definition of something that goes to the human rather than getting quietly folded.

### Windows/PowerShell reality shapes concrete implementation choices

**Lenses:** ambitious, minimalist

Two lanes independently surfaced non-obvious, specific hazards that a Linux-CI-only plan would miss and that would present as confusing runtime failures: npm scripts using && fail in PowerShell 5.1 while passing in CI; a Vite proxy to `localhost` can resolve to ::1 while uvicorn binds 127.0.0.1; uvicorn[standard] bundles uvloop, which has no Windows wheel. These are cheap to get right up front and expensive to diagnose later.

---

## Adversary summaries

### Lens: `fit-ac`

I verified every integration point the merged scope cites, and the repo-fit verdict of `clean` holds up unusually well: all five Phase 0 reservations resolve exactly as claimed (pyproject.toml:9,11-13; .github/dependabot.yml:30; .gitignore:66-68; .gitattributes:41; .claude/settings.json:16-17), datasets/manifest.json genuinely does not exist (it is ROADMAP.md:190 item 2.1) so the five data contracts are correctly N/A, no ADR is engaged, and the scope's correction of the request's false "CLAUDE.md's project map lists serving under app/" claim is itself correct (grep finds no `app/` in CLAUDE.md). The line citations are near-perfect — pyproject, ci.yml, branch-protection, both test files, DESIGN.md §3 all check out; the only drift is .gitignore:65 being a section header rather than a rule. I also confirmed two claims the scope labelled measured or unconfirmed: node v24.15.0 / npm 11.12.1 are installed, and the remote is jordan-koch/nba2k-rpg, matching ops/README.md:12 (that UNCONFIRMED can be struck). Framing is honest — the problem restatement tracks the request, the non-goals name their hard deferrals with reasons and forward pointers rather than burying them, and the item's real tension (an M-sized, non-★ roadmap row accumulating a 13-bullet core plus 13 folds plus 9 gates) is surfaced by the scope itself. The damage is concentrated in acceptance-criteria testability, not in fit. Four criteria do not meet requests/feature-requests/README.md:59-61's "one command, pass or fail" bar: two are source-mutation demonstrations (AC 3, AC 11), one is a diff review (AC 8's "zero new type: ignore"), and one core guard is specified two incompatible ways (structure-aware YAML parse vs. "twelve lines of regex" — the latter would match ci.yml's seven step-level `name:` keys) while needing a YAML library that is absent from the dev group of an item whose headline is dependency bookkeeping. Three coverage holes: the documentation goal has no criterion at all, dev-mode wiring has zero objective coverage while the goals read as if both run modes are equally delivered, and the acceptance list assumes cheap folds that gated decision 7 invites the user to drop. One honest-framing miss: the scope declines the request's env-config Constraint — a defensible call, but the request filed it under Non-negotiables and the divergence is never named as one. Plus two unnoticed repo mechanics: the other required check (gitleaks) will scan package-lock.json with no config file in the repo to fall back on, and tests/test_request_links.py will fail on the PROJECT_SCOPE document itself if it markdown-links the paths this item creates.

### Lens: `scope-completeness`

The merged scope is unusually well-grounded — I verified 20+ of its line citations (pyproject.toml:9/11-13/30-31/49/61-65/73, ci.yml:19/24-28/34/47/50, ops/branch-protection.json:4, .gitattributes:41, .github/dependabot.yml:30, tests/test_no_leaks.py:26/32-35/37/38-55, tests/test_repo_structure.py:24-34/46-54/83-92/113-133, ROADMAP.md:165, DESIGN.md:106-109) and every one resolves. Its verified-false correction of the request ("CLAUDE.md's project map lists serving under `app/`") is genuinely false — grep for `app/` in CLAUDE.md returns nothing. Node is measured correct (v24.15.0 / npm 11.12.1). datasets/manifest.json, docs/data-sources.md, .gitleaks.toml and .gitleaksignore are all verified absent. So the attack is not on accuracy; it is on load and on blind spots. On over-reach: `core` has grown to roughly twenty deliverables plus nineteen acceptance criteria plus thirteen "cheap folds" for an item ROADMAP.md:165 sizes as M and deliberately does NOT mark ★ — the scope names this mismatch as risk #12 and then does nothing about it, so the tiering is a description rather than a budget. One core item's cost is materially understated (the CI-jobs guard needs real YAML parsing, not "twelve lines of regex", because ci.yml carries `name:` at workflow level and on all seven steps), and one core guard asserts the wrong direction (jobs⊆contexts misses the stale-context case ops/README.md's own warning describes). On blind spots, the sharpest is self-inflicted: tests/test_request_links.py:40-64 resolves every relative markdown link in requests/**/*.md, so a PROJECT_SCOPE that links to `src/rpg_api/` or `app/package.json` before those exist turns CI red on its own commit. The second is the "Secret scan" required job — gitleaks with fetch-depth:0 over a newly added package-lock.json, with no gitleaks config anywhere in the repo, is never mentioned once. The third is that the repo already contains thousands of lines of Node/JS under .claude/skills/**/*.mjs, which both corrects the scope's "Node is unproven ground" framing and opens an unfenced scope-creep vector the moment setup-node lands in CI.

---

## Findings

### [BLOCKER] The scope artifact itself will fail tests/test_request_links.py if it markdown-links paths that do not exist yet

- **id:** `F1` | **confidence:** high | **category:** completeness | **adversary:** `scope-completeness`
- **location:** tests/test_request_links.py:40-64 (and :24 SCANNED_TREES); the PROJECT_SCOPE.md this stage produces, under requests/feature-requests/1.1-app-shell/

**Problem.**

```text
test_request_links.py scans every .md under requests/ (excluding _done/), strips fenced code blocks, and asserts every relative markdown link resolves on disk: `if not (path.parent / target).resolve().exists(): dead.append(...)`. The scope lists 'uv run pytest tests/test_request_links.py is green' as acceptance criterion #15 but frames it as a check on the feature directory rather than as a constraint on how the scope and plan documents are themselves written. Every forward reference this item deals in — src/rpg_api/, app/, app/package.json, app/vite.config.ts, app/dist/ — does not exist at scope-commit time. A single `[src/rpg_api/](../../../src/rpg_api/)` in PROJECT_SCOPE.md turns CI red on the very PR that lands the scope, and again on the plan's PR. Only fenced blocks, `<placeholder>` targets, var/ targets and absolute URLs are exempt (lines 8-13, 48-58); FENCED_BLOCK at line 26 requires a 3+ backtick fence, so inline backticks are not stripped — but backticked text is not a markdown link either, so inline code is safe.
```

**Proposed fix.**

Add an explicit authoring constraint to the scope and carry it into the plan: every path that does not yet exist is written as inline code (`src/rpg_api/`) or inside a fenced block, never as a markdown link. Only paths verified present today (pyproject.toml, ci.yml, ops/branch-protection.json, tests/*.py, DESIGN.md) may be linked. Restate acceptance criterion #15 to say so, and run that test before /commit on this branch.

### [MAJOR] Two core-tier guard tests and one AC need YAML parsing, but no YAML library is declared — and the scope's own "regex over ci.yml job names" will match step names

- **id:** `F1` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[3] and [13], tiered_scope.core ("Twelve lines of regex over ci.yml job names"); evidence: .github/workflows/ci.yml:1,19,24,30,36,39,42,45,50,53,58 and pyproject.toml:15-21

**Problem.**

The scope promotes the CI-jobs-vs-branch-protection guard to core and adds an AC that `.github/dependabot.yml` "parses as YAML and contains an entry with package-ecosystem npm". Both need a YAML parser. The dev group at pyproject.toml:15-21 is exactly pytest, pytest-cov, ruff, mypy — no PyYAML, and mypy strict (pyproject.toml:63) would additionally require types-PyYAML. For an item whose stated headline is "dependency bookkeeping done correctly in one commit", an undeclared test dependency is a self-inflicted miss. The stated fallback is worse: ci.yml has a workflow-level `name: CI` at line 1 and seven step-level `name:` keys (lines 24, 30, 36, 39, 42, 45, 58). A regex over "every `name:`" matches ten strings, only two of which are job display names, and the guard would then demand "Set up uv" and "Gitleaks" appear in ops/branch-protection.json:4. The AC text says "every `name:` under `jobs:`" — which is structure-aware — while the core tier says "twelve lines of regex"; the two are not the same test and the scope never resolves which one it is buying.

**Proposed fix.**

Settle it in the scope: either (a) add `pyyaml` and `types-PyYAML` to the dev group as an explicit core-tier dependency bullet alongside httpx, and word both criteria as "parse ci.yml with yaml.safe_load; collect jobs.*.name", or (b) if regex, pin the shape precisely — job display names are the `name:` keys at exactly four-space indent under a two-space job key — and add a negative AC: "the guard does not report step-level names; a ci.yml step named 'Gitleaks' does not make the test fail." Same choice applies to the dependabot AC (a `package-ecosystem: "npm"` substring assertion needs no parser at all and may be the honest cheaper form).

### [MAJOR] Two acceptance criteria are demonstrations that require mutating tracked source, not commands a cold agent can run from a clean tree

- **id:** `F2` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[2] ("adding `import fastapi` to src/rpg_core/__init__.py makes it fail") and acceptance_criteria[10] ("`npm run typecheck` exits non-zero on a deliberately introduced type error")

**Problem.**

requests/feature-requests/README.md:59-61 defines testable as "a cold agent can run one command and get a pass or fail". Both of these require the checker to first edit a tracked file, observe a failure, then revert — which is a manual procedure, is not repeatable in CI, and leaves the tree dirty if interrupted. Neither is marked user-run either, so the acceptance panel will be asked to claim them. The underlying intent (prove the guard actually bites; prove strict is really on) is right — the packaging is what fails.

**Proposed fix.**

Rewrite both as pytest/npm assertions. (a) Make the layering guard a function taking a root directory, then unit-test it twice: once against `src/rpg_core/` asserting no violations, once against a tmp_path tree containing a file with `import fastapi` asserting it reports exactly that file. One `uv run pytest` proves red-and-green with no source mutation. (b) Replace the typecheck mutation with an assertion on the resolved compiler options (see F10 for the JSONC trap), and if the mutation check is still wanted, demote it to an explicitly USER-RUN or implementer-one-time criterion so the panel does not claim it.

### [MAJOR] The CI-jobs guard test sits in core with a materially understated cost — a regex over `name:` is wrong by default, and YAML parsing needs a new dev dependency

- **id:** `F2` | **confidence:** high | **category:** scope-creep | **adversary:** `scope-completeness`
- **location:** tiered_scope.core (second guard test) and above_and_beyond 'CI-jobs ⊆ branch-protection-contexts guard test' ('Twelve lines of regex over ci.yml job names'); .github/workflows/ci.yml:1,19,24,30,36,39,42,45,50,58; pyproject.toml:15-21

**Problem.**

ci.yml carries `name:` at three levels: the workflow (line 1, `name: CI`), the two jobs (lines 19, 50), and seven steps (24, 30, 36, 39, 42, 45, 58). A naive regex yields ten strings, eight of which are not job display names, so the guard would demand 'Install' and 'Gitleaks' appear in ops/branch-protection.json. Doing it correctly needs either yaml.safe_load — and there is no YAML parser in the dependency graph (the dev group at pyproject.toml:16-21 is pytest, pytest-cov, ruff, mypy; the existing tests use tomllib for TOML), so it costs pyyaml PLUS types-PyYAML to satisfy [tool.mypy] strict at pyproject.toml:61-65, and re-locks uv.lock — or an indentation-anchored regex that is brittle against a reformat. Neither is 'twelve lines'. This is a hidden cost inside core, not inside a fold.

**Proposed fix.**

Name the parsing approach and price it: either (a) add `pyyaml` and `types-PyYAML` to the dev group as an explicit core deliverable and state that uv.lock grows accordingly, or (b) specify the anchored-regex form (2-space job key followed by a 4-space `name:`, re.MULTILINE) plus a self-check asserting the parser finds exactly the two job names present today, so a reformat of ci.yml fails loudly rather than matching nothing.

### [MAJOR] The branch-protection guard asserts the wrong direction — it misses the failure mode ops/README.md actually warns about

- **id:** `F3` | **confidence:** high | **category:** acceptance | **adversary:** `scope-completeness`
- **location:** acceptance_criteria #4 ('asserts each appears in ops/branch-protection.json's required_status_checks.contexts'); ops/branch-protection.json:4; ops/README.md:20-24

**Problem.**

The proposed assertion is one-directional: jobs ⊆ contexts. The failure ops/README.md:20-24 describes in prose is the opposite — 'PRs wait forever for a check that never reports' — which happens when contexts contains a name no job produces. That is exactly what a typo in the new context string ('Web app' vs 'Web App') or a later job deletion produces: jobs ⊆ contexts still passes while every PR hangs indefinitely with no error. The one-directional test certifies the tracked half is consistent while leaving the hang case uncaught.

**Proposed fix.**

Assert set equality rather than containment: the set of job display names in .github/workflows/ci.yml must equal required_status_checks.contexts, with a failure message naming which side carries the extra entry and citing ops/README.md's rename warning. Update acceptance criterion #4 accordingly.

### [MAJOR] Goal 7 (stop the docs lying) has no acceptance criterion at all

- **id:** `F3` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: goals[6], tiered_scope.core ("Documentation…"), risks[14] — versus the 19-item acceptance_criteria list, which never mentions README.md, CLAUDE.md, or ops/README.md

**Problem.**

Documentation appears in the goals, in the core tier, and in the risks, and the scope even enumerates the files that become false (README.md:12 "No application code yet", README.md:64 project map, README.md:74-78 Setup, CLAUDE.md:66 "the web app don't exist yet", ops/README.md:32-82). Yet nothing in the 19 acceptance criteria checks any of it. "How we'll know it worked" therefore has a hole exactly where the scope says the most drift will occur, and the only named catcher (/commit's doc gate) is a judgment step, not a pass/fail command.

**Proposed fix.**

Add one testable criterion, e.g.: "`uv run pytest tests/test_repo_structure.py` includes a new assertion that README.md no longer contains the string 'No application code yet', that CLAUDE.md's project map contains both `app/` and `src/rpg_api/`, and that ops/README.md contains a Node/toolchain heading and both run-mode commands." If a structural test is judged too brittle for prose, then state explicitly in the criteria list that documentation is delegated to /commit's doc gate and is NOT panel-verifiable — but do not leave it unstated.

### [MAJOR] The 'Secret scan' required job is never mentioned, and a package-lock.json enters a gitleaks scan with no gitleaks config in the repo

- **id:** `F4` | **confidence:** medium | **category:** risk | **adversary:** `scope-completeness`
- **location:** .github/workflows/ci.yml:49-61 (secrets job, fetch-depth: 0, gitleaks-action@v2); ops/branch-protection.json:4 ('Secret scan' is a required context); verified absent: .gitleaks.toml, .gitleaksignore

**Problem.**

The scope analyses tests/test_no_leaks.py at length but never once names gitleaks, the other required check. This item adds app/package-lock.json — for a Vite/React tree, thousands of lines of high-entropy base64 sha512 `integrity` strings — to a full-history scan (fetch-depth: 0) run by a job that blocks merge, in a repo with no gitleaks configuration file of any kind to allowlist or fingerprint anything. Whether the default ruleset flags lockfile integrity hashes is unconfirmed and version-dependent, but the exposure is real, lands on a required check, and is entirely unassessed. The 'npm supply chain in a public repo' risk entry is about install scripts, not this.

**Proposed fix.**

Add an acceptance criterion that the Secret scan job passes with app/package-lock.json committed (run gitleaks locally, or mark it user-run against the PR's check run), and name the remediation in advance rather than improvising at PR time: a `.gitleaksignore` with specific fingerprints, or a scoped path allowlist in a new `.gitleaks.toml`, with a written reason mirroring the ALLOWED-entry discipline the scope already applies to tests/test_no_leaks.py. Add it to the risks list either way.

### [MAJOR] Acceptance criteria assume the full cheap-fold tier lands, while gated decision 7 invites the user to drop folds — the two are not reconciled

- **id:** `F4` | **confidence:** high | **category:** scope-creep | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[17] (USER-RUN backend-unreachable panel) and [6] (/api 404 guard) versus gated_decisions[6] ("drop or defer the pure-tidiness ones if the branch is running long") and tiered_scope.cheap_folds

**Problem.**

AC 18 tests the "legible backend-unreachable state", which is a cheap fold. AC 7 exists, by the scope's own words, to keep "the SPA fallback, if folded in, from swallowing API 404s" — also a cheap fold, and its text hedges with "if folded in". So the acceptance list is written against a tier the same document tells the user they may trim. If the user drops those folds, two criteria become untestable or meaningless, and the scope gives the implementer no rule for what happens then. This is the one place where the tiering machinery leaks into the handoff interface.

**Proposed fix.**

Tag every acceptance criterion with the tier it depends on (core / fold-X), or — simpler and probably right — promote the two folds that criteria depend on (backend-unreachable state, SPA history fallback) into core and delete the "if folded in" hedge from AC 7. Then the acceptance list describes exactly one deliverable regardless of how the user disposes the remaining folds.

### [MAJOR] The repo already ships Node/JS that CI never checks — the 'Node is new ground' framing is incomplete and leaves a scope-creep vector unfenced

- **id:** `F5` | **confidence:** high | **category:** completeness | **adversary:** `scope-completeness`
- **location:** .claude/skills/scope-feature/scope_panel.js, .claude/skills/create-implementation-plan/plan_panel.js, .claude/skills/implement-plan/acceptance_panel.js, and six `*_guard.mjs` / `*_repro.mjs` files invoked as `node .claude/skills/.../guard.mjs` (e.g. .claude/skills/scope-feature/SKILL.md:203, .claude/skills/implement-plan/SKILL.md:271-273)

**Problem.**

Both the problem_restatement and the fit_verdict rest on 'a JavaScript build has none of that and CI does not know it exists.' That is half true: thousands of lines of JS/MJS already live under .claude/skills/, several skills document `node <guard>.mjs` as a check to run when a panel file changes, and none of it is linted, typechecked, or run in CI. Two consequences the scope never addresses: once setup-node exists in a CI job, wiring the skills' guard scripts into it becomes an obvious unbudgeted temptation; and a linter config placed at the repo root rather than inside app/ will start reporting on .claude/skills/**/*.js and either fail the build or force an ignore list nobody scoped.

**Proposed fix.**

Add a non-goal — 'the existing .claude/skills JS is out of scope for the new lint/typecheck job; the skills' node guards do not join CI in this item' — and a core constraint that the TypeScript linter config and tsconfig live inside app/ with file scope limited to app/, never a repo-root config. Optionally record skills-guards-in-CI as a candidate future request rather than leaving it as an aspiration.

### [MAJOR] The scope diverges from a request Constraint labelled non-negotiable without flagging it as a divergence

- **id:** `F5` | **confidence:** high | **category:** framing | **adversary:** `fit-ac`
- **location:** requests/feature-requests/1.1-app-shell/FEATURE_REQUEST.md:162-163 ("Constraints / Non-negotiables — Machine-specific values resolve from the environment, with keys listed in `.env.example`") versus merged scope gated_decisions[4] ("add no env keys") and above_and_beyond "Environment-resolved settings … My recommendation is no env keys"

**Problem.**

The request puts env-resolved configuration under a heading it calls Non-negotiables, and the scope recommends against it. The reasoning offered (127.0.0.1:8000 is a documented default, not a machine identifier; `uvicorn --port` already handles a collision; a second key is a second place for the proxy target to drift) is genuinely good — but it is presented as a neutral option among five, not as "we are proposing to not honor a constraint the request marked non-negotiable, here is why." The pipeline's whole point is that divergence is stated rather than quiet. Verified context: .env.example currently carries exactly three keys, all genuinely machine-specific (NBA2K26_INSTALL, NBA_ANALYSIS_PATH, POKEMON_LAB_PATH), which supports the scope's reading.

**Proposed fix.**

Reword gated_decisions[4] to open with the divergence: "FEATURE_REQUEST.md:162 lists env-resolved config under Non-negotiables. This scope proposes it does not apply here, because the constraint targets machine-specific values and a documented loopback default is not one — the three keys currently in .env.example are all real machine identifiers. If you disagree, the constraint stands and RPG_API_PORT / RPG_SPA_DIST go in .env.example." Same treatment, one sentence, no change to the recommendation.

### [MAJOR] Goal 7 (docs stop lying) has no acceptance criterion — all documentation work is delegated to /commit's judgment gate

- **id:** `F6` | **confidence:** high | **category:** acceptance | **adversary:** `scope-completeness`
- **location:** goals[6] and tiered_scope.core ('Documentation: ops/README.md ... README.md ... CLAUDE.md'); nineteen acceptance_criteria, none touching a document; .claude/skills/update-docs/SKILL.md:24-31

**Problem.**

requests/feature-requests/README.md:57-73 defines testable as 'a cold agent can run one command and get a pass or fail.' Every doc deliverable in core fails that bar — not one of the nineteen criteria asserts anything about README.md, CLAUDE.md or ops/README.md. The scope leans on /commit's doc gate, but update-docs/SKILL.md:24-31 is explicitly the judgment half, a read rather than a pass/fail. Doc drift here is the failure mode the repo treats as a correctness problem ('an agent confidently building in the wrong place'), and it is the most likely thing to be quietly skipped on a long branch.

**Proposed fix.**

Add mechanical criteria — cheap, because the strings are literal: a test or scripted grep asserting README.md no longer contains 'No application code yet' and its project map contains `app/` and `src/rpg_api/`; that CLAUDE.md's map contains the same two and no longer says the web app doesn't exist; that ops/README.md contains both run-mode commands. This is the idiom tests/test_repo_structure.py already uses for 'the repo and its documents agree'.

### [MAJOR] The PROJECT_SCOPE document itself will turn tests/test_request_links.py red if it markdown-links the paths this item creates

- **id:** `F6` | **confidence:** high | **category:** risk | **adversary:** `fit-ac`
- **location:** tests/test_request_links.py:24 (SCANNED_TREES includes REPO_ROOT/requests), :36 (rglob every *.md not under _done), :41 (fenced blocks stripped), :61 (asserts `(path.parent / target).resolve().exists()`); merged scope acceptance_criteria[14] cites this test

**Problem.**

```text
The scope names test_request_links.py as an acceptance gate but does not notice that the artifact being written is itself in scope for it. PROJECT_SCOPE.md lands via /commit at stage 2, before any code — so any markdown link of the form `[src/rpg_api/](../../../src/rpg_api/)` or `[app/](../../../app/)` points at a path that will not exist for another two stages, and the existing structural test goes red on the scope commit. Only fenced code blocks and `<placeholder>` targets are exempt (test_request_links.py:9-12, 26, 50-52). This is a foot-gun the scope hands to itself and then to the IMPLEMENTATION_PLAN, which will cite the same forward paths.
```

**Proposed fix.**

Add a one-line authoring rule to the scope (and carry it into the plan): forward-referenced paths that do not exist yet are written as inline code or inside a fenced block, never as a markdown link. Existing paths (pyproject.toml, ci.yml, ops/branch-protection.json) may be linked normally.

### [MAJOR] Two acceptance criteria are manual mutation tests requiring tracked source to be dirtied, and cannot be run as one command

- **id:** `F7` | **confidence:** high | **category:** acceptance | **adversary:** `scope-completeness`
- **location:** acceptance_criteria #3 ('adding `import fastapi` to src/rpg_core/__init__.py makes it fail; removing it makes it pass') and #11 ('`npm run typecheck` exits non-zero on a deliberately introduced type error'); CLAUDE.md convention 'Subagents get read-only git'

**Problem.**

Neither is runnable as a single command, neither is marked user-run, and both instruct the implementer or acceptance panel to edit tracked files and revert them — in a repo where agents are told git is read-only and must not use restore/checkout/stash to undo a mess. If the revert is imperfect, `import fastapi` ships inside the domain core in the same PR whose entire point is that it must not. The intent is right (a guard that cannot fail proves nothing); the mechanism is wrong.

**Proposed fix.**

Restructure both as self-testing fixtures. For the layering guard: implement it as a pure function taking a directory, then unit-test that function twice against tmp_path — one fake module containing `import fastapi` (expects failure), one clean (expects pass) — with the real assertion pointed at src/rpg_core/. For tsconfig strictness: commit a deliberately ill-typed fixture excluded from `npm run build` and checked by a dedicated `npm run typecheck:negative` asserted to exit non-zero, or drop criterion #11 and mark it user-run. Either way no tracked source is mutated.

### [MAJOR] Branch-protection re-apply is sequenced after merge, guaranteeing that this very PR can merge with a red web job

- **id:** `F8` | **confidence:** medium | **category:** risk | **adversary:** `scope-completeness`
- **location:** acceptance_criteria #19 ('USER-RUN — required-check activation. After merge, `gh api ...`'); risks[0]; ops/README.md:8-30

**Problem.**

The scope correctly identifies silent-green merges as the headline risk and then adopts the sequencing that maximally realises it on its first occurrence: protection is re-applied only after this PR merges, so the PR introducing the job is exactly the PR that can land with the frontend broken. GitHub accepts required-status-check contexts for checks that have never reported, so the user can apply the updated ops/branch-protection.json while the PR is open, making the new context blocking on its own PR. The scope does not consider this ordering. Medium confidence because I have not exercised the API, and the scope's own unconfirmed flag about whether the current JSON still applies cleanly (and whether ops/README.md's `jordan-koch/nba2k-rpg` owner still matches the remote) stands.

**Proposed fix.**

Rewrite the user-run criterion as an ordered gate: (1) push the branch and let the third job report once so the context name is confirmed verbatim; (2) user runs `gh api -X PUT ... --input ops/branch-protection.json`; (3) confirm the new check shows as Required on the open PR; (4) then merge. Put the steps in the PR description, and verify beforehand that the owner/repo in ops/README.md matches `git remote -v`.

### [MAJOR] Core has grown to roughly twenty deliverables for an item the roadmap sizes M and deliberately did not mark ★ — the tiering describes the load instead of bounding it

- **id:** `F9` | **confidence:** high | **category:** scope-creep | **adversary:** `scope-completeness`
- **location:** tiered_scope.core (14 bullets, several compound), 19 acceptance_criteria, 13 cheap_folds, 9 gated, 26 above_and_beyond entries; ROADMAP.md:165 (1.1, size M, no ★); ROADMAP.md:120-122 ('M a day or so'; 'Unmarked items should skip straight to a plan or straight to work')

**Problem.**

The scope raises this as risks[11] and gated_decisions[6] and then leaves the tiers untouched, so the mitigation is a warning label rather than a decision. Core alone requires: a new Python package, a route, four pyproject edits, a re-lock, a CI job, a --cov change, a branch-protection edit, a full Vite/React/TS/linter SPA with a committed lockfile, a dev proxy, static serving with an injectable dist and a 503 branch, two guard tests (one of which needs a YAML parser per F2), a dependabot entry, and edits to five documents. Thirteen folds on top is more surface area than the feature. The pipeline's own guidance (requests/feature-requests/README.md:23-26) is that unmarked items may skip the full panel; the panel ran anyway, which is fine, but its output must not silently upgrade an M into an L.

**Proposed fix.**

Make the tiering a budget. Declare a must-land subset explicitly (package + health route + dependency/lock bookkeeping + SPA + proxy + serving with both branches + CI job + contexts edit + the layering guard + docs) and move the rest — SPA fallback, typed fetch wrapper, .editorconfig, favicon/title, gitignore guard, test_no_leaks docstring fix — into a named 'only if the branch is still short' list. State plainly that dropping any of them is not a failure of the item.

### [MINOR] The contexts guard is sold as closing the headline risk, but it cannot — the honest claim is drift detection

- **id:** `F10` | **confidence:** high | **category:** framing | **adversary:** `scope-completeness`
- **location:** above_and_beyond 'CI-jobs ⊆ branch-protection-contexts guard test' ('makes it red instead'); convergence_map[0]

**Problem.**

The failure named — 'a PR merges green while the frontend job was failing' — is caused by GitHub's applied protection, not by the tracked JSON. The guard asserts that two files in the repo agree; it stays green while GitHub still enforces only two contexts. The scope concedes this in one clause ('It still cannot verify what GitHub has actually applied'), but the surrounding framing, and the promotion from enhancement to core, rest on the stronger claim. The danger is a reader concluding the risk is handled.

**Proposed fix.**

Restate the guard's value as 'detects tracked-config drift so the re-apply step has something correct to apply', keep it, and put the real mitigation weight on F8's sequencing. Have the test's failure message state that passing does not mean protection is applied, and point at ops/README.md.

### [MINOR] AC 11 assumes a single app/tsconfig.json holding `strict`; the Vite react-ts template emits project references plus JSONC files

- **id:** `F10` | **confidence:** medium | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[10] ("proving tsconfig.json has strict actually engaged") and cheap_folds ("TypeScript strictness beyond `strict: true` — noUncheckedIndexedAccess, …")

**Problem.**

Inferred, not verified in this repo (nothing under app/ exists yet — no app directory on disk): `npm create vite@latest -- --template react-ts` scaffolds tsconfig.json containing only `references` to tsconfig.app.json and tsconfig.node.json, all three carrying `//` comments. Two consequences the criterion does not survive: (a) `strict` is not in tsconfig.json at all, so "tsconfig.json has strict engaged" is checking the wrong file; (b) any pytest assertion that does `json.loads(app/tsconfig.json)` raises on the comments. The extended-strictness cheap fold inherits the same ambiguity — which of the three files gets the flags is unspecified.

**Proposed fix.**

Word the criterion against behavior rather than a filename: "the configuration `npm run typecheck` actually resolves has strict plus noUncheckedIndexedAccess / noUnusedLocals / noUnusedParameters / noFallthroughCasesInSwitch enabled for app/src", and if it is asserted from pytest, assert against `tsc --showConfig` output (real JSON) rather than parsing a JSONC file. Note in the scope that the plan must decide which tsconfig in the reference chain carries the flags.

### [MINOR] AC 8's "zero new `# type: ignore` and zero new per-module overrides" is a diff review, not a runnable check

- **id:** `F11` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[7]

**Problem.**

The intent is exactly right — the scope correctly identifies that a green mypy achieved by loosening strict is a failure — but as written, a cold agent verifying this has to eyeball a diff for two absences. "New" is also undefined without a baseline. It is one of the few criteria on the list that a determined implementer could satisfy while violating.

**Proposed fix.**

Convert to assertions with no baseline dependency: a pytest test asserting no file under `src/` contains the string `# type: ignore`, and that `tomllib.load(pyproject.toml)` has no `tool.mypy.overrides` key and `tool.mypy.strict is True`. tests/test_repo_structure.py:15 already imports tomllib, so this is the file's existing idiom.

### [MINOR] The doc-drift inventory misses three concrete sites

- **id:** `F11` | **confidence:** high | **category:** completeness | **adversary:** `scope-completeness`
- **location:** risks[14] lists README.md's status blockquote/map/setup and CLAUDE.md's map + 'don't exist yet' sentence. Missing: CLAUDE.md:21, ROADMAP.md:157-158, requests/feature-requests/README.md:106

**Problem.**

Verified additional statements that become false: CLAUDE.md:21 — '**no application code yet.** The first work item is Phase 1's `app-shell` (1.1)' — sits in the Status section, not the project map, and is absent from the scope's list. ROADMAP.md:157-158 — the Phase 1 header prose '**IN-PROGRESS** — 1.1 `app-shell` is at intake. No application code has landed yet.' — is prose that /commit's row-status logic will not necessarily touch. requests/feature-requests/README.md:106 — the Index row still reads `intake` and must move to `scoped` now and `implemented` later; the scope mentions it only in grounding_pointers, not as a deliverable.

**Proposed fix.**

Extend the documentation deliverable and the doc-drift risk to name all three by file:line, and fold them into F6's mechanical criteria where the string is literal (CLAUDE.md must not contain 'no application code yet'; ROADMAP.md's Phase 1 header must not contain 'is at intake').

### [MINOR] Naming the health field `version` pre-empts a word ADR 0004 reserves for something else

- **id:** `F12` | **confidence:** medium | **category:** fit | **adversary:** `scope-completeness`
- **location:** tiered_scope.core ('GET /api/health returning {"status": "ok", "version": rpg_core.__version__}'); docs/decisions/0004-rulesets-as-versioned-config.md; ROADMAP.md:168 (item 1.4 `ruleset-loader`, 'every event pins the version live at the time')

**Problem.**

From item 1.4 onward, 'version' in this project overwhelmingly means the pinned, immutable ruleset version — the thing ADR 0004 makes load-bearing and that every event carries. Establishing a top-level `version` key on the shell's only endpoint, four items before that lands, invites exactly the ambiguity this repo spends effort avoiding, and the scope's own rule ('the payload gains a field only when the thing it reports exists') does not disambiguate the name. This is the one place where an otherwise contract-free item binds downstream vocabulary.

**Proposed fix.**

Name it `app_version` — still sourced from rpg_core.__version__, still transitively pinned by tests/test_repo_structure.py:46-54 — and record in the API package docstring that `ruleset_version` is a distinct concept arriving with 1.4. Costs nothing now; renaming a documented endpoint field later costs more than it looks.

### [MINOR] The mypy-strict risk discusses FastAPI decorators but omits that tests/ is also under strict — where the conftest fixture actually lands

- **id:** `F12` | **confidence:** high | **category:** completeness | **adversary:** `fit-ac`
- **location:** pyproject.toml:65 (`files = ["src", "tests"]`); merged scope risks[4] and cheap_folds ("reusable TestClient fixture in tests/conftest.py")

**Problem.**

The risk entry frames mypy friction entirely as "strict over FastAPI" in the new API package. But mypy's file list already covers tests/, and the more likely first friction is the new test code: a generator fixture needs an explicit `Iterator[TestClient]` return annotation under strict, `@pytest.fixture` interacts with disallow_untyped_decorators, and parameterized fixtures need annotated params. That matters because the conftest fixture is a cheap fold the scope actively recommends, so it is near-certain to be written.

**Proposed fix.**

Extend risks[4] one sentence: "[tool.mypy] files includes tests, so the new TestClient fixture and the guard tests are strict-checked too — annotate fixtures fully rather than reaching for an override." Fold the same into AC 8's wording so the criterion covers tests/ explicitly.

### [MINOR] The gitignore guard cheap fold cannot detect removal of the rule it claims to protect — a blanket `dist/` already covers app/dist/

- **id:** `F13` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** .gitignore:62 (`dist/`) versus .gitignore:68 (`app/dist/`); merged scope cheap_folds ("Guard test that app/dist/ and node_modules/ are gitignored") and the above_and_beyond entry of the same name

**Problem.**

`.gitignore:62` is a blanket `dist/` rule from the Python block that matches a directory named dist at any depth — so `git check-ignore --no-index app/dist/index.html` returns ignored even if line 68 is deleted entirely. The guard therefore proves the outcome, not the rule, and the scope describes it as protecting the Node block. Its one genuinely useful property (catching a later `!app/**` carve-out that would un-ignore everything) is real but is a narrower claim than the rationale makes.

**Proposed fix.**

Either restate the rationale honestly — "asserts the outcome, and exists specifically to catch a future `!app/**` negation, not to pin the .gitignore:66-68 lines" — or strengthen it to cover paths the blanket rules do not reach, e.g. also assert `app/node_modules/x` and `.vite/x` are ignored, and consider asserting the literal Node section survives in .gitignore.

### [MINOR] The Vitest gate silently determines whether a fourth CI job — and a fourth required context — is needed

- **id:** `F13` | **confidence:** high | **category:** acceptance | **adversary:** `scope-completeness`
- **location:** gated_decisions[0]; tiered_scope.core (CI job: 'npm ci / typecheck / lint / build'); ops/branch-protection.json:4

**Problem.**

The gated Vitest decision is presented purely as a testing question, but it has a structural consequence the scope never states: if tests join the existing web job as a fifth step, contexts grows by one; if they become their own job — so a red test is legible on its own, the same argument the scope uses to justify a separate web job at all — contexts grows by two and the user's single `gh api -X PUT` must carry both. Deciding this after the workflow is written means either an inconsistent rationale or a second protection re-apply.

**Proposed fix.**

State the answer inside the gate: if Vitest is taken it is a step in the existing web job (`npm run test -- --run`), not a fourth job — one context, one re-apply. If the user wants separate legibility, that is a second context and must be in the same JSON edit. Add it as a sub-bullet of gated_decisions[0] so the choice is priced.

### [MINOR] The proposed gitignore guard passes vacuously — the blanket `dist/` rule already shadows `app/dist/`

- **id:** `F14` | **confidence:** high | **category:** acceptance | **adversary:** `scope-completeness`
- **location:** cheap_folds ('Guard test that app/dist/ and node_modules/ are gitignored'); .gitignore:62 (`dist/`, blanket, matches at any depth) vs .gitignore:68 (`app/dist/`)

**Problem.**

.gitignore:62 already ignores any directory named dist at any depth, so `git check-ignore --no-index app/dist/index.html` reports ignored whether or not line 68 exists. The guard's stated purpose — asserting nobody later adds an `!app/**` carve-out — is partly served (a negation would flip it), but its implied purpose of protecting the specific app/dist rule is not: deleting line 68 leaves the test green. Related citation nit: the scope repeatedly cites '.gitignore:65-68' for the three rules, but line 65 is the section header comment and the rules are 66-68.

**Proposed fix.**

Either keep the check-ignore assertion and drop the claim that it protects the app/dist line specifically, or add a second honest assertion that .gitignore's text contains the `app/dist/` and `node_modules/` rules verbatim. Correct the citation to .gitignore:66-68.

### [MINOR] The Vite proxy target — elevated to a core decision and a named risk — has no objective check, only a user-run one

- **id:** `F14` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: tiered_scope.core ("proxy mapping /api to the backend on the IPv4 literal 127.0.0.1 (not `localhost`)"), risks[7], versus acceptance_criteria[15] which is USER-RUN

**Problem.**

The scope makes a specific, non-obvious, well-argued call (IPv4 literal, because Windows Node can resolve localhost to ::1 while uvicorn binds 127.0.0.1) and then leaves it enforced by nothing. The failure mode it prevents presents as ECONNREFUSED that looks identical to the backend being down — the exact confusion the item exists to remove. A later agent editing vite.config.ts to `localhost` reintroduces it silently, and the only detector is the user noticing.

**Proposed fix.**

Add a cheap objective criterion: "a structural test asserts app/vite.config.ts's proxy target contains `127.0.0.1` and does not contain `localhost`." Roughly four lines, in the same read-a-tracked-file idiom tests/test_repo_structure.py already uses, and it converts a paragraph of reasoning into something that fails a build.

### [MINOR] ADR 0002 is cited as authority for excluding pydantic from the deny-list; the ADR never mentions pydantic

- **id:** `F15` | **confidence:** high | **category:** framing | **adversary:** `fit-ac`
- **location:** merged scope: grounding_pointers ("read before writing the layering guard's deny-list: it requires the DTO be constructible in tests 'with no HTTP and no UI', which is why pydantic is deliberately absent") versus docs/decisions/0002-manual-ingestion-dto-boundary.md:27-29

**Problem.**

ADR 0002 line 29 says the DTO boundary makes "the entire economy testable with no HTTP and no UI". That supports banning fastapi/starlette/uvicorn from rpg_core. It says nothing about whether a validation library counts as a web framework, and it names no library at all. Presenting the pydantic call as flowing from an accepted ADR dresses a scope-level judgment (a defensible one — that question belongs to item 1.2 or 1.8) in borrowed authority. In a repo whose stated worst outcome is re-litigating settled decisions, mis-attributing a decision to an ADR is a small but real cost.

**Proposed fix.**

Reword: "pydantic is excluded from the deny-list as this scope's own call, not the ADR's — ADR 0002 is silent on validation libraries. Whether the domain core may depend on pydantic is item 1.2's decision when the event schema arrives; the guard here bans only web frameworks so it does not pre-empt that."

### [MINOR] The watchfiles-over-uvicorn[standard] fold rests on a uvloop-on-Windows premise that is probably already false

- **id:** `F15` | **confidence:** medium | **category:** risk | **adversary:** `scope-completeness`
- **location:** cheap_folds ('Take backend hot reload via `watchfiles` ... [standard] bundles uvloop, which has no Windows wheel'); above_and_beyond 'watchfiles in the dev group instead of uvicorn[standard]'

**Problem.**

uvicorn[standard] declares uvloop behind an environment marker excluding win32, so on Windows the extra resolves without uvloop rather than failing — the stated hazard largely does not occur. uv.lock is a cross-platform lock and would carry uvloop for the Linux resolution, which installs fine on ubuntu-latest. The conclusion (plain uvicorn at runtime, watchfiles in the dev group) may still be right for dependency hygiene — `--reload` genuinely requires watchfiles — but the reason given is the wrong one, and the scope labels it 'inferred, not verified' while still presenting it as a fold rather than as something to check.

**Proposed fix.**

Replace the rationale with the honest one — keep the runtime dependency set minimal and put the reload watcher in the dev group where it belongs — and add a one-line verification to the plan: run `uv add uvicorn`, `uv add --dev watchfiles`, then confirm `uv sync --locked` and `uvicorn --reload` both work on this Windows machine before committing the lock.

### [MINOR] AC 10's claim that a green local run predicts a green CI run contradicts the scope's own Windows/CI risk entries

- **id:** `F16` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[9] ("so a green local run predicts a green CI run") versus risks[6] (PowerShell `&&`), risks[7] (IPv6 localhost), risks[8] (npm major skew, lockfileVersion)

**Problem.**

Three risk entries in the same document exist precisely because local Windows and ubuntu-latest CI diverge — including one (npm major skew producing a lockfile that installs locally and fails `npm ci` in CI) that is exactly a green-local / red-CI scenario. The criterion's trailing claim is therefore false in the dimension the scope itself is most worried about, and a reader could use it to skip a CI check.

**Proposed fix.**

Trim the claim to what is true: "these are the same four steps the new CI job runs" — and drop "so a green local run predicts a green CI run", or qualify it with "modulo the platform and npm-major differences noted in the risks".

### [MINOR] The SPA history fallback is folded without acknowledging that the request explicitly deferred routing

- **id:** `F16` | **confidence:** medium | **category:** scope-creep | **adversary:** `scope-completeness`
- **location:** cheap_folds ('SPA history fallback'); FEATURE_REQUEST.md:111-113 ('Routing and app chrome ... Deferred deliberately: structuring an app before it has surfaces pre-decides the structure blind')

**Problem.**

The scope defends the fallback against 'the minimalist' but never against the intake document, which put routing in 'Not now / later' with a reason that applies to the server half as much as the client half: a catch-all is the server-side commitment that client routing will be path-based rather than hash-based. It is a small commitment and probably the right one, but folding it while the request's own deferral goes unquoted is the quiet divergence this stage exists to surface.

**Proposed fix.**

Keep the fold if the /api-404 guard criterion stays, but say plainly that it partially overrides the request's routing deferral and why (one route, and it makes 1.10's router additive rather than breaking). Alternatively demote it to the 'only if the branch is still short' list from F9 — nothing else in the item needs it.

### [MINOR] ROADMAP.md:156 is a sixth doc-drift site the risk entry's list of five omits — and it is prose that /commit's table machinery does not maintain

- **id:** `F17` | **confidence:** high | **category:** completeness | **adversary:** `fit-ac`
- **location:** ROADMAP.md:156-157 ("**Status:** **IN-PROGRESS** — 1.1 `app-shell` is at intake. No application code has landed yet."); merged scope risks[14] lists README.md ×3 and CLAUDE.md ×2

**Problem.**

The Phase 1 header carries a prose status paragraph that will be false the moment this item lands, and it is distinct from the table row the scope correctly assigns to /commit. ROADMAP.md:127-130 scopes the /commit gate to "these rows" — the table — so the phase-header prose is not covered by the mechanism the scope relies on. Also note requests/feature-requests/README.md:106's Index row must move from `intake` to `scoped` at this stage and to `implemented` later, which the scope mentions in grounding_pointers but not in the doc-drift risk.

**Proposed fix.**

Add ROADMAP.md:156-157 to the doc-drift list explicitly, and note that the phase-header prose is outside /commit's table automation so it needs a human edit. Add the requests/feature-requests/README.md Index row to the same list.

### [MINOR] Goal 4 ("two honest ways to run it") is delivered by one automated criterion and two user-run ones — dev-mode correctness has zero objective coverage

- **id:** `F7` | **confidence:** high | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: goals[3], acceptance_criteria[4][5] (built mode, TestClient + tmp_path) versus acceptance_criteria[15][16] (both USER-RUN) and gated_decisions[5] (real-server smoke recommended out)

**Problem.**

The built-SPA branch gets real automated coverage against tmp_path. The development branch — Vite proxy, the no-CORS-middleware decision that follows from it, hot reload — is verified only by a human opening a browser and reading a network tab, and the one enhancement that would close the gap (real-server CI smoke) is recommended out. The scope names this gap honestly inside gated_decisions[5], but the goals section states the two modes as equally delivered. A reader skimming goals gets a rosier picture than the criteria support.

**Proposed fix.**

Say it plainly in the goal or in a one-line note under the criteria: "dev-mode wiring is user-verified only; no automated check exercises the proxy." Then add the cheap objective partial check described in F14 so at least the configuration (as opposed to the runtime behavior) is machine-asserted.

### [MINOR] The other required check — gitleaks / "Secret scan" — will scan package-lock.json for the first time, and the repo has no gitleaks config to fall back on

- **id:** `F8` | **confidence:** medium | **category:** risk | **adversary:** `fit-ac`
- **location:** merged scope: risks[3] covers tests/test_no_leaks.py only; .github/workflows/ci.yml:49-61 (secrets job, gitleaks-action@v2); ops/branch-protection.json:4 lists "Secret scan" as required; verified: .github contains only workflows/ci.yml and dependabot.yml — no .gitleaks.toml anywhere in the repo

**Problem.**

The scope does a careful job on tests/test_no_leaks.py's new blast radius and then stops, but that is only one of two blocking content gates. A Vite/React `package-lock.json` is thousands of lines of base64 `integrity` hashes and registry URLs — a well-known false-positive surface for entropy-based secret scanners. If gitleaks trips, the required check goes red on a repo that has no configuration file to narrow it, and the implementer discovers this at PR time with no sanctioned remedy written down. Labelled inferred, not measured: gitleaks' default ruleset usually tolerates npm integrity hashes, but nobody has run it against a lockfile in this repo.

**Proposed fix.**

Add gitleaks to the risk list beside test_no_leaks.py, add an acceptance criterion "the Secret scan job is green on the branch with app/package-lock.json tracked", and pre-state the remedy shape so it is not improvised: a narrow `.gitleaks.toml` allowlist scoped to `app/package-lock.json` with a written reason, matching the ALLOWED-entry discipline the scope already prescribes for tests/test_no_leaks.py:32-35.

### [MINOR] The layering guard is specified as a scan for import names, which will false-positive on the very docstrings that state the rule

- **id:** `F9` | **confidence:** medium | **category:** acceptance | **adversary:** `fit-ac`
- **location:** merged scope: acceptance_criteria[2] ("scans every .py under src/rpg_core/ and asserts none imports `fastapi`, `starlette`, `uvicorn`, or the API package"); src/rpg_core/__init__.py:1-12 is presently 12 lines of docstring and one assignment

**Problem.**

The scope never says how the scan works. The whole content of src/rpg_core today is a docstring whose job is to declare the constraint ("Deliberately I/O-free and web-free… The API and the web app depend on it; it depends on neither"). The obvious next edit by a well-meaning agent — spelling the rule out as "never import fastapi here" — makes a substring-based guard fail on the file it is protecting, and the natural fix at that moment is to weaken the guard. Since this guard is the single permanent artifact the scope says this content-free item leaves behind, its implementation method is a scope-level decision, not an implementation detail.

**Proposed fix.**

Specify AST-based detection in the criterion: `ast.parse` each file and walk `ast.Import` / `ast.ImportFrom`, comparing the top-level module name against the deny-set. Add a sibling criterion: "a module whose docstring mentions fastapi, but which imports nothing, does not trip the guard" — testable against the tmp_path fixture F2 already introduces.

### [NIT] npm-over-pnpm is decided inside core without being named as a decision

- **id:** `F17` | **confidence:** high | **category:** framing | **adversary:** `scope-completeness`
- **location:** tiered_scope.core ('npm as the package manager with a committed package-lock.json'); FEATURE_REQUEST.md:206-207 (Open Question 9); .gitattributes:41; .github/dependabot.yml:30

**Problem.**

The request asks npm vs pnpm as an open question. The scope answers npm — correctly, since .gitattributes:41 already declares `package-lock.json linguist-generated=true -diff` and dependabot.yml:30 reserves an npm ecosystem entry — but presents it as a given rather than as an OQ9 resolution with that evidence attached. A later reader cannot tell it was decided rather than assumed.

**Proposed fix.**

Add one line to the fit rationale or the core bullet: OQ9 resolved to npm on the strength of .gitattributes:41 and .github/dependabot.yml:30, both of which pre-reserve npm by name; the Node version half of OQ9 is resolved as measured (v24.15.0 / npm 11.12.1).

### [NIT] One flagged UNCONFIRMED item is now verified and can be struck: the remote owner matches ops/README.md

- **id:** `F18` | **confidence:** high | **category:** fit | **adversary:** `fit-ac`
- **location:** merged scope: risks[0] ("UNCONFIRMED … whether the owner/repo in ops/README.md's example still matches the actual remote"); ops/README.md:12 and :29 versus `git remote -v`

**Problem.**

Not a defect — a resolvable open item left open. `git remote -v` returns https://github.com/jordan-koch/nba2k-rpg.git, which matches the `jordan-koch/nba2k-rpg` slug hardcoded in ops/README.md:12 and :29. Carrying it as UNCONFIRMED into the plan means someone re-checks it. The sibling half of that risk — whether GitHub accepts the updated protection JSON unchanged — genuinely is unconfirmed and should stay.

**Proposed fix.**

Downgrade to: "VERIFIED 2026-08-13: the remote is jordan-koch/nba2k-rpg, matching ops/README.md:12. Still UNCONFIRMED: whether the protection API accepts the amended contexts array unchanged, since it has not been re-applied since Phase 0." Then the user-run criterion can quote the exact command from ops/README.md:12-13 verbatim rather than an `<owner>` placeholder.

### [NIT] Open Question 8's second half (a guard that app/ carries a lockfile) is silently dropped rather than declined

- **id:** `F18` | **confidence:** high | **category:** completeness | **adversary:** `scope-completeness`
- **location:** FEATURE_REQUEST.md:203-204 (OQ8: 'or that `app/` exists with a lockfile'); grounding_pointers claims the scope settles OQs 1, 2, 4, 6, 8

**Problem.**

The scope says it settles OQ8 and delivers two guards, neither of which is the lockfile-presence guard OQ8 names. The right answer is probably 'declined — `npm ci` fails loudly on a missing or mismatched lockfile, so a structural guard is redundant', but that reasoning appears nowhere, so it reads as an oversight rather than a call and invites the plan stage to reintroduce it as an obvious gap.

**Proposed fix.**

Add the one-sentence decline with its reason to the scope.

### [NIT] `.gitignore:65` is cited repeatedly as a rule; it is the section-header comment

- **id:** `F19` | **confidence:** high | **category:** fit | **adversary:** `fit-ac`
- **location:** merged scope: summary, fit_verdict.rationale, non_goals, grounding_pointers all cite ".gitignore:65-68"; .gitignore:65 is `# ─── Node / web app ───`, rules are at 66 (node_modules/), 67 (.vite/), 68 (app/dist/)

**Problem.**

Cosmetic citation drift, repeated four times. Everything else in the document's line citations checks out exactly — pyproject.toml:9/11-13/30-31/49/61-65/73, ci.yml:19/24-28/34/47/50/9-12, ops/branch-protection.json:4, .gitattributes:41, tests/test_repo_structure.py:24-34/46-54/83-92/113-133, tests/test_no_leaks.py:26-29/32-35/37/38-55, .github/dependabot.yml:30, DESIGN.md §3 at line 99 with the note at 106 — so this is the one blemish on an otherwise verified citation set and is worth fixing precisely because the rest sets a high bar.

**Proposed fix.**

Cite `.gitignore:66-68` for the three rules, or `.gitignore:65-68` only when referring to the block including its header, and say so.

### [NIT] above_and_beyond duplicates tiered_scope almost entirely, inflating the handoff for an M-sized item

- **id:** `F19` | **confidence:** high | **category:** framing | **adversary:** `scope-completeness`
- **location:** above_and_beyond (26 entries) vs tiered_scope (14 core + 13 cheap_folds + 9 gated)

**Problem.**

Most above_and_beyond entries restate a tiered_scope bullet with a longer rationale — the layering guard, the contexts guard, the conftest fixture, the client wrapper, tsconfig strictness, the Node pin, npm caching, the gitignore guard, the docstring fix, the SPA fallback and watchfiles all appear twice. A planner reading both must diff them to be sure nothing differs, and the sheer length pushes against the M sizing the scope elsewhere defends.

**Proposed fix.**

Keep above_and_beyond for entries whose tier is 'gated' or 'drop' (where the rationale is the deliverable) and for the two promotions into core; for anything already in cheap_folds, cite the fold rather than restating it.

### [NIT] Non-goals are honest overall, but the routing/fallback pair and the "no visual design" line deserve one clarifying sentence each

- **id:** `F20` | **confidence:** medium | **category:** fit | **adversary:** `fit-ac`
- **location:** merged scope: non_goals ("Client-side routing and app chrome", "Visual design") versus cheap_folds ("SPA history fallback", "legible backend-unreachable state", "real page title and favicon")

**Problem.**

I checked the non-goal list for buried hard parts and found none — the genuinely hard deferrals (type contract, persistence, domain logic, auth, packaging) are each named with a reason and a forward pointer, and the two most tempting hiding places (no CORS because the proxy makes dev same-origin; no path-filtered CI because named contexts would hang) are both argued rather than asserted. The only softness is presentational: the serving-side half of routing (history fallback) is folded in while routing is a non-goal, and three folds (unreachable panel, page title, favicon) are UI work while visual design is a non-goal. Both are reconciled somewhere in the document, but not at the non-goal itself, where a skimming reader forms their model.

**Proposed fix.**

Append the reconciliation inline: "Client-side routing … — note the server-side history fallback IS in (cheap fold), so adding a router at 1.10 is not a breaking change" and "Visual design … — the unreachable panel, page title and favicon are identity and run-story, not design." No substantive change.

### [NIT] No stated version-pinning posture for the two new runtime dependencies

- **id:** `F20` | **confidence:** medium | **category:** completeness | **adversary:** `scope-completeness`
- **location:** tiered_scope.core ('fastapi + uvicorn into [project].dependencies'); pyproject.toml:16-21 (dev group uses `>=` floors); .github/dependabot.yml:26-28 (patch updates ignored)

**Problem.**

The dev group's convention is a `>=` floor with the lock doing the pinning, and dependabot ignores patch bumps. The scope never says the new runtime dependencies follow that convention, leaving the implementer free to pin exactly — a difference that changes how dependabot behaves against the project's first runtime dependencies and how a later `uv lock` moves.

**Proposed fix.**

State it: `fastapi>=…` / `uvicorn>=…` floors matching the dev group's idiom, with uv.lock carrying the exact resolution, and the new npm dependabot entry mirroring the uv entry's monthly + patch-ignore posture (already in core).

### [QUESTION] Open question: should the scope state a forward rule for what /api may return, given every later endpoint inherits this item's prefix and payload habit?

- **id:** `F21` | **confidence:** medium | **category:** framing | **adversary:** `fit-ac`
- **location:** merged scope: gated_decisions[4] ("the health payload gains a field only when the thing it reports exists"), goals[0] ("so items 1.2-1.11 attach endpoints without re-deciding layout")

**Problem.**

The scope correctly concludes that no ledger/economy contract applies today, and that is right — careers/, rulesets/ and the event schema do not exist. But the item's own stated value is that eleven later items inherit its conventions, and two of the repo's settled rules become API-surface concerns from 1.7 onward: state is only ever derived from the fold (ADR 0003) and the build prices upgrades but never scores production (ADR 0008). The scope already invents one forward rule of exactly this kind for the health payload. Whether a second, broader one belongs here is a genuine judgment call, not an obvious yes — it risks pre-deciding 1.2's shape blind, which the scope elsewhere rightly refuses to do.

**Proposed fix.**

Decide explicitly rather than by omission. My inclination is a single sentence in the API package docstring, no more: "every /api response is derived from the ledger fold; nothing here holds authoritative state" — cheap, unenforceable-but-directional, and it costs no design freedom. If that reads as pre-deciding, say so in the scope and leave it to 1.2's request. Either answer is fine; silence is what leaves the next agent guessing.

### [QUESTION] Should the item ship a temporary guard that src/rpg_core/ stays contentless, given scope leakage is the named top failure mode?

- **id:** `F21` | **confidence:** medium | **category:** acceptance | **adversary:** `scope-completeness`
- **location:** non_goals[0] ('The single strongest failure mode for this item is deciding the status page would be more convincing with a career in it'); risks[10]; src/rpg_core/__init__.py (docstring + __version__ only)

**Problem.**

The scope names domain-logic leakage as this item's strongest failure mode and its top non-goal, but nothing tests it. The layering guard checks direction (no web imports in rpg_core), not emptiness — a player model added to rpg_core would pass it cleanly. A guard asserting src/rpg_core/ contains only __init__.py would make the non-goal mechanical, at the cost of being a test written to be deleted at item 1.2, which is its own smell and has no precedent in this repo.

**Proposed fix.**

Put it to the human as a small either/or rather than folding it: (a) no guard, rely on review and the stated non-goal; or (b) a guard whose docstring says in its first line that item 1.2 deletes it, so the deletion is expected rather than a surprise red build. Lean (a) — the non-goal plus the M sizing argue against machinery with a one-item lifetime.

### [QUESTION] /commit's doc gate will independently propose ADR 0010 — settle the ADR question before implementation, not mid-commit

- **id:** `F22` | **confidence:** medium | **category:** fit | **adversary:** `scope-completeness`
- **location:** gated_decisions[2] (recommends no ADR); .claude/skills/update-docs/SKILL.md:100-101 ('If the change makes a *new* decision that isn't recorded anywhere ... that's a missing ADR. Propose it.'); tests/test_repo_structure.py:113-133

**Problem.**

The scope recommends recording nothing as an ADR, but the doc gate that runs inside /commit is instructed to propose exactly that whenever a change makes an unrecorded decision a reader would ask 'why did you do it that way' about — which describes the two-package split, the /api prefix, and the serving strategy. Left unsettled, the debate reopens at commit time with the branch finished and the user under maximum pressure to just say yes. Mechanical constraint if it is taken: test_repo_structure.py:113-133 enforces contiguous numbering AND presence in docs/decisions/README.md's index, so the file and its index row must land in the same commit.

**Proposed fix.**

Ask the user to decide the ADR gate before the plan is written, and record the answer where /commit will see it — either the ADR exists, or DESIGN.md:106-109's 'Two packages, one repo' bullet gains a sentence naming `src/rpg_api/` and the `/api` prefix, so the decision is recorded somewhere and the doc gate has nothing to raise.

### [QUESTION] Open question: does the headline risk deserve a durable core deliverable, not just a PR note and a user-run criterion?

- **id:** `F22` | **confidence:** medium | **category:** risk | **adversary:** `fit-ac`
- **location:** merged scope: risks[0], acceptance_criteria[18] (USER-RUN), tiered_scope.core ("a loud call-out in the PR description and ops/README.md"); ops/README.md:20-24 (the existing rename warning), .claude/settings.json:8 (`PowerShell(gh api *)` in ask)

**Problem.**

The scope identifies branch-protection drift as the single risk that is invisible until broken code is on main, then mitigates it with a guard test (covers the tracked half), a note in the PR description (ephemeral), and a user-run criterion (depends on the user doing it). If the user merges without running `gh api -X PUT`, every subsequent PR merges green with a red frontend job and the guard test — which only compares two tracked files — stays green throughout. The mitigation is the best an agent can do given the permission boundary, but the scope does not say what happens if the last step is skipped.

**Proposed fix.**

Consider making the reapply instruction a durable artifact rather than a PR-description note: extend ops/README.md's existing rename warning (lines 20-24) to cover job ADDITION with the literal command and the exact three-context array, so the instruction survives the PR. Optionally add a sentence to the scope stating the residual: "if the reapply is skipped, the frontend job is advisory-only and the item's third goal is not actually met — this is the one acceptance criterion whose failure is silent."


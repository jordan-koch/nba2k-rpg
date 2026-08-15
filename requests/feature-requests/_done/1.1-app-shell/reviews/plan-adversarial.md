# Plan Panel - Adversarial, Meta-Audit & Convergence

> Provenance trail for `/create-implementation-plan` on `1.1-app-shell`, run 2026-08-14.
> Panel health: 3/3 planners, 2/2 code-grounded adversaries, 1/1 meta-audit, no degraded lenses.
> Not every finding here was accepted into IMPLEMENTATION_PLAN.md - what was applied,
> and what was judged overstated, is recorded in that document.
>
> Mechanical edits for public-repo tracking: absolute repo paths rewritten repo-relative,
> local user paths redacted, placeholder emails redacted, and passages quoting a markdown
> link to a not-yet-existing path wrapped in a fence. Text is otherwise verbatim.

Adversary findings: 27 (blocker=3, major=11, minor=9, nit=3, question=1). Meta-audit findings: 18.

---

## Convergence map

### The SPA dist location must be an injectable factory argument, not a module-level constant or an env key

**Lenses:** code-grounded, sequencing, domain-convention

All three arrived at it from different directions — AC 5's untestability with a constant, Starlette's construction-time failure on a missing directory, and Decision 5's rejection of RPG_SPA_DIST. It is the one API-shape decision the next eleven items inherit, and it is what makes ACs 5 and 6 cold-runnable with no socket and no build.

### Omitting src/rpg_api from the hatch packages list fails ONLY at runtime, because pythonpath=["src"] masks it from every local test

**Lenses:** code-grounded, sequencing, domain-convention

Three independent readings of pyproject.toml:31 against :73 reached the same conclusion the scope calls 'the sneakiest failure in the item'. The test suite structurally cannot see it, so AC 14's guard is not redundant belt-and-braces — it is the only detector, and it must land in the same commit as the packages edit.

### The CI-contexts guard needs SET EQUALITY plus a negative step-name assertion, and the workflow + branch-protection edits must be one commit

**Lenses:** code-grounded, sequencing, domain-convention

All three independently rejected containment on the same grounds: a typo'd context passes containment while hanging every PR forever on a check that never reports — the exact failure ops/README.md:20-24 warns about in prose. All three also flagged that splitting the two edits across commits defeats the guard's purpose.

### The markdown-link trap in tests/test_request_links.py will turn CI red on this very PR

**Lenses:** code-grounded, sequencing, domain-convention

Three planners independently read FENCED_BLOCK (line 26) and confirmed inline backticks are NOT exempt — only 3+ backtick fences are. The scope records the trap firing twice during stage 2, including in the sentence warning about it. It binds the plan document itself, not just the code.

### The item's design rests on unconfirmed tooling beliefs that must be measured before they are coded around

**Lenses:** sequencing, domain-convention

Two planners made it a distinct first phase, and the third flagged the same beliefs as unconfirmed inside its phases. Starlette's construction behavior (inferred), mypy strict over FastAPI decorators (unconfirmed), the leak scan over a package-lock (inferred, not measured) and gitleaks (unassessed) each change either code shape or what can be staged. CLAUDE.md's rule — an unconfirmed claim is a task, not a fact — makes the preflight phase mandatory rather than optional.

### mypy strict must NOT be loosened to accommodate FastAPI; the remedy is an annotated handler

**Lenses:** code-grounded, sequencing, domain-convention

All three named a per-module override as the specific failure mode to refuse, and all three noted it is the exact asymmetry this item exists to prevent on the frontend side. AC 8 pins it, and the check is a diff grep for `type: ignore` and `[[tool.mypy.overrides]]`, not just a green mypy run.

### Windows/CI parity: no shell operators in npm scripts, and the Vite proxy must target the IPv4 literal

**Lenses:** code-grounded, sequencing, domain-convention

Both failures point the wrong way — a `&&` script works in ubuntu CI and fails on the author's daily shell, and a `localhost` proxy target produces an ECONNREFUSED indistinguishable from a dead backend while uvicorn runs fine. Three independent flags on the same two mechanical traps.

### eslint and tsconfig must live INSIDE app/ with file scope limited to app/

**Lenses:** code-grounded, sequencing, domain-convention

All three grounded it the same way: a repo-root config would immediately start reporting on the tracked .js/.mjs under .claude/skills/ (measured: 8 files) and force an ignore list nobody scoped. The scope lists that as an explicit Non-Goal, so this is a hard constraint rather than a preference.

### Scope leakage into item 1.2 is the highest-probability way this item fails on its own terms

**Lenses:** code-grounded, sequencing, domain-convention

All three converted the scope's prose warning into the same mechanical check: `git diff src/rpg_core/` empty, and no careers/rulesets/datasets/var paths in the diff. Two of them made it an explicit acceptance line in more than one phase, which is the right posture for a failure mode that feels like an improvement while it happens.

### AC 23 is an ordered pre-merge gate an agent structurally cannot execute, and it must be written into the PR description

**Lenses:** code-grounded, sequencing, domain-convention

All three located the mechanism at .claude/settings.json line 8 (`gh api *` in the ask list) and all three independently noted that editing ops/branch-protection.json alone never changes GitHub. Two also verified the remote against ops/README.md line 12. The sequencing argument — re-applying after merge makes THIS PR the one that could land red — is what makes the ordering load-bearing rather than pedantic.

---

## Reviewer summaries

### Lens: `code-grounded`

CODE-GROUNDED VERIFICATION of the merged 1.1-app-shell plan. I read every file the plan cites — pyproject.toml, .github/workflows/ci.yml, .github/dependabot.yml, ops/branch-protection.json, ops/README.md, src/rpg_core/__init__.py, DESIGN.md §3, all three test modules, .gitignore, .gitattributes, .claude/settings.json, .claude/skills/commit/SKILL.md, .claude/skills/create-implementation-plan/SKILL.md, docs/data-access.md, docs/decisions/0002, requests/feature-requests/README.md, PROJECT_SCOPE.md, CLAUDE.md, README.md, ROADMAP.md — and re-ran the measurements it claims (git remote, node/npm versions, gitleaks presence, git check-ignore on the planned app/ paths, `git ls-files .claude` .js/.mjs count, directory absences).

VERDICT ON CITATIONS: unusually clean. Roughly 90 code_references were checked and every single file:line resolves to what the plan claims — pyproject.toml:9/11-13/30-31/49/50/61-65/73; ci.yml:10-12/19/22/25/34/42-43/47/50/53-56/58 (and line 47 really is the ONLY occurrence of rpg_core in the workflow); branch-protection.json:3-4; ops/README.md:12/20-24/29/54-57/64-73; test_repo_structure.py:24-34/46-54/60-80/83-92/107-110/113-133; test_no_leaks.py:12-13/26/29/32-35/37/38-55/58-71; test_request_links.py:24/26/40-64; .gitignore:18/43-44/62-63/66-68; .gitattributes:3/7-10/20-25/35/40/41; dependabot.yml:8-14/16-28/30; settings.json:3-12/16-17/27-28/60; commit SKILL.md:49/109/111/116/210; create-implementation-plan SKILL.md:184-228/218; data-access.md:113; ADR 0002 (lines 28-29 do say "no HTTP and no UI"); CLAUDE.md:20-21/58/66; README.md:12-13/51-72/74-83; ROADMAP.md:121-123/156/165. Named symbols all exist: `_git_check_ignore`, `_tracked_text_files`, `_dead_links`, `FENCED_BLOCK`, `TEXT_SUFFIXES`, `ALLOWED`, `test_scratch_root_is_gitignored`, `test_package_version_matches_pyproject`. Every claimed absence is real (app/, src/rpg_api/, tests/conftest.py, careers/, datasets/, rulesets/, lib/, .gitleaks.toml, .gitleaksignore, .editorconfig, docs/data-sources.md). Every measurement reproduces: remote is jordan-koch/nba2k-rpg, node v24.15.0, npm 11.12.1, gitleaks not installed, 8 tracked .js/.mjs under .claude/, CLAUDE.md contains zero "app/" matches, and `git check-ignore --no-index` confirms app/dist/index.html and app/node_modules/react/index.js ignored while app/src/main.tsx is not.

WHAT THE PLAN GOT WRONG is not its citations but its FACTS ABOUT THE WORLD IT WILL RUN IN, plus three tool-behavior assumptions no one measured. The one that stops a cold agent at step one: the feature branch already exists — HEAD is `phase1/app-shell` with the intake and scope commits on it and no upstream — while Phase 0 step 1 orders `git switch -c 1.1-app-shell`. Two more are silent false-greens rather than errors: the negative-typecheck project as specified compiles ZERO files (the inherited `exclude` cancels the child's `include`), so tsc exits non-zero with TS18003 and AC 11 passes without ever checking the fixture; and Vitest with `globals: false` neither registers jest-dom's matchers via a bare import nor runs Testing Library's auto-cleanup, so AC 12's two tests are the shape most likely to be flaky-or-vacuous. Ten findings, blocker → nit.

### Lens: `executability`

EXECUTABILITY & SEQUENCING. The plan is unusually well-grounded — I spot-checked ~40 of its citations (pyproject.toml:9/11-13/30-31/61-65/73, ci.yml:19/34/47/50/58, ops/branch-protection.json:3-4, ops/README.md:12/20-24/54-57/64-73, tests/test_repo_structure.py:24-34/46-54/83-92/107-110, tests/test_no_leaks.py:12-13/26-29/32-35/37/38-55/58-71, tests/test_request_links.py:24/26/40-64, .gitignore:18/43-44/62-63/66-68, .gitattributes:3/7-10/20-25/35/41, .gitattributes, .github/dependabot.yml:16-28/30, .claude/settings.json:3-12/16-17/27-28/60, commit SKILL.md:49/109/210, create-implementation-plan SKILL.md:218, DESIGN.md:99/106-109, CLAUDE.md:20-21/58/66, README.md:12-13/51-72/74-83, ROADMAP.md:156/165, requests/feature-requests/README.md:57-73/96-100/106, docs/data-access.md:113) and every single one is accurate. The "8 tracked .js/.mjs under .claude/" count, node v24.15.0, npm 11.12.1, gitleaks-absent, and the git remote are all confirmed by measurement. The CLAUDE.md conventions are baked in correctly and comprehensively — /commit-only, read-only-git subagents, the public-repo leak rails, careers/ inversion, the resolve-by-name convention correctly reframed in its pre-dataset form as constructor injection, and an affirmatively-argued omission of the data-contracts section.

The failures are in EXECUTION MECHANICS, not in grounding. Two are hard blockers: the plan tells a cold agent to create branch `1.1-app-shell` when the scope and intake commits already live on `phase1/app-shell` (verified: `git branch --show-current`), and Phase 5's acceptance requires observing a green CI job on a pushed branch when ci.yml:3-7 only triggers on push-to-main / pull_request — and /commit never opens the PR, so nothing runs. Beyond that, a cluster of phase-level acceptance criteria are not runnable as written (the CI-contexts honesty proof has no seam to feed a scratch file; Phase 0's var/ check is vacuous), several environment assumptions are unstated and wrong on this machine (`npm create vite` is interactive under -NonInteractive stdin; `curl` is an Invoke-WebRequest alias in PowerShell 5.1 and is not in the allow list; spawning npm/tsc from Node on Windows needs the .cmd shim), and the frontend test setup as specified will fail because `@testing-library/jest-dom` does not extend `expect` under `globals: false`. There is also one internal contradiction (Decision 9's caveat versus the documented dev-mode uvicorn incantation) and one convention violation the plan itself would introduce (`plan` where the pipeline grammar at requests/feature-requests/README.md:100 says `planned`).

Phase ordering itself is sound: 0 preflight → 1 backend+deps+lock → 2 serving → 3 guards-green-today → 4 SPA → 5 CI → 6 docs → 7 handoff. No phase depends on later work except Phase 5's CI-observation criterion. Each phase is independently shippable and each acceptance list is concrete rather than vague, which is the plan's real strength.

### Lens: `meta-audit`

META-AUDIT of the merge, not the repo. I read PROJECT_SCOPE.md in full (23 ACs, 10 Decisions, 15 Risks, the tiered scope), the pipeline README, the stage-3 SKILL.md section menu (§9 Conditional at line 218), then verified the merged plan's citations against the real files: pyproject.toml, ci.yml, ops/branch-protection.json, ops/README.md, tests/test_no_leaks.py, tests/test_repo_structure.py, tests/test_request_links.py, src/rpg_core/__init__.py, DESIGN.md, .gitignore, .gitattributes, dependabot.yml, .claude/settings.json, commit/SKILL.md, CLAUDE.md, README.md, ROADMAP.md, docs/data-access.md. I also re-measured the environment claims the merge asserts (`git remote -v` = jordan-koch/nba2k-rpg; 8 tracked .js/.mjs under .claude; gitleaks NOT installed; node v24.15.0 / npm 11.12.1) — all correct.

CONVERGENCE QUALITY: strong overall. Risk coverage is a near-complete union of all three planners (every scope risk 1-15 and every planner-raised risk except scope risk 3 appears). All 23 ACs are assigned a phase and a command. Where the planners disagreed, the merge chose and RECORDED the choice with rationale (per-request vs construction-time `spa_built`; combined vs split frontend phases; the check-negative wrapper; guard placement) — that is the behaviour I was checking for, and it held. Section 9 is omitted with an affirmative, verified justification rather than by oversight. No gated scope item was silently promoted: Decisions 1-10 are consumed as decided, and the plan's own `gated_decisions` are genuinely new questions, each carrying a recommendation.

Where it fails: (1) the merge inflated the USER-RUN set from the scope's four to five by promoting AC 19, contradicting its own testing map — a real weakening of the acceptance contract; (2) it asserts an AC 11 mechanism (`tsconfig.negative.json` extending a config that excludes the fixture) that yields a FALSE GREEN rather than a proof; (3) the CI-contexts honesty check it prescribes is not runnable against the design it prescribes; (4) it took the heaviest of three preflight variants (a tracked artifact plus its own /commit) without recording why the cheap one lost; (5) it carried one planner's traversal guard in as an acceptance line with no decision entry. Plus citation slips inherited from individual planners (`.json` cited at line 41 — it is 42; "eleven rows" over a ten-row range) and one asymmetry: Node's major is pinned while fifteen npm packages get no version guidance at all.

---

## Adversary findings (code-grounding + executability)

### [BLOCKER] Phase 0 creates the wrong branch — the work is already on `phase1/app-shell`

- **id:** `E2-01` | **confidence:** high | **category:** sequencing
- **location:** plan Phase 0, step 1 (and Phase 7's final prune step); verified against `git branch --show-current` → `phase1/app-shell`, `git log --oneline -3` → 2a03934 "Scope Phase 1 item 1.1, app-shell", e3fe5ca "Open intake for Phase 1 item 1.1, app-shell"

**Problem.**

The plan's very first executable instruction is `git switch -c 1.1-app-shell`. But the branch carrying this item already exists and is checked out: `phase1/app-shell`, holding the two commits that landed FEATURE_REQUEST.md and PROJECT_SCOPE.md. Run from the current HEAD, `git switch -c 1.1-app-shell` either fails (if re-run) or forks a second, differently-named branch off the same tip — leaving two branches for one work item and an ops/branch-protection/PR story that names neither consistently. Run from `main` (which a cold agent might do, since CLAUDE.md says 'work on a branch' and the plan implies starting fresh), it strands e3fe5ca and 2a03934 and the plan's own upstream artifact is not on the branch. The naming is also against repo convention: recent history is `phase0/public repo hardening (#8)`, `Phase0/git push and prune allowances (#11)` — slash-prefixed phase names, not roadmap-id slugs. Phase 7's prune check compounds it by naming `git diff 1.1-app-shell origin/main --stat`, a branch that will not exist if the agent correctly stays on `phase1/app-shell`.

**Proposed fix.**

Replace Phase 0 step 1 with: "Confirm you are on the existing feature branch — `git branch --show-current` must print `phase1/app-shell`, the branch already carrying this item's FEATURE_REQUEST and PROJECT_SCOPE commits. Do NOT create a new branch; `git switch -c` here would fork a duplicate. If you are on `main`, run `git switch phase1/app-shell`." Then propagate the real branch name into Phase 7's prune check (`git fetch origin; git diff phase1/app-shell origin/main --stat`) and into any PR-description text that names the branch.

### [BLOCKER] Phase 5's acceptance requires a CI run that a pushed feature branch does not trigger

- **id:** `E2-02` | **confidence:** high | **category:** executability
- **location:** .github/workflows/ci.yml:3-7 (`on: push: branches: [main]` / `pull_request` / `workflow_dispatch`); plan Phase 5 acceptance item 7 and Phase 7 step 2 (AC 23 step 1)

**Problem.**

Phase 5's final acceptance line reads "On the pushed branch the `Web app` job reports and is green, and its smoke step curls both `/` and `/api/health`". That cannot happen. ci.yml triggers on push ONLY for `branches: [main]`, plus `pull_request` and `workflow_dispatch`. `/commit` pushes the feature branch (commit SKILL.md:210) and explicitly does NOT open the PR. So after Phase 5's checkpoint, zero workflow runs exist and AC 18 — the only check in the entire item that exercises real uvicorn, the real filesystem serve, and the built artifact — is unverifiable by the agent and unverified at the point the plan declares the phase done. AC 23's step 1 has the same hole: "push the branch and let the new job report once, confirming the context name verbatim" presupposes an open PR that nobody has been told to open, and step 3 ("confirm the new check shows as Required on the open PR") confirms the PR must already exist by then.

**Proposed fix.**

Add an explicit user handoff at the Phase 1 checkpoint: "USER ACTION — after this first push, open a DRAFT PR from `phase1/app-shell` to `main`. Every later phase's CI evidence depends on it; `pull_request` is the only trigger a feature branch has (ci.yml:3-7)." Then rewrite Phase 5's acceptance item 7 as an agent-runnable read against the open PR using the already-allowed commands (`.claude/settings.json:34-35` permits `gh run list*` and `gh run view *`): "`gh run list --branch phase1/app-shell --limit 1` shows a completed run whose `Web app` job is green; `gh run view <id> --log` shows the smoke step's two curls." Name `gh workflow run` as the fallback if the user prefers not to open the PR early, and note it is not in the allow list so it prompts.

### [BLOCKER] The feature branch already exists as `phase1/app-shell`; Phase 0 orders a different one created

- **id:** `F1` | **confidence:** high | **category:** repo-state-mismatch
- **location:** requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:1 (scope committed on the live branch) — verified via `git branch --show-current` = phase1/app-shell, `git log --oneline -5` = 2a03934 "Scope Phase 1 item 1.1, app-shell" / e3fe5ca "Open intake…", `git rev-parse @{u}` empty (never pushed); plan Phase 0 step 1, conventions[0], Phase 7 step 8

**Problem.**

The plan opens with "Create the feature branch: `git switch -c 1.1-app-shell`" and repeats the name in its conventions and in Phase 7's prune check (`git diff 1.1-app-shell origin/main --stat`). But the repo is ALREADY on `phase1/app-shell`, which carries both upstream artifacts (the FEATURE_REQUEST and the PROJECT_SCOPE commits) and has no upstream set. A cold agent following the plan literally cuts a second branch off that tip, so the item's work lands on `1.1-app-shell` while the request artifacts' history sits on a differently-named branch — two branches, one PR's worth of work, and a Phase 7 prune check aimed at a branch name that may not be the one the user merges. `git branch -a` confirms only `main` and `phase1/app-shell` exist; there is no `1.1-app-shell`.

**Proposed fix.**

Replace Phase 0 step 1 with a state check rather than a create: run `git branch --show-current`; if it is already `phase1/app-shell` (or any non-`main` branch carrying the 1.1 scope commits), stay on it and set the plan's branch variable to that name. Only `git switch -c` when HEAD is `main`. Then propagate the actual name into Phase 7's prune command and the conventions bullet, and state that /commit's first push will be `git push -u origin phase1/app-shell` (commit SKILL.md:210-216). Note also the naming drift for the record: ROADMAP.md rows are `1.1`, but the live branch uses the `phase1/` prefix — pick the live one, do not rename.

### [MAJOR] Phase 5's acceptance can only be evaluated after its own /commit checkpoint — the gate is circular

- **id:** `E2-03` | **confidence:** high | **category:** sequencing
- **location:** plan Phase 5 `acceptance` (item 7) vs `commit_note`; contrasted with Phases 0-4 and 6, whose acceptance lists are all locally runnable pre-commit

**Problem.**

The plan's stated cadence — repeated in `testing` and in every commit_note — is that a phase ends at a /commit gated on a green local run. Every phase honours that except Phase 5, whose seventh acceptance line is an observation about a CI run that by construction happens after the push, which /commit performs. A cold agent hits an acceptance item it structurally cannot satisfy before the gate, and the likely resolutions are both bad: skip it (AC 18 goes unverified and the plan's strongest end-to-end check evaporates), or block indefinitely.

**Proposed fix.**

Split it. Keep Phase 5's pre-commit acceptance to what is locally checkable (test_ci_contexts green at three contexts, the character-identical cross-read, dependabot entry, no paths filters, bounded poll not a sleep). Move the CI-observation line into an explicit "Phase 5b — post-push verification" block, or fold it into Phase 7 alongside the other things that can only be seen after the branch is on GitHub, with the `gh run list` / `gh run view` commands named.

### [MAJOR] `npm create vite@latest` is interactive; the harness runs commands non-interactively with stdin at the null device

- **id:** `E2-04` | **confidence:** high | **category:** environment-assumption
- **location:** plan Phase 0 BELIEF 3 ("run `npm create vite@latest` for the react-ts template") and Phase 4 step 1 ("Scaffold Vite + React + TypeScript at `app/`"); environment: PowerShell tool runs with -NonInteractive and stdin attached to the null device

**Problem.**

Both the preflight probe and the actual scaffold are specified as bare `npm create vite@latest`, which prompts for project name, framework, and variant. In this harness those prompts read EOF immediately, so the command either errors out or scaffolds something arbitrary. The plan is otherwise meticulous about Windows/PowerShell mechanics (no `&&`, no `rm -rf`, IPv4 literal) but leaves the single command that bootstraps the entire frontend in its interactive form. A cold agent will burn a cycle discovering this and may improvise a template choice the scope did not sanction.

**Proposed fix.**

Write the exact non-interactive incantation in both places: `npm create vite@latest app -- --template react-ts` (naming the target directory suppresses the name prompt; `--template react-ts` suppresses framework and variant). For the Phase 0 probe, scaffold into the gitignored scratch tree: `npm create vite@latest var/spike/vite-probe -- --template react-ts`. Add "if any prompt still appears, the command is wrong — do not answer it, fix the invocation" so the agent does not silently hang.

### [MAJOR] The specified Vitest setup will not work under `globals: false` — jest-dom matchers and RTL cleanup both fail to register

- **id:** `E2-05` | **confidence:** high | **category:** correctness
- **location:** plan Phase 4, the `app/vite.config.ts` step (`test: { environment: "jsdom", setupFiles: "./src/setupTests.ts", globals: false }`) and the `app/src/setupTests.ts` entry in files_to_touch ("Imports @testing-library/jest-dom")

**Problem.**

With `globals: false`, Vitest does not install a global `expect`. The plain `@testing-library/jest-dom` entry point extends whatever global `expect` it finds — under globals:false there is none, so the matchers never attach and any `toBeInTheDocument()` in the two required tests fails with a confusing "expect(...).toBeInTheDocument is not a function". Separately, @testing-library/react's automatic `cleanup` also registers only when a global `afterEach` exists, so with globals off the first test's DOM leaks into the second — precisely the two-test suite AC 12 pins at exactly two. The plan also never tells the implementer that under globals:false every test file must import `describe`/`it`/`expect`/`vi` from `vitest`, though it does reference `vi.stubGlobal`.

**Proposed fix.**

Specify `app/src/setupTests.ts` exactly: `import "@testing-library/jest-dom/vitest";` plus `import { cleanup } from "@testing-library/react"; import { afterEach } from "vitest"; afterEach(cleanup);`. Add one line to the `app/src/App.test.tsx` step: "under `globals: false`, import `describe`, `it`, `expect`, `vi`, `beforeEach` explicitly from `vitest`." Alternatively set `globals: true` and drop the extra imports — but pick one and state it, because the two halves currently disagree.

### [MAJOR] Phase 3's "prove the guard is honest" step is not runnable — test_ci_contexts.py has no seam to accept a scratch file

- **id:** `E2-06` | **confidence:** high | **category:** verifiability
- **location:** plan Phase 3, acceptance item 4 ("mutate a job's display name in a scratch COPY of ci.yml … and confirm the comparison fails") vs the same phase's step specifying the test as `yaml.safe_load .github/workflows/ci.yml` and `ops/branch-protection.json` directly

**Problem.**

The plan is admirably careful with the layering guard: it mandates a PURE function `web_imports_under(root: Path)` precisely so red-and-green can both be proven without touching tracked source. It then asks for the identical proof from the CI-contexts guard but specifies that one as a test that loads the two tracked paths inline. There is no parameterized entry point, so "mutate a scratch copy and confirm the comparison fails" has nothing to call. A cold agent will either skip the acceptance line or — much worse, and the exact thing the layering-guard design was built to avoid — edit the tracked ci.yml to watch the test go red.

**Proposed fix.**

Mirror the layering guard's shape. Specify two pure helpers in `tests/test_ci_contexts.py`: `job_display_names(workflow: Path) -> set[str]` and `required_contexts(protection: Path) -> set[str]`, plus a `_diff_message(ci: set[str], protection: set[str]) -> str`. The real assertion calls them on the tracked paths; the honesty proof writes a mutated workflow to `tmp_path` and asserts the two sets differ and the message names which side carries the extra. Both polarities then land in one `uv run pytest` with zero tracked-source mutation, exactly as AC 3 does.

### [MAJOR] Decision 9 contradicts itself inside a single Phase 6 bullet — and nothing says how reload is actually invoked

- **id:** `E2-07` | **confidence:** high | **category:** correctness
- **location:** plan Phase 6, step 1 ("dev = two commands in two terminals (uvicorn with reload; `npm run dev` …)" followed by "Decision 9's caveat: do not also document a raw uvicorn incantation"); against PROJECT_SCOPE.md:514 Decision 9 ("only one canonical way to run the served BUILD gets documented")

**Problem.**

The same bullet instructs the implementer to document a raw uvicorn dev command and, one sentence later, forbids documenting a raw uvicorn incantation. A cold agent cannot satisfy both. Compounding it: Phase 1 adds `watchfiles` to the dev group specifically for reload, but `serve.py`'s `main()` is specified as `uvicorn.run(..., factory=True, host, port)` with no reload, and the plan explicitly forbids a `__main__.py`. So `watchfiles` is installed for a command the plan never actually writes down. The scope's Decision 9 is narrower than the plan's paraphrase — it scopes the one-canonical-way rule to the SERVED build, which leaves the dev-mode uvicorn command perfectly legal.

**Proposed fix.**

Reword to: "Dev mode is two terminals — `uv run uvicorn rpg_api.app:create_app --factory --reload --host 127.0.0.1 --port 8000` in one, `npm run dev` from `app/` in the other. Served mode is the console script ALONE. Decision 9's caveat binds the SERVED build only: do not document a second way to run the served build. `watchfiles` in the dev group is what makes `--reload` fast; it is a dev dependency because dev mode is the only mode that reloads." That resolves the contradiction and gives watchfiles a stated purpose.

### [MAJOR] The plan prescribes a status value the pipeline grammar does not define — `plan` where it must be `planned`

- **id:** `E2-08` | **confidence:** high | **category:** convention
- **location:** requests/feature-requests/README.md:100 ("**Status grammar:** `intake` → `scoped` → `planned` → `implemented`") vs plan files_to_touch entries for `requests/feature-requests/IMPLEMENTATION_PLAN.md` ("Opens `> **Status:** plan · created 2026-08-14 · decided · next: implement`") and `requests/feature-requests/README.md` ("advances its Stage cell to `plan`")

**Problem.**

Two places in the plan prescribe the token `plan`. The contract defines four stage values and `plan` is not one of them — `planned` is. PROJECT_SCOPE.md line 1 correctly uses `scoped`, so the precedent is unambiguous. This matters more than a typo because /update-docs is documented to check "the requests/ Index rows match their artifacts' status headers", and /commit's Step 3 runs the doc-drift gate; a cold agent writing `plan` in both places produces a self-consistent but off-grammar pair that the human reviewer has to catch. Phase 6 also folds this Index edit into the docs phase, meaning it lands under the same /commit that runs the doc gate.

**Proposed fix.**

Change both to `planned`: the plan's own header becomes `> **Status:** planned · created 2026-08-14 · decided · next: implement`, and the Index row's Stage cell at requests/feature-requests/README.md:106 advances `scoped` → `planned` (→ `implemented` after stage 4). Add a one-line pointer to requests/feature-requests/README.md:100 next to the instruction so the value is checkable rather than remembered.

### [MAJOR] `check-negative.mjs` portability and lintability are both asserted rather than specified

- **id:** `E2-09` | **confidence:** medium | **category:** executability
- **location:** plan Phase 4 ("`app/scripts/check-negative.mjs` spawns the negative tsc run and exits 0 iff the inner run failed. One command, identical on Windows and ubuntu-latest"); gated_decisions entry 5; eslint step ("keep `scripts/` linted", `globals` listed as a dev dependency)

**Problem.**

Two unstated mechanics will bite. (1) Spawning: on Windows, `npm` and `tsc` are `.cmd` shims, and Node's `spawnSync("npm", …)` without `shell: true` fails with ENOENT — the exact platform the plan is written for (PowerShell 5.1, per the environment and the plan's own `&&` warnings). The claim "identical on Windows and ubuntu-latest" is asserted, not engineered. (2) Linting: the file is inside `eslint .`'s scope (the plan ignores only `dist` and `typecheck-fixtures`) and will use `process.exit` and `node:child_process`. Under `@eslint/js` recommended, `no-undef` is on and `process` is undefined unless `languageOptions.globals` is populated. The plan lists `globals` as a dev dependency but never says where it is wired, so `npm run lint` fails on the very file that makes AC 11 runnable.

**Proposed fix.**

Specify the spawn concretely: `spawnSync(process.execPath, [require.resolve-style path to node_modules/typescript/bin/tsc, "--noEmit", "-p", "tsconfig.negative.json"], { cwd, stdio: "inherit" })` — invoking `tsc`'s JS entry through `process.execPath` sidesteps the shim entirely on both platforms. Then add the eslint block explicitly: a config object with `files: ["scripts/**/*.mjs"]` and `languageOptions: { globals: globals.node, sourceType: "module" }`, which is what the `globals` dependency is for.

### [MAJOR] AC 19 is mislabeled USER-RUN in Phase 7, and the summary claims five user-run criteria where the scope has four

- **id:** `E2-10` | **confidence:** high | **category:** verifiability
- **location:** plan Phase 7 acceptance item 1 ("USER-RUN AC 19: `uv run <console-script>` serves the built app") and plan `summary` ("hands the five USER-RUN criteria back"); against PROJECT_SCOPE.md:237-238 (AC 19, unmarked) and :239-258 (ACs 20-23, each marked USER-RUN)

**Problem.**

The scope marks exactly four criteria USER-RUN — 20, 21, 22, 23. AC 19 is an ordinary testable criterion. The plan's own `testing` section gets this right, mapping AC 19 to "`uv run <console-script>` plus a curl of both routes" among the agent-runnable selectors, and Phase 6 verifies it end to end. But Phase 7 re-lists it under USER-RUN and the summary inflates the count to five. requests/feature-requests/README.md:71-73 explains why the label is load-bearing: user-run criteria exist so the acceptance panel does NOT claim them. Mislabeling an agent-provable criterion means stage 4's panel will decline to prove something it is obligated to prove, and the item can be declared done with the console entrypoint never exercised — the one check that would catch a missing hatch `packages` entry independently of AC 14's structural test.

**Proposed fix.**

Delete the AC 19 line from Phase 7's acceptance list, correct the summary to "the four USER-RUN criteria (ACs 20-23)", and leave AC 19 where it belongs — Phase 6's step that already runs the console script and hits both routes. Add a sentence to Phase 7: "AC 19 is NOT user-run; it was proven in Phase 6 and the acceptance panel must claim it."

### [MAJOR] Phase 6's local AC-19 verification uses `curl` on PowerShell and never stops the backgrounded server

- **id:** `E2-11` | **confidence:** high | **category:** environment-assumption
- **location:** plan Phase 6, step "Verify AC 19 end to end: run the console script in one shell (backgrounded), curl `/` and `/api/health` from another"; .claude/settings.json:13-58 (allow list has no curl / Invoke-WebRequest entry); Phase 7 ACs 20-21 which then need port 8000

**Problem.**

Three problems in one step. (1) In Windows PowerShell 5.1 `curl` is an alias for `Invoke-WebRequest`, which does not accept curl's flags — a cold agent copying curl syntax gets a parameter-binding error, not a request. (2) Neither `curl` nor `Invoke-WebRequest` is in `.claude/settings.json`'s allow list (which does cover `PowerShell(uv *)`, `node *`, `npm *`), so the call prompts, breaking the plan's otherwise-careful accounting of what needs a human. (3) Nothing anywhere tells the agent to stop the backgrounded uvicorn. It holds 127.0.0.1:8000 for the rest of the session, so the very next thing the plan asks for — the user-run ACs 20 and 21, both of which start a backend on 8000 — dies with EADDRINUSE, and the symptom ("the page is blank / connection refused after I started it") points at the frontend.

**Proposed fix.**

Specify PowerShell-native, already-allowed commands: start with `uv run <console-script>` via the background runner, poll with `uv run python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health').status==200 else 1)"` (covered by `PowerShell(uv *)`, needs no new permission and no curl), or `Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/api/health` if a prompt is acceptable. Then add an explicit teardown line: "Stop the backgrounded server before moving on — Phase 7's ACs 20 and 21 both bind 127.0.0.1:8000 and will fail with EADDRINUSE if it is still running."

### [MAJOR] `tsconfig.negative.json` as specified compiles zero files — AC 11 goes green without ever checking the fixture

- **id:** `F2` | **confidence:** high | **category:** false-green
- **location:** requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:203-206 (AC 11: "a committed, deliberately ill-typed fixture … asserted to exit non-zero — proving `strict` is actually engaged"); plan Phase 4 steps 5-7 and files_to_touch app/tsconfig.json + app/tsconfig.negative.json

**Problem.**

The plan specifies `app/tsconfig.json` with `exclude: ["typecheck-fixtures", "dist", "node_modules"]`, then `app/tsconfig.negative.json` "extending tsconfig.json, including only typecheck-fixtures". In TypeScript, a child that specifies `include` does NOT reset the parent's `exclude` — `exclude` is inherited and filters the child's `include`, so the negative project resolves to an empty file set. tsc then fails with TS18003 ("No inputs were found in config file") and exits non-zero. `app/scripts/check-negative.mjs`, which exits 0 iff the inner run failed, reports success — so AC 11 passes because the config found nothing, not because `strict` caught the fixture. This is precisely the failure mode AC 11 exists to rule out, and the plan's own guidance ("errors MUST be strict-SPECIFIC") is defeated silently.

**Proposed fix.**

In `app/tsconfig.negative.json` override BOTH keys: `{"extends": "./tsconfig.json", "include": ["typecheck-fixtures"], "exclude": []}`. Then harden the wrapper so it cannot be fooled again: `app/scripts/check-negative.mjs` must capture tsc's stdout and assert (a) exit code non-zero, (b) the output does NOT contain `TS18003`, and (c) the output contains the two strict-specific codes the fixture is built to raise (the `s.length` case raises TS18048/TS2532 under strictNullChecks; the `xs[0]` return raises TS2322 under noUncheckedIndexedAccess). Add that assertion list to the Phase 4 acceptance line for AC 11.

### [MAJOR] Vitest `globals: false` breaks jest-dom matcher registration and Testing Library auto-cleanup

- **id:** `F3` | **confidence:** medium | **category:** tooling-behavior
- **location:** requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:207-208 (AC 12: exactly two Vitest tests); plan Phase 4 steps 9, 12, 13 and files_to_touch app/src/setupTests.ts + app/vite.config.ts

**Problem.**

The plan pins `test: { environment: "jsdom", setupFiles: "./src/setupTests.ts", globals: false }` and then says setupTests.ts "imports @testing-library/jest-dom". With `globals: false` there is no global `expect` for the bare `@testing-library/jest-dom` entry to extend, so matchers like `toBeInTheDocument()` are simply absent — the implementer hits a runtime TypeError and the obvious 'fix' is to flip `globals: true`, quietly diverging from the plan. Separately, @testing-library/react registers its automatic `cleanup` only when a global `afterEach` exists; with `globals: false` it does not, so the first test's rendered DOM persists into the second and a `screen.getByText(...)` on the version string can throw 'found multiple elements'. AC 12 pins the count at exactly two tests, so both tests render — this is the exact configuration where the leak bites.

**Proposed fix.**

Make three things explicit in Phase 4: (1) setupTests.ts imports the vitest-specific entry — `import "@testing-library/jest-dom/vitest"` — not the bare package; (2) setupTests.ts also does `import { afterEach } from "vitest"; import { cleanup } from "@testing-library/react"; afterEach(cleanup);`; (3) `app/src/App.test.tsx` imports `{ describe, test, expect, vi, afterEach }` from `"vitest"` explicitly, since nothing is global. Alternatively set `globals: true` and add `"types": ["vitest/globals"]` to tsconfig — but then say so, because the plan's tsconfig `types` list is currently silent and `npm run typecheck` covers `src/` including the test file.

### [MINOR] The repo-relative dist default is prescribed without its formula or its editable-install assumption

- **id:** `E2-12` | **confidence:** medium | **category:** correctness
- **location:** plan Phase 1, the `src/rpg_api/app.py` step ("resolve the default dist from the repo root derived from `Path(__file__).resolve()` — NEVER a literal path"); AC 19 and the Phase 5 smoke step both depend on it

**Problem.**

The instruction names the technique but not the arithmetic, and not the assumption underneath it. From `src/rpg_api/app.py` the repo root is `parents[2]` and the dist is `parents[2] / "app" / "dist"` — off-by-one here produces a default that silently never finds a build, so `/` always 503s and `spa_built` is always false while every unit test (which injects `tmp_path`) stays green. Underneath that: the formula only lands on the real repo when the package is installed editable or is on `pythonpath`. `uv sync` does install the root project editable by default, so AC 19 and the CI smoke step work — but that is an unstated dependency, and it is the same class of runtime-only failure the plan correctly makes AC 14 exist for.

**Proposed fix.**

Write the expression out: `_REPO_ROOT = Path(__file__).resolve().parents[2]` and `_DEFAULT_DIST = _REPO_ROOT / "app" / "dist"`, with a source comment: "correct for a source checkout or an editable install (`uv sync` installs the project editable); a non-editable wheel would resolve into site-packages, which is why AC 19 runs the console script from the checkout." Add one acceptance line to Phase 2: with no `spa_dist` argument and a real `app/dist/index.html` present, `create_app()` serves it — so the default path is exercised at least once, not only the injected one.

### [MINOR] files_to_touch omits the Vite scaffold's leftovers, and its single-tsconfig decision collides with what the template emits

- **id:** `E2-13` | **confidence:** high | **category:** completeness
- **location:** plan `files_to_touch` (app/* entries) vs plan Phase 4 steps (`app/tsconfig.json` single config; "`app/index.html` with a real page title and favicon, not the Vite template defaults")

**Problem.**

The `npm create vite@latest -- --template react-ts` scaffold emits files the checklist does not mention: `src/App.css`, `src/index.css`, `src/assets/react.svg`, `public/vite.svg`, a `README.md`, its own `eslint.config.js`, and — directly against the plan's single-config decision — `tsconfig.json` as a solver-only stub plus `tsconfig.app.json` and `tsconfig.node.json`. A cold agent working the checklist literally either commits the Vite template's identity (the scope forbids template defaults, and `public/vite.svg` plus the React logo is exactly that), or discovers the tsconfig split mid-phase with no instruction on whether to collapse it. The checklist is the artifact an implementer works down; anything the scaffold leaves that is not on it becomes an unowned decision.

**Proposed fix.**

Add an explicit post-scaffold step to Phase 4: "Delete `app/README.md`, `app/public/vite.svg`, `app/src/assets/`, `app/src/App.css`, `app/src/index.css`, and the scaffold's `eslint.config.js`; collapse `tsconfig.app.json` + `tsconfig.node.json` into the single `app/tsconfig.json` this plan specifies and delete both. Then `git status --porcelain --untracked-files=all app/` and confirm every remaining file is one the checklist names — anything else is scaffold residue and is either owned or deleted, never silently committed."

### [MINOR] Phase 0's second acceptance criterion is vacuous — gitignored paths never appear in `--untracked-files=all`

- **id:** `E2-14` | **confidence:** high | **category:** verifiability
- **location:** plan Phase 0, acceptance item 2 ("`git status --porcelain --untracked-files=all` shows nothing under `var/` as a staging candidate"); .gitignore:18 (`var/`)

**Problem.**

`var/` is gitignored, so `git status --porcelain --untracked-files=all` never lists anything under it — `--ignored` would be required. The criterion therefore passes unconditionally and proves nothing, including in the failure case it was written to catch (a probe accidentally written outside `var/`). The second half of the same line — pyproject.toml and uv.lock byte-identical to HEAD — is the real check and is stated only as prose with no command.

**Proposed fix.**

Replace with two runnable checks: `git status --porcelain --untracked-files=all` returns ONLY the new `requests/feature-requests/1.1-app-shell/reviews/preflight.md` (anything else means a probe escaped `var/`), and `git diff --stat HEAD -- pyproject.toml uv.lock` is empty (proving `uv run --with` did not disturb the lock, which is the actual claim Phase 0 rests on).

### [MINOR] The `/api` JSON-404 boundary only covers GET; non-GET methods under /api fall through to a plain-text 405

- **id:** `E2-15` | **confidence:** medium | **category:** correctness
- **location:** plan Phase 2, step 1 ("registering ONE catch-all `@app.get(\"/{full_path:path}\")`") and step 2's api-prefix branch; PROJECT_SCOPE.md:192-193 (AC 7)

**Problem.**

AC 7 is written about GET, so the plan satisfies it literally. But the catch-all is registered for GET only, which means `POST /api/unknown` matches the route path with a non-matching method and Starlette answers with a plain-text 405 — not JSON. That is the same failure class AC 7 exists to prevent (a non-JSON response on an /api path), and it is inherited: items 1.8, 1.9 and 1.11 all add POST endpoints, and the first agent to typo a POST URL debugs an HTML/plain-text body from a JSON API. The plan's own framing — "a failure a cold agent adding endpoints at items 1.7-1.11 will inherit" — applies here and is not addressed.

**Proposed fix.**

Register the catch-all for the method set rather than GET alone (`@app.api_route("/{full_path:path}", methods=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"])`), keeping the `/api` JSON-404 branch first and returning the SPA/503 branches only for GET and HEAD. Add one line to `tests/test_api_spa.py`: `POST /api/nope` returns 404 with content-type `application/json`. One assertion, and the boundary is then honest for the eleven items that inherit it.

### [MINOR] Stage value `plan` contradicts the pipeline's status grammar, which is `planned`

- **id:** `F4` | **confidence:** high | **category:** convention-drift
- **location:** requests/feature-requests/README.md:100 — "**Status grammar:** `intake` → `scoped` → `planned` → `implemented`"

**Problem.**

The plan says the Index row's Stage cell "advances to `plan` then `implemented`" (onboarding files_to_read, Phase 6 step 8, files_to_touch for requests/feature-requests/README.md), and specifies the plan document's own header as `> **Status:** plan · created 2026-08-14 · decided · next: implement`. The tracked grammar at README.md:100 has no `plan` state — the value is `planned`, and PROJECT_SCOPE.md:1 follows the grammar exactly (`scoped`). Writing `plan` puts the Index row and the artifact header out of step with the documented vocabulary, which /update-docs checks ("the requests/ Index rows match their artifacts' status headers").

**Proposed fix.**

Use `planned` in all three places: the Index row at requests/feature-requests/README.md:106, the plan's own status blockquote, and the Phase 6 step describing the advance. Keep `next: implement` — README.md:98's grammar allows the literal string "implement" for the next field.

### [MINOR] Reading the dist path off `request.app.state` leaks `Any` into a strict-mypy return — the exact friction AC 8 forbids papering over

- **id:** `F5` | **confidence:** medium | **category:** type-strictness
- **location:** pyproject.toml:61-65 (`strict = true`, `warn_unreachable = true`, `files = ["src", "tests"]`) vs plan Phase 1 step 8 ("Pass the resolved dist in via `request.app.state` or a dependency, whichever keeps mypy strict green with no ignore")

**Problem.**

Starlette types `Request.app` as `Any` and `State.__getattr__` as `-> Any`. Under `strict = true` (which enables `warn_return_any`), a health handler that computes `return (request.app.state.spa_dist / "index.html").is_file()` in a function annotated `-> bool` returns `Any` from a declared-bool function and mypy errors. The plan offers the implementer a choice without saying which side is safe, and the shortest path out of a strict error is a `# type: ignore` — which AC 8 (PROJECT_SCOPE.md:194-197) fails retroactively, and which the plan itself checks for with a diff grep. Leaving it as 'whichever keeps mypy green' hands a cold agent the failing option first.

**Proposed fix.**

Prescribe the closure/dependency form rather than app.state: inside `create_app`, resolve `dist: Path` once and define `def get_spa_dist() -> Path: return dist`, then have the health handler take `dist: Annotated[Path, Depends(get_spa_dist)]`. The closure is fully typed, mypy never sees `Any`, and `attach_spa` can capture the same local. If app.state is kept for any reason, require an annotated local (`dist: Path = request.app.state.spa_dist`) so the `Any` is absorbed at assignment rather than returned — and say explicitly that a `type: ignore` here fails AC 8.

### [MINOR] `npm create vite@latest` in Phase 0 is interactive and will hang or EOF in an agent shell

- **id:** `F6` | **confidence:** high | **category:** cold-runnability
- **location:** requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:333 ("Measured on this machine: node v24.15.0, npm 11.12.1") — plan Phase 0 BELIEF 3 step

**Problem.**

Phase 0 BELIEF 3 says: "in the scratch dir run `npm create vite@latest` for the react-ts template". Bare `npm create vite@latest` prompts for project name, framework, and variant. The agent shell here runs non-interactive with stdin on the null device, so the prompts read EOF and the probe either aborts or produces a scaffold nobody chose — and BELIEF 3 is the phase that measures the `dist/` layout the whole Phase-2 serving design keys off. (node v24.15.0 / npm 11.12.1 both reproduce as measured, so the toolchain half of the belief is fine.)

**Proposed fix.**

Give the exact non-interactive invocation: `npm create vite@latest spa-probe -- --template react-ts` run from `var/spike/`, followed by `npm install` and `npm run build` inside `var/spike/spa-probe/`. Record the resolved `lockfileVersion` and whether assets land under `dist/assets/`. Same fix applies to Phase 4's scaffold step, which inherits the same ambiguity.

### [MINOR] Phase 6 tells the implementer to document the dev-mode uvicorn command and, two clauses later, not to document a raw uvicorn incantation

- **id:** `F7` | **confidence:** high | **category:** internal-contradiction
- **location:** requests/feature-requests/1.1-app-shell/PROJECT_SCOPE.md:514 (Decision 9's caveat: "only one canonical way to run the served build gets documented — the console script, not a raw uvicorn incantation") and :239-243 (AC 20 requires two commands in two terminals, uvicorn with reload)

**Problem.**

Phase 6 step 1 instructs: "Document BOTH run modes: dev = two commands in two terminals (uvicorn with reload; `npm run dev` in app/) … and served = the console script ALONE. Decision 9's caveat: do not also document a raw uvicorn incantation." Those two sentences conflict as written, because the dev-mode backend command IS a raw uvicorn incantation (`uv run uvicorn rpg_api.app:create_app --factory --reload`) — the console script as specified in Phase 1 hardcodes `uvicorn.run(...)` with no reload flag. A cold agent resolving the contradiction by dropping the uvicorn line leaves AC 20's dev seam undocumented; resolving it the other way looks like violating Decision 9. Compounding it, AC 22 requires the unreachable panel to NAME the start command, and the plan never says which of the two it names.

**Proposed fix.**

Scope the caveat explicitly: 'Decision 9 governs the SERVED-BUILD mode only — exactly one documented way to run it (the console script). The DEV mode's backend command is necessarily a raw uvicorn invocation with `--reload`; document it once in ops/README.md's Node section and nowhere else.' Then pin AC 22's panel copy to a single string — recommend the console script name, since that is the command that works in both modes — and note it is the same string the gated console-script decision fixes in five places.

### [MINOR] A `__file__`-relative repo-root default for the SPA dist quietly breaks on a non-editable install — the very environment AC 14 is about

- **id:** `F8` | **confidence:** medium | **category:** runtime-fragility
- **location:** pyproject.toml:30-31 (`[tool.hatch.build.targets.wheel] packages = ["src/rpg_core"]`) and pyproject.toml:73 (`pythonpath = ["src"]`) — plan Phase 1 step 10 and decisions[2]

**Problem.**

The plan argues at length (risks, convergence_map, AC 14) that the hatch `packages` entry matters because the console script must resolve "on an installed environment", and in the same phase specifies `create_app`'s default dist as "the repo root derived from `Path(__file__).resolve()`". Those two claims are in tension: if the project is ever installed non-editable (a built wheel, a `uv pip install .`, a `uvx` run), `Path(__file__)` sits in site-packages and `parents[2]/app/dist` points at a directory that will never exist — so the console script starts, `/api/health` answers, `spa_built` is false, and `GET /` returns the 503 telling the user to run `npm run build`, which will not help. It works today only because `uv sync` installs the project editable, which nothing in the plan states.

**Proposed fix.**

State the assumption and make it self-diagnosing: (1) record in the plan and in a `create_app` comment that the default resolution assumes a checkout (PROJECT_SCOPE.md:130 already says "It runs from a checkout"), (2) resolve the root as `Path(__file__).resolve().parents[2]` and assert at resolve time that `(root / "pyproject.toml").is_file()`; when it is not, fall back to `Path.cwd() / "app" / "dist"` rather than a site-packages path, and (3) keep the literal-path prohibition intact (tests/test_no_leaks.py:26 fails the build on a tracked drive-letter path).

### [NIT] The per-phase gate command drifts from the one ops/README.md documents, and Phase 6 edits that file without reconciling it

- **id:** `E2-16` | **confidence:** high | **category:** convention
- **location:** ops/README.md:66-73 ("The same four commands CI runs, in the same order" — `uv run pytest`, no marker filter) vs plan `testing` and every phase acceptance (`uv run pytest -m "not network"`); ci.yml:47 (which does pass `-m "not network"`)

**Problem.**

The plan's gate is `uv run pytest -m "not network"`, which correctly mirrors ci.yml:47. ops/README.md:72 documents plain `uv run pytest` under the claim that these are "the same four commands CI runs" — a claim that is already slightly false today and that the plan cites as its authority for the cadence. Phase 6 rewrites the surrounding section (adding the Node toolchain beside it, per ops/README.md:32-62) and is the natural moment to fix it, but no step says to. The result is a plan that tells the implementer to run one thing while the document the plan just edited tells the next person to run another.

**Proposed fix.**

Add a bullet to Phase 6's ops/README.md step: "While you are in this file, correct line 72 to `uv run pytest -m \"not network\"` so the block's own claim — 'the same four commands CI runs' — matches ci.yml:47." Extend the Node section with the five frontend commands under the same framing so the doc lists the full CI-parity set for both halves.

### [NIT] Small count and line-range imprecisions in the architecture map and roadmap citations

- **id:** `F10` | **confidence:** high | **category:** citation-precision
- **location:** ROADMAP.md:166-175 (rows 1.2 through 1.11 — ten rows, not eleven); tests/test_repo_structure.py:139 (file ends at 139, not 140); tests/test_no_leaks.py:121; tests/test_request_links.py:76; ROADMAP.md:123-125 (the Status legend runs to 125)

**Problem.**

Four numeric claims are off by one and one is off by one row. The architecture map states the three test modules are 140 / 122 / 77 lines; measured with a line count they are 139 / 121 / 76. The onboarding and code_references both say "eleven Phase-1 roadmap rows (ROADMAP.md 166-175)" and "the eleven downstream Phase 1 rows (1.2 through 1.11)" — that range holds ten rows; Phase 1 has eleven rows total only if 1.1 itself is counted, and 1.1 is the item being built. The legend citation "ROADMAP.md:121-123 the ★/Status legend" truncates: ★ is at 121-122 and the Status legend runs 123-125. None of this misdirects an implementer, but the plan's whole credibility rests on line citations being literally trustworthy, and a cold agent that checks one and finds it off starts checking all of them.

**Proposed fix.**

Correct to 139 / 121 / 76 lines; say "the ten downstream Phase 1 rows (1.2 through 1.11) at ROADMAP.md:166-175", or "eleven Phase 1 rows, ten of them downstream"; cite the legend as ROADMAP.md:120-125. Everything else in code_references verified exact — worth stating that in the section-10 trust ledger as "~90 cites checked, 5 corrected, all corrections numeric".

### [NIT] The health payload uses a pydantic model, but Phase 1 declares only fastapi + uvicorn as runtime dependencies

- **id:** `F9` | **confidence:** high | **category:** dependency-hygiene
- **location:** pyproject.toml:9 (`dependencies = []`) with the reservation comment at 11-13 — plan Phase 1 steps 1 and 7

**Problem.**

Phase 1 step 1 replaces the empty dependency list with "fastapi + uvicorn" only, while step 7 specifies the health route returns "a pydantic model `Health(status: str, version: str, spa_built: bool)`". `pydantic` then becomes a directly-imported, undeclared transitive dependency — it resolves today because FastAPI requires it, but the pin is somebody else's. It is a small thing on a repo whose Phase-0 comment (pyproject.toml:11-13) is explicit that "nothing is installed speculatively", i.e. that the dependency list is meant to be an honest statement of what the code imports.

**Proposed fix.**

Either add `pydantic` to `[project].dependencies` alongside fastapi and uvicorn (one line, one lock entry, honest), or drop the model and return a `TypedDict` with an explicit `response_model=None` — the payload is three scalar fields and FastAPI serializes a dict fine. Pick one in Phase 1 so `uv lock` still runs exactly once, as the plan requires.

### [QUESTION] Intent-to-add staging is prescribed but never unwound or upgraded before /commit

- **id:** `E2-17` | **confidence:** medium | **category:** executability
- **location:** plan Phase 4, the PRE-STAGING GATE step ("stage first with `git add --intent-to-add app/`, THEN run `uv run pytest tests/test_no_leaks.py`") and the same phase's commit_note; tests/test_no_leaks.py:58-71 (`git ls-files -z`)

**Problem.**

The mechanism is right — `git add -N` creates index entries, so `git ls-files` (tests/test_no_leaks.py:59) sees them and the leak scan stops being a false green. But the plan never says what happens to those intent-to-add entries afterwards. They persist: `git status` reports the files as tracked-but-unstaged, `git diff` renders every one of them (including package-lock.json) as an addition, and /commit's Step 2 deliberate-staging survey (commit SKILL.md:49) now reads a working tree in a half-staged state it was not designed around. It probably resolves cleanly when /commit runs `git add app/`, but the plan asserts nothing about it and I have not run it (read-only).

**Proposed fix.**

Add one sentence after the gate: "The `-N` entries stay in the index. When you invoke /commit, stage `app/` by path for real (`git add app/`) so the intent-to-add placeholders are replaced by content — never `git add -A` (commit SKILL.md:49). If you need to back out before committing, `git rm --cached -r app/` removes the placeholders without touching the working tree." That keeps the leak gate honest and leaves the tree in a state /commit's survey step reads normally.

---

## Meta-audit findings (did the merge converge faithfully?)

### [MAJOR] Merge promoted AC 19 into the USER-RUN set, contradicting the scope and the plan's own testing map

- **id:** `M1` | **confidence:** high | **category:** completeness-contract-drift
- **location:** Merged plan → summary ("Phase 7 hands the five USER-RUN criteria back") and phases[7].acceptance[0] ("USER-RUN AC 19"), against PROJECT_SCOPE.md:237-258 and the merged plan's own testing section ("AC 19 -> `uv run <console-script>` plus a curl of both routes"; "AC 20-23 -> USER-RUN")

**Problem.**

The decided scope marks exactly FOUR criteria USER-RUN — ACs 20, 21, 22, 23 (PROJECT_SCOPE.md:239-258). AC 19 ("`uv run <console-script>` serves the built app", line 237) carries no USER-RUN marker and is plainly agent-runnable. The merge's summary claims "five USER-RUN criteria" and Phase 7's acceptance list opens with "USER-RUN AC 19", while the merge's own testing section maps AC 19 to an agent command and says "AC 20-23 -> USER-RUN, Phase 7", and Phase 6 already prescribes "Verify AC 19 end to end". Two of the three planners (code-grounded, sequencing) listed four; the merge picked up domain-convention's Phase-7 "Hand over AC 19" step and propagated it into the summary. Per requests/feature-requests/README.md:71-73 the USER-RUN marker exists so "the acceptance panel doesn't claim them" — mislabeling an agent-checkable criterion inverts that, licensing the stage-4 panel to skip an executable check on the one entrypoint AC 14 exists to protect.

**Proposed fix.**

Strike AC 19 from phases[7].acceptance and from the USER-RUN framing; change the summary to "the four USER-RUN criteria". Keep AC 19 where the testing map already puts it: Phase 6's agent-run check (console script backgrounded + curl of `/` and `/api/health`), corroborated by the Phase 5 CI smoke step. Phase 7 then hands over 20, 21, 22, 23 only.

### [MAJOR] AC 11's negative-typecheck design produces a false green: tsconfig.negative.json inherits the parent's `exclude`

- **id:** `M2` | **confidence:** high | **category:** cost-unrealism
- **location:** Merged plan → phases[4].steps ("`app/tsconfig.json` ... exclude [\"typecheck-fixtures\", \"dist\", \"node_modules\"]" and "`app/tsconfig.negative.json` extending tsconfig.json, including only typecheck-fixtures"), plus files_to_touch entries for app/tsconfig.negative.json and app/scripts/check-negative.mjs; scope AC 11 at PROJECT_SCOPE.md:203-206

**Problem.**

In TypeScript an extending config replaces the parent's `include` but INHERITS `exclude` unless it redefines it. The plan has the parent exclude `typecheck-fixtures` and the child include only `typecheck-fixtures`, so the child resolves to zero input files and tsc exits with TS18003 ("No inputs were found in config file") — a NON-ZERO exit. `check-negative.mjs` is specified to "exit 0 iff the inner run failed", so it reports success while proving nothing about `strict`, `noUncheckedIndexedAccess`, or the fixture. That is exactly the failure AC 11 was written to prevent ("a default-generated config that checks nothing"), reproduced one level up. All three planners assumed the extend-and-narrow pattern works and none named the inheritance rule, so the merge had no signal to catch it and states the mechanism as cheap and settled.

**Proposed fix.**

In the Phase 4 steps require `app/tsconfig.negative.json` to override the inherited exclude explicitly (`"exclude": []`) alongside `"include": ["typecheck-fixtures"]`. Additionally harden `app/scripts/check-negative.mjs`: fail if the inner run's output contains `TS18003` (config resolved no inputs) and require at least one error code from the strict family the fixture targets (TS2532/TS18048 for the strictNullChecks case, TS2322 for the noUncheckedIndexedAccess case). Add that assertion to Phase 4's acceptance line for AC 11 so the criterion tests what it claims.

### [MINOR] Advancing the track README's Index row to `plan` is placed inside implementation Phase 6

- **id:** `M10` | **confidence:** high | **category:** process-misplacement
- **location:** Merged plan → phases[6].steps ("Advance the pipeline artifacts: requests/feature-requests/README.md's Index row (line 106) Stage cell to `plan` when the plan lands (and `implemented` after stage 4)"); .claude/skills/create-implementation-plan/SKILL.md:170-173

**Problem.**

SKILL.md:170-172 assigns the Index-row advance to `plan` to the stage-3 deliverable's own landing — it happens in the commit that lands IMPLEMENTATION_PLAN.md, before any implementation phase runs. Putting it in Phase 6 tells a cold implementer to set a stage cell that should already read `plan`, and blurs it with the `implemented` transition that belongs to stage 4's report. code-grounded listed it as a files_to_touch entry with no phase; domain-convention put it in Phase 6; the merge took the phase placement and kept the stage-4 parenthetical, producing a step whose owner is ambiguous.

**Proposed fix.**

Remove the Index-row step from phases[6]. Keep the files_to_touch entry for requests/feature-requests/README.md but retitle its change note: "EDIT at plan-landing time (stage 3), not during implementation — the Index row at line 106 goes to `plan` in the commit that lands IMPLEMENTATION_PLAN.md, and to `implemented` in stage 4's commit." Leave Phase 6 owning only the plan's own status blockquote if it changes.

### [MINOR] Gitleaks posture is stated three different ways across the plan

- **id:** `M11` | **confidence:** high | **category:** consistency
- **location:** Merged plan → phases[0].steps BELIEF 5 ("Either install it — a user action ... — or record honestly that CI's `Secret scan` job is the accepted gate"), gated_decisions[2] ("Accept CI as the gate"), phases[6].steps ("If gitleaks was installed in Phase 0, run it over the tree now"); PROJECT_SCOPE.md:398-406

**Problem.**

The scope's risk 5 mitigation is unambiguous: "Run gitleaks locally once before pushing." The merged plan leaves the implementer three postures — Phase 0 offers a fork with no default, the gated decision recommends accepting CI as the gate, and Phase 6 conditions a local run on a Phase 0 install the gated decision just recommended against. Re-measured here: gitleaks is not installed on this machine, and the repo has no `.gitleaks.toml` or `.gitleaksignore`. A cold agent following the phases in order gets no single answer, and the likely outcome is that neither the local run nor an explicit written deferral happens — precisely what the scope said not to do.

**Proposed fix.**

Pick one posture and make the other mentions point at it. Recommended: make gated_decisions[2] the default — CI's `Secret scan` is the accepted gate — rewrite Phase 0 BELIEF 5 to record that as decided with its evidence (`Get-Command gitleaks` empty, no `.gitleaks.toml`, no `.gitleaksignore`), and reduce Phase 6's step to "if the user installed gitleaks, run it; otherwise the PR's Secret scan is the gate and remediation is specific `.gitleaksignore` fingerprints with a written reason each".

### [MINOR] The prescribed honesty check for the CI-contexts guard cannot be run against the design the plan prescribes

- **id:** `M3` | **confidence:** high | **category:** completeness
- **location:** Merged plan → phases[3].acceptance[3] ("mutate a job's display name in a scratch COPY of ci.yml ... and confirm the comparison fails") vs phases[3].steps for tests/test_ci_contexts.py, which prescribes no injectable paths

**Problem.**

The plan deliberately makes the LAYERING guard a pure function over a directory root so both polarities are provable without touching tracked source (AC 3). It then demands the same red-proof for the CI-contexts guard — "mutate a job's display name in a scratch COPY of ci.yml" — while prescribing that guard as a test that loads the real `.github/workflows/ci.yml` and `ops/branch-protection.json` with no path parameters. As written the acceptance line is unrunnable, and the likely improvisation is the thing the plan bans everywhere else: editing the tracked workflow to watch it go red. domain-convention hedged this honestly ("verify by reasoning through the negative case, or with a tmp_path fixture pair"); code-grounded asserted the scratch-copy check; the merge kept the assertive phrasing and dropped the hedge without supplying the seam that makes it true.

**Proposed fix.**

Prescribe the same purity the layering guard gets: module-level helpers `_job_display_names(workflow: Path) -> set[str]` and `_required_contexts(protection: Path) -> set[str]`, with the real assertion calling them on the repo paths. The honesty check then becomes a tmp_path unit test in the same module — write a two-job workflow and a contexts array with one name typo'd, assert the comparison fails and names which side carries the extra. Update phases[3].acceptance[3] and the testing section's AC 4 line so both polarities run under one `uv run pytest`.

### [MINOR] Phase 0's `npm create vite@latest` step is interactive and will stall or fail in this harness

- **id:** `M4` | **confidence:** high | **category:** cost-unrealism
- **location:** Merged plan → phases[0].steps BELIEF 3 ("in the scratch dir run `npm create vite@latest` for the react-ts template, `npm install`, then `npm run build`"); mirrored in phases[4]'s scaffolding step

**Problem.**

`npm create vite@latest` with no target directory and no `--template` prompts for a project name and a framework. This environment runs PowerShell non-interactively with stdin attached to the null device, so a console prompt reads EOF and the step errors out or hangs to timeout — the first concrete command in the plan's first phase. Phase 0 is sold as "the first surprise costs a probe rather than a rewrite", so a cold agent stalling here spends the phase debugging the probe instead of the beliefs. The wording comes from the sequencing proposal; the merge carried it verbatim without adapting it to the shell it is otherwise scrupulous about (it warns repeatedly that PowerShell 5.1 has no `&&`, but says nothing about interactivity).

**Proposed fix.**

Write the non-interactive form explicitly in both places: `npm create vite@latest spa -- --template react-ts` (npm 7+ needs the `--` separator before the template flag), run from `var/spike/` in Phase 0 and as the `app/` scaffold in Phase 4. Add one line to the Phase 0 goal that every probe command must be non-interactive because stdin is null in this harness.

### [MINOR] Preflight promoted to a tracked artifact plus its own /commit — the heaviest of three variants, chosen without recording why the cheap one lost

- **id:** `M5` | **confidence:** medium | **category:** scope-creep
- **location:** Merged plan → phases[0] (entire phase, incl. commit_note) and files_to_touch entry for `requests/feature-requests/1.1-app-shell/reviews/preflight.md`; against PROJECT_SCOPE.md's Core and Folded-in lists (lines 265-346), which enumerate no such artifact

**Problem.**

Measuring the item's unconfirmed tooling beliefs is right and well-justified (CLAUDE.md's epistemics rule; the scope labels risks 4/5/6/7 inferred-or-unconfirmed). But the planners proposed three different costs: domain-convention folded the two backend probes into Phase 1 and recorded results in the commit-message body with no new tracked file; code-grounded had no preflight phase at all; sequencing proposed a standalone phase writing `reviews/preflight.md`. The merge took sequencing's, expanded it from four beliefs to six, and added a dedicated /commit checkpoint — and its decisions entry argues only FOR preflight, never that a tracked artifact plus an extra user-gated commit was the right cost. Net: one extra tracked document in `reviews/` (which the scope's Panel Trail section, line 528-534, describes as the panel's provenance trail rather than the implementer's), one more file inside tests/test_request_links.py's scan surface, and one more user interaction, none of which any acceptance criterion asks for.

**Proposed fix.**

Keep the six measurements and keep them first — that part is correct. Either (a) drop the tracked file and fold results into the Phase 1 commit body per domain-convention, deleting the Phase 0 checkpoint so the item lands in seven commits not eight; or (b) keep `reviews/preflight.md` and add a one-line justification to the decisions array for why a tracked epistemic record beats a commit-message record here (e.g. items 1.2-1.11 inherit the measurements). Either is defensible; leaving the choice unrecorded is what makes it read as smuggled.

### [MINOR] Path-traversal guard folded in from a single planner with no decision entry, and given its own acceptance line

- **id:** `M6` | **confidence:** high | **category:** scope-creep
- **location:** Merged plan → architecture_map ("a real traversal guard"), phases[2].steps item 2, phases[2].acceptance[3], and the testing section ("tests/test_api_spa.py  ACs 5, 6, 7 + the history fallback + a path-traversal guard")

**Problem.**

The decided scope's serving requirement is exactly two branches — "present → `index.html` at `/`; absent → 503 naming the build command" (PROJECT_SCOPE.md:298-301) — plus the folded-in history fallback paired with the AC 7 JSON-404 guard (line 318). Path traversal appears nowhere in the scope, which explicitly de-scopes the security surface ("Auth, users, sessions, HTTPS, multi-user, hosting", line 116). Only code-grounded proposed it; sequencing and domain-convention did not. The merge adopted it, made it a Phase 2 acceptance line and a named test case, and — unlike the `check-negative.mjs` addition, which it flags honestly as "flagged, not smuggled" — recorded no decision for it. The code is two lines and worth having; the problem is a new acceptance criterion the scope never agreed, which stage 4's panel will now be held to.

**Proposed fix.**

Keep the `candidate.is_relative_to(dist.resolve())` check in `spa.py` — cheap and correct. Demote it from an acceptance line to an implementation note inside the AC 6 step, and add a decisions entry in the same register used for check-negative.mjs: one planner proposed it, it is two lines inside a branch the scope already requires, it is not a new criterion. That keeps the acceptance panel measuring the 23 criteria the scope decided.

### [MINOR] AC 18 is declared "CI only" with no command, though `gh run list` / `gh run view` are already allowed to the agent

- **id:** `M7` | **confidence:** high | **category:** completeness
- **location:** Merged plan → testing section ("AC 18 -> CI only — the Web app job's smoke step") and phases[5].acceptance[6] ("On the pushed branch the `Web app` job reports and is green"); .claude/settings.json:32-35

**Problem.**

Phase 5's acceptance asks the implementer to confirm a pushed-branch CI result, and the testing section labels AC 18 "CI only" without naming any way to observe it — leaving a cold agent to guess, or to silently mark a core acceptance criterion unverifiable. But .claude/settings.json lines 32-35 already ALLOW `PowerShell(gh pr view *)`, `gh pr list*`, `gh run list*` and `gh run view *` unprompted, so the agent can watch its own job. All three planners cited the settings file for the `ask` list (to justify AC 23 being user-run) and none noticed the allow-list half; the merge inherited the blind spot and under-uses a capability the repo already granted.

**Proposed fix.**

Add a final Phase 5 step: after `/commit` pushes the branch, run `gh run list --branch 1.1-app-shell --limit 1` then `gh run view <id>` (allowed unprompted, .claude/settings.json:34-35) and confirm the `Web app` job and its smoke step are green; on failure read the log rather than re-pushing blind. Change the testing map's AC 18 line from "CI only" to that command pair, noting that `gh api` remains user-only (line 8) — reading a run is not applying protection.

### [MINOR] Node's major is pinned but fifteen npm packages get no version guidance, and two known major-boundary traps go unnamed

- **id:** `M8` | **confidence:** medium | **category:** cost-unrealism
- **location:** Merged plan → phases[4].steps dependency list ("Dependencies: react, react-dom. Dev: typescript, vite, @vitejs/plugin-react, @types/react, @types/react-dom, @types/node, vitest, jsdom, @testing-library/react, @testing-library/jest-dom, eslint, @eslint/js, typescript-eslint, eslint-plugin-react-hooks, globals"); contrast phases[1] ("Take version floors from what `uv lock` actually resolves; do not commit a floor nobody has seen resolve")

**Problem.**

The merge is scrupulous about Python floors and about pinning the Node major in CI (scope risk 10), then lists fifteen frontend packages as bare names. Two sit on known major boundaries a fresh `npm create vite@latest` walks into: `@testing-library/react` before v16 declares a React 18 peer and conflicts with the React 19 the current react-ts template scaffolds, and `eslint-plugin-react-hooks` before v5.2 exposes no flat-config object, so `app/eslint.config.js` cannot compose it the way the plan describes. Both surface as install-time or config-time errors naming a package rather than the version boundary — exactly the failure shape the merge already warns about for npm major skew. code-grounded raised precisely this in its open questions ("React 19 vs 18 changes the @testing-library/react major, and the Vite major changes the flat-eslint plugin set") and the merge dropped it while keeping the Python half of the same warning.

**Proposed fix.**

Add a Phase 4 step (or extend the Phase 0 BELIEF 3 record) requiring the implementer to write down the resolved majors for react, react-dom, vite, vitest, @testing-library/react, typescript-eslint and eslint-plugin-react-hooks after `npm install`, and to check two things explicitly: `@testing-library/react` major >= 16 when React is 19, and that `eslint-plugin-react-hooks` exports a flat config (falling back to manual `plugins`/`rules` wiring if not). Add a matching Phase 4 acceptance line: `npm ci` exits 0 with no peer-dependency error.

### [MINOR] The repo-relative SPA-dist default silently depends on the project being installed editable

- **id:** `M9` | **confidence:** medium | **category:** cost-unrealism
- **location:** Merged plan → phases[1].steps ("resolve the default dist from the repo root derived from `Path(__file__).resolve()`"), decisions[2], architecture_map ("`create_app()` with no argument resolves a repo-relative default")

**Problem.**

The plan's headline packaging risk is that the console script must work "on an installed environment" — the entire justification for AC 14 and tests/test_packaging.py. But the default dist location derives from `Path(__file__)`, which lands inside the repo tree only while the project is installed EDITABLE (uv's default for the root project, true under `uv run`, not true of a built wheel — which is the environment AC 14's failure story invokes). The plan asserts the mechanism three times and never states the assumption, so a cold agent debugging a 503 from an installed console script has no pointer. The scope's packaging non-goal (line 129-130, "It runs from a checkout") makes editable-only correct; the gap is that it is unstated, not that it is wrong.

**Proposed fix.**

Add one sentence to the Phase 1 step and decisions[2]: the default resolves via `Path(__file__).resolve().parents[2] / "app" / "dist"` and is correct only because uv installs the project editable from a checkout — exactly the scope's "it runs from a checkout" non-goal; a non-editable wheel gets the 503 branch, which is the designed fallback rather than a bug. State that the Phase 5 CI smoke step is the check that would catch a wrong `parents[N]`.

### [NIT] `.json` cited at tests/test_no_leaks.py line 41; it is line 42

- **id:** `M12` | **confidence:** high | **category:** citation-accuracy
- **location:** Merged plan → code_references entry for tests/test_no_leaks.py:38-55 ("TEXT_SUFFIXES contains .json (41)") and the files_to_touch entry for tests/test_no_leaks.py ("(.json is in TEXT_SUFFIXES at line 41)")

**Problem.**

Verified by reading the file: TEXT_SUFFIXES opens at line 38 and its entries run `.py` (39), `.md` (40), `.toml` (41), `.json` (42). Line 41 is `.toml`. The slip comes from the sequencing planner (code-grounded cited only the 38-55 range and was correct); the merge adopted the more precise-looking number. The surrounding claim — that tracking `app/package-lock.json` puts it inside the leak scan — is correct and load-bearing for AC 13, so the substance survives; the line number does not, and a cold implementer told to check line 41 finds `.toml` and starts doubting the rest of the citations.

**Proposed fix.**

Change both occurrences to "`.json` at line 42 (TEXT_SUFFIXES spans 38-55)", or drop the precise line and cite the range as code-grounded did.

### [NIT] "Eleven Phase-1 roadmap rows (ROADMAP.md 166-175)" — that range contains ten rows

- **id:** `M13` | **confidence:** high | **category:** citation-accuracy
- **location:** Merged plan → onboarding.what_it_is ("Eleven Phase-1 roadmap rows (ROADMAP.md 166-175) are surfaces blocked on the same missing seam") and the code_references entry for ROADMAP.md:166-175 ("The eleven downstream Phase 1 rows (1.2 through 1.11)")

**Problem.**

Verified: ROADMAP.md line 166 is row 1.2 and line 175 is row 1.11 — ten rows, not eleven. The count originates in PROJECT_SCOPE.md's Problem section (line 65) and both code-grounded and sequencing repeated it; the merge pinned it to a line range, which makes the arithmetic checkable and wrong. Harmless to the build, but the plan's credibility rests on a cold agent trusting `file:line` claims literally, and this is the one an onboarding reader can falsify in ten seconds.

**Proposed fix.**

Write "the ten downstream Phase 1 rows, 1.2 through 1.11 (ROADMAP.md:166-175)" in both places. If the intent was to include 1.1 itself, write "the eleven Phase 1 rows (165-175), ten of them downstream of this seam".

### [NIT] Phase 0's staging-cleanliness acceptance check cannot detect what it claims to

- **id:** `M14` | **confidence:** high | **category:** completeness
- **location:** Merged plan → phases[0].acceptance[1] ("`git status --porcelain --untracked-files=all` shows nothing under `var/` as a staging candidate; pyproject.toml and uv.lock are byte-identical to HEAD")

**Problem.**

`var/` is gitignored at .gitignore:18, so `git status --porcelain --untracked-files=all` never lists anything under it — that flag controls expansion of untracked DIRECTORIES, not display of ignored paths (which needs `--ignored`). The check therefore passes unconditionally and proves nothing about the probe files the phase creates, while the half that does matter (pyproject.toml and uv.lock unchanged) is buried in the same bullet.

**Proposed fix.**

Replace with two checks that can actually fail: `git status --porcelain` is empty except for the new `reviews/preflight.md`, and `git diff --stat HEAD -- pyproject.toml uv.lock` is empty (proving `uv run --with` did not touch the lock). Offer `git status --porcelain --ignored var/` as an informational command if eyeballing the probe files was the intent.

### [NIT] Decision 7's "size M is now advisory — flagged, not changed" rail was dropped in the merge

- **id:** `M15` | **confidence:** medium | **category:** completeness
- **location:** Merged plan → files_to_touch entry for ROADMAP.md and the conventions array; against PROJECT_SCOPE.md:512 (Decision 7's Consequence) and the domain-convention proposal's ROADMAP.md:165 reference

**Problem.**

Decision 7 states its consequence explicitly: ROADMAP.md sizes 1.1 as `M`, that is now advisory rather than descriptive, and it is "flagged, not changed, since `/commit` maintains status and not size". domain-convention carried this; the merge kept the guidance about the Status cell and the line-156 prose but dropped the Size-cell rail entirely. Given the merged plan is eight phases against a row marked `M` ("a day or so", ROADMAP.md:120), an implementer or a later doc sweep has an obvious incentive to "correct" the cell to `L` — a hand edit to a /commit-maintained table that the conventions forbid.

**Proposed fix.**

Add one line to the ROADMAP.md files_to_touch entry and to the conventions array: the Size cell on row 1.1 stays `M`. Decision 7 made it advisory and deliberately did not change it; /commit's mandate (commit/SKILL.md:109) covers Status cells only, so editing Size is exactly the ad-hoc table edit CLAUDE.md forbids.

### [NIT] `rpg_api` is prescribed to import pydantic directly while only fastapi is declared

- **id:** `M16` | **confidence:** medium | **category:** dependency-hygiene
- **location:** Merged plan → phases[1].steps ("a fully annotated `GET /health` returning a pydantic model `Health(status: str, version: str, spa_built: bool)`") against the same phase's pyproject.toml edit (fastapi + uvicorn only, pyproject.toml:9)

**Problem.**

The plan adds fastapi and uvicorn to `[project].dependencies` and then has `src/rpg_api/health.py` import pydantic, which arrives only transitively via fastapi. Nothing in the toolchain complains — ruff selects no such rule (pyproject.toml:40-52) and mypy resolves the installed package — so it lands silently, and a future fastapi major that changes its pydantic pin becomes an unrelated-looking breakage. It is also avoidable: the payload is three scalar fields. Related, in the same step: passing the dist "via `request.app.state` or a dependency, whichever keeps mypy strict green" leaves a known trap unnamed — starlette's `State.__getattr__` returns `Any`, so returning it straight out of a `-> Path` helper trips strict's `warn_return_any`, and AC 8 forbids the `# type: ignore` that would paper over it.

**Proposed fix.**

Either declare `pydantic` explicitly alongside fastapi in `[project].dependencies` (one more line in the single lock commit), or return a `TypedDict`/dataclass so `rpg_api` imports only what it declares. Separately add the app.state note to the Phase 1 step: bind through an annotated local (`dist: Path = request.app.state.spa_dist`), never an ignore.

### [NIT] Phase 0's mypy probe covers only the decorator friction, not the app.state/dependency path the plan actually uses

- **id:** `M17` | **confidence:** medium | **category:** completeness
- **location:** Merged plan → phases[0].steps BELIEF 2 ("Record whether `disallow_untyped_decorators` fires on `@app.get(...)`") vs phases[1].steps ("Pass the resolved dist in via `request.app.state` or a dependency, whichever keeps mypy strict green with no ignore")

**Problem.**

BELIEF 2 exists to de-risk AC 8 and probes exactly one construct — the route decorator, which scope risk 6 names as "the classic friction point". But the plan's own design introduces a second novel strict-mode surface it never probes: reading the injected dist off `request.app.state` (untyped `Any`) or wiring it through `Depends`. Since the phase's stated purpose is to convert beliefs into measurements "before any code is designed around a guess", leaving the design's other new typing construct unmeasured undercuts the phase's rationale — and the remedy space is narrow because AC 8 bans ignores and per-module overrides.

**Proposed fix.**

Extend the BELIEF 2 probe file to include both shapes the plan may use: a handler reading `request.app.state.<attr>` into an annotated local and returning it, and a `Depends(...)`-injected value, both under `mypy --strict --warn-unreachable`. Record which is clean and have Phase 1 use the measured shape rather than choosing at implementation time.

### [NIT] Scope risk 3 ("stale lockfiles, twice") is not carried as a standalone risk entry

- **id:** `M18` | **confidence:** medium | **category:** completeness
- **location:** Merged plan → risks array (21 entries; uv.lock staleness appears only inside phases[1].commit_note); PROJECT_SCOPE.md:389-391

**Problem.**

The merged risks array is otherwise an impressively complete union of the scope's 15 risks and everything the three planners raised — I found no other omission. Risk 3 is the exception: the scope pairs `uv sync --locked` hard-failing with `npm ci` failing when package.json and package-lock.json disagree, and notes "ops/README.md documents the uv rule sharply; the Node rule needs the same sharpness". The merge carries the uv half (Phase 1 commit note) and the documentation half (Phase 6 ops/README step) but never states the npm half as a risk the implementer can hit — e.g. hand-editing a script name in app/package.json after `npm install` and pushing a lock that no longer matches, which turns the new CI job red with an error naming a package.

**Proposed fix.**

Add one risk entry mirroring the scope's wording: `npm ci` fails when package.json and package-lock.json disagree, exactly as `uv sync --locked` does — so any edit to app/package.json (a script rename, a dependency bump) requires re-running `npm install` and committing the regenerated lock in the same commit. Cross-reference the Phase 4 step that generates the lock and the Phase 6 ops/README.md rule.


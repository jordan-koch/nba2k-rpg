> **Status:** preflight · created 2026-08-15 · decided · next: implement

# Preflight — App Shell (Phase 1, item 1.1)

Six beliefs gated the shape of this item. Each is measured here **before** a tracked dependency
landed, so the first surprise cost a probe rather than a rewrite. Probes ran in `var/spike/`
(gitignored at `.gitignore:18`); `uv run --with` builds an ephemeral overlay and did not touch
`uv.lock`.

Labels follow CLAUDE.md's vocabulary. **No belief is left `unconfirmed`.**

Per Decision M this file is tracked, because items 1.2–1.11 inherit these measurements rather than
re-measuring them per item.

---

## Results

| # | Belief | Was | Now | Result |
|---|---|---|---|---|
| 1 | `StaticFiles(directory=<absent>)` raises at construction | inferred | **measured** | **Confirmed** — `RuntimeError` |
| 2 | mypy strict is clean over FastAPI | unconfirmed | **measured** | **Confirmed with a constraint** |
| 3 | Vite react-ts scaffolds non-interactively; stack majors | unconfirmed | **measured** | **Confirmed, three corrections** |
| 4 | Leak regexes trip on npm artifacts | inferred | **measured** | **Refuted** — no hits |
| 5 | gitleaks trips on lockfile integrity hashes | unconfirmed | **measured** | **Refuted** — no leaks |
| 6 | Remote is `jordan-koch/nba2k-rpg` | measured | **verified** | **Confirmed** |

---

## 1 — `StaticFiles` construction · scope risk 7 · **measured**

```
absent exists? False
RAISED AT CONSTRUCTION: RuntimeError: Directory '<...>/var/spike/definitely-not-here' does not exist
check_dir=False: no raise
```

**Confirmed.** The obvious `app.mount("/", StaticFiles(directory=dist, html=True))` gives a fresh
clone an import-time traceback, which AC 5 forbids. `check_dir=False` suppresses it, but does not
address the *other* half — a mount at `/` still answers unknown `/api` paths with a non-JSON 404,
which AC 7 forbids. **Decision I stands on measurement, not inference.**

## 2 — mypy strict over FastAPI · scope risk 6 · **measured**

All three shapes pass `mypy --strict --warn-unreachable`, with one binding constraint:

| Shape | Result |
|---|---|
| (a) `@app.get(...)` on an annotated handler | clean |
| (b) `request.app.state.<attr>` → **annotated local** | clean |
| (c) `Depends(...)`-injected value | clean |
| (b′) same value **returned directly** from a `-> Path` helper | **error TS-equivalent:** `Returning Any from function declared to return "Path"  [no-any-return]` |

Measured both directions — strict enables `warn_unused_ignores`, and the ignore on (b′) was reported
as *used*, so the error is real rather than assumed.

**Constraint for Phase 1:** bind `app.state` through an annotated local. Returning it straight trips
`warn_return_any`, and the `# type: ignore` that would silence it is banned by AC 8.

## 3 — Vite toolchain · scope risk 10 · **measured**

`npm create vite@latest vite-probe -- --template react-ts` ran with **no prompts**. Build clean.
`lockfileVersion: 3`. Node **v24.15.0**, npm **11.12.1**.

`dist/` layout: `index.html` at the root, hashed bundles under `dist/assets/`, static files copied
from `public/` to the root.

**Resolved majors** — both boundaries the plan flagged are clear:

| Package | Resolved | Note |
|---|---|---|
| react / react-dom | 19.2.8 | |
| vite | 8.2.1 | |
| typescript | 6.0.2 | |
| `@vitejs/plugin-react` | 6.0.4 | |
| `@testing-library/react` | **16.3.2** | **≥ 16 boundary clear** — React 19 peer |
| `eslint-plugin-react-hooks` | **7.1.1** | flat config present — see correction B |
| eslint | 10.8.1 | |
| typescript-eslint | 8.67.0 | works against eslint 10 + TS 6 |
| vitest | 4.1.10 | |
| jsdom | 30.0.1 | |
| `@testing-library/jest-dom` | 7.0.1 | |

### Three corrections to the plan's assumptions

**A. The template now ships `oxlint`, not eslint.** `create-vite` 9.1.2 generates
`"lint": "oxlint"` and an `oxlint` devDependency. Decision 2 chose eslint + typescript-eslint +
`eslint-plugin-react-hooks` **against** the panel's oxlint recommendation, so the scaffold's linter
is removed and replaced. This is the decided call being honored, not re-opened.

**B. The flat-config key is nested.** The plan said to check that `eslint-plugin-react-hooks`
"exports a flat config object (≥ 5.2)". In **v7** the export is nested one level deeper, and the
obvious key is the *legacy* eslintrc shape:

```
configs -> [ 'recommended', 'recommended-latest', 'flat' ]
  recommended        -> legacy  { plugins: [...], rules }   <- plugins is an ARRAY of strings
  recommended-latest -> legacy  { plugins: [...], rules }
  flat               -> { 'recommended-latest', 'recommended' }
```

`configs['recommended-latest']` fails under eslint 10 with *"A config object has a `plugins` key
defined as an array of strings"*. `configs.flat` fails with *"Unexpected key
`recommended-latest`"* — it is a namespace, not a config. **The correct wiring is
`reactHooks.configs.flat.recommended`**, measured green.

**C. The template's tsconfig sets no `strict` flag.** `create-vite` generates a three-file project-
reference split (`tsconfig.json` → `tsconfig.app.json` + `tsconfig.node.json`), and the app config
carries `noUnusedLocals` / `noUnusedParameters` / `erasableSyntaxOnly` /
`noFallthroughCasesInSwitch` but **no `strict` and no `noUncheckedIndexedAccess`**. This is exactly
the "default-generated config that checks nothing" AC 11 exists to rule out. Decision H's single
config sets both explicitly.

The template's `"build": "tsc -b && vite build"` is the `&&` shape risk 10 warns about — broken on
PowerShell 5.1. Replaced with separate scripts, per the plan.

### 3b — the strict-family error codes · **measured**

AC 11's checker asserts on specific codes, and the plan's were inferred. Measured under TS 6.0.2
against `strict: true` + `noUncheckedIndexedAccess`:

```
bad.ts(6,10): error TS18048: 's' is possibly 'undefined'.
bad.ts(11,3): error TS2322: Type 'string | undefined' is not assignable to type 'string'.
EXIT=2
```

**The plan's inferred codes are correct** — TS18048 for the `strictNullChecks` case, TS2322 for the
`noUncheckedIndexedAccess` case, non-zero exit. `check-negative.mjs` asserts these.

## 4 — leak regexes on npm artifacts · scope risk 4 · **measured → refuted**

The three shipped patterns, imported from `tests/test_no_leaks.py` itself rather than copied, run
against the probe's real artifacts:

```
=== package.json (823 bytes) ===      WINDOWS_PATH: 0   POSIX_HOME: 0   EMAIL: 0
=== package-lock.json (145,233 bytes) === WINDOWS_PATH: 0   POSIX_HOME: 0   EMAIL: 0
```

**Refuted — no `ALLOWED` entry is needed.** The known EMAIL tripwire is the npm `author` field,
which the template does not generate and which the plan forbids anyway. `lockfileVersion: 3` embeds
resolved registry URLs and integrity hashes, not local paths.

This does **not** retire the pre-staging gate: `tests/test_no_leaks.py` reads the git **index**
(docstring, lines 12–13), so the AC 13 run still happens after `git add --intent-to-add`.

## 5 — gitleaks · scope risk 5 · **measured → refuted**

Decision B's `winget install gitleaks.gitleaks` was already done — **gitleaks 8.30.1** is on PATH.
Measured two ways, because the first result was a false green:

1. `gitleaks dir` pointed inside `var/spike/` reported *"scanned ~0 bytes"* — it honors
   `.gitignore`, so it silently scanned nothing. **A pass here would have meant nothing.**
2. Re-run against a copy outside any ignore rule: 823 bytes scanned — `package.json` only. The
   145 KB lockfile was skipped **by filename**, via gitleaks' default path allowlist.
3. Re-run with the lockfile **renamed** to defeat that allowlist: 146 KB scanned in full,
   **no leaks found**.

**Refuted on both paths.** The sha512 integrity strings do not trip gitleaks even when force-
scanned, so no `.gitleaksignore` and no fingerprints are needed. Risk 17 (npm supply-chain exposure)
is unaffected and stands as recorded.

## 6 — the remote · scope risk 1 · **verified**

```
origin  https://github.com/jordan-koch/nba2k-rpg.git (fetch)
origin  https://github.com/jordan-koch/nba2k-rpg.git (push)
```

Matches `ops/README.md` lines 12 and 29, so AC 23's `gh api -X PUT` target is correct as written. No
`gh api` was run — it is in the ask list at `.claude/settings.json:8`, and stays the user's step.

**Still unconfirmed, deliberately:** whether GitHub's protection API accepts the current
`ops/branch-protection.json` unchanged. Only the user can test that, and it is AC 23 step 2.

---

## What this changes downstream

- **Decision I** (no `StaticFiles`) is now measured, not inferred.
- **Phase 1** must bind `app.state` through an annotated local.
- **Phase 4** removes the scaffold's `oxlint`, wires `reactHooks.configs.flat.recommended`, and sets
  `strict` explicitly because the template does not.
- **No `ALLOWED` entry and no `.gitleaksignore`** are needed for the frontend files.
- **`actions/setup-node` is v7 — CONFIRMED**, closing Decision E. Checked against the marketplace
  releases page before the Phase 5 commit (latest release v7.0.0), then **exercised**: the `Web app`
  job's *Set up Node* step resolved v7 and installed node v24.19.0 on the first green CI run. This
  was the plan's last claim carrying an `unconfirmed` label; nothing in this item is now unmeasured.
  Notable because v7 is well ahead of the v4 most examples still show — consistent with this repo
  already pinning `checkout@v5` and `setup-uv@v6`.

**Also settled after the fact:** GitHub's protection API accepts
`ops/branch-protection.json` unchanged. The `gh api -X PUT` re-apply returned
`{Lint, types, tests, Secret scan, Web app}` with `strict: true`, which was belief 6's deliberate
carve-out and could only ever be tested by running it.

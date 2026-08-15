# Ops

Repo governance as code. Nothing here runs automatically — these are user-run
actions, deliberately, because they change repository settings rather than code.

## Branch protection

[`branch-protection.json`](branch-protection.json) is the intended protection
ruleset for `main`. Apply it with:

```powershell
gh api -X PUT repos/jordan-koch/nba2k-rpg/branches/main/protection `
  --input ops/branch-protection.json
```

**Apply it after the first push, not before** — protection with
`enforce_admins: true` blocks the initial direct push to `main` that creates the
branch in the first place.

> **Renaming *or adding* a CI job silently breaks this.** The `contexts` array
> matches job **display names** from
> [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) — currently
> `Lint, types, tests`, `Secret scan`, and `Web app`. Rename one, or add a job
> without adding its context, and PRs wait forever for a check that never
> reports, with no error explaining why. Change both in the same commit.
>
> `tests/test_ci_contexts.py` now enforces exactly that, asserting **set
> equality** between the two files — but it can only see the *tracked* half.

> **This file is inert until it is re-applied.** Editing `branch-protection.json`
> changes nothing on GitHub. The rule on the server only moves when somebody runs
> the `gh api -X PUT` command above, and an agent structurally cannot: `gh api *`
> sits in `.claude/settings.json`'s `ask` list. When a commit adds a job, the
> order matters — let the new check report once on the open PR, re-apply this
> file, confirm the check shows as **Required**, and only then merge. Re-applying
> afterwards guarantees the PR that introduced the job is exactly the one that
> could have landed with it red.

To read back what's actually applied:

```powershell
gh api repos/jordan-koch/nba2k-rpg/branches/main/protection
```

## Local toolchain

`uv` is the package manager, matching CI. Install it once:

```powershell
winget install --id=astral-sh.uv -e
```

winget drops shims in `%LOCALAPPDATA%\Microsoft\WinGet\Links`, which is already on
`PATH` — but **an already-open shell won't see them**. Open a new terminal after
installing, or prepend the directory for the current session:

```powershell
$env:Path = "$env:LOCALAPPDATA\Microsoft\WinGet\Links;$env:Path"
```

Then create the environment from the committed lockfile:

```powershell
uv sync
```

**`uv.lock` is tracked**, and CI installs with `uv sync --locked` — a stale or
missing lockfile fails the build rather than silently re-resolving. Changing
anything in `pyproject.toml`'s dependencies means running `uv lock` and committing
the result in the same commit as the change.

> **Harmless warning on this machine.** If the repo and uv's cache sit on different
> drives, `uv sync` reports *"Failed to hardlink files; falling back to full copy."*
> It is a speed note, not an error. Silence it with `UV_LINK_MODE=copy` if it gets
> annoying.

## Node toolchain

The web app lives in `app/` and every one of its config files is scoped to that
directory — there is deliberately no eslint or tsconfig at the repo root.

Measured on the development machine: **node v24.15.0, npm 11.12.1**. CI pins
node 24 to match. Install once:

```powershell
winget install --id=OpenJS.NodeJS.LTS -e
```

Then, from `app/`:

```powershell
npm ci
```

**`app/package-lock.json` is tracked**, and both CI and the command above install
with `npm ci` — which **fails when `package.json` and `package-lock.json`
disagree**, exactly as `uv sync --locked` does for the Python half. This is the
same rule stated for the other toolchain: any edit to `app/package.json` — a
script rename, a dependency bump, a new devDependency — means running
`npm install` and committing the regenerated lockfile **in the same commit**. Skip
it and CI goes red with an error naming some package, which reads like a broken
dependency rather than the lockfile skew it actually is.

## Running the checks locally

The same four Python commands CI runs, in the same order:

```powershell
uv run ruff check
uv run ruff format --check
uv run mypy
uv run pytest
```

`uv run` syncs the environment first, so there is nothing to activate.

And the five frontend commands, from `app/` — these *are* the `Web app` job's
steps, so a green run here predicts a green run there:

```powershell
npm run typecheck
npm run check:negative
npm run lint
npm run test
npm run build
```

`npm run typecheck` is separate from `npm run build` on purpose: **`vite build`
does not typecheck** — esbuild strips types without checking them — so a green
build proves nothing about types. Never fold them back together.

`npm run check:negative` is the inverted one. It compiles a deliberately
ill-typed fixture and **passes only when that compilation fails**, which is what
proves `strict` is genuinely engaged rather than a generated config that checks
nothing. To assert it by hand in PowerShell (which cannot negate an exit code
inline):

```powershell
npm run typecheck:negative
if ($LASTEXITCODE -eq 0) { Write-Error "strict is NOT engaged — the bad fixture compiled" }
```

Without `uv`, the tests alone will run under a plain interpreter — `pythonpath`
in `pyproject.toml` exists for exactly this. Lint and types will not.

```powershell
python -m pytest
```

## Running the app

Two modes, and they are genuinely different things.

**Dev — two terminals.** Vite serves the frontend with hot reload and proxies
`/api` to uvicorn, so both halves are same-origin and no CORS middleware exists
anywhere in the stack.

```powershell
uv run uvicorn rpg_api.app:create_app --factory --reload --host 127.0.0.1 --port 8000
```

```powershell
npm run dev     # from app/
```

Deliberately two commands rather than one launcher: a Node process-runner
receiving Ctrl+C in PowerShell can orphan the Python child still holding port
8000, and the next run then dies with `EADDRINUSE` pointing at nothing useful.
`watchfiles` is in the dev dependency group to make `--reload` fast; that is its
whole purpose.

**Served — one command, and this is the only documented way to run it.**

```powershell
uv run rpg-serve
```

That serves the built SPA and the API from a single origin on
`http://127.0.0.1:8000`. It needs a build first (`npm run build` from `app/`); if
there isn't one, the page returns a 503 that says so and names the command,
rather than a confusing 404. The build can be run while the server is up — the
page starts working on the next reload, with no restart needed.

The API port is hardcoded in exactly two places — `src/rpg_api/serve.py` and the
proxy target in `app/vite.config.ts`. Those are the pair that must stay in step,
and both use the IPv4 literal `127.0.0.1` rather than `localhost`, because Node
on Windows can resolve `localhost` to `::1` while uvicorn binds IPv4 and the
resulting connection error looks exactly like a dead backend.

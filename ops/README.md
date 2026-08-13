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

> **Renaming a CI job silently breaks this.** The `contexts` array matches job
> **display names** from [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
> — `Lint, types, tests` and `Secret scan`. Rename one without updating this file
> and PRs wait forever for a check that never reports, with no error explaining
> why. Change both in the same commit.

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

## Running the checks locally

The same four commands CI runs, in the same order:

```powershell
uv run ruff check
uv run ruff format --check
uv run mypy
uv run pytest
```

`uv run` syncs the environment first, so there is nothing to activate.

Without `uv`, the tests alone will run under a plain interpreter — `pythonpath`
in `pyproject.toml` exists for exactly this. Lint and types will not.

```powershell
python -m pytest
```

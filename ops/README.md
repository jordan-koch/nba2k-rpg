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

`uv` is the package manager, matching CI. It is **not currently installed on the
dev machine**. Install it once:

```powershell
winget install --id=astral-sh.uv -e
```

Then generate and commit the lockfile:

```powershell
uv lock
uv sync
```

**Once `uv.lock` is committed, flip CI's install step from `uv sync` to
`uv sync --locked`** (see the TODO in `ci.yml`). Until then CI resolves fresh on
every run, which works but isn't reproducible.

## Running the checks locally

```powershell
uv run ruff check
uv run ruff format --check
uv run mypy
uv run pytest
```

Without `uv`, the tests alone will run under a plain interpreter:

```powershell
python -m pytest
```

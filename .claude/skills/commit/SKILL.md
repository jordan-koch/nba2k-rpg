---
name: commit
description: >-
  Stage the current work, check the docs still describe it, show you exactly what's about to land,
  and commit once you say yes. This is the ONLY sanctioned path by which an agent commits in this
  repo — never run `git commit` ad hoc. Use it whenever a unit of work is finished: "commit this",
  "commit the changes", "let's land this", "/commit", or as the natural end of a pipeline stage.
  It stages deliberately (never a blind `git add -A`), refuses to stage secrets or bulk data, runs
  the doc-drift checks proportionally to what changed, keeps `ROADMAP.md`'s per-item completion
  statuses in step with what actually landed, surfaces any parked escalation entries against a row
  it is closing, proposes a message, and asks before writing anything.
  On approval it commits and pushes the feature branch. It does NOT open the PR, never pushes
  `main`, and never force-pushes — those stay yours. It does NOT run lint, types, tests; CI owns
  those and runs them on the PR.
---

# Commit

## What this produces and why

One commit, on a branch, containing exactly what you meant to land — after the docs have been
checked against it and you've seen the staged list.

The rule this replaces was "agents never commit," which was correct about the risk and wrong about
the friction. The actual hazard isn't an agent committing; it's an agent committing **something you
didn't see**: a stray credential, a 400MB Parquet file, a half-finished refactor swept up by
`git add -A`. So the guard is *deliberate staging plus an explicit yes*, not a blanket prohibition.

**Keep this skill lightweight.** It is a gate, not a pipeline. If it grows a panel, something has
gone wrong.

---

## Step 1 — Survey

```
git status --porcelain --untracked-files=all
git diff HEAD --stat
git branch --show-current
```

**Read the actual diff**, not just the file list. You're about to describe it in a commit message,
and a message that misdescribes its diff is worse than no message.

**Branch check.** If the current branch is `main`, say so and stop for a decision. `main` is
protected and work is supposed to land by PR. Offer to create a branch — `git switch -c
<descriptive-slug>` — and note that this is cheap now and annoying later. Proceed on `main` only if
the user explicitly says to.

## Step 2 — Stage deliberately

**Never `git add -A` or `git add .` without reading the untracked list first.** That single habit
is the one this skill exists to prevent.

Go through the untracked and modified files and decide, per file, whether it belongs in this
commit. Then stage by path.

**Refuse to stage** any of these, and say why rather than staging quietly:

| Refuse | Because |
|---|---|
| Anything under `var/` | Gitignored working root — regenerable, machine-local |
| `.env`, `*.pem`, `*.key`, credentials | This repo is **public**; a leaked secret is permanent in history |
| `*.parquet`, `*.sqlite`, `*.db` outside `tests/fixtures/` | The repo holds code, config and the career ledger — not bulk data |
| `var/`, `node_modules/`, `.venv/`, `__pycache__/` | Generated or machine-local |
| Anything you can't explain the presence of | If you don't know why it changed, neither will the reviewer |

Most of these are already in `.gitignore`. If one shows up as untracked anyway, that's a
`.gitignore` gap worth fixing in this same commit — say so.

Then sanity-check what you staged:

```
git diff --cached --stat
```

Scan the staged diff for anything that looks like a credential, an account ID, a bucket name, or a
connection string. `gitleaks` will catch it in CI, but catching it *before* it enters history is
the difference between an edit and a history rewrite.

## Step 3 — Doc drift, proportional to the change

Run the checks in proportion to what actually changed — this is the step that keeps the gate
lightweight.

**Run the full [`/update-docs`](../update-docs/SKILL.md) sweep** when the change touches anything
the docs describe:

- a new or changed directory (the `CLAUDE.md` project map)
- a new convention, constraint, or gotcha (the rules sections)
- a new dataset, external source, or a changed grain (dataset docs, and its manifest entry)
- a completed phase or a changed setup step (`README.md`)
- anything contradicting an accepted ADR
- a source claim that moved from `unconfirmed` to `verified` (`docs/data-access.md`)
- a request artifact whose status advanced (the track Index rows)

**Otherwise, do the two-minute version yourself:**

```
uv run pytest tests/test_request_links.py -q
```

plus a read of `CLAUDE.md`'s project map against the tree. A typo fix in a test does not need the
full sweep, and pretending it does is how a gate becomes something people route around.

If `/update-docs` flags something needing your judgment — a superseded ADR, a grain/test mismatch —
**stop and surface it.** Those are not commit-blockers by policy, but they're decisions, and a
commit is a bad place to make one silently.

## Step 4 — Roadmap status

`ROADMAP.md` carries a **Status** column on every phase item — `NOT STARTED` ·
`IN-PROGRESS` · `DONE` — plus an aggregate on each phase header. **This skill owns
keeping those true.** Nowhere else in the pipeline is guaranteed to run at the moment work
actually lands, so if the gate doesn't advance them, they rot.

Check the staged diff against the roadmap rows and update in the same commit:

| Signal in the diff | Status becomes |
|---|---|
| First commit toward an item — partial deliverable, scaffolding, a `requests/` artifact opened for it | `IN-PROGRESS` |
| The item's **Deliverable** column is fully satisfied by what's now in the tree | `DONE` |
| Nothing matches a roadmap row | Leave every status alone |

**Match on the deliverable, not the branch name.** A branch called `app-shell` that only lands a
`FEATURE_REQUEST` has started 1.1, not finished it. Read the Deliverable cell and ask whether the
tree now contains all of it.

**Phase headers are derived, not independent.** A phase goes `IN-PROGRESS` when any item is, and
`DONE` only when *every* item is `DONE` **and** the phase's stated **Exit** condition has actually
been met — the exit is a separate claim from the item list and is often the thing not yet true.
When you mark a phase `DONE`, stamp the date on its `**Status:**` line.

Three rails, because this column is a record rather than a plan:

- **Never mark ahead.** An item is `DONE` when the commit that completes it is being made, not when
  a plan says it will be.
- **Never mark down silently.** If work already recorded as `DONE` looks regressed or reverted,
  stop and surface it. Walking a status backwards is a decision, not bookkeeping.
- **Before flipping a row to `DONE`, surface open entries naming it.** Check
  [`ESCALATIONS.md`](../../../ESCALATIONS.md) for open entries whose `Bears on:` names that item —
  **or, when you are marking a phase header `DONE`, that phase name** — and report them. Closing
  the row is the moment they stop being findable. Surface only; nothing here blocks the commit, and
  no agent resolves an entry.

If the change is a doc edit, a typo fix, or otherwise maps to no roadmap row, say "no roadmap
change" and move on. Most commits are this.

Stage `ROADMAP.md` by path if you edited it — the status belongs in the same commit as the work it
describes, not in a tidy-up commit afterwards.

## Step 5 — Propose, then ask

Show the user four things:

```
STAGED    — the file list, grouped by area, with the stat line
DOCS      — what the drift check did: updated / flagged / clean
ROADMAP   — which items moved, and to what — or "no roadmap change"
MESSAGE   — the proposed commit message
```

**Message format:** an imperative subject line under ~72 characters saying what the commit *does*,
and — when the change isn't self-evident — a body explaining *why*, wrapped at 72. The diff already
shows what changed; the body is for what the diff can't say.

```
Add career ledger fold and replay-determinism test

The bulk endpoint returns a full season per call, so the backfill is ~50
requests rather than ~60k. Fixtures cover 2019-20 (bubble) and 2011-12
(lockout) since both break the 82-game assumption.
```

Then **ask, explicitly, and wait.** Not a rhetorical "shall I commit?" trailing a wall of text — a
real question with the staged list visible above it. The user's yes is the gate.

That one yes covers **commit and push** (Steps 6 and 7). Say so when you ask, so the scope of the
approval is on screen rather than assumed.

## Step 6 — Commit

On approval, **write the message to a file and commit with `-F`.** Not `-m`:

1. Write the full message — subject, blank line, body — to `var/commit-msg.txt` **using the `Write`
   tool**, not a shell redirect.
2. ```
   git commit -F var/commit-msg.txt
   ```
3. Delete the file. `var/` is gitignored, so a leftover is harmless, but a stale message is a trap
   for the next run.

**Why not `-m`.** Windows PowerShell 5.1 rebuilds the argument list for native executables, and a
double quote *inside* a here-string or a quoted `-m` argument terminates the argument early. A
message containing `"..."`, a backtick, or a token that looks like a switch gets split, and git
receives the fragment as a flag — the observed failure was ``unknown switch `D'`` from a body that
mentioned `-D`. It fails loudly rather than committing something wrong, but it fails every time and
the workaround is not obvious mid-commit.

**Why the `Write` tool and not `Out-File`/`Set-Content`.** Both default to UTF-8 **with a BOM** in
PowerShell 5.1, and git copies the BOM into the message as literal leading characters. `Write`
emits UTF-8 without one, so em-dashes and accented names survive intact.

`var/commit-msg.txt` is repo-relative on purpose. Never write an absolute path into a tracked file —
`tests/test_no_leaks.py` fails the build on drive letters and home directories, and this repo is
public.

Hard rails, no exceptions without an explicit request:

- **Never `--no-verify`.** If a hook fails, that's the hook working.
- **Never `--amend`.** Amending rewrites history that may already be pushed. A follow-up commit is
  almost always right; if the user genuinely wants an amend, they'll say so.
- **Never `-A` at this stage.** Staging happened in Step 2, deliberately — plus the doc and
  roadmap files you edited in Steps 3–4, staged by path.

## Step 7 — Push the branch

The user's yes in Step 5 covers the commit **and** pushing it. Push without asking again:

```
git push -u origin <branch>
```

`-u` on the first push of a branch, plain `git push` after. Then report the short SHA and the
PR-creation URL the remote hands back.

Three limits, and they are not negotiable without an explicit request:

- **Never push `main`.** If Step 1 was overridden and the commit landed on `main`, stop here and
  hand the command back. Protection will reject it anyway; better to say so than to generate a
  confusing rejection.
- **Never force-push.** Not `--force`, not `--force-with-lease`. Rewriting published history is the
  user's call, always.
- **Never open the PR.** Push, then hand over the URL. Opening it — title, body, reviewers — is a
  judgment call the user makes.

Pushing runs CI only if a PR exists; a first push to a fresh branch triggers nothing, because the
workflow fires on `pull_request` and on `push` to `main`. Say so rather than leaving the user
watching for a run that will never start.

---

## What good looks like

- **Nothing landed that the user didn't see.** The staged list was shown before the yes, not after.
- **Staging was per-path, not wholesale.** `git add -A` appears nowhere in the transcript.
- **The message describes the diff.** Someone reading `git log` in six months learns why, not just
  what.
- **The doc check was sized to the change.** Full sweep on a new model; link check on a typo fix.
- **`ROADMAP.md` still describes reality.** An item that finished is `DONE` in the same commit that
  finished it — never marked ahead of the work, never walked backwards without asking.
- **It committed, pushed the branch, and stopped there.** No PR, no merge, no amend, no
  force-push, no `--no-verify`.

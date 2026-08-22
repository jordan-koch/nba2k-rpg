"""Link-drift guard for process artifacts and the root documents.

Requests, plans, reports, and skills are read by cold agents that follow their pointers.
A dead relative link doesn't fail loudly — it silently sends the next stage somewhere
that doesn't exist, and the agent invents something plausible instead. So links are
checked mechanically.

The root `*.md` documents are scanned for the same reason: they are the first thing
an agent onboarding to this repo reads, so a pointer that rots there misdirects
every stage downstream of it. They are globbed non-recursively — see `_scanned_files`
for why that is not the same as adding the repo root to `SCANNED_TREES`.

Exempt, deliberately:
  - fenced code blocks, so an artifact can quote a dead or forward-referenced path
  - `<placeholder>` targets, so a skill can show the shape of a link it tells you to write
  - `var/` targets, which are gitignored and machine-local
  - absolute URLs and bare `#anchors`

Archived (`_done/`) artifacts are skipped: they describe the repo as it was, and
rewriting history to satisfy a link checker would destroy the provenance trail.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNED_TREES = (REPO_ROOT / "requests", REPO_ROOT / ".claude" / "skills")

FENCED_BLOCK = re.compile(r"^([ \t>]*)(`{3,}|~{3,}).*?^\1\2.*?$", re.DOTALL | re.MULTILINE)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
LINE_SUFFIX = re.compile(r":\d+(-\d+)?$")


def _scanned_files() -> list[Path]:
    files: list[Path] = []
    for tree in SCANNED_TREES:
        if not tree.is_dir():
            continue
        files.extend(p for p in tree.rglob("*.md") if "_done" not in p.parts)

    # Root documents, globbed NON-recursively and deliberately kept out of
    # SCANNED_TREES: that loop calls rglob() per entry, so REPO_ROOT added there
    # would sweep app/node_modules/, .venv/ and var/. (The `_done` exemption is
    # not a reason — the loop above already filters it, and this glob is one
    # level deep, so it cannot reach a `_done/` tree at all.)
    #
    # This is a filesystem glob rather than a `git ls-files` read, unlike the
    # sibling guard in tests/test_no_leaks.py. Accepted deliberately: it keeps
    # the module subprocess-free, and the cost is that untracked scratch
    # markdown left at the repo root is scanned too — a confusing local red at
    # worst, never a missed defect.
    files.extend(REPO_ROOT.glob("*.md"))

    return sorted(set(files))


def _dead_links(path: Path) -> list[str]:
    body = FENCED_BLOCK.sub("", path.read_text(encoding="utf-8"))
    dead: list[str] = []

    for raw_target in MARKDOWN_LINK.findall(body):
        # Strip an optional link title: [text](path "Title")
        target = raw_target.split()[0].strip()

        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # `[<slug>](<slug>/)` — a template showing the shape of a link, not a link.
        if "<" in target and ">" in target:
            continue
        # Drop an anchor fragment, then a `file.py:123` citation suffix.
        target = target.split("#", 1)[0]
        if not target:
            continue
        target = LINE_SUFFIX.sub("", target)
        if target.startswith("var/") or "/var/" in target:
            continue

        if not (path.parent / target).resolve().exists():
            dead.append(raw_target)

    return dead


def test_the_root_documents_are_actually_scanned() -> None:
    """The guard on the guard.

    The test below asserts only that whatever was scanned had no dead links —
    which passes just as happily over silence. If the root glob ever stopped
    matching, AC 18's added coverage would evaporate with no signal at all.
    """
    scanned = {path.name for path in _scanned_files() if path.parent == REPO_ROOT}

    assert {"CLAUDE.md", "README.md", "ROADMAP.md", "ESCALATIONS.md"} <= scanned, (
        f"Root documents missing from the scan set: {sorted({'CLAUDE.md', 'README.md', 'ROADMAP.md', 'ESCALATIONS.md'} - scanned)}"
    )


def test_process_artifacts_have_no_dead_relative_links() -> None:
    failures = {
        str(path.relative_to(REPO_ROOT)): dead
        for path in _scanned_files()
        if (dead := _dead_links(path))
    }

    assert not failures, "Dead relative links in process artifacts:\n" + "\n".join(
        f"  {file}: {targets}" for file, targets in sorted(failures.items())
    )

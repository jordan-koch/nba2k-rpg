"""Structural guards.

These assert that the repo's configuration and its filesystem agree. They exist
because this repo is written mostly by agents against docs treated as
authoritative — so a document claiming a thing that doesn't exist, or a thing
nobody documented, is a real failure mode rather than a theoretical one.

Cheap, fast, and they run on every PR.
"""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUEST_TRACKS = ("feature-requests", "bugfix-requests", "calibration-findings")
ADR_FILENAME = re.compile(r"^(\d{4})-[a-z0-9-]+\.md$")


def _git_check_ignore(relative_path: str) -> bool:
    """True if git would ignore `relative_path`. Works on paths that don't exist."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--no-index", relative_path],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    # 0 = ignored, 1 = not ignored, 128 = not a git repo / git unavailable.
    if result.returncode == 128:
        raise RuntimeError("git check-ignore unavailable")
    return result.returncode == 0


# ─── Package ──────────────────────────────────────────────────────────────────


def test_package_imports_and_declares_a_version() -> None:
    import rpg_core

    assert rpg_core.__version__


def test_package_version_matches_pyproject() -> None:
    import rpg_core

    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        pyproject = tomllib.load(fh)

    assert rpg_core.__version__ == pyproject["project"]["version"], (
        "src/rpg_core/__init__.py and pyproject.toml disagree about the version."
    )


# ─── The one inverted convention ──────────────────────────────────────────────


def test_career_ledger_is_not_gitignored() -> None:
    """The career ledger MUST be tracked.

    The 2K save file is encrypted, so there is no upstream to re-ingest a career
    from — `careers/<slug>/events.jsonl` is the only copy that will ever exist.
    A blanket `*.jsonl` or `careers/` rule in .gitignore would silently stop
    backing up the single most irreplaceable thing in the repo, and nothing else
    would complain. See ADR 0003.
    """
    try:
        ignored = _git_check_ignore("careers/example-career/events.jsonl")
    except RuntimeError:
        import pytest

        pytest.skip("git unavailable")

    assert not ignored, (
        "careers/**/events.jsonl is gitignored. The career ledger has no upstream "
        "and cannot be regenerated — it must be tracked. Check .gitignore for a "
        "blanket *.jsonl rule shadowing the carve-out."
    )


def test_scratch_root_is_gitignored() -> None:
    """The mirror of the rule above: var/ holds only regenerable things."""
    try:
        ignored = _git_check_ignore("var/cache/anything.json")
    except RuntimeError:
        import pytest

        pytest.skip("git unavailable")

    assert ignored, "var/ must be gitignored — it holds caches and the rebuildable read-model."


# ─── Process artifacts ────────────────────────────────────────────────────────


def test_every_request_track_exists_and_documents_itself() -> None:
    missing = [
        track
        for track in REQUEST_TRACKS
        if not (REPO_ROOT / "requests" / track / "README.md").is_file()
    ]
    assert not missing, f"Request track(s) missing a README.md: {missing}"


def test_request_tracks_readme_links_every_track() -> None:
    body = (REPO_ROOT / "requests" / "README.md").read_text(encoding="utf-8")
    unlinked = [track for track in REQUEST_TRACKS if f"{track}/" not in body]
    assert not unlinked, f"requests/README.md does not link track(s): {unlinked}"


def test_every_adr_is_listed_in_the_index() -> None:
    """An ADR nobody can find from the index may as well not have been written."""
    decisions = REPO_ROOT / "docs" / "decisions"
    index = (decisions / "README.md").read_text(encoding="utf-8")

    on_disk = {p.name for p in decisions.glob("*.md") if ADR_FILENAME.match(p.name)}
    unlisted = sorted(name for name in on_disk if name not in index)

    assert not unlisted, f"ADR(s) absent from docs/decisions/README.md index: {unlisted}"


def test_adr_numbers_are_unique_and_contiguous() -> None:
    decisions = REPO_ROOT / "docs" / "decisions"
    numbers = sorted(
        int(match.group(1))
        for p in decisions.glob("*.md")
        if (match := ADR_FILENAME.match(p.name))
    )

    assert numbers, "No ADRs found."
    assert len(numbers) == len(set(numbers)), f"Duplicate ADR numbers: {numbers}"
    assert numbers == list(range(1, len(numbers) + 1)), (
        f"ADR numbers must run 1..N with no gaps; found {numbers}"
    )


def test_core_documents_exist() -> None:
    """The three documents that carry the design, each doing one job."""
    for name in ("GAME_DESIGN.md", "ROADMAP.md", "DESIGN.md", "README.md", "CLAUDE.md"):
        assert (REPO_ROOT / name).is_file(), f"{name} is missing."

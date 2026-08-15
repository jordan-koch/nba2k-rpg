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


def test_web_app_build_output_is_ignored_but_sources_are_not() -> None:
    """The frontend's generated output stays out; its sources stay in.

    The assertion that actually protects something is the **negative** one.
    `.gitignore` lines 62-63 blanket-match `dist/` and `build/` at *any* depth,
    so a source file landing under a directory with either name inside `app/`
    would be silently untracked with nothing complaining — the same class of
    silent shadowing the career-ledger carve-out above exists to prevent.

    Note `app/dist/` is covered twice, by the blanket `dist/` rule and by its
    own entry, so this test passing does NOT prove the explicit entry survives.
    """
    try:
        generated = {
            "app/dist/index.html": _git_check_ignore("app/dist/index.html"),
            "app/node_modules/react/index.js": _git_check_ignore("app/node_modules/react/index.js"),
        }
        sources = {
            "app/src/main.tsx": _git_check_ignore("app/src/main.tsx"),
            "app/package.json": _git_check_ignore("app/package.json"),
            "app/vite.config.ts": _git_check_ignore("app/vite.config.ts"),
        }
    except RuntimeError:
        import pytest

        pytest.skip("git unavailable")

    assert all(generated.values()), (
        f"Build output must be gitignored: {sorted(k for k, v in generated.items() if not v)}"
    )
    assert not any(sources.values()), (
        "Frontend SOURCE files must be tracked, but git ignores: "
        f"{sorted(k for k, v in sources.items() if v)}. Check .gitignore for a "
        "blanket dist/ or build/ rule shadowing them — those match at any depth."
    )


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
    matches = (ADR_FILENAME.match(p.name) for p in decisions.glob("*.md"))
    numbers = sorted(int(m.group(1)) for m in matches if m)

    assert numbers, "No ADRs found."
    assert len(numbers) == len(set(numbers)), f"Duplicate ADR numbers: {numbers}"
    assert numbers == list(range(1, len(numbers) + 1)), (
        f"ADR numbers must run 1..N with no gaps; found {numbers}"
    )


def test_core_documents_exist() -> None:
    """The three documents that carry the design, each doing one job."""
    for name in ("GAME_DESIGN.md", "ROADMAP.md", "DESIGN.md", "README.md", "CLAUDE.md"):
        assert (REPO_ROOT / name).is_file(), f"{name} is missing."


# ─── Documentation ────────────────────────────────────────────────────────────
# "The docs describe the application that exists" is otherwise a goal with no
# pass/fail check at all, which means it rots the first time somebody is in a
# hurry. These are cheap substring assertions in the same idiom as the rest of
# this module.


def _read(name: str) -> str:
    return (REPO_ROOT / name).read_text(encoding="utf-8")


def test_no_document_still_claims_there_is_no_application() -> None:
    """Compared LOWERCASED, and that is not incidental.

    README.md capitalized the N in "No application code yet" and CLAUDE.md did
    not, so a case-sensitive check would silently pass on one of the two while
    the other kept lying.
    """
    stale = "no application code yet"

    for name in ("README.md", "CLAUDE.md"):
        assert stale not in _read(name).lower(), (
            f"{name} still says there is no application code, but src/rpg_api/ "
            "and app/ both exist and run."
        )


def test_claude_md_project_map_lists_both_new_directories() -> None:
    body = _read("CLAUDE.md")

    for path in ("src/rpg_api/", "app/"):
        assert path in body, (
            f"CLAUDE.md's project map does not mention {path}. An agent "
            "onboarding from it would not know the directory exists."
        )


def test_index_stage_cells_match_their_artifact_status_headers() -> None:
    """The Index and the artifacts must not disagree about what stage an item is at.

    They did once: the Index said `planned` and every artifact header agreed,
    while ROADMAP.md said `DONE` and the item had in fact shipped. A cold agent
    reading requests/ would have concluded 1.1 was planned-but-unbuilt.

    Nothing caught it — test_request_links only checks that links resolve, and
    the Documentation assertions above deliberately do not reach the Index. So
    this closes the gap in the same read-and-assert idiom.
    """
    stage_cell = re.compile(r"^\|\s*\[(?P<slug>[^\]]+)\]\((?P<link>[^)]+)\)\s*\|\s*(?P<stage>\w+)")
    status_header = re.compile(r"^>\s*\*\*Status:\*\*\s*(?P<stage>\w+)", re.MULTILINE)

    for track in REQUEST_TRACKS:
        track_dir = REPO_ROOT / "requests" / track
        for line in (track_dir / "README.md").read_text(encoding="utf-8").splitlines():
            row = stage_cell.match(line)
            if not row:
                continue

            item_dir = track_dir / row["link"]
            if not item_dir.is_dir():
                continue

            for artifact in sorted(item_dir.glob("*.md")):
                header = status_header.search(artifact.read_text(encoding="utf-8"))
                if not header:
                    continue
                assert header["stage"] == row["stage"], (
                    f"{track}/README.md lists {row['slug']} as '{row['stage']}' but "
                    f"{artifact.name} declares '{header['stage']}'. The Index and the "
                    "artifacts must agree — a stale Index makes a shipped item look unbuilt."
                )


def test_ops_readme_documents_the_node_toolchain_and_both_run_modes() -> None:
    body = _read("ops/README.md")

    assert "## Node toolchain" in body, (
        "ops/README.md needs a Node toolchain section beside the uv one — the "
        "frontend has its own install step and its own lockfile rule."
    )

    for command in (
        "uv run rpg-serve",  # served mode — the one canonical incantation
        "npm run dev",  # dev mode, second terminal
        "uv run uvicorn rpg_api.app:create_app",  # dev mode, first terminal
        "npm ci",  # the install that respects the lockfile
    ):
        assert command in body, f"ops/README.md does not document `{command}`."

"""Leak guards for a public repo.

This repo is public so that branch protection works on GitHub Free. That is a
deliberate trade (see ADR 0007), and it means every tracked file is
world-readable — including the career ledger, which is tracked on purpose.

Gitleaks catches credentials by content in CI. These catch the quieter class:
machine-specific absolute paths and personal identifiers that leak the author's
environment, break on anyone else's machine, and accumulate silently because
nothing else complains about them.

Scanned files are the git index, so anything gitignored is out of scope by
construction.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# A Windows drive-letter absolute path: C:\..., d:/... — two or more segments so
# a bare "C:" in prose doesn't trip it.
WINDOWS_PATH = re.compile(r"\b[A-Za-z]:[\\/](?:[\w .()-]+[\\/]){1,}[\w .()-]*")
# A POSIX home directory belonging to a named user.
POSIX_HOME = re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Paths whose *content* is allowed to contain these patterns, with the reason.
ALLOWED = {
    "tests/test_no_leaks.py": "this file — it contains the detection patterns",
    ".env.example": "documents the config keys; values are deliberately empty",
}

# Extensions worth scanning. Binary files are skipped, and so is uv.lock — but
# NOT every lockfile: `.json` is in this set, so app/package-lock.json IS
# scanned. That is deliberate; npm lockfiles have historically carried local
# paths and registry credentials.
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".toml",
    ".json",
    ".yml",
    ".yaml",
    ".ps1",
    ".psm1",
    ".js",
    ".mjs",
    ".ts",
    ".tsx",
    ".css",
    ".html",
    ".jsonl",
    ".txt",
}


def _tracked_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    names = [n for n in result.stdout.split("\0") if n]
    return [
        REPO_ROOT / n for n in names if n not in ALLOWED and Path(n).suffix.lower() in TEXT_SUFFIXES
    ]


def _hits(pattern: re.Pattern[str]) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path in _tracked_text_files():
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        matches = sorted(set(pattern.findall(body)))
        if matches:
            found[str(path.relative_to(REPO_ROOT)).replace("\\", "/")] = matches[:5]
    return found


def test_no_windows_absolute_paths() -> None:
    """A literal `D:\\...` breaks on every other machine and leaks drive layout.

    Resolve paths instead: an env var with a documented default, a registry
    probe, or a path relative to the repo root. `research/tools/iff.ps1` is the
    worked example.
    """
    found = _hits(WINDOWS_PATH)
    assert not found, "Machine-specific absolute path(s) in tracked files:\n" + "\n".join(
        f"  {file}: {matches}" for file, matches in sorted(found.items())
    )


def test_no_posix_home_directories() -> None:
    found = _hits(POSIX_HOME)
    assert not found, "Home-directory path(s) in tracked files:\n" + "\n".join(
        f"  {file}: {matches}" for file, matches in sorted(found.items())
    )


def test_no_email_addresses() -> None:
    """Commit metadata carries an address by necessity; file contents shouldn't."""
    found = _hits(EMAIL)
    assert not found, "Email address(es) in tracked files:\n" + "\n".join(
        f"  {file}: {matches}" for file, matches in sorted(found.items())
    )


def test_dotenv_is_ignored_and_an_example_is_committed() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "\n.env\n" in gitignore, ".env must be gitignored — this repo is public."
    assert (REPO_ROOT / ".env.example").is_file(), (
        ".env.example must be committed so a fresh clone knows what configuration is expected."
    )

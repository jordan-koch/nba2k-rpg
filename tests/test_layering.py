"""AC 3 — the domain core stays web-free.

`src/rpg_core/` is the I/O-free domain; the API and web app depend on it and it
depends on neither. That direction is what makes the economy testable without a
server and what keeps Phase 2's ruleset swap a config change rather than a
migration.

Scope decision 3 chose this guard **instead of** a tenth ADR, on the grounds
that a test failing the build is a stronger record than prose. That makes the
failure message below the record — it cites DESIGN.md by name on purpose.

The guard is a pure function so it can be proven red **and** green in one
`uv run pytest`, against `tmp_path` fakes, without ever editing tracked source.
The obvious alternative — add `import fastapi` to the core and revert it — is
not available: subagents have read-only git, and this is the very PR whose
point is that the import must not be there.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DESIGN_CITATION = "DESIGN.md §3 — 'Two packages, one repo'"

# First dotted segment of any import the domain core must not have.
#
# `pydantic` is deliberately ABSENT. ADR 0002 requires the ingestion DTO to be
# constructible with no HTTP and no UI, which is a different question from
# whether the core may use pydantic for validation — that is item 1.2's call to
# make. Do not add it here "for completeness"; adding it pre-empts a decision
# nobody has taken.
WEB_PACKAGES = frozenset({"fastapi", "starlette", "uvicorn", "rpg_api"})


def web_imports_under(root: Path) -> list[tuple[str, str]]:
    """Every (file, package) pair where a module under `root` imports the web.

    Parses with `ast` rather than grepping: a docstring that mentions fastapi —
    like the one in `src/rpg_api/__init__.py` — must not trip this, and a regex
    cannot tell the difference. Comparing the first dotted segment catches
    `from fastapi.testclient import TestClient` as well as a plain import.
    """
    violations: list[tuple[str, str]] = []

    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                # `from . import x` has module None — a relative import can
                # never name a third-party package, so it is not a violation.
                if node.module is None:
                    continue
                names = [node.module]

            for name in names:
                head = name.split(".")[0]
                if head in WEB_PACKAGES:
                    violations.append((path.name, head))

    return violations


def violation_message(violations: list[tuple[str, str]]) -> str:
    """The record. Decision 3 chose this guard over a tenth ADR, so the
    citation below is where the architectural rule is written down."""
    return (
        "src/rpg_core/ must not import the web layer — it is the I/O-free "
        f"domain, and the dependency arrow points one way. See {DESIGN_CITATION}. "
        "If the core needs something the API has, the thing to move is the data, "
        "not the import.\n"
        + "\n".join(f"  {file} imports {package}" for file, package in violations)
    )


# ─── The guard, proven both ways against tmp_path ────────────────────────────


def test_a_web_import_is_reported(tmp_path: Path) -> None:
    (tmp_path / "clean.py").write_text("import json\n", encoding="utf-8")
    (tmp_path / "dirty.py").write_text(
        "from fastapi.testclient import TestClient\n", encoding="utf-8"
    )

    assert web_imports_under(tmp_path) == [("dirty.py", "fastapi")]


def test_a_clean_tree_reports_nothing(tmp_path: Path) -> None:
    (tmp_path / "core.py").write_text(
        '"""A docstring mentioning fastapi and uvicorn."""\n\nimport json\nfrom . import sibling\n',
        encoding="utf-8",
    )

    assert web_imports_under(tmp_path) == []


# ─── The real assertion ──────────────────────────────────────────────────────


def test_the_domain_core_imports_nothing_web() -> None:
    violations = web_imports_under(REPO_ROOT / "src" / "rpg_core")

    assert not violations, violation_message(violations)


def test_the_failure_message_cites_the_architecture_record() -> None:
    """Decision 3 made this test the record instead of an ADR.

    A failure message that just says "layering violation" sends the reader
    nowhere; this one has to name the document that explains the rule, or the
    decision to skip the ADR costs more than it saved.
    """
    message = violation_message([("ledger.py", "fastapi")])

    assert DESIGN_CITATION in message
    assert "DESIGN.md" in message
    assert "ledger.py imports fastapi" in message

"""The health endpoint — `GET /api/health`.

STANDING RULE for this payload (scope decision 6): **a field arrives only when
the thing it reports exists.** No `career_count` until item 1.2 lands the
ledger, no `ruleset_version` until 1.4 lands rulesets — a field reporting on a
subsystem that does not exist is a lie the frontend will render. No
`started_at`/`uptime` either: nothing consumes them, and ruff's DTZ rules tax a
naive datetime for good reason.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from fastapi import APIRouter, Request

from rpg_core import __version__

router = APIRouter()


class HealthPayload(TypedDict):
    """The whole contract. Three fields, each reporting something that exists."""

    status: str
    version: str
    spa_built: bool


@router.get("/health")
async def health(request: Request) -> HealthPayload:
    """Liveness plus the two facts a fresh clone needs to explain itself.

    `spa_built` is computed per request rather than at construction (decision
    J): the catch-all route decides with this same predicate, so the flag and
    the route cannot disagree, and running `npm run build` while uvicorn is
    already up flips both in the same instant — no "restart the server" caveat.

    `request.app.state` is typed `Any`, so it is bound through an annotated
    local. Returning it straight from a `-> Path` context trips mypy's
    `warn_return_any`, and the `# type: ignore` that silences it is banned by
    AC 8. Measured, not assumed — see reviews/preflight.md belief 2.
    """
    dist: Path = request.app.state.spa_dist
    return {
        "status": "ok",
        # Read from the core, never re-typed as a literal here.
        # tests/test_repo_structure.py already pins it to pyproject.toml, so
        # this payload inherits that pin for free.
        "version": __version__,
        "spa_built": (dist / "index.html").is_file(),
    }

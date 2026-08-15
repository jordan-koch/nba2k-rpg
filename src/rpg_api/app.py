"""The application factory.

The dist location is a **factory argument**, not a module constant (decision K).
Two reasons, and the first is an acceptance criterion: AC 5 requires
constructing the app against a path that does not exist and getting no
exception, which a module constant makes untestable. The second is the
convention items 1.2-1.11 will copy — a consumer never hardcodes a location, it
*receives* one. There is no `datasets/manifest.json` yet, so this is what
"resolve by name, never a literal path" looks like in its pre-dataset form:
**the injection point is the convention.**
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from rpg_api import health
from rpg_api.spa import attach_spa
from rpg_core import __version__


def default_spa_dist() -> Path:
    """Where `npm run build` puts the SPA, resolved relative to this file.

    Never a literal path — the repo is public and a drive letter in a tracked
    file fails `tests/test_no_leaks.py`.

    ASSUMPTION, stated rather than hidden: this lands inside the tree only
    because uv installs the project **editable** from a checkout, which is
    exactly the scope's "it runs from a checkout" non-goal. A non-editable
    wheel resolves somewhere without an `app/dist/` and gets the 503 branch —
    the designed fallback, not a bug.
    """
    return Path(__file__).resolve().parents[2] / "app" / "dist"


def create_app(spa_dist: Path | None = None) -> FastAPI:
    """Build the application. Constructing it must never touch the filesystem."""
    app = FastAPI(title="nba2k-rpg", version=__version__)

    # Read per request by both the health payload and the catch-all route.
    dist = default_spa_dist() if spa_dist is None else spa_dist
    app.state.spa_dist = dist

    app.include_router(health.router, prefix="/api")

    # LAST, always. FastAPI matches in registration order, so the catch-all
    # must come after every real route or it shadows them — see spa.py.
    attach_spa(app, dist)

    return app

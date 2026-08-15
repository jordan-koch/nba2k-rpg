"""Shared fixtures for the API tests.

Everything here exists to make the dist location **injectable**. AC 5 requires
constructing the app against a directory that does not exist and observing no
exception, so the tests must be able to point it anywhere — including nowhere.
No fixture starts a server or binds a socket.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from rpg_api import create_app

INDEX_HTML = '<!doctype html>\n<title>nba2k-rpg</title>\n<div id="root"></div>\n'
ASSET_JS = "export const ok = true;\n"


@pytest.fixture
def client_factory() -> Callable[[Path], TestClient]:
    """Build a client over an arbitrary dist location, existing or not."""

    def build(spa_dist: Path) -> TestClient:
        return TestClient(create_app(spa_dist=spa_dist))

    return build


@pytest.fixture
def client(tmp_path: Path, client_factory: Callable[[Path], TestClient]) -> TestClient:
    """A client over a dist that does **not** exist — the fresh-clone state.

    This is the branch every cold agent hits first: clone, `uv sync`, run, and
    there is no `app/dist/` because nobody has run `npm run build` yet.
    """
    absent = tmp_path / "never-built"
    assert not absent.exists(), "fixture precondition: the dist must not exist"
    return client_factory(absent)


@pytest.fixture
def built_spa_dist(tmp_path: Path) -> Path:
    """A dist that looks like a real `npm run build` output."""
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (dist / "assets" / "index-abc123.js").write_text(ASSET_JS, encoding="utf-8")
    return dist

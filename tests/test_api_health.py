"""AC 2 — the health endpoint, with no live server and no socket."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from fastapi.testclient import TestClient

import rpg_core


def test_health_returns_ok_json(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["status"] == "ok"


def test_health_version_comes_from_the_domain_core(client: TestClient) -> None:
    """Never a literal re-typed in the API layer.

    tests/test_repo_structure.py pins rpg_core.__version__ to pyproject.toml,
    so asserting against the core here makes the payload inherit that pin
    rather than adding a second place for the version to drift.
    """
    assert client.get("/api/health").json()["version"] == rpg_core.__version__


def test_spa_built_is_a_bool_and_false_without_a_build(client: TestClient) -> None:
    body = client.get("/api/health").json()

    assert isinstance(body["spa_built"], bool)
    assert body["spa_built"] is False


def test_spa_built_is_true_against_a_built_dist(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    assert client_factory(built_spa_dist).get("/api/health").json()["spa_built"] is True


def test_spa_built_flips_without_reconstructing_the_app(
    client_factory: Callable[[Path], TestClient], tmp_path: Path
) -> None:
    """Decision J: the flag is computed per request, not at construction.

    Building the SPA while uvicorn is already running must flip the flag in the
    same instant. If this ever fails, someone has hoisted the predicate into
    create_app and quietly introduced a "restart the server" caveat.
    """
    dist = tmp_path / "dist"
    dist.mkdir()
    built_client = client_factory(dist)

    assert built_client.get("/api/health").json()["spa_built"] is False

    (dist / "index.html").write_text("<!doctype html>\n", encoding="utf-8")

    assert built_client.get("/api/health").json()["spa_built"] is True

"""ACs 5, 6 and 7 — the two dist states, and the API/SPA boundary between them.

No live server and no socket anywhere in this module.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from fastapi import APIRouter
from fastapi.testclient import TestClient

from rpg_api import create_app
from rpg_api.spa import resolves_inside

# ─── AC 5 — the missing-build branch (the fresh-clone state) ──────────────────


def test_constructing_against_an_absent_dist_raises_nothing(tmp_path: Path) -> None:
    """The whole reason there is no StaticFiles mount.

    A mount raises RuntimeError right here, so a fresh clone gets a traceback
    on import rather than a running server that explains itself.
    """
    absent = tmp_path / "never-built"

    app = create_app(spa_dist=absent)

    assert app is not None
    assert not absent.exists(), "constructing the app must not create the dist"


def test_api_still_answers_without_a_build(client: TestClient) -> None:
    assert client.get("/api/health").status_code == 200


def test_root_is_503_naming_the_build_command(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 503
    assert "npm run build" in response.text


# ─── AC 6 — the present-build branch ─────────────────────────────────────────


def test_root_serves_index_html_bytes(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    response = client_factory(built_spa_dist).get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    # Bytes, not text: the response is served raw, while read_text would apply
    # universal-newline translation and mask a CRLF mismatch on Windows.
    assert response.content == (built_spa_dist / "index.html").read_bytes()


def test_a_real_asset_is_served(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    response = client_factory(built_spa_dist).get("/assets/index-abc123.js")

    assert response.status_code == 200
    assert "export const ok" in response.text


def test_unknown_path_falls_back_to_the_shell(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """History fallback: a client-side route is not a 404."""
    response = client_factory(built_spa_dist).get("/careers/some-guy/season/3")

    assert response.status_code == 200
    assert response.content == (built_spa_dist / "index.html").read_bytes()


# ─── AC 7 — the API boundary, asserted on BOTH branches ──────────────────────


def test_unknown_api_path_is_json_404_without_a_build(client: TestClient) -> None:
    response = client.get("/api/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")


def test_unknown_api_path_is_json_404_with_a_build(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """The branch that actually bites.

    With a build present, a naive catch-all hands back index.html with a 200
    for every unknown /api path — so the frontend sees HTML where it expected
    JSON and the bug looks like a frontend parse error.
    """
    response = client_factory(built_spa_dist).get("/api/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
    assert response.content != (built_spa_dist / "index.html").read_bytes()


def test_the_catch_all_did_not_shadow_the_health_route(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """Registration order, asserted where a build exists to shadow it with."""
    response = client_factory(built_spa_dist).get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ─── Traversal (implementation note, not an acceptance criterion) ─────────────


def test_resolves_inside_refuses_an_escape_that_names_a_real_file(
    built_spa_dist: Path, tmp_path: Path
) -> None:
    """The guard proven RED-able, against a file that really exists.

    Asserted on the pure function, not over HTTP, and that is the whole point:
    an HTTP client resolves `..` segments client-side before sending, so
    `client.get("/../secret.txt")` arrives as `/secret.txt` and never reaches
    the containment check at all. The previous version of this test passed
    with the guard deleted.
    """
    secret = tmp_path / "secret.txt"
    secret.write_text("do not serve me", encoding="utf-8")
    assert secret.is_file(), "the escape must name a real file or this proves nothing"

    assert resolves_inside(built_spa_dist, "../secret.txt") is None


def test_resolves_inside_returns_a_real_asset(built_spa_dist: Path) -> None:
    resolved = resolves_inside(built_spa_dist, "assets/index-abc123.js")

    assert resolved is not None
    assert resolved.name == "index-abc123.js"


def test_resolves_inside_returns_none_for_a_path_that_is_not_there(
    built_spa_dist: Path,
) -> None:
    assert resolves_inside(built_spa_dist, "assets/never-built.js") is None


def test_traversal_over_http_is_not_served(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path, tmp_path: Path
) -> None:
    """The HTTP half, using the ENCODED form so it survives normalization.

    `/../secret.txt` is collapsed to `/secret.txt` by the client; `/%2e%2e/`
    reaches the handler intact. Do not "tidy" this back to a plain `../` — it
    silently disarms the test.
    """
    (tmp_path / "secret.txt").write_text("do not serve me", encoding="utf-8")

    response = client_factory(built_spa_dist).get("/%2e%2e/secret.txt")

    assert "do not serve me" not in response.text
    # Positive assertion too, because the negative alone also passes on a 500
    # or an empty body. 404 rather than the shell: the escape names a path with
    # an extension, so the static-asset guard refuses it outright instead of
    # treating it as a client-side route.
    assert response.status_code == 404
    assert response.content != (built_spa_dist / "index.html").read_bytes()


# ─── Missing assets 404 rather than falling back ─────────────────────────────


def test_a_missing_asset_is_404_but_a_client_route_still_falls_back(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """The pairing IS the test — a 404 alone would not show the distinction.

    A rebuild renames every hashed chunk, so a stale tab requests one that no
    longer exists. Answering that with index.html and a 200 kills the module
    loader with a MIME-type error pointing at the frontend.
    """
    client = client_factory(built_spa_dist)

    missing_asset = client.get("/assets/index-GONE.js")
    assert missing_asset.status_code == 404
    assert missing_asset.content != (built_spa_dist / "index.html").read_bytes()

    client_route = client.get("/careers/some-guy/season/3")
    assert client_route.status_code == 200
    assert client_route.content == (built_spa_dist / "index.html").read_bytes()


def test_a_missing_file_with_an_extension_is_404(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    assert client_factory(built_spa_dist).get("/favicon.svg").status_code == 404


# ─── Registration order is structural, not a comment ─────────────────────────


def test_routers_passed_to_the_factory_are_reachable(tmp_path: Path) -> None:
    """The trap items 1.2-1.11 would otherwise inherit.

    Calling `app.include_router(...)` on the returned app registers it AFTER
    the catch-all, so every one of its paths 404s. Passing routers in through
    the factory is what makes the correct order the only order available.
    """
    later = APIRouter()

    @later.get("/careers")
    async def list_careers() -> dict[str, list[str]]:
        return {"careers": []}

    client = TestClient(create_app(spa_dist=tmp_path / "absent", routers=[later]))

    response = client.get("/api/careers")

    assert response.status_code == 200, (
        "A router passed to create_app must be registered before the SPA "
        "catch-all. If this 404s, the catch-all is shadowing it."
    )
    assert response.json() == {"careers": []}


def test_the_catch_all_is_always_the_last_route(tmp_path: Path) -> None:
    app = create_app(spa_dist=tmp_path / "absent", routers=[APIRouter()])

    assert getattr(app.routes[-1], "path", None) == "/{full_path:path}"

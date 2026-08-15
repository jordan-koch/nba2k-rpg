"""Serve the built SPA from the same origin as the API.

WHY THERE IS NO `StaticFiles` MOUNT — both halves matter, and a future
simplification back to `app.mount("/", StaticFiles(directory=dist, html=True))`
reintroduces two bugs at once:

1. **It raises at construction when the directory is absent.** Measured, not
   assumed: `RuntimeError: Directory '...' does not exist` (see
   reviews/preflight.md belief 1). A fresh clone has no `app/dist/` until
   somebody runs `npm run build`, so the obvious mount gives that clone an
   import-time traceback. AC 5 forbids exactly that.
2. **A mount at `/` still answers unknown `/api` paths**, and with HTML. AC 7
   requires a JSON 404 there, because the SPA history fallback silently
   swallowing API 404s is a bug that presents as a frontend problem.

So this hand-rolls one catch-all instead, registered **last**, deciding per
request. `check_dir=False` would fix only the first half.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse

# Named so the 503 body and ops/README.md cannot drift apart.
BUILD_COMMAND = "npm run build"

# Vite's default output directory for hashed bundles.
ASSET_PREFIX = "assets/"


def resolves_inside(dist: Path, full_path: str) -> Path | None:
    """The file `full_path` names inside `dist`, or None if there isn't one.

    A **pure function** so the traversal defense can be proven red and green
    against `tmp_path`, with no HTTP client in the loop. That is not
    fastidiousness: an HTTP client resolves `..` segments itself before the
    request is ever sent, so a test that asks a client for `/../secret.txt`
    exercises nothing here and stays green with this guard deleted. Same idiom
    as tests/test_layering.py and tests/test_ci_contexts.py.

    Containment is checked BEFORE existence so an escape is refused even when
    it names a real file — which is exactly the case a test must be able to
    construct.
    """
    candidate = (dist / full_path).resolve()

    if not candidate.is_relative_to(dist.resolve()):
        return None
    if not candidate.is_file():
        return None

    return candidate


def looks_like_a_static_asset(full_path: str) -> bool:
    """Whether a miss on `full_path` should 404 rather than fall back.

    The static-side twin of the `/api` branch below, and it exists for the same
    reason: a fallback that swallows misses turns a backend answer into a
    frontend-looking bug. Vite emits content-hashed chunk names, so a rebuild
    renames everything under `dist/assets/`. A tab holding the previous page
    then requests a chunk that no longer exists — and without this, it gets
    `index.html` with a 200 and the module loader dies on "Expected a
    JavaScript module script but the server responded with a MIME type of
    text/html", which points at the frontend rather than at the stale tab.
    That breaks the build-while-serving workflow ops/README.md advertises.

    Client-side routes are extensionless (`/careers/some-guy/season/3`), so the
    suffix test separates them cleanly. A path segment containing a dot would
    be misread as an asset, which is why slugs stay kebab-case.
    """
    return full_path.startswith(ASSET_PREFIX) or bool(PurePosixPath(full_path).suffix)


MISSING_BUILD_MESSAGE = (
    "The web app has not been built yet.\n\n"
    f"Run `{BUILD_COMMAND}` from the app/ directory, then reload this page.\n"
    "The API itself is up — try /api/health.\n"
)


def attach_spa(app: FastAPI, dist: Path) -> None:
    """Register the catch-all. MUST be the last route added to `app`.

    Registration order is a correctness constraint, not a style preference:
    FastAPI matches in registration order, so a catch-all added before the API
    router makes `/api/health` return `index.html` — a backend bug that
    presents as a frontend one, and one items 1.7-1.11 would inherit.
    """

    # response_model=None because the return is a union of Response subclasses,
    # which is not a pydantic field type — FastAPI raises at registration
    # otherwise. Disabling model generation is its documented remedy and keeps
    # the precise annotation for mypy instead of widening it to Response.
    # include_in_schema=False because a catch-all matching every path would
    # otherwise appear in /docs as a real endpoint and misdescribe the API.
    @app.get("/{full_path:path}", response_model=None, include_in_schema=False)
    async def serve_spa(full_path: str) -> FileResponse | PlainTextResponse:
        # (a) The API boundary, checked FIRST. Anything under /api that got
        #     this far matched no route, so it is a genuine 404 — and it must
        #     be JSON, which is how FastAPI renders HTTPException.
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")

        # (b) A real build artifact, if the path names one inside the dist.
        #     Traversal is refused by resolves_inside; an escape falls through
        #     rather than erroring, which is the right answer for something
        #     indistinguishable from a client-side route.
        candidate = resolves_inside(dist, full_path)
        if candidate is not None:
            return FileResponse(candidate)

        # (b2) A miss that is obviously an asset is a 404, not the shell.
        if looks_like_a_static_asset(full_path):
            raise HTTPException(status_code=404, detail="Not Found")

        # (c) History fallback: any unmatched path is a client-side route, so
        #     hand back the shell and let the SPA router decide.
        index = dist / "index.html"
        if index.is_file():
            return FileResponse(index)

        # (d) No build at all. Say so in words that name the fix, rather than
        #     404ing at someone who has just cloned the repo.
        return PlainTextResponse(MISSING_BUILD_MESSAGE, status_code=503)

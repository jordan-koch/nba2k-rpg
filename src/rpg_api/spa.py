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

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse

# Named so the 503 body and ops/README.md cannot drift apart.
BUILD_COMMAND = "npm run build"

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

        # (b) A real build artifact. `.resolve()` then `is_relative_to` keeps a
        #     traversal like `../../etc/passwd` from escaping the dist root;
        #     an escape falls through to the history fallback rather than
        #     erroring, which is the correct answer for a client-side route.
        candidate = (dist / full_path).resolve()
        if candidate.is_file() and candidate.is_relative_to(dist.resolve()):
            return FileResponse(candidate)

        # (c) History fallback: any unmatched path is a client-side route, so
        #     hand back the shell and let the SPA router decide.
        index = dist / "index.html"
        if index.is_file():
            return FileResponse(index)

        # (d) No build at all. Say so in words that name the fix, rather than
        #     404ing at someone who has just cloned the repo.
        return PlainTextResponse(MISSING_BUILD_MESSAGE, status_code=503)

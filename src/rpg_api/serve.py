"""The `rpg-serve` console entrypoint — the served build, one canonical way.

Scope decision 9 permits exactly one documented incantation for the served
build, which is why there is no `__main__.py` alongside this. Dev mode is a
different thing and documents its own uvicorn command; see ops/README.md.
"""

from __future__ import annotations

import uvicorn

HOST = "127.0.0.1"
PORT = 8000


def main() -> None:
    """Serve the built SPA and the API on one origin.

    The host is the **IPv4 literal**, not `localhost`, and it must stay in step
    with the Vite dev proxy target. Node on Windows can resolve `localhost` to
    `::1` while uvicorn binds `127.0.0.1`, and the resulting ECONNREFUSED is
    indistinguishable from a dead backend — an hour lost to a symptom pointing
    at the wrong process.

    `factory=True` because create_app is a factory, not a module-level app.
    """
    uvicorn.run("rpg_api.app:create_app", factory=True, host=HOST, port=PORT)

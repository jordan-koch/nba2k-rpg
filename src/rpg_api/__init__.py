"""HTTP seam for the NBA 2K26 RPG progression engine.

The mirror of `rpg_core`'s docstring, from the API side. This package owns
transport and nothing else: routing, serialization, and serving the built SPA.
It imports `rpg_core`; `rpg_core` must never import it, and
`tests/test_layering.py` fails the build if that direction ever inverts.

Keeping the domain core web-free is what makes the economy testable without a
server and what keeps Phase 2's ruleset swap a config change. See DESIGN.md §3.
"""

from __future__ import annotations

from rpg_api.app import create_app

__all__ = ["create_app"]

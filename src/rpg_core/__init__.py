"""Domain core for the NBA 2K26 RPG progression engine.

Deliberately I/O-free and web-free. This package holds the event ledger, the
fold that turns it into current player state, the economy (earning, pricing,
expectation), and the ruleset loader. The API and the web app depend on it;
it depends on neither.

That direction is what makes the economy testable in isolation and what makes
Phase 2's ruleset swap a config change rather than a migration. See ROADMAP.md.

Phase 0: empty. Contents arrive with Phase 1.
"""

from __future__ import annotations

__version__ = "0.1.0"

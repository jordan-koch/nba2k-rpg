import { useEffect, useState } from "react";

import { fetchHealth, type Health } from "./api/client";

// Spelled out because the unreachable panel is useless without it — the whole
// point of that state is telling somebody what to run. Kept in step with
// [project.scripts] in pyproject.toml and the Setup block in README.md.
const START_COMMAND = "uv run rpg-serve";

// Exactly three states, and "unreachable" is a first-class one rather than an
// error boundary afterthought: a backend that isn't running is the normal case
// for anyone who has just cloned the repo.
type Status =
  | { kind: "loading" }
  | { kind: "ok"; health: Health }
  | { kind: "unreachable" };

export default function App() {
  const [status, setStatus] = useState<Status>({ kind: "loading" });

  useEffect(() => {
    let cancelled = false;

    fetchHealth()
      .then((health) => {
        if (!cancelled) setStatus({ kind: "ok", health });
      })
      .catch(() => {
        if (!cancelled) setStatus({ kind: "unreachable" });
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main className="shell">
      <h1>nba2k-rpg</h1>
      <p className="tagline">A progression layer for MyNBA player-locked careers.</p>

      {status.kind === "loading" && <p className="muted">Checking the backend…</p>}

      {status.kind === "ok" && (
        <dl className="facts">
          <dt>API</dt>
          <dd>
            <span className="dot dot--ok" aria-hidden="true" /> {status.health.status}
          </dd>

          <dt>Version</dt>
          <dd>{status.health.version}</dd>

          {/* Render the FACT the payload carries, not a mode inferred from
              it. `spa_built` reports whether app/dist/index.html exists on
              disk — nothing about which process answered this request. In dev
              the two diverge: Vite serves the page while the proxied backend
              still sees a build present, so "served from dist" was simply
              false there. The mode is known client-side, so it is read from
              there instead and both rows are true in both modes. */}
          <dt>SPA build</dt>
          <dd>{status.health.spa_built ? "built" : "not built"}</dd>

          <dt>Serving</dt>
          <dd>{import.meta.env.DEV ? "Vite dev server" : "uvicorn"}</dd>
        </dl>
      )}

      {status.kind === "unreachable" && (
        <section className="panel" role="alert">
          <h2>
            <span className="dot dot--bad" aria-hidden="true" /> Backend unreachable
          </h2>
          <p>Nothing is answering on the API. Start it with:</p>
          <pre>
            <code>{START_COMMAND}</code>
          </pre>
          <p className="muted">Then reload this page.</p>
        </section>
      )}
    </main>
  );
}

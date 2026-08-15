// EXACTLY TWO TESTS. AC 12 is a count, not a floor — the scope decided this
// suite lands minimally, covering the one piece of real branching logic the
// shell has. If a third belongs here, that is a scope conversation, not a
// drive-by addition.
//
// Under `globals: false` every helper is imported explicitly rather than
// assumed present.
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import App from "./App";

// Stubbing fetch rather than mocking ./api/client means client.ts is genuinely
// exercised — its relative URL, its response.ok check, and its JSON parse. A
// module mock would test the mock.
function stubFetch(impl: () => Promise<Response>): void {
  vi.stubGlobal("fetch", vi.fn(impl));
}

describe("App", () => {
  it("renders the version returned by the API", async () => {
    stubFetch(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ status: "ok", version: "9.9.9", spa_built: false }),
      } as Response),
    );

    render(<App />);

    expect(await screen.findByText("9.9.9")).toBeInTheDocument();

    // Asserted HERE rather than in a third test, so AC 12's exact count of two
    // survives. `spa_built: false` must render as the fact it is — the page
    // must not restate it as a claim about which server is answering, which it
    // cannot know from this payload and got wrong in dev.
    expect(screen.getByText("not built")).toBeInTheDocument();
    expect(screen.getByText("Serving")).toBeInTheDocument();
  });

  it("renders the unreachable panel naming the start command when the fetch rejects", async () => {
    stubFetch(() => Promise.reject(new Error("ECONNREFUSED")));

    render(<App />);

    expect(await screen.findByRole("alert")).toBeInTheDocument();
    expect(screen.getByText(/backend unreachable/i)).toBeInTheDocument();
    // The panel is worthless without the command, so assert the command.
    expect(screen.getByText("uv run rpg-serve")).toBeInTheDocument();
  });
});

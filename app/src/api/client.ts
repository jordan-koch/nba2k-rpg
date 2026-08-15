// The API seam. Deliberately hand-written and deliberately tiny.
//
// This is NOT the generated-client contract — that is item 1.8's job. This is
// the seam it slots into, so keep it boring: one interface, one function.

export interface Health {
  status: string;
  version: string;
  spa_built: boolean;
}

// RELATIVE, never an absolute origin. This one detail is what makes both run
// modes same-origin: in dev the Vite proxy forwards /api to 127.0.0.1:8000, and
// in the served build uvicorn is already the origin. An absolute URL here would
// work in exactly one of the two and need CORS middleware for the other.
const HEALTH_URL = "/api/health";

export async function fetchHealth(): Promise<Health> {
  const response = await fetch(HEALTH_URL);

  if (!response.ok) {
    throw new Error(`GET ${HEALTH_URL} returned ${response.status}`);
  }

  return (await response.json()) as Health;
}

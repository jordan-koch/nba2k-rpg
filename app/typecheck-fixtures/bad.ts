// Deliberately ill-typed. This file MUST NOT compile.
//
// It is the evidence for AC 11: it proves `strict` is actually engaged rather
// than a default-generated config that checks nothing. Excluded from the real
// project and from the build; only tsconfig.negative.json compiles it, and
// scripts/check-negative.mjs asserts that compilation FAILS.
//
// Both errors are strict-family on purpose. A plain `const n: number = "x"`
// errors with strict OFF too, so it would prove only that the compiler ran.
//
// Measured error codes under TypeScript 6 (see reviews/preflight.md):
//   len()   -> TS18048  's' is possibly 'undefined'      (strictNullChecks)
//   first() -> TS2322   string | undefined not assignable (noUncheckedIndexedAccess)
//
// If you are here because the negative check went green unexpectedly, the
// likely cause is a strictness flag being dropped from tsconfig.json — not a
// problem with this file.

export function len(s?: string): number {
  return s.length;
}

export function first(xs: string[]): string {
  return xs[0];
}

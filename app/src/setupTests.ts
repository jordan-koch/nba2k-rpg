// Both imports are load-bearing under `globals: false`, which is why the
// vitest config sets it explicitly rather than leaving it to a default.
//
// 1. The VITEST-SPECIFIC jest-dom entry. The bare package has no global
//    `expect` to extend, so importing it instead leaves toBeInTheDocument()
//    simply absent — and the obvious "fix" is to flip globals: true, silently
//    diverging from the config this project decided on.
import "@testing-library/jest-dom/vitest";
// 2. RTL's auto-cleanup never registers without an explicit afterEach when
//    globals are off. Without it the first test's DOM leaks into the second and
//    getByText on the version string throws "found multiple elements" — in
//    exactly the two-test suite this project pins.
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(cleanup);

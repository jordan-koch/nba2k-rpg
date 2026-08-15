// AC 11's assertion: the negative typecheck must FAIL.
//
// An npm script cannot assert its own exit code, and PowerShell 5.1 cannot
// negate one inline, so the assertion lives here — one command invocation,
// identical on Windows and Linux, keeping every npm script free of shell
// operators.
//
// This deliberately does more than invert the exit code, because there are two
// ways to get a non-zero exit that mean nothing:
//
//   1. TS18003 "No inputs were found" — the config matched no files at all.
//      That is the exact false green tsconfig.negative.json's `"exclude": []`
//      exists to prevent, so seeing it here is a FAILURE, not a pass.
//   2. A non-strict error — the fixture failing for a reason that would also
//      fail with `strict` off proves only that the compiler ran.
//
// So: non-zero exit, no TS18003, and at least one code from the strict family.

import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

// Spawn tsc's JS entry through this same Node binary rather than the `tsc`
// shim. On Windows npm installs `tsc.cmd`, and spawnSync without shell:true
// fails ENOENT on it; resolving the entry point sidesteps the shim on both
// platforms without opening a shell.
const tscEntry = require.resolve("typescript/lib/tsc.js");

const result = spawnSync(
  process.execPath,
  [tscEntry, "--noEmit", "-p", "tsconfig.negative.json"],
  { encoding: "utf8" },
);

const output = `${result.stdout ?? ""}${result.stderr ?? ""}`;

// Codes the committed fixture is built to produce. Measured under TS 6.
const STRICT_FAMILY = ["TS18048", "TS2532", "TS2322"];

const problems = [];

if (result.error) {
  problems.push(`could not run tsc: ${result.error.message}`);
}
if (result.status === 0) {
  problems.push(
    "the negative typecheck SUCCEEDED. typecheck-fixtures/bad.ts is supposed " +
      "to be ill-typed, so a strictness flag has probably been dropped from " +
      "tsconfig.json.",
  );
}
if (output.includes("TS18003")) {
  problems.push(
    "TS18003 'No inputs were found' — the negative project matched no files, " +
      "so it failed for the wrong reason. Check that tsconfig.negative.json " +
      'still sets "exclude": [], since a child config inherits its parent\'s.',
  );
}
if (!STRICT_FAMILY.some((code) => output.includes(code))) {
  problems.push(
    `expected one of ${STRICT_FAMILY.join(", ")} in the output, proving the ` +
      "failure is strict-specific rather than any old type error.",
  );
}

if (problems.length > 0) {
  console.error("negative typecheck check FAILED:");
  for (const problem of problems) {
    console.error(`  - ${problem}`);
  }
  console.error("\ntsc output was:\n" + (output || "(empty)"));
  process.exit(1);
}

console.log(
  "negative typecheck OK — tsc rejected typecheck-fixtures/bad.ts for a " +
    "strict-specific reason, so `strict` is genuinely engaged.",
);

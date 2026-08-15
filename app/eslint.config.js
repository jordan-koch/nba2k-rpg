// Flat config, scoped to app/ on purpose. A repo-root eslint would immediately
// start reporting on the 8 tracked .js/.mjs files under .claude/, forcing an
// ignore list nobody scoped.
//
// Decision 2 chose this stack over oxlint (which create-vite now scaffolds by
// default): eslint-plugin-react-hooks catches rules-of-hooks violations that
// are real runtime bugs, and that value grows sharply at items 1.7-1.11.
//
// No prettier gate. That is a visible default, not an oversight.
import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  // typecheck-fixtures is ill-typed BY DESIGN — linting it reports noise about
  // code whose entire job is to be wrong.
  { ignores: ["dist", "typecheck-fixtures"] },

  js.configs.recommended,
  tseslint.configs.recommended,

  // NOT configs["recommended-latest"], and NOT configs.flat. In v7 the first is
  // the legacy eslintrc shape (its `plugins` is an array of strings, which flat
  // config rejects outright) and the second is a namespace, not a config.
  // Measured — see reviews/preflight.md belief 3.
  reactHooks.configs.flat.recommended,

  {
    files: ["src/**/*.{ts,tsx}"],
    languageOptions: { globals: globals.browser },
  },

  // scripts/ stays linted — it holds the file that makes AC 11 runnable — so
  // its Node globals have to be wired or `npm run lint` fails on it.
  {
    files: ["scripts/**/*.mjs"],
    languageOptions: { globals: globals.node, sourceType: "module" },
  },
);

import react from "@vitejs/plugin-react";
// vitest/config re-exports vite's defineConfig and adds the `test` block, so
// there is no second config file to keep in step.
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],

  server: {
    proxy: {
      // The IPv4 LITERAL, deliberately — never `localhost`. Node on Windows can
      // resolve localhost to ::1 while uvicorn binds 127.0.0.1, and the
      // resulting ECONNREFUSED is indistinguishable from a dead backend.
      //
      // This proxy is the ENTIRE CORS story. Both run modes are same-origin
      // because of it — dev through here, served build through uvicorn itself —
      // so there is no CORS middleware anywhere in the Python half. Removing
      // this means adding that.
      //
      // The port is hardcoded in exactly two places: here and
      // src/rpg_api/serve.py. ops/README.md names both as the pair that must
      // stay in step.
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: false,
      },
    },
  },

  test: {
    environment: "jsdom",
    setupFiles: "./src/setupTests.ts",
    globals: false,
  },
});

import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm"],
  dts: true,
  clean: true,
  treeshake: true,
  outDir: "dist",
  external: [
    "react",
    "react-dom",
    "react/jsx-runtime",
    /^@radix-ui\//,
    /^@ui-sdk\//,
    /^@chamuka\//,
    "class-variance-authority",
    "clsx",
    "tailwind-merge",
  ],
});

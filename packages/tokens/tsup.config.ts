import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts", "src/preset.ts"],
  format: ["esm", "cjs"],
  dts: true,
  clean: false,
  splitting: false,
  treeshake: true,
  outDir: "dist",
});

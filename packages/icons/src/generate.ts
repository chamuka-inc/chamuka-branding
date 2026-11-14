import { transform } from "@svgr/core";
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const SVG_DIR = join(ROOT, "../../../brand/svg");
const OUT_DIR = join(ROOT, "generated");

const INCLUDE = [
  "mark.svg",
  "mark-simple.svg",
  "mark-mono-dark.svg",
  "mark-mono-light.svg",
  "mark-on-cream.svg",
  "mark-on-ember.svg",
  "mark-on-slate.svg",
  "wordmark.svg",
  "lockup-horizontal.svg",
  "lockup-horizontal-mono-dark.svg",
  "lockup-horizontal-mono-light.svg",
  "lockup-stacked.svg",
  "lockup-drawit.svg",
  "lockup-formit.svg",
  "lockup-play.svg",
  "lockup-waypoint.svg",
  "lockup-vmette.svg",
  "app-icon-512.svg",
  "app-icon-drawit-512.svg",
  "app-icon-formit-512.svg",
  "app-icon-play-512.svg",
  "app-icon-waypoint-512.svg",
  "app-icon-vmette-512.svg",
];

const NAME_OVERRIDES: Record<string, string> = {
  "lockup-drawit": "LockupDrawIt",
  "lockup-formit": "LockupFormIt",
  "app-icon-drawit-512": "AppIconDrawIt",
  "app-icon-formit-512": "AppIconFormIt",
  "app-icon-512": "AppIcon",
  "app-icon-play-512": "AppIconPlay",
  "app-icon-waypoint-512": "AppIconWaypoint",
  "app-icon-vmette-512": "AppIconVmette",
};

function pascalCase(file: string): string {
  const base = basename(file, ".svg");
  if (NAME_OVERRIDES[base]) return NAME_OVERRIDES[base];
  return base
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join("");
}

async function main() {
  mkdirSync(OUT_DIR, { recursive: true });
  const available = new Set(readdirSync(SVG_DIR));
  const exports: string[] = [];

  for (const file of INCLUDE) {
    if (!available.has(file)) {
      throw new Error(`Missing brand SVG: ${file}`);
    }
    const svg = readFileSync(join(SVG_DIR, file), "utf8");
    const componentName = pascalCase(file);
    const jsx = await transform(
      svg,
      {
        plugins: ["@svgr/plugin-jsx"],
        typescript: true,
        jsxRuntime: "automatic",
        svgo: false,
        titleProp: true,
        ref: true,
        svgProps: {
          role: "img",
        },
      },
      { componentName },
    );
    const withDefaultTitle = jsx
      .replace(
        'import { Ref, forwardRef } from "react";',
        'import { type Ref, forwardRef } from "react";',
      )
      .replace(
        /role="img"/,
        'role="img" aria-hidden={title ? undefined : true}',
      );
    writeFileSync(join(OUT_DIR, `${componentName}.tsx`), withDefaultTitle);
    exports.push(`export { default as ${componentName} } from "./${componentName}";`);
  }

  writeFileSync(
    join(OUT_DIR, "index.ts"),
    `${exports.join("\n")}\n`,
  );
  writeFileSync(
    join(ROOT, "index.ts"),
    `export * from "./generated";\n`,
  );
  console.log(`generated ${INCLUDE.length} icon components`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

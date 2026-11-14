/**
 * Compile DTCG JSON into CSS (shadcn + Tailwind v4) and typed TS exports.
 * Values come from src/tokens; emission order matches the original brand tokens.css.
 */
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const TOKENS_DIR = join(ROOT, "tokens");
const DIST = join(ROOT, "..", "dist");
const GENERATED = join(ROOT, "generated.ts");

type TokenNode = {
  $value?: unknown;
  $type?: string;
  $description?: string;
  [key: string]: unknown;
};

type FlatToken = {
  path: string;
  value: unknown;
  type?: string;
  description?: string;
};

function isToken(node: unknown): node is TokenNode {
  return Boolean(node && typeof node === "object" && "$value" in (node as object));
}

function walk(node: unknown, prefix: string[], acc: FlatToken[]): void {
  if (!node || typeof node !== "object") return;
  if (isToken(node)) {
    acc.push({
      path: prefix.join("."),
      value: node.$value,
      type: node.$type,
      description: node.$description,
    });
    return;
  }
  for (const [key, child] of Object.entries(node as Record<string, unknown>)) {
    if (key.startsWith("$")) continue;
    walk(child, [...prefix, key], acc);
  }
}

function loadTokens(): FlatToken[] {
  const acc: FlatToken[] = [];
  for (const file of readdirSync(TOKENS_DIR).sort()) {
    if (!file.endsWith(".json")) continue;
    const json = JSON.parse(readFileSync(join(TOKENS_DIR, file), "utf8")) as unknown;
    walk(json, [], acc);
  }
  return acc;
}

const REF = /^\{([^}]+)\}$/;

function cssName(path: string): string {
  const map: Record<string, string> = {
    "radius.default": "--radius",
    "font.display": "--font-display",
    "font.sans": "--font-sans",
    "font.mono": "--font-mono",
  };
  if (map[path]) return map[path];
  if (path.startsWith("color.neutral.")) {
    return `--neutral-${path.slice("color.neutral.".length)}`;
  }
  if (path.startsWith("color.")) return `--${path.slice("color.".length)}`;
  if (path.startsWith("semantic.light.") || path.startsWith("semantic.dark.")) {
    const name = path.split(".").slice(2).join("-");
    return `--${name}`;
  }
  if (path.startsWith("fontSize.")) return `--font-size-${path.slice("fontSize.".length)}`;
  if (path.startsWith("lineHeight.")) return `--line-height-${path.slice("lineHeight.".length)}`;
  if (path.startsWith("fontWeight.")) return `--font-weight-${path.slice("fontWeight.".length)}`;
  if (path.startsWith("spacing.")) return `--spacing-${path.slice("spacing.".length)}`;
  if (path.startsWith("radius.")) return `--radius-${path.slice("radius.".length)}`;
  if (path.startsWith("shadow.")) return `--shadow-${path.slice("shadow.".length)}`;
  if (path.startsWith("motion.duration.")) {
    return `--duration-${path.slice("motion.duration.".length)}`;
  }
  if (path.startsWith("motion.easing.")) {
    return `--easing-${path.slice("motion.easing.".length)}`;
  }
  if (path.startsWith("zIndex.")) return `--z-${path.slice("zIndex.".length)}`;
  return `--${path.replaceAll(".", "-")}`;
}

const CSS_GENERIC_FAMILIES = new Set([
  "ui-sans-serif",
  "system-ui",
  "sans-serif",
  "ui-monospace",
  "monospace",
  "serif",
  "cursive",
  "fantasy",
]);

function formatValue(value: unknown): string {
  if (Array.isArray(value)) {
    if (value.every((n) => typeof n === "number")) {
      return `cubic-bezier(${value.join(", ")})`;
    }
    return value
      .map((item) =>
        CSS_GENERIC_FAMILIES.has(String(item)) ? String(item) : `"${item}"`,
      )
      .join(", ");
  }
  if (typeof value === "number") return String(value);
  return String(value);
}

function resolveRaw(
  value: unknown,
  byPath: Map<string, FlatToken>,
  stack: string[] = [],
): unknown {
  if (typeof value !== "string") return value;
  const m = value.match(REF);
  if (!m?.[1]) return value;
  const ref = m[1];
  if (stack.includes(ref)) throw new Error(`Cycle: ${[...stack, ref].join(" -> ")}`);
  const token = byPath.get(ref);
  if (!token) throw new Error(`Unresolved token reference {${ref}}`);
  return resolveRaw(token.value, byPath, [...stack, ref]);
}

function cssRefOrValue(token: FlatToken, byPath: Map<string, FlatToken>): string {
  if (typeof token.value === "string") {
    const m = token.value.match(REF);
    if (m?.[1]) {
      return `var(${cssName(m[1])})`;
    }
  }
  return formatValue(resolveRaw(token.value, byPath));
}

function comment(token: FlatToken | undefined): string {
  return token?.description ? ` /* ${token.description} */` : "";
}

function emitTokensCss(byPath: Map<string, FlatToken>): string {
  const v = (path: string) => {
    const token = byPath.get(path);
    if (!token) throw new Error(`Missing token ${path}`);
    return cssRefOrValue(token, byPath);
  };
  const t = (path: string) => byPath.get(path);

  const core = [
    "ember",
    "gold",
    "slate",
    "paper",
    "mist",
    "ink",
    "muted",
  ] as const;
  const semantic = [
    "success",
    "warning",
    "danger",
    "info",
    "play",
    "forest",
    "mineral",
  ] as const;
  const neutrals = [
    "50",
    "100",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "950",
  ] as const;
  const light = [
    "background",
    "foreground",
    "card",
    "card-foreground",
    "popover",
    "popover-foreground",
    "primary",
    "primary-foreground",
    "secondary",
    "secondary-foreground",
    "muted-bg",
    "muted-foreground",
    "accent",
    "accent-foreground",
    "destructive",
    "destructive-foreground",
    "border",
    "input",
    "ring",
  ] as const;
  const accents = [
    "accent-drawit",
    "accent-formit",
    "accent-play",
    "accent-forest",
    "accent-mineral",
  ] as const;
  const dark = light;

  const coreLines = core.map(
    (name) => `  --${name}: ${v(`color.${name}`)};${comment(t(`color.${name}`))}`,
  );
  const semanticLines = semantic.map(
    (name) => `  --${name}: ${v(`color.${name}`)};${comment(t(`color.${name}`))}`,
  );
  const neutralLines = neutrals.map(
    (step) => `  --neutral-${step}: ${v(`color.neutral.${step}`)};`,
  );
  const lightLines = light.map(
    (name) =>
      `  --${name}: ${v(`semantic.light.${name}`)};${comment(t(`semantic.light.${name}`))}`,
  );
  const accentLines = accents.map(
    (name) => `  --${name}: ${v(`semantic.light.${name}`)};`,
  );
  const darkLines = dark.map(
    (name) =>
      `  --${name}: ${v(`semantic.dark.${name}`)};${comment(t(`semantic.dark.${name}`))}`,
  );

  const extraRoot = [
    `  --radius: ${v("radius.default")};${comment(t("radius.default"))}`,
    `  --font-display: ${v("font.display")};`,
    `  --font-sans: ${v("font.sans")};`,
    `  --font-mono: ${v("font.mono")};`,
    `  --font-weight-regular: ${v("fontWeight.regular")};`,
    `  --font-weight-medium: ${v("fontWeight.medium")};`,
    `  --font-weight-semibold: ${v("fontWeight.semibold")};`,
    `  --font-weight-bold: ${v("fontWeight.bold")};`,
    ...["display", "h1", "h2", "h3", "h4", "body", "small", "caption", "code"].map(
      (step) =>
        `  --font-size-${step}: ${v(`fontSize.${step}`)};\n  --line-height-${step}: ${v(`lineHeight.${step}`)};`,
    ),
    ...["0", "1", "2", "3", "4", "5", "6", "8", "10", "12", "16", "20", "24"].map(
      (step) => `  --spacing-${step}: ${v(`spacing.${step}`)};`,
    ),
    `  --duration-fast: ${v("motion.duration.fast")};`,
    `  --duration-base: ${v("motion.duration.base")};`,
    `  --duration-slow: ${v("motion.duration.slow")};`,
    `  --easing-out: ${v("motion.easing.out")};`,
    `  --easing-standard: ${v("motion.easing.standard")};`,
    `  --z-base: ${v("zIndex.base")};`,
    `  --z-dropdown: ${v("zIndex.dropdown")};`,
    `  --z-sticky: ${v("zIndex.sticky")};`,
    `  --z-overlay: ${v("zIndex.overlay")};`,
    `  --z-modal: ${v("zIndex.modal")};`,
    `  --z-toast: ${v("zIndex.toast")};`,
    `  --z-tooltip: ${v("zIndex.tooltip")};`,
  ];

  const themeColors = [
    ...core,
    ...semantic,
    ...neutrals.map((step) => `neutral-${step}`),
  ];
  const themeColorLines = themeColors.map((name) => {
    const path = name.startsWith("neutral-")
      ? `color.neutral.${name.slice("neutral-".length)}`
      : `color.${name}`;
    return `  --color-${name}: ${v(path)};`;
  });

  return `/* Chamuka Daybreak — design tokens
   Generated from DTCG JSON in packages/tokens/src/tokens.
   Screen values are authored in sRGB. Print equivalents: see brand/print/README.md
   and brand/colors.json (CMYK method and Pantone nearest-match notes).
*/

:root {
  /* Core */
${coreLines.join("\n")}

  /* Semantic */
${semanticLines.join("\n")}

  /* Neutral ramp */
${neutralLines.join("\n")}

  /* Light theme (default) — shadcn-style */
${lightLines.join("\n")}
${accentLines.join("\n")}

  /* Typography, space, radius, motion, z-index */
${extraRoot.join("\n")}
}

.dark,
[data-theme="dark"] {
${darkLines.join("\n")}
}

/* Tailwind CSS v4 */
@theme {
${themeColorLines.join("\n")}
  --font-display: ${v("font.display")};
  --font-sans: ${v("font.sans")};
  --font-mono: ${v("font.mono")};
  --radius-sm: ${v("radius.sm")};
  --radius-md: ${v("radius.md")};
  --radius-lg: ${v("radius.lg")};
  --radius-xl: ${v("radius.xl")};
  --shadow-sm: ${v("shadow.sm")};
  --shadow-md: ${v("shadow.md")};
  --shadow-lg: ${v("shadow.lg")};
}
`;
}

function emitThemeCss(byPath: Map<string, FlatToken>): string {
  const v = (path: string) => {
    const token = byPath.get(path);
    if (!token) throw new Error(`Missing token ${path}`);
    return cssRefOrValue(token, byPath);
  };

  const primitives = [
    "ember",
    "gold",
    "slate",
    "paper",
    "mist",
    "ink",
    "muted",
    "success",
    "warning",
    "danger",
    "info",
    "play",
    "forest",
    "mineral",
  ];
  const neutrals = [
    "50",
    "100",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "950",
  ];
  const semantic = [
    "background",
    "foreground",
    "card",
    "card-foreground",
    "popover",
    "popover-foreground",
    "primary",
    "primary-foreground",
    "secondary",
    "secondary-foreground",
    "accent",
    "accent-foreground",
    "destructive",
    "destructive-foreground",
    "border",
    "input",
    "ring",
  ];

  const colorLines = [
    ...primitives.map((name) => `  --color-${name}: ${v(`color.${name}`)};`),
    ...neutrals.map((step) => `  --color-neutral-${step}: ${v(`color.neutral.${step}`)};`),
    ...semantic.map((name) => `  --color-${name}: var(--${name});`),
    `  --color-muted: var(--muted-bg);`,
    `  --color-muted-foreground: var(--muted-foreground);`,
  ];

  return `/* Tailwind CSS v4 @theme — import after tokens.css */
@theme {
${colorLines.join("\n")}
  --font-display: ${v("font.display")};
  --font-sans: ${v("font.sans")};
  --font-mono: ${v("font.mono")};
  --radius-sm: ${v("radius.sm")};
  --radius-md: ${v("radius.md")};
  --radius-lg: ${v("radius.lg")};
  --radius-xl: ${v("radius.xl")};
  --shadow-sm: ${v("shadow.sm")};
  --shadow-md: ${v("shadow.md")};
  --shadow-lg: ${v("shadow.lg")};
  --spacing-1: ${v("spacing.1")};
  --spacing-2: ${v("spacing.2")};
  --spacing-3: ${v("spacing.3")};
  --spacing-4: ${v("spacing.4")};
  --spacing-5: ${v("spacing.5")};
  --spacing-6: ${v("spacing.6")};
  --spacing-8: ${v("spacing.8")};
  --spacing-10: ${v("spacing.10")};
  --spacing-12: ${v("spacing.12")};
  --spacing-16: ${v("spacing.16")};
  --text-display: ${v("fontSize.display")};
  --text-display--line-height: ${v("lineHeight.display")};
  --text-h1: ${v("fontSize.h1")};
  --text-h1--line-height: ${v("lineHeight.h1")};
  --text-h2: ${v("fontSize.h2")};
  --text-h2--line-height: ${v("lineHeight.h2")};
  --text-h3: ${v("fontSize.h3")};
  --text-h3--line-height: ${v("lineHeight.h3")};
  --text-h4: ${v("fontSize.h4")};
  --text-h4--line-height: ${v("lineHeight.h4")};
  --text-body: ${v("fontSize.body")};
  --text-body--line-height: ${v("lineHeight.body")};
  --z-index-dropdown: ${v("zIndex.dropdown")};
  --z-index-sticky: ${v("zIndex.sticky")};
  --z-index-overlay: ${v("zIndex.overlay")};
  --z-index-modal: ${v("zIndex.modal")};
  --z-index-toast: ${v("zIndex.toast")};
  --z-index-tooltip: ${v("zIndex.tooltip")};
  --duration-fast: ${v("motion.duration.fast")};
  --duration-base: ${v("motion.duration.base")};
  --duration-slow: ${v("motion.duration.slow")};
}
`;
}

function jsLiteral(value: unknown): string {
  const resolved = value;
  if (Array.isArray(resolved)) return JSON.stringify(resolved);
  if (typeof resolved === "number") return String(resolved);
  return JSON.stringify(resolved);
}

function emitTs(byPath: Map<string, FlatToken>): string {
  const resolved = (path: string) => {
    const token = byPath.get(path);
    if (!token) throw new Error(`Missing token ${path}`);
    return resolveRaw(token.value, byPath);
  };

  const colorEntries = [
    "ember",
    "gold",
    "slate",
    "paper",
    "mist",
    "ink",
    "muted",
    "success",
    "warning",
    "danger",
    "info",
    "play",
    "forest",
    "mineral",
    "white",
  ].map((name) => `    ${name}: ${jsLiteral(resolved(`color.${name}`))},`);

  const neutralEntries = [
    "50",
    "100",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "950",
  ].map((step) => `      "${step}": ${jsLiteral(resolved(`color.neutral.${step}`))},`);

  const semanticKeys = [
    "background",
    "foreground",
    "card",
    "cardForeground",
    "popover",
    "popoverForeground",
    "primary",
    "primaryForeground",
    "secondary",
    "secondaryForeground",
    "mutedBg",
    "mutedForeground",
    "accent",
    "accentForeground",
    "destructive",
    "destructiveForeground",
    "border",
    "input",
    "ring",
  ] as const;
  const semanticPaths: Record<(typeof semanticKeys)[number], string> = {
    background: "background",
    foreground: "foreground",
    card: "card",
    cardForeground: "card-foreground",
    popover: "popover",
    popoverForeground: "popover-foreground",
    primary: "primary",
    primaryForeground: "primary-foreground",
    secondary: "secondary",
    secondaryForeground: "secondary-foreground",
    mutedBg: "muted-bg",
    mutedForeground: "muted-foreground",
    accent: "accent",
    accentForeground: "accent-foreground",
    destructive: "destructive",
    destructiveForeground: "destructive-foreground",
    border: "border",
    input: "input",
    ring: "ring",
  };

  const themeBlock = (theme: "light" | "dark") =>
    semanticKeys
      .map(
        (key) =>
          `      ${key}: ${jsLiteral(resolved(`semantic.${theme}.${semanticPaths[key]}`))},`,
      )
      .join("\n");

  const accentBlock = [
    `      drawit: ${jsLiteral(resolved("semantic.light.accent-drawit"))},`,
    `      formit: ${jsLiteral(resolved("semantic.light.accent-formit"))},`,
    `      play: ${jsLiteral(resolved("semantic.light.accent-play"))},`,
    `      forest: ${jsLiteral(resolved("semantic.light.accent-forest"))},`,
    `      mineral: ${jsLiteral(resolved("semantic.light.accent-mineral"))},`,
  ].join("\n");

  return `/* Generated from DTCG JSON. Do not edit. */
export const color = {
${colorEntries.join("\n")}
    neutral: {
${neutralEntries.join("\n")}
    },
} as const;

export const semantic = {
    light: {
${themeBlock("light")}
      productAccent: {
${accentBlock}
      },
    },
    dark: {
${themeBlock("dark")}
    },
} as const;

export const fontFamily = {
    display: ${jsLiteral(resolved("font.display"))},
    sans: ${jsLiteral(resolved("font.sans"))},
    mono: ${jsLiteral(resolved("font.mono"))},
} as const;

export const fontWeight = {
    regular: ${jsLiteral(resolved("fontWeight.regular"))},
    medium: ${jsLiteral(resolved("fontWeight.medium"))},
    semibold: ${jsLiteral(resolved("fontWeight.semibold"))},
    bold: ${jsLiteral(resolved("fontWeight.bold"))},
} as const;

export const fontSize = {
    display: ${jsLiteral(resolved("fontSize.display"))},
    h1: ${jsLiteral(resolved("fontSize.h1"))},
    h2: ${jsLiteral(resolved("fontSize.h2"))},
    h3: ${jsLiteral(resolved("fontSize.h3"))},
    h4: ${jsLiteral(resolved("fontSize.h4"))},
    body: ${jsLiteral(resolved("fontSize.body"))},
    small: ${jsLiteral(resolved("fontSize.small"))},
    caption: ${jsLiteral(resolved("fontSize.caption"))},
    code: ${jsLiteral(resolved("fontSize.code"))},
} as const;

export const lineHeight = {
    display: ${jsLiteral(resolved("lineHeight.display"))},
    h1: ${jsLiteral(resolved("lineHeight.h1"))},
    h2: ${jsLiteral(resolved("lineHeight.h2"))},
    h3: ${jsLiteral(resolved("lineHeight.h3"))},
    h4: ${jsLiteral(resolved("lineHeight.h4"))},
    body: ${jsLiteral(resolved("lineHeight.body"))},
    small: ${jsLiteral(resolved("lineHeight.small"))},
    caption: ${jsLiteral(resolved("lineHeight.caption"))},
    code: ${jsLiteral(resolved("lineHeight.code"))},
} as const;

export const spacing = {
    0: ${jsLiteral(resolved("spacing.0"))},
    1: ${jsLiteral(resolved("spacing.1"))},
    2: ${jsLiteral(resolved("spacing.2"))},
    3: ${jsLiteral(resolved("spacing.3"))},
    4: ${jsLiteral(resolved("spacing.4"))},
    5: ${jsLiteral(resolved("spacing.5"))},
    6: ${jsLiteral(resolved("spacing.6"))},
    8: ${jsLiteral(resolved("spacing.8"))},
    10: ${jsLiteral(resolved("spacing.10"))},
    12: ${jsLiteral(resolved("spacing.12"))},
    16: ${jsLiteral(resolved("spacing.16"))},
    20: ${jsLiteral(resolved("spacing.20"))},
    24: ${jsLiteral(resolved("spacing.24"))},
} as const;

export const radius = {
    sm: ${jsLiteral(resolved("radius.sm"))},
    md: ${jsLiteral(resolved("radius.md"))},
    lg: ${jsLiteral(resolved("radius.lg"))},
    xl: ${jsLiteral(resolved("radius.xl"))},
    full: ${jsLiteral(resolved("radius.full"))},
    default: ${jsLiteral(resolved("radius.default"))},
} as const;

export const shadow = {
    sm: ${jsLiteral(resolved("shadow.sm"))},
    md: ${jsLiteral(resolved("shadow.md"))},
    lg: ${jsLiteral(resolved("shadow.lg"))},
} as const;

export const motion = {
    duration: {
        fast: ${jsLiteral(resolved("motion.duration.fast"))},
        base: ${jsLiteral(resolved("motion.duration.base"))},
        slow: ${jsLiteral(resolved("motion.duration.slow"))},
    },
    easing: {
        out: ${jsLiteral(resolved("motion.easing.out"))},
        standard: ${jsLiteral(resolved("motion.easing.standard"))},
    },
} as const;

export const zIndex = {
    base: ${jsLiteral(resolved("zIndex.base"))},
    dropdown: ${jsLiteral(resolved("zIndex.dropdown"))},
    sticky: ${jsLiteral(resolved("zIndex.sticky"))},
    overlay: ${jsLiteral(resolved("zIndex.overlay"))},
    modal: ${jsLiteral(resolved("zIndex.modal"))},
    toast: ${jsLiteral(resolved("zIndex.toast"))},
    tooltip: ${jsLiteral(resolved("zIndex.tooltip"))},
} as const;

export const tokens = {
    color,
    semantic,
    fontFamily,
    fontWeight,
    fontSize,
    lineHeight,
    spacing,
    radius,
    shadow,
    motion,
    zIndex,
} as const;

export type Tokens = typeof tokens;
`;
}

function main() {
  const flat = loadTokens();
  const byPath = new Map(flat.map((token) => [token.path, token]));
  mkdirSync(DIST, { recursive: true });
  writeFileSync(join(DIST, "tokens.css"), emitTokensCss(byPath));
  writeFileSync(join(DIST, "theme.css"), emitThemeCss(byPath));
  writeFileSync(GENERATED, emitTs(byPath));
  console.log("wrote dist/tokens.css, dist/theme.css, src/generated.ts");
}

main();

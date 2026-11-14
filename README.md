# Chamuka design system (Daybreak)

Daybreak is the master brand and UI/UX design system for everything [chamuka-inc](https://chamuka.ai) builds. This repository holds the brand pack, design tokens, React components, generated logo icons, Storybook, and reusable surface templates.

Packages are private (`@chamuka/*`). Do not publish them to npm.

## Folder map

```
.
├── apps/docs                 Storybook 8 (components, tokens, guidelines)
├── brand/                    Logo masters, print, colour/type/voice docs, Python generators
│   ├── svg/ png/ mockups/    Asset names unchanged from the original pack
│   ├── print/                One-ink SVGs, print templates, merch mockups
│   ├── docs/                 Colour, type, voice
│   └── scripts/              _build.py, _templates.py, _surfaces.py
├── packages/tokens           @chamuka/tokens — DTCG JSON → CSS, Tailwind, TS
├── packages/ui               @chamuka/ui — React 19 + Radix components
├── packages/icons            @chamuka/icons — Daybreak mark/lockups as React
├── templates/                Digital surfaces (GitHub, OG, slides, email, web)
├── turbo.json                pnpm + Turborepo pipelines
└── .github/workflows/ci.yml  install --frozen-lockfile, build, lint, typecheck, test, build-storybook
```

Print templates stay under `brand/print/templates` (millimetre artboards with bleed). Digital surfaces stay at `/templates` so product apps can find them next to the design system rather than inside the print pack.

## Quick start

```bash
pnpm install
pnpm build
pnpm test
pnpm --filter @chamuka/docs dev
```

Requires Node 22+ and pnpm 10.

## Consume in a Next.js app (DrawIt, FormIt, Play)

Workspace dependency, not a public registry package. Add `@chamuka/tokens` and `@chamuka/ui` to the app. Import CSS once in the root layout. Wrap the tree with `ThemeProvider`.

### Tailwind v4

```css
@import "tailwindcss";
@import "@chamuka/tokens/tokens.css";
@import "@chamuka/tokens/theme.css";
@import "@chamuka/ui/styles.css";
```

`tokens.css` defines `:root` and `.dark, [data-theme="dark"]` shadcn-style variables. `theme.css` maps them onto Tailwind v4 `@theme` so `bg-background`, `text-ember`, and `font-display` work.

### Tailwind v3

```ts
import type { Config } from "tailwindcss";
import chamuka from "@chamuka/tokens/preset";

export default {
  presets: [chamuka],
  content: [
    "./src/**/*.{ts,tsx}",
    "./node_modules/@chamuka/ui/dist/**/*.js",
  ],
  darkMode: ["class"],
} satisfies Config;
```

```ts
import "@chamuka/tokens/tokens.css";
import "@chamuka/ui/styles.css";
```

### React

```tsx
import { ThemeProvider, Button, ToastProvider, TooltipProvider } from "@chamuka/ui";
import { LockupHorizontal } from "@chamuka/icons";

export function App({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider defaultTheme="system">
      <ToastProvider>
        <TooltipProvider>
          <LockupHorizontal title="Chamuka" height={32} />
          <Button>Save</Button>
          {children}
        </TooltipProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}
```

Core `--muted` is Daybreak muted ink. The muted *surface* is `--muted-bg` so it does not collide with shadcn’s `--muted`.

## Brand regeneration

```bash
python brand/scripts/_build.py
python brand/scripts/_templates.py
python brand/scripts/_surfaces.py
```

If the palette changes, update both the Python `PALETTE` and `packages/tokens/src/tokens` so brand files and `@chamuka/tokens` stay aligned.

## Licence

Copyright © Chamuka. All rights reserved. A licence has not yet been added. Do not assume the files are open source.

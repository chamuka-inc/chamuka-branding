# `@chamuka/tokens`

Daybreak design tokens. DTCG JSON in `src/tokens` is the source of truth. The build emits:

- `tokens.css` — primitives and shadcn-style semantic variables on `:root`, dark overrides on `.dark` and `[data-theme="dark"]`, plus a Tailwind v4 `@theme` block
- `theme.css` — Tailwind v4 `@theme` with `bg-background` / `text-foreground` utilities
- `preset` — Tailwind v3 preset
- typed JS/TS exports

## Consume

### CSS variables (any stack)

```ts
import "@chamuka/tokens/tokens.css";
```

### Tailwind v4

```css
@import "tailwindcss";
@import "@chamuka/tokens/tokens.css";
@import "@chamuka/tokens/theme.css";
```

### Tailwind v3

```ts
import type { Config } from "tailwindcss";
import chamuka from "@chamuka/tokens/preset";

export default {
  presets: [chamuka],
  content: ["./src/**/*.{ts,tsx}"],
  darkMode: ["class"],
} satisfies Config;
```

Import `tokens.css` in the app root so semantic `var(--primary)` colours resolve.

### TypeScript

```ts
import { color, semantic, fontSize } from "@chamuka/tokens";

color.ember; // "#E24E1B"
semantic.light.primary;
```

## Notes

Core `--muted` is the Daybreak muted ink (`#6B645C`). Shadcn’s muted *surface* is `--muted-bg` so the two do not collide. Map Tailwind `muted` to `--muted-bg` (the v3 preset already does this).

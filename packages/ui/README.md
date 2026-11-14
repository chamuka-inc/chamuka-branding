# `@chamuka/ui`

React 19 components for Chamuka products. **Look:** Tailwind utilities + `cva` + Daybreak tokens. **Behaviour:** [UI SDK](https://github.com/vercel-labs/ui) (`@ui-sdk/react` / `@ui-sdk/core` 0.1.0-beta.2) for interactive components, wrapped so public props stay stable.

Light and dark via `ThemeProvider` (`class="dark"` and `data-theme`).

## Install

Published on GitHub Packages (not npmjs yet). Copy the repo `.npmrc.example`, then `pnpm add @chamuka/ui @chamuka/tokens`.

```ts
import "@chamuka/tokens/tokens.css";
import "@chamuka/tokens/theme.css";
import { ThemeProvider, Button, ToastProvider, TooltipProvider } from "@chamuka/ui";
```

Scan this package with Tailwind (`@source` / `content` glob on `node_modules/@chamuka/ui/dist/**/*.js`) or import `@chamuka/ui/styles.css` as a precompiled fallback.

```tsx
<ThemeProvider defaultTheme="system">
  <ToastProvider>
    <TooltipProvider>{children}</TooltipProvider>
  </ToastProvider>
</ThemeProvider>
```

## Components

**UI SDK:** Dialog, Popover, DropdownMenu, Select, Combobox, Tabs, Tooltip, Toast, Checkbox, RadioGroup, Switch, Accordion, Label.

**Plain:** Button, IconButton, Link, Input, Textarea, Card, Badge, Alert, Skeleton, Spinner, Stack, Container, ThemeProvider.

**Radix (presentational leftovers):** Avatar, Separator.

Primary buttons use ember. Ember on paper is 3.74:1 — labels are 16 px (14 px minimum, medium weight) so they pass AA large.

See [`AGENTS.md`](./AGENTS.md) and [`src/catalog.ts`](./src/catalog.ts).

## Accessibility

UI SDK supplies keyboard behaviour and ARIA on interactive components. Focus is `:focus-visible` with `--ring`. Motion respects `prefers-reduced-motion`. Pair every Checkbox, Switch, and Radio with a Label. IconButton requires `label`.

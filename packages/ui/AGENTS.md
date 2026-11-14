# `@chamuka/ui`

React 19 components. **Look** is Tailwind + `cva` + Daybreak tokens. **Behaviour** for interactive components is UI SDK (`@ui-sdk/react` / `@ui-sdk/core` **0.1.0-beta.2**), wrapped so public props stay Chamuka-shaped.

Source of truth for the inventory: [`src/catalog.ts`](./src/catalog.ts) (generated into `/manifest.json` and `/registry`).

## Layers

- **plain** — Button, IconButton, Link, Input, Textarea, Card, Badge, Alert, Skeleton, Spinner, Stack, Container, ThemeProvider. React + Tailwind. Radix `Slot` only for `asChild` on Button/Link.
- **ui-sdk** — Dialog, Popover, DropdownMenu, Select, Combobox, Tabs, Tooltip, Toast, Checkbox, RadioGroup, Switch, Accordion, Label. Wrap `@ui-sdk/react/<entry>`. Pin exact versions. Do not export UI SDK types.
- **radix** — Avatar (`@radix-ui/react-avatar` image fallback), Separator (`@radix-ui/react-separator`). UI SDK ships both; we kept Radix because these are presentational, not keyboard/ARIA behaviour.

If UI SDK cannot do a component well (missing primitive, a11y gap, SSR/React 19 bug), keep or restore Radix and set `behaviour: "radix"` plus `behaviourReason` in `catalog.ts`.

## Extending vs restyling

- Restyle: edit Tailwind classes in the wrapper. Keep `cn` + `cva`. Target `data-open`, `data-checked`, `data-selected`, `data-highlighted` from UI SDK — not `data-[state=open]` unless the wrapper still uses Radix.
- New behaviour: `npx skills add vercel-labs/ui --skill ui-sdk`, then `definePrimitive` + `createParts`. Read `node_modules/@ui-sdk/react/docs/llms.txt`.
- `asChild` → UI SDK `render={<Child />}`. Never add an `as` prop.

## Tailwind scan

Consumers must `@source` `node_modules/@chamuka/ui/dist/**/*.js` (v4) or add that glob to v3 `content`, **or** import `@chamuka/ui/styles.css` (precompiled fallback).

## Tests

`src/components.test.tsx` — axe (color-contrast off in jsdom). `src/interactions.test.tsx` — keyboard for Tabs, Dialog, Checkbox, Switch, Accordion. Add a keyboard case when you add an interactive component.

jsdom is missing Web Animations, Popover CSS, and `CSS.supports`. `src/test/setup.ts` polyfills those the same way UI SDK's own test mount does. Do not treat a jsdom gap as a reason to drop back to Radix.

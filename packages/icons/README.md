# `@chamuka/icons`

React components generated from Daybreak SVG masters in `brand/svg`. Fills stay as authored — do not recolour the sun, horizon, or gold bar.

```tsx
import { Mark, LockupHorizontal, LockupDrawIt } from "@chamuka/icons";

<LockupHorizontal title="Chamuka" height={32} />
<LockupDrawIt title="Chamuka DrawIt" height={32} />
```

Pass `title` for an accessible name. Without `title`, the SVG is `aria-hidden`.

## What’s generated

- Mark: `Mark`, `MarkSimple`, colour plates, mono dark/light
- Lockups: horizontal, stacked, mono, product lockups (DrawIt, FormIt, Play, Waypoint, Vmette)
- Wordmark and product app icons

Diagrams (`donts`, `clear-space`, `min-sizes`) stay in `brand/svg` and are not components.

## Lucide for UI icons

Product chrome (navigation, actions, status) uses [Lucide](https://lucide.dev) at 1.5–2 px stroke, currentColor. Do not redraw the Daybreak mark in Lucide. Do not mix another icon set into product UI.

```tsx
import { Plus } from "lucide-react";
import { IconButton } from "@chamuka/ui";

<IconButton label="Add row">
  <Plus strokeWidth={1.75} />
</IconButton>
```

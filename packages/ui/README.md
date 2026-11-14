# `@chamuka/ui`

React 19 components for Chamuka products. Built on Radix primitives, styled with Daybreak tokens (`@chamuka/tokens`). Light and dark via `ThemeProvider` (`class="dark"` and `data-theme`).

## Install in an app

Workspace package — not published to npm. In a chamuka-inc app:

```ts
import "@chamuka/tokens/tokens.css";
import "@chamuka/ui/styles.css";
import { ThemeProvider, Button, ToastProvider, TooltipProvider } from "@chamuka/ui";
```

Wrap the tree:

```tsx
<ThemeProvider defaultTheme="system">
  <ToastProvider>
    <TooltipProvider>{children}</TooltipProvider>
  </ToastProvider>
</ThemeProvider>
```

## Components

Button, IconButton, Link, Input, Textarea, Select, Checkbox, RadioGroup, Switch, Label / Field (help + error), Card, Badge, Avatar, Tooltip, Dialog, Popover, DropdownMenu, Tabs, Toast, Alert, Skeleton, Spinner, Separator, Stack, Container, ThemeProvider.

Primary buttons use ember. Ember on paper is 3.74:1 — labels are 16 px (14 px minimum, medium weight) so they pass AA large.

## Accessibility

Radix supplies keyboard behaviour and ARIA. Focus is `:focus-visible` with `--ring`. Motion respects `prefers-reduced-motion`. Pair every Checkbox, Switch, and Radio with a Label. IconButton requires `label`.

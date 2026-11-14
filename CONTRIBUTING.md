# Contributing

Thanks for helping with Daybreak, the brand and UI system for [Chamuka Labs](https://chamuka.ai).

Please read the [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you agree to follow it.

## Setup

Requires Node 22+ and [pnpm](https://pnpm.io) 10.

```bash
pnpm install
pnpm build
pnpm test
```

Storybook (component docs):

```bash
pnpm --filter @chamuka/docs dev
```

Then open http://localhost:6006.

Agents: start at [`AGENTS.md`](./AGENTS.md) and [`llms.txt`](./llms.txt).

## Commands

| Command | What it does |
|---|---|
| `pnpm build` | Build tokens, UI, and icons |
| `pnpm lint` | ESLint across packages |
| `pnpm typecheck` | TypeScript `--noEmit` |
| `pnpm test` | Vitest (axe + keyboard on UI) |
| `pnpm generate:agent` | Rewrite `manifest.json` and `registry/` from `packages/ui/src/catalog.ts` |
| `pnpm build-storybook` | Static Storybook |
| `pnpm changeset` | Record a version bump for `@chamuka/*` |

CI on pull requests runs build, lint, typecheck, test, `generate:agent` (must be a no-op diff), and Storybook.

## Changesets

This repo versions `@chamuka/tokens`, `@chamuka/ui`, and `@chamuka/icons` with [Changesets](https://github.com/changesets/changesets).

If your PR changes a published package, run `pnpm changeset` and commit the file under `.changeset/`. Releases publish to **GitHub Packages** from `main` (not npmjs). Public npm can come later.

Do not publish from your laptop. Do not push to `main`.

## How to add a component

1. Decide the **behaviour layer** (see `packages/ui/AGENTS.md`):
   - **plain** — presentational (Button, Card, Badge, …): React + Tailwind + `cva`.
   - **ui-sdk** — interactive (Dialog, Select, Tabs, …): wrap `@ui-sdk/react`, pin exact versions, keep Chamuka public props.
   - **radix** — only if UI SDK cannot do it well; record why in `packages/ui/src/catalog.ts`.
2. Add the source under `packages/ui/src/`, export it from `packages/ui/src/index.ts`.
3. Add a row to `packages/ui/src/catalog.ts` (`behaviour` + `behaviourReason`).
4. Add a Storybook story under `apps/docs/src/components/`.
5. Add an axe case in `packages/ui/src/components.test.tsx`. For interactive components, add a keyboard case in `packages/ui/src/interactions.test.tsx`.
6. Run `pnpm generate:agent` so `manifest.json` and `registry/` stay in sync.
7. Run `pnpm changeset` if `@chamuka/ui` should bump.

Install the UI SDK skill before extending behaviour:

```bash
npx skills add vercel-labs/ui --skill ui-sdk
```

## Brand assets

Logo masters live in `/brand`. Do not recolour the sun, horizon, or gold bar. Marks and names are covered by [`TRADEMARKS.md`](./TRADEMARKS.md): forks must rebrand.

If the palette changes, update both `packages/tokens/src/tokens` and `brand/scripts` `PALETTE`.

## Pull request checklist

- [ ] `pnpm build`, `pnpm lint`, `pnpm typecheck`, and `pnpm test` pass
- [ ] `pnpm generate:agent` produces no git diff
- [ ] Storybook story exists for a new component
- [ ] Axe (and keyboard, if interactive) coverage added
- [ ] Changeset included when a published package changes
- [ ] Public props stay Chamuka-shaped (do not re-export UI SDK types)
- [ ] Copy follows [`brand/docs/voice.md`](./brand/docs/voice.md) — no lab tagline; “From thoughts to form” is DrawIt only

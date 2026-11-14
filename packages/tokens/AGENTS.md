# `@chamuka/tokens`

DTCG JSON in `src/tokens` is the source of truth. `src/build.ts` emits `dist/tokens.css`, `dist/theme.css`, and `src/generated.ts`.

- `tokens.css` — `:root` primitives + shadcn semantic vars; dark on `.dark, [data-theme="dark"]`; Tailwind v4 `@theme` primitives.
- `theme.css` — maps semantic CSS vars onto Tailwind v4 `--color-primary` etc. so `bg-primary` and `text-muted-foreground` work. `--color-muted` is `var(--muted-bg)` (surface), not core `--muted` (ink).
- `preset` — Tailwind v3 preset. Pair with `tokens.css`. `content` in the app must include `@chamuka/ui/dist/**/*.js`.

If you change a colour, update **both** `src/tokens` and `brand/scripts` `PALETTE` so brand assets stay aligned.

Do not put component styles here. This package is the token layer only.

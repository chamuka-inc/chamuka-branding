# `@chamuka/docs`

Storybook 8 (`react-vite`) for Daybreak. Fonts via `@fontsource`. Tailwind v4 via `@tailwindcss/vite` and `@source` on `packages/ui/src`.

Stories must cover every public `@chamuka/ui` export used in apps, including Accordion and Combobox. Theme toolbar toggles `ThemeProvider`. Do not import `@chamuka/ui/styles.css` here — the `@source` path is the one consuming apps should copy.

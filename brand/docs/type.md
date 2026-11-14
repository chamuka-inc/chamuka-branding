# Type

Three families, no substitutes in product UI. Wordmark outlines in the SVGs are Sora SemiBold, so printers do not need the font files.

| Role | Family | Weights |
|---|---|---|
| Display, headings, wordmark | **Sora** | 500 / 600 / 700 |
| UI and body | **IBM Plex Sans** | 400 / 500 / 600 |
| Code and tabular data | **IBM Plex Mono** | 400 / 500 |

Load them through `@fontsource` (see `apps/docs`) or a licensed self-host. Do not silently fall back to Geist, Inter, or system UI for product chrome.

## Scale

Sizes are px / line-height, with the intended weight.

| Step | Size / line | Weight | Family |
|---|---|---|---|
| Display | 56 / 64 | 600 | Sora |
| H1 | 40 / 48 | 600 | Sora |
| H2 | 32 / 40 | 600 | Sora |
| H3 | 24 / 32 | 600 | Sora |
| H4 | 20 / 28 | 500 | Sora |
| Body | 16 / 24 | 400 | IBM Plex Sans |
| Small | 14 / 20 | 400 | IBM Plex Sans |
| Caption | 12 / 16 | 400 | IBM Plex Sans |
| Code | 14 / 22 | 400 | IBM Plex Mono |

Body copy is 16 / 24 in IBM Plex Sans. Display and heroes are Sora 600. Ember and gold are not paragraph colours.

## Pairing with colour

- Titles in ink (or paper on ink / slate bands).
- Secondary lines in muted.
- Product names in the product accent, IBM Plex Sans Medium, at 0.72 of the wordmark size — never a second display face.
- Tabular numbers and code in IBM Plex Mono so columns hold.

## Tracking and measure

Default tracking is 0. Sora at display size can take a hair of negative tracking; do not letterspace body copy. Aim for 45–75 characters per line in reading text. On marketing heroes, shorter lines are fine.

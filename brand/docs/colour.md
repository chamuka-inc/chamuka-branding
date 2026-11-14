# Colour

Daybreak colour is warm, high-contrast, and rooted in morning light: ember sun, slate horizon, gold bar, morning paper, and ink. It should feel African-rooted and adult, not toy-like. Business teams read long forms and dashboards in these colours — contrast and restraint matter more than saturation.

Screen values are sRGB. Print equivalents, CMYK method, and Pantone nearest-match caveats live in [`../colors.json`](../colors.json) and [`../print/README.md`](../print/README.md). Product UI should consume [`@chamuka/tokens`](../../packages/tokens), not copy hex values into app CSS.

## Core

| Token | Hex | Role |
|---|---|---|
| Ember | `#E24E1B` | Master primary. DrawIt accent. Buttons and the sun. Not body text. |
| Gold | `#E6B422` | Horizon bar and highlights. Never body text on paper. Never a product accent. |
| Slate | `#2B4C7E` | Horizon rule, FormIt accent, supporting headings, info. |
| Morning paper | `#FFF8F1` | Default light background. |
| Mist | `#F3EBE0` | Subtle surfaces, chips, secondary fills. |
| Ink | `#17141C` | Text, chrome, mono lockups. |
| Muted | `#6B645C` | Secondary text (AA on paper: 5.54:1). |

## Semantic

| Token | Hex | Use |
|---|---|---|
| Success | `#1F8A5B` | Large text / icons on paper (4.12:1, AA large only). Darken for small text. |
| Warning | `#E0A100` | On ink only. Fails on paper. |
| Danger | `#C5362B` | Errors. AA on paper (5.07:1). |
| Info | `#2B4C7E` | Same as slate. |

## Product accents

Do not recolour the sun, horizon, or gold bar. Accents colour the product name in a Chamuka + Name lockup, the app-icon field, and selected / primary controls on that product’s surfaces.

| Accent | Hex | Example |
|---|---|---|
| Coral (`play`) | `#D9487A` | Play — playful but adult |
| Forest | `#2F6B4F` | Waypoint — calm green |
| Mineral | `#1F7A6B` | Vmette — infra / platform |
| Ember | `#E24E1B` | DrawIt |
| Slate | `#2B4C7E` | FormIt |

## Neutral ramp

`#FBF7F2` 50 · `#F3EBE0` 100 · `#E6D9C8` 200 · `#D0C0AA` 300 · `#B3A28A` 400 · `#8F8170` 500 · `#6B645C` 600 · `#524C46` 700 · `#3A3531` 800 · `#241F1C` 900 · `#17141C` 950.

## Contrast (selected)

Computed WCAG 2.x ratios; full table in `colors.json`.

- Ink on paper **17.30 AAA**; slate on paper **8.18 AAA**; muted on paper **5.54 AA**.
- Ember on paper **3.74, fails AA for small text**, passes AA large. Use ember for buttons, marks, and display. White on ember is the same ratio — large UI only (16 px+ / 14 px bold).
- Gold on paper fails; gold on ink **9.47 AAA**.
- Success on paper **4.12** — large text / icons only.
- Play on paper **3.87** — large UI only.

## Light and dark UI

Light theme sits on paper with ink text. Dark theme sits on ink (`#17141C`) with paper text. Dark **primary** lifts ember to `#F06A3A` so filled buttons hold contrast on ink. Dark **accent** lifts slate to `#7FA0D4` for text and links; fills may still use `#2B4C7E`. Dark **destructive** is `#E0564A`.

Do not invent a second palette for a campaign or a product shell. Dark bands on a light marketing page may use ink or slate with paper type.

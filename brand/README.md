# Chamuka brand system (Daybreak)

Daybreak is the master brand for everything chamuka-inc builds or communicates. This folder holds logo masters, colour documentation, print files, and the Python generators. Screen tokens for product UI live in [`@chamuka/tokens`](../packages/tokens); this folder keeps a regenerated snapshot at `tokens.css` for brand QA.

Website: [chamuka.ai](https://chamuka.ai). Email uses the `@chamuka.ai` domain; `name@chamuka.ai` in templates is a **placeholder** for a person’s address, not a real inbox. Product sites follow the pattern `drawit.chamuka.ai` and `formit.chamuka.ai` (examples). Do not invent social handles — leave them as placeholders until they are confirmed.

## Folder map

```
brand/
├── README.md                 This file
├── docs/                     Colour, type, and voice
├── tokens.css                Regenerated screen snapshot (apps should use @chamuka/tokens)
├── colors.json               Hex, RGB, HSL, contrast, and print notes
├── scripts/                  _build.py, _templates.py, _surfaces.py
├── svg/                      Logo and lockup SVG masters (outlined type)
├── png/                      Raster previews of the logo masters
├── mockups/                  Product UI photo mockups
└── print/
    ├── README.md             CMYK, Pantone method, sizes, bleed, apparel
    ├── svg/                  One-ink and knockout constructions
    ├── png/                  Print preview rasters
    ├── templates/            Business card, sticker sheet, A2 poster, roll-up
    └── mockups/              Apparel, mug/tote, cards, event banner photos
```

Digital surface templates (GitHub, OG, slides, email, web) live at [`/templates`](../templates) so they sit beside the product design system rather than inside the print pack.

Start from the SVGs, not the PNGs, for any production use. PNG previews are for checking, not for print.

## How to use the logos

- **Master lockup (default):** `svg/lockup-horizontal.svg`. Stacked: `svg/lockup-stacked.svg`. Mark alone: `svg/mark.svg`.
- **Small / embroidery / screen print:** `svg/mark-simple.svg` (horizon removed, bar thickened). Use the full mark at 24 px tall and above on screen, and at 10 mm tall and above in print. Below that, or whenever the horizon would print thinner than 0.3 mm, switch to the simple mark. Favicons at 16 and 32 px already use it.
- **Minimum horizontal lockup:** 120 px wide on screen, 32 mm wide in print.
- **Clear space:** one sun radius on every side (half the disc diameter), equal to 0.36 × the optical mark height (disc top to gold-bar bottom).
- **Colourways:** colour on cream, knockout on ember or slate, and mono ink / light plates are in `svg/` and `png/`.
- **Sub-brands:** a named product uses a Chamuka + Name lockup (`svg/lockup-drawit.svg` and the other examples). The Name is IBM Plex Sans Medium, in the product accent, at 0.72 of the wordmark size. Do not recolour the sun, horizon, or gold bar. Do not drop “Chamuka” from the lockup. Product icons are the mark knocked out on a 22% rounded square in the accent; at 16 / 32 px use the simple mark.
- **Don’ts:** see `svg/donts.svg` — do not stretch, rotate, recolour the sun, drop the bar or horizon, outline the mark, add a drop shadow, or place it on a busy photograph without a solid plate.
- Wordmark outlines are Sora SemiBold, so printers do not need the font.

DrawIt, FormIt, Play, Waypoint, and Vmette in this pack are worked examples of the sub-brand pattern, not a closed product list.

In product UI, prefer the React components in [`@chamuka/icons`](../packages/icons) over inlining these SVGs.

## Colour, type, and voice

See [docs/colour.md](docs/colour.md), [docs/type.md](docs/type.md), and [docs/voice.md](docs/voice.md). Ember `#E24E1B` is the master primary, but it is not body text (3.74:1 on paper — fails WCAG AA for small text, passes AA large). Ink, slate, and muted carry the reading. Gold is a highlight, never a paragraph colour on paper, and never a product accent.

## Regenerating

From the repository root, with the brand Python environment (font files, cairosvg, uharfbuzz, fontTools, Pillow):

```bash
python brand/scripts/_build.py
python brand/scripts/_templates.py
python brand/scripts/_surfaces.py
```

`_build.py` writes logo masters, rasters, and `colors.json` under `brand/`. `_templates.py` writes print templates, `brand/tokens.css`, and `brand/print/README.md`. `_surfaces.py` writes digital surfaces under `/templates` and extra product lockups under `brand/svg`. Domain, site URL, and the email placeholder are constants in `_build.py` (`SITE_HOST`, `SITE_URL`, `EMAIL_PLACEHOLDER`). These scripts do not overwrite the root README.

If the Daybreak palette changes, update both the Python `PALETTE` and the DTCG JSON in `packages/tokens` so brand files and `@chamuka/tokens` stay aligned.

## Print colour caveats

Physical items use the same mark and palette. One-ink, knockout, and simple (no-horizon) constructions are in `print/svg/`. See `print/README.md` for CMYK method, Pantone nearest-match notes, sizes, bleed, and apparel.

**Print colour is a starting point, not a contract.** Never treat Pantone numbers as official equivalents.

## Licence

Copyright © Chamuka. All rights reserved.

A licence for this brand pack has not yet been added. Do not assume the files are open source, and do not publish or redistribute them until a licence is in place.

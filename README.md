# Chamuka brand system (Daybreak)

Daybreak is the master brand for everything chamuka-inc builds or communicates. This folder is the working pack of logo masters, colour tokens, print files, and reusable surface templates. The live guide is the brand Page; this repository is the source of the files.

Website: [chamuka.ai](https://chamuka.ai). Email uses the `@chamuka.ai` domain; `name@chamuka.ai` in templates is a **placeholder** for a person’s address, not a real inbox. Product sites follow the pattern `drawit.chamuka.ai` and `formit.chamuka.ai` (examples). Do not invent social handles — leave them as placeholders until they are confirmed.

## Folder map

Paths below are the layout in this pack. They are stable; scripts and docs refer to them. An optional future tidy is noted at the end, but files have not been moved.

```
.
├── README.md                 This file
├── tokens.css                Screen tokens (light / dark, shadcn-style, Tailwind v4 @theme)
├── colors.json               Hex, RGB, HSL, contrast, and print notes
├── _build.py                 Shared geometry, palette, SITE_HOST / SITE_URL / EMAIL_PLACEHOLDER
├── _templates.py             Builds print templates, tokens.css, print/README.md
├── _surfaces.py              Builds digital surface templates and templates/README.md
├── page.canvas.tsx           Local snapshot; the live Page is on Canvas (may lag)
├── svg/                      Logo and lockup SVG masters (outlined type)
├── png/                      Raster previews of the logo masters
├── mockups/                  Product UI photo mockups
├── templates/                Digital surfaces
│   ├── README.md             Sizes, safe areas, substitution rules
│   ├── email-signature.html
│   ├── *.svg                 GitHub, README, docs, X, LinkedIn, OG, slides, web, repo tone
│   └── png/                  Preview rasters
└── print/
    ├── README.md             CMYK, Pantone method, sizes, bleed, apparel guidance
    ├── svg/                  One-ink and knockout constructions
    ├── png/                  Print preview rasters (including crops / bleed marks)
    ├── templates/            Business card, sticker sheet, A2 poster, roll-up
    └── mockups/              Apparel, mug/tote, cards, event banner photos
```

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

## How to use the tokens

- `tokens.css` — core palette, semantic colours, product accents (including forest and mineral), a light and `.dark` shadcn-style variable set, and a Tailwind CSS v4 `@theme` block.
- `colors.json` — the same palette with RGB, HSL, and contrast figures.
- Ember `#E24E1B` is the master primary, but it is not body text (3.74:1 on paper — fails WCAG AA for small text, passes AA large). Ink, slate, and muted carry the reading. Gold is a highlight, never a paragraph colour on paper, and never a product accent.
- Type: Sora 500 / 600 / 700 for display, headings, and the wordmark; IBM Plex Sans 400 / 500 / 600 for UI and body; IBM Plex Mono for code and tabular data. Scale: display 56/64 600; h1 40/48 600; h2 32/40 600; h3 24/32 600; h4 20/28 500; body 16/24 400; small 14/20; caption 12/16; code 14/22 Mono.

## How to use the templates

Reusable masters live in `templates/`. Full sizes, safe areas, and substitution rules are in `templates/README.md`.

| Surface | File | Size |
|---|---|---|
| GitHub social preview | `github-social-preview.svg` | 1280 × 640 |
| README banner | `readme-banner.svg` | 1280 × 400 |
| Docs header | `docs-header.svg` (product example also supplied) | 1600 × 200 |
| X post | `x-post.svg` | 1600 × 900 |
| X header | `x-header.svg` — keep the bottom-left clear of the profile avatar | 1500 × 500 |
| LinkedIn post | `linkedin-post.svg` | 1200 × 627 |
| Open Graph / link preview | `og-image.svg` | 1200 × 630 |
| Slides (title, section, content) | `slide-title.svg`, `slide-section.svg`, `slide-content.svg` | 1920 × 1080 |
| Email signature | `email-signature.html` plus a mark PNG to host | HTML table, system sans |
| Web / landing guidance | `web-landing.svg`, tied to `tokens.css` | 1440 × 900 |
| Repo naming and description tone | `github-repo-naming.svg` and `templates/README.md` | — |

Use the master lockup on org and company surfaces; swap in a Chamuka + Name lockup and the product accent when the surface belongs to a sub-brand. Do not invent a second banner style. In the email signature, replace Name, Role, and `name@chamuka.ai` (a placeholder). Website footers and social/OG templates use `chamuka.ai`.

Print templates (business card 85 × 55 mm with 3 mm bleed, sticker sheet, A2 poster, 850 × 2000 mm roll-up) are in `print/templates/`, with notes in `print/README.md`.

To regenerate previews after a change, from this folder, with the brand Python environment:

```bash
python _templates.py
python _surfaces.py
```

Domain, site URL, and the email placeholder are constants in `_build.py` (`SITE_HOST`, `SITE_URL`, `EMAIL_PLACEHOLDER`) so regenerating stays on `chamuka.ai`. Those scripts update `tokens.css`, `print/README.md`, and `templates/README.md`. They do not overwrite this `README.md`.

## Print colour caveats

Physical items use the same mark and palette. One-ink, knockout, and simple (no-horizon) constructions are in `print/svg/`.

**Print colour is a starting point, not a contract.** CMYK values were separated from sRGB with LittleCMS, using Ghostscript’s sRGB profile and the Artifex CMYK SWOP profile, Relative Colorimetric intent. That is a US SWOP-like coated separation — not FOGRA39 / ISO Coated v2, and not GRACoL 2013. A European printer should re-separate to FOGRA39; a North American printer should re-separate to GRACoL if that is the house profile.

Pantone numbers in `print/README.md` and on the brand Page are **nearest matches**, ranked by CIEDE2000 against commonly circulated Color Bridge / converter screen hexes, which are not official Pantone measurements. Uncoated recommendations are the same PMS number in the Uncoated library. Verify every match against a physical Pantone guide before printing. Never treat them as official equivalents.

Morning paper and mist should be specified as stock, not as a printed fill. For ink, prefer a rich black such as C60 M40 Y40 K100, or process black — not the heavy SWOP build of `#17141C`.

## Licence

Copyright © Chamuka. All rights reserved.

A licence for this brand pack has not yet been added. Do not assume the files are open source, and do not publish or redistribute them until a licence is in place.

## Optional future layout

The current paths are already usable in a `chamuka-inc/chamuka-branding` repo. A slightly tidier tree, if it is ever worth a mechanical move, would be:

```
logo/svg/          (today: svg/)
logo/png/          (today: png/)
tokens/tokens.css, tokens/colors.json
scripts/_build.py, _templates.py, _surfaces.py
```

Do not move those files until every script, README, and Page path has been updated in the same change. `templates/` and `print/` can stay as they are.


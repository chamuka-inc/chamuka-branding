# Daybreak print and merchandise

Masters in `svg/` and `templates/`. Preview rasters in `png/` and `mockups/`. Production should start from the SVGs, not the PNGs.

The website is chamuka.ai. Email uses the @chamuka.ai domain; `name@chamuka.ai` on the business card is a placeholder. Product sites follow the pattern drawit.chamuka.ai and formit.chamuka.ai (examples).

Print files use Daybreak marks. Names and logos are covered by [`TRADEMARKS.md`](../../TRADEMARKS.md); the repository code is Apache 2.0. Forks must rebrand.

## How the print values were made

**CMYK.** Separated from sRGB with LittleCMS (Pillow ImageCms) using Ghostscript’s sRGB profile and the **Artifex CMYK SWOP** profile (`default_cmyk.icc`), Relative Colorimetric intent, values rounded to whole percentages. This is a US SWOP-like coated separation. It is **not** FOGRA39 / ISO Coated v2 and **not** GRACoL 2013 (CRPC6). A European printer should re-separate to FOGRA39 (ISO Coated v2 300%) in prepress; a North American printer should re-separate to GRACoL 2013 if that is the house profile. Treat the builds below as starting points.

**Pantone.** Coated nearest matches were ranked with CIEDE2000 (D65/2°, sRGB-encoded Lab) against a compiled table of commonly circulated Color Bridge / converter *screen* hex approximations. Those hex values are **not official Pantone-published measurements**. Uncoated recommendations are the **same PMS number in the Uncoated library** (the conventional C/U pairing), not a separately measured nearest-U. **Every entry is a nearest match — verify against a physical Pantone Coated or Uncoated guide before printing. Never treat these as official equivalents.**

Paper and mist are backgrounds: prefer an unprinted cream / off-white stock over a printed fill. Any named PMS for them is a distant nearest (ΔE well above 5) and will look like a tan or grey wash, not morning paper.

For typography in four-colour process, do not use the heavy SWOP conversion of ink (C75 M70 Y62 K87). Prefer a rich black such as C60 M40 Y40 K100, or process black, and reserve Black 6 as a spot if ink is printed solid.

## Core colours — CMYK and nearest Pantone

All Pantone rows: **nearest match, verify against a physical Pantone guide before printing.**

| Colour | Hex | CMYK (SWOP, RelCol, starting point) | Nearest Pantone Coated (ΔE00) | Other close C | Uncoated (same number) |
|---|---|---|---|---|---|
| Ember | `#E24E1B` | C6 87 100 1 | Pantone 1665 C (ΔE 2.83, screen approx #DC4405) | Pantone 166 C (ΔE 3.24), Pantone 7625 C (ΔE 3.24) | Pantone 1665 U |
| Gold | `#E6B422` | C11 30 100 0 | Pantone 7409 C (ΔE 2.94, #F0B323) | Pantone 110 C (ΔE 3.36), Pantone 7408 C (ΔE 3.5) | Pantone 7409 U |
| Slate | `#2B4C7E` | C100 83 26 11 | Pantone 7686 C (ΔE 2.99, #1D4F91) | Pantone 7687 C (ΔE 2.99), Pantone 7693 C (ΔE 2.99) | Pantone 7686 U |
| Morning paper | `#FFF8F1` | C0 3 4 0 | Do not print a fill if a cream stock can be specified. Distant nearest Pantone 663 C (ΔE 7.68) is not a visual match. | Pantone Cool Gray 1 C (ΔE 7.72), Pantone Warm Gray 1 C (ΔE 8.43) | Specify uncoated cream / off-white stock |
| Mist | `#F3EBE0` | C4 6 11 0 | Prefer a tint of stock or a 5–10% warm-grey wash. Distant nearest Pantone Warm Gray 1 C (ΔE 5.97). | Pantone Cool Gray 1 C (ΔE 6.21), Pantone 7527 C (ΔE 6.47) | Specify stock or a light warm-grey U |
| Ink | `#17141C` | C75 70 62 87 (too heavy for type — see note above) | Pantone Black 6 C (ΔE 6.62, #101820) | Pantone Neutral Black C (ΔE 6.8), Pantone 7547 C (ΔE 7.84) | Pantone Black 6 U |
| Muted | `#6B645C` | C55 54 61 28 | Pantone Warm Gray 11 C (ΔE 2.64, #6E6259) | Pantone Cool Gray 11 C (ΔE 9.55), Pantone 448 C (ΔE 14.23) | Pantone Warm Gray 11 U |
| Success | `#1F8A5B` | C89 23 87 9 | Pantone 7725 C (ΔE 4.07, #06815B) | Pantone 7724 C (ΔE 4.79), Pantone 335 C (ΔE 6.14) | Pantone 7725 U |
| Warning | `#E0A100` | C12 40 100 0 | Pantone 143 C (ΔE 2.05, #E5A823) | Pantone 7550 C (ΔE 2.4), Pantone 124 C (ΔE 2.61) | Pantone 143 U |
| Danger | `#C5362B` | C16 98 100 7 | Pantone 180 C (ΔE 2.08, #C52928) | Pantone 7626 C (ΔE 2.67), Pantone 711 C (ΔE 2.82) | Pantone 180 U |
| Play accent | `#D9487A` | C10 92 30 0 | Pantone 205 C (ΔE 1.2, #E0457B) | Pantone 7424 C (ΔE 2.72), Pantone 213 C (ΔE 4.69) | Pantone 205 U |

Info uses the same values as slate.

## One-ink, knockout, screen print and embroidery

| File | Use |
|---|---|
| `svg/mark-ink-on-light.svg`, `svg/lockup-ink-on-light.svg` | Single ink (ink / black) on a light stock or light garment |
| `svg/lockup-white-on-ember.svg`, `svg/mark-white-on-ember.svg` | Knockout / white ink on an ember field or ember garment |
| `svg/lockup-white-on-slate.svg`, `svg/mark-white-on-slate.svg` | Knockout / white ink on slate |
| `svg/mark-knockout.svg` | White mark, no background, for placing on a coloured field |
| `svg/mark-simple-one-colour-ink.svg` (and `-ember`, `-white`) | **Preferred for screen print and embroidery** |
| `svg/lockup-simple-one-colour-*.svg` | Lockup, same construction |

The thin horizon rule is 1.25 units in a 64-unit mark (about 2.8% of the optical height). It will fall apart below about 0.3 mm in offset, and it will not hold in embroidery or in most screen printing.

**At small sizes, and always for screen print and embroidery, use the simple mark:** drop the horizon entirely and keep the thickened gold bar. If a three-colour (ember / slate / gold) print is required at larger sizes, thicken the horizon to at least 0.4 mm (preferably 0.5–0.6 mm) rather than attempting the hairline.

Embroidery notes: simple mark only; minimum 12 mm tall; satin-stitch the bar as a column; fill or satin the disc; do not program a run stitch under 1 mm for the horizon.

## Minimum print sizes and clear space

- Full colour mark (with horizon): **10 mm** tall, optical (disc top to bar bottom).
- Simple mark: **8 mm** tall (12 mm for embroidery).
- Horizontal lockup: **32 mm** wide.
- Stacked lockup: **18 mm** wide (wordmark).
- Below **12 mm** mark height, switch to the simple mark so the horizon is not asked to print.
- Clear space: **one sun radius** on every side, equal to **0.36 × optical mark height** (for a 10 mm mark, leave 3.6 mm).
- Bleed: **3 mm** on business cards and stickers; **5 mm** on posters and banners. Keep type and the lockup inside a **5 mm** safe area on cards, **12 mm** on posters, **40 mm** side / **80 mm** top on a roll-up.
- Roll-up cassette: reserve the bottom **250 mm** — no type or logo.

## Templates

All template SVGs are in millimetres, with bleed, trim and safe guides (cyan / magenta / green) and crop marks. **Do not print the guides or the caption.** Delete or hide the `#guides` layer before going to plate.

- `templates/business-card-front.svg` and `business-card-back.svg` — 85 × 55 mm trim, 3 mm bleed. Front: cream, colour lockup, chamuka.ai. Back: ember field, knockout mark, placeholder name / role / name@chamuka.ai (an address placeholder). Replace the name and role.
- `templates/sticker-sheet.svg` — A5 landscape sheet: 50 mm round colour mark, 40 mm ember and slate knockouts, a die-cut mark (kiss-cut around the sun and bar), and a wordmark pill. Dashed strokes are die lines.
- `templates/poster-a2.svg` — 420 × 594 mm trim, 5 mm bleed.
- `templates/rollup-banner.svg` — 850 × 2000 mm, 5 mm bleed, cassette zone marked.

Preview PNGs in `png/` are for review only (well below production resolution on the poster and banner).

## Apparel, mugs, totes

**T-shirt and hoodie, left chest.** Simple or colour mark **40–50 mm** tall, or a horizontal lockup **80–100 mm** wide. Place 20–30 mm below the shoulder seam and 70–90 mm from the centre front (so it sits on the chest, not the shoulder). On light garments use the colour or ink-on-light lockup; on ember, slate, or black garments use the knockout / white version. At chest size the horizon may be kept if it prints at ≥ 0.4 mm; otherwise use the simple mark.

**Back print.** Horizontal or stacked lockup **180–250 mm** wide, 80–120 mm below the collar. Hoodies can combine a small left-chest mark with a larger back wordmark.

**Sleeve.** Simple mark **35–45 mm** tall, mid upper sleeve, aligned to the garment grain. No horizon.

**Mug.** Lockup or mark opposite the handle, **50–70 mm** wide, centred in the printable band (often about 70–80 mm tall). Prefer the simple mark on a curved, small print area. Allow for the handle exclusion and wrap limits of the chosen print process (ceramic decal, dye-sub, or screen).

**Tote.** Centre the horizontal lockup, **160–200 mm** wide, with the top of the artwork about 120–150 mm down from the bag opening. Colour on natural / cream cotton; knockout on ember or slate bags.

For all garments, send the vendor the one-colour simple SVG plus a colour reference (Pantone, labelled as a nearest match to verify) and a placement sketch. Do not send a screenshot of a mockup as the master.

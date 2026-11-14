# Daybreak surface templates

Reusable masters for the places **Chamuka Labs** shows up online and in documents. Chamuka Labs is an applied AI lab; experiments such as DrawIt and FormIt are sub-brands. Production starts from the SVGs (and the HTML signature). PNG previews are for review.

The website is chamuka.ai. Email uses the @chamuka.ai domain; in templates, name@chamuka.ai is a placeholder for the person’s address. Product sites follow the pattern drawit.chamuka.ai and formit.chamuka.ai (examples). Do not invent social handles — leave them as placeholders until they are confirmed.

**Do not put “From thoughts to form” on lab or org templates.** That line is DrawIt’s only. Do not invent a lab slogan. Names and Daybreak marks: [`TRADEMARKS.md`](../TRADEMARKS.md).

All templates use the Daybreak core: morning paper `#FFF8F1`, ink `#17141C`, ember `#E24E1B`, gold `#E6B422`, slate `#2B4C7E`, and Sora + IBM Plex Sans (outlined in the SVGs). Swap in a **Chamuka + Name** lockup and the product accent when the surface belongs to a sub-brand; use the master lockup for lab, hiring, and company channels.

Hide any leftover notes before publishing. Safe-area guidance is in this file, not drawn on the art.

## Sizes

| Surface | File | Size (px) |
|---|---|---|
| GitHub social preview | `github-social-preview.svg` | 1280 × 640 |
| README banner | `readme-banner.svg` | 1280 × 400 |
| Docs header (master) | `docs-header.svg` | 1600 × 200 |
| Docs header, product example | `docs-header-product-example.svg` | 1600 × 200 |
| X post | `x-post.svg` | 1600 × 900 |
| X header / banner | `x-header.svg` | 1500 × 500 |
| LinkedIn post | `linkedin-post.svg` | 1200 × 627 |
| Open Graph / link preview | `og-image.svg` | 1200 × 630 |
| Slide — title | `slide-title.svg` | 1920 × 1080 |
| Slide — section | `slide-section.svg` | 1920 × 1080 |
| Slide — content | `slide-content.svg` | 1920 × 1080 |
| Email signature | `email-signature.html` | — |
| Email signature preview | `email-signature-preview.svg` | 720 × 220 |
| Web / landing guidance | `web-landing.svg` | 1440 × 900 |
| Repo naming examples | `github-repo-naming.svg` | 1280 × 720 |

Previews: `png/`.

## GitHub social preview and README banner

GitHub may crop the social preview slightly. Keep the lockup and any line of type at least 64 px from every edge. The README banner is shorter (1280 × 400) so it does not dominate a repository page. For a product repo, replace the master lockup with the Chamuka + Name lockup; do not invent a second banner style.

## Docs header

A 1600 × 200 bar for documentation sites. Master lockup on the left, “Documentation” (or the page family) on the right, gold rule along the bottom. The product example shows Chamuka FormIt — use that pattern whenever the docs belong to a sub-brand. Background is morning paper; type is ink and muted.

## X and LinkedIn

- **X post (1600 × 900).** A 16:9 image for a post. Cream field, master or product lockup, one short headline, a gold rule, chamuka.ai. Do not fill the frame with body copy.
- **X header (1500 × 500).** Slate field, knockout lockup. The profile avatar overlaps the bottom-left of the banner. Keep the lockup and type out of the left 240 × 180 px at the bottom. Vertically centre the lockup in the remaining safe area.
- **LinkedIn post (1200 × 627).** Same family as the OG image. Use the master lockup for company posts; a product lockup only when the post is clearly about that product.

## Open Graph

`og-image.svg` is 1200 × 630, the common link-preview size. Use it as the default `og:image` and Twitter `summary_large_image`. Product sites may substitute the Chamuka + Name lockup and, if needed, a thin accent rule in the product colour instead of gold — do not recolour the sun.

## Slides

Three 16:9 (1920 × 1080) layouts:

- **Title** — cream, lockup, a Sora title, a Plex subtitle, chamuka.ai in the footer.
- **Section** — slate field, knockout lockup, gold “Section 0X”, a short Sora title.
- **Content** — cream, small lockup in the header, a content title, two optional columns of Plex, a quiet footer.

Keep margins at 96 px. Ember is for emphasis, not for paragraphs. Titles in Sora, body in IBM Plex Sans. Do not stretch the mark to fill a title slide.

## Email signature

`email-signature.html` is a table-based signature for inbox clients. Host `png/email-signature-mark.png` (or the SVG) and update the `img src`. Do not depend on Sora loading in the inbox — Helvetica / Arial / IBM Plex Sans if available is enough for the type. Colours are inline. Replace Name, Role, and the email address. Do not add a slogan under the name; chamuka.ai is enough. name@chamuka.ai in the signature is a placeholder — replace with the person’s address.

## Repo naming and description tone

Visual examples: `github-repo-naming.svg`.

- Public name: Chamuka Labs. GitHub owner: `chamuka-labs`.
- User-facing products and tools: `chamuka-<name>` in lowercase kebab-case (`chamuka-drawit`, `chamuka-formit`). Do not use camelCase in the repo name.
- Shared libraries: `@chamuka/<package>` on the registry, `chamuka-<package>` in GitHub (for example `chamuka-ui`).
- Infra and platform that are not a named product may drop the product suffix (`vmette`, `chamuka` for the platform) — but the README still opens as Chamuka, not as a private nickname.
- Descriptions are one sentence, what the thing is, no trailing exclamation mark, no emoji, no “best”, no marketing puff. Play stays adult in the org listing even if the product itself is more playful.
- The first line of the README should be able to replace the GitHub description without a rewrite.

## Web and landing pages

`web-landing.svg` is a guidance frame, not a finished site. Tie implementation to `tokens.css`:

- Page background `--paper` (`#FFF8F1`), body `--ink`, secondary `--muted`.
- Display and heroes in **Sora 600**; UI and body in **IBM Plex Sans 16/24**; code in **IBM Plex Mono**.
- Primary CTA is ember on company pages, or the product accent on a product page. Ember on paper is 3.74:1 — use 16 px+ / medium weight labels (AA large). Do not set body copy in ember or gold.
- Secondary buttons: slate stroke or mist fill.
- Radius 8 px for buttons, 12 px for cards. Shadows are warm and quiet (`tokens.css`).
- Motion 150–300 ms ease-out; honour `prefers-reduced-motion`.
- Icons: Lucide, 1.5–2 px strokes.
- Dark bands may use ink or slate with paper type; lifted ember `#F06A3A` is the dark-mode primary in `tokens.css`.
- The header uses the master lockup on company pages and the Chamuka + Name lockup on product pages. Do not introduce a new logo for a campaign.

## Sub-brand substitution

On any of these surfaces, a sub-brand swaps only:

1. The lockup (Chamuka + Name, name in the product accent).
2. The product icon, if an icon is needed — the Daybreak mark on a rounded square in the accent (22% corner).
3. The primary button / selected state colour.

Everything else — paper, ink, type, radius, the sun-and-horizon mark itself — stays Daybreak.

#!/usr/bin/env python3
"""Daybreak surface templates, example sub-brand lockups, and PNG previews."""
from __future__ import annotations

import sys
from pathlib import Path

import cairosvg

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
REPO = ROOT.parent
sys.path.insert(0, str(SCRIPTS))
from _build import (  # noqa: E402
    HORIZON_X1,
    HORIZON_X2,
    MARK_BOT,
    MARK_H,
    MARK_TOP,
    PALETTE,
    PLEX_MD,
    PLEX_RG,
    SORA_MD,
    SORA_SB,
    lockup_horizontal,
    lockup_stacked,
    mark_elements,
    paths_to_el,
    shape_paths,
    svg_doc,
    write,
    SITE_HOST,
    SITE_URL,
    EMAIL_PLACEHOLDER,
    contrast_ratio,
    wcag_level,
    hex_to_rgb,
    rgb_to_hsl,
    srgb_to_cmyk_swop,
)

ember, gold, slate = PALETTE["ember"], PALETTE["gold"], PALETTE["slate"]
ink, paper, white, mist = PALETTE["ink"], PALETTE["paper"], PALETTE["white"], PALETTE["mist"]
muted, coral = PALETTE["muted"], PALETTE["play"]
FOREST = "#2F6B4F"
MINERAL = "#1F7A6B"

TPL = REPO / "templates"
TPNG = TPL / "png"
SVG = ROOT / "svg"
PNG = ROOT / "png"
for d in (TPL, TPNG, SVG, PNG):
    d.mkdir(parents=True, exist_ok=True)


def raster(svg_path: Path, png_path: Path, output_width=None, background=None):
    kw = {"url": str(svg_path), "write_to": str(png_path)}
    if output_width:
        kw["output_width"] = output_width
    else:
        # keep native pixel size from width/height attributes
        kw["output_width"] = None
    if background:
        kw["background_color"] = background
    if output_width:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=output_width, background_color=background) if background else cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=output_width)
    else:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), background_color=background) if background else cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))
    print("png", png_path)


def px_svg(w, h, body, bg=None):
    bg_el = f'<rect width="{w}" height="{h}" fill="{bg}"/>\n  ' if bg else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n'
        f"  {bg_el}{body}\n"
        f"</svg>\n"
    )


def place_h_lockup(x, y, target_h, product=None, pf=None, knockout=False, sun=None, ho=None, go=None, wf=None):
    su = paper if knockout else (sun or ember)
    hor = paper if knockout else (ho or slate)
    go_ = paper if knockout else (go or gold)
    wf_ = paper if knockout else (wf or ink)
    w, h, body, vb, *rest = lockup_horizontal(su, hor, go_, wf_, product, pf, pad=0)
    scale = target_h / 64
    g = f'<g transform="translate({x:.3f} {y:.3f}) scale({scale:.5f})">\n{body}\n  </g>'
    return g, w * scale, 64 * scale


def place_s_lockup(x, y, target_w, product=None, pf=None, knockout=False):
    su, hor, go_, wf_ = (paper, paper, paper, paper) if knockout else (ember, slate, gold, ink)
    w, h, body, vb = lockup_stacked(su, hor, go_, wf_, product, pf, pad=0)
    scale = target_w / w
    g = f'<g transform="translate({x:.3f} {y:.3f}) scale({scale:.5f})">\n{body}\n  </g>'
    return g, w * scale, h * scale


def text_at(font, string, size, fill, x, y):
    sh = shape_paths(font, string, size)
    el = f'<g transform="translate({x:.3f} {y:.3f})">\n      {paths_to_el(sh["paths"], fill)}\n    </g>'
    return el, sh


def centered(font, string, size, fill, cx, y):
    sh = shape_paths(font, string, size)
    x = cx - sh["width"] / 2
    el = f'<g transform="translate({x:.3f} {y:.3f})">\n      {paths_to_el(sh["paths"], fill)}\n    </g>'
    return el, sh


def app_icon_group(cx, cy, size, field, knockout=True):
    """Icon centred at cx,cy, size is the square edge."""
    x, y = cx - size / 2, cy - size / 2
    rr = size * 0.22
    ox0, oy0 = HORIZON_X1, MARK_TOP
    ow, oh = HORIZON_X2 - HORIZON_X1, MARK_H
    fill = 0.54
    scale = (size * fill) / oh
    tx = x + (size - ow * scale) / 2 - ox0 * scale
    ty = y + (size - oh * scale) / 2 - oy0 * scale
    sun = paper if knockout else ember
    ho = paper if knockout else slate
    go = paper if knockout else gold
    inner = mark_elements(sun, ho, go)
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rr}" ry="{rr}" fill="{field}"/>\n'
        f'  <g transform="translate({tx:.3f} {ty:.3f}) scale({scale:.5f})">{inner}</g>'
    )


def example_lockups_and_icons():
    # Sub-brand examples
    for name, accent, fname in (
        ("Waypoint", FOREST, "lockup-waypoint"),
        ("Vmette", MINERAL, "lockup-vmette"),
    ):
        w, h, body, vb, *_ = lockup_horizontal(ember, slate, gold, ink, name, accent)
        write(SVG / f"{fname}.svg", svg_doc(w, h, body, vb=vb))
        w, h, body, vb = lockup_stacked(ember, slate, gold, ink, name, accent, pad=16)
        write(SVG / f"{fname}-stacked.svg", svg_doc(w, h, body, vb=vb))
        # cream preview
        w, h, body, vb, *_ = lockup_horizontal(ember, slate, gold, ink, name, accent)
        write(SVG / f"{fname}-on-cream.svg", svg_doc(w, h, body, vb=vb, bg=paper))
        raster(SVG / f"{fname}-on-cream.svg", PNG / f"{fname}-on-cream.png", output_width=1800)

    # Product icons from the mark
    def icon_svg(size, field):
        # reuse geometry from earlier build: optical centering
        from _build import mark_elements as me
        ox0, oy0 = HORIZON_X1, MARK_TOP
        ox1, oy1 = HORIZON_X2, MARK_BOT
        ow, oh = ox1 - ox0, oy1 - oy0
        scale = (size * 0.54) / oh
        tx = (size - ow * scale) / 2 - ox0 * scale
        ty = (size - oh * scale) / 2 - oy0 * scale
        rr = size * 0.22
        bg = f'<rect width="{size}" height="{size}" rx="{rr}" ry="{rr}" fill="{field}"/>'
        inner = me(paper, paper, paper)
        body = f"{bg}\n  <g transform='translate({tx:.3f} {ty:.3f}) scale({scale:.5f})'>\n    {inner}\n  </g>"
        return svg_doc(size, size, body, vb=f"0 0 {size} {size}")

    write(SVG / "app-icon-waypoint-512.svg", icon_svg(512, FOREST))
    write(SVG / "app-icon-vmette-512.svg", icon_svg(512, MINERAL))
    # Generic "derive an icon" specimen: master cream + five accent plates
    write(SVG / "app-icon-forest-512.svg", icon_svg(512, FOREST))
    write(SVG / "app-icon-mineral-512.svg", icon_svg(512, MINERAL))
    raster(SVG / "app-icon-waypoint-512.svg", PNG / "app-icon-waypoint-512.png", output_width=512)
    raster(SVG / "app-icon-vmette-512.svg", PNG / "app-icon-vmette-512.png", output_width=512)


def github_social():
    W, H = 1280, 640
    g, lw, lh = place_h_lockup(80, 200, 140)
    tag, _ = text_at(PLEX_RG, "Work, come alive.", 36, slate, 80, 200 + lh + 64)
    url, _ = text_at(PLEX_MD, SITE_HOST, 22, muted, 80, H - 72)
    rule = f'<rect x="80" y="{200 + lh + 28}" width="72" height="6" fill="{gold}"/>'
    body = f"{g}\n  {rule}\n  {tag}\n  {url}"
    write(TPL / "github-social-preview.svg", px_svg(W, H, body, bg=paper))
    raster(TPL / "github-social-preview.svg", TPNG / "github-social-preview.png", output_width=W)


def readme_banner():
    W, H = 1280, 400
    g, lw, lh = place_h_lockup(64, (H - 100) / 2, 100)
    tag, tsh = text_at(PLEX_RG, "Work, come alive.", 28, slate, 0, 0)
    # tag to the right of lockup, optically centred
    tx = 64 + lw + 48
    ty = (H - 100) / 2 + 100 * 0.72
    tag = f'<g transform="translate({tx:.3f} {ty:.3f})">{paths_to_el(tsh["paths"], slate)}</g>'
    rule = f'<rect x="{tx}" y="{ty - 36}" width="48" height="4" fill="{gold}"/>'
    body = f"{g}\n  {rule}\n  {tag}"
    write(TPL / "readme-banner.svg", px_svg(W, H, body, bg=paper))
    raster(TPL / "readme-banner.svg", TPNG / "readme-banner.png", output_width=W)


def docs_header():
    W, H = 1600, 200
    g, lw, lh = place_h_lockup(48, (H - 72) / 2, 72)
    # example of a product docs header: Chamuka FormIt on the left, section on the right
    # Master version here; README explains how to swap in a product lockup
    sec, ssh = text_at(PLEX_MD, "Documentation", 22, muted, 0, 0)
    sx = W - 48 - ssh["width"]
    sy = H / 2 + 8
    sec = f'<g transform="translate({sx:.3f} {sy:.3f})">{paths_to_el(ssh["paths"], muted)}</g>'
    line = f'<rect x="0" y="{H-2}" width="{W}" height="2" fill="{gold}"/>'
    body = f"{g}\n  {sec}\n  {line}"
    write(TPL / "docs-header.svg", px_svg(W, H, body, bg=paper))
    raster(TPL / "docs-header.svg", TPNG / "docs-header.png", output_width=W)
    # Product variant as a worked example
    g2, lw2, lh2 = place_h_lockup(48, (H - 72) / 2, 72, product="FormIt", pf=slate)
    write(TPL / "docs-header-product-example.svg", px_svg(W, H, f"{g2}\n  {sec}\n  {line}", bg=paper))
    raster(TPL / "docs-header-product-example.svg", TPNG / "docs-header-product-example.png", output_width=W)


def x_post():
    W, H = 1600, 900
    g, lw, lh = place_h_lockup(120, 260, 150)
    head, _ = text_at(SORA_SB, "Work, come alive.", 64, ink, 120, 260 + lh + 100)
    sub, _ = text_at(PLEX_RG, "The Chamuka brand system, for everything the org builds.", 28, muted, 120, 260 + lh + 150)
    url, _ = text_at(PLEX_MD, SITE_HOST, 24, slate, 120, H - 100)
    rule = f'<rect x="120" y="{260 + lh + 40}" width="80" height="6" fill="{gold}"/>'
    body = f"{g}\n  {rule}\n  {head}\n  {sub}\n  {url}"
    write(TPL / "x-post.svg", px_svg(W, H, body, bg=paper))
    raster(TPL / "x-post.svg", TPNG / "x-post.png", output_width=W)


def x_header():
    # Slate field, knockout lockup. Keep the bottom-left clear of a profile avatar.
    W, H = 1500, 500
    g, lw, lh = place_h_lockup(520, (H - 120) / 2 - 10, 120, knockout=True)
    # visually centre the lockup in the safe zone (away from left avatar)
    # Recentre: safe starts after x=280
    g, lw, lh = place_h_lockup(280 + (W - 280 - 80 - 0) / 2, 0, 120, knockout=True)
    # wait, I need to compute width first
    g0, lw, lh = place_h_lockup(0, 0, 120, knockout=True)
    x = 280 + (W - 280 - 80 - lw) / 2
    y = (H - lh) / 2 - 16
    g, lw, lh = place_h_lockup(x, y, 120, knockout=True)
    tag, tsh = centered(PLEX_RG, "Work, come alive.", 26, gold, W / 2 + 100, y + lh + 48)
    body = f"{g}\n  {tag}"
    write(TPL / "x-header.svg", px_svg(W, H, body, bg=slate))
    raster(TPL / "x-header.svg", TPNG / "x-header.png", output_width=W)


def linkedin_post():
    W, H = 1200, 627
    g, lw, lh = place_h_lockup(80, 180, 120)
    head, _ = text_at(SORA_SB, "Work, come alive.", 48, ink, 80, 180 + lh + 80)
    url, _ = text_at(PLEX_MD, SITE_HOST, 22, slate, 80, H - 72)
    rule = f'<rect x="80" y="{180 + lh + 32}" width="64" height="5" fill="{gold}"/>'
    body = f"{g}\n  {rule}\n  {head}\n  {url}"
    write(TPL / "linkedin-post.svg", px_svg(W, H, body, bg=paper))
    raster(TPL / "linkedin-post.svg", TPNG / "linkedin-post.png", output_width=W)


def og_image():
    W, H = 1200, 630
    g, lw, lh = place_h_lockup(80, 200, 130)
    tag, _ = text_at(PLEX_RG, "Work, come alive.", 36, slate, 80, 200 + lh + 70)
    url, _ = text_at(PLEX_MD, SITE_HOST, 22, muted, 80, H - 70)
    rule = f'<rect x="80" y="{200 + lh + 32}" width="72" height="6" fill="{gold}"/>'
    body = f"{g}\n  {rule}\n  {tag}\n  {url}"
    write(TPL / "og-image.svg", px_svg(W, H, body, bg=paper))
    raster(TPL / "og-image.svg", TPNG / "og-image.png", output_width=W)


def slides():
    W, H = 1920, 1080
    margin = 96

    # Title
    g, lw, lh = place_h_lockup(margin, 280, 140)
    title, _ = text_at(SORA_SB, "A talk title sits here", 72, ink, margin, 280 + lh + 120)
    sub, _ = text_at(PLEX_RG, "Subtitle or speaker line in IBM Plex Sans", 32, muted, margin, 280 + lh + 180)
    url, _ = text_at(PLEX_MD, SITE_HOST, 22, muted, margin, H - 80)
    rule = f'<rect x="{margin}" y="{280 + lh + 48}" width="80" height="6" fill="{gold}"/>'
    write(TPL / "slide-title.svg", px_svg(W, H, f"{g}\n  {rule}\n  {title}\n  {sub}\n  {url}", bg=paper))
    raster(TPL / "slide-title.svg", TPNG / "slide-title.png", output_width=1280)

    # Section — slate field
    label, _ = text_at(PLEX_MD, "Section 02", 28, gold, margin, 360)
    st, _ = text_at(SORA_SB, "A section title", 88, paper, margin, 480)
    g2, lw2, lh2 = place_h_lockup(margin, 80, 72, knockout=True)
    write(TPL / "slide-section.svg", px_svg(W, H, f"{g2}\n  {label}\n  {st}", bg=slate))
    raster(TPL / "slide-section.svg", TPNG / "slide-section.png", output_width=1280)

    # Content
    g3, lw3, lh3 = place_h_lockup(margin, 48, 56)
    ct, _ = text_at(SORA_SB, "Content title", 48, ink, margin, 180)
    # two columns of placeholder body
    col_y = 260
    left_lines = [
        "A short heading",
        "Body text sits in IBM Plex Sans at 16 / 24.",
        "Keep line length comfortable. Use ink on paper.",
    ]
    bits = [g3, ct, f'<rect x="{margin}" y="200" width="64" height="4" fill="{gold}"/>']
    y = col_y
    for i, line in enumerate(left_lines):
        font = SORA_SB if i == 0 else PLEX_RG
        size = 24 if i == 0 else 22
        col = ink if i == 0 else muted
        el, sh = text_at(font, line, size, col, margin, y)
        bits.append(el)
        y += 44 if i == 0 else 36
    y2 = col_y
    right_x = 1040
    right_lines = [
        "Another heading",
        "A second column is optional. Do not pack a slide.",
        "Accent is for emphasis, never for paragraphs.",
    ]
    for i, line in enumerate(right_lines):
        font = SORA_SB if i == 0 else PLEX_RG
        size = 24 if i == 0 else 22
        col = ink if i == 0 else muted
        el, sh = text_at(font, line, size, col, right_x, y2)
        bits.append(el)
        y2 += 44 if i == 0 else 36
    foot, _ = text_at(PLEX_RG, "Chamuka  ·  " + SITE_HOST, 18, muted, margin, H - 64)
    bits.append(foot)
    write(TPL / "slide-content.svg", px_svg(W, H, "\n  ".join(bits), bg=paper))
    raster(TPL / "slide-content.svg", TPNG / "slide-content.png", output_width=1280)


def email_signature():
    # Small mark PNG for the HTML signature
    write(
        TPL / "email-signature-mark.svg",
        svg_doc(64, 64, mark_elements(ember, slate, gold), bg=None),
    )
    raster(TPL / "email-signature-mark.svg", TPNG / "email-signature-mark.png", output_width=80)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Chamuka email signature</title>
</head>
<body style="margin:0;padding:24px;background:#FFF8F1;">
<!-- Daybreak email signature. Host email-signature-mark.png (or the SVG) and update the img src.
     Use a table, not flex or grid. Do not rely on Sora loading in the inbox — system sans is safer for type.
     Colours: ink #17141C, muted #6B645C, ember #E24E1B, slate #2B4C7E, paper #FFF8F1.
     Email name@chamuka.ai is a placeholder; replace with the person’s @chamuka.ai address. Website: https://chamuka.ai -->
<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="font-family:IBM Plex Sans, Helvetica Neue, Arial, sans-serif;color:#17141C;">
  <tr>
    <td valign="top" style="padding-right:14px;">
      <img src="png/email-signature-mark.png" width="40" height="40" alt="Chamuka" style="display:block;border:0;width:40px;height:40px;">
    </td>
    <td valign="top" style="border-left:2px solid #E6B422;padding-left:14px;">
      <p style="margin:0 0 2px 0;font-size:14px;line-height:20px;font-weight:600;color:#17141C;">Name</p>
      <p style="margin:0 0 8px 0;font-size:13px;line-height:18px;color:#6B645C;">Role, Chamuka</p>
      <p style="margin:0;font-size:13px;line-height:18px;">
        <a href="mailto:name@chamuka.ai" style="color:#2B4C7E;text-decoration:none;">name@chamuka.ai</a>
        <span style="color:#6B645C;"> · </span>
        <a href="https://chamuka.ai" style="color:#2B4C7E;text-decoration:none;">chamuka.ai</a>
      </p>
    </td>
  </tr>
</table>
</body>
</html>
"""
    write(TPL / "email-signature.html", html)

    # Visual preview of the signature at a comfortable size
    W, H = 720, 220
    icon = f'<g transform="translate(40 70) scale({80/64:.5f})">{mark_elements(ember, slate, gold)}</g>'
    rule = f'<rect x="140" y="70" width="3" height="80" fill="{gold}"/>'
    n, _ = text_at(SORA_SB, "Name", 22, ink, 160, 96)
    r, _ = text_at(PLEX_RG, "Role, Chamuka", 16, muted, 160, 124)
    e, _ = text_at(PLEX_RG, EMAIL_PLACEHOLDER + "  ·  " + SITE_HOST, 15, slate, 160, 154)
    write(TPL / "email-signature-preview.svg", px_svg(W, H, f"{icon}\n  {rule}\n  {n}\n  {r}\n  {e}", bg=paper))
    raster(TPL / "email-signature-preview.svg", TPNG / "email-signature-preview.png", output_width=W)


def web_landing():
    W, H = 1440, 900
    # Browser chrome suggestion + hero
    chrome = f'<rect x="0" y="0" width="{W}" height="64" fill="{paper}"/>'
    g, lw, lh = place_h_lockup(48, 12, 40)
    nav_items = ["Product", "Docs", "Company"]
    bits = [chrome, g]
    nx = W - 48
    for label in reversed(nav_items + ["Sign in"]):
        font = PLEX_MD if label == "Sign in" else PLEX_RG
        col = ember if label == "Sign in" else ink
        el, sh = text_at(font, label, 16, col, 0, 0)
        nx -= sh["width"] + 36
        bits.append(f'<g transform="translate({nx:.3f} 40)">{paths_to_el(sh["paths"], col)}</g>')
    # Hero
    bits.append(f'<rect x="0" y="64" width="{W}" height="{H-64}" fill="{paper}"/>')
    ht, _ = text_at(SORA_SB, "Work, come alive.", 72, ink, 80, 260)
    bits.append(ht)
    sub, _ = text_at(PLEX_RG, "A short supporting line in IBM Plex Sans. One thought, not a paragraph.", 24, muted, 80, 320)
    bits.append(sub)
    # CTA button
    bits.append(f'<rect x="80" y="370" width="180" height="52" rx="8" fill="{ember}"/>')
    cta, csh = text_at(PLEX_MD, "Get started", 18, white, 0, 0)
    bits.append(f'<g transform="translate({80 + (180-csh["width"])/2:.3f} 404)">{paths_to_el(csh["paths"], white)}</g>')
    bits.append(f'<rect x="272" y="370" width="180" height="52" rx="8" fill="none" stroke="{slate}" stroke-width="1.5"/>')
    cta2, c2 = text_at(PLEX_MD, "Read the docs", 18, slate, 0, 0)
    bits.append(f'<g transform="translate({272 + (180-c2["width"])/2:.3f} 404)">{paths_to_el(c2["paths"], slate)}</g>')
    # Three quiet feature cards
    cards = ["Draw together", "Shape a form", "Run a session"]
    for i, label in enumerate(cards):
        x = 80 + i * 420
        bits.append(f'<rect x="{x}" y="500" width="392" height="220" rx="12" fill="{white}" stroke="{mist}" stroke-width="1"/>')
        bits.append(f'<rect x="{x + 28}" y="528" width="40" height="6" fill="{gold}"/>')
        el, _ = text_at(SORA_SB, label, 22, ink, x + 28, 580)
        bits.append(el)
        bl, _ = text_at(PLEX_RG, "A single sentence in Plex, 16 / 24, ink on paper.", 16, muted, x + 28, 624)
        bits.append(bl)
    foot, _ = text_at(PLEX_RG, SITE_HOST, 16, muted, 80, H - 40)
    bits.append(foot)
    write(TPL / "web-landing.svg", px_svg(W, H, "\n  ".join(bits), bg=paper))
    raster(TPL / "web-landing.svg", TPNG / "web-landing.png", output_width=W)


def github_repo_listing():
    """A visual of repo naming and description tone — not a GitHub UI clone."""
    W, H = 1280, 720
    title, _ = text_at(SORA_SB, "Repo names and descriptions", 36, ink, 64, 80)
    bits = [title]

    examples = [
        ("chamuka-labs/chamuka-drawit", "A canvas for humans and agents.", True),
        ("chamuka-labs/chamuka-formit", "A form builder for business teams.", True),
        ("chamuka-labs/vmette", "MicroVMs for running untrusted code.", True),
        ("chamuka-labs/awesome-drawit!!!", "The BEST drawing app :)", False),
    ]
    y = 140
    for name, desc, good in examples:
        label = "Do" if good else "Don't"
        lcol = FOREST if good else PALETTE["danger"]
        bits.append(f'<rect x="64" y="{y}" width="1152" height="110" rx="12" fill="{white}" stroke="{mist}" stroke-width="1"/>')
        lb, _ = text_at(PLEX_MD, label, 16, lcol, 88, y + 36)
        bits.append(lb)
        nm, _ = text_at(PLEX_MD, name, 22, ink, 88, y + 64)
        bits.append(nm)
        ds, _ = text_at(PLEX_RG, desc, 18, muted, 88, y + 92)
        bits.append(ds)
        y += 128
    write(TPL / "github-repo-naming.svg", px_svg(W, H, "\n  ".join(bits), bg=paper))
    raster(TPL / "github-repo-naming.svg", TPNG / "github-repo-naming.png", output_width=W)


def write_docs():
    md = f"""# Daybreak surface templates

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

`web-landing.svg` is a guidance frame, not a finished site. Tie implementation to `@chamuka/tokens` (and the brand snapshot at `brand/tokens.css`):

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
"""
    write(TPL / "README.md", md)


def patch_tokens_and_root_readme():
    tokens = (ROOT / "tokens.css").read_text()
    needle = "  --play: #D9487A; /* Play product accent only */"
    insert = (
        "  --play: #D9487A; /* Coral — playful-but-adult products (Play is an example) */\n"
        "  --forest: #2F6B4F; /* Forest — calm green products (Waypoint is an example) */\n"
        "  --mineral: #1F7A6B; /* Mineral — infra / platform tools (Vmette is an example) */"
    )
    if needle in tokens and "--forest:" not in tokens:
        tokens = tokens.replace(needle, insert, 1)
        tokens = tokens.replace(
            "  --accent-play: var(--play);\n",
            "  --accent-play: var(--play);\n"
            "  --accent-forest: var(--forest);\n"
            "  --accent-mineral: var(--mineral);\n",
            1,
        )
        tokens = tokens.replace(
            "  --color-play: #D9487A;\n",
            "  --color-play: #D9487A;\n"
            "  --color-forest: #2F6B4F;\n"
            "  --color-mineral: #1F7A6B;\n",
            1,
        )
        write(ROOT / "tokens.css", tokens)

    # Repo README.md is hand-maintained. Do not patch or overwrite it on regenerate.


def main():
    for name, hx in (("forest", FOREST), ("mineral", MINERAL)):
        print(
            name,
            hx,
            "HSL",
            rgb_to_hsl(*hex_to_rgb(hx)),
            "paper",
            round(contrast_ratio(hx, paper), 2),
            wcag_level(contrast_ratio(hx, paper)),
            "ink",
            round(contrast_ratio(hx, ink), 2),
        )
    example_lockups_and_icons()
    github_social()
    readme_banner()
    docs_header()
    x_post()
    x_header()
    linkedin_post()
    og_image()
    slides()
    email_signature()
    web_landing()
    github_repo_listing()
    write_docs()
    patch_tokens_and_root_readme()
    print("SURFACES OK")


if __name__ == "__main__":
    main()

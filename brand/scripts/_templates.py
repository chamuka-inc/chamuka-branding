#!/usr/bin/env python3
"""Print templates, tokens.css, and README files for Daybreak."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cairosvg

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
from _build import (  # noqa: E402
    BAR_H,
    BAR_W,
    BAR_Y,
    CX,
    CY,
    HORIZON_W,
    HORIZON_X1,
    HORIZON_X2,
    HORIZON_Y,
    MARK_BOT,
    MARK_H,
    MARK_TOP,
    PALETTE,
    PLEX_MD,
    PLEX_RG,
    R,
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
    EMAIL_PLACEHOLDER,
)

SVG = ROOT / "svg"
PNG = ROOT / "png"
PRINT = ROOT / "print"
TEMPL = PRINT / "templates"
PRINT_PNG = PRINT / "png"
ember, gold, slate = PALETTE["ember"], PALETTE["gold"], PALETTE["slate"]
ink, paper, white, mist = PALETTE["ink"], PALETTE["paper"], PALETTE["white"], PALETTE["mist"]
muted, play = PALETTE["muted"], PALETTE["play"]


def raster(svg_path, png_path, output_width=None, background=None):
    kw = {"url": str(svg_path), "write_to": str(png_path)}
    if output_width:
        kw["output_width"] = output_width
    if background:
        kw["background_color"] = background
    cairosvg.svg2png(**kw)
    print("png", png_path)


def g_lockup_h(sun, ho, go, wf, product=None, pf=None, simple=False, scale=1, x=0, y=0):
    w, h, body, vb, *rest = lockup_horizontal(sun, ho, go, wf, product, pf, simple, pad=0)
    # vb with pad=0 is "-0 -0 width+0 height+0"? pad=0 -> vb = f"{-0} {-0} {width} {height}"
    # body is in mark/word coordinates with origin at 0,0 of the 64-tall frame
    return f'<g transform="translate({x} {y}) scale({scale})">\n{body}\n</g>', w, h


def g_lockup_s(sun, ho, go, wf, product=None, pf=None, simple=False, scale=1, x=0, y=0):
    w, h, body, vb = lockup_stacked(sun, ho, go, wf, product, pf, simple, pad=0)
    return f'<g transform="translate({x} {y}) scale({scale})">\n{body}\n</g>', w, h


def text_group(font, string, size, fill, x, y, tracking=0):
    """Baseline at y."""
    sh = shape_paths(font, string, size, letter_spacing=tracking)
    el = f'<g transform="translate({x:.3f} {y:.3f})">\n      {paths_to_el(sh["paths"], fill)}\n    </g>'
    return el, sh


def svg_mm(width_mm, height_mm, body, vb=None, extras=""):
    vb = vb or f"0 0 {width_mm} {height_mm}"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_mm}mm" height="{height_mm}mm" '
        f'viewBox="{vb}" fill="none">\n{extras}{body}\n</svg>\n'
    )


def crop_marks(trim_x, trim_y, trim_w, trim_h, len_=4, offset=1.5, color="#17141C"):
    """Crop marks around a trim box, sitting outside the bleed."""
    x0, y0, x1, y1 = trim_x, trim_y, trim_x + trim_w, trim_y + trim_h
    segs = []
    # corners: left-top, right-top, left-bottom, right-bottom — two marks each
    pts = [
        (x0, y0, -1, 0, 0, -1),
        (x1, y0, 1, 0, 0, -1),
        (x0, y1, -1, 0, 0, 1),
        (x1, y1, 1, 0, 0, 1),
    ]
    for x, y, dx, dy, dx2, dy2 in pts:
        segs.append(
            f'<line x1="{x+dx*offset}" y1="{y}" x2="{x+dx*(offset+len_)}" y2="{y}" />'
        )
        segs.append(
            f'<line x1="{x}" y1="{y+dx2*offset if dy==0 else y+dy*offset}" '
            f'x2="{x}" y2="{y+(offset+len_)* (dx2 if dy==0 else dy)}" />'
        )
        # the above is messy; write explicitly below
    marks = f'''  <g stroke="{color}" stroke-width="0.15" fill="none">
    <line x1="{x0-offset-len_}" y1="{y0}" x2="{x0-offset}" y2="{y0}"/>
    <line x1="{x0}" y1="{y0-offset-len_}" x2="{x0}" y2="{y0-offset}"/>
    <line x1="{x1+offset}" y1="{y0}" x2="{x1+offset+len_}" y2="{y0}"/>
    <line x1="{x1}" y1="{y0-offset-len_}" x2="{x1}" y2="{y0-offset}"/>
    <line x1="{x0-offset-len_}" y1="{y1}" x2="{x0-offset}" y2="{y1}"/>
    <line x1="{x0}" y1="{y1+offset}" x2="{x0}" y2="{y1+offset+len_}"/>
    <line x1="{x1+offset}" y1="{y1}" x2="{x1+offset+len_}" y2="{y1}"/>
    <line x1="{x1}" y1="{y1+offset}" x2="{x1}" y2="{y1+offset+len_}"/>
  </g>'''
    return marks


def business_cards():
    bleed = 3
    trim_w, trim_h = 85, 55
    art_w, art_h = trim_w + 2 * bleed, trim_h + 2 * bleed  # 91 × 61
    margin = 8  # around the artboard for crop marks
    sheet_w, sheet_h = art_w + 2 * margin, art_h + 2 * margin
    ax, ay = margin, margin  # artboard origin (bleed box)
    tx, ty = ax + bleed, ay + bleed  # trim origin

    # FRONT — cream, lockup left-of-centre, URL bottom right in the safe area
    # Safe = 5 mm inside trim
    safe = 5
    sx, sy, sw, sh = tx + safe, ty + safe, trim_w - 2 * safe, trim_h - 2 * safe  # 75 × 45

    g, lw, lh = g_lockup_h(ember, slate, gold, ink, scale=1, x=0, y=0)
    # lockup design units: width ~ 64-ish + word. Scale so lockup optical height is ~14 mm
    target_h = 14
    scale = target_h / 64
    # position: left safe, vertically centred in trim
    lx = sx
    ly = ty + (trim_h - 64 * scale) / 2
    lockup = f'<g transform="translate({lx:.3f} {ly:.3f}) scale({scale:.5f})">\n{g[g.find(">")+1:] if False else "" }</g>'
    # simpler: use the group from g_lockup_h with x,y,scale
    g, lw, lh = g_lockup_h(ember, slate, gold, ink, scale=scale, x=lx, y=ly)

    url_el, url_sh = text_group(PLEX_RG, SITE_HOST, 2.6, muted, 0, 0)
    url_w = url_sh["width"]
    url = f'<g transform="translate({tx + trim_w - safe - url_w:.3f} {ty + trim_h - safe:.3f})">\n{url_el}\n</g>'

    # bleed + trim guides (non-printing, in a separate 'guides' layer, dashed)
    guides = f'''  <g id="guides" fill="none">
    <rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" stroke="#00A3E0" stroke-width="0.2" stroke-dasharray="1 0.7"/>
    <rect x="{tx}" y="{ty}" width="{trim_w}" height="{trim_h}" stroke="#E0008C" stroke-width="0.15" stroke-dasharray="0.8 0.6"/>
    <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" stroke="#00A300" stroke-width="0.12" stroke-dasharray="0.6 0.6"/>
  </g>'''
    caption = f'''  <g font-family="IBM Plex Sans, sans-serif" font-size="2.2" fill="{muted}">
    <text x="{margin}" y="{sheet_h - 1.6}">Daybreak business card front · 85×55 mm trim · 3 mm bleed · cyan=bleed magenta=trim green=safe 5 mm · do not print guides</text>
  </g>'''
    bg = f'<rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" fill="{paper}"/>'
    # trim is 85x55; bleed extends paper
    body = f"  {bg}\n  {g}\n  {url}\n{guides}\n{crop_marks(tx, ty, trim_w, trim_h)}\n{caption}"
    write(TEMPL / "business-card-front.svg", svg_mm(sheet_w, sheet_h, body, vb=f"0 0 {sheet_w} {sheet_h}"))

    # BACK — ember field to bleed, knockout mark on the left, contact column on the right
    mark_h_mm = 22
    mscale = mark_h_mm / MARK_H
    # optical mark centred vertically in the trim, inset from the left safe edge
    mx = sx + 2 - HORIZON_X1 * mscale
    my = ty + (trim_h - MARK_H * mscale) / 2 - MARK_TOP * mscale
    g2 = f'<g transform="translate({mx:.3f} {my:.3f}) scale({mscale:.5f})">{mark_elements(paper, paper, paper)}</g>'
    lines = [
        ("Name", 3.8, SORA_SB, paper),
        ("Role / team", 2.7, PLEX_RG, paper),
        (EMAIL_PLACEHOLDER, 2.5, PLEX_RG, paper),
        (SITE_HOST, 2.5, PLEX_RG, paper),
    ]
    cx = sx + 32
    contact = []
    y = ty + 16
    for text, sz, font, col in lines:
        el, sh = text_group(font, text, sz, col, cx, y)
        contact.append(el)
        y += sz + 2.4
    contact_el = "\n  ".join(contact)
    bg2 = f'<rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" fill="{ember}"/>'
    body2 = f"  {bg2}\n  {g2}\n  {contact_el}\n{guides}\n{crop_marks(tx, ty, trim_w, trim_h, color='#FFFFFF')}\n{caption.replace('front', 'back').replace(muted, paper)}"
    write(TEMPL / "business-card-back.svg", svg_mm(sheet_w, sheet_h, body2, vb=f"0 0 {sheet_w} {sheet_h}"))


def sticker_sheet():
    # A5 landscape 210 × 148 mm, 3 mm bleed, die-cut guides
    bleed = 3
    trim_w, trim_h = 210, 148
    art_w, art_h = trim_w + 2 * bleed, trim_h + 2 * bleed
    margin = 8
    sheet_w, sheet_h = art_w + 2 * margin, art_h + 2 * margin
    ax, ay = margin, margin
    tx, ty = ax + bleed, ay + bleed

    bg = f'<rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" fill="{mist}"/>'

    def circle_sticker(cx, cy, r, field, mark_sun, mark_h, mark_g, simple=False, label=""):
        # mark optical height 44.5 in 64 box; fill ~62% of diameter
        fill = 0.62
        scale = (2 * r * fill) / MARK_H
        # center optical mark in the circle
        ox0, oy0 = HORIZON_X1, MARK_TOP
        ow, oh = HORIZON_X2 - HORIZON_X1, MARK_H
        mx = cx - (ox0 + ow / 2) * scale
        my = cy - (oy0 + oh / 2) * scale
        inner = mark_elements(mark_sun, mark_h, mark_g, simple=simple)
        die = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{field}" stroke="#111" stroke-width="0.15" stroke-dasharray="0.8 0.5"/>'
        return f'{die}\n  <g transform="translate({mx:.3f} {my:.3f}) scale({scale:.5f})">{inner}</g>'

    # Large colour mark, 50 mm die-cut circle
    s1 = circle_sticker(tx + 38, ty + 50, 25, paper, ember, slate, gold)
    # Ember knockout, 40 mm
    s2 = circle_sticker(tx + 100, ty + 42, 20, ember, paper, paper, paper)
    # Slate knockout, 40 mm
    s3 = circle_sticker(tx + 155, ty + 42, 20, slate, paper, paper, paper)
    # Die-cut mark: one connected silhouette (disc + neck covering the horizon + bar)
    mark_h_mm = 42
    scale = mark_h_mm / MARK_H
    mx, my = tx + 22, ty + 88
    die_offset = 2.2
    gx, gy = mx, my - MARK_TOP * scale
    inner = mark_elements(ember, slate, gold)
    disc_cx = gx + CX * scale
    disc_cy = gy + CY * scale
    disc_r = R * scale + die_offset
    neck_x = gx + HORIZON_X1 * scale - die_offset
    neck_w = (HORIZON_X2 - HORIZON_X1) * scale + 2 * die_offset
    neck_y = disc_cy
    neck_h = (gy + (BAR_Y + BAR_H) * scale + die_offset) - neck_y
    bar_x = gx + (CX - BAR_W / 2) * scale - die_offset
    bar_y = gy + BAR_Y * scale - die_offset
    bar_w = BAR_W * scale + 2 * die_offset
    bar_h = BAR_H * scale + 2 * die_offset
    dash = 'stroke="#111" stroke-width="0.15" stroke-dasharray="0.8 0.5"'
    die_mark = (
        f'  <g>\n'
        f'    <circle cx="{disc_cx:.3f}" cy="{disc_cy:.3f}" r="{disc_r:.3f}" fill="{paper}"/>\n'
        f'    <rect x="{neck_x:.3f}" y="{neck_y:.3f}" width="{neck_w:.3f}" height="{neck_h:.3f}" fill="{paper}"/>\n'
        f'    <rect x="{bar_x:.3f}" y="{bar_y:.3f}" width="{bar_w:.3f}" height="{bar_h:.3f}" rx="1.4" fill="{paper}"/>\n'
        f'    <circle cx="{disc_cx:.3f}" cy="{disc_cy:.3f}" r="{disc_r:.3f}" fill="none" {dash}/>\n'
        f'    <rect x="{neck_x:.3f}" y="{neck_y:.3f}" width="{neck_w:.3f}" height="{neck_h:.3f}" fill="none" {dash}/>\n'
        f'    <rect x="{bar_x:.3f}" y="{bar_y:.3f}" width="{bar_w:.3f}" height="{bar_h:.3f}" rx="1.4" fill="none" {dash}/>\n'
        f'    <g transform="translate({gx:.3f} {gy:.3f}) scale({scale:.5f})">{inner}</g>\n'
        f'  </g>'
    )

    # Wordmark pill sticker
    g, lw, lh = g_lockup_h(ember, slate, gold, ink, scale=1)
    pill_h = 22
    scale_p = pill_h / 64
    pill_w = lw * scale_p + 14
    px, py = tx + 85, ty + 100
    pill = f'''  <rect x="{px}" y="{py}" width="{pill_w:.3f}" height="{pill_h + 8}" rx="14" fill="{paper}" stroke="#111" stroke-width="0.15" stroke-dasharray="0.8 0.5"/>
  <g transform="translate({px + 7:.3f} {py + 4:.3f}) scale({scale_p:.5f})">{mark_elements(ember, slate, gold)}
  </g>'''
    # The lockup group already includes the mark — use the full lockup
    pill = f'''  <rect x="{px}" y="{py}" width="{pill_w:.3f}" height="{pill_h + 8}" rx="14" fill="{paper}" stroke="#111" stroke-width="0.15" stroke-dasharray="0.8 0.5"/>
  <g transform="translate({px + 7:.3f} {py + 4:.3f}) scale({scale_p:.5f})">
    {g_lockup_h(ember, slate, gold, ink, scale=1, x=0, y=0)[0].split('>',1)[1].rsplit('</g>',1)[0] if False else ''}
  </g>'''
    # Cleaner: just translate the prebuilt group
    grp, lw, lh = g_lockup_h(ember, slate, gold, ink, scale=scale_p, x=px + 7, y=py + 4)
    pill = (
        f'<rect x="{px}" y="{py}" width="{pill_w:.3f}" height="{pill_h + 8}" rx="14" '
        f'fill="{paper}" stroke="#111" stroke-width="0.15" stroke-dasharray="0.8 0.5"/>\n  {grp}'
    )

    title_el, _ = text_group(SORA_SB, "Daybreak sticker sheet", 4.2, ink, tx + 8, ty + 12)
    note_el, _ = text_group(
        PLEX_RG,
        "Dashed lines = die-cut. Kiss-cut on cream vinyl. 3 mm bleed on the sheet edge.",
        2.2,
        muted,
        tx + 8,
        ty + 17,
    )

    guides = f'''  <g id="guides" fill="none">
    <rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" stroke="#00A3E0" stroke-width="0.2" stroke-dasharray="1 0.7"/>
    <rect x="{tx}" y="{ty}" width="{trim_w}" height="{trim_h}" stroke="#E0008C" stroke-width="0.15" stroke-dasharray="0.8 0.6"/>
  </g>'''
    body = f"  {bg}\n  {title_el}\n  {note_el}\n  {s1}\n  {s2}\n  {s3}\n  {die_mark}\n  {pill}\n{guides}\n{crop_marks(tx, ty, trim_w, trim_h)}"
    write(TEMPL / "sticker-sheet.svg", svg_mm(sheet_w, sheet_h, body, vb=f"0 0 {sheet_w} {sheet_h}"))


def poster_a2():
    bleed = 5
    trim_w, trim_h = 420, 594
    art_w, art_h = trim_w + 2 * bleed, trim_h + 2 * bleed
    margin = 12
    sheet_w, sheet_h = art_w + 2 * margin, art_h + 2 * margin
    ax, ay = margin, margin
    tx, ty = ax + bleed, ay + bleed
    safe = 12
    sx, sy = tx + safe, ty + safe

    bg = f'<rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" fill="{paper}"/>'
    # Large colour mark, upper half
    mark_h_mm = 160
    scale = mark_h_mm / MARK_H
    # center mark horizontally on the trim
    optical_w = (HORIZON_X2 - HORIZON_X1) * scale
    mx = tx + (trim_w - optical_w) / 2 - HORIZON_X1 * scale
    my = ty + 70 - MARK_TOP * scale
    mark = f'<g transform="translate({mx:.3f} {my:.3f}) scale({scale:.5f})">{mark_elements(ember, slate, gold)}</g>'

    # Wordmark
    word = shape_paths(SORA_SB, "Chamuka", 64)
    word_w = word["width"]
    wx = tx + (trim_w - word_w) / 2
    wy = ty + 70 + mark_h_mm + 50 + abs(word["bounds"][1])
    word_el = f'<g transform="translate({wx:.3f} {wy:.3f})">{paths_to_el(word["paths"], ink)}</g>'

    line = shape_paths(PLEX_RG, "Work, come alive.", 16)
    lx = tx + (trim_w - line["width"]) / 2
    ly = wy + 28
    line_el = f'<g transform="translate({lx:.3f} {ly:.3f})">{paths_to_el(line["paths"], slate)}</g>'

    products = shape_paths(PLEX_MD, "DrawIt    FormIt    Play", 10)
    px = tx + (trim_w - products["width"]) / 2
    py = ty + trim_h - safe - 18
    prod_el = f'<g transform="translate({px:.3f} {py:.3f})">{paths_to_el(products["paths"], muted)}</g>'

    url = shape_paths(PLEX_RG, SITE_HOST, 8)
    ux = tx + (trim_w - url["width"]) / 2
    uy = py + 14
    url_el = f'<g transform="translate({ux:.3f} {uy:.3f})">{paths_to_el(url["paths"], ink)}</g>'

    # a thin gold rule under the wordmark, echoing the mark
    rule_w = 48
    rule = f'<rect x="{tx + (trim_w-rule_w)/2:.3f}" y="{wy + 10:.3f}" width="{rule_w}" height="2.4" fill="{gold}"/>'

    guides = f'''  <g id="guides" fill="none">
    <rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" stroke="#00A3E0" stroke-width="0.3" stroke-dasharray="2 1"/>
    <rect x="{tx}" y="{ty}" width="{trim_w}" height="{trim_h}" stroke="#E0008C" stroke-width="0.25" stroke-dasharray="1.5 1"/>
    <rect x="{sx}" y="{sy}" width="{trim_w-2*safe}" height="{trim_h-2*safe}" stroke="#00A300" stroke-width="0.2" stroke-dasharray="1.2 1"/>
  </g>'''
    cap = f'<text x="{margin}" y="{sheet_h - 3}" font-family="sans-serif" font-size="3.2" fill="{muted}">Daybreak A2 poster · 420×594 mm trim · 5 mm bleed · guides are non-printing</text>'
    body = f"  {bg}\n  {mark}\n  {word_el}\n  {rule}\n  {line_el}\n  {prod_el}\n  {url_el}\n{guides}\n{crop_marks(tx, ty, trim_w, trim_h, len_=6, offset=2)}\n  {cap}"
    write(TEMPL / "poster-a2.svg", svg_mm(sheet_w, sheet_h, body, vb=f"0 0 {sheet_w} {sheet_h}"))


def rollup():
    # 850 × 2000 mm. Hardware cassette covers the bottom ~200–250 mm.
    # Add 5 mm bleed on sides/top; extra 5 mm foot for finishing. Guides for stand.
    w, h = 850, 2000
    bleed = 5
    art_w, art_h = w + 2 * bleed, h + bleed  # no extra at the very bottom if it's in the cassette; still add 5
    art_h = h + 2 * bleed
    margin = 20
    sheet_w, sheet_h = art_w + 2 * margin, art_h + 2 * margin
    ax, ay = margin, margin
    tx, ty = ax + bleed, ay + bleed
    stand = 250  # unprintable / visually blocked by cassette
    safe_side = 40
    safe_top = 80

    bg = f'<rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" fill="{slate}"/>'
    # Large stacked knockout lockup in the upper third
    g, lw, lh = g_lockup_s(paper, paper, paper, paper, scale=1)
    # We want the stacked lockup about 420 mm wide
    scale = 420 / lw
    lx = tx + (w - lw * scale) / 2
    ly = ty + safe_top + 40
    lock = f'<g transform="translate({lx:.3f} {ly:.3f}) scale({scale:.5f})">{g.split(">",1)[1] if False else ""}</g>'
    grp, lw, lh = g_lockup_s(paper, paper, paper, paper, scale=scale, x=lx, y=ly)

    line = shape_paths(PLEX_RG, "Work, come alive.", 36)
    lxx = tx + (w - line["width"]) / 2
    lyy = ly + lh * 1  # lh already includes scale? g_lockup_s with scale still returns unscaled w,h
    # Wait: g_lockup_s returns unscaled width/height of the design (pad=0), scale is only in the transform.
    lyy = ly + (lh * scale) + 40
    line_el = f'<g transform="translate({lxx:.3f} {lyy:.3f})">{paths_to_el(line["paths"], gold)}</g>'

    products = shape_paths(PLEX_MD, "DrawIt     ·     FormIt     ·     Play", 22)
    px = tx + (w - products["width"]) / 2
    py = lyy + 70
    prod_el = f'<g transform="translate({px:.3f} {py:.3f})">{paths_to_el(products["paths"], paper)}</g>'

    url = shape_paths(SORA_SB, SITE_HOST, 28)
    ux = tx + (w - url["width"]) / 2
    uy = ty + h - stand - 80
    url_el = f'<g transform="translate({ux:.3f} {uy:.3f})">{paths_to_el(url["paths"], paper)}</g>'

    # gold horizon echo above the stand
    rule = f'<rect x="{tx + 200}" y="{uy - 30}" width="450" height="6" fill="{gold}"/>'

    # cassette zone
    cass = f'''  <g id="cassette-zone" fill="{ink}" fill-opacity="0.28">
    <rect x="{tx}" y="{ty + h - stand}" width="{w}" height="{stand}"/>
  </g>
  <text x="{tx + w/2}" y="{ty + h - stand + 40}" text-anchor="middle" font-family="sans-serif" font-size="16" fill="{paper}">Hardware / cassette zone — keep clear (~250 mm)</text>'''

    guides = f'''  <g id="guides" fill="none">
    <rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" stroke="#00A3E0" stroke-width="0.8" stroke-dasharray="4 2"/>
    <rect x="{tx}" y="{ty}" width="{w}" height="{h}" stroke="#E0008C" stroke-width="0.6" stroke-dasharray="3 2"/>
    <rect x="{tx+safe_side}" y="{ty+safe_top}" width="{w-2*safe_side}" height="{h-stand-safe_top}" stroke="#00A300" stroke-width="0.5" stroke-dasharray="3 2"/>
  </g>'''
    cap = f'<text x="{margin}" y="{sheet_h - 6}" font-family="sans-serif" font-size="8" fill="{mist}">Daybreak roll-up banner · 850×2000 mm · 5 mm bleed · bottom 250 mm reserved for cassette · guides non-printing</text>'
    body = f"  {bg}\n  {grp}\n  {line_el}\n  {prod_el}\n  {rule}\n  {url_el}\n{cass}\n{guides}\n{crop_marks(tx, ty, w, h, len_=10, offset=3, color='#FFFFFF')}\n  {cap}"
    write(TEMPL / "rollup-banner.svg", svg_mm(sheet_w, sheet_h, body, vb=f"0 0 {sheet_w} {sheet_h}"))


def donts_sheet():
    """A compact don'ts board for the brand page / README."""
    W, H = 1200, 780
    bg = f'<rect width="{W}" height="{H}" fill="{paper}"/>'
    title = shape_paths(SORA_SB, "Don't", 36)
    title_el = f'<g transform="translate(48 64)">{paths_to_el(title["paths"], ember)}</g>'

    def cell(x, y, w, h, inner, label):
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{white}" stroke="{mist}" stroke-width="2"/>'
        cap = shape_paths(PLEX_RG, label, 16)
        cap_el = f'<g transform="translate({x + 16} {y + h - 18})">{paths_to_el(cap["paths"], ink)}</g>'
        return f"{box}\n  {inner}\n  {cap_el}"

    cells = []
    # 1 stretch
    g, lw, lh = g_lockup_h(ember, slate, gold, ink, scale=1.1, x=70, y=130)
    stretched = f'<g transform="translate(70 130) scale(2.2, 0.7)">{mark_elements(ember, slate, gold)}</g>'
    cells.append(cell(40, 90, 270, 280, stretched, "Don't stretch or squash"))
    # 2 rotate oddly
    rot = f'<g transform="translate(445 250) rotate(-22) scale(2.2) translate(-32 -32)">{mark_elements(ember, slate, gold)}</g>'
    cells.append(cell(330, 90, 270, 280, rot, "Don't rotate the mark"))
    # 3 recolour
    rec = f'<g transform="translate(655 150) scale(2.2)">{mark_elements(play, gold, slate)}</g>'
    cells.append(cell(620, 90, 270, 280, rec, "Don't recolour the sun"))
    # 4 drop the bar
    drop = f'<g transform="translate(945 140) scale(2.4)"><circle cx="{CX}" cy="{CY}" r="{R}" fill="{ember}"/></g>'
    cells.append(cell(910, 90, 250, 280, drop, "Don't drop the horizon or bar"))
    # 5 outline
    outline = (
        f'<g transform="translate(90 470) scale(2.1)" fill="none" stroke="{ember}" stroke-width="2.5">'
        f'<circle cx="{CX}" cy="{CY}" r="{R}"/>'
        f'<line x1="{HORIZON_X1}" y1="{HORIZON_Y}" x2="{HORIZON_X2}" y2="{HORIZON_Y}" stroke="{slate}" stroke-width="2.5"/>'
        f'<rect x="{CX-BAR_W/2}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" stroke="{gold}" fill="none"/>'
        f"</g>"
    )
    cells.append(cell(40, 400, 270, 280, outline, "Don't outline or add a stroke"))
    # 6 low contrast
    low = (
        f'<rect x="330" y="400" width="270" height="280" rx="10" fill="#E8C9B4"/>'
        + f'<g transform="translate(385 455) scale(2.1)">{mark_elements("#E89A7A", "#C4A090", "#E8C98A")}</g>'
        + f'<g transform="translate(346 652)">{paths_to_el(shape_paths(PLEX_RG, "Don\'t use low contrast", 16)["paths"], ink)}</g>'
    )
    cells.append(low)
    # 7 drop shadow
    shadow = (
        f'<g transform="translate(690 460) scale(2.1)" opacity="0.25">{mark_elements("#000","#000","#000")}</g>'
        f'<g transform="translate(680 450) scale(2.1)">{mark_elements(ember, slate, gold)}</g>'
    )
    cells.append(cell(620, 400, 270, 280, shadow, "Don't add drop shadows"))
    # 8 busy photo without plate — simulated with a patterned rect
    busy = (
        f'<defs><pattern id="busy" width="18" height="18" patternUnits="userSpaceOnUse">'
        f'<rect width="18" height="18" fill="#8A6A4A"/>'
        f'<circle cx="5" cy="6" r="4" fill="#C48A4A"/>'
        f'<circle cx="14" cy="13" r="5" fill="#5A3A28"/>'
        f"</pattern></defs>"
        f'<rect x="910" y="400" width="250" height="280" rx="10" fill="url(#busy)"/>'
        f'<g transform="translate(965 455) scale(1.8)">{mark_elements(ember, slate, gold)}</g>'
        f'<g transform="translate(926 652)">{paths_to_el(shape_paths(PLEX_RG, "Don\'t sit on a busy photo", 15)["paths"], paper)}</g>'
    )
    cells.append(busy)

    body = bg + "\n  " + title_el + "\n  " + "\n  ".join(cells)
    write(SVG / "donts.svg", svg_doc(W, H, body, vb=f"0 0 {W} {H}"))


def min_size_sheet():
    W, H = 1100, 420
    bg = f'<rect width="{W}" height="{H}" fill="{paper}"/>'
    title = f'<g transform="translate(40 48)">{paths_to_el(shape_paths(SORA_SB, "Minimum sizes", 28)["paths"], ink)}</g>'
    # digital px and print mm shown as two rows of marks at scale, with labels
    body_bits = [bg, title]
    # We'll just produce a typographic spec card; actual numbers live in the README.
    lines = [
        (PLEX_MD, "Digital", 18, slate, 40, 100),
        (PLEX_RG, "Full mark  24 px tall   ·   Simple mark / favicon  16 px   ·   Horizontal lockup  120 px wide", 15, ink, 40, 128),
        (PLEX_MD, "Print", 18, slate, 40, 180),
        (PLEX_RG, "Full mark  10 mm tall   ·   Simple mark  8 mm   ·   Horizontal lockup  32 mm wide   ·   Stacked lockup  18 mm wide", 15, ink, 40, 208),
        (PLEX_RG, "Horizon rule must print at least 0.3 mm. Below 12 mm mark height, or for screen print and embroidery, use the simple (no-horizon) mark.", 15, ink, 40, 236),
        (PLEX_RG, "Clear space  =  1 sun radius  (0.36 × the optical mark height)  on every side, in px or mm.", 15, ink, 40, 264),
        (PLEX_RG, "Bleed  3 mm (cards, stickers)   ·   5 mm (posters, banners)   ·   Roll-up: keep the bottom 250 mm clear of type for the cassette.", 15, ink, 40, 292),
    ]
    for font, text, sz, col, x, y in lines:
        body_bits.append(f'<g transform="translate({x} {y})">{paths_to_el(shape_paths(font, text, sz)["paths"], col)}</g>')
    write(SVG / "min-sizes.svg", svg_doc(W, H, "\n  ".join(body_bits), vb=f"0 0 {W} {H}"))


def tokens_and_readme():
    colors = json.loads((ROOT / "colors.json").read_text())
    core = colors["core"]

    def cmyk_str(name):
        c = core[name]["cmyk_swop_relative"]
        return f"{c['c']} {c['m']} {c['y']} {c['k']}"

    def pms_c(name):
        hits = core[name]["pantone_coated_nearest"]
        top = hits[0]
        alts = ", ".join(f"{h['name']} (ΔE {h['delta_e00']})" for h in hits[1:3])
        return top, alts

    # tokens.css
    css = f"""/* Chamuka Daybreak — design tokens
   Screen values are authored in sRGB. Print equivalents: see print/README.md
   and colors.json (CMYK method and Pantone nearest-match notes).
*/

:root {{
  /* Core */
  --ember: #E24E1B;
  --gold: #E6B422;
  --slate: #2B4C7E;
  --paper: #FFF8F1;
  --mist: #F3EBE0;
  --ink: #17141C;
  --muted: #6B645C;

  /* Semantic */
  --success: #1F8A5B;
  --warning: #E0A100;
  --danger: #C5362B;
  --info: #2B4C7E;
  --play: #D9487A; /* Coral — playful-but-adult products (Play is an example) */
  --forest: #2F6B4F; /* Forest — calm green products (Waypoint is an example) */
  --mineral: #1F7A6B; /* Mineral — infra / platform tools (Vmette is an example) */

  /* Neutral ramp */
  --neutral-50: #FBF7F2;
  --neutral-100: #F3EBE0;
  --neutral-200: #E6D9C8;
  --neutral-300: #D0C0AA;
  --neutral-400: #B3A28A;
  --neutral-500: #8F8170;
  --neutral-600: #6B645C;
  --neutral-700: #524C46;
  --neutral-800: #3A3531;
  --neutral-900: #241F1C;
  --neutral-950: #17141C;

  /* Light theme (default) — shadcn-style */
  --background: var(--paper);
  --foreground: var(--ink);
  --card: var(--paper);
  --card-foreground: var(--ink);
  --popover: #FFFFFF;
  --popover-foreground: var(--ink);
  --primary: var(--ember);
  --primary-foreground: #FFFFFF; /* large UI only; ember fails WCAG AA for small text on paper (3.74:1) */
  --secondary: var(--mist);
  --secondary-foreground: var(--ink);
  --muted-bg: var(--mist);
  --muted-foreground: var(--muted);
  --accent: var(--slate);
  --accent-foreground: var(--paper);
  --destructive: var(--danger);
  --destructive-foreground: #FFFFFF;
  --border: #E6D9C8;
  --input: #E6D9C8;
  --ring: var(--ember);
  --radius: 0.5rem;

  /* Product accents */
  --accent-drawit: var(--ember);
  --accent-formit: var(--slate);
  --accent-play: var(--play);
  --accent-forest: var(--forest);
  --accent-mineral: var(--mineral);
}}

.dark {{
  --background: #17141C;
  --foreground: #FFF8F1;
  --card: #241F1C;
  --card-foreground: #FFF8F1;
  --popover: #241F1C;
  --popover-foreground: #FFF8F1;
  --primary: #F06A3A; /* slightly lifted ember so filled buttons hold contrast on ink */
  --primary-foreground: #17141C;
  --secondary: #3A3531;
  --secondary-foreground: #FFF8F1;
  --muted-bg: #241F1C;
  --muted-foreground: #A39484;
  --accent: #7FA0D4; /* lifted slate for text/links on ink; fills may still use #2B4C7E */
  --accent-foreground: #17141C;
  --destructive: #E0564A;
  --destructive-foreground: #17141C;
  --border: #3A3531;
  --input: #3A3531;
  --ring: #F06A3A;
}}

/* Tailwind CSS v4 */
@theme {{
  --color-ember: #E24E1B;
  --color-gold: #E6B422;
  --color-slate: #2B4C7E;
  --color-paper: #FFF8F1;
  --color-mist: #F3EBE0;
  --color-ink: #17141C;
  --color-muted: #6B645C;
  --color-success: #1F8A5B;
  --color-warning: #E0A100;
  --color-danger: #C5362B;
  --color-info: #2B4C7E;
  --color-play: #D9487A;
  --color-forest: #2F6B4F;
  --color-mineral: #1F7A6B;
  --color-neutral-50: #FBF7F2;
  --color-neutral-100: #F3EBE0;
  --color-neutral-200: #E6D9C8;
  --color-neutral-300: #D0C0AA;
  --color-neutral-400: #B3A28A;
  --color-neutral-500: #8F8170;
  --color-neutral-600: #6B645C;
  --color-neutral-700: #524C46;
  --color-neutral-800: #3A3531;
  --color-neutral-900: #241F1C;
  --color-neutral-950: #17141C;
  --font-display: "Sora", ui-sans-serif, system-ui, sans-serif;
  --font-sans: "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, monospace;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 20px;
  --shadow-sm: 0 1px 2px rgb(23 20 28 / 0.06);
  --shadow-md: 0 8px 20px rgb(23 20 28 / 0.08);
  --shadow-lg: 0 18px 40px rgb(23 20 28 / 0.12);
}}
"""
    write(ROOT / "tokens.css", css)

    readme = """# Chamuka Daybreak — brand masters

Hand-built SVG masters, PNG previews, screen tokens, and print/merch files for the Daybreak system. Nothing in this folder has been published or pushed to GitHub.

## Colour (screen)

| Name | Hex | RGB | HSL | Role |
|---|---|---|---|---|
| Ember | `#E24E1B` | 226, 78, 27 | 15, 79%, 50% | Primary, DrawIt accent, buttons (large UI) |
| Gold | `#E6B422` | 230, 180, 34 | 45, 80%, 52% | Horizon bar, highlights — not body text on paper |
| Slate | `#2B4C7E` | 43, 76, 126 | 216, 49%, 33% | Horizon rule, FormIt accent, headings support |
| Morning paper | `#FFF8F1` | 255, 248, 241 | 30, 100%, 97% | Default light background |
| Mist | `#F3EBE0` | 243, 235, 224 | 35, 44%, 92% | Subtle surfaces, chips |
| Ink | `#17141C` | 23, 20, 28 | 262, 17%, 9% | Text and mono lockups |
| Muted | `#6B645C` | 107, 100, 92 | 32, 8%, 39% | Secondary text (AA on paper: 5.54:1) |
| Success | `#1F8A5B` | 31, 138, 91 | 154, 63%, 33% | Large text / icons on paper (4.12:1, AA large only) |
| Warning | `#E0A100` | 224, 161, 0 | 43, 100%, 44% | On ink only (fails on paper) |
| Danger | `#C5362B` | 197, 54, 43 | 4, 64%, 47% | AA on paper (5.07:1) |
| Play | `#D9487A` | 217, 72, 122 | 339, 66%, 57% | Play product accent only; AA large on paper (3.87:1) |

Key contrast (WCAG 2.x, computed):

- Ink on paper 17.30 AAA; slate on paper 8.18 AAA; muted on paper 5.54 AA.
- Ember on paper **3.74, fails AA for small text**, passes AA large. Use ember for buttons, marks and display, not body copy. White/paper type on ember is the same ratio — large UI only (button labels 16px+ / 14px bold).
- Gold on paper fails; gold on ink 9.47 AAA.
- Success on paper 4.12 — large text / icons only, or darken for small text.
- Full table: `colors.json`.

Print (CMYK + Pantone) is documented in `print/README.md`. Never treat Pantone nearest matches as official.

## Type

- **Sora** (500/600/700) — display, headings, wordmark (outlines in the SVGs).
- **IBM Plex Sans** (400/500/600) — UI and body.
- **IBM Plex Mono** — code and tabular data.

Scale: display 56/64 600; h1 40/48 600; h2 32/40 600; h3 24/32 600; h4 20/28 500; body 16/24 400; small 14/20; caption 12/16; code 14/22 Mono.

## Logo files (`svg/`, `png/`)

Primary lockup: `lockup-horizontal.svg`. Stacked: `lockup-stacked.svg`. Mark: `mark.svg`. Small-size / embroidery: `mark-simple.svg` (horizon removed, bar thickened).

Mono dark / light, plates on cream, ember and slate, product lockups (DrawIt ember, FormIt slate, Play coral), app icons 512 and favicons 16/32 are in the same folders. Wordmark outlines are Sora SemiBold.

Clear space = one sun radius on every side (half the disc diameter), equal to 0.36 × the optical mark height (disc top to gold-bar bottom).

Minimum digital sizes: full mark 24 px tall; simple mark 16 px; horizontal lockup 120 px wide.

Don’ts: see `svg/donts.svg` — don’t stretch, rotate, recolour, drop the bar or horizon, outline, add a drop shadow, or place the mark on a busy photograph without a solid plate.

## Product architecture

Shared Daybreak core (ember / gold / slate / paper / ink, Sora + Plex). One accent each:

- **DrawIt** — ember `#E24E1B`
- **FormIt** — slate `#2B4C7E`
- **Play** — coral `#D9487A` (product layer only; chrome and wordmark stay Daybreak)

Waypoint and Vmette, if they rejoin the suite, can pick a remaining in-family accent (gold or a deeper ink) without inventing a fourth typeface or a new primary.

### Code-change recommendations (from the audit; not applied)

These are suggested follow-ups for the product repos — this pack does not change any repository.

- **DrawIt**: favicon / manifest theme is still `#2563EB`. Move to ember `#E24E1B` (and the cream / ink surfaces).
- **FormIt**: primary `#2463EB` and Geist should move to Daybreak slate + Sora / IBM Plex Sans.
- **Platform / marketing**: daisyUI teal should give way to Daybreak tokens (`tokens.css`).
- **Play**: grape `#7A3CF0` can remain a product-layer accent if needed, but shell, wordmark and marketing chrome should use Daybreak; the in-system Play accent is coral `#D9487A`.

## Tokens

`tokens.css` — light and `.dark` shadcn-style variables, plus a Tailwind v4 `@theme` block.

## Print and merchandise

See `print/` — one-ink and knockout SVGs, business card, sticker sheet, A2 poster, roll-up banner, apparel / mug / tote placement, CMYK and Pantone notes.
"""
    # Repo README.md is hand-maintained (overview, folder map, usage, licence).
    # Do not overwrite it on regenerate. Colour/print detail lives in print/README.md.

    # print README
    ember_p, ember_alts = pms_c("ember")
    gold_p, gold_alts = pms_c("gold")
    slate_p, slate_alts = pms_c("slate")
    ink_p, ink_alts = pms_c("ink")
    muted_p, muted_alts = pms_c("muted")
    success_p, success_alts = pms_c("success")
    warning_p, warning_alts = pms_c("warning")
    danger_p, danger_alts = pms_c("danger")
    play_p, play_alts = pms_c("play")
    paper_p, paper_alts = pms_c("paper")
    mist_p, mist_alts = pms_c("mist")

    print_readme = f"""# Daybreak print and merchandise

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
| Ember | `#E24E1B` | C{cmyk_str('ember').replace(' ','  ')} | {ember_p['name']} (ΔE {ember_p['delta_e00']}, screen approx {ember_p['hex_approx']}) | {ember_alts} | Pantone 1665 U |
| Gold | `#E6B422` | C{cmyk_str('gold')} | {gold_p['name']} (ΔE {gold_p['delta_e00']}, {gold_p['hex_approx']}) | {gold_alts} | Pantone 7409 U |
| Slate | `#2B4C7E` | C{cmyk_str('slate')} | {slate_p['name']} (ΔE {slate_p['delta_e00']}, {slate_p['hex_approx']}) | {slate_alts} | Pantone 7686 U |
| Morning paper | `#FFF8F1` | C{cmyk_str('paper')} | Do not print a fill if a cream stock can be specified. Distant nearest {paper_p['name']} (ΔE {paper_p['delta_e00']}) is not a visual match. | {paper_alts} | Specify uncoated cream / off-white stock |
| Mist | `#F3EBE0` | C{cmyk_str('mist')} | Prefer a tint of stock or a 5–10% warm-grey wash. Distant nearest {mist_p['name']} (ΔE {mist_p['delta_e00']}). | {mist_alts} | Specify stock or a light warm-grey U |
| Ink | `#17141C` | C{cmyk_str('ink')} (too heavy for type — see note above) | {ink_p['name']} (ΔE {ink_p['delta_e00']}, {ink_p['hex_approx']}) | {ink_alts} | Pantone Black 6 U |
| Muted | `#6B645C` | C{cmyk_str('muted')} | {muted_p['name']} (ΔE {muted_p['delta_e00']}, {muted_p['hex_approx']}) | {muted_alts} | Pantone Warm Gray 11 U |
| Success | `#1F8A5B` | C{cmyk_str('success')} | {success_p['name']} (ΔE {success_p['delta_e00']}, {success_p['hex_approx']}) | {success_alts} | Pantone 7725 U |
| Warning | `#E0A100` | C{cmyk_str('warning')} | {warning_p['name']} (ΔE {warning_p['delta_e00']}, {warning_p['hex_approx']}) | {warning_alts} | Pantone 143 U |
| Danger | `#C5362B` | C{cmyk_str('danger')} | {danger_p['name']} (ΔE {danger_p['delta_e00']}, {danger_p['hex_approx']}) | {danger_alts} | Pantone 180 U |
| Play accent | `#D9487A` | C{cmyk_str('play')} | {play_p['name']} (ΔE {play_p['delta_e00']}, {play_p['hex_approx']}) | {play_alts} | Pantone 205 U |

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
"""
    # Fix the ember CMYK formatting I botched with replace
    print_readme = print_readme.replace(
        f"C{cmyk_str('ember').replace(' ','  ')}",
        f"C{cmyk_str('ember')}",
    )
    write(PRINT / "README.md", print_readme)


def main():
    business_cards()
    sticker_sheet()
    poster_a2()
    rollup()
    donts_sheet()
    min_size_sheet()
    tokens_and_readme()

    # previews — modest pixel sizes
    raster(TEMPL / "business-card-front.svg", PRINT_PNG / "business-card-front.png", output_width=1200)
    raster(TEMPL / "business-card-back.svg", PRINT_PNG / "business-card-back.png", output_width=1200)
    raster(TEMPL / "sticker-sheet.svg", PRINT_PNG / "sticker-sheet.png", output_width=1600)
    raster(TEMPL / "poster-a2.svg", PRINT_PNG / "poster-a2.png", output_width=1200)
    raster(TEMPL / "rollup-banner.svg", PRINT_PNG / "rollup-banner.png", output_width=900)
    raster(SVG / "donts.svg", PNG / "donts.png", output_width=1400)
    raster(SVG / "min-sizes.svg", PNG / "min-sizes.png", output_width=1400)
    print("TEMPLATES OK")


if __name__ == "__main__":
    main()

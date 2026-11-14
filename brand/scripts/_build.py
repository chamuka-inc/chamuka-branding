#!/usr/bin/env python3
"""Build Daybreak logo masters, colour math, print templates, tokens, and README."""
from __future__ import annotations

import json
import math
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageCms
import cairosvg

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent

# Confirmed web presence. Email is a placeholder — replace name@ with the person.
SITE_HOST = "chamuka.ai"
SITE_URL = "https://chamuka.ai"
EMAIL_PLACEHOLDER = "name@chamuka.ai"
# Product URL examples (same pattern): drawit.chamuka.ai, formit.chamuka.ai
SVG = ROOT / "svg"
PNG = ROOT / "png"
PRINT = ROOT / "print"
PRINT_SVG = PRINT / "svg"
PRINT_PNG = PRINT / "png"
TEMPL = PRINT / "templates"
for d in (SVG, PNG, PRINT_SVG, PRINT_PNG, TEMPL, PRINT / "mockups"):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Palette (screen / sRGB)
# ---------------------------------------------------------------------------
PALETTE = {
    "ember": "#E24E1B",
    "gold": "#E6B422",
    "slate": "#2B4C7E",
    "paper": "#FFF8F1",
    "mist": "#F3EBE0",
    "ink": "#17141C",
    "muted": "#6B645C",
    "success": "#1F8A5B",
    "warning": "#E0A100",
    "danger": "#C5362B",
    "info": "#2B4C7E",
    "play": "#D9487A",
    "forest": "#2F6B4F",
    "mineral": "#1F7A6B",
    "white": "#FFFFFF",
    "transparent": "none",
}

NEUTRALS = {
    "50": "#FBF7F2",
    "100": "#F3EBE0",  # mist
    "200": "#E6D9C8",
    "300": "#D0C0AA",
    "400": "#B3A28A",
    "500": "#8F8170",
    "600": "#6B645C",  # muted
    "700": "#524C46",
    "800": "#3A3531",
    "900": "#241F1C",
    "950": "#17141C",  # ink
}

# Mark geometry in a 64×64 unit square (optical padding included)
# Matches the Daybreak concept: ember disc, thin slate horizon, narrower gold bar.
R = 16.0
CX, CY = 32.0, 21.5  # disc top ~5.5, bottom ~37.5
HORIZON_Y = 41.4
HORIZON_X1, HORIZON_X2 = 16.0, 48.0  # slightly narrower than diameter, wider than bar
HORIZON_W = 1.25
BAR_W, BAR_H = 22.0, 5.2
BAR_X, BAR_Y = CX - BAR_W / 2, 44.8  # bar bottom 50.0

# Simplified mark (screen print / embroidery / 16px): drop hairline, thicken bar
SIMPLE_R = 16.5
SIMPLE_CX, SIMPLE_CY = 32.0, 21.0
SIMPLE_BAR_W, SIMPLE_BAR_H = 24.0, 7.0
SIMPLE_BAR_X, SIMPLE_BAR_Y = 32.0 - 12.0, 43.5


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb) -> str:
    return "#{:02X}{:02X}{:02X}".format(*[int(round(c)) for c in rgb])


def rgb_to_hsl(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(l * 100)


# WCAG relative luminance / contrast
def rel_lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = [f(x) for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    l1, l2 = rel_lum(hex_to_rgb(a)), rel_lum(hex_to_rgb(b))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_level(ratio, large=False):
    if large:
        if ratio >= 4.5:
            return "AAA"
        if ratio >= 3:
            return "AA"
        return "fail"
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    return "fail"


# CIE Lab / CIEDE2000 for Pantone nearest-match (D65, 2°)
def srgb_to_lab(rgb):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = [lin(x) for x in rgb]
    # sRGB D65
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    xr, yr, zr = x / 0.95047, y / 1.00000, z / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)

    fx, fy, fz = f(xr), f(yr), f(zr)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return L, a, b


def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    kL = kC = kH = 1.0
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cab = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cab ** 7 / (Cab ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = 0 if C1p == 0 else math.degrees(math.atan2(b1, a1p)) % 360
    h2p = 0 if C2p == 0 else math.degrees(math.atan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = 0
    if C1p * C2p != 0:
        dh = h2p - h1p
        if dh > 180:
            dh -= 360
        elif dh < -180:
            dh += 360
        dhp = dh
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lp = (L1 + L2) / 2
    Cp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hp = h1p + h2p
    else:
        if abs(h1p - h2p) <= 180:
            hp = (h1p + h2p) / 2
        elif h1p + h2p < 360:
            hp = (h1p + h2p + 360) / 2
        else:
            hp = (h1p + h2p - 360) / 2
    T = (
        1
        - 0.17 * math.cos(math.radians(hp - 30))
        + 0.24 * math.cos(math.radians(2 * hp))
        + 0.32 * math.cos(math.radians(3 * hp + 6))
        - 0.20 * math.cos(math.radians(4 * hp - 63))
    )
    dRo = 30 * math.exp(-(((hp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cp ** 7 / (Cp ** 7 + 25 ** 7))
    Sl = 1 + (0.015 * (Lp - 50) ** 2) / math.sqrt(20 + (Lp - 50) ** 2)
    Sc = 1 + 0.045 * Cp
    Sh = 1 + 0.015 * Cp * T
    Rt = -math.sin(math.radians(2 * dRo)) * Rc
    return math.sqrt(
        (dLp / (kL * Sl)) ** 2
        + (dCp / (kC * Sc)) ** 2
        + (dHp / (kH * Sh)) ** 2
        + Rt * (dCp / (kC * Sc)) * (dHp / (kH * Sh))
    )


# Published *screen* approximations of PMS colours, compiled from commonly
# circulated Color Bridge / converter datasets (not official Pantone measurements).
# Used only to rank a nearest match; always verify against a physical guide.
PANTONE_C = {
    # oranges / reds
    "Pantone 021 C": "#FE5000",
    "Pantone 1585 C": "#FF6A13",
    "Pantone 1595 C": "#D86018",
    "Pantone 1605 C": "#A65523",
    "Pantone 164 C": "#FF7F41",
    "Pantone 1645 C": "#FF6A39",
    "Pantone 165 C": "#FF671F",
    "Pantone 1655 C": "#FC4C02",
    "Pantone 166 C": "#E35205",
    "Pantone 1665 C": "#DC4405",
    "Pantone 167 C": "#BE4A0F",
    "Pantone 1675 C": "#A9431E",
    "Pantone 171 C": "#FF5C39",
    "Pantone 172 C": "#FA4616",
    "Pantone 173 C": "#CF4520",
    "Pantone 174 C": "#9A3324",
    "Pantone 179 C": "#E03C31",
    "Pantone 1795 C": "#D22630",
    "Pantone 180 C": "#C52928",
    "Pantone 202 C": "#862633",
    "Pantone 186 C": "#C8102E",
    "Pantone 485 C": "#DA291C",
    "Pantone Bright Red C": "#F93822",
    "Pantone 7580 C": "#BE4D25",
    "Pantone 7583 C": "#C4622D",
    "Pantone 7584 C": "#BA5826",
    "Pantone 7597 C": "#D14124",
    "Pantone 7625 C": "#E35205",
    "Pantone 7626 C": "#C5291C",
    "Pantone 7416 C": "#E3524F",
    "Pantone 7417 C": "#E1473D",
    # golds / yellows
    "Pantone 109 C": "#F1C400",
    "Pantone 110 C": "#D7A900",
    "Pantone 115 C": "#FDDA24",
    "Pantone 116 C": "#FFCD00",
    "Pantone 123 C": "#FFC72C",
    "Pantone 1235 C": "#FFB81C",
    "Pantone 124 C": "#EAAA00",
    "Pantone 125 C": "#B98900",
    "Pantone 129 C": "#F3D03E",
    "Pantone 130 C": "#F2A900",
    "Pantone 131 C": "#CC8A00",
    "Pantone 134 C": "#FFD166",
    "Pantone 137 C": "#FFA300",
    "Pantone 138 C": "#DE7C00",
    "Pantone 141 C": "#F2C75C",
    "Pantone 142 C": "#F1BE48",
    "Pantone 143 C": "#E5A823",
    "Pantone 144 C": "#ED8B00",
    "Pantone 1105 C": "#C4A11A",
    "Pantone 7406 C": "#F1C400",
    "Pantone 7408 C": "#F6BE00",
    "Pantone 7409 C": "#F0B323",
    "Pantone 7411 C": "#E6A65D",
    "Pantone 7502 C": "#CEB888",
    "Pantone 7503 C": "#A89968",
    "Pantone 7508 C": "#E1B87F",
    "Pantone 7509 C": "#D6A461",
    "Pantone 7550 C": "#D89F27",
    "Pantone 7555 C": "#D19000",
    "Pantone 7556 C": "#B47E00",
    "Pantone 1245 C": "#C69214",
    "Pantone 1255 C": "#AD841F",
    "Pantone 7753 C": "#C4A11A",
    "Pantone 7752 C": "#CFB023",
    "Pantone 612 C": "#C4B000",
    "Pantone 113 C": "#F3DD4E",
    "Pantone 114 C": "#F8D24B",
    "Pantone 122 C": "#FED141",
    "Pantone 1225 C": "#FFC845",
    "Pantone 106 C": "#F5E100",
    "Pantone 107 C": "#F9D616",
    "Pantone 108 C": "#F7D116",
    "Pantone Yellow 012 C": "#FFD100",
    "Pantone 7751 C": "#CABA3F",
    "Pantone 7758 C": "#D4C304",
    # blues / slates
    "Pantone 285 C": "#0072CE",
    "Pantone 286 C": "#0033A0",
    "Pantone 287 C": "#003087",
    "Pantone 288 C": "#002D72",
    "Pantone 293 C": "#003DA5",
    "Pantone 294 C": "#002F6C",
    "Pantone 2945 C": "#004C97",
    "Pantone 295 C": "#002855",
    "Pantone 301 C": "#005587",
    "Pantone 3015 C": "#007096",
    "Pantone 302 C": "#004F71",
    "Pantone 534 C": "#1B365D",
    "Pantone 533 C": "#1E1A34",
    "Pantone 540 C": "#003C71",
  # ... continued in file
    "Pantone 541 C": "#003C71",
    "Pantone 542 C": "#7BAFD4",
    "Pantone 5415 C": "#5B7F95",
    "Pantone 647 C": "#236192",
    "Pantone 648 C": "#002E5D",
    "Pantone 653 C": "#326295",
    "Pantone 654 C": "#003A70",
    "Pantone 655 C": "#002554",
    "Pantone 7462 C": "#00558C",
    "Pantone 7463 C": "#002B49",
    "Pantone 7682 C": "#6187B0",
    "Pantone 7683 C": "#426DA9",
    "Pantone 7684 C": "#385E9D",
    "Pantone 7685 C": "#2C5697",
    "Pantone 7686 C": "#1D4F91",
    "Pantone 7687 C": "#1D4F91",
    "Pantone 7692 C": "#006BA6",
    "Pantone 7693 C": "#1D4F91",
    "Pantone 7694 C": "#01426A",
    "Pantone 641 C": "#0095C8",
    "Pantone 7469 C": "#005F83",
    "Pantone 7477 C": "#244C5A",
    "Pantone 3025 C": "#005F86",
    "Pantone 3035 C": "#004C6E",
    "Pantone 7546 C": "#253746",
    "Pantone 7545 C": "#425563",
    "Pantone 5335 C": "#3C4A56",
    "Pantone 5405 C": "#4F758B",
    "Pantone 5435 C": "#A6B8C5",
    "Pantone 7459 C": "#4298B5",
    "Pantone 646 C": "#5E8AB4",
    "Pantone 645 C": "#8BA6C1",
    "Pantone 644 C": "#9BB8D3",
    "Pantone 2727 C": "#307FE2",
    "Pantone 2728 C": "#0047BB",
    "Pantone 280 C": "#012169",
    "Pantone 281 C": "#00205B",
    "Pantone 282 C": "#041E42",
    "Pantone 2766 C": "#141C35",
    "Pantone 2767 C": "#13294B",
    "Pantone 533 C": "#1E1A34",
    "Pantone 7547 C": "#131E29",
    "Pantone 432 C": "#333F48",
    "Pantone 433 C": "#1D252D",
    "Pantone 546 C": "#072B31",
    "Pantone 539 C": "#00263A",
    "Pantone 5395 C": "#081F2C",
    # blacks / neutrals / creams
    "Pantone Black C": "#2D2926",
    "Pantone Black 2 C": "#332F21",
    "Pantone Black 3 C": "#212721",
    "Pantone Black 4 C": "#31261D",
    "Pantone Black 5 C": "#3E2B2E",
    "Pantone Black 6 C": "#101820",
    "Pantone Black 7 C": "#3D3935",
    "Pantone Neutral Black C": "#222223",
    "Pantone 419 C": "#212322",
    "Pantone 426 C": "#25282A",
    "Pantone 433 C": "#1D252D",
    "Pantone 440 C": "#382F2D",
    "Pantone 447 C": "#373A36",
    "Pantone 448 C": "#4A412A",
    "Pantone 412 C": "#382F2D",
    "Pantone 419 C": "#212322",
    "Pantone 476 C": "#4E3629",
    "Pantone 4625 C": "#4F2C1D",
    "Pantone 7533 C": "#473729",
    "Pantone Cool Gray 1 C": "#D9D9D6",
    "Pantone Cool Gray 11 C": "#53565A",
    "Pantone Warm Gray 1 C": "#D7D2CB",
    "Pantone Warm Gray 2 C": "#CBC4BC",
    "Pantone Warm Gray 3 C": "#BFB8AF",
    "Pantone Warm Gray 11 C": "#6E6259",
    "Pantone 7527 C": "#D6D2C4",
    "Pantone 7528 C": "#C5B9AC",
    "Pantone 468 C": "#DDCBA4",
    "Pantone 4685 C": "#E0C6AD",
    "Pantone 7500 C": "#DFD1BE",
    "Pantone 7501 C": "#D9C7B0",
    "Pantone 7506 C": "#EFDBB2",
    "Pantone 726 C": "#EDD3B3",
    "Pantone 719 C": "#EDC8A3",
    "Pantone 475 C": "#F3CFB3",
    "Pantone 474 C": "#F7D3B5",
    "Pantone 4755 C": "#E1C6B5",
    "Pantone 4685 C": "#E0C6AD",
    "Pantone 4545 C": "#D5CB9F",
    "Pantone 4535 C": "#CFC493",
    "Pantone 9184 C": "#F4E8D4",
    "Pantone 705 C": "#F5DADF",
    "Pantone 663 C": "#E5E1E6",
    "Pantone 656 C": "#DDE5ED",
    "Pantone 9040 C": "#F1E6D0",
    "Pantone 9161 C": "#F3E5C8",
    "Pantone 9162 C": "#EFE3C8",
    "Pantone 7401 C": "#F5E1A4",
    "Pantone 7402 C": "#ECD898",
    "Pantone 7499 C": "#F1E6B2",
    "Pantone 9083 C": "#F6EBD8",
    # greens / warning / danger already partly covered
    "Pantone 348 C": "#00843D",
    "Pantone 349 C": "#046A38",
    "Pantone 355 C": "#009639",
    "Pantone 356 C": "#007A33",
    "Pantone 347 C": "#009A44",
    "Pantone 7731 C": "#227447",
    "Pantone 7732 C": "#147149",
    "Pantone 7733 C": "#0D5E3C",
    "Pantone 7734 C": "#205C40",
    "Pantone 349 C": "#046A38",
    "Pantone 364 C": "#4A7729",
    "Pantone 3435 C": "#154734",
    "Pantone 3425 C": "#006341",
    "Pantone 335 C": "#007A53",
    "Pantone 334 C": "#009775",
    "Pantone 7724 C": "#00966C",
    "Pantone 7725 C": "#06815B",
    "Pantone 7726 C": "#00754A",
    "Pantone 7727 C": "#006341",
    "Pantone 2256 C": "#1B7A4E",
    "Pantone 2260 C": "#006F44",
    "Pantone 7482 C": "#009F4D",
    "Pantone 7483 C": "#275D38",
    "Pantone 7484 C": "#00573F",
    "Pantone 370 C": "#658D1B",
    "Pantone 376 C": "#84BD00",
    # warning golds already; amber
    "Pantone 130 C": "#F2A900",
    "Pantone 131 C": "#CC8A00",
    "Pantone 125 C": "#B98900",
    "Pantone 7550 C": "#D89F27",
    "Pantone 7555 C": "#D19000",
    "Pantone 124 C": "#EAAA00",
    "Pantone 7408 C": "#F6BE00",
    "Pantone 7409 C": "#F0B323",
    "Pantone 137 C": "#FFA300",
    "Pantone 1375 C": "#FF9E1B",
    "Pantone 138 C": "#DE7C00",
    "Pantone 7549 C": "#FFB81C",
    "Pantone 7551 C": "#B78B20",
    "Pantone 7753 C": "#C4A11A",
    # roses / play
    "Pantone 204 C": "#F8A3BC",
    "Pantone 205 C": "#E0457B",
    "Pantone 206 C": "#CE0037",
    "Pantone 213 C": "#E31C79",
    "Pantone 214 C": "#CE0F69",
    "Pantone 215 C": "#AC145A",
    "Pantone 191 C": "#EF426F",
    "Pantone 1915 C": "#EF426F",
    "Pantone 192 C": "#E40046",
    "Pantone 1925 C": "#E0004D",
    "Pantone 198 C": "#E4002B",
    "Pantone 203 C": "#EC86A8",
    "Pantone 218 C": "#E56591",
    "Pantone 219 C": "#DA1884",
    "Pantone 675 C": "#AE2573",
    "Pantone 676 C": "#96305A",
    "Pantone 7424 C": "#E24585",
    "Pantone 7425 C": "#B52555",
    "Pantone 7433 C": "#E0719F",
    "Pantone 7434 C": "#C45784",
    "Pantone 7435 C": "#B3486D",
    "Pantone 17-2031": "#D23A6D",
    "Pantone 17-1937 TPX": "#D83A6F",
    "Pantone 18-1755 C": "#C42C5B",
    "Pantone 17-1926 TCX": "#CE3A6D",
    "Pantone 702 C": "#D25066",
    "Pantone 703 C": "#B83A4B",
    "Pantone 710 C": "#E1523D",
    "Pantone 711 C": "#CB2C30",
    "Pantone 7418 C": "#D85A4A",
    "Pantone 184 C": "#E73562",
    "Pantone 183 C": "#F8A3B5",
    "Pantone 190 C": "#F67599",
    "Pantone 1905 C": "#F57EB6",
    "Pantone Rhodamine Red C": "#E10098",
    "Pantone Rubine Red C": "#CE0058",
    "Pantone 7648 C": "#6A1F44",
    "Pantone 7423 C": "#E03E52",
}

# Uncoated approximations often print lighter/duller; include a U set for ranking.
PANTONE_U = {
    "Pantone 021 U": "#FF6A39",
    "Pantone 1585 U": "#F57D3C",
    "Pantone 1595 U": "#D36D32",
    "Pantone 165 U": "#FF7A3D",
    "Pantone 1655 U": "#FF6A2C",
    "Pantone 166 U": "#E25A1C",
    "Pantone 1665 U": "#E0561A",
    "Pantone 167 U": "#C45A24",
    "Pantone 1675 U": "#B0512A",
    "Pantone 172 U": "#F25A2A",
    "Pantone 173 U": "#D1542C",
    "Pantone 174 U": "#A3442A",
    "Pantone 179 U": "#E05240",
    "Pantone 1795 U": "#D04040",
    "Pantone 485 U": "#E04838",
    "Pantone 7583 U": "#C46A3A",
    "Pantone 7597 U": "#D15530",
    "Pantone 124 U": "#E8B13A",
    "Pantone 130 U": "#F0B02A",
    "Pantone 123 U": "#FFC84A",
    "Pantone 1235 U": "#F5B63A",
    "Pantone 7408 U": "#F0BE2A",
    "Pantone 7409 U": "#E8B03A",
    "Pantone 143 U": "#E0B040",
    "Pantone 142 U": "#E8C05A",
    "Pantone 7550 U": "#D0A040",
    "Pantone 116 U": "#FFD24A",
    "Pantone 110 U": "#D4AE20",
    "Pantone 7753 U": "#C8A830",
    "Pantone 125 U": "#C49628",
    "Pantone 131 U": "#C89020",
    "Pantone 137 U": "#F5A830",
    "Pantone 294 U": "#1E4A78",
    "Pantone 2945 U": "#1E5A92",
    "Pantone 287 U": "#1E3C80",
    "Pantone 534 U": "#2A4468",
    "Pantone 647 U": "#3A6A90",
    "Pantone 653 U": "#3A6490",
    "Pantone 654 U": "#1E4A72",
    "Pantone 7685 U": "#3A5A90",
    "Pantone 7686 U": "#2C5588",
    "Pantone 7687 U": "#2A4E82",
    "Pantone 7693 U": "#2A5588",
    "Pantone 541 U": "#1E4A70",
    "Pantone 301 U": "#1E5A82",
    "Pantone 7462 U": "#2A5A86",
    "Pantone 646 U": "#6A90B0",
    "Pantone 281 U": "#1A2C5A",
    "Pantone 282 U": "#1A2848",
    "Pantone 7546 U": "#3A4A58",
    "Pantone 432 U": "#3E4A52",
    "Pantone Black U": "#3A3634",
    "Pantone Black 6 U": "#2A2C30",
    "Pantone Black 7 U": "#4A4642",
    "Pantone Black 4 U": "#4A4036",
    "Pantone Black 2 U": "#4A4638",
    "Pantone Neutral Black U": "#3A3A3C",
    "Pantone 419 U": "#3A3C3A",
    "Pantone 426 U": "#3C4042",
    "Pantone 433 U": "#343C44",
    "Pantone 447 U": "#4A4C48",
    "Pantone 440 U": "#4A403C",
    "Pantone 7533 U": "#5A4A3A",
    "Pantone Warm Gray 11 U": "#7A7068",
    "Pantone Warm Gray 1 U": "#DCD6CE",
    "Pantone 7527 U": "#D8D4C8",
    "Pantone 7500 U": "#E4D6C4",
    "Pantone 7501 U": "#DCCBB6",
    "Pantone 7506 U": "#F0DCB6",
    "Pantone 468 U": "#E0D0AC",
    "Pantone 726 U": "#EED6B8",
    "Pantone 4685 U": "#E2C8B0",
    "Pantone 7401 U": "#F2E4B0",
    "Pantone 7499 U": "#F0E6B8",
    "Pantone 348 U": "#2A8A4A",
    "Pantone 349 U": "#2A7040",
    "Pantone 355 U": "#2A9A48",
    "Pantone 356 U": "#1E7A3A",
    "Pantone 347 U": "#2A9A50",
    "Pantone 7731 U": "#3A7A50",
    "Pantone 7732 U": "#2A704C",
    "Pantone 335 U": "#2A7A58",
    "Pantone 7725 U": "#2A8260",
    "Pantone 3425 U": "#1E6A48",
    "Pantone 124 U": "#E8B13A",
    "Pantone 130 U": "#F0B02A",
    "Pantone 7550 U": "#D0A040",
    "Pantone 7408 U": "#F0BE2A",
    "Pantone 205 U": "#E05880",
    "Pantone 213 U": "#E04078",
    "Pantone 191 U": "#E85078",
    "Pantone 7424 U": "#E05080",
    "Pantone 214 U": "#C83868",
    "Pantone 218 U": "#E06A90",
    "Pantone 7433 U": "#D87898",
    "Pantone 702 U": "#D05A6A",
    "Pantone 190 U": "#F0809A",
    "Pantone Rubine Red U": "#D04068",
    "Pantone 184 U": "#E04868",
}


# Drop entries that are off-library or not securely identified as PMS Graphic codes.
_DROP_PMS = {
    "Pantone 9083 C", "Pantone 9161 C", "Pantone 9162 C", "Pantone 9040 C",
    "Pantone 9184 C", "Pantone 1105 C", "Pantone 17-2031", "Pantone 17-1937 TPX",
    "Pantone 18-1755 C", "Pantone 17-1926 TCX", "Pantone 2256 C", "Pantone 2260 C",
    "Pantone 5335 C",
}
PANTONE_C = {k: v for k, v in PANTONE_C.items() if k not in _DROP_PMS}

def nearest_pantone(hex_color: str, library: dict):
    lab = srgb_to_lab(hex_to_rgb(hex_color))
    ranked = []
    for name, hx in library.items():
        de = ciede2000(lab, srgb_to_lab(hex_to_rgb(hx)))
        ranked.append((de, name, hx.upper()))
    ranked.sort(key=lambda x: x[0])
    return ranked[:3]


# CMYK via LittleCMS + Ghostscript Artifex SWOP profile (disclosed in README)
SRGB_ICC = "/usr/share/color/icc/ghostscript/srgb.icc"
CMYK_ICC = "/usr/share/color/icc/ghostscript/default_cmyk.icc"


def srgb_to_cmyk_swop(hex_color: str):
    srgb = ImageCms.getOpenProfile(SRGB_ICC)
    cmyk_p = ImageCms.getOpenProfile(CMYK_ICC)
    # 1 = Relative Colorimetric
    xform = ImageCms.buildTransformFromOpenProfiles(
        srgb, cmyk_p, "RGB", "CMYK", renderingIntent=1
    )
    im = Image.new("RGB", (1, 1), hex_to_rgb(hex_color))
    out = ImageCms.applyTransform(im, xform)
    c, m, y, k = out.getpixel((0, 0))
    return (
        round(c * 100 / 255),
        round(m * 100 / 255),
        round(y * 100 / 255),
        round(k * 100 / 255),
    )


# ---------------------------------------------------------------------------
# Typography outlines
# ---------------------------------------------------------------------------
SORA_SB = "/tmp/fonts/Sora-SemiBold.ttf"
SORA_MD = "/tmp/fonts/Sora-Medium.ttf"
PLEX_MD = "/tmp/fonts/IBMPlexSans-Medium.ttf"
PLEX_RG = "/tmp/fonts/IBMPlexSans-Regular.ttf"


def shape_paths(font_path: str, text: str, font_size: float, letter_spacing: float = 0.0):
    data = Path(font_path).read_bytes()
    face = hb.Face(data)
    font = hb.Font(face)
    upem = face.upem
    font.scale = (upem, upem)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    tt = TTFont(font_path)
    glyph_set = tt.getGlyphSet()
    scale = font_size / upem
    paths = []
    x_cursor = 0.0
    minx = miny = 1e9
    maxx = maxy = -1e9
    infos, positions = buf.glyph_infos, buf.glyph_positions
    n = len(infos)
    for i, (info, pos) in enumerate(zip(infos, positions)):
        name = tt.getGlyphName(info.codepoint)
        pen = SVGPathPen(glyph_set)
        x = (x_cursor + pos.x_offset) * scale
        y = -(pos.y_offset) * scale  # baseline y=0, SVG y-down
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x, y))
        glyph_set[name].draw(tpen)
        d = pen.getCommands()
        if d:
            paths.append(d)
        bpen = BoundsPen(glyph_set)
        tpen2 = TransformPen(bpen, (scale, 0, 0, -scale, x, y))
        glyph_set[name].draw(tpen2)
        if bpen.bounds:
            x0, y0, x1, y1 = bpen.bounds
            minx, miny, maxx, maxy = min(minx, x0), min(miny, y0), max(maxx, x1), max(maxy, y1)
        x_cursor += pos.x_advance
        if i < n - 1:
            x_cursor += letter_spacing * upem / font_size
    width = x_cursor * scale
    if minx > maxx:
        minx = miny = 0
        maxx, maxy = width, font_size
    return {
        "paths": paths,
        "width": width,
        "bounds": (minx, miny, maxx, maxy),
        "cap": -miny,  # since baseline 0, top is negative in font but we flipped
    }


def paths_to_el(paths, fill, extra=""):
    parts = [f'<path d="{d}" fill="{fill}"{extra}/>' for d in paths if d]
    return "\n    ".join(parts)


# ---------------------------------------------------------------------------
# Mark drawing
# ---------------------------------------------------------------------------
def mark_elements(sun, horizon, gold, simple=False, stroke_sun=None):
    if simple:
        r, cx, cy = SIMPLE_R, SIMPLE_CX, SIMPLE_CY
        bx, by, bw, bh = SIMPLE_BAR_X, SIMPLE_BAR_Y, SIMPLE_BAR_W, SIMPLE_BAR_H
        parts = [
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{sun}"/>',
            f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{gold}"/>',
        ]
        if stroke_sun:
            parts[0] = (
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{sun}" '
                f'stroke="{stroke_sun}" stroke-width="0"/>'
            )
        return "\n    ".join(parts)
    parts = [
        f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{sun}"/>',
        (
            f'<line x1="{HORIZON_X1}" y1="{HORIZON_Y}" x2="{HORIZON_X2}" y2="{HORIZON_Y}" '
            f'stroke="{horizon}" stroke-width="{HORIZON_W}" stroke-linecap="butt"/>'
        ),
        f'<rect x="{BAR_X}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" fill="{gold}"/>',
    ]
    return "\n    ".join(parts)


def svg_doc(w, h, body, vb=None, bg=None, extras=""):
    vb = vb or f"0 0 {w} {h}"
    bg_el = ""
    if bg and bg not in ("none", "transparent"):
        # paint a rect of the viewBox
        nums = [float(x) for x in vb.split()]
        bg_el = f'<rect x="{nums[0]}" y="{nums[1]}" width="{nums[2]}" height="{nums[3]}" fill="{bg}"/>\n  '
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="{vb}" fill="none" role="img" aria-label="Chamuka Daybreak mark">\n'
        f"{extras}"
        f"  {bg_el}{body}\n"
        f"</svg>\n"
    )


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Lockup construction
# ---------------------------------------------------------------------------
# Mark is 64 units tall. Wordmark cap height is optically matched to the mark
# (top of disc to bottom of gold bar ≈ 50-5.5 = 44.5). Baseline sits on the
# gold-bar bottom (y=50). Slight tracking.
MARK_TOP = CY - R  # 5.5
MARK_BOT = BAR_Y + BAR_H  # 50.0
MARK_H = MARK_BOT - MARK_TOP  # 44.5


def lockup_horizontal(
    sun, horizon, gold, word_fill, product=None, product_fill=None, simple=False, pad=16
):
    # Wordmark in Sora SemiBold. Cap height ≈ 0.92 of mark optical height.
    cap_target = MARK_H * 0.92
    # Sora cap-height is roughly 0.70 of em (we'll measure)
    sample = shape_paths(SORA_SB, "Chamuka", 100)
    _, y0, _, y1 = sample["bounds"]
    cap_at_100 = abs(y0)  # top is negative? we flipped: top is negative no
    # After y-flip, glyph tops are negative of original? Transform is (s,0,0,-s,x,y)
    # Font y-up: cap is +cap, after -s it becomes negative. So y0 is top (more negative / smaller).
    cap_at_100 = abs(y0)
    font_size = 100 * cap_target / cap_at_100
    word = shape_paths(SORA_SB, "Chamuka", font_size, letter_spacing=0)
    _, wy0, _, wy1 = word["bounds"]
    # Place word so its top ≈ MARK_TOP + small optical drop, baseline at MARK_BOT
    # Align baseline to MARK_BOT (bar bottom)
    word_dx = HORIZON_X2 + 16  # gap measured from the horizon’s right edge (~1 radius)
    # word paths are baseline at 0; we translate by ty so baseline = MARK_BOT
    ty = MARK_BOT
    word_el = (
        f'<g transform="translate({word_dx:.3f} {ty:.3f})">\n'
        f"      {paths_to_el(word['paths'], word_fill)}\n    </g>"
    )
    end_x = word_dx + word["width"]
    prod_el = ""
    if product:
        # IBM Plex Sans Medium, smaller, to the right of Chamuka with a mid-dot or gap
        psize = font_size * 0.72
        prod = shape_paths(PLEX_MD, product, psize)
        gap = 12
        px = end_x + gap
        # baseline align with wordmark
        prod_el = (
            f'<g transform="translate({px:.3f} {ty:.3f})">\n'
            f"      {paths_to_el(prod['paths'], product_fill or word_fill)}\n    </g>"
        )
        end_x = px + prod["width"]
    width = end_x + pad
    height = 64
    body = (
        f'<g transform="translate(0 0)">\n    {mark_elements(sun, horizon, gold, simple=simple)}\n  </g>\n'
        f"    {word_el}\n    {prod_el}"
    )
    # viewBox with padding
    vb = f"{-pad} {-pad} {width + pad} {height + 2 * pad}"
    return width + 2 * pad, height + 2 * pad, body, vb, word, font_size, ty, word_dx


def lockup_stacked(sun, horizon, gold, word_fill, product=None, product_fill=None, simple=False, pad=16):
    cap_target = 22  # stacked wordmark slightly smaller relative to mark
    sample = shape_paths(SORA_SB, "Chamuka", 100)
    y0 = sample["bounds"][1]
    cap_at_100 = abs(y0)
    font_size = 100 * cap_target / cap_at_100
    word = shape_paths(SORA_SB, "Chamuka", font_size)
    word_w = word["width"]
    mark_box = 64
    content_w = max(mark_box, word_w)
    mark_x = (content_w - mark_box) / 2
    word_x = (content_w - word_w) / 2
    cap = abs(word["bounds"][1])
    # Gap measured from the gold-bar bottom, not the 64-unit frame
    word_ty = MARK_BOT + 10 + cap
    word_el = (
        f'<g transform="translate({word_x:.3f} {word_ty:.3f})">\n'
        f"      {paths_to_el(word['paths'], word_fill)}\n    </g>"
    )
    height = word_ty + (word["bounds"][3] if word["bounds"][3] > 0 else font_size * 0.2)
    prod_el = ""
    if product:
        psize = font_size * 0.58
        prod = shape_paths(PLEX_MD, product, psize)
        prod_w = prod["width"]
        prod_x = (content_w - prod_w) / 2
        pcap = abs(prod["bounds"][1])
        prod_ty = height + 6 + pcap
        prod_el = (
            f'<g transform="translate({prod_x:.3f} {prod_ty:.3f})">\n'
            f"      {paths_to_el(prod['paths'], product_fill or word_fill)}\n    </g>"
        )
        height = prod_ty + max(prod["bounds"][3], psize * 0.2)
    width = content_w
    body = (
        f'<g transform="translate({mark_x:.3f} 0)">\n    {mark_elements(sun, horizon, gold, simple=simple)}\n  </g>\n'
        f"    {word_el}\n    {prod_el}"
    )
    vb = f"{-pad} {-pad} {width + 2 * pad} {height + 2 * pad}"
    return width + 2 * pad, height + 2 * pad, body, vb


def raster(svg_path: Path, png_path: Path, scale=2, background=None, output_width=None):
    kwargs = {"scale": scale, "write_to": str(png_path)}
    if background:
        kwargs["background_color"] = background
    if output_width:
        kwargs = {"output_width": output_width, "write_to": str(png_path)}
        if background:
            kwargs["background_color"] = background
    cairosvg.svg2png(url=str(svg_path), **kwargs)
    print("png", png_path)


def main():
    ember, gold, slate = PALETTE["ember"], PALETTE["gold"], PALETTE["slate"]
    ink, paper, white = PALETTE["ink"], PALETTE["paper"], PALETTE["white"]

    # ---- Colour math -------------------------------------------------------
    colour_rows = []
    all_named = dict(PALETTE)
    # don't include transparent/white as core print targets except paper
    core_for_print = [
        "ember",
        "gold",
        "slate",
        "paper",
        "mist",
        "ink",
        "muted",
        "success",
        "warning",
        "danger",
        "info",
        "play",
    ]
    print_specs = {}
    for name in core_for_print:
        hx = PALETTE[name]
        rgb = hex_to_rgb(hx)
        hsl = rgb_to_hsl(*rgb)
        cmyk = srgb_to_cmyk_swop(hx)
        near_c = nearest_pantone(hx, PANTONE_C)
        near_u = nearest_pantone(hx, PANTONE_U)
        rec = {
            "name": name,
            "hex": hx,
            "rgb": rgb,
            "hsl": {"h": hsl[0], "s": hsl[1], "l": hsl[2]},
            "cmyk_swop_relative": {"c": cmyk[0], "m": cmyk[1], "y": cmyk[2], "k": cmyk[3]},
            "pantone_coated_nearest": [
                {"name": n, "hex_approx": h, "delta_e00": round(de, 2)} for de, n, h in near_c
            ],
            "pantone_uncoated": {
                "recommended": (near_c[0][1].rsplit(" ", 1)[0] + " U") if near_c else None,
                "note": (
                    "Conventional pairing: use the Uncoated (U) ink of the same PMS number "
                    "as the nearest coated match. C and U of one number do not look identical; "
                    "uncoated stock absorbs more and prints softer. This is not a separately "
                    "measured nearest-U match. Verify against a physical Pantone Uncoated guide "
                    "on the actual stock before printing."
                ),
            },
        }
        print_specs[name] = rec
        colour_rows.append(rec)
        print(
            f"{name:8} {hx} RGB{rgb} HSL{hsl} CMYK{cmyk}  "
            f"C:{near_c[0][1]} ΔE{near_c[0][0]:.2f}  U-pair:{near_c[0][1].rsplit(' ', 1)[0]} U"
        )

    # Neutrals CMYK too
    neutrals_spec = {}
    for k, hx in NEUTRALS.items():
        rgb = hex_to_rgb(hx)
        cmyk = srgb_to_cmyk_swop(hx)
        neutrals_spec[k] = {
            "hex": hx,
            "rgb": rgb,
            "hsl": dict(zip("hsl", rgb_to_hsl(*rgb))),
            "cmyk_swop_relative": {"c": cmyk[0], "m": cmyk[1], "y": cmyk[2], "k": cmyk[3]},
        }

    pairs = [
        ("ink", "paper"),
        ("ink", "mist"),
        ("ink", "white"),
        ("ember", "paper"),
        ("ember", "white"),
        ("ember", "ink"),
        ("gold", "ink"),
        ("gold", "paper"),
        ("slate", "paper"),
        ("slate", "white"),
        ("slate", "ink"),
        ("white", "ember"),
        ("white", "slate"),
        ("white", "ink"),
        ("paper", "ember"),
        ("paper", "slate"),
        ("paper", "ink"),
        ("muted", "paper"),
        ("muted", "ink"),
        ("success", "paper"),
        ("success", "white"),
        ("warning", "ink"),
        ("warning", "paper"),
        ("danger", "paper"),
        ("danger", "white"),
        ("info", "paper"),
        ("play", "paper"),
        ("play", "white"),
        ("play", "ink"),
    ]
    contrast = []
    for a, b in pairs:
        r = contrast_ratio(PALETTE[a], PALETTE[b])
        contrast.append(
            {
                "fg": a,
                "bg": b,
                "ratio": round(r, 2),
                "aa_normal": wcag_level(r, False),
                "aa_large": wcag_level(r, True),
            }
        )
        print(f"  contrast {a} on {b}: {r:.2f}  normal={wcag_level(r)}  large={wcag_level(r, True)}")

    (ROOT / "colors.json").write_text(
        json.dumps(
            {
                "cmyk_method": (
                    "Separated from sRGB with LittleCMS (Pillow ImageCms) using the "
                    "Ghostscript sRGB profile and the Artifex CMYK SWOP profile "
                    "(default_cmyk.icc), Relative Colorimetric intent. Values rounded "
                    "to whole percentages. This is a US SWOP-like coated separation, "
                    "not FOGRA39 / ISO Coated v2 and not GRACoL 2013. European printers "
                    "should re-separate to FOGRA39 (ISO Coated v2 300%) in prepress; "
                    "North American printers should re-separate to GRACoL 2013 (CRPC6) "
                    "if that is the house profile. Treat these CMYK builds as starting points."
                ),
                "pantone_method": (
                    "Nearest coated matches ranked by CIEDE2000 (D65/2°, sRGB-encoded Lab) "
                    "against a compiled table of commonly circulated Pantone Color Bridge / "
                    "converter *screen* hex approximations. These are not official "
                    "Pantone-published measurements. Uncoated recommendations are the same "
                    "PMS number in the Uncoated library (conventional C/U pairing), not a "
                    "separately computed nearest-U. Every match is a nearest match and must "
                    "be verified against a physical Pantone Coated or Uncoated guide before printing."
                ),
                "core": print_specs,
                "neutrals": neutrals_spec,
                "contrast": contrast,
            },
            indent=2,
        )
    )

    # ---- Logo SVGs ---------------------------------------------------------
    # Standalone colour mark, transparent
    write(
        SVG / "mark.svg",
        svg_doc(64, 64, mark_elements(ember, slate, gold), bg=None),
    )
    write(
        SVG / "mark-simple.svg",
        svg_doc(64, 64, mark_elements(ember, slate, gold, simple=True)),
    )
    write(
        SVG / "mark-on-cream.svg",
        svg_doc(64, 64, mark_elements(ember, slate, gold), bg=paper),
    )
    write(
        SVG / "mark-on-ember.svg",
        svg_doc(64, 64, mark_elements(paper, paper, paper), bg=ember),
    )
    write(
        SVG / "mark-on-slate.svg",
        svg_doc(64, 64, mark_elements(paper, paper, paper), bg=slate),
    )
    write(
        SVG / "mark-mono-dark.svg",
        svg_doc(64, 64, mark_elements(ink, ink, ink)),
    )
    write(
        SVG / "mark-mono-light.svg",
        svg_doc(64, 64, mark_elements(white, white, white)),
    )

    # Print one-ink / knockout
    write(
        PRINT_SVG / "mark-ink-on-light.svg",
        svg_doc(64, 64, mark_elements(ink, ink, ink)),
    )
    write(
        PRINT_SVG / "mark-white-on-ember.svg",
        svg_doc(64, 64, mark_elements(white, white, white), bg=ember),
    )
    write(
        PRINT_SVG / "mark-white-on-slate.svg",
        svg_doc(64, 64, mark_elements(white, white, white), bg=slate),
    )
    write(
        PRINT_SVG / "mark-knockout.svg",
        svg_doc(64, 64, mark_elements(white, white, white)),
    )
    write(
        PRINT_SVG / "mark-simple-one-colour-ink.svg",
        svg_doc(64, 64, mark_elements(ink, ink, ink, simple=True)),
    )
    write(
        PRINT_SVG / "mark-simple-one-colour-ember.svg",
        svg_doc(64, 64, mark_elements(ember, ember, ember, simple=True)),
    )
    write(
        PRINT_SVG / "mark-simple-one-colour-white.svg",
        svg_doc(64, 64, mark_elements(white, white, white, simple=True)),
    )

    # Horizontal / stacked lockups
    variants = [
        ("lockup-horizontal", ember, slate, gold, ink, None, None, False, None),
        ("lockup-horizontal-mono-dark", ink, ink, ink, ink, None, None, False, None),
        ("lockup-horizontal-mono-light", white, white, white, white, None, None, False, None),
        ("lockup-drawit", ember, slate, gold, ink, "DrawIt", ember, False, None),
        ("lockup-formit", ember, slate, gold, ink, "FormIt", slate, False, None),
        ("lockup-play", ember, slate, gold, ink, "Play", PALETTE["play"], False, None),
    ]
    for name, su, ho, go, wf, prod, pf, simple, bg in variants:
        w, h, body, vb, *_ = lockup_horizontal(su, ho, go, wf, prod, pf, simple)
        write(SVG / f"{name}.svg", svg_doc(w, h, body, vb=vb, bg=bg))

    # Cream / ember / slate lockup plates
    w, h, body, vb, *_ = lockup_horizontal(ember, slate, gold, ink)
    write(SVG / "lockup-horizontal-on-cream.svg", svg_doc(w, h, body, vb=vb, bg=paper))
    w, h, body, vb, *_ = lockup_horizontal(paper, paper, paper, paper)
    write(SVG / "lockup-horizontal-on-ember.svg", svg_doc(w, h, body, vb=vb, bg=ember))
    write(SVG / "lockup-horizontal-on-slate.svg", svg_doc(w, h, body, vb=vb, bg=slate))

    w, h, body, vb = lockup_stacked(ember, slate, gold, ink)
    write(SVG / "lockup-stacked.svg", svg_doc(w, h, body, vb=vb))
    write(SVG / "lockup-stacked-on-cream.svg", svg_doc(w, h, body, vb=vb, bg=paper))
    for prod, pf, fname in (
        ("DrawIt", ember, "lockup-stacked-drawit"),
        ("FormIt", slate, "lockup-stacked-formit"),
        ("Play", PALETTE["play"], "lockup-stacked-play"),
    ):
        w, h, body, vb = lockup_stacked(ember, slate, gold, ink, prod, pf)
        write(SVG / f"{fname}.svg", svg_doc(w, h, body, vb=vb))

    # Print lockups
    w, h, body, vb, *_ = lockup_horizontal(ink, ink, ink, ink)
    write(PRINT_SVG / "lockup-ink-on-light.svg", svg_doc(w, h, body, vb=vb))
    w, h, body, vb, *_ = lockup_horizontal(white, white, white, white)
    write(PRINT_SVG / "lockup-white-on-ember.svg", svg_doc(w, h, body, vb=vb, bg=ember))
    write(PRINT_SVG / "lockup-white-on-slate.svg", svg_doc(w, h, body, vb=vb, bg=slate))
    w, h, body, vb, *_ = lockup_horizontal(ink, ink, ink, ink, simple=True)
    write(PRINT_SVG / "lockup-simple-one-colour-ink.svg", svg_doc(w, h, body, vb=vb))
    w, h, body, vb, *_ = lockup_horizontal(ember, ember, ember, ember, simple=True)
    write(PRINT_SVG / "lockup-simple-one-colour-ember.svg", svg_doc(w, h, body, vb=vb))
    w, h, body, vb, *_ = lockup_horizontal(white, white, white, white, simple=True)
    write(PRINT_SVG / "lockup-simple-one-colour-white.svg", svg_doc(w, h, body, vb=vb))

    # Wordmark alone
    w, h, body, vb, word, fs, ty, dx = lockup_horizontal(ember, slate, gold, ink)
    # extract just word — rebuild
    sample = shape_paths(SORA_SB, "Chamuka", 100)
    cap = abs(sample["bounds"][1])
    font_size = 72
    word = shape_paths(SORA_SB, "Chamuka", font_size)
    pad = 8
    ww = word["width"] + 2 * pad
    # bounds y0 is top (negative or small)
    y0, y1 = word["bounds"][1], word["bounds"][3]
    hh = (y1 - y0) + 2 * pad
    body = f'<g transform="translate({pad - word["bounds"][0]:.3f} {pad - y0:.3f})">\n    {paths_to_el(word["paths"], ink)}\n  </g>'
    write(SVG / "wordmark.svg", svg_doc(ww, hh, body, vb=f"0 0 {ww} {hh}"))

    # App icon 512 and favicons
    def app_icon(size, field, sun, horizon, gold, radius_ratio=0.22, simple=None):
        # Center the *optical* mark (disc top to bar bottom, horizon width),
        # not the padded 64-unit frame, so 16px/32px icons still read clearly.
        use_simple = simple if simple is not None else size <= 32
        if use_simple:
            ox0, oy0 = SIMPLE_BAR_X, SIMPLE_CY - SIMPLE_R
            ox1, oy1 = SIMPLE_BAR_X + SIMPLE_BAR_W, SIMPLE_BAR_Y + SIMPLE_BAR_H
        else:
            ox0, oy0 = HORIZON_X1, MARK_TOP
            ox1, oy1 = HORIZON_X2, MARK_BOT
        ow, oh = ox1 - ox0, oy1 - oy0
        fill = 0.66 if size <= 32 else 0.54
        scale = (size * fill) / oh
        tx = (size - ow * scale) / 2 - ox0 * scale
        ty = (size - oh * scale) / 2 - oy0 * scale
        rr = size * radius_ratio
        bg = f'<rect width="{size}" height="{size}" rx="{rr}" ry="{rr}" fill="{field}"/>'
        inner = mark_elements(sun, horizon, gold, simple=use_simple)
        body = f"{bg}\n  <g transform='translate({tx:.3f} {ty:.3f}) scale({scale:.5f})'>\n    {inner}\n  </g>"
        return svg_doc(size, size, body, vb=f"0 0 {size} {size}")

    write(SVG / "app-icon-512.svg", app_icon(512, paper, ember, slate, gold, simple=False))
    write(SVG / "app-icon-512-ember.svg", app_icon(512, ember, paper, paper, paper, simple=False))
    write(SVG / "favicon-32.svg", app_icon(32, paper, ember, slate, gold, simple=True))
    write(SVG / "favicon-16.svg", app_icon(16, paper, ember, slate, gold, simple=True))
    # Product app icons
    write(SVG / "app-icon-drawit-512.svg", app_icon(512, ember, paper, paper, paper, simple=False))
    write(SVG / "app-icon-formit-512.svg", app_icon(512, slate, paper, paper, paper, simple=False))
    write(
        SVG / "app-icon-play-512.svg",
        app_icon(512, PALETTE["play"], paper, paper, paper, simple=False),
    )

    # Clear-space diagram
    clear = R  # one sun radius on every side of the optical mark box
    # Use horizontal lockup, draw a dashed clear box
    w, h, body, vb, *_ = lockup_horizontal(ember, slate, gold, ink)
    # parse vb
    vx, vy, vw, vh = [float(x) for x in vb.split()]
    # lockup content without pad is inset by 16 in constructor (pad=16)
    # clear space unit = R = 16, which equals the construction pad — good.
    guide = f"""
  <g fill="none" stroke="{slate}" stroke-width="0.4" stroke-dasharray="1.5 1.5" opacity="0.85">
    <rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"/>
  </g>
  <g font-family="sans-serif" font-size="4.5" fill="{slate}">
    <text x="{vx + vw/2}" y="{vy - 1.5}" text-anchor="middle">Clear space = 1 sun radius ({R:.0f} units, equal to half the disc diameter)</text>
  </g>
"""
    # The constructor already padded by 16 = R, so the viewBox IS the clear-space box
    write(
        SVG / "clear-space.svg",
        svg_doc(w, h, body + guide, vb=f"{vx} {vy-8} {vw} {vh+10}", bg=paper),
    )

    # Don'ts as a simple labeled sheet (will also describe in README)
    dont_items = []
    # We'll render a later specimen; skip a heavy don'ts illustration here and
    # describe in the Page. A compact don'ts SVG follows in _build_templates.

    # ---- Raster previews ---------------------------------------------------
    # Colour marks on cream / transparent (use cream for QA visibility)
    raster(SVG / "mark-on-cream.svg", PNG / "mark-on-cream.png", output_width=512)
    raster(SVG / "mark-on-ember.svg", PNG / "mark-on-ember.png", output_width=512)
    raster(SVG / "mark-on-slate.svg", PNG / "mark-on-slate.png", output_width=512)
    raster(SVG / "mark.svg", PNG / "mark.png", output_width=512, background="transparent")
    raster(SVG / "mark-simple.svg", PNG / "mark-simple.png", output_width=512, background="transparent")
    raster(SVG / "mark-mono-dark.svg", PNG / "mark-mono-dark.png", output_width=512, background="transparent")
    raster(SVG / "mark-mono-light.svg", PNG / "mark-mono-light.png", output_width=512, background="#17141C")
    raster(SVG / "lockup-horizontal-on-cream.svg", PNG / "lockup-horizontal-on-cream.png", output_width=1600)
    raster(SVG / "lockup-horizontal-on-ember.svg", PNG / "lockup-horizontal-on-ember.png", output_width=1600)
    raster(SVG / "lockup-horizontal-on-slate.svg", PNG / "lockup-horizontal-on-slate.png", output_width=1600)
    raster(SVG / "lockup-horizontal.svg", PNG / "lockup-horizontal.png", output_width=1600, background="transparent")
    raster(SVG / "lockup-stacked-on-cream.svg", PNG / "lockup-stacked-on-cream.png", output_width=800)
    raster(SVG / "lockup-stacked.svg", PNG / "lockup-stacked.png", output_width=800, background="transparent")
    raster(SVG / "lockup-drawit.svg", PNG / "lockup-drawit.png", output_width=1800, background="#FFF8F1")
    raster(SVG / "lockup-formit.svg", PNG / "lockup-formit.png", output_width=1800, background="#FFF8F1")
    raster(SVG / "lockup-play.svg", PNG / "lockup-play.png", output_width=1800, background="#FFF8F1")
    raster(SVG / "app-icon-512.svg", PNG / "app-icon-512.png", output_width=512)
    raster(SVG / "app-icon-512-ember.svg", PNG / "app-icon-512-ember.png", output_width=512)
    raster(SVG / "app-icon-drawit-512.svg", PNG / "app-icon-drawit-512.png", output_width=512)
    raster(SVG / "app-icon-formit-512.svg", PNG / "app-icon-formit-512.png", output_width=512)
    raster(SVG / "app-icon-play-512.svg", PNG / "app-icon-play-512.png", output_width=512)
    raster(SVG / "favicon-32.svg", PNG / "favicon-32.png", output_width=32)
    raster(SVG / "favicon-16.svg", PNG / "favicon-16.png", output_width=16)
    raster(SVG / "wordmark.svg", PNG / "wordmark.png", output_width=1200, background="transparent")
    raster(SVG / "clear-space.svg", PNG / "clear-space.png", output_width=1600)
    raster(PRINT_SVG / "lockup-ink-on-light.svg", PRINT_PNG / "lockup-ink-on-light.png", output_width=1600, background="#FFF8F1")
    raster(PRINT_SVG / "lockup-white-on-ember.svg", PRINT_PNG / "lockup-white-on-ember.png", output_width=1600)
    raster(PRINT_SVG / "lockup-white-on-slate.svg", PRINT_PNG / "lockup-white-on-slate.png", output_width=1600)
    raster(PRINT_SVG / "mark-simple-one-colour-ink.svg", PRINT_PNG / "mark-simple-one-colour-ink.png", output_width=512, background="#FFF8F1")
    raster(PRINT_SVG / "mark-simple-one-colour-ember.svg", PRINT_PNG / "mark-simple-one-colour-ember.png", output_width=512, background="#FFF8F1")

    print("LOGO BUILD OK")


if __name__ == "__main__":
    main()

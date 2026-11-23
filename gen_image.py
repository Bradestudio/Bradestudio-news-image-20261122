#!/usr/bin/env python3
"""Draw the Sunday 22 November 2026 front page from scratch.

Round 2 of the news-image-20261122 entry. Everything is drawn with
Pillow shapes and text only: no photos, no network, no clock, no
randomness, so two runs produce byte-identical PNGs.

Layout, top to bottom on a 1024x1024 sheet:
  masthead -> 3 illustrated hero panels -> UTC timeline ->
  BY THE NUMBERS strip -> 9 briefs with drawn thumbnails ->
  dot-matrix world map -> 36 more stories -> DATE CHECK footer.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # 976, the content width

# --- palette -----------------------------------------------------------
PAPER = (246, 241, 229)
INK = (25, 23, 19)
SOFT = (107, 101, 90)
RULE = (25, 23, 19)
RED = (156, 31, 31)
BLUE = (29, 63, 110)
GOLD = (146, 104, 12)
FAINT = (232, 226, 212)
PANEL = (255, 253, 247)
SKY_NIGHT = (13, 22, 48)
SKY_DUSK = (64, 48, 84)
SEA = (18, 48, 84)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_cache = {}


def font(path, size):
    """Load a truetype font, cached; fall back to the default bitmap font."""
    key = (path, size)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _cache[key] = ImageFont.load_default()
    return _cache[key]


def serif_b(size):
    return font(SERIF_B, size)


def serif(size):
    return font(SERIF, size)


def sans(size):
    return font(SANS, size)


def sans_b(size):
    return font(SANS_B, size)


def text_w(draw, text, fnt):
    """Pixel width of one line of text."""
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=0):
    """Draw stacked lines; leading is extra space between lines."""
    step = fnt.size + leading
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def tag_chip(draw, x, y, label):
    """Small certainty tag: REPORTED blue, CLAIM red, FORECAST gold."""
    fills = {"REPORTED": BLUE, "CLAIM": RED, "FORECAST": GOLD}
    fill = fills.get(label, BLUE)
    fnt = sans_b(8)
    w = text_w(draw, label, fnt) + 10
    draw.rounded_rectangle([x, y, x + w, y + 12], radius=6, fill=fill)
    draw.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def rule(draw, x0, y, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, r_max, r_min, colour):
    """A starburst explosion: alternating long/short spikes."""
    import math

    pts = []
    for i in range(24):
        ang = i * math.pi / 12
        r = r_max if i % 2 == 0 else r_min
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=colour)


def flame(draw, cx, base, w, h, colour):
    """One teardrop flame rising from (cx, base)."""
    draw.polygon(
        [
            (cx - w, base),
            (cx - w * 0.55, base - h * 0.55),
            (cx, base - h),
            (cx + w * 0.55, base - h * 0.55),
            (cx + w, base),
        ],
        fill=colour,
    )
    draw.ellipse([cx - w * 0.45, base - h * 0.5, cx + w * 0.45, base], fill=colour)


def puff(draw, cx, cy, r, colour):
    """A lumpy smoke puff: three overlapping ellipses, not one circle."""
    draw.ellipse([cx - r, cy - r * 0.7, cx + r * 0.4, cy + r * 0.7], fill=colour)
    draw.ellipse([cx - r * 0.4, cy - r, cx + r, cy + r * 0.5], fill=colour)
    draw.ellipse([cx - r * 0.6, cy - r * 0.4, cx + r * 0.6, cy + r * 0.9], fill=colour)


# --- hero illustrations -------------------------------------------------
# Each hero panel is a drawn scene, no photo. Fixed star positions come
# from a deterministic formula, never from the random module.


def sky_bands(draw, x, y, w, h, top, bottom, steps=8):
    """Vertical gradient made of flat bands (keeps the PNG small)."""
    for i in range(steps):
        t0 = i / steps
        t1 = (i + 1) / steps
        col = tuple(int(top[k] + (bottom[k] - top[k]) * (t0 + t1) / 2) for k in range(3))
        draw.rectangle([x, y + h * t0, x + w, y + h * t1 + 1], fill=col)


def star_field(draw, x, y, w, h, n, seed):
    """Fixed pseudo-random stars from a sine hash (deterministic)."""
    import math

    for i in range(n):
        sx = x + int(((math.sin(seed * 12.9898 + i * 78.233) * 43758.5453) % 1.0) * w)
        sy = y + int(((math.sin(seed * 4.1414 + i * 11.13) * 24634.6345) % 1.0) * h)
        r = 1 if i % 4 else 2
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 232, 220))


def hero_bahrain(draw, x, y, w, h):
    """Night over the Gulf: base silhouettes, blasts, drones, moon."""
    sky_bands(draw, x, y, w, h, (10, 16, 38), (44, 34, 66))
    star_field(draw, x, y, w, int(h * 0.55), 26, 3)
    draw.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(238, 230, 200))
    draw.ellipse([x + w - 46, y + 16, x + w - 28, y + 34], fill=(210, 198, 160))
    horizon = y + int(h * 0.68)
    # Distant base: hangars, tower, radar dome, runway lights.
    draw.rectangle([x, horizon - 26, x + w, horizon], fill=(8, 10, 24))
    draw.rectangle([x + 18, horizon - 44, x + 66, horizon - 26], fill=(8, 10, 24))
    draw.rectangle([x + 88, horizon - 52, x + 98, horizon - 26], fill=(8, 10, 24))
    draw.ellipse([x + 118, horizon - 62, x + 146, horizon - 34], fill=(8, 10, 24))
    draw.rectangle([x + 170, horizon - 40, x + 214, horizon - 26], fill=(8, 10, 24))
    for lx in range(x + 8, x + w - 8, 22):
        draw.ellipse([lx, horizon - 4, lx + 3, horizon - 1], fill=(255, 190, 90))
    # Sea below the horizon.
    draw.rectangle([x, horizon, x + w, y + h], fill=(12, 26, 52))
    for wy in range(horizon + 6, y + h - 2, 9):
        draw.line([(x + 6, wy), (x + w - 6, wy)], fill=(30, 58, 100), width=1)
    # Two blasts over the base, with smoke (all kept inside the panel).
    burst(draw, x + 52, horizon - 48, 20, 9, (255, 176, 66))
    burst(draw, x + 52, horizon - 48, 12, 6, (255, 232, 150))
    burst(draw, x + 196, horizon - 42, 16, 7, (255, 150, 50))
    burst(draw, x + 196, horizon - 42, 9, 4, (255, 220, 130))
    puff(draw, x + 48, horizon - 58, 11, (96, 92, 100))
    puff(draw, x + 192, horizon - 52, 9, (96, 92, 100))
    # Drone silhouettes with rotor glints.
    for dx, dy in [(x + 130, y + 22), (x + 250, y + 34), (x + 92, y + 44)]:
        draw.line([(dx - 12, dy), (dx + 12, dy)], fill=(220, 220, 220), width=2)
        draw.line([(dx, dy - 5), (dx, dy + 5)], fill=(220, 220, 220), width=2)
        draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 120, 60))
    # Missile trail arcing down to the left blast.
    draw.arc([x + 60, y + 4, x + 190, horizon - 30], start=200, end=330, fill=(255, 200, 120), width=2)


def tanker_hull(draw, x, y, w, h, hull, deck):
    """A simple tanker: long hull, bow, deckhouse, funnel."""
    draw.polygon(
        [(x, y), (x + w - 26, y), (x + w, y + h // 2), (x + w - 26, y + h), (x, y + h)],
        fill=hull,
    )
    draw.rectangle([x + 8, y - 16, x + 44, y], fill=deck)
    draw.rectangle([x + 14, y - 26, x + 38, y - 16], fill=deck)
    draw.rectangle([x + w - 78, y - 12, x + w - 62, y], fill=(150, 60, 40))
    draw.line([(x, y + h), (x + w, y + h)], fill=(0, 0, 0), width=2)


def hero_tankers(draw, x, y, w, h):
    """Dusk in the Strait of Hormuz: two tankers, one burning, a mine."""
    sky_bands(draw, x, y, w, h, (58, 44, 80), (214, 120, 66))
    draw.ellipse([x + w - 70, y + 14, x + w - 34, y + 50], fill=(255, 214, 150))
    horizon = y + int(h * 0.58)
    draw.rectangle([x, horizon, x + w, y + h], fill=(16, 42, 74))
    for wy in range(horizon + 5, y + h - 2, 8):
        draw.line([(x + 4, wy), (x + w - 4, wy)], fill=(36, 76, 120), width=1)
    # Far cliffs of the Omani coast.
    draw.polygon([(x, horizon), (x + 52, horizon - 26), (x + 96, horizon)], fill=(52, 40, 58))
    draw.polygon([(x + w - 110, horizon), (x + w - 62, horizon - 20), (x + w, horizon)], fill=(52, 40, 58))
    # Tanker one, mid-frame, stern hit and burning.
    tanker_hull(draw, x + 34, horizon - 12, 150, 16, (40, 44, 52), (200, 200, 196))
    flame(draw, x + 56, horizon - 12, 12, 30, (255, 150, 40))
    flame(draw, x + 70, horizon - 12, 8, 20, (255, 220, 110))
    burst(draw, x + 62, horizon - 34, 14, 6, (255, 190, 80))
    puff(draw, x + 58, horizon - 40, 10, (96, 92, 100))
    # Tanker two, smaller and further, listing slightly.
    tanker_hull(draw, x + 196, horizon - 8, 104, 12, (52, 54, 62), (210, 208, 200))
    flame(draw, x + 282, horizon - 8, 8, 18, (255, 150, 40))
    puff(draw, x + 280, horizon - 20, 8, (96, 92, 100))
    # A spiked naval mine floating in the foreground water.
    mx, my = x + 236, y + h - 14
    draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(20, 20, 22))
    for sx, sy in [(-8, 0), (8, 0), (0, -8), (0, 8), (-6, -6), (6, -6), (-6, 6), (6, 6)]:
        draw.line([(mx, my), (mx + sx * 1.4, my + sy * 1.4)], fill=(20, 20, 22), width=2)


def hero_sparta(draw, x, y, w, h):
    """Cold Baltic morning: Sparta II burning in the Gulf of Finland."""
    sky_bands(draw, x, y, w, h, (148, 158, 168), (196, 186, 168))
    draw.ellipse([x + 26, y + 12, x + 52, y + 30], fill=(240, 236, 220))
    horizon = y + int(h * 0.60)
    draw.rectangle([x, horizon, x + w, y + h], fill=(38, 66, 88))
    for wy in range(horizon + 5, y + h - 2, 8):
        draw.line([(x + 4, wy), (x + w - 4, wy)], fill=(70, 104, 130), width=1)
    # Low grey coastline behind the ship.
    draw.polygon([(x, horizon), (x + 70, horizon - 14), (x + 150, horizon)], fill=(110, 118, 116))
    # Cargo ship: hull, containers, bridge tower.
    draw.polygon(
        [
            (x + 30, horizon - 14),
            (x + 250, horizon - 14),
            (x + 272, horizon + 2),
            (x + 250, horizon + 14),
            (x + 30, horizon + 14),
        ],
        fill=(96, 30, 28),
    )
    for i, col in enumerate([(52, 96, 120), (168, 120, 52), (90, 110, 90), (120, 84, 60)]):
        cx0 = x + 52 + i * 34
        draw.rectangle([cx0, horizon - 34, cx0 + 30, horizon - 14], fill=col)
        draw.line([(cx0, horizon - 24), (cx0 + 30, horizon - 24)], fill=(0, 0, 0), width=1)
    draw.rectangle([x + 232, horizon - 40, x + 250, horizon - 14], fill=(220, 220, 214))
    draw.rectangle([x + 235, horizon - 46, x + 247, horizon - 40], fill=(220, 220, 214))
    # Fire amidships and a smoke column (all kept inside the panel).
    flame(draw, x + 118, horizon - 34, 18, 32, (255, 140, 30))
    flame(draw, x + 138, horizon - 34, 14, 24, (255, 210, 90))
    burst(draw, x + 128, horizon - 52, 13, 6, (255, 180, 70))
    puff(draw, x + 118, horizon - 44, 12, (96, 92, 100))
    puff(draw, x + 136, horizon - 52, 10, (110, 106, 110))
    # Small rescue tug alongside, and two gulls.
    draw.rectangle([x + 258, horizon + 20, x + 292, horizon + 30], fill=(200, 60, 40))
    draw.rectangle([x + 266, horizon + 12, x + 280, horizon + 20], fill=(240, 240, 236))
    for gx, gy in [(x + 40, y + 46), (x + 66, y + 38)]:
        draw.arc([gx - 8, gy - 5, gx, gy + 5], start=200, end=340, fill=(40, 40, 40), width=2)
        draw.arc([gx, gy - 5, gx + 8, gy + 5], start=200, end=340, fill=(40, 40, 40), width=2)


# --- small thumbnails for the briefs ------------------------------------
# Each thumbnail is a 48x48 drawn icon on a tinted square.


def thumb(draw, x, y, kind):
    """Draw one tiny scene icon for a brief, keyed by kind."""
    tints = {
        "globe": (210, 222, 232),
        "euro": (214, 200, 150),
        "cross": (226, 214, 214),
        "siren": (206, 214, 228),
        "bars": (210, 210, 204),
        "bat": (214, 224, 198),
        "bridge": (208, 220, 224),
        "gavel": (220, 206, 180),
        "flag": (212, 220, 230),
    }
    draw.rectangle([x, y, x + 48, y + 48], fill=tints.get(kind, (220, 220, 214)))
    draw.rectangle([x, y, x + 48, y + 48], outline=(120, 112, 96), width=1)
    cx, cy = x + 24, y + 24
    if kind == "globe":  # COP31: a globe on a table
        draw.ellipse([cx - 13, cy - 16, cx + 13, cy + 10], fill=(52, 110, 150))
        draw.ellipse([cx - 9, cy - 12, cx - 1, cy - 2], fill=(96, 150, 90))
        draw.ellipse([cx + 3, cy + 1, cx + 11, cy + 9], fill=(96, 150, 90))
        draw.line([(cx - 16, cy + 14), (cx + 16, cy + 14)], fill=INK, width=2)
        draw.line([(cx - 10, cy + 14), (cx - 10, cy + 20)], fill=INK, width=2)
        draw.line([(cx + 10, cy + 14), (cx + 10, cy + 20)], fill=INK, width=2)
    elif kind == "euro":  # EU tax: a coin with a euro mark
        draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(198, 152, 52))
        draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=(120, 88, 20), width=2)
        draw.text((cx - 8, cy - 11), "€", font=sans_b(20), fill=(90, 62, 10))
    elif kind == "cross":  # Bolsonaro: hospital cross
        draw.rectangle([cx - 5, cy - 14, cx + 5, cy + 14], fill=(178, 40, 40))
        draw.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=(178, 40, 40))
    elif kind == "siren":  # Sinaloa: flashing light bars
        draw.rectangle([cx - 16, cy - 8, cx - 2, cy + 8], fill=(30, 60, 160))
        draw.rectangle([cx + 2, cy - 8, cx + 16, cy + 8], fill=(178, 40, 40))
        draw.line([(cx - 16, cy + 14), (cx + 16, cy + 14)], fill=INK, width=2)
        draw.line([(cx, cy - 14), (cx, cy - 8)], fill=INK, width=2)
    elif kind == "bars":  # Rikers: prison bars
        for bx in range(cx - 16, cx + 17, 8):
            draw.line([(bx, cy - 16), (bx, cy + 16)], fill=INK, width=3)
        draw.line([(cx - 18, cy - 16), (cx + 18, cy - 16)], fill=INK, width=3)
        draw.line([(cx - 18, cy + 16), (cx + 18, cy + 16)], fill=INK, width=3)
    elif kind == "bat":  # Wellington Test: bat and ball
        draw.line([(cx - 12, cy + 14), (cx + 8, cy - 14)], fill=(150, 100, 40), width=5)
        draw.ellipse([cx + 6, cy - 18, cx + 16, cy - 8], fill=(178, 40, 40))
        draw.ellipse([cx - 14, cy + 10, cx - 6, cy + 18], fill=(255, 255, 255))
    elif kind == "bridge":  # Nitish Setu: a bridge over a river
        draw.line([(cx - 18, cy + 6), (cx + 18, cy + 6)], fill=INK, width=3)
        draw.arc([cx - 18, cy - 8, cx - 2, cy + 8], start=180, end=360, fill=INK, width=2)
        draw.arc([cx + 2, cy - 8, cx + 18, cy + 8], start=180, end=360, fill=INK, width=2)
        draw.line([(cx - 18, cy + 12), (cx + 18, cy + 12)], fill=(52, 110, 150), width=3)
        draw.line([(cx - 18, cy + 16), (cx + 18, cy + 16)], fill=(52, 110, 150), width=2)
    elif kind == "gavel":  # Roundup: a judge's gavel
        draw.line([(cx - 12, cy + 12), (cx + 12, cy - 12)], fill=(120, 80, 40), width=4)
        draw.rectangle([cx - 2, cy - 16, cx + 16, cy - 6], fill=(90, 58, 26))
        draw.line([(cx - 14, cy + 16), (cx + 14, cy + 16)], fill=INK, width=2)
    elif kind == "flag":  # Rutte to Warsaw: a compass star
        draw.polygon([(cx, cy - 15), (cx + 4, cy - 4), (cx + 15, cy), (cx + 4, cy + 4),
                      (cx, cy + 15), (cx - 4, cy + 4), (cx - 15, cy), (cx - 4, cy - 4)],
                     fill=(29, 63, 110))
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))


# --- dot-matrix world map ----------------------------------------------
# Continents as flat ellipses in lon/lat space; dots are sampled on a
# fixed grid and kept when they fall inside any ellipse.

CONTINENTS = [
    (-100, 48, 32, 18), (-150, 62, 18, 10), (-90, 15, 10, 6),   # N America
    (-42, 73, 10, 7),                                            # Greenland
    (-60, -15, 13, 20),                                          # S America
    (12, 52, 16, 10), (18, 63, 8, 7), (0, 54, 3, 4),            # Europe + UK
    (18, 5, 18, 26), (47, -19, 3, 6),                           # Africa + Madag.
    (80, 50, 45, 20), (78, 21, 8, 9), (102, 12, 10, 8),         # Asia
    (115, -3, 14, 5), (138, 37, 4, 8), (45, 24, 9, 8),          # SE Asia, Japan
    (134, -25, 14, 8), (172, -41, 3, 5),                         # Australia + NZ
]


def on_land(lon, lat):
    for cx, cy, rx, ry in CONTINENTS:
        if ((lon - cx) / rx) ** 2 + ((lat - cy) / ry) ** 2 <= 1.0:
            return True
    return False


# story number -> (lon, lat, label, label side, label dy)
# dy values were hand-placed so no two labels touch; Wellington's label
# sits to the LEFT of its pin so it never clips at the right edge.
PINS = {
    1: (50.6, 26.2, "BAHRAIN", "R", 8),
    2: (56.3, 26.2, "OMAN", "R", -12),
    3: (27.5, 60.0, "GULF OF FINLAND", "L", -20),
    4: (30.7, 36.9, "ANTALYA", "R", 10),
    5: (4.4, 50.8, "BRUSSELS", "L", -6),
    6: (-47.9, -15.8, "BRASILIA", "R", 8),
    7: (-107.4, 24.8, "SINALOA", "R", 8),
    8: (-74.0, 40.7, "NEW YORK", "R", -12),
    9: (174.8, -41.3, "WELLINGTON", "L", 0),
    10: (85.1, 25.6, "PATNA", "R", -12),
    11: (-92.5, 38.5, "MISSOURI", "L", -12),
    12: (21.0, 52.2, "WARSAW", "R", 8),
}


def draw_map(draw, x, y, w, h):
    """Dot-matrix world map with numbered pins; labels never clip."""
    import math

    lon0, lon1, lat0, lat1 = -180.0, 180.0, 72.0, -55.0

    def px(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w,
                y + (lat0 - lat) / (lat0 - lat1) * h)

    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    step = 6
    gx = x + 4
    while gx < x + w - 2:
        gy = y + 4
        while gy < y + h - 2:
            lon = lon0 + (gx - x) / w * (lon1 - lon0)
            lat = lat0 - (gy - y) / h * (lat0 - lat1)
            if on_land(lon, lat):
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(88, 84, 74))
            gy += step
        gx += step
    # graticule: equator and tropics, faint
    for lat, lab in [(0, "EQUATOR"), (23.4, ""), (-23.4, "")]:
        _, ey = px(0, lat)
        draw.line([(x, ey), (x + w, ey)], fill=(200, 194, 178), width=1)
    pin_f = sans_b(8)
    lab_f = sans_b(8)
    for num in range(1, 13):
        lon, lat, label, side, dy = PINS[num]
        px0, py0 = px(lon, lat)
        draw.ellipse([px0 - 7, py0 - 7, px0 + 7, py0 + 7], fill=RED)
        draw.ellipse([px0 - 7, py0 - 7, px0 + 7, py0 + 7], outline=(255, 255, 255), width=1)
        tw = text_w(draw, str(num), pin_f)
        draw.text((px0 - tw / 2, py0 - 6), str(num), font=pin_f, fill=(255, 255, 255))
        lw = text_w(draw, label, lab_f)
        if side == "R":
            lx = min(px0 + 10, x + w - lw - 2)
            lx = max(lx, x + 2)
        else:
            lx = max(px0 - 10 - lw, x + 2)
            lx = min(lx, x + w - lw - 2)
        ly = py0 - 5 + dy
        ly = max(612, min(ly, y + h - 11))
        draw.line([(px0, py0), (lx + (0 if side == "R" else lw), ly + 4)],
                  fill=(120, 112, 96), width=1)
        draw.text((lx, ly), label, font=lab_f, fill=INK)


# --- the 48 stories -------------------------------------------------------
# Reused from the verified round-1 list; nothing new is invented here.

HEROES = [
    ("CLAIM", "BAHRAIN · THE GULF", "Iran hits two US bases in Bahrain",
     "Iran's Revolutionary Guards say they hit Sheikh Isa and Juffair "
     "late on Saturday, after US drones entered Iranian airspace. "
     "No one was hurt."),
    ("REPORTED", "OFF OMAN · STRAIT OF HORMUZ", "Two tankers hit off Oman",
     "UKMTO says two tankers were struck by unknown projectiles near "
     "Khasab, one in the engine room, one in the stern. No casualties."),
    ("REPORTED", "GULF OF FINLAND · THE BALTIC",
     "Russian cargo ship ablaze after drone hit",
     "The Sparta II, bound for Kaliningrad, caught fire after two drones "
     "hit it west of Gogland Island. All 16 crew were evacuated safely."),
]

HERO_ART = [hero_bahrain, hero_tankers, hero_sparta]

TIMELINE = [
    ("≈02:00", "India take control in Wellington: 486/4, Pant 128"),
    ("≈06:00", "Sparta II ablaze in the Gulf of Finland"),
    ("≈10:00", "COP31 draft drops fossil-fuel text"),
    ("≈14:00", "EU unveils its Big Tech tax plan"),
    ("≈16:00", "Two tankers struck off Oman"),
    ("≈21:00", "Iran hits US bases in Bahrain"),
]

NUMBERS = [
    ("2", "US bases hit in Bahrain"),
    ("2", "tankers struck off Oman"),
    ("879,000", "AI chips the US approved for China"),
    ("$7.25bn", "Roundup settlement approved"),
    ("11", "killed in Sinaloa cartel violence"),
    ("$120bn", "climate target dropped at COP31"),
    ("10,000", "forest workers insured by Prince William"),
]

BRIEFS = [
    (4, "globe", "REPORTED", "Climate talks deadlocked into overtime",
     "COP31 draft drops all fossil-fuel mentions and a $120bn target; a third draft is due."),
    (5, "euro", "FORECAST", "EU mulls a Big Tech tax to fund budget",
     "Costa unveils a plan cutting €204bn, partly paid by a levy on the biggest digital firms."),
    (6, "cross", "REPORTED", "Bolsonaro taken to intensive care",
     "The jailed ex-president is in ICU with an acute bowel obstruction; he is stable and conscious."),
    (7, "siren", "REPORTED", "Cartel violence kills 11 after kingpin arrest",
     "Eleven died in Sinaloa after troops captured cartel boss Fausto Isidro Meza Flores."),
    (8, "bars", "FORECAST", "Mamdani unveils plan to close Rikers Island",
     "New York's mayor says the notorious jail will close 'once and for all', calling it a blight."),
    (9, "bat", "REPORTED", "India 486/4, lead 118; Pant 128 on day four",
     "Rahul made 136 and Gill 98 in Wellington; Pant then passed 600 with a day-four ton."),
    (10, "bridge", "REPORTED", "Modi opens Nitish Setu bridge",
     "The PM inaugurates the link between Patna and Vaishali in Bihar, named after Nitish Kumar."),
    (11, "gavel", "REPORTED", "Judge approves $7.25bn Roundup deal",
     "A Missouri judge approves Bayer's settlement; payouts of $10,000–$165,000 for lymphoma cases."),
    (12, "flag", "REPORTED", "Rutte flies to Warsaw after Poland strikes",
     "The NATO chief heads to Warsaw after Russian missiles landed in Poland; Tusk calls it a provocation."),
]

REST = [
    "Estonia to shut Russia road crossings from 1 Dec.",
    "Japan GDP shrinks 0.1% annualised in Q3.",
    "US approved 879,000 AI chips for China in six months.",
    "Trump: an Iran deal could last 20 years.",
    "Zelenskyy: Crimea Bridge strikes a \u201cfair response\u201d.",
    "Denmark: Russia plotted to kill US-Ukrainian rapper.",
    "FBI probing apparent hack of its criminal database.",
    "US airlines warned of Al-Qaeda threat.",
    "Third US aircraft carrier arrives in the Middle East.",
    "South Africa votes; ANC fights to keep its cities.",
    "Nepal PM Shah meets Modi on first bilateral visit.",
    "Cyclone Akvan: 14 flights cancelled at Ranchi airport.",
    "Air India extends Jeddah flight suspension to 24 Nov.",
    "Prince William insures 10,000 forest workers.",
    "Hegseth sets fresh limits on US-Canada defence ties.",
    "South Korea: $75,000 bounty for exam-cheating tips.",
    "Iran warns of \u201cfierce response\u201d if its oil convoy is engaged.",
    "Bahrain probes Patriot interceptor crash on Sitra Island.",
    "Iran: Qeshm blasts were US munitions disposal.",
    "COP31 AI pledge fails to win over major US tech firms.",
    "Crude oil futures fall more than 3%.",
    "Australia v England T20 series opens in Melbourne today.",
    "Pat Cummins keeps Australia Test captaincy.",
    "ICMR completes 100 tech transfers, signs 20 licences.",
    "Trafalgar Square tree sets off from Oslo.",
    "Palisades Fire: man convicted of starting the blaze.",
    "Eleven killed as vehicle plunges into river in PoK.",
    "France probes Depardieu over gang-rape claim.",
    "Eisenkot invites Netanyahu's Likud to coalition talks.",
    "Melania Trump seeks more ceasefires before Christmas.",
    "Trump calls Putin a friend; Zelenskyy calls him a \u201ckiller\u201d.",
    "EU and Indonesia sign free-trade deal after a decade.",
    "Japan's pilotless air taxi completes passenger flight.",
    "US Forest Service releases 1982 Bigfoot probe files.",
    "Boy, 11, writes to NASA with a plan to save Hubble.",
    "Anthropic shares fall a day after blockbuster IPO.",
]


def fit_line(draw, text, fnt, max_w):
    """Shorten one line with an ellipsis until it fits max_w."""
    if text_w(draw, text, fnt) <= max_w:
        return text
    while text and text_w(draw, text + "…", fnt) > max_w:
        text = text[:-1].rstrip()
    return text + "…"


def section_head(draw, x, y, title, right=""):
    """Small red-bar section title with an optional right-aligned note."""
    draw.rectangle([x, y + 1, x + 5, y + 13], fill=RED)
    draw.text((x + 10, y), title, font=sans_b(12), fill=INK)
    if right:
        rw = text_w(draw, right, sans(10))
        draw.text((x + CW - rw, y + 1), right, font=sans(10), fill=SOFT)
    return y + 18


def masthead(draw):
    title = "THE WORLD IN ONE PICTURE"
    size = 44
    fnt = serif_b(size)
    while text_w(draw, title, fnt) > CW and size > 30:
        size -= 1
        fnt = serif_b(size)
    tw = text_w(draw, title, fnt)
    draw.text(((W - tw) / 2, 4), title, font=fnt, fill=INK)
    draw.text((MARGIN, 50), "SUNDAY, 22 NOVEMBER 2026", font=sans_b(11), fill=INK)
    right = "48 STORIES · ONE DAY · EVERY CONTINENT"
    rw = text_w(draw, right, sans_b(11))
    draw.text((W - MARGIN - rw, 50), right, font=sans_b(11), fill=RED)
    rule(draw, MARGIN, 66, W - MARGIN, width=2)


def heroes(draw):
    y0, ph, pw = 72, 214, 318
    for i, (tag, kicker, head, body) in enumerate(HEROES):
        x = MARGIN + i * (pw + 11)
        draw.rectangle([x, y0, x + pw, y0 + ph], fill=PANEL, outline=RULE, width=1)
        HERO_ART[i](draw, x + 1, y0 + 1, pw - 2, 112)
        tx = x + 10
        num = str(i + 1)
        draw.ellipse([tx, y0 + 118, tx + 16, y0 + 134], fill=RED)
        nw = text_w(draw, num, sans_b(10))
        draw.text((tx + (16 - nw) / 2, y0 + 120), num, font=sans_b(10), fill=(255, 255, 255))
        draw.text((tx + 21, y0 + 119), kicker, font=sans_b(9), fill=RED)
        hl = wrap(draw, head, serif_b(16), pw - 20)
        hy = y0 + 134
        draw_lines(draw, hl[:2], tx, hy, serif_b(16), leading=1)
        # Body starts right under the headline and runs to 3 lines when
        # the headline took one line, 2 when it took two.
        by = hy + 18 * len(hl[:2]) + 4
        room = (y0 + ph - 18 - by) // 13
        bl = wrap(draw, body, sans(11), pw - 20)
        draw_lines(draw, bl[:max(1, room)], tx, by, sans(11), leading=1)
        tag_chip(draw, tx, y0 + ph - 17, tag)


def timeline(draw):
    y0 = 292
    section_head(draw, MARGIN, y0, "THE DAY IN UTC", "times approximate · UTC")
    ly = y0 + 34
    rule(draw, MARGIN, ly, W - MARGIN, width=1, fill=SOFT)
    cell = CW / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = MARGIN + cell * (i + 0.5)
        draw.ellipse([cx - 4, ly - 4, cx + 4, ly + 4], fill=RED)
        tw = text_w(draw, when, sans_b(11))
        draw.text((cx - tw / 2, ly - 17), when, font=sans_b(11), fill=INK)
        lines = wrap(draw, what, sans(9), cell - 12)
        lh = draw_lines(draw, lines[:2], cx - (cell - 12) / 2, ly + 7, sans(9),
                        fill=SOFT, leading=0)
        _ = lh


def numbers(draw):
    y0 = 356
    section_head(draw, MARGIN, y0, "BY THE NUMBERS")
    cell = CW / len(NUMBERS)
    top = y0 + 20
    for i, (val, lab) in enumerate(NUMBERS):
        cx = MARGIN + cell * (i + 0.5)
        vw = text_w(draw, val, serif_b(19))
        draw.text((cx - vw / 2, top), val, font=serif_b(19), fill=RED)
        lines = wrap(draw, lab, sans(9), cell - 8)
        total = len(lines[:2]) * 11
        draw_lines(draw, lines[:2], cx - (cell - 8) / 2, top + 23, sans(9),
                   fill=SOFT, leading=0)
        _ = total
        if i:
            draw.line([(MARGIN + cell * i, top + 2), (MARGIN + cell * i, top + 40)],
                      fill=FAINT, width=1)


def briefs(draw):
    y0 = 420
    section_head(draw, MARGIN, y0, "THE DAY IN BRIEF", "stories 4–12")
    pw, ph, gap = 318, 56, 11
    for idx, (num, kind, tag, head, body) in enumerate(BRIEFS):
        r, c = divmod(idx, 3)
        x = MARGIN + c * (pw + gap)
        y = 438 + r * (ph + 4)
        thumb(draw, x, y + 4, kind)
        tx = x + 56
        chip_w = text_w(draw, tag, sans_b(8)) + 10
        tag_chip(draw, x + pw - chip_w, y + 4, tag)
        hl = wrap(draw, f"{num}. {head}", sans_b(11), pw - 56 - chip_w - 6)
        draw_lines(draw, hl[:2], tx, y + 3, sans_b(11), leading=1)
        bl = wrap(draw, body, sans(10), pw - 56)
        draw_lines(draw, [fit_line(draw, l, sans(10), pw - 56) for l in bl[:2]],
                   tx, y + 31, sans(10), fill=SOFT, leading=1)


def rest_list(draw):
    y0 = 760
    section_head(draw, MARGIN, y0, "THE REST OF THE DAY — 36 MORE STORIES",
                 "stories 13–48")
    col_w = (CW - 16) // 2
    fnt = sans(10)
    row_h = 10.3
    for i, item in enumerate(REST):
        col, row = divmod(i, 18)
        x = MARGIN + col * (col_w + 16)
        y = 778 + row * row_h
        label = f"{13 + i}. {item}"
        draw.text((x, y), fit_line(draw, label, fnt, col_w), font=fnt, fill=INK)


def footer(draw):
    y0 = 967
    rule(draw, MARGIN, y0, W - MARGIN, width=2)
    y = y0 + 6
    head = "DATE CHECK — LEFT OUT ON PURPOSE: "
    draw.text((MARGIN, y), head, font=sans_b(9), fill=RED)
    hw = text_w(draw, head, sans_b(9))
    note = ("the Peru M6.9 quake (20 Nov local, 21 Nov 00:09 UTC) is not a 22 Nov story. "
            "Japan's GDP fall and Estonia's border closure are older announcements, "
            "shown as live follow-ups, not as events of the 22nd.")
    lines = wrap(draw, note, sans(9), CW - hw)
    draw.text((MARGIN + hw, y), lines[0], font=sans(9), fill=INK)
    if len(lines) > 1:
        draw.text((MARGIN, y + 11), lines[1], font=sans(9), fill=INK)
    y += 24
    legend = ("CERTAINTY:  REPORTED = confirmed by officials or wires  ·  "
              "CLAIM = one side's account  ·  FORECAST = a plan or proposal, not yet fact")
    draw.text((MARGIN, y), legend, font=sans(9), fill=SOFT)
    y += 12
    src = "SOURCES: Reuters · Fars · UKMTO · AP · AFP · Cricinfo · Times of India · The Daily Jagran · Yle"
    draw.text((MARGIN, y), src, font=sans(9), fill=SOFT)


def render(path):
    """Build the whole front page and save it as a PNG."""
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    heroes(draw)
    timeline(draw)
    numbers(draw)
    briefs(draw)
    section_head(draw, MARGIN, 618, "WHERE IT HAPPENED", "stories 1–12")
    draw_map(draw, MARGIN, 634, CW, 122)
    rest_list(draw)
    footer(draw)
    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import os

    render(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))

#!/usr/bin/env python3
"""Render the 22 November 2026 front page: 48 stories, one 1024x1024 PNG.

Everything here is drawn with Pillow only. No network, no clock, no
external assets: the picture is fully deterministic, so running this
script twice produces byte-identical output.

Layout, top to bottom (my own grid):
  masthead -> ticker -> two lead cards -> ten brief cards (2 cols x 5)
  -> "by the numbers" strip -> stylised world map with 12 pins
  -> numbered list of the remaining 36 stories -> footer.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
PAGE_W = 1024
PAGE_H = 1024
SIDE = 26                      # side margin
GAP = 6                        # gap between stacked sections
COL_W = (PAGE_W - 2 * SIDE - 12) // 2   # two-column card width: 474

# ---------------------------------------------------------------- palette
PAPER = (251, 247, 238)
NAVY = (16, 38, 66)
NAVY_SOFT = (28, 58, 94)
RED = (178, 39, 30)
RED_SOFT = (196, 64, 52)
GOLD = (201, 154, 43)
GOLD_PALE = (232, 203, 120)
INK = (24, 24, 22)
GREY = (96, 96, 90)
LINE = (178, 168, 148)
CARD = (255, 255, 255)
SEA = (214, 232, 243)
LAND = (233, 214, 172)
LAND_EDGE = (190, 170, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _load(path, size):
    return ImageFont.truetype(path, size)


class Type:
    """Font cache with short, semantic accessors."""

    def __init__(self):
        self._cache = {}

    def get(self, name, size):
        key = (name, size)
        if key not in self._cache:
            self._cache[key] = _load(os.path.join(FONT_DIR, name), size)
        return self._cache[key]

    def serif_b(self, size):
        return self.get("DejaVuSerif-Bold.ttf", size)

    def sans(self, size):
        return self.get("DejaVuSans.ttf", size)

    def sans_b(self, size):
        return self.get("DejaVuSans-Bold.ttf", size)


FONTS = Type()


# ---------------------------------------------------------------- story data
# Each lead: place line, headline, body, credit line.
LEADS = [
    {
        "place": "1  ·  BAHRAIN  —  GULF WAR",
        "headline": "Iran hits two US bases in Bahrain",
        "body": (
            "Iran's Revolutionary Guards say they hit US positions at "
            "Sheikh Isa and Juffair late on Saturday, in response to US "
            "drones entering Iranian airspace. Bahrain says a civilian "
            "industrial site caught fire; no one was hurt."
        ),
        "credit": "Fars / Bahrain govt  ·  Saturday night",
        "accent": NAVY,
    },
    {
        "place": "2  ·  KHASAB, OMAN  —  STRAIT OF HORMUZ",
        "headline": "Two tankers hit off Oman",
        "body": (
            "UK maritime agency UKMTO says two tankers were struck by "
            "unknown projectiles near Khasab on Saturday, one in the "
            "engine room, one in the stern. No casualties. Iran says a "
            "tanker hit a mine; it also claims a US MQ-9 downed."
        ),
        "credit": "UKMTO / Reuters  ·  Saturday",
        "accent": RED,
    },
]

# Each brief: number, place, section, headline, body, icon key.
BRIEFS = [
    {
        "num": 3, "place": "GULF OF FINLAND", "section": "BALTIC",
        "headline": "Russian cargo ship ablaze after drone hit",
        "body": "The Sparta II, bound for Kaliningrad, caught fire after "
                "two drones hit it. Its 16 crew evacuated safely.",
        "icon": "ship",
    },
    {
        "num": 4, "place": "ANTALYA", "section": "COP31",
        "headline": "Climate talks deadlocked into overtime",
        "body": "Draft drops all fossil-fuel mentions and a $120bn "
                "target. A third draft is due Saturday as talks stall.",
        "icon": "sun",
    },
    {
        "num": 5, "place": "BRUSSELS", "section": "EU BUDGET",
        "headline": "EU mulls a Big Tech tax to fund budget",
        "body": "Costa unveils a plan cutting \u20ac204bn from the budget, "
                "partly paid by a levy on the biggest digital firms.",
        "icon": "flag",
    },
    {
        "num": 6, "place": "BRASILIA", "section": "BRAZIL",
        "headline": "Bolsonaro taken to intensive care",
        "body": "The jailed ex-president is in ICU with an acute bowel "
                "obstruction. He is stable and conscious.",
        "icon": "scales",
    },
    {
        "num": 7, "place": "SINALOA", "section": "MEXICO",
        "headline": "Cartel violence kills 11 after kingpin arrest",
        "body": "Eleven died in Sinaloa after troops captured cartel "
                "boss Fausto Isidro Meza Flores, \u2018El Chapo Isidro\u2019.",
        "icon": "warn",
    },
    {
        "num": 8, "place": "NEW YORK", "section": "RIKERS",
        "headline": "Mamdani unveils plan to close Rikers Island",
        "body": "Mayor Zohran Mamdani says New York will close the "
                "notorious jail \u2018once and for all\u2019, calling it a blight.",
        "icon": "bars",
    },
    {
        "num": 9, "place": "WELLINGTON", "section": "CRICKET",
        "headline": "India 486/4, lead 118; Pant 128 day four",
        "body": "Rahul made 136 and Gill 98 as India took control; Pant "
                "then passed 600 with a day-four ton.",
        "icon": "bat",
    },
    {
        "num": 10, "place": "PATNA", "section": "INDIA",
        "headline": "Modi opens Nitish Setu bridge",
        "body": "The PM inaugurates the Nitish Setu linking Patna and "
                "Vaishali in Bihar, named after Nitish Kumar.",
        "icon": "bridge",
    },
    {
        "num": 11, "place": "ST LOUIS", "section": "BAYER",
        "headline": "Judge approves $7.25bn Roundup deal",
        "body": "A Missouri judge approves Bayer\u2019s Roundup settlement; "
                "payouts of $10,000\u2013$165,000 for lymphoma cases.",
        "icon": "pill",
    },
    {
        "num": 12, "place": "WARSAW", "section": "NATO",
        "headline": "Rutte flies to Warsaw after Poland strikes",
        "body": "The NATO chief heads to Warsaw today after Russian "
                "missiles landed in Poland; Tusk calls it a provocation.",
        "icon": "flag",
    },
]

# Big figures for the strip under the briefs: (figure, caption line 1, 2).
FIGURES = [
    ("2", "US bases hit in", "Bahrain"),
    ("2", "tankers struck off", "Oman"),
    ("16", "crew evacuated,", "Sparta II"),
    ("879,000", "AI chips approved", "for China"),
    ("$7.25bn", "Bayer Roundup", "settlement"),
    ("486/4", "India at stumps,", "day 3"),
    ("14", "flights cancelled at", "Ranchi"),
    ("11", "killed in Sinaloa", "violence"),
]

# The remaining 36 stories, one line each.
REST = [
    "Estonia to shut Russia road crossings from 1 Dec.",
    "Japan GDP shrinks 0.1% annualised in Q3.",
    "US approved 879,000 AI chips for China in six months.",
    "Trump: an Iran deal could last 20 years.",
    "Zelenskyy: Crimea Bridge strikes a \u2018fair response\u2019.",
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
    "Iran warns of \u2018fierce response\u2019 if its oil convoy is engaged.",
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
    "Eisenkot invites Netanyahu\u2019s Likud to coalition talks.",
    "Melania Trump seeks more ceasefires before Christmas.",
    "Trump calls Putin a friend; Zelenskyy calls him a \u2018killer\u2019.",
    "EU and Indonesia sign free-trade deal after a decade.",
    "Japan\u2019s pilotless air taxi completes passenger flight.",
    "US Forest Service releases 1982 Bigfoot probe files.",
    "Boy, 11, writes to NASA with a plan to save Hubble.",
    "Anthropic shares fall a day after blockbuster IPO.",
]

TICKER = [
    "IRAN HITS US BASES",
    "TANKERS HIT OFF OMAN",
    "SPARTA II ABLAZE",
    "COP31 DEADLOCK",
    "BAYER $7.25BN",
]

# Map pins: (story number, label, longitude, latitude, label dx, dy).
# dx/dy move the label away from the pin; a thin leader joins them.
PINS = [
    (1, "Bahrain", 50.5, 26.2, 8, 12),
    (2, "Khasab", 56.2, 26.2, 10, -16),
    (3, "Gulf of Finland", 26.0, 59.5, 12, -20),
    (4, "Antalya", 30.7, 36.9, -52, 10),
    (5, "Brussels", 4.4, 50.8, -58, -4),
    (6, "Brasilia", -47.9, -15.8, 8, 4),
    (7, "Sinaloa", -107.0, 25.0, -62, -2),
    (8, "New York", -74.0, 40.7, 8, -14),
    (9, "Wellington", 174.8, -41.3, -72, -14),
    (10, "Patna", 85.1, 25.6, 8, 10),
    (11, "St Louis", -90.2, 38.6, 8, 10),
    (12, "Warsaw", 21.0, 52.2, -72, -18),
]

# Rough continent outlines in (lon, lat); drawn as flat blobs, not a survey.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-80, 73),
     (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 7), (-60, 5), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -55), (-73, -40),
     (-72, -20), (-77, -12), (-80, -3)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 59), (30, 60), (30, 70), (25, 71),
     (18, 69), (12, 65), (5, 60), (5, 58), (-2, 57), (-5, 50), (-9, 43)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -18),
     (32, -26), (26, -34), (19, -35), (15, -27), (12, -18), (9, -1),
     (9, 4), (-8, 4), (-13, 8)],
    [(30, 70), (40, 68), (55, 68), (70, 72), (90, 75), (110, 77),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 56),
     (158, 52), (142, 50), (140, 40), (130, 35), (127, 40), (122, 38),
     (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (85, 20), (80, 10), (77, 8), (72, 20), (66, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (43, 28), (40, 32), (36, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (132, -32),
     (137, -35), (140, -38), (147, -39), (150, -37), (153, -32),
     (153, -27), (146, -19), (142, -11), (136, -12), (132, -11),
     (126, -14), (122, -17), (118, -20)],
]


# ---------------------------------------------------------------- text tools
def text_w(draw, text, font):
    return draw.textlength(text, font=font)


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if text_w(draw, trial, font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, font, x, y, width, fill, leading):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def shrink_to_fit(draw, text, font_name, size, width, floor=8):
    """Largest font size >= floor that lets `text` fit `width`."""
    while size > floor:
        font = FONTS.get(font_name, size)
        if text_w(draw, text, font) <= width:
            return font
        size -= 1
    return FONTS.get(font_name, floor)


# ---------------------------------------------------------------- little icons
def paint_icon(draw, kind, x, y, s, colour):
    """Draw a tiny pictogram inside the s-by-s box at (x, y)."""
    cx, cy = x + s // 2, y + s // 2
    if kind == "ship":
        draw.polygon([(x + 2, cy + 2), (x + s - 2, cy + 2),
                      (x + s - 6, cy + 8), (x + 6, cy + 8)], fill=colour)
        draw.rectangle([cx - 5, cy - 8, cx + 5, cy + 2], fill=colour)
        draw.line([cx, cy - 8, cx, cy - 13], fill=colour, width=2)
        draw.line([x + 2, cy + 12, x + s - 2, cy + 12], fill=colour, width=2)
    elif kind == "sun":
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=colour)
        for dx, dy in [(0, -11), (0, 11), (-11, 0), (11, 0),
                       (-8, -8), (8, -8), (-8, 8), (8, 8)]:
            draw.line([cx + dx * 0.6, cy + dy * 0.6, cx + dx, cy + dy],
                      fill=colour, width=2)
        draw.line([x + 2, cy + 12, x + s - 2, cy + 12], fill=colour, width=2)
    elif kind == "flag":
        draw.line([x + 5, y + 2, x + 5, y + s - 2], fill=colour, width=2)
        draw.polygon([(x + 5, y + 3), (x + s - 3, y + 7), (x + 5, y + 12)],
                     fill=colour)
    elif kind == "scales":
        draw.line([cx, y + 3, cx, y + s - 4], fill=colour, width=2)
        draw.line([cx - 9, y + 6, cx + 9, y + 6], fill=colour, width=2)
        for sx in (cx - 9, cx + 9):
            draw.line([sx, y + 6, sx, y + 11], fill=colour, width=1)
            draw.polygon([(sx - 5, y + 11), (sx + 5, y + 11), (sx, y + 16)],
                         outline=colour, width=1)
        draw.line([cx - 7, y + s - 3, cx + 7, y + s - 3], fill=colour, width=2)
    elif kind == "warn":
        draw.polygon([(cx, y + 2), (x + s - 2, y + s - 3), (x + 2, y + s - 3)],
                     outline=colour, width=2)
        draw.text((cx - 2, cy - 6), "!", font=FONTS.sans_b(13), fill=colour)
    elif kind == "bars":
        draw.rectangle([x + 3, y + 3, x + s - 3, y + s - 3],
                       outline=colour, width=2)
        for bx in (x + 9, x + 14, x + 19):
            draw.line([bx, y + 3, bx, y + s - 3], fill=colour, width=1)
    elif kind == "bat":
        draw.line([x + 6, y + s - 4, x + s - 6, y + 6], fill=colour, width=4)
        draw.ellipse([x + s - 11, y + 1, x + s - 3, y + 9], fill=RED)
    elif kind == "bridge":
        draw.arc([x + 2, y + 4, x + s - 2, y + 18], 180, 360, fill=colour,
                 width=2)
        draw.line([x + 2, cy + 6, x + s - 2, cy + 6], fill=colour, width=2)
        draw.line([x + 5, cy + 6, x + 5, y + s - 3], fill=colour, width=1)
        draw.line([x + s - 5, cy + 6, x + s - 5, y + s - 3], fill=colour,
                  width=1)
    elif kind == "pill":
        draw.rounded_rectangle([x + 3, cy - 5, x + s - 3, cy + 5], radius=5,
                               outline=colour, width=2)
        draw.line([cx, cy - 5, cx, cy + 5], fill=colour, width=2)
    else:  # fallback dot
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)


# ---------------------------------------------------------------- sections
def paint_masthead(draw, y):
    """Navy masthead band; returns the y below it."""
    h = 80
    draw.rectangle([0, y, PAGE_W, y + h], fill=NAVY)
    draw.rectangle([0, y + h - 4, PAGE_W, y + h], fill=GOLD)
    title = "THE WORLD IN ONE PICTURE"
    draw.text((SIDE, y + 8), title, font=FONTS.serif_b(40), fill=(255, 255, 255))
    draw.text((SIDE, y + 56), "SUNDAY 22 NOVEMBER 2026  ·  48 STORIES",
              font=FONTS.sans_b(15), fill=GOLD_PALE)
    right = FONTS.sans_b(17)
    draw.text((PAGE_W - SIDE - text_w(draw, "make.fun", right), y + 12),
              "make.fun", font=right, fill=GOLD_PALE)
    small = FONTS.sans(11)
    tag = "news-image-20261122"
    draw.text((PAGE_W - SIDE - text_w(draw, tag, small), y + 38),
              tag, font=small, fill=(200, 210, 225))
    return y + h


def paint_ticker(draw, y):
    """One-line red ticker of the day's biggest beats."""
    h = 22
    font = FONTS.sans_b(12)
    x = SIDE
    for i, item in enumerate(TICKER):
        draw.text((x, y + 4), item, font=font, fill=RED)
        x += text_w(draw, item, font) + 10
        if i < len(TICKER) - 1:
            draw.text((x, y + 4), "·", font=font, fill=GOLD)
            x += 14
    draw.line([SIDE, y + h - 1, PAGE_W - SIDE, y + h - 1], fill=LINE, width=1)
    return y + h


def paint_lead(draw, lead, x, y, w, h):
    """One lead card: coloured header, serif headline, body, credit."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, outline=NAVY,
                           width=2, fill=CARD)
    strip_h = 25
    draw.rounded_rectangle([x, y, x + w, y + strip_h], radius=4,
                           fill=lead["accent"])
    draw.rectangle([x, y + strip_h - 6, x + w, y + strip_h],
                   fill=lead["accent"])
    draw.text((x + 10, y + 5), lead["place"], font=FONTS.sans_b(12),
              fill=(255, 255, 255))
    inner = w - 20
    head_font = shrink_to_fit(draw, lead["headline"],
                             "DejaVuSerif-Bold.ttf", 26, inner, floor=20)
    lines = wrap(draw, lead["headline"], head_font, inner)
    hy = y + strip_h + 8
    for line in lines:
        draw.text((x + 10, hy), line, font=head_font, fill=INK)
        hy += 31
    body_font = FONTS.sans(12)
    by = draw_wrapped(draw, lead["body"], body_font, x + 10, hy + 2,
                      inner, (52, 52, 48), 15)
    credit_font = FONTS.sans(10)
    draw.text((x + 10, y + h - 20), lead["credit"], font=credit_font,
              fill=GREY)
    link = "FULL STORY \u2192"
    draw.text((x + w - 10 - text_w(draw, link, credit_font), y + h - 20),
              link, font=credit_font, fill=RED)


def paint_leads(draw, y):
    h = 154
    paint_lead(draw, LEADS[0], SIDE, y, COL_W, h)
    paint_lead(draw, LEADS[1], SIDE + COL_W + 12, y, COL_W, h)
    return y + h


def paint_brief(draw, brief, x, y, w, h):
    """One brief card: icon at left, kicker, headline, two-line body."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, outline=LINE,
                           width=1, fill=CARD)
    icon_x, icon_y, icon_s = x + 8, y + 8, 26
    paint_icon(draw, brief["icon"], icon_x, icon_y, icon_s, RED)
    tx = x + 44
    tw = w - 54
    kicker = "%d  ·  %s  —  %s" % (brief["num"], brief["place"],
                                  brief["section"])
    draw.text((tx, y + 5), kicker, font=FONTS.sans_b(10), fill=RED)
    head = shrink_to_fit(draw, brief["headline"], "DejaVuSerif-Bold.ttf",
                         15, tw)
    draw.text((tx, y + 20), brief["headline"], font=head, fill=INK)
    body_font = FONTS.sans(11)
    lines = wrap(draw, brief["body"], body_font, tw)[:2]
    by = y + 40
    for line in lines:
        draw.text((tx, by), line, font=body_font, fill=(52, 52, 48))
        by += 14


def paint_briefs(draw, y):
    row_h, row_gap = 67, 5
    for row in range(5):
        for col in range(2):
            brief = BRIEFS[row * 2 + col]
            bx = SIDE + col * (COL_W + 12)
            paint_brief(draw, brief, bx, y + row * (row_h + row_gap),
                        COL_W, row_h)
    return y + 5 * row_h + 4 * row_gap


def paint_figures(draw, y):
    """Dark strip of eight big numbers."""
    h = 42
    draw.rectangle([SIDE, y, PAGE_W - SIDE, y + h], fill=NAVY)
    draw.text((SIDE + 8, y + 4), "BY THE", font=FONTS.sans_b(11),
              fill=GOLD_PALE)
    draw.text((SIDE + 8, y + 19), "NUMBERS", font=FONTS.sans_b(11),
              fill=GOLD_PALE)
    cell_w = (PAGE_W - 2 * SIDE - 92) / len(FIGURES)
    num_font = FONTS.sans_b(17)
    cap_font = FONTS.sans(9)
    for i, (num, cap1, cap2) in enumerate(FIGURES):
        cx = SIDE + 92 + i * cell_w
        draw.text((cx, y + 3), num, font=num_font, fill=(255, 255, 255))
        draw.text((cx, y + 22), cap1, font=cap_font, fill=(200, 210, 225))
        draw.text((cx, y + 31), cap2, font=cap_font, fill=(200, 210, 225))
    return y + h


def project(lon, lat, box):
    """Equirectangular projection of (lon, lat) into map box."""
    x0, y0, w, h = box
    x = x0 + (lon + 170.0) / 360.0 * w
    y = y0 + (75.0 - lat) / 130.0 * h
    return x, y


def paint_map(draw, y):
    """Stylised world map with numbered pins and offset labels."""
    h = 92
    box = (SIDE, y, PAGE_W - 2 * SIDE, h)
    draw.rectangle([SIDE, y, PAGE_W - SIDE, y + h], fill=SEA,
                   outline=NAVY, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    label_font = FONTS.sans_b(10)
    draw.text((SIDE + 6, y + 3), "WHERE IT HAPPENED  —  stories 1–12",
              font=FONTS.sans_b(10), fill=NAVY)
    for num, label, lon, lat, dx, dy in PINS:
        px, py = project(lon, lat, box)
        lx, ly = px + dx, py + dy
        draw.line([px, py, lx + 4, ly + 4], fill=NAVY, width=1)
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        num_font = FONTS.sans_b(9)
        nw = text_w(draw, str(num), num_font)
        draw.text((px - nw / 2, py - 6), str(num), font=num_font,
                  fill=(255, 255, 255))
        draw.text((lx, ly), label, font=label_font, fill=NAVY)
    return y + h


def paint_list(draw, y, bottom):
    """The remaining 36 stories in two columns of 18."""
    head_font = FONTS.sans_b(13)
    draw.text((SIDE, y), "THE REST OF THE DAY  —  36 MORE STORIES",
              font=head_font, fill=RED)
    draw.line([SIDE, y + 18, PAGE_W - SIDE, y + 18], fill=RED, width=2)
    top = y + 24
    rows = 18
    row_h = (bottom - top) / rows
    col_gap = 20
    col_w = (PAGE_W - 2 * SIDE - col_gap) // 2
    for col in range(2):
        for row in range(rows):
            idx = col * rows + row
            item = "%d. %s" % (13 + idx, REST[idx])
            font = shrink_to_fit(draw, item, "DejaVuSans.ttf", 10, col_w)
            iy = top + row * row_h + (row_h - 11) / 2
            draw.text((SIDE + col * (col_w + col_gap), iy), item, font=font,
                      fill=INK)
    return bottom


def paint_footer(draw, y):
    draw.rectangle([0, y, PAGE_W, PAGE_H], fill=NAVY)
    font = FONTS.sans(10)
    draw.text((SIDE, y + 4),
              "Sources: Reuters, AP, Fars, UKMTO, AFP, BBC, Cricinfo, TOI  ·  "
              "All 48 stories first reported 21–22 Nov 2026",
              font=font, fill=(200, 210, 225))
    tag = "make.fun  ·  news-image-20261122"
    draw.text((PAGE_W - SIDE - text_w(draw, tag, font), y + 4), tag,
              font=font, fill=GOLD_PALE)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 0
    y = paint_masthead(draw, y)
    y = paint_ticker(draw, y + GAP)
    y = paint_leads(draw, y + GAP)
    y = paint_briefs(draw, y + GAP)
    y = paint_figures(draw, y + GAP)
    y = paint_map(draw, y + GAP)
    y = paint_list(draw, y + 5, PAGE_H - 16)
    paint_footer(draw, PAGE_H - 16)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()

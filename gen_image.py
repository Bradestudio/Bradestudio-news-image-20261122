#!/usr/bin/env python3
"""Sunday 22 November 2026 -- the day in world news, one image.

Renders entry.png (1024x1024): a broadsheet front page with a navy
masthead, a gold time ticker, two lead stories, ten illustrated
briefs, a BY THE NUMBERS strip, a world map with numbered pins for
stories 1-12, and a numbered list of 36 more stories. 48 verified
stories in total, all first reported on 22 November 2026 (or late
on 21 November, carrying into the 22nd).

Pillow only, no network, no clock: two runs write byte-identical
files. Run:  python3 gen_image.py [output-path]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (12, 28, 56)
NAVY2 = (18, 44, 84)
GOLD = (214, 158, 58)
GOLD_SOFT = (240, 214, 150)
PAPER = (252, 251, 245)
INK = (22, 22, 22)
GREY = (98, 98, 96)
RED = (176, 30, 42)
LINE = (30, 30, 30)
SEA = (206, 228, 236)
LAND = (231, 211, 172)
LAND_LINE = (172, 148, 104)
STEEL = (64, 104, 156)
TEAL = (14, 112, 104)
ORANGE = (208, 104, 28)
CRIMSON = (176, 30, 42)
CREAM = (244, 238, 222)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)
MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)


def wrap(text, fnt, width, d):
    """Greedy word wrap; returns lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text(d, xy, text, fnt, fill=INK, anchor="la", spacing=2):
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor, spacing=spacing)


def para(d, x, y, width, text, fnt, fill=INK, leading=None, max_lines=None):
    """Draw a wrapped paragraph; return the y just below it."""
    if leading is None:
        leading = fnt.size + 3
    lines = wrap(text, fnt, width, d)
    if max_lines is not None:
        assert len(lines) <= max_lines, f"para overflow: {len(lines)} > {max_lines}: {text[:60]}"
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(d, x, y, width, text, fnt, leading=None, max_lines=3):
    if leading is None:
        leading = fnt.size + 2
    lines = wrap(text, fnt, width, d)
    assert len(lines) <= max_lines, f"headline overflow: {text[:60]} ({len(lines)} lines)"
    for line in lines:
        d.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def kicker(d, x, y, text, color=RED, size=13):
    d.text((x, y), text, font=SANS_B(size), fill=color)
    return y + size + 4


def rule(d, x0, y, x1, width=2, fill=LINE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
LEADS = [
    {
        "no": 1, "place": "BAHRAIN", "tag": "GULF WAR",
        "head": "Iran hits two US bases in Bahrain",
        "body": "Iran's Revolutionary Guards say they hit US positions "
                "at Sheikh Isa and Juffair late on Saturday, in response "
                "to US drones entering Iranian airspace. Bahrain says a "
                "civilian industrial site caught fire; no one was hurt.",
        "src": "Fars / Bahrain govt  \u00b7  Saturday night",
    },
    {
        "no": 2, "place": "KHASAB, OMAN", "tag": "STRAIT OF HORMUZ",
        "head": "Two tankers hit off Oman",
        "body": "UK maritime agency UKMTO says two tankers were struck "
                "by unknown projectiles near Khasab on Saturday, one in "
                "the engine room, one in the stern. No casualties. Iran "
                "says a tanker hit a mine; it also claims a US MQ-9 downed.",
        "src": "UKMTO / Reuters  \u00b7  Saturday",
    },
]

BRIEFS = [
    {"no": 3, "place": "GULF OF FINLAND", "tag": "BALTIC",
     "head": "Russian cargo ship ablaze after drone hit",
     "body": "The Sparta II, bound for Kaliningrad, caught fire after "
             "two drones hit it. Its 16 crew evacuated safely.",
     "art": "storm"},
    {"no": 4, "place": "ANTALYA", "tag": "COP31",
     "head": "Climate talks deadlocked into overtime",
     "body": "Draft drops all fossil-fuel mentions and a $120bn target. "
             "A third draft is due Saturday as talks stall.",
     "art": "sun"},
    {"no": 5, "place": "BRUSSELS", "tag": "EU BUDGET",
     "head": "EU mulls a Big Tech tax to fund budget",
     "body": "Costa unveils a plan cutting \u20ac204bn from the budget, "
             "partly paid by a levy on the biggest digital firms.",
     "art": "flags"},
    {"no": 6, "place": "BRASILIA", "tag": "BRAZIL",
     "head": "Bolsonaro taken to intensive care",
     "body": "The jailed ex-president is in ICU with an acute bowel "
             "obstruction. He is stable and conscious.",
     "art": "scales"},
    {"no": 7, "place": "SINALOA", "tag": "MEXICO",
     "head": "Cartel violence kills 11 after kingpin arrest",
     "body": "Eleven died in Sinaloa after troops captured cartel boss "
             "Fausto Isidro Meza Flores, 'El Chapo Isidro'.",
     "art": "dc"},
    {"no": 8, "place": "NEW YORK", "tag": "RIKERS",
     "head": "Mamdani unveils plan to close Rikers Island",
     "body": "Mayor Zohran Mamdani says New York will close the "
             "notorious jail 'once and for all', calling it a blight.",
     "art": "dc"},
    {"no": 9, "place": "WELLINGTON", "tag": "CRICKET",
     "head": "India 486/4, lead 118; Pant 128 day four",
     "body": "Rahul made 136 and Gill 98 as India took control; Pant "
             "then passed 600 with a day-four ton.",
     "art": "bat"},
    {"no": 10, "place": "PATNA", "tag": "INDIA",
     "head": "Modi opens Nitish Setu bridge",
     "body": "The PM inaugurates the Nitish Setu linking Patna and "
             "Vaishali in Bihar, named after Nitish Kumar.",
     "art": "globe"},
    {"no": 11, "place": "ST LOUIS", "tag": "BAYER",
     "head": "Judge approves $7.25bn Roundup deal",
     "body": "A Missouri judge approves Bayer's Roundup settlement; "
             "payouts of $10,000-$165,000 for lymphoma cases.",
     "art": "rupee"},
    {"no": 12, "place": "WARSAW", "tag": "NATO",
     "head": "Rutte flies to Warsaw after Poland strikes",
     "body": "The NATO chief heads to Warsaw today after Russian "
             "missiles landed in Poland; Tusk calls it a provocation.",
     "art": "flags"},
]

NUMBERS = [
    ("2", "US bases hit in Bahrain"),
    ("2", "tankers struck off Oman"),
    ("16", "crew evacuated, Sparta II"),
    ("879,000", "AI chips approved for China"),
    ("$7.25bn", "Bayer Roundup settlement"),
    ("486/4", "India at stumps, day 3"),
    ("14", "flights cancelled at Ranchi"),
    ("11", "killed in Sinaloa violence"),
]

MORE = [
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
    "Eisenkot invites Netanyahu's Likud to coalition talks.",
    "Melania Trump seeks more ceasefires before Christmas.",
    "Trump calls Putin a friend; Zelenskyy calls him a \u2018killer\u2019.",
    "EU and Indonesia sign free-trade deal after a decade.",
    "Japan's pilotless air taxi completes passenger flight.",
    "US Forest Service releases 1982 Bigfoot probe files.",
    "Boy, 11, writes to NASA with a plan to save Hubble.",
    "Anthropic shares fall a day after blockbuster IPO.",
]

# Map pins: (story no, label, lon, lat) -- equirectangular, nudged apart
PINS = [
    (1, "Bahrain", 50.6, 26.2),
    (2, "Khasab", 56.2, 26.2),
    (3, "Gulf of Finland", 24.0, 59.8),
    (4, "Antalya", 30.7, 36.9),
    (5, "Brussels", 4.4, 50.8),
    (6, "Brasilia", -47.9, -15.8),
    (7, "Sinaloa", -107.4, 24.8),
    (8, "New York", -74.0, 40.7),
    (9, "Wellington", 174.8, -41.3),
    (10, "Patna", 85.1, 25.6),
    (11, "St Louis", -90.2, 38.6),
    (12, "Warsaw", 21.0, 52.2),
]

# ---------------------------------------------------------------- pictograms
def pictogram(d, kind, x, y, s, ink=STEEL, accent=RED):
    """Small line-art picture for a brief card, drawn in a s x s box."""
    if kind == "storm":
        d.ellipse([x + s * 0.15, y + s * 0.12, x + s * 0.85, y + s * 0.62], outline=ink, width=3)
        d.ellipse([x + s * 0.32, y + s * 0.28, x + s * 0.68, y + s * 0.58], outline=accent, width=3)
        for i, yy in enumerate([0.68, 0.78, 0.88]):
            d.line([(x + s * (0.15 + 0.1 * i), y + s * yy), (x + s * (0.85 - 0.1 * i), y + s * yy)],
                   fill=ink, width=3)
    elif kind == "chart":
        d.line([(x + s * 0.1, y + s * 0.85), (x + s * 0.9, y + s * 0.85)], fill=ink, width=3)
        d.line([(x + s * 0.1, y + s * 0.85), (x + s * 0.1, y + s * 0.15)], fill=ink, width=3)
        pts = [(0.18, 0.55), (0.38, 0.4), (0.55, 0.55), (0.72, 0.25), (0.88, 0.35)]
        xy = [(x + s * px, y + s * py) for px, py in pts]
        d.line(xy, fill=accent, width=4)
        d.ellipse([xy[-1][0] - 4, xy[-1][1] - 4, xy[-1][0] + 4, xy[-1][1] + 4], fill=accent)
    elif kind == "chip":
        d.rectangle([x + s * 0.25, y + s * 0.25, x + s * 0.75, y + s * 0.75], outline=ink, width=3)
        d.rectangle([x + s * 0.4, y + s * 0.4, x + s * 0.6, y + s * 0.6], fill=accent)
        for t in (0.32, 0.5, 0.68):
            d.line([(x + s * t, y + s * 0.08), (x + s * t, y + s * 0.25)], fill=ink, width=3)
            d.line([(x + s * t, y + s * 0.75), (x + s * t, y + s * 0.92)], fill=ink, width=3)
            d.line([(x + s * 0.08, y + s * t), (x + s * 0.25, y + s * t)], fill=ink, width=3)
            d.line([(x + s * 0.75, y + s * t), (x + s * 0.92, y + s * t)], fill=ink, width=3)
    elif kind == "dc":
        d.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.85, y + s * 0.35),
                   (x + s * 0.15, y + s * 0.35)], fill=ink)
        d.rectangle([x + s * 0.2, y + s * 0.38, x + s * 0.8, y + s * 0.5], fill=ink)
        for t in (0.28, 0.42, 0.58, 0.72):
            d.rectangle([x + s * t - 3, y + s * 0.55, x + s * t + 3, y + s * 0.88], fill=ink)
        d.line([(x + s * 0.12, y + s * 0.9), (x + s * 0.88, y + s * 0.9)], fill=ink, width=3)
    elif kind == "flags":
        d.line([(x + s * 0.25, y + s * 0.1), (x + s * 0.25, y + s * 0.9)], fill=ink, width=3)
        d.line([(x + s * 0.72, y + s * 0.1), (x + s * 0.72, y + s * 0.9)], fill=ink, width=3)
        d.polygon([(x + s * 0.25, y + s * 0.12), (x + s * 0.62, y + s * 0.22),
                   (x + s * 0.25, y + s * 0.34)], fill=STEEL)
        d.polygon([(x + s * 0.72, y + s * 0.12), (x + s * 0.38, y + s * 0.24),
                   (x + s * 0.72, y + s * 0.36)], fill=accent)
    elif kind == "sun":
        d.ellipse([x + s * 0.3, y + s * 0.3, x + s * 0.7, y + s * 0.7], fill=GOLD)
        for a in range(0, 360, 45):
            import math
            r1, r2 = 0.42, 0.5
            cx, cy = x + s * 0.5, y + s * 0.5
            d.line([(cx + s * r1 * math.cos(math.radians(a)), cy + s * r1 * math.sin(math.radians(a))),
                    (cx + s * r2 * math.cos(math.radians(a)), cy + s * r2 * math.sin(math.radians(a)))],
                   fill=ORANGE, width=3)
        d.rectangle([x + s * 0.1, y + s * 0.82, x + s * 0.9, y + s * 0.9], fill=TEAL)
    elif kind == "scales":
        d.line([(x + s * 0.5, y + s * 0.1), (x + s * 0.5, y + s * 0.85)], fill=ink, width=3)
        d.line([(x + s * 0.18, y + s * 0.28), (x + s * 0.82, y + s * 0.28)], fill=ink, width=3)
        for cx in (0.22, 0.78):
            d.line([(x + s * cx, y + s * 0.28), (x + s * cx, y + s * 0.55)], fill=ink, width=2)
            d.polygon([(x + s * (cx - 0.16), y + s * 0.55), (x + s * (cx + 0.16), y + s * 0.55),
                       (x + s * cx, y + s * 0.78)], outline=accent, width=3)
        d.line([(x + s * 0.32, y + s * 0.88), (x + s * 0.68, y + s * 0.88)], fill=ink, width=3)
    elif kind == "bat":
        d.line([(x + s * 0.3, y + s * 0.85), (x + s * 0.68, y + s * 0.2)], fill=ink, width=6)
        d.rectangle([x + s * 0.62, y + s * 0.08, x + s * 0.78, y + s * 0.26], fill=accent)
        d.ellipse([x + s * 0.14, y + s * 0.62, x + s * 0.34, y + s * 0.82], outline=accent, width=3)
        d.line([(x + s * 0.1, y + s * 0.9), (x + s * 0.9, y + s * 0.9)], fill=TEAL, width=3)
    elif kind == "rupee":
        d.text((x + s * 0.22, y + s * 0.02), "\u20b9", font=SERIF_B(int(s * 0.62)), fill=accent)
        d.line([(x + s * 0.15, y + s * 0.82), (x + s * 0.85, y + s * 0.82)], fill=ink, width=3)
    elif kind == "globe":
        d.ellipse([x + s * 0.1, y + s * 0.1, x + s * 0.9, y + s * 0.9], outline=ink, width=3)
        d.ellipse([x + s * 0.32, y + s * 0.1, x + s * 0.68, y + s * 0.9], outline=ink, width=2)
        d.line([(x + s * 0.1, y + s * 0.5), (x + s * 0.9, y + s * 0.5)], fill=ink, width=2)
        d.arc([x + s * 0.15, y + s * 0.22, x + s * 0.85, y + s * 0.78], 200, 340, fill=TEAL, width=3)
        d.ellipse([x + s * 0.55, y + s * 0.28, x + s * 0.72, y + s * 0.45], fill=TEAL)
    else:
        d.ellipse([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8], outline=ink, width=3)


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=GOLD)
    d.text((24, 8), "THE WORLD IN ONE PICTURE", font=SERIF_B(34), fill=PAPER)
    d.text((24, 48), "SUNDAY 22 NOVEMBER 2026  \u00b7  48 STORIES", font=SANS_B(15), fill=GOLD)
    d.text((W - 24, 12), "make.fun", font=SERIF_B(24), fill=GOLD, anchor="ra")
    d.text((W - 24, 44), "news-image-20261122", font=SANS(13), fill=GOLD_SOFT, anchor="ra")
    d.text((24, 92), "IRAN HITS US BASES  \u00b7  TANKERS HIT OFF OMAN  \u00b7  SPARTA II ABLAZE  \u00b7  COP31 DEADLOCK  \u00b7  BAYER $7.25BN",
           font=MONO_B(12), fill=RED)


def draw_leads(d, y0):
    """Two lead panels side by side; returns y below them."""
    gap, mx = 12, 24
    col_w = (W - 2 * mx - gap) // 2
    top = y0 + 22
    height = 160
    for i, lead in enumerate(LEADS):
        x = mx + i * (col_w + gap)
        d.rectangle([x, top, x + col_w, top + height], outline=LINE, width=2)
        d.rectangle([x, top, x + col_w, top + 24], fill=NAVY if i == 0 else CRIMSON)
        d.text((x + 10, top + 4), f"{lead['no']}  \u00b7  {lead['place']}  \u2014  {lead['tag']}",
               font=SANS_B(13), fill=PAPER)
        yy = top + 34
        yy = headline(d, x + 12, yy, col_w - 24, lead["head"], SERIF_B(24), leading=26, max_lines=1)
        yy = para(d, x + 12, yy + 4, col_w - 24, lead["body"], SANS(13), leading=17, max_lines=4)
        d.text((x + 12, top + height - 18), lead["src"], font=SANS(11), fill=GREY)
        d.text((x + col_w - 12, top + height - 18), "FULL STORY \u2192", font=SANS_B(11), fill=RED, anchor="ra")
    return top + height + 8

# ---------------------------------------------------------------- briefs
def draw_briefs(d, y0):
    """Ten briefs in two columns x five rows; returns y below them."""
    mx, gap = 24, 12
    col_w = (W - 2 * mx - gap) // 2
    row_h, row_gap = 62, 5
    y = y0
    for row in range(5):
        for col in range(2):
            b = BRIEFS[row * 2 + col]
            x = mx + col * (col_w + gap)
            d.rectangle([x, y, x + col_w, y + row_h], outline=(180, 175, 165), width=1)
            d.rectangle([x, y, x + 5, y + row_h], fill=GOLD)
            pictogram(d, b["art"], x + 12, y + 8, 44)
            tx = x + 66
            d.text((tx, y + 4), f"{b['no']}  \u00b7  {b['place']}  \u2014  {b['tag']}",
                   font=SANS_B(11), fill=RED)
            yy = headline(d, tx, y + 18, col_w - 78, b["head"], SERIF_B(14), leading=16, max_lines=1)
            para(d, tx, yy + 1, col_w - 78, b["body"], SANS(11), leading=13, max_lines=2)
        y += row_h + row_gap
    return y - row_gap


def draw_numbers(d, y0):
    """BY THE NUMBERS strip; returns y below it."""
    h = 50
    d.rectangle([24, y0, W - 24, y0 + h], fill=NAVY2)
    d.text((36, y0 + 6), "BY THE", font=SANS_B(12), fill=GOLD)
    d.text((36, y0 + 22), "NUMBERS", font=SANS_B(12), fill=GOLD)
    x = 150
    cell = (W - 24 - 150 - 12) // len(NUMBERS)
    for val, label in NUMBERS:
        d.text((x, y0 + 6), val, font=SERIF_B(17), fill=PAPER)
        lab = wrap(label, SANS(10), cell - 8, d)
        yy = y0 + 28
        for ln in lab[:2]:
            d.text((x, yy), ln, font=SANS(10), fill=GOLD_SOFT)
            yy += 11
        x += cell
    return y0 + h + 6


# ---------------------------------------------------------------- map
# Continents as rough (lon, lat) outlines for the small world map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60), (-60, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-150, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -35),
     (-65, -45), (-70, -54), (-73, -37), (-80, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50), (30, 45), (23, 40),
     (19, 42), (12, 44), (3, 43)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -18), (32, -26), (26, -33), (18, -35),
     (15, -27), (12, -18), (9, 4), (-8, 5), (-13, 9)],
    [(40, 68), (60, 70), (75, 73), (90, 75), (110, 76), (130, 72), (160, 70), (178, 66),
     (170, 60), (162, 56), (158, 52), (142, 50), (140, 40), (135, 35), (130, 33),
     (127, 35), (122, 38), (120, 30), (110, 20), (105, 10), (100, 8), (98, 15),
     (95, 22), (90, 22), (85, 20), (80, 15), (77, 8), (73, 20), (66, 25), (60, 25),
     (55, 28), (50, 30), (48, 30), (44, 30), (40, 36), (36, 36)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -8),
     (130, -3), (135, 0), (130, 5), (120, 5), (110, 0)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (130, -13), (126, -14), (122, -17),
     (118, -20)],
]

# Per-pin style: (pin dx, pin dy, label dx, label dy, label anchor)
# so the crowded Europe pins and the far-right Wellington pin stay readable.
PIN_STYLE = {
    1: (-18, 16, -24, -12, "ra"),
    2: (18, -10, 11, -8, "la"),
    3: (-8, -18, -11, -10, "ra"),
    4: (14, 20, 11, 10, "la"),
    5: (-38, -14, -11, -8, "ra"),
    6: (0, 0, 11, -6, "la"),
    7: (0, 0, 11, -6, "la"),
    8: (0, -12, 11, -6, "la"),
    9: (0, 0, -11, -6, "ra"),
    10: (0, 8, 11, -6, "la"),
    11: (0, 0, 11, -6, "la"),
    12: (0, -16, 11, -10, "la"),
}



def draw_map(d, y0):
    """World map with numbered pins; returns y below it."""
    h = 100
    mx = 24
    d.rectangle([mx, y0, W - mx, y0 + h], fill=SEA, outline=LINE, width=2)
    d.text((mx + 10, y0 + 5), "WHERE IT HAPPENED  \u2014  stories 1\u201312", font=SANS_B(11), fill=NAVY)
    x0, x1 = mx + 8, W - mx - 8
    top, bot = y0 + 20, y0 + h - 4

    def to_xy(lon, lat):
        return (x0 + (lon + 180) / 360.0 * (x1 - x0),
                top + (75 - lat) / 130.0 * (bot - top))

    for poly in CONTINENTS:
        d.polygon([to_xy(lon, lat) for lon, lat in poly], fill=LAND, outline=LAND_LINE)
    placed = []
    for no, label, lon, lat in PINS:
        px, py = to_xy(lon, lat)
        pdx, pdy, ldx, ldy, anchor = PIN_STYLE.get(no, (0, 0, 11, -6, "la"))
        lx, ly = px + pdx, py + pdy
        placed.append((lx, ly))
        if (pdx, pdy) != (0, 0):
            d.line([(px, py), (lx, ly)], fill=GREY, width=1)
        d.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=RED, outline=PAPER, width=2)
        d.text((lx, ly), str(no), font=SANS_B(10), fill=PAPER, anchor="mm")
        d.text((lx + ldx, ly + ldy), label, font=SANS_B(9), fill=NAVY, anchor=anchor)
    return y0 + h + 4


# ---------------------------------------------------------------- list
def draw_more(d, y0):
    """Numbered list 13-48 in three columns, one line each."""
    mx, gap = 24, 10
    col_w = (W - 2 * mx - 2 * gap) // 3
    d.text((mx, y0), "THE REST OF THE DAY  \u2014  36 MORE STORIES", font=SANS_B(13), fill=RED)
    rule(d, mx, y0 + 20, W - mx, width=2)
    y = y0 + 28
    per_col = 12
    for col in range(3):
        x = mx + col * (col_w + gap)
        yy = y
        for i in range(per_col):
            item = MORE[col * per_col + i]
            no = 13 + col * per_col + i
            d.text((x, yy), f"{no}.", font=SANS_B(10), fill=RED)
            lines = wrap(item, SANS(10), col_w - 24, d)
            assert len(lines) == 1, f"list item wraps: {item}"
            d.text((x + 24, yy), lines[0], font=SANS(10), fill=INK)
            yy += 14
    return y + per_col * 14


def render(out_path):
    assert len(MORE) == 36, f"need 36 more stories, have {len(MORE)}"
    assert len(LEADS) + len(BRIEFS) + len(MORE) == 48
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_leads(d, 100)
    y = draw_briefs(d, y + 4)
    y = draw_numbers(d, y + 6)
    y = draw_map(d, y)
    # list occupies the rest; 12 rows in ~150px
    draw_more(d, y)
    d.rectangle([0, H - 22, W, H], fill=NAVY)
    d.text((24, H - 18), "Sources: Reuters, AP, Fars, UKMTO, AFP, BBC, Cricinfo, TOI  \u00b7  All 48 stories first reported 21\u201322 Nov 2026",
           font=SANS(11), fill=GOLD_SOFT)
    d.text((W - 24, H - 18), "make.fun \u00b7 news-image-20261122", font=SANS_B(11), fill=PAPER, anchor="ra")
    img.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print(f"wrote {out}")

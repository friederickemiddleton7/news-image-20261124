#!/usr/bin/env python3
"""news-image-20261124 round-3 generator — front page of 24 November 2026.
Implements the official design brief: palette, header band with the date as the
dominant element, lead story card with pictogram, 2x3 story grid with region
chips + pictograms, and an ALSO TODAY bottom band. Deterministic (no clocks,
no randomness). 1024x1024 RGB PNG, well under 1 MiB. Every text line is
measured and wrapped/shrunk so nothing overflows and nothing is below 19 px.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = '/usr/share/fonts/truetype/dejavu/'

NAVY = (11, 18, 32)
CARD = (21, 31, 51)
HAIR = (42, 58, 87)
BODY = (215, 222, 234)
WHITE = (255, 255, 255)
AMBER = (242, 179, 61)
TEAL = (79, 209, 197)
MUTED = (154, 164, 182)
PANEL = (30, 42, 66)

MINPX = 19  # brief: no text smaller than 19 px


def F(name, size):
    return ImageFont.truetype(FD + name, size)


img = Image.new('RGB', (W, H), NAVY)
d = ImageDraw.Draw(img)


def fit_size(text, name, size, max_w, min_size=MINPX):
    s = size
    while s > min_size and d.textlength(text, font=F(name, s)) > max_w:
        s -= 1
    return s


def wrap_fit(text, name, size, max_w, max_lines, min_size=MINPX):
    """Return (lines, size) with every line <= max_w, at most max_lines,
    font >= min_size. Tries the requested size first, then shrinks."""
    s = size
    while s >= min_size:
        f = F(name, s)
        words, lines, cur = text.split(), [], ''
        ok = True
        for w_ in words:
            t = (cur + ' ' + w_).strip()
            if d.textlength(t, font=f) <= max_w:
                cur = t
            elif cur:
                lines.append(cur)
                cur = w_
                if d.textlength(cur, font=f) > max_w:
                    ok = False
                    break
            else:
                ok = False
                break
        if ok and cur:
            lines.append(cur)
        if ok and len(lines) <= max_lines:
            return lines, s
        s -= 1
    # last resort at min_size: hard-wrap by words, keep only max_lines
    f = F(name, min_size)
    lines, cur = [], ''
    for w_ in text.split():
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines[:max_lines], min_size


def draw_lines(x, y, lines, name, size, fill, lh):
    f = F(name, size)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)


# ---------------- header band ----------------
d.text((48, 22), ' '.join('WORLD NEWS'), font=F('DejaVuSans-Bold.ttf', 26), fill=AMBER)
dsz = fit_size('24 NOVEMBER 2026', 'DejaVuSans-Bold.ttf', 76, W - 96)
d.text((48, 54), '24 NOVEMBER 2026', font=F('DejaVuSans-Bold.ttf', dsz), fill=WHITE)
d.line([(48, 140), (W - 48, 140)], fill=AMBER, width=3)

# ---------------- lead story card ----------------
d.rectangle([40, 148, W - 40, 452], fill=CARD, outline=HAIR, width=1)
d.text((56, 160), 'LIBYA  ·  BENGHAZI', font=F('DejaVuSans-Bold.ttf', 24), fill=AMBER)
ly = 192
for ln in ['UKRAINIAN SEA DRONES', 'SINK A RUSSIAN WARSHIP', 'IN LIBYA']:
    s = fit_size(ln, 'DejaVuSans-Bold.ttf', 46, 620)
    d.text((56, ly), ln, font=F('DejaVuSans-Bold.ttf', s), fill=WHITE)
    ly += 48
by = 344
for t in ['Seven drones hit the corvette Merkury at Benghazi; at least 10 wounded.',
          'The UN wants an independent probe; Tripoli says it will not be dragged into the war.']:
    lines, s = wrap_fit(t, 'DejaVuSans.ttf', 20, 620, 2)
    draw_lines(56, by, lines, 'DejaVuSans.ttf', s, BODY, 25)
    by += 25 * len(lines) + 4

# lead pictogram: tilting hull, three drones with dashed trails, two wave lines
cx, cy = 800, 268
d.polygon([(cx - 118, cy + 6), (cx + 118, cy + 6), (cx + 86, cy + 58), (cx - 86, cy + 58)],
          fill=PANEL, outline=HAIR)
d.polygon([(cx - 118, cy + 6), (cx + 118, cy + 6), (cx + 126, cy - 10), (cx - 126, cy - 10)],
          fill=(38, 52, 80), outline=HAIR)
for sx, sy in [(668, 176), (800, 154), (932, 176)]:
    d.polygon([(sx, sy - 14), (sx - 16, sy + 10), (sx + 16, sy + 10)], fill=AMBER)
    for k in range(1, 7):
        t0 = k / 7
        x0, y0 = sx + (cx - sx) * t0, sy + (cy - sy) * t0
        d.line([(x0, y0), (x0 + 9, y0 + 6)], fill=HAIR, width=2)
for off in (0, 15):
    d.line([(664 + i * 21, cy + 92 + off + (6 if i % 2 else -6)) for i in range(14)],
           fill=TEAL, width=2)

# ---------------- 2x3 story grid ----------------
stories = [
    ('EUROPE · RUSSIA/UKRAINE', 'REFINERIES BURN AFTER PUTIN VOW',
     "Novoshakhtinsk halts, Lukoil's Perm hit; 350,000 lose power.", 'flame_tank'),
    ('EUROPE · BRUSSELS', 'EU READIES 22ND SANCTIONS PACKAGE',
     'Banks, crypto and athletes targeted; NATO sends AWACS to Poland.', 'star_ring'),
    ('GLOBAL · ANTALYA', 'COP31 ENDS WITH NO DEAL',
     'Fossil-fuel wording sank the final text; Pacific states dismayed.', 'thermo_globe'),
    ('AMERICAS · SILICON VALLEY', 'NVIDIA REINSTATES HUANG AS CEO',
     "Shares jump about 30% after Trump's call to the board.", 'arrow_chip'),
    ('ASIA-PACIFIC · AOMORI', 'MAGNITUDE 7.6 QUAKE, TSUNAMI ALERT',
     'Three-metre warning for Hokkaido, Aomori, Iwate; trains halted.', 'seismo_wave'),
    ('SOUTHEAST ASIA · BANTEN', 'FACTORY FIRE KILLS 24 IN INDONESIA',
     'Rescuers hunt about 30 missing in a collapsed candy plant.', 'flame_roof'),
]

CW, CH, GUT, MX = 320, 190, 12, 16


def pictogram(kind, x, y):
    """44 px pictogram from plain shapes; no text, no faces."""
    if kind == 'flame_tank':
        d.rectangle([x, y + 24, x + 42, y + 42], fill=PANEL, outline=HAIR)
        d.polygon([(x + 21, y), (x + 10, y + 20), (x + 32, y + 20)], fill=AMBER)
        d.polygon([(x + 21, y + 7), (x + 15, y + 20), (x + 27, y + 20)], fill=WHITE)
    elif kind == 'star_ring':
        for k in range(8):
            a = k * math.pi / 4
            d.ellipse([x + 21 + 15 * math.cos(a) - 3, y + 21 + 15 * math.sin(a) - 3,
                       x + 21 + 15 * math.cos(a) + 3, y + 21 + 15 * math.sin(a) + 3], fill=TEAL)
        d.line([(x + 3, y + 21), (x + 39, y + 21)], fill=AMBER, width=3)
    elif kind == 'thermo_globe':
        d.ellipse([x + 16, y + 14, x + 44, y + 42], outline=TEAL, width=2)
        d.line([(x + 25, y), (x + 25, y + 28)], fill=AMBER, width=4)
        d.ellipse([x + 21, y + 26, x + 29, y + 34], fill=AMBER)
    elif kind == 'arrow_chip':
        d.rectangle([x + 2, y + 22, x + 28, y + 42], fill=PANEL, outline=HAIR)
        d.line([(x + 6, y + 32), (x + 22, y + 16)], fill=AMBER, width=3)
        d.polygon([(x + 30, y + 6), (x + 17, y + 12), (x + 27, y + 21)], fill=AMBER)
    elif kind == 'seismo_wave':
        d.line([(x, y + 30), (x + 8, y + 10), (x + 16, y + 38), (x + 24, y + 4),
                (x + 32, y + 32), (x + 42, y + 20)], fill=AMBER, width=3)
        d.arc([x, y + 28, x + 42, y + 48], 180, 360, fill=TEAL, width=2)
    elif kind == 'flame_roof':
        d.polygon([(x, y + 22), (x + 21, y + 4), (x + 42, y + 22)], fill=PANEL, outline=HAIR)
        d.rectangle([x + 8, y + 22, x + 34, y + 42], fill=(26, 36, 58), outline=HAIR)
        d.polygon([(x + 21, y + 12), (x + 14, y + 30), (x + 28, y + 30)], fill=AMBER)


for i, (c, head, line, pk) in enumerate(stories):
    col, row = i % 3, i // 3
    x = MX + col * (CW + GUT)
    y = 466 + row * (CH + GUT)
    d.rectangle([x, y, x + CW, y + CH], fill=CARD, outline=HAIR, width=1)
    cs = fit_size(c, 'DejaVuSans-Bold.ttf', 19, CW - 16)
    d.text((x + 8, y + 10), c, font=F('DejaVuSans-Bold.ttf', cs), fill=TEAL)
    hl, hs = wrap_fit(head, 'DejaVuSans-Bold.ttf', 27, CW - 16, 2)
    draw_lines(x + 8, y + 38, hl, 'DejaVuSans-Bold.ttf', hs, WHITE, 30)
    bl, bs = wrap_fit(line, 'DejaVuSans.ttf', 19, CW - 88, 4)
    draw_lines(x + 8, y + 100, bl, 'DejaVuSans.ttf', bs, BODY, 22)
    pictogram(pk, x + CW - 56, y + CH - 56)

# ---------------- bottom band ----------------
d.line([(40, 838), (W - 40, 838)], fill=HAIR, width=1)
d.text((40, 848), 'ALSO TODAY', font=F('DejaVuSans-Bold.ttf', 20), fill=TEAL)
bands = ['Houthi strike in Yemen kills 11 · Israeli strikes kill 3 in Gaza, including a UNRWA worker · armed groups shut two Libyan pipelines, a quarter of output lost',
         'Bomb threats close schools across Germany and Denmark · Kenya picks a US-led group for its $60bn Mrima Hill minerals · El Chapo Isidro captured in Sinaloa']
by = 880
for t in bands:
    lines, s = wrap_fit(t, 'DejaVuSans.ttf', 20, W - 80, 2)
    draw_lines(40, by, lines, 'DejaVuSans.ttf', s, MUTED, 26)
    by += 26 * len(lines) + 6

out = os.environ.get('MAKEFUN_OUTPUT_DIR') or os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
img.save(os.path.join(out, 'entry.png'), 'PNG', optimize=True)
print('wrote entry.png', img.size)

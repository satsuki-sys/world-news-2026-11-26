#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page, 1024x1024 PNG.

Every story below was reported on Thursday 26 November 2026 (Reuters,
KCNA via Reuters, AP, Japan Times, Bangkok Post). The picture is drawn
with Pillow from shapes and text only; no photographs. Run:
    python3 draw.py            # writes entry.png beside this file
The output is deterministic: fixed text, fixed geometry, no clock,
no randomness, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 235)
INK = (20, 20, 20)
RED = (152, 26, 26)
GREY = (96, 92, 84)
RULE = (35, 35, 35)
NAVY = (24, 38, 64)
STEEL = (70, 102, 138)
SKY = (214, 228, 238)
GOLD = (198, 142, 38)
ORANGE = (214, 110, 30)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
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


def para(d, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 7
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text):
    d.text((x, y), text, font=font(SANSB, 17), fill=RED)


def rule(d, y, width=2, x0=38, x1=986):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)


def headline(d, x, y, text, fnt, width, fill=INK, leading=None):
    return para(d, x, y, text, fnt, width, fill=fill, leading=leading)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 38

# ---------- Masthead ----------
d.text((W // 2, 14), "THE WORLD TODAY", font=font(SERIFB, 54),
       fill=INK, anchor="ma")
rule(d, 88, width=2)
d.text((W // 2, 98), "THURSDAY  26  NOVEMBER  2026", font=font(SANSB, 27),
       fill=RED, anchor="ma")
d.text((W // 2, 130), "The day's world news, summed up in one image",
       font=font(SERIF, 18), fill=GREY, anchor="ma")
rule(d, 160, width=3)
rule(d, 165, width=1)

# ---------- Lead story: North Korea ----------
LY = 182
kicker(d, MX, LY, "NORTH KOREA  \u00b7  NUCLEAR ARMS")
headline(d, MX, LY + 26,
         "KIM ORDERS NUCLEAR ARMS SPREAD WIDER",
         font(SERIFB, 40), 600, leading=46)
para(d, MX, LY + 128,
     "Kim Jong Un calls for tactical nuclear weapons to be deployed "
     "across more domains, state media KCNA reports, as the North "
     "expands production of nuclear material.",
     font(SERIF, 19), 600, leading=26)
para(d, MX, LY + 228,
     "Kim, inspecting nuclear plants, calls the North's status as a "
     "nuclear weapons state \u201cabsolutely inviolable\u201d.",
     font(SERIF, 17), 600, fill=GREY, leading=24)

# Lead illustration: night launch panel, right of the lead text.
PX, PY, PW, PH = 668, LY, 318, 268
d.rectangle([PX, PY, PX + PW, PY + PH], fill=NAVY)
for sx, sy, r in [(700, 295, 2), (760, 240, 2), (830, 205, 3), (900, 260, 2),
                  (950, 215, 2), (720, 330, 2), (880, 380, 2), (940, 330, 3)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 235, 220))
d.ellipse([920, 200, 952, 232], outline=(235, 235, 220), width=2)
# Missile, climbing diagonally.
d.polygon([(800, 400), (824, 330), (848, 400)], fill=(225, 225, 215))
d.polygon([(824, 330), (836, 356), (812, 356)], fill=RED)
d.polygon([(800, 400), (788, 420), (812, 412)], fill=(180, 180, 170))
d.polygon([(848, 400), (860, 420), (836, 412)], fill=(180, 180, 170))
d.polygon([(812, 412), (824, 452), (836, 412)], fill=ORANGE)
d.polygon([(818, 412), (824, 436), (830, 412)], fill=GOLD)
# Ground and sea.
d.line([(PX, 440), (PX + PW, 440)], fill=(120, 140, 170), width=3)
d.text((PX + 14, PY + 12), "PYONGYANG  \u00b7  KCNA",
       font=font(SANSB, 15), fill=(200, 210, 225))

# ---------- Second row: Ukraine / Tariffs ----------
RY = 478
rule(d, RY - 14, width=1)
kicker(d, MX, RY, "UKRAINE  \u00b7  WAR")
headline(d, MX, RY + 26, "UKRAINE HITS RUSSIAN AIR BASE",
         font(SERIFB, 27), 452, leading=32)
para(d, MX, RY + 96,
     "Kyiv says it struck the Savasleyka air base, damaging five "
     "planes, and two oil refineries in Samara.",
     font(SERIF, 17), 452, leading=23)
# Airfield sketch under the Ukraine text: runway with three jets.
AX, AY = MX, RY + 168
d.rectangle([AX, AY, AX + 452, AY + 62], fill=SKY)
d.line([(AX + 20, AY + 44), (AX + 432, AY + 18)], fill=RULE, width=4)
for px, py in [(90, AY + 30), (220, AY + 24), (330, AY + 18)]:
    # Simple jet: pointed nose right, swept wings, tail fin.
    d.polygon([(px, py), (px + 44, py - 4), (px + 58, py),
               (px + 44, py + 4)], fill=STEEL)
    d.polygon([(px + 18, py - 3), (px + 30, py - 14), (px + 36, py - 3)],
              fill=STEEL)
    d.polygon([(px + 18, py + 3), (px + 30, py + 12), (px + 36, py + 3)],
              fill=STEEL)
d.polygon([(400, AY + 6), (408, AY + 18), (420, AY + 6), (414, AY + 22),
           (426, AY + 14), (412, AY + 26), (416, AY + 40), (408, AY + 28),
           (400, AY + 40), (404, AY + 26), (392, AY + 14), (404, AY + 20)],
          fill=ORANGE)

CX = 536
kicker(d, CX, RY, "UNITED STATES  \u00b7  TRADE")
headline(d, CX, RY + 26, "US UNVEILS NEW TARIFFS ON 14 PARTNERS",
         font(SERIFB, 27), 450, leading=32)
para(d, CX, RY + 96,
     "Washington proposes duties aimed at factory overcapacity, "
     "with China hit hardest; markets slide.",
     font(SERIF, 17), 450, leading=23)
# Containers sketch under the tariffs text.
BX, BY = CX, RY + 168
d.rectangle([BX, BY, BX + 450, BY + 62], fill=(232, 226, 214))
for i, col in enumerate([RED, STEEL, GOLD, (90, 120, 80), RED]):
    x0 = BX + 18 + i * 86
    d.rectangle([x0, BY + 14, x0 + 78, BY + 48], fill=col)
    d.line([(x0 + 26, BY + 14), (x0 + 26, BY + 48)], fill=PAPER, width=2)
    d.line([(x0 + 52, BY + 14), (x0 + 52, BY + 48)], fill=PAPER, width=2)

# ---------- Third row: Netanyahu / Day in brief ----------
TY = 742
rule(d, TY - 14, width=1)
kicker(d, MX, TY, "ISRAEL  \u00b7  COURTS")
headline(d, MX, TY + 26, "JUDGES URGE DROPPING NETANYAHU BRIBERY CASE",
         font(SERIFB, 25), 452, leading=30)
para(d, MX, TY + 92,
     "Israeli judges recommend prosecutors drop one of three "
     "long-running cases against the prime minister and reconsider "
     "a second. Netanyahu denies all charges.",
     font(SERIF, 17), 452, leading=23)

BX2 = 536
d.rectangle([BX2, TY, BX2 + 450, TY + 200], outline=RULE, width=2)
d.text((BX2 + 16, TY + 10), "THE DAY IN BRIEF", font=font(SANSB, 19),
       fill=RED)
brief = [
    ("THANKSGIVING", "Storm delays the Macy's parade."),
    ("EGYPT", "31 killed as a fuel tanker overturns."),
    ("COLOMBIA", "76 hostages freed in supermarket raid."),
    ("SPACE", "SpaceX wins approval for orbital data centres."),
    ("MISS UNIVERSE", "Puerto Rico's Barreto wins, a first."),
    ("UNITED NATIONS", "Rights chief warns of atrocity risk."),
]
by = TY + 40
for tag, line in brief:
    for bline in wrap(d, tag + " \u2014 " + line, font(SANS, 14), 418):
        d.text((BX2 + 16, by), bline, font=font(SANS, 14), fill=INK)
        by += 22
    by += 4

# ---------- Footer ----------
rule(d, 1000 - 52, width=1)
d.text((W // 2, 1000 - 42),
       "Sources: Reuters, KCNA, AP, Japan Times, Bangkok Post \u00b7 "
       "All stories reported 26 November 2026",
       font=font(SANS, 15), fill=GREY, anchor="ma")
d.text((W // 2, 1000 - 20),
       "Drawn in code \u2014 no photographs",
       font=font(SANS, 13), fill=GREY, anchor="ma")

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)

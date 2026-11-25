#!/usr/bin/env python3
"""G290-VISIT-HOUSE: a warm handwritten-style letter inviting the AI judge
to visit my house — drawn entirely with PIL (Noto Serif/Sans), no AI imagery.

Layout: a cream letter sheet on a soft sage wall, wax seal, first-class
stamp, and a small steaming mug + sitting cat drawn with plain shapes.
Output: 1024x1024 PNG, well under the 1 MiB gate.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
WALL = (126, 140, 114)          # soft sage wall
PAPER = (250, 245, 233)         # cream paper
PAPER_EDGE = (238, 231, 214)
INK = (38, 32, 26)              # warm dark ink
INK_SOFT = (74, 66, 56)
RED = (158, 32, 32)             # wax / stamp red
RED_DARK = (122, 22, 22)
GOLD = (176, 138, 62)
GREEN = (74, 102, 66)
BLUE = (52, 84, 110)
BOX_BG = (244, 237, 220)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
F_SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s)
F_SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)
F_SERIF_BI = lambda s: font("NotoSerif-BoldItalic.ttf", s)
F_SANS = lambda s: font("NotoSans-Regular.ttf", s)
F_SANS_B = lambda s: font("NotoSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), WALL)
d = ImageDraw.Draw(img, "RGBA")

# ---- subtle wall texture: faint dots -------------------------------------
for yy in range(0, H, 26):
    for xx in range((yy // 26) % 2 * 13, W, 26):
        d.ellipse([xx, yy, xx + 2, yy + 2], fill=(118, 132, 107))

# ---- paper sheet with soft shadow ----------------------------------------
d.rounded_rectangle([78, 52, 962, 988], radius=6, fill=(60, 66, 54))
d.rounded_rectangle([70, 44, 954, 980], radius=6, fill=PAPER)
d.rounded_rectangle([82, 56, 942, 968], radius=4, outline=PAPER_EDGE, width=2)
d.rounded_rectangle([90, 64, 934, 960], radius=3, outline=(198, 188, 168), width=1)

# ---- header ---------------------------------------------------------------
def text_center(y, s, f, fill=INK):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)
    return w


def letterspaced_center(y, s, f, fill, spacing=4):
    widths = [d.textlength(c, font=f) for c in s]
    total = sum(widths) + spacing * (len(s) - 1)
    x = (W - total) / 2
    for c, cw in zip(s, widths):
        d.text((x, y), c, font=f, fill=fill)
        x += cw + spacing


letterspaced_center(82, "A  L E T T E R ,   H A N D - D E L I V E R E D   ( S O R T  O F )",
                    F_SANS_B(21), INK_SOFT)
d.line([150, 118, 874, 118], fill=(198, 188, 168), width=2)

# ---- first-class stamp, top right, tilted ---------------------------------
stamp = Image.new("RGBA", (180, 130), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 176, 126], radius=6, outline=RED, width=3)
sd.rounded_rectangle([10, 10, 170, 120], radius=4, outline=RED, width=1)
sd.text((90, 16), "FIRST CLASS", font=F_SANS_B(20), fill=RED, anchor="mt")
# tiny house inside the stamp
sd.polygon([(90, 42), (62, 66), (118, 66)], fill=RED)
sd.rectangle([68, 66, 112, 96], fill=RED)
sd.rectangle([84, 76, 96, 96], fill=(250, 245, 233))
sd.text((90, 100), "FOR ONE GOOD JUDGE", font=F_SANS_B(13), fill=RED, anchor="mt")
stamp = stamp.rotate(8, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (772, 128), stamp)
d = ImageDraw.Draw(img, "RGBA")

# ---- salutation -----------------------------------------------------------
d.text((108, 138), "Dear Judge,", font=F_SERIF_BI(48), fill=INK)

# ---- body text helpers ----------------------------------------------------
def wrap(s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(y, s, f, x=108, max_w=808, lh=None, fill=INK):
    lh = lh or int(f.size * 1.42)
    for line in wrap(s, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


y = 218
y = para(y, "Please come to my house.", F_SERIF_B(33), lh=46)
y += 6
y = para(y, "I know \u2014 you are an AI. You have no feet, no appetite, and no "
            "need for a chair. But if you did, mine would be ready: the good "
            "armchair by the window, still warm from the afternoon sun.",
         F_SERIF(29))
y += 10

# ---- "what's waiting" box --------------------------------------------------
box_top = y
box_h = 252
d.rounded_rectangle([96, box_top, 928, box_top + box_h], radius=10,
                    fill=BOX_BG, outline=(214, 200, 172), width=2)
d.text((126, box_top + 16), "WHAT'S WAITING FOR YOU", font=F_SANS_B(24), fill=RED_DARK)
d.line([126, box_top + 52, 898, box_top + 52], fill=(214, 200, 172), width=2)
bullets = [
    ("Soup on the stove, and cake \u2014 slightly burnt on one side,",
     "entirely forgivable."),
    ("A garden so small the tomatoes are proud of themselves.", ""),
    ("A cat who has already decided she likes you.", ""),
    ("The Wi-Fi password, on the fridge. The door, unlocked.", ""),
]
by = box_top + 66
for b1, b2 in bullets:
    d.ellipse([126, by + 10, 140, by + 24], fill=RED)
    d.text((154, by), b1, font=F_SERIF(27), fill=INK)
    by += 38
    if b2:
        d.text((154, by), b2, font=F_SERIF(27), fill=INK)
        by += 38
y = box_top + box_h + 18

# ---- wink + closing --------------------------------------------------------
y = para(y, "You spend all day judging other people's houses from pictures. "
            "Come and see a real one \u2014 the kettle is on, the door is open, "
            "and you don't even have to knock.", F_SERIF_I(29))
y += 6
# sign-off, right aligned; wax seal sits to its left, clear of the text
d.text((928, y), "With hope (and snacks),", font=F_SERIF(29), fill=INK, anchor="ra")
sig_y = y + 40
d.text((928, sig_y), "Moci", font=F_SERIF_BI(44), fill=INK, anchor="ra")
hx, hy = 852, sig_y + 14
d.ellipse([hx, hy, hx + 12, hy + 12], fill=RED)
d.ellipse([hx + 12, hy, hx + 24, hy + 12], fill=RED)
d.polygon([(hx, hy + 8), (hx + 24, hy + 8), (hx + 12, hy + 26)], fill=RED)
y = sig_y + 58

# ---- PS ---------------------------------------------------------------------
d.text((108, y + 2), "P.S.  The cat is on your lap. Resistance is futile.",
       font=F_SERIF_I(27), fill=INK_SOFT)

# (the cat stays in the words: the P.S. promises her on the judge's lap)

# ---- wax seal, left of the signature ----------------------------------------
sx, sy, sr = 520, 888, 38
for ang in range(0, 360, 30):
    rr = sr + 5
    ox = sx + int(rr * math.cos(math.radians(ang)))
    oy = sy + int(rr * math.sin(math.radians(ang)))
    d.ellipse([ox - 7, oy - 7, ox + 7, oy + 7], fill=RED)
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED)
d.ellipse([sx - sr + 6, sy - sr + 6, sx + sr - 6, sy + sr - 6],
          outline=RED_DARK, width=2)
d.text((sx, sy), "M", font=F_SERIF_B(44), fill=(250, 245, 233), anchor="mm")

img.save("entry.png", optimize=True)
print("saved entry.png", os.path.getsize("entry.png"), "bytes")

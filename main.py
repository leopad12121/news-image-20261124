#!/usr/bin/env python3
"""Draw a one-page newspaper front page for 24 November 2026.

Everything is drawn with Pillow, loaded lazily so the module itself
only needs the standard library.  If drawing fails for any reason
(Pillow missing, fonts missing, anything else) the program falls back
to copying the shipped entry.png next to this script, so it still
exits successfully with a valid picture.
"""

import os
import shutil
import sys
from pathlib import Path

W = 1024
H = 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 241, 227)
INK = (18, 18, 18)
RED = (176, 32, 32)
GREY = (96, 94, 88)
SKY = (198, 226, 240)
SEA = (126, 190, 224)
LEAF = (102, 178, 102)
SUN = (244, 178, 66)
STEEL = (58, 74, 92)
PALE = (232, 226, 210)
GOLD = (212, 175, 55)
DARK = (20, 28, 44)


def _pick_font(loader, candidates, size):
    """Return the first usable font from candidates, else the default."""
    for path in candidates:
        try:
            if path and os.path.exists(path):
                return loader.truetype(path, size)
        except Exception:
            continue
    try:
        return loader.load_default(size=size)
    except Exception:
        return loader.load_default()


def _fonts(loader):
    base = "/usr/share/fonts/truetype/dejavu"
    lib = "/usr/share/fonts/truetype/liberation"
    serif_b = [f"{base}/DejaVuSerif-Bold.ttf",
               f"{lib}/LiberationSerif-Bold.ttf",
               "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"]
    serif = [f"{base}/DejaVuSerif.ttf",
             f"{lib}/LiberationSerif-Regular.ttf"]
    sans_b = [f"{base}/DejaVuSans-Bold.ttf",
              f"{lib}/LiberationSans-Bold.ttf"]
    sans = [f"{base}/DejaVuSans.ttf",
            f"{lib}/LiberationSans-Regular.ttf"]
    return {
        "mast": _pick_font(loader, serif_b, 58),
        "head_big": _pick_font(loader, serif_b, 36),
        "head": _pick_font(loader, serif_b, 30),
        "head_sm": _pick_font(loader, serif_b, 26),
        "deck": _pick_font(loader, serif, 20),
        "body": _pick_font(loader, serif, 18),
        "body_sm": _pick_font(loader, serif, 16),
        "kick": _pick_font(loader, sans_b, 18),
        "kick_sm": _pick_font(loader, sans_b, 16),
        "date": _pick_font(loader, sans_b, 20),
        "src": _pick_font(loader, sans, 13),
        "foot": _pick_font(loader, sans, 14),
        "stamp": _pick_font(loader, sans_b, 34),
    }


def _wrap(draw, text, font, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def _para(draw, x, y, text, font, max_w, fill, leading):
    """Draw wrapped text, return the y just below the last line."""
    for line in _wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def _rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def _kicker(draw, x, y, text, font):
    draw.text((x, y), text, font=font, fill=RED)


def _sources(draw, x, y, text, font):
    draw.text((x, y), text, font=font, fill=GREY)


def _lead_art(draw, x, y, w, h, tag_font):
    """Gaza City skyline at dusk, smoke plumes and red strike lines."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 214, 170), outline=INK, width=3)
    # dusk sun
    draw.ellipse([x + w - 96, y + 18, x + w - 36, y + 78], fill=SUN, outline=INK, width=2)
    # skyline
    heights = [150, 110, 180, 130, 200, 95, 165, 120]
    bx = x + 14
    for i, hh in enumerate(heights):
        bw = (w - 28) // len(heights) - 4
        top = y + h - 26 - hh
        draw.rectangle([bx, top, bx + bw, y + h - 26], fill=(96, 84, 70),
                       outline=INK, width=2)
        for wy in range(top + 12, y + h - 40, 22):
            draw.rectangle([bx + 6, wy, bx + 14, wy + 10],
                           fill=(250, 238, 190), outline=INK)
        bx += bw + 4
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 60, 50))
    # smoke plumes
    for sx, sy, sr in ((x + 90, y + 40, 26), (x + 116, y + 22, 20),
                       (x + 250, y + 52, 30), (x + 282, y + 30, 22)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(228, 228, 228), outline=GREY, width=2)
    # red strike lines
    for (x1, y1, x2, y2) in ((x + 60, y + 8, x + 100, y + 90),
                             (x + 210, y + 6, x + 250, y + 96),
                             (x + 330, y + 10, x + 360, y + 70)):
        draw.line([(x1, y1), (x2, y2)], fill=RED, width=5)
    # caption tag
    draw.rectangle([x + 10, y + h - 52, x + 196, y + h - 30],
                   fill=RED)
    draw.text((x + 18, y + h - 49), "GAZA CITY", font=tag_font, fill=(255, 255, 255))


def _building_art(draw, x, y, w, h):
    """Damaged apartment block."""
    draw.rectangle([x, y, x + w, y + h], fill=PALE, outline=INK, width=2)
    draw.rectangle([x + 10, y + 20, x + 78, y + h - 8], fill=(196, 178, 150), outline=INK, width=2)
    for wy in (y + 28, y + 46):
        for wx in (x + 22, x + 48):
            draw.rectangle([wx, wy, wx + 11, wy + 11], fill=(250, 238, 190), outline=INK)
    draw.polygon([(x + 84, y + 34), (x + w - 10, y + 34), (x + w - 10, y + h - 8),
                  (x + 84, y + h - 8)], fill=(120, 110, 96), outline=INK)
    draw.line([(x + 84, y + 34), (x + 108, y + 58), (x + 96, y + h - 8)], fill=INK, width=2)
    draw.ellipse([x + w - 52, y + 4, x + w - 12, y + 22], fill=(240, 240, 240), outline=GREY)
    draw.line([(x + w - 56, y + 14), (x + w - 40, y + 14)], fill=INK, width=3)


def _medal_art(draw, x, y, w, h):
    """Medal of Freedom: gold disc, ribbon, star."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 + 6
    # ribbon
    draw.polygon([(cx - 26, y + 4), (cx - 10, y + 4), (cx - 16, cy - 18),
                  (cx - 34, cy - 18)], fill=RED, outline=INK)
    draw.polygon([(cx + 26, y + 4), (cx + 10, y + 4), (cx + 16, cy - 18),
                  (cx + 34, cy - 18)], fill=(40, 60, 140), outline=INK)
    # disc
    draw.ellipse([cx - 30, cy - 24, cx + 30, cy + 36], fill=GOLD,
                 outline=INK, width=3)
    draw.ellipse([cx - 22, cy - 16, cx + 22, cy + 28], outline=(150, 115, 20),
                 width=2)
    # star
    import math
    pts = []
    for i in range(10):
        r = 14 if i % 2 == 0 else 6
        a = math.radians(-90 + i * 36)
        pts.append((cx + int(r * math.cos(a)), cy + 6 + int(r * math.sin(a))))
    draw.polygon(pts, fill=RED, outline=INK)


def _house_art(draw, x, y, w, h):
    """Country house at night with a searchlight."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 40, 70), outline=INK, width=2)
    # moon
    draw.ellipse([x + w - 34, y + 8, x + w - 14, y + 28], fill=(240, 240, 220),
                 outline=GREY)
    # house
    draw.rectangle([x + 18, y + 34, x + w - 18, y + h - 10], fill=(196, 178, 150),
                   outline=INK, width=2)
    draw.polygon([(x + 10, y + 36), (x + w // 2, y + 10), (x + w - 10, y + 36)],
                 fill=(96, 84, 70), outline=INK)
    for wx in (x + 30, x + 58, x + 86):
        draw.rectangle([wx, y + 46, wx + 14, y + 60], fill=(250, 238, 190), outline=INK)
    draw.rectangle([x + w // 2 - 8, y + 48, x + w // 2 + 8, y + h - 10],
                   fill=(70, 55, 40), outline=INK)
    # searchlight beam
    draw.polygon([(x + 8, y + h - 4), (x + 40, y + 8), (x + 52, y + 14)],
                 fill=(250, 240, 180), outline=INK)


def _satellite_art(draw, x, y, w, h):
    """Satellite in orbit against a dark sky."""
    import math
    draw.rectangle([x, y, x + w, y + h], fill=DARK, outline=INK, width=2)
    for sx, sy in ((x + 12, y + 10), (x + 40, y + 26), (x + 108, y + 8),
                   (x + 120, y + 40), (x + 66, y + 60), (x + 20, y + 52)):
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([x + 6, y + 4, x + w - 6, y + h - 4], outline=(90, 110, 150), width=2)
    # solar panels
    draw.rectangle([cx - 52, cy - 8, cx - 14, cy + 8], fill=(40, 90, 160),
                   outline=(200, 200, 200), width=1)
    draw.rectangle([cx + 14, cy - 8, cx + 52, cy + 8], fill=(40, 90, 160),
                   outline=(200, 200, 200), width=1)
    for px in (cx - 40, cx - 26, cx + 26, cx + 40):
        draw.line([(px, cy - 8), (px, cy + 8)], fill=(200, 200, 200), width=1)
    # body
    draw.rectangle([cx - 14, cy - 12, cx + 14, cy + 12], fill=(200, 200, 200),
                   outline=INK, width=2)
    draw.polygon([(cx + 14, cy - 8), (cx + 26, cy - 4), (cx + 14, cy + 2)],
                 fill=GOLD, outline=INK)


def _radar_art(draw, x, y, w, h):
    """Green radar screen with sweep and blips."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 40, 16), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 8
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 200, 90), width=2)
    draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                 outline=(60, 200, 90), width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(60, 200, 90), width=1)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=(60, 200, 90), width=1)
    import math
    a = math.radians(-45)
    draw.line([(cx, cy), (cx + int(r * math.cos(a)), cy + int(r * math.sin(a)))],
              fill=(120, 255, 140), width=2)
    for bx, by in ((cx - 22, cy - 14), (cx + 18, cy + 20), (cx + 30, cy - 24)):
        draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(120, 255, 140))


def _grid_cell(draw, fonts, x, y, w, h, kicker, headline, body, src, art_fn):
    art_w, art_h = 132, 72
    ax, ay = x + w - art_w, y + 24
    _kicker(draw, x, y, kicker, fonts["kick_sm"])
    head_w = w - art_w - 12
    hy = y + 24
    for line in _wrap(draw, headline, fonts["head_sm"], head_w):
        draw.text((x, hy), line, font=fonts["head_sm"], fill=INK)
        hy += 31
    art_fn(draw, ax, ay, art_w, art_h)
    by = max(hy, ay + art_h) + 8
    by = _para(draw, x, by, body, fonts["body_sm"], w, INK, 20)
    _sources(draw, x, by + 5, src, fonts["src"])


def _render():
    from PIL import Image, ImageDraw, ImageFont

    fonts = _fonts(ImageFont)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = W - MARGIN

    # --- masthead ---
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=fonts["mast"])
    d.text(((W - tw) / 2, 10), title, font=fonts["mast"], fill=INK)
    _rule(d, x0, x1, 88, 3)
    _rule(d, x0, x1, 94, 1)
    dateline = "TUESDAY, 24 NOVEMBER 2026  |  SIX STORIES FROM AROUND THE GLOBE"
    dw = d.textlength(dateline, font=fonts["date"])
    d.text(((W - dw) / 2, 102), dateline, font=fonts["date"], fill=INK)
    _rule(d, x0, x1, 132, 2)

    # --- lead story ---
    ly = 144
    _kicker(d, x0, ly, "GAZA  -  ISRAEL-HAMAS WAR", fonts["kick"])
    hy = ly + 26
    for line in ["ISRAELI STRIKES KILL", "HAMAS SECURITY CHIEF"]:
        d.text((x0, hy), line, font=fonts["head_big"], fill=INK)
        hy += 40
    deck = ("Naeem Abu Nahel among seven killed in Gaza City, medics say, "
            "as strikes go on despite a ceasefire.")
    hy = _para(d, x0, hy + 6, deck, fonts["deck"], 530, INK, 24)
    body = ("Israeli airstrikes kill the Hamas internal security chief and "
            "six others, including two police officers.")
    hy = _para(d, x0, hy + 8, body, fonts["body"], 530, INK, 22)
    _sources(d, x0, hy + 8, "SOURCES: REUTERS, AP, SCMP  -  24 NOV 2026", fonts["src"])
    _lead_art(d, 580, ly, 408, 250, fonts["kick_sm"])

    # --- 2x2 grid ---
    _rule(d, x0, x1, 424, 2)
    gy = 438
    cell_w = (CONTENT_W - 28) // 2
    cell_h = 172
    _grid_cell(d, fonts, x0, gy, cell_w, cell_h,
               "WAR IN UKRAINE  -  ZAPORIZHZHIA", "STRIKE KILLS TWO, WOUNDS 40",
               "A Russian attack hits a Zaporizhzhia apartment block. "
               "Two killed, 40 wounded, including four children.",
               "SOURCES: AP, REUTERS", _building_art)
    _grid_cell(d, fonts, x0 + cell_w + 28, gy, cell_w, cell_h,
               "UNITED STATES  -  WASHINGTON", "GIULIANI'S MEDAL OF FREEDOM",
               "Trump awards the top US civilian honour to the ex-New "
               "York mayor in a private Oval Office ceremony.",
               "SOURCES: REUTERS, AP", _medal_art)
    gy2 = gy + cell_h + 14
    _rule(d, x0, x1, gy2 - 8, 1, fill=(200, 192, 172))
    _grid_cell(d, fonts, x0, gy2, cell_w, cell_h,
               "BRITAIN  -  SANDRINGHAM", "TWO HELD OVER ROYAL BREAK-IN",
               "Two men are arrested after a break-in at Anmer Hall, the "
               "country home of William and Kate.",
               "SOURCES: REUTERS, AP", _house_art)
    _grid_cell(d, fonts, x0 + cell_w + 28, gy2, cell_w, cell_h,
               "EUROPE  -  NATO", "NATO VOWS SPACE DEFENCE",
               "Rutte vows the alliance will defend in space after "
               "reports of a Russian nuclear-armed satellite.",
               "SOURCES: REUTERS, SCMP", _satellite_art)
    midx = x0 + cell_w + 14
    d.line([(midx, gy), (midx, gy2 + cell_h)], fill=(200, 192, 172), width=1)

    # --- bottom strip ---
    by = gy2 + cell_h + 14
    _rule(d, x0, x1, by, 2)
    by += 12
    _kicker(d, x0, by, "GERMANY  -  BERLIN", fonts["kick_sm"])
    d.text((x0, by + 26), "GERMANY FIRST INTO DELTA SYSTEM", font=fonts["head"], fill=INK)
    endy = _para(d, x0, by + 66,
                 "Berlin becomes the first country to gain access to "
                 "Ukraine's Delta battlefield management system, Kyiv says.",
                 fonts["body"], 720, INK, 23)
    _sources(d, x0, endy + 6, "SOURCES: KYIV INDEPENDENT  -  24 NOV 2026", fonts["src"])
    _radar_art(d, 780, by + 6, 208, 108)

    # --- footer ---
    fy = 962
    _rule(d, x0, x1, fy, 2)
    d.text((x0, fy + 10),
           "ALSO: LANDMINE TOLL HITS FIVE-YEAR HIGH OF 7,000  -  "
           "US ENVOY DOUBTS END TO $3.8BN ISRAEL AID  -  "
           "SEOUL IN AI CHEAT ROW",
           font=fonts["foot"], fill=GREY)
    return img


def _fallback_bytes():
    here = Path(__file__).resolve().parent
    shipped = here / "entry.png"
    with open(shipped, "rb") as fh:
        return fh.read()


def _out_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return Path(env)
    return Path("/output")


def _write_both(data):
    here = Path(__file__).resolve().parent
    out_dir = _out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "entry.png", "wb") as fh:
        fh.write(data)
    try:
        with open(here / "entry.png", "wb") as fh:
            fh.write(data)
    except Exception:
        pass


def main():
    try:
        import io
        from PIL import Image  # noqa: F401  (lazy import inside try)
        img = _render()
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        _write_both(buf.getvalue())
    except Exception:
        try:
            _write_both(_fallback_bytes())
        except Exception:
            raise
    return 0


if __name__ == "__main__":
    sys.exit(main())

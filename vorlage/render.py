"""Mamasafely TikTok-Vorlage: Hook -> 5 Karten -> Frage. 1080x1920, 30 fps, ~15 s.

Aufruf: python3 render.py spec.json ausgabe.mp4 [--frames 0.5,5,10]
"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/truetype/google-fonts/Poppins-"
BG = (255, 248, 240)
INK = (45, 45, 45)
CORAL = (248, 99, 95)
CARD_COLORS = ["#A8D8F0", "#FDE68A", "#FFCBA4", "#A8E6CF", "#D4A5E8"]

_fc = {}
def font(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(F + w + ".ttf", s)
    return _fc[k]

def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def ctext(d, y, text, f, fill=INK):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill)

def card_img(i, title, sub, color, highlight):
    cw, ch = 880, 214
    im = Image.new("RGBA", (cw + 14, ch + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, cw + 12, ch + 12), 34, fill=INK)  # Schatten
    d.rounded_rectangle((0, 0, cw, ch), 34, fill=hexrgb(color),
                        outline=CORAL if highlight else INK, width=9 if highlight else 6)
    d.ellipse((30, 57, 130, 157), fill="white", outline=INK, width=6)
    n = str(i + 1); f = font("Bold", 56)
    d.text((80 - d.textlength(n, font=f) / 2, 66), n, font=f, fill=INK)
    ft, fs = font("Bold", 44), font("Medium", 32)
    tl = wrap(d, title, ft, cw - 190)
    sl = wrap(d, sub, fs, cw - 190)
    total = len(tl) * 56 + len(sl) * 42 + 8
    y = (ch - total) / 2 - 4
    for l in tl: d.text((160, y), l, font=ft, fill=INK); y += 56
    y += 8
    for l in sl: d.text((160, y), l, font=fs, fill=(70, 60, 60)); y += 42
    return im

def badge(d, x, y, text):
    fb = font("Bold", 30); bw = d.textlength(text, font=fb) + 44
    d.rounded_rectangle((x - bw, y, x, y + 54), 27, fill=CORAL, outline=INK, width=5)
    d.text((x - bw + 22, y + 7), text, font=fb, fill="white")

def render(spec, out, only=None):
    cards = [card_img(i, *c[:2], CARD_COLORS[i], i + 1 == spec["highlight"])
             for i, c in enumerate(spec["facts"])]
    T_CARDS, STEP = 1.5, 1.9
    T_CTA = T_CARDS + 5 * STEP + 2.4
    DUR = T_CTA + 3.6
    nframes = int(DUR * FPS)
    proc = None
    if only is None:
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
             "-f", "lavfi", "-t", f"{DUR:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
             "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out],
            stdin=subprocess.PIPE)
    frames = [int(t * FPS) for t in only] if only else range(nframes)
    for fi in frames:
        t = fi / FPS
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
        # dezente Punkte im Hintergrund
        for k in range(14):
            x = (k * 263 + 90) % W; y = (k * 517 + 140) % H
            r = 10 + (k % 3) * 6
            d.ellipse((x - r, y - r, x + r, y + r), fill=(252, 232, 222))
        # --- Hook ---
        if t < T_CARDS + 0.3:
            a = 1 - clamp((t - T_CARDS) / 0.3)
            off = (1 - ease_out(t / 0.35)) * 120
            ink = tuple(int(BG[j] + (INK[j] - BG[j]) * a) for j in range(3))
            y0 = 560 + off
            ctext(d, y0, spec["kicker"], font("Bold", 38), CORAL if a > .5 else BG)
            y = y0 + 90
            for line in spec["hook"]:
                if line.startswith("*"):
                    txt = line[1:]; f = font("Bold", 112)
                    tw = d.textlength(txt, font=f)
                    p = ease_out((t - 0.25) / 0.3)
                    if a > 0.05:
                        d.rounded_rectangle(((W - tw) / 2 - 24, y + 22,
                                             (W - tw) / 2 - 24 + (tw + 48) * p, y + 140), 24,
                                            fill=CORAL)
                    ctext(d, y, txt, f, "white" if a > .5 else BG)
                    y += 150
                else:
                    ctext(d, y, line, font("Bold", 96), ink); y += 125
            sc = 1 + 0.06 * math.sin(t * 9)
            fz = int(52 * sc)
            ctext(d, y + 50, spec["teaser"], font("Bold", fz), CORAL if a > .5 else BG)
        # --- Themenleiste oben ---
        if t >= T_CARDS - 0.1 and t < T_CTA + 0.4:
            p = ease_out((t - T_CARDS + 0.1) / 0.4)
            q = 1 - clamp((t - T_CTA) / 0.4)
            y = -120 + 290 * p - (1 - q) * 300
            fb = font("Bold", 42); tw = d.textlength(spec["topic"], font=fb)
            d.rounded_rectangle(((W - tw) / 2 - 36, y, (W + tw) / 2 + 36, y + 86), 43,
                                fill=INK)
            ctext(d, y + 14, spec["topic"], fb, "white")
        # --- Karten ---
        if T_CARDS <= t < T_CTA + 0.5:
            for i, c in enumerate(cards):
                ts = T_CARDS + 0.15 + i * STEP
                if t < ts: continue
                p = ease_back((t - ts) / 0.45)
                side = -1 if i % 2 == 0 else 1
                x = 86 + side * (1 - p) * 1100
                y = 300 + i * 232
                if t > T_CTA:  # Karten fliegen raus
                    x += -side * ease_out((t - T_CTA) / 0.45) * 1200
                im.paste(c, (int(x), int(y)), c)
                if i + 1 == spec["highlight"] and t > ts + 0.4:
                    pul = 1 + 0.08 * math.sin((t - ts) * 10)
                    badge(d, int(x) + 860, int(y) - 28, "WICHTIG")
        # --- Frage am Ende ---
        if t >= T_CTA + 0.2:
            p = ease_back((t - T_CTA - 0.2) / 0.5)
            y = 560 + (1 - p) * 200
            for k, line in enumerate(spec["question"]):
                f = font("Bold", 92)
                if line.startswith("*"):
                    txt = line[1:]; tw = d.textlength(txt, font=f)
                    d.rounded_rectangle(((W - tw) / 2 - 24, y + 18, (W + tw) / 2 + 24, y + 132),
                                        24, fill=CORAL)
                    ctext(d, y, txt, f, "white")
                else:
                    ctext(d, y, line, f)
                y += 135
            ctext(d, y + 40, spec["sub"], font("Medium", 44))
            fb = font("Bold", 40); tw = d.textlength(spec["save"], font=fb)
            y2 = y + 150
            d.rounded_rectangle(((W - tw) / 2 - 40, y2, (W + tw) / 2 + 40, y2 + 90), 45,
                                fill="white", outline=INK, width=6)
            ctext(d, y2 + 17, spec["save"], fb)
        ctext(d, 1520 if t >= T_CTA else 1495, "@mamasafely", font("Bold", 34), (190, 150, 140))
        if proc: proc.stdin.write(im.tobytes())
        else: im.save(f"{out}-{fi/FPS:.1f}s.jpg", quality=88)
    if proc:
        proc.stdin.close(); rc = proc.wait()
        if rc: sys.exit(rc)
    return DUR

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    only = None
    if "--frames" in sys.argv:
        only = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]
    print(render(spec, sys.argv[2], only))

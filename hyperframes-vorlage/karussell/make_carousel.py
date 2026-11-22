#!/usr/bin/env python3
"""MamaSafely-Karussell (7 Slides, 1080x1350 = 4:5) aus einer JSON-Spec bauen.

Aufruf:
    python3 make_carousel.py spec.json AUSGABE_ORDNER [--png]

Erzeugt ein HyperFrames-Projekt (jede Slide = 1 Sekunde). Mit --png werden die
7 Slides als slide-1.png ... slide-7.png in AUSGABE_ORDNER/out/ exportiert.
Aufbau und alle Regeln: siehe ../CLAUDE.md
"""
import glob, html, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))
STYLE = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
CHECK = '<svg viewBox="0 0 40 40"><path d="M9 21 L17 29 L32 12" fill="none" stroke="#2D2D2D" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV = '<div class="chev"><svg viewBox="0 0 40 60"><path d="M8 6 L32 30 L8 54" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
FARBEN = ["#A8D8F0", "#FDE68A", "#FFCBA4", "#A8E6CF", "#D4A5E8"]


def build(spec, out):
    os.makedirs(out, exist_ok=True)
    if not os.path.exists(os.path.join(out, "assets")):
        shutil.copytree(os.path.join(HERE, "assets"), os.path.join(out, "assets"))
    slides = [("cover", None)] + [("item", s) for s in spec["slides"]] + [("cta", None)]
    n = len(slides)
    body = ""
    for i, (kind, s) in enumerate(slides):
        inner = '<div class="pill"><div class="dot"></div>@mamasafely</div>'
        if kind == "cover":
            c = spec["cover"]
            inner += f'''<div class="kicker">{c["kicker"]}</div><h1 class="cv-h">{c["titel"]}</h1>
<div class="cv-art">{ICONS[c["icon"]]}</div><div class="teaser">{c["teaser"]}</div>
<div class="swipe">Wischen <svg viewBox="0 0 60 40"><path d="M6 20 H50 M36 6 L52 20 L36 34" fill="none" stroke="#2D2D2D" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></div>{CHEV}'''
        elif kind == "cta":
            c = spec["schluss"]
            inner += f'''<div class="ct-flow"><h1 class="ct-h">{c["titel"]}</h1><div class="ct-when">{c["text"]}</div><div class="ct-tip">{c["tipp"]}</div></div>
<div class="ct-btn ct-share">{c.get("teilen", "Schick das einer Schwangeren")}</div>
<div class="ct-row"><div class="ct-save"><svg viewBox="0 0 46 56"><path d="M5 5 H41 V51 L23 38 L5 51 Z" fill="#FDE68A" stroke="#2D2D2D" stroke-width="5" stroke-linejoin="round"/></svg>Speichern</div><div class="ct-follow">Folge @mamasafely</div></div>
<div class="src">{c.get("quelle", "")}</div>'''
        else:
            farbe = s.get("farbe", FARBEN[(i - 1) % 5])
            items = "".join(f'<li><span class="box" style="background:{farbe}">{CHECK}</span><span>{html.escape(t)}</span></li>' for t in s["punkte"])
            hl = f'<div class="hl">{html.escape(s["hinweis"])}</div>' if s.get("hinweis") else ""
            inner += f'''<div class="badge">{i}</div><h2 class="sl-t">{html.escape(s["titel"])}</h2>{hl}
<div class="card"><div class="ic" style="background:{farbe}">{ICONS[s["icon"]]}</div><ul>{items}</ul></div>
<div class="note">{html.escape(s.get("notiz", ""))}</div>{CHEV}'''
        body += f'<div id="s{i+1}" class="clip slide" data-start="{i}" data-duration="1" data-track-index="1">{inner}</div>\n'
    doc = f'''<!doctype html><html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1350">
<script src="assets/gsap.min.js"></script><style>{STYLE}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{n}" data-width="1080" data-height="1350">
<div class="blob" style="width:620px;height:620px;left:-240px;top:60px;background:#f7c8d4"></div>
<div class="blob" style="width:560px;height:560px;left:700px;top:520px;background:#a8e6cf"></div>
<div class="blob" style="width:640px;height:640px;left:-200px;top:1020px;background:#fde68a"></div>
<div class="blob" style="width:380px;height:380px;left:820px;top:1100px;background:#d4a5e8"></div>
<div id="dots"></div>
{body}</div><script>const tl=gsap.timeline({{paused:true}});tl.set({{}},{{}},{n});window.__timelines["main"]=tl;</script></body></html>'''
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(doc)
    return n


def export_png(out, n):
    times = ",".join(f"{i}.5" for i in range(n))
    subprocess.run(["npx", "--yes", "hyperframes@0.9.33", "snapshot", "--at", times], cwd=out, check=True)
    snap = max(glob.glob(os.path.join(out, ".hyperframes/artifacts/snapshots/*")), key=os.path.getmtime)
    os.makedirs(os.path.join(out, "out"), exist_ok=True)
    for i in range(n):
        src = glob.glob(os.path.join(snap, f"frame-{i:02d}-at-{i}.5s.png"))[0]
        shutil.copy(src, os.path.join(out, "out", f"slide-{i+1}.png"))
    print("PNGs:", os.path.join(out, "out"))


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    assert len(spec["slides"]) == 5, "Es müssen genau 5 Inhalts-Slides sein"
    out = os.path.abspath(sys.argv[2])
    n = build(spec, out)
    print(f"Projekt: {out}  ({n} Slides)")
    if "--png" in sys.argv:
        export_png(out, n)


if __name__ == "__main__":
    main()

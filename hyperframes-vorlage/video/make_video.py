#!/usr/bin/env python3
"""MamaSafely-Video aus einer JSON-Spec bauen (HyperFrames, 1080x1920, ~15 s).

Aufruf:
    python3 make_video.py spec.json AUSGABE_ORDNER [--render datei.mp4]

Ohne --render wird nur das HyperFrames-Projekt erzeugt (zum Prüfen mit
`npx hyperframes@0.9.33 snapshot`). Mit --render wird zusätzlich das MP4 gerendert.
Aufbau und alle Regeln: siehe ../CLAUDE.md
"""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template")
HOOK = 1.5          # Länge Titelbild
CTA = 2.5           # Länge Schluss-Szene
FD_NORMAL = 2.2     # Länge pro Karte
FD_STEMPEL = 2.6    # Länge pro Karte, wenn Stempel (MYTHOS/STIMMT!) drauf sind
FIVE = '<span id="hk-five">5</span>'


def host(id_, src, start, dur, track, z, extra=""):
    return (f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{src}" '
            f'data-start="{start}" data-duration="{dur}"\n        data-track-index="{track}" '
            f'data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"{extra}></div>\n')


def build(spec, out):
    karten = spec["karten"]
    assert len(karten) == 5, "Es müssen genau 5 Karten sein"
    stempel = any(k.get("stempel") for k in karten)
    FD = FD_STEMPEL if stempel else FD_NORMAL
    hl = int(spec.get("highlight", 3))
    chips = spec.get("zahlen_chips", True)
    starts = [round(HOOK + i * FD, 2) for i in range(5)]
    cta_s = round(HOOK + 5 * FD, 2)
    tot = round(cta_s + CTA, 2)

    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(TEMPLATE, out)

    # index.html
    hosts = host("bg", "bg.html", 0, tot, 0, 1) + host("hook", "hook.html", 0, HOOK, 1, 2)
    for i, k in enumerate(karten):
        v = {"num": str(i + 1), "title": k["titel"], "sub": k["text"], "accent": k["farbe"],
             "icon": k["icon"], "stamp": k.get("stempel", ""), "dur": FD}
        hosts += host(f"fact{i+1}", "fact.html", starts[i], FD, 1, 2,
                      " data-variable-values='" + json.dumps(v, ensure_ascii=False).replace("'", "&#39;") + "'")
    hosts += host("cta", "cta.html", cta_s, CTA, 1, 2) + host("brand", "brand.html", 0, tot, 2, 3)
    idx = open(os.path.join(TEMPLATE, "index.html"), encoding="utf-8").read()
    head = idx.split('<div\n      id="root"')[0]
    head = re.sub(r"<html[^>]*>", '<html lang="de">', head, count=1, flags=re.S)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(head + f'''<div id="root" data-composition-id="main" data-start="0" data-duration="{tot}" data-width="1080" data-height="1920">
{hosts}    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {tot});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')

    comp = lambda n: os.path.join(out, "compositions", n)

    # Hintergrund
    s = open(comp("bg.html"), encoding="utf-8").read()
    s = s.replace('data-duration="27"', f'data-duration="{tot}"').replace("duration: 27,", f"duration: {tot},") \
         .replace("tl.set({}, {}, 27);", f"tl.set({{}}, {{}}, {tot});")
    open(comp("bg.html"), "w", encoding="utf-8").write(s)

    # Branding: @mamasafely, Fortschrittsbalken, Themenzeile
    s = open(comp("brand.html"), encoding="utf-8").read()
    s = s.replace("const starts = [3, 7, 11, 15, 19];", f"const starts = {json.dumps(starts)};")
    s = s.replace('data-start="0" data-duration="27"', f'data-start="0" data-duration="{tot}"') \
         .replace('id="br-progress" class="clip" data-start="0" data-duration="23"',
                  f'id="br-progress" class="clip" data-start="0" data-duration="{cta_s}"')
    s = s.replace("tl.set({}, {}, 27);",
                  f'tl.fromTo("#br-topic", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {HOOK});\n    tl.set({{}}, {{}}, {tot});')
    s = s.replace("      #root #br-progress {", '''      #root #br-topic {
        position: absolute; left: 72px; top: 296px; width: 860px;
        font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 42px; color: #2d2d2d;
      }
      #root #br-progress {''')
    s = s.replace('    <div id="br-progress"',
                  f'    <div id="br-topicwrap" class="clip" data-start="{HOOK}" data-duration="{round(cta_s-HOOK,2)}"><div id="br-topic">{spec["thema"]}</div></div>\n    <div id="br-progress"')
    open(comp("brand.html"), "w", encoding="utf-8").write(s)

    # Titelbild (Hook)
    l1, l2, mark, l4 = (spec["hook"] + ["", "", "", ""])[:4]
    l1 = l1.replace("{5}", FIVE)
    mark_style = f' style="font-size:{spec["mark_groesse"]}px"' if spec.get("mark_groesse") else ""
    s = open(comp("hook.html"), encoding="utf-8").read()
    s = re.sub(r'(<div id="hk-kicker"[^>]*>)[^<]*', lambda m: m.group(1) + spec["kicker"], s)
    s = re.sub(r'(<span class="hk-line" id="hk-l1">).*?(</span>\n)', lambda m: m.group(1) + l1 + m.group(2), s, count=1)
    s = re.sub(r'(<span class="hk-line" id="hk-l2">)[^<]*', lambda m: m.group(1) + l2, s)
    s = re.sub(r'<span class="hk-mark">[^<]*</span>', f'<span class="hk-mark"{mark_style}>{mark}</span>', s)
    s = re.sub(r'(<span class="hk-line" id="hk-l4">)[^<]*', lambda m: m.group(1) + l4, s)
    s = re.sub(r'(<span id="hk-teaser-in"[^>]*>)[^<]*', lambda m: m.group(1) + spec["teaser"], s)
    if "hk-five" not in l1:
        s = re.sub(r'\n\s*tl\.fromTo\("#hk-five".*?\n', "\n", s)
    s = s.replace('data-duration="3"', f'data-duration="{HOOK}"').replace("}, 2.78);", f"}}, {HOOK-0.15});") \
         .replace("tl.set({}, {}, 3);", f"tl.set({{}}, {{}}, {HOOK});").replace("}, 0.5);\n", "}, 0.25);\n")
    open(comp("hook.html"), "w", encoding="utf-8").write(s)

    # Schluss-Szene
    f1, f2 = spec["frage"]
    s = open(comp("cta.html"), encoding="utf-8").read()
    s = re.sub(r'(<span id="ct-q-in"[^>]*>).*?</span></span>',
               lambda m: m.group(1) + f'{f1} <span class="ct-mark">{f2}</span></span>', s, count=1, flags=re.S)
    s = re.sub(r'(<span id="ct-sub-in"[^>]*>)[^<]*', lambda m: m.group(1) + spec["unterzeile"], s)
    s = re.sub(r"Speichern – für [^<]*", spec["speichern"], s)
    s = s.replace('data-duration="4"', f'data-duration="{CTA}"')
    if not chips:
        s = s.replace('<div id="ct-chips" class="clip"', '<div id="ct-chips" class="clip" style="display:none"')
        s = s.replace("top: 1100px;", "top: 930px;").replace("top: 1250px;", "top: 1090px;")
    js = ['const tl = gsap.timeline({ paused: true });',
          'tl.fromTo("#ct-q-in", { y: 60, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.8)" }, 0);',
          'tl.fromTo("#ct-sub-in", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.2, ease: "power3.out" }, 0.15);']
    if chips:
        js += ['tl.fromTo(["#ct-c1", "#ct-c2", "#ct-c3", "#ct-c4", "#ct-c5"], { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.25, ease: "back.out(2.6)", stagger: 0.05 }, 0.25);',
               f'tl.fromTo("#ct-c{hl}", {{ y: 0 }}, {{ y: -22, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 5, immediateRender: false }}, 0.75);']
    js += ['tl.fromTo("#ct-follow", { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.28, ease: "back.out(1.8)" }, 0.45);',
           'tl.fromTo("#ct-follow", { scale: 1 }, { scale: 1.05, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 5, immediateRender: false }, 0.8);',
           'tl.fromTo("#ct-save", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.22, ease: "power3.out" }, 0.65);',
           f"tl.set({{}}, {{}}, {CTA});", 'window.__timelines["cta"] = tl;']
    s = re.sub(r"<script>.*?</script>", "<script>\n    " + "\n    ".join(js) + "\n  </script>", s, count=1, flags=re.S)
    open(comp("cta.html"), "w", encoding="utf-8").write(s)
    return tot


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.abspath(sys.argv[2])
    tot = build(spec, out)
    print(f"Projekt: {out}  ({tot} s)")
    if "--render" in sys.argv:
        mp4 = os.path.abspath(sys.argv[sys.argv.index("--render") + 1])
        subprocess.run(["npx", "--yes", "hyperframes@0.9.33", "render", "--output", mp4], cwd=out, check=True)
        print("Video:", mp4)


if __name__ == "__main__":
    main()

# MamaSafely – Content-Vorlage (HyperFrames)

Dieser Ordner enthält das **echte, freigegebene Design** für @mamasafely (TikTok + Instagram):
Videos (1080×1920, ~15 s), Karussells (1080×1350, 7 Slides) und Story-Clips (1080×1920, 7 s).
Alles wird mit [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → Video) gebaut.

> Der ältere Ordner `/vorlage` (Python/PIL-Renderer) ist eine vereinfachte Nachbildung.
> **Für neue Posts immer diesen Ordner hier verwenden.**

## Schnellstart

```bash
cd hyperframes-vorlage
export HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome   # falls Chrome dort liegt; sonst weglassen

# Video
python3 video/make_video.py beispiele/videos/kliniktasche.json /tmp/kt
cd /tmp/kt && npx --yes hyperframes@0.9.33 check          # muss "Check passed" sagen
npx --yes hyperframes@0.9.33 snapshot --at 0.1,2.5,4.7,6.9,9.1,11.3,13.9   # Kontaktbogen ansehen!
npx --yes hyperframes@0.9.33 render --output kliniktasche.mp4
# oder in einem Schritt:  python3 video/make_video.py spec.json /tmp/x --render /tmp/x.mp4

# Karussell (PNG-Export)
python3 karussell/make_carousel.py beispiele/karussells/u-untersuchungen.json /tmp/u --png
# → /tmp/u/out/slide-1.png … slide-7.png
```

Voraussetzungen: Node ≥ 22, Python 3, Chrome/Chromium, FFmpeg (für Video-Render).
Schriften (Fredoka, Quicksand) und GSAP liegen lokal in `assets/` – kein Internet nötig.

**Immer prüfen, bevor geliefert wird:** `check` ausführen und den Kontaktbogen (Snapshot) ansehen –
überlappende Texte, zu lange Zeilen und abgeschnittene Hinweise fallen nur dort auf.

## Ordner

| Pfad | Inhalt |
|---|---|
| `video/template/` | HyperFrames-Projekt: `compositions/bg.html` (Hintergrund), `hook.html` (Titelbild), `fact.html` (wiederverwendbare Karte, 18 Icons), `cta.html` (Schluss), `brand.html` (@mamasafely-Pill, Fortschrittsbalken, Themenzeile) |
| `video/make_video.py` | JSON-Spec → fertiges Projekt (+ optional MP4) |
| `karussell/make_carousel.py` | JSON-Spec → 7 Slides (+ PNG-Export) · `style.css`, `icons.json` |
| `story/template/` | 7-s-Story „Mythos oder Wahrheit?“ (Frage + 2 Antwort-Buttons, springendes „?“) – Texte direkt in `compositions/story.html` ändern |
| `beispiele/` | Alle bisher produzierten Specs (13 Videos, 4 Karussells) als Vorlage zum Kopieren |

## Design-System (nicht ändern)

- Hintergrund Creme `#F5F0E6` mit Pastell-Kreisen + Punktraster, gezeichnete Ornamente
- Text/Linien `#2D2D2D`, Akzent Koralle `#F8635F`, „STIMMT!“-Grün `#23935A`
- Kartenfarben (immer in dieser Reihenfolge 1–5): `#A8D8F0` `#FDE68A` `#FFCBA4` `#A8E6CF` `#D4A5E8`
- Highlight-Rosa `#F7C8D4` (Markierung im Titel), Gelb `#FDE68A` (Markierung in der Frage)
- Schriften: **Fredoka** 600/700 (Überschriften), **Quicksand** 600/700 (Fließtext)
- Stil: dicke dunkle Konturen (4–5 px), harte Schatten (6–12 px versetzt), runde Ecken, Sticker-Look
- Branding oben links: weiße Pill „@mamasafely“ mit rotem Punkt

## Video-Aufbau (schnelle Version – wegen Wiedergabezeit!)

Analyse hat gezeigt: Zuschauer wischen nach ~3 s weg, wenn nichts passiert. Deshalb:

| Teil | Zeit |
|---|---|
| Titelbild (Hook) – Frame 0 ist schon voll lesbar (= Vorschaubild) | 0–1,5 s |
| 5 Karten, abwechselnd links/rechts einfliegend | je 2,2 s (mit Stempel 2,6 s) |
| Schluss-Szene (Frage, Zahlen-Chips, „Folge @mamasafely“, Speichern) | 2,5 s |
| **Gesamt** | **15 s** (mit Stempeln 17 s) |

Die Themenzeile bleibt ab 1,5 s oben stehen. **Keine Musik einbauen** – Sound wählt der Nutzer in der App
(nur kommerziell lizenzierte Sounds, s. u.).

### Video-Spec (JSON)

```json
{
  "thema": "Checkliste Kliniktasche",            // kleine Zeile oben, ab 1,5 s sichtbar
  "kicker": "CHECKLISTE · KLINIKTASCHE",          // gelbe Pill über dem Titel, GROSS
  "hook": ["{5} Dinge, die", "in die", "Kliniktasche", "müssen"],  // Zeile 1, 2, MARKIERT, 4 ({5} = rote 5)
  "mark_groesse": 112,                            // optional, wenn markiertes Wort > 11 Zeichen
  "teaser": "Nr. 2 vergessen viele!",             // roter Sticker, max. ~24 Zeichen
  "highlight": 2,                                 // welche Nummer am Ende hüpft (= die im Teaser)
  "karten": [ {"titel": "…", "text": "…", "farbe": "#A8D8F0", "icon": "doc", "stempel": "MYTHOS"} ],
  "frage": ["Schick das einer", "Schwangeren!"],  // 2. Teil wird gelb markiert
  "unterzeile": "Was darf bei dir nicht fehlen?",
  "speichern": "Jetzt speichern!",
  "zahlen_chips": false                           // false, wenn nicht nach einer Nummer gefragt wird (z. B. „deine SSW“)
}
```

**Icons:** `babyface bag carrot carseat cup doc drop eye feet flame flower hand heart hiccup moon pacifier plug voice`
(`voice` = Herz mit Schallwellen, `flame` = Sodbrennen/Fieber/schnell, `doc` = Mutterpass/Heft, `plug` = Ladekabel)

**Stempel:** `"MYTHOS"` (rot) oder `"STIMMT!"` / `"STIMMT WOHL!"` (grün, automatisch bei STIMMT/WAHR).

### Längen-Grenzen (sonst überlappt etwas)

- Hook-Zeilen ≤ 12–13 Zeichen, markiertes Wort ≤ 11 (sonst `mark_groesse` 100–112)
- Teaser ≤ ~24 Zeichen (sonst schiebt er sich übers Babygesicht)
- Kartentitel ≤ ~35 Zeichen (ab 25 Zeichen automatisch kleiner), Kartentext ≤ ~55 Zeichen / max. 8 Wörter
- Frage 2. Teil ≤ ~12 Zeichen

## Karussell-Aufbau (Instagram + TikTok-Fotos)

7 Slides, 1080×1350: **Titelbild** (Doppelpunkt-Titel, Teaser, „Wischen →“, roter Pfeil am Rand) →
**5 Slides** (Nummer, Titel, 3 Abhak-Punkte, Notiz, Icon) → **Schluss** (Titel, Kernaussage, Tipp-Box,
„Schick das …“, Speichern, Folgen, Quelle). **Kein Seitenzähler** (verwirrt neben den Nummern).

- Titel im **Doppelpunkt-Stil**: „Das passiert in den ersten 24 Stunden:“ – macht Lust aufs Wischen
- 3 Punkte pro Slide, je ≤ ~45 Zeichen; `hinweis` (roter Sticker) nur auf der Teaser-Slide
- Schluss immer mit Teilen-Aufforderung (DM-Teilen ist Instagrams stärkstes Signal) + Quelle, wenn vorhanden
- Spec-Format: siehe `beispiele/karussells/*.json`

## Inhaltliche Regeln (wichtig!)

1. **Alles muss den Empfehlungen von Ärzten/Hebammen entsprechen.** Nichts ungeprüft formulieren.
   Zahlen mit „ca.“ absichern, wo es individuell schwankt. Bei Unsicherheit recherchieren
   (z. B. Netzwerk Gesund ins Leben, Verbraucherzentrale, G-BA, BZgA/kindergesundheit-info).
2. Wo ein Thema ein Risiko berührt (Kindsbewegungen, Blasensprung, Schlaf, Gelbsucht …), einen
   **Sicherheitshinweis** einbauen („dann direkt Klinik/Hebamme anrufen“) – in der Karte oder im angepinnten Kommentar.
3. **Keine erfundenen Zitate, Personen, Bewertungen oder Studien.**
4. **Highlight-Nummer variieren** – nicht immer Nr. 3. Teaser-Formulierungen ebenfalls abwechseln.
5. Keine Fernauskünfte in Kommentar-Antworten – allgemein antworten und auf Hebamme/Ärztin verweisen.

## Caption-Format (pro Post mitliefern)

```
<Hook-Zeile mit 1–2 Emojis>
<Warum anschauen / Highlight-Nummer>
<Frage oder Teilen-Aufforderung> 👇
#tag1 #tag2 #tag3 #tag4 #mamasafely      (genau 5 Hashtags, Suchbegriffe vorne)
📌 Anzupinnender Kommentar: <Frage, die Mamas zum Erzählen bringt, oder Sicherheitshinweis>
```
Suchbegriffe (z. B. „ab wann“, „Baby treten“, „Herzschlag“) in die erste Zeile und Hashtags.

## Posting-Plan & Praxis

- TikTok: morgens (~8–9 Uhr) + abends (~20 Uhr). Rhythmus: **2 Videos → 1 Karussell → 2 Videos → …**
- Papa-Videos bevorzugt am Wochenendabend.
- Titelbild in der App auf das erste Bild setzen.
- **Musik nur aus „Kommerzielle Sounds“** (Abmahnrisiko bei Trend-Musik für kommerzielle Accounts),
  Lautstärke 10–20 %. Feste Sounds: „Little Fairy“ (Little Garden), „Softly“ (Claudio Constantini).
  Auf Instagram Sound aus Metas eigener Bibliothek; **MP4 direkt hochladen, nie TikTok-Download (Wasserzeichen).**
- Optional Text-to-Speech pro Karte: Karten beginnen bei 1,5 / 3,7 / 5,9 / 8,1 / 10,3 s, Schluss bei 12,5 s
  (mit Stempeln: 1,5 / 4,1 / 6,7 / 9,3 / 11,9 s, Schluss 14,5 s).
- Urheberrechts-Prüfung des Sounds in den Post-Optionen einschalten.

## Lieferung an den Nutzer

Dateien in Posting-Reihenfolge benennen (`01-Mo-08-Video-….mp4`, Karussells als Ordner mit `slide-1…7.png`)
und als ZIP liefern; dazu pro Post Termin, Caption, Hashtags, anzupinnender Kommentar.

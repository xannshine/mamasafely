"""Inhalte 28.11.–07.12.2026: 13 neue Videos + 6 Karussells (+ Video „Baby satt“ vom 22.11.)."""
F = ["#A8D8F0", "#FDE68A", "#FFCBA4", "#A8E6CF", "#D4A5E8"]

def k(titel, text, icon, stempel=None):
    return {"titel": titel, "text": text, "icon": icon, **({"stempel": stempel} if stempel else {})}

def video(thema, kicker, hook, teaser, hl, karten, frage, unter, speichern, chips=True, mark=None):
    for i, c in enumerate(karten): c["farbe"] = F[i]
    d = dict(thema=thema, kicker=kicker, hook=hook, teaser=teaser, highlight=hl, karten=karten,
             frage=frage, unterzeile=unter, speichern=speichern, zahlen_chips=chips)
    if mark: d["mark_groesse"] = mark
    return d

def s(titel, icon, punkte, notiz, hinweis=None):
    return {"titel": titel, "icon": icon, "punkte": punkte, "notiz": notiz, **({"hinweis": hinweis} if hinweis else {})}

def karussell(kicker, titel, icon, teaser, slides, schluss):
    for i, x in enumerate(slides): x["farbe"] = F[i]
    return {"cover": dict(kicker=kicker, titel=titel, icon=icon, teaser=teaser), "slides": slides, "schluss": schluss}

M = lambda t: f'<span class="mark">{t}</span>'
Y = lambda t: f'<span class="mark yel">{t}</span>'

VIDEOS = {
"papa-teil3": video("Für Papas · Teil 3", "FÜR PAPAS · TEIL 3", ["{5} Dinge,", "die Papas", "unterschätzen", ""],
  "Nr. 3 sagt dir keiner", 3, [
    k("Papa kann genauso trösten", "Tragen und deine tiefe Stimme beruhigen", "voice"),
    k("Wickeln & Baden übernehmen", "so wachst ihr zusammen", "babyface"),
    k("Auch Papas bekommen Blues", "auch Väter können eine Wochenbettdepression bekommen", "heart"),
    k("Partnermonate nutzen", "Elterngeld gibt’s länger, wenn beide pausieren", "hand"),
    k("Besuch managen", "du entscheidest mit, wer wann kommt", "flower")],
  ["Schick das", "dem Papa!"], "Welcher Punkt passt bei euch?", "Speichern – für euch beide", mark=100),
"hungerzeichen": video("Hat mein Baby Hunger?", "STILLEN · ERSTE WOCHEN", ["{5} Zeichen,", "dass dein", "Baby Hunger", "hat"],
  "Nr. 5 ist schon spät!", 5, [
    k("Schmatzen & Lippen lecken", "eins der ersten, leisen Hungerzeichen", "cup"),
    k("Kopf dreht sich suchend", "der Suchreflex – Mund weit offen", "babyface"),
    k("Händchen zum Mund", "es nuckelt an Faust oder Fingern", "hand"),
    k("Unruhe & Strampeln", "es wird quengelig und zappelig", "feet"),
    k("Weinen", "ein spätes Zeichen – erst beruhigen, dann anlegen", "voice")],
  ["Welches zeigt", "dein Baby?"], "Nummer in die Kommentare:", "Speichern – für die Stillzeit"),
"uebelkeit": video("Wann hört die Übelkeit auf?", "SCHWANGERSCHAFT · WOCHE FÜR WOCHE", ["Wann hört", "die", "Übelkeit", "auf?"],
  "Nr. 5 musst du kennen!", 5, [
    k("Ca. 6. SSW: es geht los", "oft morgens – kann aber den ganzen Tag sein", "cup"),
    k("Ca. 8.–10. SSW: am stärksten", "bei vielen ist es jetzt am schlimmsten", "flame"),
    k("Ca. 12.–14. SSW: es wird besser", "bei den meisten lässt es spürbar nach", "heart"),
    k("Kleine Snacks helfen", "lieber oft wenig essen – und viel trinken", "carrot"),
    k("Nichts bleibt drin?", "kein Essen, kein Trinken: bitte zur Ärztin", "drop")],
  ["Wie war es", "bei dir?"], "Schreib deine SSW in die Kommentare", "Speichern – für deine Schwangerschaft", chips=False),
"mythen-teil5": video("Schwangerschafts-Mythen · Teil 5", "MYTHOS ODER WAHRHEIT? TEIL 5", ["{5} Mythen, die", "fast jede", "Schwangere", "hört"],
  "Nr. 5 stimmt wirklich!", 5, [
    k("„Du musst für zwei essen“", "erst später etwas mehr – nicht doppelt so viel", "carrot", "MYTHOS"),
    k("„Der Bauch verrät das Geschlecht“", "die Form hängt von Muskeln und Lage ab", "babyface", "MYTHOS"),
    k("„Kaffee ist komplett verboten“", "bis ca. 200 mg Koffein am Tag gelten als okay", "cup", "MYTHOS"),
    k("„Nicht die Arme über den Kopf“", "das schadet der Nabelschnur nicht", "hand", "MYTHOS"),
    k("„Folsäure früh nehmen“", "am besten schon vor der Schwangerschaft", "heart", "STIMMT!")],
  ["Welchen hast du", "geglaubt?"], "Nummer in die Kommentare:", "Speichern – für deine Schwangerschaft"),
"babybad": video("Babys erstes Bad", "BABYPFLEGE · ERSTE WOCHEN", ["{5} Tipps", "fürs erste", "Babybad", ""],
  "Nr. 3 ist ein Muss!", 3, [
    k("1–2 Mal pro Woche reicht", "öfter trocknet die zarte Haut aus", "drop"),
    k("Wasser ca. 37 °C", "mit dem Badethermometer prüfen", "flame"),
    k("Nie allein lassen", "auch nicht kurz – Baby immer festhalten", "hand"),
    k("5–10 Minuten genügen", "danach gut abtrocknen, auch in den Falten", "babyface"),
    k("Ohne Badezusatz", "in den ersten Wochen reicht klares Wasser", "flower")],
  ["Badet dein Baby", "gerne?"], "Erzähl’s uns in den Kommentaren", "Speichern – fürs erste Bad", chips=False),
"warnzeichen-wochenbett": video("Warnzeichen im Wochenbett", "WOCHENBETT · WICHTIG", ["{5} Zeichen", "im", "Wochenbett", "ernst nehmen"],
  "Nr. 5 kennen viele nicht", 5, [
    k("Fieber über 38 °C", "dann Hebamme oder Ärztin anrufen", "flame"),
    k("Plötzlich sehr starke Blutung", "oder große Klumpen – sofort Hilfe holen", "drop"),
    k("Wochenfluss riecht übel", "kann auf eine Entzündung hinweisen", "flower"),
    k("Rote, harte Stelle an der Brust", "mit Fieber – oft eine Brustentzündung", "heart"),
    k("Geschwollene, schmerzende Wade", "kann eine Thrombose sein – abklären lassen", "feet")],
  ["Schick das einer", "Schwangeren!"], "Lieber einmal zu viel anrufen!", "Speichern – fürs Wochenbett", chips=False),
"ab-wann-laecheln": video("Ab wann lächelt mein Baby?", "BABYS ERSTES JAHR", ["Ab wann", "lächelt", "dein Baby?", ""],
  "Nr. 2 ist so süß!", 2, [
    k("Ab Geburt: im Schlaf", "das „Engelslächeln“ – noch ein Reflex", "moon"),
    k("Ca. 6.–8. Woche: echtes Lächeln", "dein Baby lächelt dich bewusst an", "babyface"),
    k("Ca. 3–4 Monate: erstes Lachen", "richtiges Glucksen und Quietschen", "voice"),
    k("Lächle zurück!", "Blickkontakt und Mimik fördern das", "eye"),
    k("Jedes Baby hat sein Tempo", "Fragen? Bei der U-Untersuchung ansprechen", "heart")],
  ["Wann hat deins", "gelächelt?"], "Schreib’s in die Kommentare", "Speichern – fürs erste Jahr", chips=False),
"vor-der-geburt": video("Vor der Geburt erledigen", "SCHWANGERSCHAFT · TO-DO", ["{5} Dinge, die", "du vor der", "Geburt", "erledigst"],
  "Nr. 1 unbedingt früh!", 1, [
    k("Hebamme suchen", "für die Nachsorge – Plätze sind oft knapp", "heart"),
    k("Kinderarzt aussuchen", "früh fragen, ob die Praxis neue Babys nimmt", "doc"),
    k("In der Klinik anmelden", "viele Kliniken wünschen das vorher", "bag"),
    k("Babyschale einbauen üben", "vor der Heimfahrt einmal ausprobieren", "carseat"),
    k("Elternzeit anmelden", "spätestens 7 Wochen vor Beginn beim Arbeitgeber", "hand")],
  ["Was hast du", "vergessen?"], "Nummer in die Kommentare:", "Speichern – für deine To-do-Liste"),
"baby-schreit": video("Wenn das Baby schreit", "BABY BERUHIGEN", ["{5} Dinge, die", "helfen, wenn", "dein Baby", "schreit"],
  "Nr. 5 ist am wichtigsten", 5, [
    k("Hunger, Windel, Wärme?", "erst die Grundbedürfnisse checken", "cup"),
    k("Nah am Körper tragen", "Wärme und Herzschlag beruhigen", "heart"),
    k("Sanft wiegen", "ruhige, gleichmäßige Bewegungen", "moon"),
    k("Leises „Schhh“", "gleichmäßiges Rauschen erinnert an den Bauch", "voice"),
    k("Nie schütteln – Pause machen", "Baby sicher ablegen, rausgehen, durchatmen", "hand")],
  ["Was hilft", "bei euch?"], "Nummer in die Kommentare:", "Speichern – für harte Nächte"),
"nabelpflege": video("Nabelpflege", "BABYPFLEGE · ERSTE TAGE", ["{5} Dinge", "zum", "Nabel", "deines Babys"],
  "Bei Nr. 5 aufpassen!", 5, [
    k("Sauber & trocken halten", "das ist die wichtigste Pflege", "drop"),
    k("Windel umklappen", "so bekommt der Nabel Luft", "babyface"),
    k("Fällt von allein ab", "meist nach ca. 5–15 Tagen", "flower"),
    k("Nicht daran ziehen", "auch wenn er schon locker ist", "hand"),
    k("Rot, nässt oder riecht?", "dann Hebamme oder Kinderarzt fragen", "eye")],
  ["Wann fiel er", "bei euch ab?"], "Schreib’s in die Kommentare", "Speichern – für die ersten Tage", chips=False),
"was-sieht-baby": video("Was sieht mein Baby?", "BABYS ERSTES JAHR", ["Was sieht", "dein Baby", "wirklich?", ""],
  "Nr. 5 kennen wenige", 5, [
    k("Ab Geburt: ca. 20–30 cm scharf", "genau bis zu deinem Gesicht", "eye"),
    k("Starke Kontraste", "Schwarz-Weiß fällt am meisten auf", "flower"),
    k("Ca. 2–3 Monate: folgt mit Blick", "es verfolgt Gesichter und Spielzeug", "babyface"),
    k("Ca. 4 Monate: mehr Farben", "jetzt sieht es Farben deutlich besser", "heart"),
    k("Schielen am Anfang?", "gelegentlich normal – ständig? Kinderarzt fragen", "eye")],
  ["Erkennt es", "dich schon?"], "Schreib’s in die Kommentare", "Speichern – fürs erste Jahr", chips=False),
"still-mythen": video("Still-Mythen", "MYTHOS ODER WAHRHEIT? STILLEN", ["{5} Mythen", "übers", "Stillen", ""],
  "Nr. 4 stimmt wirklich!", 4, [
    k("„Kleine Brüste, wenig Milch“", "die Größe sagt nichts über die Milchmenge", "heart", "MYTHOS"),
    k("„Stillen muss wehtun“", "starke Schmerzen? Anlegen mit Hebamme prüfen", "hand", "MYTHOS"),
    k("„Stillen ist sichere Verhütung“", "nicht zuverlässig – Verhütung früh besprechen", "doc", "MYTHOS"),
    k("„Muttermilch hat Abwehrstoffe“", "sie schützt dein Baby vor manchen Infekten", "drop", "STIMMT!"),
    k("„Malzbier bringt mehr Milch“", "häufiges Anlegen bringt viel mehr", "cup", "MYTHOS")],
  ["Welchen hast du", "gehört?"], "Nummer in die Kommentare:", "Speichern – für die Stillzeit"),
"beikostreife": video("Bereit für Brei?", "BABYS ERSTES JAHR · BEIKOST", ["{5} Zeichen", "für die", "Beikostreife", ""],
  "Nr. 3 ist entscheidend", 3, [
    k("Frühestens ab dem 5. Monat", "spätestens zu Beginn des 7. Monats", "babyface"),
    k("Hält den Kopf sicher", "und sitzt mit etwas Unterstützung", "heart"),
    k("Zeigt Interesse am Essen", "guckt mit, greift zu, öffnet den Mund", "eye"),
    k("Schiebt Brei nicht mehr raus", "der Zungenstoß-Reflex lässt nach", "carrot"),
    k("Hand zum Mund klappt", "es führt Dinge gezielt zum Mund", "hand")],
  ["Wann gab’s den", "ersten Brei?"], "Schreib’s in die Kommentare", "Speichern – für später", chips=False, mark=100),
}

KARUSSELLS = {
"antraege-nach-geburt": karussell("NACH DER GEBURT · PAPIERKRAM", f"Das musst du nach der Geburt {M('beantragen:')}", "doc",
  "Bei Nr. 4 Frist beachten!", [
    s("Geburtsurkunde", "doc", ["Geburt beim Standesamt anzeigen", "Innerhalb von einer Woche", "Das übernehmen oft die Kliniken"], "Du brauchst sie für fast alle anderen Anträge."),
    s("Krankenkasse", "heart", ["Baby familienversichern", "Geburtsurkunde mitschicken", "Dann kommt die Versichertenkarte"], "Frag deine Kasse, welche Unterlagen sie braucht."),
    s("Kindergeld", "hand", ["Antrag bei der Familienkasse", "Steuer-ID des Babys nötig", "Die kommt automatisch per Post"], "Der Antrag geht auch online."),
    s("Elterngeld", "babyface", ["Antrag bei der Elterngeldstelle", "Nur 3 Monate rückwirkend!", "Früh planen, wer wann zu Hause ist"], "In vielen Bundesländern auch online möglich.", "Frist beachten!"),
    s("Arbeitgeber", "bag", ["Geburtsurkunde für den Mutterschutz", "Elternzeit rechtzeitig anmelden", "Mutterschaftsgeld über die Kasse"], "Elternzeit spätestens 7 Wochen vor Beginn anmelden.")],
  dict(titel=f"Alles {Y('erledigt?')}", text="Zuerst die Geburtsurkunde – der Rest baut darauf auf.",
       tipp="<b>Tipp:</b> Leg dir eine Mappe für alle Papiere an – das spart Nerven.",
       teilen="Schick das frischen Eltern", quelle="Quelle: familienportal.de · Stand 2026, ohne Gewähr")),
"wickeltasche": karussell("UNTERWEGS MIT BABY · CHECKLISTE", f"Das gehört in die {M('Wickeltasche:')}", "bag",
  "Nr. 5 vergessen viele!", [
    s("Fürs Wickeln", "drop", ["Windeln – lieber ein paar mehr", "Feuchttücher oder Waschlappen", "Faltbare Wickelunterlage"], "Wundschutzcreme nicht vergessen."),
    s("Kleidung", "babyface", ["Ein komplettes Wechsel-Outfit", "Mütze – je nach Wetter", "Spucktuch (oder zwei)"], "Ein Wechselshirt für dich schadet auch nicht."),
    s("Essen & Trinken", "cup", ["Stilltuch oder Fläschchen", "Portioniertes Milchpulver", "Wasser und Snack für dich"], "Stillen macht unterwegs schnell durstig."),
    s("Kleine Helfer", "hand", ["Beutel für volle Windeln", "Desinfektion für die Hände", "Schnuller, falls ihr einen nutzt"], "Ein kleines Spielzeug lenkt beim Wickeln ab."),
    s("Wichtiges", "doc", ["Gelbes Heft & Versichertenkarte", "Handy und Powerbank", "Wichtige Telefonnummern"], "Pack alles in eine extra Innentasche.", "Vergessen viele!")],
  dict(titel=f"Was fehlt {Y('noch?')}", text="Nach jedem Ausflug direkt wieder auffüllen.",
       tipp="<b>Tipp:</b> Eine Ersatzwindel und Tücher zusätzlich im Auto lagern – das rettet so manchen Tag.",
       teilen="Schick das einer Schwangeren", quelle="")),
"babyschale-auto": karussell("SICHER IM AUTO · ZUM SPEICHERN", f"So fährt dein Baby {M('sicher mit:')}", "carseat",
  "Nr. 3 machen viele falsch!", [
    s("Richtig herum", "carseat", ["Babyschale gegen die Fahrtrichtung", "Am sichersten auf der Rückbank", "Fest eingebaut, nichts wackelt"], "Bei Isofix auf die grüne Anzeige achten."),
    s("Beifahrersitz?", "eye", ["Nur mit ausgeschaltetem Airbag", "Airbag-Anzeige vor jeder Fahrt prüfen", "Sonst lieber hinten"], "Ein aktiver Airbag ist für Babyschalen lebensgefährlich."),
    s("Gurte eng", "hand", ["Höchstens eine flache Hand Platz", "Gurte auf Schulterhöhe einstellen", "Keine dicke Jacke unter dem Gurt"], "Lieber eine Decke über den Gurt legen.", "Häufiger Fehler!"),
    s("Pausen machen", "moon", ["Bei langen Fahrten regelmäßig halten", "Baby zwischendurch rausnehmen", "Atmung & Wärme im Blick behalten"], "Die Babyschale ist kein Schlafplatz für zu Hause."),
    s("Einbau üben", "babyface", ["Vor der Geburt einmal einbauen", "Anleitung im Auto aufbewahren", "Bei Unsicherheit beraten lassen"], "Viele Fachhändler zeigen dir den Einbau.")],
  dict(titel=f"Alles {Y('gecheckt?')}", text="Die Babyschale muss zu Größe und Gewicht deines Babys passen.",
       tipp="<b>Tipp:</b> Achte auf die Norm i-Size (R129) – und kauf gebraucht nur unfallfrei.",
       teilen="Schick das werdenden Eltern", quelle="")),
"hebamme-wochenbett": karussell("WOCHENBETT · ZUM SPEICHERN", f"Das macht deine Hebamme im {M('Wochenbett:')}", "heart",
  "Nr. 5 wissen viele nicht!", [
    s("Wann sie kommt", "doc", ["Hausbesuche nach der Geburt", "Anspruch bis 12 Wochen danach", "Die Krankenkasse zahlt"], "Mit ärztlicher Verordnung auch länger."),
    s("Check bei dir", "heart", ["Gebärmutter & Wochenfluss", "Naht oder Kaiserschnittnarbe", "Kreislauf & Wohlbefinden"], "Sag ihr ehrlich, wie es dir geht."),
    s("Check beim Baby", "babyface", ["Gewicht & Trinken", "Nabel & Haut (z. B. Gelbsucht)", "Atmung & Verhalten"], "Sie wiegt dein Baby regelmäßig."),
    s("Stillen & Füttern", "cup", ["Hilfe beim richtigen Anlegen", "Tipps bei wunden Brustwarzen", "Beratung auch zur Flasche"], "Stillprobleme? Sprich sie früh an."),
    s("Für deine Seele", "voice", ["Zuhören bei Sorgen & Tränen", "Baby Blues oder mehr? Sie schaut hin", "Vermittelt weiter, wenn nötig"], "Auch Fragen vom Partner sind willkommen.", "Wissen viele nicht!")],
  dict(titel=f"Noch keine {Y('Hebamme?')}", text="Am besten schon früh in der Schwangerschaft suchen.",
       tipp="<b>Tipp:</b> Keine gefunden? Frag bei deiner Krankenkasse oder der Geburtsklinik nach.",
       teilen="Schick das einer Schwangeren", quelle="Quelle: Leistungen der gesetzlichen Krankenkassen")),
"baby-hausapotheke": karussell("BABYS ERSTES JAHR · CHECKLISTE", f"Die {M('Hausapotheke')} fürs Baby:", "drop",
  "Nr. 5 unbedingt merken!", [
    s("Fieberthermometer", "flame", ["Digital – am besten für den Po", "Bei Babys am genauesten", "Nach jedem Messen reinigen"], "Im Ohr messen ist bei Babys oft ungenau."),
    s("Für die Nase", "voice", ["Kochsalz-Nasentropfen", "Sanfter Nasensauger", "Abschwellende Tropfen nur nach Rat"], "Für Babys gibt es eigene, niedrig dosierte Mittel."),
    s("Für die Haut", "flower", ["Wundschutzcreme für den Po", "Kinderpflaster & Kompressen", "Milde, parfümfreie Pflege"], "Babyhaut ist dünn – weniger ist mehr."),
    s("Fiebermittel", "doc", ["Nur speziell für Babys", "Dosis nach Gewicht – nie schätzen", "Vorher mit Kinderarzt besprechen"], "Frag bei der U-Untersuchung, was ihr haben solltet."),
    s("Wichtige Nummern", "heart", ["Kinderarzt & Hebamme", "Ärztlicher Bereitschaftsdienst 116 117", "Notruf 112 & Giftnotruf deiner Region"], "Baby unter 3 Monaten mit Fieber ab 38 °C: sofort zum Arzt.", "Unbedingt merken!")],
  dict(titel=f"Alles {Y('da?')}", text="Ablaufdaten regelmäßig prüfen.",
       tipp="<b>Tipp:</b> Leg einen Zettel mit allen Nummern und dem aktuellen Gewicht deines Babys dazu.",
       teilen="Schick das frischen Eltern", quelle="Im Zweifel immer Kinderarzt oder Hebamme fragen.")),
"nach-kaiserschnitt": karussell("NACH DEM KAISERSCHNITT", f"Das hilft dir nach dem {M('Kaiserschnitt:')}", "heart",
  "Nr. 1 unterschätzen viele!", [
    s("Früh aufstehen", "feet", ["Mit Hilfe, sobald es erlaubt ist", "Bewegung beugt Thrombosen vor", "Langsam – erst sitzen, dann stehen"], "Lass dir beim ersten Mal helfen.", "Unterschätzen viele!"),
    s("Die Narbe", "flower", ["Sauber und trocken halten", "Weite Hose, nichts drückt", "Rot, warm oder nässt? Abklären"], "Die Hebamme schaut sie sich mit an."),
    s("Schmerzmittel", "doc", ["Wie verordnet einnehmen", "Viele sind stillverträglich", "Schmerzfrei bewegst du dich besser"], "Frag nach, was beim Stillen passt."),
    s("Schonen", "hand", ["Nichts Schweres heben", "Faustregel: nicht mehr als dein Baby", "Sport erst nach Absprache"], "Zum Aufstehen über die Seite rollen."),
    s("Hilfe annehmen", "babyface", ["Partner übernimmt Haushalt & Tragen", "Stillkissen schützt die Narbe", "Besuch ruhig begrenzen"], "Dein Körper hatte eine große OP – sei geduldig.")],
  dict(titel=f"Du schaffst {Y('das!')}", text="Die Narbe heilt oft in wenigen Wochen – innen dauert es länger.",
       tipp="<b>Tipp:</b> Ein Kissen fest auf den Bauch drücken hilft beim Husten oder Lachen.",
       teilen="Schick das einer Schwangeren", quelle="Bei Fragen: Hebamme oder Frauenärztin")),
}

if __name__ == "__main__":
    import json, os, sys
    out = sys.argv[1]
    for n, d in VIDEOS.items():
        os.makedirs(f"{out}/{n}", exist_ok=True); json.dump(d, open(f"{out}/{n}/spec.json", "w"), ensure_ascii=False, indent=2)
    for n, d in KARUSSELLS.items():
        os.makedirs(f"{out}/{n}", exist_ok=True); json.dump(d, open(f"{out}/{n}/spec.json", "w"), ensure_ascii=False, indent=2)
    print(len(VIDEOS), len(KARUSSELLS))

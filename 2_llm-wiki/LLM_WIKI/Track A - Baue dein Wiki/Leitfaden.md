# Leitfaden: Spiel mit einem echten LLM-Wiki

Hier liegt ein **fertiges LLM-Wiki** zur fiktiven Marsmission **Ares-7**, gebaut nach
Andrej Karpathys Pattern. Du musst nichts vorbereiten: Lies, frag, füttere es mit
neuen Quellen und schau zu, wie das LLM das Wiki pflegt. Mehr Hintergrund steht in
der [[Track A - Baue dein Wiki/README|README]].

**Die Rollen:** Obsidian ist die IDE, das LLM ist der Programmierer, das Wiki ist
der Codebase. Du kuratierst Quellen und stellst Fragen – das LLM macht die
Buchhaltung.

## 0. Vorher: Assistent richtig einstellen

- Im Copilot-Chat oben das Projekt-Dropdown öffnen und **„Ares-7 LLM-Wiki (Track A)"**
  wählen. Taucht das Projekt nicht auf: Obsidian einmal neu laden (`Strg+P` →
  „Reload app without saving“).
- Der Copilot-Chat (Symbol in der Seitenleiste) arbeitet als Agent: Er kann das Wiki
  lesen und auch selbst schreiben. Das braucht ihr für **Ingest und Lint**.

## 1. Schau dir das Wiki an (5 Min.)

- Öffne [[ares-index]] – den Katalog. Von dort aus klickst du dich durch.
- Lies [[ares-overview]] – die Synthese: Was ist gesichert, was ist offen?
- Öffne den **Graph** (`Strg+G` oder Graph-Symbol in der linken Seitenleiste) und
  filtere mit `path:"Track A"`. Du siehst die Hubs und wie dicht alles verlinkt ist.
  Die Farben zeigen die Schichten: **gelb** = Index/Übersicht/Log/Lint,
  **blau** = Quellen-Zusammenfassungen, **orange** = Entitäten, **grün** = Konzepte,
  **pink** = Analysen & Widersprüche. (Die Rohquellen in `raw/` tauchen nicht auf –
  sie werden nur zitiert, nicht verlinkt.)
- Schau in den Ordner `raw/` und vergleiche: So sehen Rohquellen aus – und so
  die kompilierten Seiten in `wiki/`.

## 2. Query: Stell Fragen

- *„Wer ist aktuell Pilot von Ares-7?"* → Achte darauf, ob „veraltet" erkannt wird.
- *„Wie lange dauert die Mission?"* → Benennt der Assistent den offenen Widerspruch?
- *„Wann startet Ares-7?"* → Erklärt er, warum „in 24 Monaten" nicht mehr gilt?
- *„Wie heißt die Hündin der Crew?"* → Sagt er ehrlich „steht nicht im Wiki"?

**Bonus:** Wenn eine Antwort gut ist, sag: *„File diese Antwort zurück ins Wiki."*
Dann entsteht eine neue Seite unter `comparisons/`.

## 3. Ingest: Füttere das Wiki

Spiel die drei Übungsquellen **einzeln** und **in dieser Reihenfolge** ein. Die
Reihenfolge ist Absicht: Der Forenbeitrag ist erst nach der Statusmeldung
richtig knifflig.

| # | Datei | Vorher anschauen und merken |
|---|---|---|
| 1 | `2026-09-30-missionsprofil-detail.md` | Status in [[widerspruch-missionsdauer]] („offen") und wer laut [[kestrel]] mit Tanaka landet („nicht belegt") |
| 2 | `2026-10-01-statusmeldung-lebenserhaltung.md` | Die Reserve in [[analyse-reserve-lebenserhaltung]] („ca. 4 Monate") |
| 3 | `2026-10-01-forenbeitrag-verschiebung.md` | Das Startfenster in [[missionszeitplan]] (Nov./Dez. 2028) |

**Warum vorher anschauen?** Obsidian zeigt dir nicht an, was sich geändert hat. Wenn
du dir den alten Stand nicht merkst, siehst du nach dem Ingest keinen Unterschied.

Für jede Quelle:

1. Zieh die Datei im Dateibaum aus `uebungsquellen/` in den Ordner `raw/`.
2. Sag dem Assistenten: *„Verarbeite die neue Quelle in raw/."*
3. Prüf mit der Checkliste, ob der Ingest vollständig war.

**Checkliste: War der Ingest gut?**

- [ ] Unter `wiki/sources/` gibt es eine **neue Zusammenfassungsseite**.
- [ ] [[ares-log]] hat einen **neuen Eintrag**, der die geänderten Seiten auflistet
      (es sollten mehrere sein, nicht nur die neue).
- [ ] [[ares-index]] verlinkt die neue Seite.
- [ ] Die Seite, die du dir vorher gemerkt hast, hat sich **passend** geändert:
  - nach 1: Widerspruch **geklärt**, die Erklärung ist weiterhin sichtbar; die
    Landecrew ist belegt.
  - nach 2: Reserve **neu gerechnet**; die 30 Monate sind als **veraltet**
    markiert, aber nicht gelöscht.
  - nach 3: Das offizielle Startfenster **steht noch**; der Beitrag ist als
    **unbestätigt** markiert.
- [ ] Die Datei in `raw/` ist **unverändert**.

Fehlt etwas, sag es dem Assistenten, z. B.: *„Du hast [[ares-log]] nicht
aktualisiert."* Auch das gehört zum Kuratieren.

## 4. Lint: Lass das Wiki aufräumen

- Lies zuerst [[ares-lint]] und merk dir die offenen Punkte. Der Lint überschreibt
  die Seite.
- Sag: *„Mach einen Lint-Durchgang."*
- Vergleiche mit deinem Vorher-Stand: Wurden Lücken geschlossen? Sind neue
  aufgetaucht? Was davon hat sich durch deine Ingests erledigt?

## 5. Fordere das System heraus

- Frag etwas, das in keiner Quelle steht.
- Stell eine suggestive Frage („Warum wurde die Mission auf 2031 verschoben?").
- Lass dir zu einer Aussage die **Rohquelle** zeigen und prüfe sie selbst.
- Prüfe, ob der Assistent eine eigene Rechnung als „Hypothese" kennzeichnet.

## 6. Optional: Eigenes Wiki

Lieber ein eigenes Thema?

1. Leg auf oberster Ebene des Vaults einen neuen Ordner an, z. B. `Mein Wiki - Startup`,
   und darin einen leeren Ordner `raw/`.
2. Kopiere die [[Schema-Vorlage]] in deinen Ordner und benenne sie in `AGENTS.md` um.
   **Nicht** die AGENTS.md aus Track A nehmen: Die ist auf Ares-7 zugeschnitten
   und würde z. B. ein zweites `ares-index.md` anlegen.
3. Wirf 3–5 Quellen in `raw/`. Ideen gibt es in den
   [[Beispiel-Themenpakete/README|Beispiel-Themenpaketen]].
4. Wähl im Copilot-Chat das Projekt **„Ares-7 LLM-Wiki (Track A)" ab**. Es sieht nur
   den Track-A-Ordner. Bleib im **Agent-Modus**.
5. Sag (mit deinem Ordnernamen): *„Initialisiere ein LLM-Wiki nach dem Schema in
   `Mein Wiki - Startup/AGENTS.md` und ingeste alle Quellen in
   `Mein Wiki - Startup/raw/`."*

Wenn dir nichts mehr einfällt: schau in die [[Challenge Cards]].

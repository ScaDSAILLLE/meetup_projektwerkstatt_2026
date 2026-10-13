# ares-log.md — Chronologisches Protokoll

Append-only. Jeder Eintrag beginnt mit einem konsistenten Präfix, damit die Datei
z. B. mit `grep "^## \[" ares-log.md | tail -5` parsebar bleibt.

## [2026-06-15] init | Wiki angelegt
Drei Schichten eingerichtet: `raw/` (4 Quellen), `wiki/` (leer), `AGENTS.md` (Schema).
Struktur nach Karpathys LLM-Wiki-Pattern.

## [2026-06-15] ingest | batch (4 Quellen)
Alle vier Rohquellen in `raw/` aufgenommen und kompiliert:
- 2026-03-10-missionsbriefing.md
- 2026-04-02-crew-bekanntgabe.md
- 2026-05-20-datenblatt-halcyon.md
- 2026-06-12-risikobericht.md

Erstellt: 4 Quellenzusammenfassungen, 11 Entitätsseiten, 6 Konzeptseiten,
1 Vergleich. Widerspruch bei der Missionsdauer erkannt und dokumentiert.
`ares-index.md` angelegt.

## [2026-06-15] lint | erster Durchgang
Ergebnis siehe [[ares-lint]]. Offen: Missionsdauer, Strahlenschutz-Lücke,
fehlende Angaben zur Lande-/Orbitcrew.

## [2026-07-10] ingest | Interview Yuki Tanaka
Neue Quelle `raw/2026-07-08-interview-tanaka.md` aufgenommen.
Betroffene Seiten aktualisiert (9):
- neu: [[quellen-interview-tanaka]], [[widerspruch-startdatum]] (neuer Widerspruch:
  „in 24 Monaten" vs. „Ende 2028")
- aktualisiert: [[yuki-tanaka]], [[kestrel]] (Landecrew), [[halcyon]] (Schutzraum),
  [[strahlenschutz]], [[crew-training]], [[widerspruch-missionsdauer]]
  („10 Tage" = Oberfläche), `ares-index.md`

## [2026-07-10] query | Reicht die Lebenserhaltung?
Antwort aus [[lebenserhaltung]], [[missionsrisiken]], [[missionszeitplan]]
synthetisiert und als [[analyse-reserve-lebenserhaltung]] zurück ins Wiki gefiled.
Neuer Zusammenhang: Bei verpasstem Rückflugfenster reicht die Auslegung nicht.

## [2026-09-16] ingest | Crew-Änderung
Neue Quelle `raw/2026-09-15-crew-aenderung.md` aufgenommen.
Betroffene Seiten aktualisiert (9):
- neu: [[quellen-crew-aenderung]]
- aktualisiert: [[elena-vasquez]] (Status: CAPCOM), [[kofi-mensah]] (Pilot),
  [[ares-7]], [[kestrel]], [[yuki-tanaka]], [[quellen-crew-bekanntgabe]] und
  [[quellen-interview-tanaka]] (Vasquez-Angaben als **veraltet** markiert),
  `ares-index.md`
Rohquellen unverändert.

## [2026-09-29] ingest | Festlegung des Startfensters
Neue Quelle `raw/2026-09-28-startfenster.md` aufgenommen.
Betroffene Seiten aktualisiert (8):
- neu: [[quellen-startfenster]]
- aktualisiert: [[widerspruch-startdatum]] (Status **geklärt**), [[missionszeitplan]],
  [[ares-7]], [[quellen-missionsbriefing]] („24 Monate" als veraltet markiert),
  [[widerspruch-missionsdauer]] (26 Monate bestätigt, Lücke bleibt),
  [[ares-overview]], `ares-index.md`

## [2026-09-29] lint | zweiter Durchgang
Ergebnis siehe [[ares-lint]]. Startdatum geklärt; Missionsdauer weiter offen;
neue Lücke: Wer landet nach der Crew-Änderung mit Tanaka?

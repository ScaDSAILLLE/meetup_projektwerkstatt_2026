# Schema-Vorlage für ein eigenes LLM-Wiki

> **So benutzt du diese Vorlage:** Kopiere diese Datei in deinen Wiki-Ordner und
> benenne sie dort in `AGENTS.md` um. Ändern musst du nichts – das Präfix trägt der
> Agent beim Initialisieren selbst ein. (Diese Vorlage ist eine neutrale Fassung
> des Ares-7-Schemas aus [[Track A - Baue dein Wiki/AGENTS|Track A]].)

---

# Schema für dieses LLM-Wiki

Dieses Dokument ist die **Konfigurationsdatei des Wikis**. Es sagt dem LLM-Agenten,
wie das Wiki strukturiert ist und welchen Workflows er folgt. Mensch und LLM
entwickeln es gemeinsam weiter (Karpathys „schema"-Schicht).

**Thema:** _(trägt der Agent beim Initialisieren ein)_
**Präfix:** _(trägt der Agent beim Initialisieren ein: ein kurzes Kürzel aus dem
Thema, klein, ohne Umlaute, z. B. `startup` oder `rezepte`)_

Im Folgenden steht `PRAEFIX` für dieses Präfix.

## Die drei Schichten

- `raw/` — **Unveränderliche Rohquellen.** Der Agent liest sie, ändert sie aber
  **niemals**. Quelle der Wahrheit.
- `wiki/` — **Vom LLM gepflegte Markdown-Seiten.** Zusammenfassungen, Entitäts-,
  Konzept- und Vergleichsseiten, Übersicht. Der Agent schreibt, der Mensch liest.
- `AGENTS.md` — dieses Schema.

## Wiki-Struktur

```
wiki/
  PRAEFIX-index.md     Katalog aller Wiki-Seiten — zuerst lesen
  PRAEFIX-log.md       Chronologisches, append-only Protokoll aller Operationen
  PRAEFIX-overview.md  Verdichtete Synthese des gesamten Wikis
  PRAEFIX-lint.md      Ergebnis des letzten Lint-Durchgangs / offene Punkte
  sources/             Je eine Zusammenfassungsseite pro Rohquelle
  entities/            Personen, Organisationen, Orte, Dinge
  concepts/            Themen, Systeme, Prozesse
  comparisons/         Gegenüberstellungen, Analysen, Antworten auf Fragen
```

Die Meta-Dateien tragen das Präfix statt `index.md`/`log.md`, damit sie vault-weit
eindeutig bleiben. In diesem Vault gibt es bereits `ares-index.md` usw. aus Track A.

## Konventionen

- Sprache: Deutsch. Dateinamen auf `kleinbuchstaben-mit-bindestrich.md`,
  **keine Doppelpunkte, keine Umlaute** (Windows-Dateisystem).
- **Dateinamen vault-weit eindeutig.** Vor dem Anlegen prüfen, dass es den Namen
  im ganzen Vault nicht schon gibt (auch nicht in `Track A`, `Track B`, `Track C` oder
  `Beispiel-Themenpakete/`; Groß-/Kleinschreibung zählt nicht). Im Zweifel
  präzisieren oder das Präfix voranstellen, z. B. `PRAEFIX-produkt` statt `produkt`.
- Quellenzusammenfassungen heißen `quellen-PRAEFIX-<kurzname>.md`.
- Jede Wiki-Seite beginnt mit einem H1-Titel und einem kurzen Kopfblock im
  Fließtext (Typ, Status, Quellen, zuletzt aktualisiert).
- Verlinkung untereinander per `[[dateiname-ohne-endung]]`.
- Jede Aussage auf einer Wiki-Seite muss auf mindestens eine Rohquelle
  zurückführbar sein. Quellen als `[src: raw/datei.md]` kennzeichnen.
- Widersprüche werden **nicht geglättet**, sondern auf der betroffenen Seite
  unter `## Widersprüche` offen markiert, mit Verweis auf beide Quellen.
- Veraltete Aussagen (durch neuere Quelle überholt) bleiben sichtbar, werden
  aber als `(veraltet, siehe [src: ...])` gekennzeichnet.
- **Eigene Schlussfolgerungen** des Agenten (Rechnungen, Hypothesen) sind
  als solche zu kennzeichnen („Hypothese, nicht in Quellen belegt").
- **Quellenqualität** angeben: offizielle Dokumente vs. Interviews vs. unbestätigte
  Quellen (Foren, Gerüchte). Unbestätigtes überschreibt nie Bestätigtes.

## Operationen

### Initialisieren (einmalig)
1. Thema und Präfix oben in dieser Datei eintragen.
2. Ordner `wiki/` mit den Unterordnern und den vier `PRAEFIX-…`-Meta-Dateien anlegen.
3. Alle Dateien in `raw/` nacheinander ingesten (siehe unten).
4. Einen ersten Lint-Durchgang machen.

### Ingest
1. Neue Datei liegt in `raw/`; der Mensch bittet um Verarbeitung.
2. Der Agent liest die Quelle und nennt dem Menschen kurz die Kernpunkte.
3. Der Agent legt eine Zusammenfassungsseite in `wiki/sources/` an.
4. Der Agent aktualisiert **alle betroffenen** Entitäts-, Konzept-, Vergleichs- und
   Übersichtsseiten.
5. Der Agent markiert neue Widersprüche und überholte Aussagen und schließt
   geklärte Widersprüche (Status „geklärt", Erklärung bleibt sichtbar).
6. Der Agent aktualisiert `PRAEFIX-index.md`, `PRAEFIX-lint.md` und ergänzt einen
   Eintrag in `PRAEFIX-log.md` mit der Liste aller geänderten Seiten.

### Query
1. Der Agent liest zuerst `PRAEFIX-index.md`, dann die relevanten Seiten, und
   antwortet **mit Quellenangaben**.
2. Steht etwas nicht im Wiki, sagt der Agent das klar, statt zu raten oder im
   Web zu suchen.
3. Gute Antworten werden auf Wunsch als neue Seite unter `wiki/comparisons/`
   zurück ins Wiki gefiled.

### Lint
Der Agent sucht nach Widersprüchen, veralteten Aussagen, verwaisten Seiten (keine
eingehenden Links), fehlenden Seiten, fehlenden Querverweisen und Datenlücken.
Ergebnis in `PRAEFIX-lint.md`, Eintrag in `PRAEFIX-log.md`.

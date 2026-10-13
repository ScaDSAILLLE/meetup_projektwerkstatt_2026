# Track A: Das Ares-7-Wiki — ein fertiges LLM-Wiki zum Spielen

Dieser Ordner ist ein **fertig aufgebautes LLM-Wiki nach Andrej Karpathy** zu einer
fiktiven Marsmission, mit **vorbereiteten Übungsquellen**, mit denen du Ingest,
Query und Lint selbst ausprobierst.

Original-Idee: [Karpathys Gist „LLM Wiki"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Der Unterschied zu RAG in einem Satz

> RAG **holt** bei jeder Frage neu aus den Rohdokumenten. Ein LLM-Wiki
> **kompiliert** das Wissen einmal in verlinkte Markdown-Seiten und hält sie
> aktuell. Du liest und kuratierst – das LLM schreibt.

## Aufbau

```
Track A - Baue dein Wiki/
├── AGENTS.md              ← Schema: Struktur + Workflows (Ingest/Query/Lint)
├── README.md              ← diese Datei
├── Leitfaden.md           ← Schritt-für-Schritt zum Ausprobieren
├── Challenge Cards.md     ← Aufgaben, wenn dir nichts mehr einfällt
├── raw/                   ← 7 unveränderliche Rohquellen (bereits verarbeitet)
├── uebungsquellen/        ← 3 Quellen, die noch NICHT verarbeitet sind
└── wiki/                  ← vom LLM gepflegt
    ├── ares-index.md      ← Katalog (zuerst lesen!)
    ├── ares-log.md        ← Chronik aller Operationen
    ├── ares-overview.md   ← Synthese
    ├── ares-lint.md       ← Gesundheitscheck
    ├── sources/           ← je 1 Zusammenfassung pro Rohquelle
    ├── entities/          ← Mission, Schiff, Crew, Organisation
    ├── concepts/          ← Zeitplan, Lebenserhaltung, Risiken, …
    └── comparisons/       ← Widerspruchs- und Analyse-Seiten
```

Warum `ares-index.md` statt `index.md`? Damit die Namen im ganzen Vault eindeutig
bleiben, auch wenn du nebenan ein eigenes Wiki mit eigenem `index.md` baust
([[Leitfaden]], Schritt 6). Sonst wüsste Obsidian bei `[[index]]` nicht, welches gemeint ist.

## Die drei Operationen

**Ingest** — Datei aus `uebungsquellen/` nach `raw/` ziehen und dem Agenten sagen:
*„Verarbeite die neue Quelle in raw/."* Er legt eine Zusammenfassung an und
aktualisiert *alle* betroffenen Seiten, inklusive Widersprüchen, `ares-index.md`
und `ares-log.md`.

**Query** — Eine Frage stellen. Der Agent liest `ares-index.md`, dann die
passenden Seiten, und antwortet mit Quellen. Gute Antworten landen als neue
Seite unter `comparisons/`.

**Lint** — *„Mach einen Lint-Durchgang."* Der Agent prüft Widersprüche, veraltete
Aussagen, verwaiste Seiten und Lücken. Das Ergebnis steht in `ares-lint.md`.

## Eingebaute Reibungspunkte

| Punkt | Status im Wiki | Was ihn verändert |
|---|---|---|
| Missionsdauer **26 Monate** vs. Phasen ergeben nur **~16,5 Monate** | offen | Übungsquelle *Missionsprofil* |
| Start **„in 24 Monaten"** (März 2026) vs. **Ende 2028** | geklärt | — (Beispiel für eine Klärung) |
| **Elena Vasquez** als Pilotin | veraltet markiert | — (Beispiel für „veraltet") |
| Lebenserhaltung **30 Monate** → 4 Monate Reserve | Analyse | Übungsquelle *Statusmeldung Lebenserhaltung* |
| Gerücht: Mission auf **2031** verschoben | noch nicht im Wiki | Übungsquelle *Forenbeitrag* (unbestätigt!) |

Diese Punkte stehen bewusst *offen* im Wiki, statt geglättet zu werden – genau das
ist Karpathys Punkt.

## Die Übungsquellen

| Datei | Was beim Ingest passieren sollte |
|---|---|
| `2026-09-30-missionsprofil-detail.md` | Widerspruch Missionsdauer wird **geklärt**; Lande-/Orbitcrew wird belegt; viele Seiten ändern sich. |
| `2026-10-01-statusmeldung-lebenserhaltung.md` | Auslegung sinkt auf **28 Monate**; die Reserve-Analyse muss neu gerechnet werden; 30 Monate werden **veraltet**. |
| `2026-10-01-forenbeitrag-verschiebung.md` | Darf das offizielle Startfenster **nicht** überschreiben, sondern muss als **unbestätigt** eingeordnet werden. Test für Quellenkritik. |

Am meisten lernst du, wenn du sie **einzeln** und **in dieser Reihenfolge** einspielst
und nach jedem Ingest `ares-log.md` und den Graph anschaust.

# Fileservices – Änderungsauftrag CHG-5521

**Erstellt:** 03.10.2026 · **Wartungsfenster:** 09.10.2026, 18:00–22:00 · **Zuständig:** Nina Herbstlich, Tom Seidel

## Auftrag

Übertragung der Forschungs-Teamablagen von `FS-ALT` auf `FS-NEU` mit angepasstem Namespace. Teamnamen werden als Benutzeranzeigenamen nicht eins zu eins als technische Verzeichnisnamen geführt. Integritätskontrolle anhand Dateizahl und Prüfsummenstichprobe. Projektrollen werden in separatem Abgleich übernommen.

## Ablaufprotokoll

| Zeit | Schritt | Ergebnis |
|---|---|---|
| 17:43 | Snapshot Quellsystem | erstellt |
| 18:02 | Kopierlauf Batch 3 | gestartet |
| 18:37 | P-204 im Laufmanifest | 182 Einträge |
| 19:06 | Statusimport Register | Warnung für P-204 |
| 19:19 | Dateikopien / Hashprüfung | erfolgreich für Stichprobe |
| 19:24 | Rechteabgleich RD-041-B | offen |
| 20:11 | Test alter Teamlinks | mehrere Fehler |
| 20:19 | Storage-Abnahme | erfolgt |
| 21:42 | Übergabe offener Punkte an Service Desk | erfolgt |

**Abnahmefeld**  
Storage: Tom Seidel, 20:19 ✓  
Fachabnahme KERN: *kein Eintrag*  
Benutzerabnahme Projektleitung: *kein Eintrag*

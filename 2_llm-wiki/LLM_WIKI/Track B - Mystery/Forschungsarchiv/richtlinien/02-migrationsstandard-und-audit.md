# Betriebsstandard IT-07 – Migration von Teamablagen

**Version:** 3.1 · **Gültig ab:** 01.08.2026 · **Eigentümer:** IT Fileservices

## Ziel

Umstellung von Forschungs- und Teamablagen ohne Verlust fachlich benötigter Dokumente. Die Quellstruktur darf während des Wartungsfensters schreibgeschützt oder unerreichbar sein.

## Verbindliche Prüfschritte

| Phase | Zuständig | Mindestnachweis |
|---|---|---|
| 1. Vorbereitung | Fileservices | Inventarliste und Snapshot |
| 2. Übertragung | Fileservices | Manifest mit Quelle, Ziel, Dateizahl |
| 3. Integrität | Fileservices | Prüfsummenstichprobe und Fehlerliste |
| 4. Registerabgleich | PMO / Schnittstellenbetrieb | Anzeigename, Projektstatus und Zielzuordnung |
| 5. Berechtigungen | IAM | Gruppen und Rollen je Nutzer |
| 6. Benutzerabnahme | Fachbereich | Test mit tatsächlichem Projektkonto |

**Abschlussregel:** Ein erfolgreiches Kopierprotokoll allein schließt die fachliche Wiederinbetriebnahme nicht ab. Offene Register-, Rollen- oder Teamlink-Probleme bleiben bis zur Einzelprüfung als Tickets bestehen.

## Auditdaten

Dateioperationen, Benutzerzugriffe und technische Prüfläufe können in getrennten Systemen protokolliert werden. Ein Auszug ist mit Quelle und Zeitraum zu kennzeichnen. Bei Sicherheitsvorfällen sind Originalprotokolle zu sichern; das Betriebs-Team bearbeitet weiterhin die Wiederherstellung des Zugangs.

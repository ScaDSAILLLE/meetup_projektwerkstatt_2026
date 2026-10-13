# SEC-488 – Sicherheitsprüfung und Gesprächsnotizen

**Begonnen:** 10.10.2026, 10:30 · **Verantwortung:** Informationssicherheit

## Anlass

Nach Eingang von INC-2684 wurden die vorhandenen Zugriffsereignisse auf ungewöhnliche Dateioperationen geprüft. Die Fachabteilung hat auf den Konflikt um die Projektleitung hingewiesen; außerdem liegen Wartungsaktivitäten am Vorabend vor.

## Auditstichprobe

| Vorgang | Feststellung |
|---|---|
| Zugriff Alex Berger, 09.10. 16:41 | Datei `KERN_Review_v6.docx` geöffnet; kein Löschereignis im vorliegenden Auszug |
| Dienstkonto `svc-fs-move`, 09.10. ab 18:02 | großvolumige Dateibewegungen im angemeldeten Wartungsfenster |
| Adminzugriff Nina Herbstlich, 09.10. 19:27 | Verzeichnisauflistung im Zielbereich |
| Zugang Dr. Nina Herbst, 10.10. 08:13 | Berechtigung verweigert |

## Gesprächsnotizen

**Alex Berger, 10.10., 12:05:** „Ja, ich war sauer. Meine fachlichen Einwände bestehen weiterhin. Aber ich habe weder die Datenablage verwaltet noch den Ordner gelöscht.“

**Dr. Nina Herbst, 10.10., 12:21:** „Ich habe ihn wegen der Kommentare angerufen. Ich kann eine Präsentation nur halten, wenn ich die Rohdaten selbst sehen kann.“

**Nina Herbstlich, 10.10., 12:34:** „Ich hatte am Freitag Fileservice-Bereitschaft. Mein Konto erscheint in der Prüfung des neuen Speicherbereichs. Die fachlichen Berichte bearbeite ich nicht.“

**Zwischenstatus:** Weitere Systemauszüge werden angefordert; die Prüfung ist nicht abgeschlossen.

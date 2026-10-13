# Überwachung und Datei-Audit – Auszug

**Bereich:** Forschungs-File-Service · **Zeitzone:** Europe/Berlin  
**Export:** 10.10.2026, 11:10

## Alte Teamlink-Prüfung (Monitoring)

```text
2026-10-09 18:42:00 FS-ALT check /forschung/KERN/Review -> FAIL unavailable
2026-10-09 19:42:00 FS-ALT check /forschung/KERN/Review -> FAIL unavailable
2026-10-09 20:11:22 FS-ALT check /forschung/KERN/Review -> FAIL not_found
2026-10-10 07:42:00 FS-ALT check /forschung/KERN/Review -> FAIL not_found
2026-10-10 08:42:00 FS-ALT check /forschung/KERN/Review -> FAIL not_found
```

## Storage- und Auditereignisse

| Zeitpunkt | Konto | Aktion | Ziel / Status |
|---|---|---|---|
| 09.10. 16:41 | a.berger | Datei öffnen | `KERN_Review_v6.docx`, Erfolg |
| 09.10. 18:02 | svc-fs-move | Daten übertragen | Batch 3, Start |
| 09.10. 19:18 | svc-fs-move | Datei verifizieren | `CIR-204/Review/KERN_Review_v7.pdf`, Erfolg |
| 09.10. 19:27 | n.herbstlich | Verzeichnisliste prüfen | `CIR-204/Review`, Erfolg (Admin) |
| 10.10. 08:13 | n.herbst | Datei öffnen | `CIR-204/Review`, verweigert |
| 10.10. 08:34 | l.hartmann | Datei öffnen | `CIR-204/Daten`, Erfolg |

**Hinweis der Audit-Konsole:** Suchereignisse, Zugriffstests und Dateioperationen werden in unterschiedlichen Protokolltypen geführt. Dieser Auszug zeigt die aufgelisteten Vorgänge, keine Vollhistorie aller Systeme.

# Systemauszüge: Projektdatenbank und IAM

**Quellen:** Register-Sync vom 09.10. und Rollenabgleich vom 10.10.  
**Auszug erstellt:** 10.10.2026, 11:40

## Register-Sync, Lauf REG-774

```text
2026-10-09 19:05:58 import: project_key=P-204 source=legacy-projects
2026-10-09 19:06:01 label=KERN, new_namespace=CIR-204
2026-10-09 19:06:02 warn: display_alias missing in target registry
2026-10-09 19:06:02 warn: project_state fallback value=archived
2026-10-09 19:06:03 write: project=P-204, display_name=KERN, state=archiviert
2026-10-09 19:06:03 pending: display_alias sync requires PMO owner confirmation
```

## Rollenabgleich, RD-041

| Konto | Rolle am 08.10. | Zielrolle beantragt | 10.10. 08:00 |
|---|---|---|---|
| a.berger | KERN-lead | KERN-review-read | alte Rolle entzogen; neue Rolle offen |
| n.herbst | KERN-materials | KERN-lead | PMO bestätigt; FS-NEU-Zuordnung pending |
| l.hartmann | KERN-lab | KERN-lab | auf neuer Gruppe aktiv |
| n.herbstlich | fileservice-admin | fileservice-admin | aktiv (technischer Dienst) |

**Ereignisse IAM**

```text
2026-10-09 19:24:17 group-resolution P-204 -> CIR-204
2026-10-09 19:24:18 warning: lead entitlement RD-041-B not provisioned
2026-10-10 08:13:50 n.herbst access denied: \FS-NEU\groups\CIR-204\Review
2026-10-10 08:14:02 a.berger access denied: \FS-NEU\groups\CIR-204\Review
2026-10-10 08:34:29 l.hartmann access granted: \FS-NEU\groups\CIR-204\Daten
```

**Statusfeld:** Nachbearbeitung durch PMO und IAM vorgesehen, kein Abschlussstempel.

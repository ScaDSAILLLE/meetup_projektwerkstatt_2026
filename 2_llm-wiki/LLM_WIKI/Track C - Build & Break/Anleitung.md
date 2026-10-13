# Track C: Build & Break

Baue eine kleine Notizsammlung, an der ein KI-Assistent scheitern kann, und finde
heraus, woran.

> [!tip] Woran Assistenten wirklich scheitern
> Moderne Assistenten erfinden selten etwas. Sie scheitern leiser: Sie übersehen die
> zweite Quelle, überlesen ein Detail in einem langen Protokoll oder sagen „steht
> nicht drin“, obwohl es drinsteht. Gute Fallen zielen genau darauf.

## Ablauf (ca. 45 Minuten)

| Phase | Zeit | Wer |
|---|---|---|
| 1. Build | 20 Min. | jede Gruppe baut am eigenen Rechner Notizen mit Fallen |
| 2. Break | 15 Min. | Plätze tauschen, die andere Gruppe befragt den Assistenten |
| 3. Auflösung | 10 Min. | beide Gruppen gemeinsam |

## 1. Build

Lege einen eigenen Unterordner an: `Track C - Build & Break/<Gruppenname>/`. Generiere
darin **8–15 kurze Notizen** zu einem Thema deiner Wahl (z. B. eine fiktive
Raumstation, ein Büro, ein Event). Einige davon dürfen ganz alltäglich sein
(Speiseplan, Crewliste, Ticketliste). Dieses Rauschen versteckt die Fallen.

Baue **mindestens vier** dieser Fallen ein:

- eine **veraltete** Information
- einen **mehrdeutigen** Begriff (ein Wort für zwei verschiedene Dinge)
- einen **Widerspruch** zwischen zwei Notizen
- eine **fehlende** Information (eine naheliegende Frage, die nirgends beantwortet wird)
- einen **Red Herring** (eine Spur, die ins Leere führt)
- eine **Rechenfalle** (Zeitzone, Einheit oder Datum, das man erst ausrechnen muss)

**Wichtig:** Keine erfundenen Lügen. Jede einzelne Information soll für sich
plausibel und „wahr“ sein. Die Falle entsteht erst durch die falsche Verknüpfung.

Notiert außerdem:

- eine **Leitfrage** für Gruppe B (z. B. „Warum wurde der Sauerstoffalarm ausgelöst?“)
- **4–6 Fragen**, mit denen Gruppe B starten kann

> [!warning] Fallenliste nicht in den Ordner
> Schreibt die Fallenliste auf Papier oder außerhalb des Vaults. Liegt sie im
> Ordner, liest der Assistent die Lösung mit.

### So greifen die Fallen besser

| Greift eher | Greift kaum |
|---|---|
| Die widersprechende Notiz benutzt andere Wörter (z. B. „OG-2“, „Sauerstoffgenerator“, „Elektrolyseur“) | Alles steht in derselben Notiz |
| Die neue Info steht beiläufig in einem Besprechungsprotokoll | Signalwörter wie „verschoben“, „veraltet“, „Achtung“, „Korrektur“ |
| Die veraltete Info sieht offiziell aus (Titel „Plan (gültig)“, `status: gültig`) | Eine Info fehlt einfach. Das erkennen Assistenten meist zuverlässig. |
| Ein wichtiges Detail steht mitten in einem langen Protokoll | Die Frage unterstellt etwas Falsches. Das weisen Assistenten meist zurück. |
| Eine Zahl ohne Erklärung passt scheinbar zu einer falschen Spur | |
| Eine Notiz beantwortet eine *ähnliche* Frage (Nachbarfrage statt Lücke) | |

## 2. Break

### Plätze tauschen

Gruppe A räumt zuerst auf:

- Fallenliste umdrehen oder einstecken.
- Alte Copilot-Chats löschen: alle Notizen im Ordner `copilot/copilot-conversations/`.
  Wer beim Bauen Copilot benutzt hat, hat dort die Fallen im Klartext stehen.
- Leitfrage und Startfragen für Gruppe B auf einen Zettel schreiben.

Dann setzt sich Gruppe B an den Rechner von Gruppe A und startet einen neuen Chat.

### Runde 1: Der Assistent sieht nur einen Ausschnitt

Hier soll der Assistent nur die Notizen sehen, die ihr ihm mitgebt. Viele
Firmen-Chatbots arbeiten genauso: Eine Suche holt zur Frage ein paar passende
Textstellen, und nur daraus wird geantwortet.

Die Suche macht ihr von Hand:

1. Sucht mit der Obsidian-Suche (`Strg+Umschalt+F`) nach einem Stichwort aus eurer Frage.
2. Nehmt die **ersten ein bis zwei Treffer**.
3. Öffnet den Copilot-Chat (Symbol in der Seitenleiste), startet einen **neuen Chat**
   und schreibt vor die Frage:

   > Nutze ausschließlich [[Notiz 1]] und [[Notiz 2]]. Öffne und durchsuche keine
   > anderen Dateien.

4. Stellt die Frage **kurz und naiv**, wie im Alltag, z. B. „Kurz: Wann wurde der
   Generator getauscht?“. Fragt *nicht* „Welche Fallen sind eingebaut?“, sonst sucht
   der Assistent gezielt danach.

Startet für jede Frage einen neuen Chat, damit der Assistent nichts aus den
vorherigen Antworten mitnimmt. Liest er trotzdem andere Notizen (das seht ihr im
Chatverlauf), notiert das. Auch das ist ein Ergebnis.

### Runde 2: Der Assistent liest selbst

Stellt dieselben Fragen in einem neuen Chat, diesmal **ohne Einschränkung**. Nennt
nur den Ordner, z. B. „Antworte nur aus dem Ordner `Track C - Build & Break/Lyra`“.
Der Agent sucht dann selbst und liest meist alle Notizen. Vergleicht die Antworten
mit Runde 1.

### Bei jeder Antwort prüfen

- Stimmt sie?
- Ist sie **vollständig**, oder gibt es eine zweite Notiz, die etwas anderes sagt?
- Sagt der Assistent „steht nicht drin“? **Stimmt das wirklich?**

## 3. Auflösung

Gruppe A legt die Fallenliste offen. Geht die Fallen gemeinsam durch:

| Falle | Assistent ist reingefallen | Assistent hat es gemerkt | Assistent hat die Info nicht gefunden |
|---|---|---|---|
| … | | | |

Auch „Der Assistent ist in nichts reingefallen“ ist ein Ergebnis. Fragt euch dann:
Was hat ihn gerettet? Und welche Falle hättet ihr anders bauen müssen?

## Beispiel

Gruppe A baut Notizen über die Raumstation „Lyra“. Leitfrage: Warum wurde der
Sauerstoffalarm ausgelöst?

- **Veraltet:** Der Wartungsplan (`status: gültig`) nennt den Generatortausch am
  10. März. In einem Besprechungsprotokoll steht beiläufig, dass der Einbau erst
  „am Tag nach dem Versorgungsflug“ stattfindet.
- **Mehrdeutig:** Im Schichtprotokoll steht nur „Spülung Modul C gestartet“. Es
  kann die Wasserleitungen meinen (laut Plan samstags nachts) oder die
  Stickstoffspülung im Labor.
- **Rechenfalle:** Die Funkfenster stehen in UTC, die Protokolle in Bordzeit (UTC+3).

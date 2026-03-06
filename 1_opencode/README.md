# OpenCode – Prompt-Playbook

## Setup

- Anleitung: [`setup.md`](setup.md)

## Tags

- opencode
- plan-mode
- build-mode
- prompt-playbook
- workflow

## Usage

### Der Einstieg

OpenCode ist ein AI-Coding-Agent, der wie ein Junior-Developer mit dir zusammenarbeitet. Er kann:
- Code erklären und verstehen
- Neue Features implementieren
- Bugs fixen
- Refactorings durchführen
- Tests schreiben

---

### Wichtige Tastenkürzel

| Taste | Funktion |
|-------|----------|
| `Tab` | Zwischen Plan-Modus und Build-Modus wechseln |
| `@` | Datei im Projekt auswählen und referenzieren |
| `/undo` | Letzte Änderung rückgängig machen |
| `/redo` | Letzte Änderung wiederholen |
| `/share` | Konversation teilen |
| `/connect` | API-Provider konfigurieren |
| `/init` | Projekt initialisieren |

---

### Plan-Modus (WICHTIG!)

### Warum Plan-Modus?

Der **Plan-Modus** ist der beste Freund beim Experimentieren:
- OpenCode kann nichts verändern – nur Vorschläge machen
- Du kannst in Ruhe den Plan prüfen, Feedback geben, iterieren
- Erst wenn du zufrieden bist, wechselst du zum Build-Modus

### So nutzt du den Plan-Modus:

1. **`Tab` drücken** → Lower-Right zeigt "Plan mode"
2. Beschreibe was du willst:
   ```
   Ich möchte ein Programm das per Webcam Handgesten erkennt und
   damit eine Präsentation steuern kann. Wie könnte das gehen?
   ```
3. OpenCode zeigt dir einen Plan
4. Feedback geben:
   ```
   Das gefällt mir, aber ich möchte statt PowerPoint lieber
   eine Web-App steuern. Ändere den Plan entsprechend.
   ```
5. Wenn der Plan gut ist: **`Tab` drücken** → "Build mode"
6. Sag: "Go ahead and make the changes!"

---

### Gute Prompts schreiben

### ✅ Gute Beispiele

```
Erkläre mir wie die Face Detection in @3_mediapipe_detection/beispiele/face_detection.py funktioniert
```

```
Ich möchte die Hand-Tracking-App erweitern: Wenn eine Faust
erkannt wird, soll stattdessen ein anderes Event gefeuert werden.
Schau dir den Code an und sag mir was ich ändern muss.
```

```
Wir bauen eine Gestensteuerung für eine Web-App. Erstelle einen
Plan für eine Python-Backend-API die Gesten als WebSocket streamt.
```

### ❌ Vermeiden

```
Mach das Ding fertig
```

```
Fix den Bug
```

---

### Dateien referenzieren mit @

Nutze `@`, um Dateien direkt zu referenzieren:

```
Erkläre @src/main.py
```

```
Was passiert in @utils/helper.py:45 ?
```

---

### Bilder einfügen

Du kannst **Bilder in das Terminal ziehen** – OpenCode analysiert sie!

Nützlich für:
- Screenshots von Fehlermeldungen
- UI-Entwürfe
- Diagramme

---

### Fehler rückgängig machen

```
/undo  # Eine Änderung zurück
/undo  # Noch eine zurück
/redo  # Wiederholen
```

---

### Workflow für dieses Projekt

### 1. Wähle ein Beispielprojekt

- **MediaPipe**: [`3_mediapipe_detection/`](../3_mediapipe_detection/)
- **VLM Scene**: [`4_qwen_vl_scene/`](../4_qwen_vl_scene/)

### 2. Starte im Plan-Modus

Frag zuerst:
```
Ich möchte [deine Idee]. Kannst du mir einen Plan zeigen,
wie wir das umsetzen könnten?
```

### 3. Iteriere

Gib Feedback:
- "Das gefällt mir, aber..."
- "Kannst du auch X berücksichtigen?"
- "Zu kompliziert – vereinfach das bitte"

### 4. Baue

Wenn der Plan steht:
```
<Tab>  (zu Build-Modus wechseln)
Go ahead and make the changes!
```

### 5. Teste & iteriere

Lass dir erklären was gebaut wurde:
```
Kannst du mir erklären was du gemacht hast?
```

---

### Best Practices

### 1. Nutze den Plan-Modus für neue Ideen
- Keine Angst vor versehentlichen Änderungen
- Bessere Ergebnisse durch Iteration

### 2. Gib Kontext
- Was ist das Ziel?
- Welche Einschränkungen gibt es?
- Referenziere bestehenden Code mit @

### 3. Sei spezifisch
- "Erkläre mir X" ist besser als "Was macht das?"
- "Ändere die Funktion so, dass sie Y tut" ist besser als "Mach das anders"

### 4. Nutze /share für Teamarbeit
- Teile deine Session mit Kolleg*innen
- Kopiert den Link automatisch

### 5. Nutze UV für Pakete
- Statt `pip install` → `uv add <paket>`
- UV ist schneller und moderner

---

### Befehls-Referenz

| Befehl | Beschreibung |
|--------|--------------|
| `/init` | Projekt initialisieren |
| `/connect` | API-Provider verbinden |
| `/undo` | Letzte Änderung rückgängig |
| `/redo` | Letzte Änderung wiederholen |
| `/share` | Konversation teilen |
| `/ask` | Eine Frage stellen |

---

### Troubleshooting

### "OpenCode kann nicht auf Dateien zugreifen"
→ Stelle sicher, dass du im richtigen Verzeichnis bist und `/init` ausgeführt hast

### "API-Key fehlt"
→ Nutze `/connect` oder setze Umgebungsvariablen

### "Modell antwortet nicht"
→ Prüfe Internetverbindung und API-Key

---

### Mehr Infos

- Offizielle Docs: https://opencode.ai/docs
- GitHub: https://github.com/anomalyco/opencode

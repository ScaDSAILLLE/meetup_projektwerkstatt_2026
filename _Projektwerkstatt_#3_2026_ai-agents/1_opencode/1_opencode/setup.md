# OpenCode Setup

## Installation

### Windows: WSL für OpenCode empfohlen

Für die beste Erfahrung mit OpenCode empfiehlt auch die offizielle Doku **WSL (Windows Subsystem for Linux)** auf Windows. Auf den Workshop-Laptops ist WSL vorbereitet: In einem Terminal `wsl` eingeben und ihr seid im Linux-Subsystem.

Wichtig: Diese Empfehlung gilt für OpenCode selbst. Die SmolAgents-App der Projektwerkstatt wird auf den Workshop-Laptops bewusst im normalen Windows-Terminal von VS Code gestartet, damit es keine WSL-Pfad- oder Environment-Missverständnisse gibt.

#### WSL installieren (falls nicht vorhanden) & für alle, die das eigens aufsetzen wollen/müssen:

1. PowerShell als Administrator öffnen:
   ```powershell
   wsl --install
   ```
2. Neustart erforderlich
3. Ubuntu (oder andere Distribution) auswählen
4. Benutzerkonto einrichten

#### OpenCode in WSL installieren

Nach der WSL-Installation:

```bash
# OpenCode installieren
curl -fsSL https://opencode.ai/install | bash

# Oder alternativ mit npm, falls Node.js bereits installiert ist. curl-Befehl ist aber klar empfohlen!
npm install -g opencode-ai
```

### macOS / Linux

```bash
# Option 1: Install-Skript
curl -fsSL https://opencode.ai/install | bash

# Option 2: npm
npm install -g opencode-ai

# Option 3: Homebrew
brew install anomalyco/tap/opencode
```

### Direkt unter Windows (ohne WSL)

Schau vorher bitte hier: https://opencode.ai/docs/ und https://opencode.ai/docs/windows-wsl. Falls WSL nicht genutzt werden soll:

```powershell
# Option 1: npm
npm install -g opencode-ai

# Option 2: Scoop
scoop install opencode

# Option 3: Chocolatey
choco install opencode
```

---

## API-Keys konfigurieren (Auch bereits erledigt! NUR FÜR TN, die das eigens einrichten wollen.)

### Option 1: In OpenCode (empfohlen)

1. OpenCode starten:
   ```bash
   opencode
   ```

2. `/connect` eingeben:
   ```
   /connect
   ```

3. Provider auswählen (z.B. OpenAI, Anthropic)

4. API-Key eingeben oder via Browser/Subscription connecten

### Option 2: Umgebungsvariablen

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Mistral
export MISTRAL_API_KEY="..."

# KIARA (Uni-Cluster)
export KIARA_API_KEY="..."
```

Unter Windows (CMD):
```cmd
setx OPENAI_API_KEY "sk-..."
```

---

## Projekt initialisieren

1. In das Projektverzeichnis navigieren:
   ```bash
   cd /pfad/zum/projekt
   ```

2. (WSL &) OpenCode starten:
   ```bash
   wsl
   # in wsl:
   opencode
   ```

3. `/init` eingeben:
   ```
   /init
   ```

   Dies erstellt oder aktualisiert eine `AGENTS.md`-Datei mit projektspezifischen Anweisungen und schaut schon mal grob den Ordner durch.

   Hinweis für dieses Repo: `AGENTS.md` ist bewusst lokal und in `.gitignore` eingetragen. Bitte nicht committen.

---

## Verifizierung

Prüfen ob alles funktioniert:

```bash
opencode --version
```

In VS Code kann OpenCode außerdem direkt im integrierten Terminal gestartet werden:

```bash
opencode
```

Die VS-Code-Erweiterung kann sich dabei automatisch installieren. Aktuelle Shortcuts laut OpenCode-Doku: `Ctrl+Esc` öffnet/fokussiert OpenCode, `Ctrl+Shift+Esc` startet eine neue Session.

---

## Nächste Schritte

- Siehe [`README.md`](README.md) für das Prompt-Playbook
- Projektstruktur: Siehe Haupt-[`README.md`](../README.md)

# OpenCode Setup

## Installation

### Windows: WSL empfohlen!

Für die beste Erfahrung mit OpenCode empfehlen wir **WSL (Windows Subsystem for Linux)** auf Windows 11.

#### WSL installieren (falls nicht vorhanden)

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

# Oder alternativ mit npm
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

Falls WSL nicht genutzt werden soll:

```powershell
# Option 1: npm
npm install -g opencode-ai

# Option 2: Scoop
scoop install opencode

# Option 3: Chocolatey
choco install opencode
```

---

## API-Keys konfigurieren

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

4. API-Key eingeben

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
set OPENAI_API_KEY=sk-...
```

---

## Projekt initialisieren

1. In das Projektverzeichnis navigieren:
   ```bash
   cd /pfad/zum/projekt
   ```

2. OpenCode starten:
   ```bash
   opencode
   ```

3. `/init` eingeben:
   ```
   /init
   ```

   Dies erstellt eine `AGENTS.md`-Datei mit projektspezifischen Anweisungen.

---

## Verifizierung

Prüfen ob alles funktioniert:

```bash
opencode --version
```

---

## Nächste Schritte

- Siehe [`README.md`](README.md) für das Prompt-Playbook
- Projektstruktur: Siehe Haupt-[`README.md`](../README.md)

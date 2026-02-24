@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   ScaDS.AI Meetup Setup Script
echo   Computer Vision Workshop
echo ========================================
echo.

REM ========================================
REM API Keys setzen
REM ========================================
echo [1/5] Setting up API keys...
echo.

set /p OPENAI_API_KEY="OpenAI API Key (leave empty to skip): "
set /p ANTHROPIC_API_KEY="Anthropic API Key (leave empty to skip): "
set /p MISTRAL_API_KEY="Mistral API Key (leave empty to skip): "
set /p KIARA_API_KEY="KIARA API Key (leave empty to skip): "

if not "%OPENAI_API_KEY%"=="" (
    setx OPENAI_API_KEY "%OPENAI_API_KEY%" >nul
    echo   - OpenAI API Key set
)
if not "%ANTHROPIC_API_KEY%"=="" (
    setx ANTHROPIC_API_KEY "%ANTHROPIC_API_KEY%" >nul
    echo   - Anthropic API Key set
)
if not "%MISTRAL_API_KEY%"=="" (
    setx MISTRAL_API_KEY "%MISTRAL_API_KEY%" >nul
    echo   - Mistral API Key set
)
if not "%KIARA_API_KEY%"=="" (
    setx KIARA_API_KEY "%KIARA_API_KEY%" >nul
    echo   - KIARA API Key set
)

echo.

REM ========================================
REM UV installieren (falls nicht vorhanden)
REM ========================================
echo [2/5] Checking UV installation...
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo   UV not found. Installing UV...
    curl -LsSf https://astral.sh/uv/install.sh | powershell -Command "$input | Invoke-Expression"
    set PATH=%PATH%;%USERPROFILE%\.local\bin
    echo   - UV installed
) else (
    echo   - UV already installed
)
echo.

REM ========================================
REM Ollama installieren (falls nicht vorhanden)
REM ========================================
echo [3/5] Checking Ollama installation...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo   Ollama not found. Installing Ollama...
    curl -L -o ollama-installer.exe https://ollama.ai/install.bat
    call ollama-installer.exe
    del ollama-installer.exe
    echo   - Ollama installed
) else (
    echo   - Ollama already installed
)
echo.

REM ========================================
REM qwen3-vl:2b Modell vorladen
REM ========================================
echo [4/5] Checking qwen3-vl:2b model...
ollama list | findstr "qwen3-vl" >nul
if %errorlevel% neq 0 (
    echo   Pulling qwen3-vl:2b model (this may take a while)...
    ollama pull qwen3-vl:2b
    echo   - Model ready
) else (
    echo   - Model already available
)
echo.

REM ========================================
REM OpenCode installieren (WSL empfohlen!)
REM ========================================
echo [5/5] OpenCode Setup (WSL recommended!)
echo.
echo   ========================================
echo   OPTION A: WSL (Recommended)
echo   ========================================
echo   Run in WSL (Ubuntu):
echo.
echo     curl -fsSL https://opencode.ai/install ^| bash
echo.
echo   Then configure with:
echo     opencode
echo     /connect
echo.
echo   ========================================
echo   OPTION B: Windows Direct (not recommended)
echo   ========================================
echo   Using npm:
echo     npm install -g opencode-ai
echo.
echo   Or using scoop:
echo     scoop install opencode
echo.
echo   Or using chocolatey:
echo     choco install opencode
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Open WSL and run 'opencode'
echo   2. Use /connect to configure API keys
echo   3. Run /init to initialize your project
echo   4. Start coding with AI!
echo.

pause

<#
Build script (PowerShell).

Prerequisites:
- Python 3.8+ installed and on PATH
- `pip install -r requirements.txt`
- `pip install pyinstaller`

This script will create a venv, install requirements and build single-file EXEs with PyInstaller.
#>

$ErrorActionPreference = 'Stop'

if (-not (Test-Path .venv)) {
    python -m venv .venv
}

.
.\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

# Build online clipboard EXE
pyinstaller --onefile --name ai_clipboard_online ai_clipboard_online.py

# Build offline clipboard EXE (hotkey)
pyinstaller --onefile --name ai_clipboard_offline ai_clipboard_offline.py

Write-Host "Build complete. Check the 'dist' folder for executables." -ForegroundColor Green

# Optionally create a zip for distribution
if (Test-Path dist\ai_clipboard_online.exe) {
    Compress-Archive -Path dist\ai_clipboard_online.exe -DestinationPath ai_clipboard_online.zip -Force
    Write-Host "Packed ai_clipboard_online.zip" -ForegroundColor Green
}

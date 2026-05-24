<#
Build script (PowerShell).

Prerequisites:
- Python 3.8+ installed and on PATH
- `pip install -r requirements.txt`
- `pip install pyinstaller`

This script will create a venv, install requirements and build single-file EXEs with PyInstaller.
#>

$ErrorActionPreference = 'Stop'
$PreferredPythonVersion = "3.12"

function Invoke-SystemPython {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PythonArgs)

    & py "-$PreferredPythonVersion" --version *> $null
    if ($LASTEXITCODE -eq 0) {
        & py "-$PreferredPythonVersion" @PythonArgs
        if ($LASTEXITCODE -ne 0) {
            throw "Python command failed with exit code $LASTEXITCODE."
        }
        return
    }

    & python --version *> $null
    if ($LASTEXITCODE -eq 0) {
        & python @PythonArgs
        if ($LASTEXITCODE -ne 0) {
            throw "Python command failed with exit code $LASTEXITCODE."
        }
        return
    }

    throw "Python $PreferredPythonVersion was not found. Install Python $PreferredPythonVersion and make sure the 'py' launcher is available."
}

function Invoke-VenvPython {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PythonArgs)

    & $VenvPython @PythonArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Virtual environment Python command failed with exit code $LASTEXITCODE."
    }
}

$VenvDir = Join-Path (Get-Location) ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$WorkspaceRoot = [System.IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\') + '\'
$VenvFullPath = [System.IO.Path]::GetFullPath($VenvDir).TrimEnd('\') + '\'

if (Test-Path $VenvPython) {
    $VenvVersion = & $VenvPython -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($VenvVersion -ne $PreferredPythonVersion) {
        if (-not $VenvFullPath.StartsWith($WorkspaceRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove venv outside the workspace: $VenvFullPath"
        }
        Write-Host "Removing .venv built with Python $VenvVersion; rebuilding with Python $PreferredPythonVersion." -ForegroundColor Yellow
        Remove-Item -LiteralPath $VenvDir -Recurse -Force
    }
}

if (-not (Test-Path $VenvPython)) {
    Invoke-SystemPython -m venv .venv
}

Invoke-VenvPython -m pip install --upgrade pip
Invoke-VenvPython -m pip install -r requirements.txt

# Build online clipboard EXE
Invoke-VenvPython -m PyInstaller --onefile --name ai_clipboard_online ai_clipboard_online.py

# Build offline clipboard EXE (hotkey)
Invoke-VenvPython -m PyInstaller --onefile --name ai_clipboard_offline ai_clipboard_offline.py

Write-Host "Build complete. Check the 'dist' folder for executables." -ForegroundColor Green

if (-not (Test-Path web)) {
    New-Item -ItemType Directory -Path web | Out-Null
}

if (Test-Path dist\ai_clipboard_online.exe) {
    Copy-Item -Path dist\ai_clipboard_online.exe -Destination web\ai_clipboard_online.exe -Force
    Write-Host "Copied web\ai_clipboard_online.exe for Vercel download." -ForegroundColor Green
}

# Optionally create a zip for distribution
if (Test-Path dist\ai_clipboard_online.exe) {
    Compress-Archive -Path dist\ai_clipboard_online.exe -DestinationPath ai_clipboard_online.zip -Force
    Write-Host "Packed ai_clipboard_online.zip" -ForegroundColor Green
}

# Inno Setup script to create a simple installer for ai_clipboard_online
# Adjust `Source` path below if your built EXE is in a different folder.

[Setup]
AppName=AI Clipboard
AppVersion=1.0
DefaultDirName={pf}\AI Clipboard
DefaultGroupName=AI Clipboard
OutputBaseFilename=ai_clipboard_online_installer
Compression=lzma
SolidCompression=yes

[Files]
; Path to the single-file exe produced by PyInstaller
Source: "{#MySourceExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AI Clipboard"; Filename: "{app}\ai_clipboard_online.exe"

[Run]
Filename: "{app}\ai_clipboard_online.exe"; Description: "Launch AI Clipboard"; Flags: nowait postinstall skipifsilent

; Instructions: Replace {#MySourceExe} with the actual path, for example:
; Source: "..\dist\ai_clipboard_online.exe"; DestDir: "{app}"; Flags: ignoreversion

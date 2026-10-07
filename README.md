# AI Clipboard

This repository contains two variants of an "AI Clipboard" helper:

- `ai_clipboard_online.py` — uses Google Generative API (gemini) to solve problems copied to the clipboard.
- `ai_clipboard_offline.py` — uses a local LLM endpoint (OLLAMA) and a hotkey.

Safety notes
- `ai_clipboard_online.py` reads the API key from the `GENAI_API_KEY` (or `GOOGLE_API_KEY`) environment variable.
- Never hardcode a key in this repo. Google automatically blocks keys found in public repos ("403 Your API key was reported as leaked").

Quick workflow
1. Set your API key in PowerShell (persistent):

```powershell
setx GENAI_API_KEY "your_api_key_here"
```

2. Install dev tools and build the portable EXE:

```powershell
.\build_exe.ps1
```

3. Create an installer (requires Inno Setup installed) — run Inno from the `.iss` script or follow the script comments.

4. Initialize git and push to GitHub (set your remote first):

```powershell
.\push_to_github.ps1
```

5. Deploy to Vercel. The root `vercel.json` config serves the static site from `web/`, so Vercel does not try to build the desktop Python scripts. Place the built installer into `web/` (or upload to GitHub Releases) and update `index.html` download link accordingly.

More details and troubleshooting are in the file headers and scripts.

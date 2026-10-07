# AI Clipboard

This repository contains two variants of an "AI Clipboard" helper:

- `ai_clipboard_online.py` — sends problems copied to the clipboard to `api/solve.js` (a Vercel function), which solves them with Gemini. The EXE needs no setup on any computer.
- `ai_clipboard_offline.py` — uses a local LLM endpoint (OLLAMA) and a hotkey.

Safety notes
- The Gemini key lives only in the Vercel project's `GEMINI_API_KEY` environment variable. It is never in this repo or in the EXE.
- Never hardcode a key in this repo. Google automatically blocks keys found in public repos ("403 Your API key was reported as leaked").

Quick workflow
1. One time: in the Vercel dashboard (Project → Settings → Environment Variables), add `GEMINI_API_KEY` for Production, then redeploy.

2. Install dev tools and build the portable EXE:

```powershell
.\build_exe.ps1
```

3. Create an installer (requires Inno Setup installed) — run Inno from the `.iss` script or follow the script comments.

4. Initialize git and push to GitHub (set your remote first):

```powershell
.\push_to_github.ps1
```

5. Deploy to Vercel. The root `vercel.json` config serves the static site from `web/` and the `api/` function, so Vercel does not try to build the desktop Python scripts. Place the built installer into `web/` (or upload to GitHub Releases) and update `index.html` download link accordingly.

More details and troubleshooting are in the file headers and scripts.

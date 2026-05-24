import keyboard
import pyperclip
import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"

print("AI Clipboard Assistant Running...")
print("Copy coding question and press CTRL + SHIFT + X")

def solve_problem():

    try:
        problem = pyperclip.paste()

        if not problem.strip():
            print("Clipboard empty")
            return

        print("\nSolving...\n")

        prompt = f"""
You are a competitive programming expert.

Solve this problem in Python.

Return ONLY code.
No explanation.

Problem:
{problem}
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()["response"]

        pyperclip.copy(result)

        print("Code copied to clipboard!")
        print("-" * 50)

    except Exception as e:
        print("Error:", e)

keyboard.add_hotkey("ctrl+shift+x", solve_problem)

keyboard.wait()
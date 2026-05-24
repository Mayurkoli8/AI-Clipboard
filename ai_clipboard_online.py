import os
import pyperclip
import google.generativeai as genai
import re
import threading
import keyboard

# Configure API key from environment for safety
API_KEY = "AIzaSyCRlgsexMUzJFKvaGqehQeZ2Ip3XPWDl08"
if not API_KEY:
    raise SystemExit("GENAI_API_KEY (or GOOGLE_API_KEY) environment variable not set.\nSet it before running: `setx GENAI_API_KEY \"your_key\"` and reopen the shell.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
HOTKEY = "ctrl+shift+x"
solve_lock = threading.Lock()

print("AI Clipboard Solver running in the background...")
print(f"Copy a LeetCode problem statement, then press {HOTKEY.upper()} to solve it.")

problem_patterns = [
    r"\binput\b",
    r"\boutput\b",
    r"example",
    r"constraints",
    r"given two",
    r"string",
    r"nums",
    r"return",
    r"\bclass\b",
    r"\bfunction\b",
]

ignore_patterns = [
    r"python was not found",
    r"install python",
    r"add python to path",
    r"app execution aliases",
    r"microsoft store",
    r"error:\s*",
    r"clipboard",
    r"# this script",
    r"# the error",
]


def looks_like_leetcode_problem(text: str) -> bool:
    if not text or len(text.strip()) < 40:
        return False
    lower = text.lower()
    if any(re.search(pattern, lower) for pattern in ignore_patterns):
        return False
    score = sum(bool(re.search(pattern, lower)) for pattern in problem_patterns)
    return score >= 2


def build_prompt(problem_text: str) -> str:
    return f"""
You are an expert competitive programmer solving a LeetCode-style algorithm problem.
Write clean, efficient Python 3 code that passes LeetCode constraints.
Do not include any markdown, comments, explanation, or extra text.
Do not include input/output code, test cases, or `if __name__ == '__main__':`.
Return only the function or class implementation required for the problem.
Problem:
{problem_text}
"""


def solve_problem(problem_text: str) -> str:
    prompt = build_prompt(problem_text)
    response = model.generate_content(prompt)
    result = response.text.strip()
    result = result.replace("```python", "")
    result = result.replace("```", "")
    return result.strip()


def solve_from_clipboard():
    if not solve_lock.acquire(blocking=False):
        print("Solve already running. Please wait.")
        return

    try:
        try:
            current_text = pyperclip.paste()
        except Exception as e:
            print("Clipboard read failed:", e)
            return

        if not current_text.strip():
            print("Clipboard is empty.")
            return

        if not looks_like_leetcode_problem(current_text):
            print("Clipboard does not look like a LeetCode-style problem.")
            return

        try:
            print("Solving clipboard problem...")
            solution = solve_problem(current_text)
            pyperclip.copy(solution)
            print("Solved and copied solution to clipboard.")
        except Exception as e:
            print("Solve failed:", e)
    finally:
        solve_lock.release()


if __name__ == "__main__":
    keyboard.add_hotkey(HOTKEY, solve_from_clipboard, trigger_on_release=True)
    keyboard.wait()

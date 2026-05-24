import os
import pyperclip
import google.generativeai as genai
import re
import threading
import ctypes
from ctypes import wintypes

# Configure API key from environment for safety
API_KEY = "AIzaSyCRlgsexMUzJFKvaGqehQeZ2Ip3XPWDl08"
if not API_KEY:
    raise SystemExit("GENAI_API_KEY (or GOOGLE_API_KEY) environment variable not set.\nSet it before running: `setx GENAI_API_KEY \"your_key\"` and reopen the shell.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
HOTKEY = "Ctrl+Shift+X"
HOTKEY_ID = 1
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
VK_X = 0x58
WM_HOTKEY = 0x0312
solve_lock = threading.Lock()
user32 = ctypes.WinDLL("user32", use_last_error=True)

user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
user32.RegisterHotKey.restype = wintypes.BOOL
user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
user32.UnregisterHotKey.restype = wintypes.BOOL
user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = ctypes.c_int
user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]

print("AI Clipboard Solver running in the background...")
print(f"Copy a LeetCode problem statement, then press {HOTKEY} to solve it.")

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


def run_hotkey_loop():
    modifiers = MOD_CONTROL | MOD_SHIFT
    if not user32.RegisterHotKey(None, HOTKEY_ID, modifiers, VK_X):
        error_code = ctypes.get_last_error()
        raise OSError(error_code, f"Could not register {HOTKEY}. Another app may already be using it.")

    print(f"Hotkey registered: {HOTKEY}")
    msg = wintypes.MSG()
    try:
        while True:
            result = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if result == 0:
                break
            if result == -1:
                raise ctypes.WinError(ctypes.get_last_error())
            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                threading.Thread(target=solve_from_clipboard, daemon=True).start()
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
    finally:
        user32.UnregisterHotKey(None, HOTKEY_ID)


if __name__ == "__main__":
    run_hotkey_loop()

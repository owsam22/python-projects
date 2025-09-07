import keyboard
import pyperclip
import time
import requests

# --- CONFIG ---
API_KEY = "YOUR_API_KEY"   # Replace with your key
MODEL = "deepseek/deepseek-r1:free"   # Example model ,you can change to your model
HOTKEY_REPLACE = "ctrl+alt+v"         # Correct + replace
HOTKEY_CLIPBOARD = "ctrl+alt+c"       # Correct + copy only
# --------------

def get_selected_text():
    """Force copy selected text and wait until clipboard updates."""
    # Clear clipboard first
    pyperclip.copy("")
    time.sleep(0.05)

    # Press Ctrl+C twice (safer for some apps)
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.2)
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.3)

    new_clip = pyperclip.paste().strip()
    return new_clip if new_clip else None


def fetch_correction(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Correct grammar and rewrite naturally. Only return the corrected text. No explanations."
            },
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def correct_and_replace():
    text = get_selected_text()
    if not text:
        print("⚠️ No text detected.")
        return
    print(f"Selected (replace): {text}")
    corrected = fetch_correction(text)
    pyperclip.copy(corrected)
    time.sleep(0.1)
    keyboard.press_and_release("ctrl+v")
    print(f"✅ Corrected (replaced): {corrected}")


def correct_to_clipboard():
    text = get_selected_text()
    if not text:
        print("⚠️ No text detected.")
        return
    print(f"Selected (clipboard): {text}")
    corrected = fetch_correction(text)
    pyperclip.copy(corrected)
    print(f"✅ Corrected copied: {corrected}")


# Assign hotkeys
keyboard.add_hotkey(HOTKEY_REPLACE, correct_and_replace)
keyboard.add_hotkey(HOTKEY_CLIPBOARD, correct_to_clipboard)

print(f"Running... Press {HOTKEY_REPLACE} to replace, {HOTKEY_CLIPBOARD} to copy. ESC to exit.")
keyboard.wait("esc")

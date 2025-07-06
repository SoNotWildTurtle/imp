from pathlib import Path
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
PERSONALITY_FILE = BASE_DIR / "config" / "imp-personality.json"
CHAT_HISTORY_FILE = BASE_DIR / "logs" / "imp-chat-history.json"


def load_personality():
    if not PERSONALITY_FILE.exists():
        return "IMP", ""
    with open(PERSONALITY_FILE, "r") as f:
        data = json.load(f)
    name = data.get("name", "IMP")
    tone = data.get("personality", {}).get("tone", "")
    return name, tone


def load_history():
    if not CHAT_HISTORY_FILE.exists():
        return []
    with open(CHAT_HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def append_history(role: str, message: str):
    history = load_history()
    history.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "message": message,
    })
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def generate_response(message: str) -> str:
    name, tone = load_personality()
    response = f"{name} ({tone}): I have received your message -> {message}"
    append_history("imp", response)
    return response


def chat_once():
    try:
        prompt = input("You: ")
    except EOFError:
        return
    append_history("user", prompt)
    response = generate_response(prompt)
    print(response)


def chat_session():
    while True:
        try:
            prompt = input("You: ")
        except EOFError:
            break
        if not prompt or prompt.lower() in {"quit", "exit"}:
            break
        append_history("user", prompt)
        response = generate_response(prompt)
        print(response)


if __name__ == "__main__":
    chat_session()

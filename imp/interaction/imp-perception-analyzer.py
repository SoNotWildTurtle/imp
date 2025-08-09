from pathlib import Path
import json
import time
import re

BASE_DIR = Path(__file__).resolve().parents[1]
HISTORY_FILE = BASE_DIR / "logs" / "imp-chat-history.json"
PERCEPTION_LOG = BASE_DIR / "logs" / "imp-perception-log.json"

NEGATIVE_WORDS = {
    "stupid", "idiot", "hate", "dumb", "annoying", "angry", "mad",
    "terrible", "worst", "useless", "shut", "trash"
}
POSITIVE_WORDS = {
    "great", "awesome", "nice", "love", "good", "excellent", "amazing",
    "wonderful", "happy"
}


def load_history():
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def calculate_tone(messages):
    neg = 0
    pos = 0
    for msg in messages:
        words = re.findall(r"[a-zA-Z']+", msg.lower())
        for w in words:
            if w in NEGATIVE_WORDS:
                neg += 1
            elif w in POSITIVE_WORDS:
                pos += 1
    if neg > pos:
        return "aggressive", neg, pos
    if pos > neg:
        return "friendly", neg, pos
    return "neutral", neg, pos


def save_perception(entry):
    data = []
    if PERCEPTION_LOG.exists():
        with open(PERCEPTION_LOG, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append(entry)
    with open(PERCEPTION_LOG, "w") as f:
        json.dump(data, f, indent=4)


def analyze_perception():
    history = load_history()
    user_msgs = [h.get("message", "") for h in history if h.get("role") == "user"]
    tone, neg, pos = calculate_tone(user_msgs)
    suggested = "tough" if tone == "aggressive" else "friendly"
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tone": tone,
        "neg_words": neg,
        "pos_words": pos,
        "suggested_personality": suggested,
    }
    save_perception(entry)
    print(f"[+] Perception analysis recorded with tone: {tone}")
    return entry


if __name__ == "__main__":
    analyze_perception()

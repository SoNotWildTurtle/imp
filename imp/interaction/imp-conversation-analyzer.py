from pathlib import Path
import json
import time
import re
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]
HISTORY_FILE = BASE_DIR / "logs" / "imp-chat-history.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_history():
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def analyze_history():
    history = load_history()
    text = " ".join(entry.get("message", "") for entry in history)
    words = re.findall(r"[a-zA-Z']{4,}", text.lower())
    counts = Counter(words)
    common = counts.most_common(5)
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "top_words": common,
    }


def save_insight(insight):
    insights = []
    if INSIGHTS_FILE.exists():
        with open(INSIGHTS_FILE, "r") as f:
            try:
                insights = json.load(f)
            except json.JSONDecodeError:
                insights = []
    insights.append(insight)
    with open(INSIGHTS_FILE, "w") as f:
        json.dump(insights, f, indent=4)


def run_analysis():
    insight = analyze_history()
    save_insight(insight)
    print(f"[+] Conversation analysis recorded with {len(insight['top_words'])} keywords.")


if __name__ == "__main__":
    run_analysis()

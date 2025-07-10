import os
import argparse
import json
from pathlib import Path
from typing import List

try:
    import openai
except ImportError:
    openai = None

ROOT = Path(__file__).resolve().parents[1]
CHAT_LOG = ROOT / "logs" / "imp-chat-log.txt"
GOALS_FILE = ROOT / "logs" / "imp-goals.json"
NOTES_DIR = ROOT / "notes"

SYSTEM_PROMPT = (
    "You are an assistant helping manage and evaluate goals for the IMP AI system."
)


def load_notes() -> str:
    """Return concatenated text from all files in the notes folder."""
    if not NOTES_DIR.exists():
        return ""
    notes: List[str] = []
    for path in NOTES_DIR.glob("*.txt"):
        try:
            notes.append(path.read_text().strip())
        except Exception:
            continue
    return "\n".join(n for n in notes if n)


def send_chatgpt_request(message: str, use_notes: bool = False) -> str:
    """Send a user message to ChatGPT and return the response text."""
    if openai is None:
        print("[!] openai package not available.")
        return ""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[!] OPENAI_API_KEY environment variable not set.")
        return ""
    openai.api_key = api_key
    try:
        if use_notes:
            notes = load_notes()
            if notes:
                message = f"Personal notes:\n{notes}\n\n{message}"
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        )
        text = resp["choices"][0]["message"]["content"].strip()
        with open(CHAT_LOG, "a") as log:
            log.write(f"USER: {message}\nASSISTANT: {text}\n\n")
        return text
    except Exception as exc:
        print(f"[!] ChatGPT request failed: {exc}")
        return ""


def evaluate_current_goals(use_notes: bool = False) -> str:
    """Ask ChatGPT to review existing goals and return the feedback."""
    if not GOALS_FILE.exists():
        return "No goals to evaluate."
    with open(GOALS_FILE, "r") as f:
        goals = json.load(f)
    goal_text = "\n".join(f"- {g['goal']}" for g in goals)
    prompt = f"Please evaluate the following goals and suggest improvements:\n{goal_text}"
    return send_chatgpt_request(prompt, use_notes)


def chat_loop(use_notes: bool = False):
    """Interactive chat loop with ChatGPT."""
    print("Type your questions about goal management. Press Enter on an empty line to exit.")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            break
        reply = send_chatgpt_request(user_input, use_notes)
        if reply:
            print(f"GPT: {reply}")
        else:
            print("(No response)")


def main():
    parser = argparse.ArgumentParser(description="IMP Goal Chatbot")
    parser.add_argument(
        "--mode",
        choices=["online", "offline"],
        default="online",
        help="ChatGPT is available only in online mode.",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Request ChatGPT to evaluate current goals and exit.",
    )
    parser.add_argument(
        "--use-notes",
        action="store_true",
        help="Include personal notes in ChatGPT requests.",
    )
    args = parser.parse_args()

    if args.mode != "online":
        print("ChatGPT assistance is only available in online mode.")
        return

    if args.evaluate:
        feedback = evaluate_current_goals(args.use_notes)
        print(feedback)
    else:
        chat_loop(args.use_notes)


if __name__ == "__main__":
    main()

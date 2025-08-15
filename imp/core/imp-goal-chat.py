import os
import argparse
import json
import time
from pathlib import Path
from typing import List, Dict
import importlib.util
import sys

try:
    import openai
except ImportError:
    openai = None

# Track last request times for OpenAI models
OPENAI_LAST_REQUEST: Dict[str, float] = {}
# Approximate requests per minute; throttled to one quarter
OPENAI_RPM: Dict[str, int] = {
    "gpt-3.5-turbo": 60,
    "gpt-4": 40,
}

try:
    from transformers import pipeline
except Exception:
    pipeline = None


def decide_mode() -> str:
    if openai is not None and os.getenv("OPENAI_API_KEY"):
        return "online"
    return "offline"

ROOT = Path(__file__).resolve().parents[1]
CHAT_LOG = ROOT / "logs" / "imp-chat-log.txt"
GOALS_FILE = ROOT / "logs" / "imp-goals.json"
NOTES_DIR = ROOT / "notes"

_speech_path = ROOT / "core" / "imp-speech-to-text.py"
spec_speech = importlib.util.spec_from_file_location("imp_speech_to_text", _speech_path)
imp_speech_to_text = importlib.util.module_from_spec(spec_speech)
spec_speech.loader.exec_module(imp_speech_to_text)

_auth_path = ROOT / "security" / "imp-authenticator.py"
spec_auth = importlib.util.spec_from_file_location("imp_authenticator", _auth_path)
imp_authenticator = importlib.util.module_from_spec(spec_auth)
spec_auth.loader.exec_module(imp_authenticator)

def _throttle(model: str) -> None:
    """Pause to respect OpenAI rate limits divided by four."""
    rpm = OPENAI_RPM.get(model, 60)
    interval = 60 / (rpm / 4)
    last = OPENAI_LAST_REQUEST.get(model, 0)
    elapsed = time.time() - last
    if elapsed < interval:
        time.sleep(interval - elapsed)
    OPENAI_LAST_REQUEST[model] = time.time()

SYSTEM_PROMPT = (
    "You are an assistant helping manage and evaluate goals for the IMP AI system."
)

def _build_offline_generator():
    if pipeline is None:
        return None
    try:
        return pipeline("text-generation", model="gpt2")
    except Exception:
        return None

offline_generator = _build_offline_generator()

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


def send_chatgpt_request(
    message: str,
    use_notes: bool = False,
    mode: str = "auto",
    history: List[Dict[str, str]] | None = None,
) -> str:
    """Return a response generated either with ChatGPT or a local model.

    If ``history`` is provided, it is treated as a list of previous
    conversation turns and will be appended with the latest user/assistant
    messages to maintain context across calls.
    """
    if mode == "auto":
        mode = decide_mode()

    if mode == "online" and openai is not None and os.getenv("OPENAI_API_KEY"):
        api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key
        try:
            _throttle("gpt-3.5-turbo")
            if use_notes:
                notes = load_notes()
                if notes:
                    message = f"Personal notes:\n{notes}\n\n{message}"
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": message})
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            text = resp["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            print(f"[!] ChatGPT request failed: {exc}")
            text = ""
    else:
        if offline_generator is not None:
            if history:
                # simple context by prepending prior exchanges
                prior = "\n".join(h["content"] for h in history if h["role"] == "user")
                msg = f"{prior}\n{message}" if prior else message
            else:
                msg = message
            output = offline_generator(msg, max_length=200, num_return_sequences=1)
            text = output[0]["generated_text"].strip()
        else:
            text = message.strip()

    if text:
        if history is not None:
            history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": text},
            ])
        with open(CHAT_LOG, "a") as log:
            log.write(f"USER: {message}\nASSISTANT: {text}\n\n")
    return text


def evaluate_current_goals(use_notes: bool = False, mode: str = "auto") -> str:
    """Ask ChatGPT to review existing goals and return the feedback."""
    if not GOALS_FILE.exists():
        return "No goals to evaluate."
    with open(GOALS_FILE, "r") as f:
        goals = json.load(f)
    goal_text = "\n".join(f"- {g['goal']}" for g in goals)
    prompt = f"Please evaluate the following goals and suggest improvements:\n{goal_text}"
    return send_chatgpt_request(prompt, use_notes, mode)


def chat_loop(use_notes: bool = False, mode: str = "auto", phone: str | None = None, google_email: str | None = None):
    """Interactive chat loop with ChatGPT using conversational context."""
    if not sys.stdin.isatty():
        print("Interactive terminal required.")
        return
    prompt = (
        "Speak your question or type it. Press Enter on an empty line to exit."
    )
    print(prompt)
    history: List[Dict[str, str]] = []
    last_active = time.time()
    while True:
        if not imp_authenticator.idle_relog(last_active, phone, google_email):
            print("Re-authentication required.")
            break
        if chat_loop.use_speech:
            user_input = imp_speech_to_text.transcribe(offline=(mode != "online"))
        else:
            user_input = input("You: ").strip()
        if not user_input:
            break
        reply = send_chatgpt_request(user_input, use_notes, mode, history)
        last_active = time.time()
        if reply:
            print(f"GPT: {reply}")
        else:
            print("(No response)")


chat_loop.use_speech = False

def main():
    parser = argparse.ArgumentParser(description="IMP Goal Chatbot")
    parser.add_argument(
        "--mode",
        choices=["online", "offline", "auto"],
        default="auto",
        help="Select online, offline, or auto mode.",
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
    parser.add_argument(
        "--new-goal",
        metavar="TEXT",
        help="Send text to ChatGPT and store the resulting goal.",
    )
    parser.add_argument(
        "--term",
        choices=["short-term", "long-term"],
        default="long-term",
        help="Term for the new goal when using --new-goal",
    )
    parser.add_argument(
        "--speech",
        action="store_true",
        help="Capture input using speech-to-text",
    )
    parser.add_argument(
        "--google-email",
        help="Google account email for re-login",
    )
    parser.add_argument(
        "--phone",
        help="Phone number for Twilio verification",
    )
    args = parser.parse_args()

    mode = args.mode
    if mode == "auto":
        mode = decide_mode()

    if args.new_goal:
        from . import imp_goal_manager
        reply = send_chatgpt_request(args.new_goal, args.use_notes, mode)
        if reply:
            imp_goal_manager.add_new_goal(reply, args.term, "low", mode)
    elif args.evaluate:
        feedback = evaluate_current_goals(args.use_notes, mode)
        print(feedback)
    else:
        chat_loop.use_speech = args.speech
        chat_loop(args.use_notes, mode, args.phone, args.google_email)


if __name__ == "__main__":
    main()

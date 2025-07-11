import os
import json
from pathlib import Path
try:
    from transformers import pipeline
except Exception:
    pipeline = None
from typing import Optional

def decide_mode() -> str:
    """Return 'online' if ChatGPT credentials are available, else 'offline'."""
    if openai is not None and os.getenv("OPENAI_API_KEY"):
        return "online"
    return "offline"

try:
    import openai
except ImportError:
    openai = None

ROOT = Path(__file__).resolve().parents[1]
GOALS_FILE = ROOT / "logs" / "imp-goals.json"
PRIORITIES = ["low", "medium", "high"]

if pipeline is not None:
    offline_generator = pipeline("text-generation", model="gpt2")
else:
    offline_generator = None

def generate_text(prompt: str, mode: str = "auto") -> str:
    """Generate text from ChatGPT when available, otherwise use the local model."""
    if mode == "auto":
        mode = decide_mode()
    if mode == "online" and openai is not None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                )
                return resp["choices"][0]["message"]["content"].strip()
            except Exception as exc:
                print(f"[!] ChatGPT request failed: {exc}")
    if offline_generator is not None:
        output = offline_generator(prompt, max_length=500, num_return_sequences=1)
        return output[0]["generated_text"].strip()
    # fallback simple echo if no generator available
    return prompt.strip()

def get_existing_goals(term: Optional[str] = None):
    """Return all stored goals. Optionally filter by 'short-term' or 'long-term'."""
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        goals = json.load(f)
    if term:
        return [g for g in goals if g.get("term") == term]
    return goals

def add_new_goal(
    user_input: str,
    term: str = "long-term",
    priority: str = "low",
    mode: str = "online",
):
    """Add a new goal with the provided term. Priority defaults to lowest."""
    existing_goals = get_existing_goals()

    prompt = (
        f"User has provided the following input:\n{user_input}\n"
        "Convert this into a structured, actionable AI goal."
    )

    new_goal = generate_text(prompt, mode)

    if term not in ("short-term", "long-term"):
        term = "long-term"
    # All user-provided goals default to lowest priority
    priority = "low"

    existing_goals.append(
        {"goal": new_goal, "term": term, "priority": priority, "status": "pending"}
    )

    with open(GOALS_FILE, "w") as f:
        json.dump(existing_goals, f, indent=4)

    print(f"[+] New goal added: {new_goal}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IMP Goal Manager")
    parser.add_argument(
        "--mode",
        choices=["online", "offline", "auto"],
        default="auto",
    )
    args = parser.parse_args()

    user_input = input("You: ")
    term_choice = input("Is this goal short-term or long-term? [s/l]: ").strip().lower()
    term = "short-term" if term_choice.startswith("s") else "long-term"
    # Incoming goals are automatically set to lowest priority
    add_new_goal(user_input, term, "low", args.mode)

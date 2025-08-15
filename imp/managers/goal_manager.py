from pathlib import Path
import json
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parents[1]
GOALS_FILE = BASE_DIR / "logs" / "imp-goals.json"

_generator = pipeline("text-generation", model="gpt2")


def read_goals():
    if GOALS_FILE.exists():
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    return []


def add_goal(user_input):
    prompt = (
        f"User has provided the following input:\n{user_input}\n"
        "Convert this into a structured, actionable AI goal."
    )
    response = _generator(prompt, max_length=500, num_return_sequences=1)
    new_goal = response[0]["generated_text"]

    goals = read_goals()
    goals.append({"goal": new_goal, "status": "pending"})

    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=4)

    return new_goal

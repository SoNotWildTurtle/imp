import os
import json
import time
from transformers import pipeline

GOALS_FILE = "/root/imp/logs/imp-goals.json"

generator = pipeline("text-generation", model="gpt2")

def get_existing_goals():
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        return json.load(f)

def add_new_goal(user_input):
    existing_goals = get_existing_goals()

    prompt = f"""
    User has provided the following input:
    "{user_input}"

    Convert this into a structured, actionable AI goal.
    """

    response = generator(prompt, max_length=500, num_return_sequences=1)
    new_goal = response[0]['generated_text']

    existing_goals.append({"goal": new_goal, "status": "pending"})

    with open(GOALS_FILE, "w") as f:
        json.dump(existing_goals, f, indent=4)

    print(f"[+] New goal added: {new_goal}")

while True:
    user_input = input("You: ")
    add_new_goal(user_input)

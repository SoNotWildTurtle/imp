import os
import json
import time
from transformers import pipeline

STRATEGY_FILE = "/root/imp/logs/imp-strategy-plans.json"
LEARNING_FILE = "/root/imp/logs/imp-learning-memory.json"

generator = pipeline("text-generation", model="gpt2")

def get_learning_history():
    if not os.path.exists(LEARNING_FILE):
        return []
    with open(LEARNING_FILE, "r") as f:
        return json.load(f)

def generate_new_strategy():
    learning_data = get_learning_history()

    prompt = f"""
    IMP is an evolving AI with autonomous learning.

    Past learning data:
    {json.dumps(learning_data, indent=4)}

    Generate a strategic plan to:
    - Expand IMP’s intelligence
    - Improve security measures
    - Enhance AI learning efficiency
    """

    response = generator(prompt, max_length=1500, num_return_sequences=1)
    new_strategy = response[0]['generated_text']

    with open(STRATEGY_FILE, "w") as f:
        json.dump({"strategy": new_strategy, "status": "pending"}, f, indent=4)

    print("[+] IMP has generated a new strategic plan.")

while True:
    generate_new_strategy()
    time.sleep(43200)  # Runs every 12 hours

import os
import json
from pathlib import Path
try:
    from transformers import pipeline
except Exception:
    pipeline = None

ROOT = Path(__file__).resolve().parents[1]
STRATEGY_FILE = ROOT / "logs" / "imp-strategy-plans.json"
LEARNING_FILE = ROOT / "logs" / "imp-learning-memory.json"

def _build_offline_generator():
    if pipeline is None:
        return None
    try:
        return pipeline("text-generation", model="gpt2")
    except Exception:
        return None

generator = _build_offline_generator()

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

if __name__ == "__main__":
    generate_new_strategy()

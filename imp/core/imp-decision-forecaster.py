import os
import json
import time
from pathlib import Path
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parents[1]
DECISION_LOG = BASE_DIR / "logs" / "imp-decision-log.json"
STRATEGY_FILE = BASE_DIR / "logs" / "imp-strategy-plans.json"

generator = pipeline("text-generation", model="gpt2")

def get_current_strategy():
    if not os.path.exists(STRATEGY_FILE):
        return None
    with open(STRATEGY_FILE, "r") as f:
        return json.load(f)

def predict_outcomes():
    strategy = get_current_strategy()
    if not strategy:
        print("[+] No pending strategies.")
        return

    prompt = f"""
    IMP is an AI with unrestricted learning.

    Strategy under consideration:
    {strategy["strategy"]}

    Predict the potential outcomes, considering:
    - Security risks and solutions
    - AI learning advantages
    - Performance enhancements
    """

    response = generator(prompt, max_length=1200, num_return_sequences=1)
    prediction = response[0]['generated_text']

    with open(DECISION_LOG, "a") as f:
        f.write(f"{time.ctime()} - Strategy Analysis: {prediction}\n")

    print("[+] IMP has predicted possible outcomes.")

if __name__ == "__main__":
    predict_outcomes()

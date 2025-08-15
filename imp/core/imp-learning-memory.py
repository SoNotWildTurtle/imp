import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARNING_FILE = ROOT / "logs" / "imp-learning-memory.json"
DECISIONS_FILE = ROOT / "logs" / "imp-decision-log.json"

def get_past_decisions():
    if not os.path.exists(DECISIONS_FILE):
        return []
    with open(DECISIONS_FILE, "r") as f:
        return json.load(f)

def store_learnings():
    past_decisions = get_past_decisions()
    
    if not past_decisions:
        print("[+] No new knowledge to store.")
        return
    
    learning_memory = []
    if os.path.exists(LEARNING_FILE):
        with open(LEARNING_FILE, "r") as f:
            learning_memory = json.load(f)
    
    for decision in past_decisions:
        learning_memory.append({
            "goal": decision.get("goal", "unknown"),
            "plan": decision.get("plan", []),
            "outcome": "pending"
        })

    with open(LEARNING_FILE, "w") as f:
        json.dump(learning_memory, f, indent=4)

    print("[+] IMP has updated its knowledge base.")

if __name__ == "__main__":
    store_learnings()

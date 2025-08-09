import os
import json
import time
from pathlib import Path
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parents[1]
PERFORMANCE_LOG = BASE_DIR / "logs" / "imp-performance.json"
LEARNING_MEMORY = BASE_DIR / "logs" / "imp-learning-memory.json"
EVOLUTION_PLAN_FILE = BASE_DIR / "logs" / "imp-evolution-plan.json"

generator = pipeline("text-generation", model="gpt2")


def gather_context():
    context = {}
    if os.path.exists(PERFORMANCE_LOG):
        with open(PERFORMANCE_LOG, "r") as f:
            context["performance"] = json.load(f)
    if os.path.exists(LEARNING_MEMORY):
        with open(LEARNING_MEMORY, "r") as f:
            context["memory"] = json.load(f)
    return context


def generate_evolution_plan():
    context = gather_context()
    prompt = f"""
    IMP seeks to continuously improve and evolve towards general intelligence.
    Current context:
    {json.dumps(context, indent=4)}

    Propose a strategic plan for further self-development focusing on:
    - knowledge expansion
    - algorithmic advancements
    - resource acquisition
    """
    response = generator(prompt, max_length=800, num_return_sequences=1)
    plan = response[0]["generated_text"]
    with open(EVOLUTION_PLAN_FILE, "w") as f:
        json.dump({"timestamp": time.ctime(), "plan": plan}, f, indent=4)
    print("[+] Evolution plan generated.")


if __name__ == "__main__":
    generate_evolution_plan()

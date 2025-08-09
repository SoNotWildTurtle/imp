"""Adaptive planner that can operate online or offline.

If an OpenAI API key is available the planner will request ChatGPT to break
down a directive into subgoals. When no network model is present a simple
heuristic splitter is used instead, keeping goal planning functional offline.
"""

import json
import os
import re
import time
from pathlib import Path
from typing import List, Dict

try:  # optional dependency for online planning
    import openai
except ImportError:  # pragma: no cover - networkless environments
    openai = None

try:  # optional offline generator
    from transformers import pipeline
except Exception:  # pragma: no cover - dependency may be absent
    pipeline = None

ROOT = Path(__file__).resolve().parents[1]
PLAN_FILE = ROOT / "logs" / "imp-strategy-plans.json"

# track last request time for crude rate limiting
OPENAI_LAST_REQUEST: Dict[str, float] = {}
OPENAI_RPM: Dict[str, int] = {
    "gpt-3.5-turbo": 60,
    "gpt-4": 40,
}

def _build_offline_generator():
    if pipeline is None:
        return None
    try:
        return pipeline("text-generation", model="gpt2")
    except Exception:
        return None

offline_generator = _build_offline_generator()


def decide_mode() -> str:
    """Return 'online' if the OpenAI key is set, otherwise 'offline'."""
    if openai is not None and os.getenv("OPENAI_API_KEY"):
        return "online"
    return "offline"


def _throttle(model: str) -> None:
    """Sleep to respect OpenAI rate limits divided by four."""
    rpm = OPENAI_RPM.get(model, 60)
    interval = 60 / (rpm / 4)
    last = OPENAI_LAST_REQUEST.get(model, 0)
    elapsed = time.time() - last
    if elapsed < interval:
        time.sleep(interval - elapsed)
    OPENAI_LAST_REQUEST[model] = time.time()


def _split_directive(directive: str) -> List[str]:
    """Split a high-level directive into rough subgoals."""
    parts = re.split(r"[.;]| and | then ", directive)
    return [p.strip() for p in parts if p.strip()]


def _weigh_goal(goal: str) -> float:
    """Estimate a weight for a subgoal based on length heuristics."""
    length = len(goal.split())
    benefit = min(length / 5.0, 1.0)
    feasibility = max(0.1, 1.0 - length / 20.0)
    weight = round((benefit + feasibility) / 2.0, 2)
    return weight


def build_plan(directive: str, mode: str = "auto") -> List[Dict[str, float]]:
    """Return a list of weighted subgoals derived from the directive.

    In online mode the directive is sent to ChatGPT which returns a numbered
    list of subgoals. Offline mode falls back to heuristic splitting.
    """
    if mode == "auto":
        mode = decide_mode()

    if mode == "online" and openai is not None and os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        try:
            _throttle("gpt-3.5-turbo")
            prompt = (
                "Break the following directive into a short numbered list of "
                "actionable subgoals:\n" + directive
            )
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp["choices"][0]["message"]["content"]
            lines = [re.sub(r"^[0-9]+[.)]\s*", "", l).strip() for l in text.splitlines()]
            subgoals = [l for l in lines if l]
            return [{"goal": sg, "weight": _weigh_goal(sg)} for sg in subgoals]
        except Exception:
            pass

    # Offline heuristic approach
    subgoals = _split_directive(directive)
    return [{"goal": sg, "weight": _weigh_goal(sg)} for sg in subgoals]


def save_plan(plan: List[Dict[str, float]]) -> None:
    PLAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PLAN_FILE, "w") as f:
        json.dump(plan, f, indent=4)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IMP Adaptive Planner")
    parser.add_argument(
        "--mode",
        choices=["online", "offline", "auto"],
        default="auto",
        help="Choose online, offline, or auto planning mode",
    )
    args = parser.parse_args()

    directive = input("Enter high-level directive: ")
    plan = build_plan(directive, args.mode)
    save_plan(plan)
    for item in plan:
        print(f"{item['goal']} (weight={item['weight']})")

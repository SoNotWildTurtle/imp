import json
import re
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).resolve().parents[1]
PLAN_FILE = ROOT / "logs" / "imp-strategy-plans.json"


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


def build_plan(directive: str) -> List[Dict[str, float]]:
    """Return a list of weighted subgoals derived from the directive."""
    subgoals = _split_directive(directive)
    plan = []
    for sg in subgoals:
        plan.append({"goal": sg, "weight": _weigh_goal(sg)})
    return plan


def save_plan(plan: List[Dict[str, float]]) -> None:
    PLAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PLAN_FILE, "w") as f:
        json.dump(plan, f, indent=4)


if __name__ == "__main__":
    directive = input("Enter high-level directive: ")
    plan = build_plan(directive)
    save_plan(plan)
    for item in plan:
        print(f"{item['goal']} (weight={item['weight']})")

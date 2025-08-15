from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MOOD_PATH = ROOT / "core" / "imp-mood-manager.py"
GOAL_MANAGER_PATH = ROOT / "core" / "imp-goal-manager.py"

spec = importlib.util.spec_from_file_location("imp_mood_manager", MOOD_PATH)
mood_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mood_manager)

spec_g = importlib.util.spec_from_file_location("imp_goal_manager", GOAL_MANAGER_PATH)
goal_manager = importlib.util.module_from_spec(spec_g)
spec_g.loader.exec_module(goal_manager)


def generate_motivations() -> None:
    """Create self-motivated goals based on current mood."""
    mood = mood_manager.load_mood()
    existing = [g["goal"] for g in goal_manager.get_existing_goals()]

    if mood < 0 and "Improve mood through positive tasks" not in existing:
        goal_manager.add_new_goal(
            "Improve mood through positive tasks",
            term="short-term",
            priority="low",
            mode="offline",
        )
    elif mood > 0.5 and "Explore advanced self-improvement techniques" not in existing:
        goal_manager.add_new_goal(
            "Explore advanced self-improvement techniques",
            term="long-term",
            priority="low",
            mode="offline",
        )


if __name__ == "__main__":
    generate_motivations()

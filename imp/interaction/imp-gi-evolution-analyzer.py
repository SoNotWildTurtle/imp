from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))
from managers import log_manager
CONFIG_DIR = BASE_DIR / "config" / "gi"

# Default modules recommended for every GI
DEFAULT_MODULES = [
    "imp-gi-memory.py",
    "imp-gi-task-manager.py",
    "imp-gi-self-evolver.py",
    "imp-gi-knowledge.py",
    "imp-gi-skill-tracker.py",
    "imp-gi-performance.py",
    "imp-gi-safety.py",
    "imp-gi-risk-analyzer.py",
    "imp-gi-planner.py",
    "imp-gi-comm-log.py",
    "imp-gi-implementation-log.py",
    "imp-gi-request.py",
    "imp-gi-feedback.py",
    "imp-gi-personality.py",
]

def analyze_gi(name: str):
    """Analyze a GI's existing modules and log suggestions."""
    config_path = CONFIG_DIR / f"{name}.json"
    if not config_path.exists():
        print(f"⚠️ No configuration found for {name}.")
        return
    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Invalid configuration file.")
            return
    modules = config.get("modules", [])
    skills = config.get("skills", [])
    suggestions = []
    for mod in DEFAULT_MODULES:
        if mod not in modules:
            suggestions.append(f"Consider adding {mod}")
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "modules": modules,
        "skills": skills,
        "suggestions": suggestions,
    }
    log_manager.append_log("gi_evolution_analysis", entry)
    print(f"[+] Logged evolution analysis for {name}.")
    return entry


if __name__ == "__main__":
    target = input("GI name to analyze: ").strip()
    if target:
        analyze_gi(target)

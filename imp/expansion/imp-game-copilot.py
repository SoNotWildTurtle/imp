"""Game Copilot for IMP.

Acts as a simple copilot so IMP can learn new games and craft
Sword Art Online-inspired dreamscapes for experimental blockchain games.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
GAMES_FILE = LOG_DIR / "imp-games.json"
DREAM_FILE = LOG_DIR / "imp-dreamscape.json"


def _load(path: Path) -> dict:
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}


def _save(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def learn_game(name: str, rules: str) -> dict:
    """Store rules for a new game.

    Returns the stored entry so other modules can reference it.
    """
    games = _load(GAMES_FILE)
    games[name] = {
        "rules": rules,
        "learned": datetime.utcnow().isoformat(),
    }
    _save(GAMES_FILE, games)
    return games[name]


def build_dreamscape(name: str) -> dict:
    """Create a simple Sword Art Online-inspired dreamscape for a game.

    This placeholder turns game rules into a basic SAO scene string and
    records it so IMP can reference the dreamscape later.
    """
    games = _load(GAMES_FILE)
    rules = games.get(name, {}).get("rules", "")
    dream = _load(DREAM_FILE)
    dream[name] = {
        "based_on": rules,
        "sao_theme": f"{name}-sao-field",
        "created": datetime.utcnow().isoformat(),
    }
    _save(DREAM_FILE, dream)
    return dream[name]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IMP Game Copilot")
    parser.add_argument("name", help="Name of the game")
    parser.add_argument("--rules", default="", help="Rules for the game")
    parser.add_argument("--dream", action="store_true", help="Build a dreamscape instead of learning")
    args = parser.parse_args()

    if args.dream:
        print(build_dreamscape(args.name))
    else:
        print(learn_game(args.name, args.rules))

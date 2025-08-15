from pathlib import Path
import json
import time

INSIGHTS_FILE = Path(__file__).resolve().parents[1] / "logs" / "imp-conversation-insights.json"

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
EXPERIENCE_FILE = BASE_DIR / "logs" / "imp-gi-experience.json"


def load_insights():
    if not INSIGHTS_FILE.exists():
        return []
    with open(INSIGHTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def load_profiles():
    if not PROFILE_FILE.exists():
        return []
    with open(PROFILE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def update_experience():
    profiles = load_profiles()
    stats = {"count": len(profiles), "skills": {}, "traits": {}, "keywords": {}}
    for p in profiles:
        for skill in p.get("skills", []):
            stats["skills"][skill] = stats["skills"].get(skill, 0) + 1
        for trait in p.get("personality", []):
            stats["traits"][trait] = stats["traits"].get(trait, 0) + 1
    for insight in load_insights():
        for word, count in insight.get("top_words", []):
            stats["keywords"][word] = stats["keywords"].get(word, 0) + count
    EXPERIENCE_FILE.parent.mkdir(exist_ok=True)
    with open(EXPERIENCE_FILE, "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats
        }, f, indent=4)
    print(f"[+] GI experience updated with {stats['count']} profiles")


def get_experience_stats():
    """Return aggregated skill, trait and keyword statistics."""
    if not EXPERIENCE_FILE.exists():
        return {"count": 0, "skills": {}, "traits": {}, "keywords": {}}
    try:
        with open(EXPERIENCE_FILE, "r") as f:
            data = json.load(f)
            return data.get("stats", {"count": 0, "skills": {}, "traits": {}, "keywords": {}})
    except json.JSONDecodeError:
        return {"count": 0, "skills": {}, "traits": {}, "keywords": {}}


def summarize_experience(n: int = 3) -> str:
    """Return a short summary of the most common skills, traits and keywords."""
    stats = get_experience_stats()
    skills = sorted(stats.get("skills", {}).items(), key=lambda x: x[1], reverse=True)
    traits = sorted(stats.get("traits", {}).items(), key=lambda x: x[1], reverse=True)
    keywords = sorted(stats.get("keywords", {}).items(), key=lambda x: x[1], reverse=True)
    top_skills = ", ".join([s[0] for s in skills[:n]]) if skills else "none"
    top_traits = ", ".join([t[0] for t in traits[:n]]) if traits else "none"
    top_keywords = ", ".join([k[0] for k in keywords[:n]]) if keywords else "none"
    return (
        f"Profiles: {stats.get('count', 0)} | "
        f"Top skills: {top_skills} | Top traits: {top_traits} | "
        f"Top words: {top_keywords}"
    )


if __name__ == "__main__":
    update_experience()

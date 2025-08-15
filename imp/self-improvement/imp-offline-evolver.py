"""Analyze existing logs to propose offline self-evolution ideas."""

from datetime import datetime
from statistics import mean
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))
from managers import log_manager


def run_offline_evolver():
    """Summarize logs and recommend skill improvements for offline evolution."""
    skills = log_manager.read_logs("gi_skills")
    performance = log_manager.read_logs("gi_performance")
    insights = log_manager.read_logs("conversation_insights")

    existing = {s.get("skill") for s in skills}
    top_words = []
    if insights:
        top_words = [w for w, _ in insights[-1].get("top_words", [])]
    suggested = [w for w in top_words if w not in existing]

    avg_cpu = mean([p.get("cpu", 0) for p in performance]) if performance else 0
    avg_mem = mean([p.get("memory", 0) for p in performance]) if performance else 0

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "skill_count": len(skills),
        "performance_entries": len(performance),
        "avg_cpu": avg_cpu,
        "avg_memory": avg_mem,
        "suggested_skills": suggested,
        "note": "Offline evolution analysis recorded",
    }
    log_manager.append_log("offline_evolution", entry)
    return entry


if __name__ == "__main__":
    run_offline_evolver()
    print("[+] Offline evolution analysis logged")

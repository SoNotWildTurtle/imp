from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]

LOG_FILES = {
    "activity": BASE_DIR / "logs" / "imp-activity-log.json",
    "security": BASE_DIR / "logs" / "imp-security-log.json",
    "safety": BASE_DIR / "logs" / "imp-safety-log.json",
    "updates": BASE_DIR / "logs" / "imp-update-log.json",
    "decisions": BASE_DIR / "logs" / "imp-decision-log.json",
    "performance": BASE_DIR / "logs" / "imp-performance.json",
    "integrity": BASE_DIR / "logs" / "imp-integrity-log.json",
    "metacognition": BASE_DIR / "logs" / "imp-metacognition-log.json",
    "gi_implementation": BASE_DIR / "logs" / "imp-gi-implementation-log.json",
    "gi_skills": BASE_DIR / "logs" / "imp-gi-skills.json",
    "gi_performance": BASE_DIR / "logs" / "imp-gi-performance.json",
    "gi_safety": BASE_DIR / "logs" / "imp-gi-safety.json",
    "gi_risks": BASE_DIR / "logs" / "imp-gi-risks.json",
    "gi_plans": BASE_DIR / "logs" / "imp-gi-plans.json",
    "gi_requests": BASE_DIR / "logs" / "imp-gi-requests.json",
    "gi_feedback": BASE_DIR / "logs" / "imp-gi-feedback.json",
    "gi_personality": BASE_DIR / "logs" / "imp-gi-personality.json",
    "conversation_insights": BASE_DIR / "logs" / "imp-conversation-insights.json",
    "gi_snapshots": BASE_DIR / "logs" / "imp-gi-snapshots.json",
    "gi_upgrade_decisions": BASE_DIR / "logs" / "imp-gi-upgrade-decisions.json",
    "gi_evolution_analysis": BASE_DIR / "logs" / "imp-gi-evolution-analysis.json",
    "offline_evolution": BASE_DIR / "logs" / "imp-offline-evolution.json",
    "threats": BASE_DIR / "logs" / "imp-threat-log.json",
    "ai_countermeasures": BASE_DIR / "logs" / "imp-ai-countermeasures.json",
    "remote_terminal": BASE_DIR / "logs" / "imp-remote-terminal.json",
    "startup_verification": BASE_DIR / "logs" / "imp-startup-verification.json",
}


def read_logs(log_type):
    path = LOG_FILES.get(log_type)
    if not path:
        raise ValueError("Invalid log type")
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []


def append_log(log_type, entry):
    path = LOG_FILES.get(log_type)
    if not path:
        raise ValueError("Invalid log type")
    logs = read_logs(log_type)
    logs.append(entry)
    with open(path, "w") as f:
        json.dump(logs, f, indent=4)


def clear_logs(log_type):
    path = LOG_FILES.get(log_type)
    if not path:
        raise ValueError("Invalid log type")
    with open(path, "w") as f:
        json.dump([], f, indent=4)

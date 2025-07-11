from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_LOG = ROOT / "logs" / "imp-model-analysis.json"


def _load_last_diff():
    if not ANALYSIS_LOG.exists():
        return None
    try:
        with open(ANALYSIS_LOG, "r") as f:
            data = json.load(f)
        return data[-1]["diff"] if data else None
    except Exception:
        return None


def spatiotemporal_confidence() -> float:
    """Estimate confidence in the self-evolved network based on recent diffs."""
    diff = _load_last_diff()
    if not diff:
        return 0.0
    avg_change = (abs(diff.get("w1_diff", 0)) + abs(diff.get("w2_diff", 0))) / 2
    confidence = max(0.0, 1.0 - avg_change)
    return confidence


def choose_generation_mode(off_model_available: bool) -> str:
    """Return 'online' or 'offline' depending on confidence and API access."""
    api_available = os.getenv("OPENAI_API_KEY") is not None
    confidence = spatiotemporal_confidence()
    if confidence > 0.6 and off_model_available:
        return "offline"
    if api_available:
        return "online"
    return "offline" if off_model_available else "online"


def evaluate_request_quality(text: str) -> float:
    """Simple heuristic to score generation output."""
    score = 1.0
    if "Traceback" in text or "ERROR" in text.upper():
        score -= 0.5
    if len(text.strip()) < 20:
        score -= 0.3
    return max(0.0, score)

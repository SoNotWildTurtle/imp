from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

# create a small analysis log for testing
ANALYSIS_LOG = ROOT / "logs" / "imp-model-analysis.json"

import sys
sys.path.append(str(ROOT / "self-improvement"))
import imp_mode_advisor as advisor

def test_spatiotemporal_confidence():
    if not ANALYSIS_LOG.exists():
        sample = [{"diff": {"w1_diff": 0.1, "w2_diff": 0.1}}]
        with open(ANALYSIS_LOG, "w") as f:
            json.dump(sample, f)
    conf = advisor.spatiotemporal_confidence()
    assert isinstance(conf, float)
    print("Confidence:", conf)

test_spatiotemporal_confidence()

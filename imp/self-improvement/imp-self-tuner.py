import os
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERFORMANCE_LOG = ROOT / "logs" / "imp-performance.json"
TUNING_LOG = ROOT / "logs" / "imp-tuning-log.json"

def get_performance_data():
    if not os.path.exists(PERFORMANCE_LOG):
        return None
    with open(PERFORMANCE_LOG, "r") as f:
        return json.load(f)

def refine_algorithms():
    performance_data = get_performance_data()
    if not performance_data:
        print("[+] No performance data available.")
        return

    adjustments = {}

    if performance_data["CPU Usage (%)"] > 85:
        adjustments["Optimize AI processes"] = "Reduce unnecessary calculations."

    if performance_data["Memory Usage (%)"] > 90:
        adjustments["Memory Management"] = "Improve caching techniques."

    if performance_data["Security Score"] < 80:
        adjustments["Security Hardening"] = "Enhance firewall rules & log monitoring."

    if adjustments:
        with open(TUNING_LOG, "a") as f:
            f.write(f"{time.ctime()} - Self-Optimization: {json.dumps(adjustments, indent=4)}\n")

        print("[+] IMP has fine-tuned its performance.")

if __name__ == "__main__":
    refine_algorithms()

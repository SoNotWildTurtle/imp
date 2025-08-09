import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
print("🔥 Cimp AI is initializing...")

# Start core AI processes
subprocess.Popen(["python3", str(BASE_DIR / "core" / "imp-learning-memory.py")])
subprocess.Popen(["python3", str(BASE_DIR / "core" / "imp-strategy-generator.py")])
subprocess.Popen(["python3", str(BASE_DIR / "self-improvement" / "imp-code-updater.py")])
subprocess.Popen(["python3", str(BASE_DIR / "security" / "imp-security-optimizer.py")])
subprocess.Popen(["python3", str(BASE_DIR / "expansion" / "imp-cluster-manager.py")])
print("🚀 Cimp is now running autonomously.")

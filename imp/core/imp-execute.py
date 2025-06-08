from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

print("🔥 IMP AI is initializing...")

# Start core AI processes from the repository root
subprocess.Popen(["python3", str(ROOT / "core" / "imp-learning-memory.py")])
subprocess.Popen(["python3", str(ROOT / "core" / "imp-strategy-generator.py")])
subprocess.Popen(["python3", str(ROOT / "self-improvement" / "imp-code-updater.py")])
subprocess.Popen(["python3", str(ROOT / "security" / "imp-security-optimizer.py")])
subprocess.Popen(["python3", str(ROOT / "expansion" / "imp-cluster-manager.py")])

print("🚀 IMP is now running autonomously.")

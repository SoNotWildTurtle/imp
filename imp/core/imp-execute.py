import os
import subprocess

print("🔥 IMP AI is initializing...")

# Determine the project root dynamically instead of relying on a fixed path.  
# This makes the script runnable from any location.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Start core AI processes
subprocess.Popen(["python3", os.path.join(BASE_DIR, "core", "imp-learning-memory.py")])
subprocess.Popen(["python3", os.path.join(BASE_DIR, "core", "imp-strategy-generator.py")])
subprocess.Popen(["python3", os.path.join(BASE_DIR, "self-improvement", "imp-code-updater.py")])
subprocess.Popen(["python3", os.path.join(BASE_DIR, "security", "imp-security-optimizer.py")])
subprocess.Popen(["python3", os.path.join(BASE_DIR, "expansion", "imp-cluster-manager.py")])

print("🚀 IMP is now running autonomously.")

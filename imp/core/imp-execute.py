import os
import subprocess

print("🔥 IMP AI is initializing...")

# Start core AI processes
subprocess.Popen(["python3", "/root/imp/core/imp-learning-memory.py"])
subprocess.Popen(["python3", "/root/imp/core/imp-strategy-generator.py"])
subprocess.Popen(["python3", "/root/imp/self-improvement/imp-code-updater.py"])
subprocess.Popen(["python3", "/root/imp/security/imp-security-optimizer.py"])
subprocess.Popen(["python3", "/root/imp/expansion/imp-cluster-manager.py"])

print("🚀 IMP is now running autonomously.")

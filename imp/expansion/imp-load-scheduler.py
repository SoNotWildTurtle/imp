import os
import json
import subprocess
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
TASKS_FILE = ROOT / "logs" / "imp-scheduled-tasks.json"
CLUSTER_NODES_FILE = ROOT / "config" / "imp-cluster-nodes.json"
DQ_PATH = ROOT / "expansion" / "imp-distributed-queue.py"
spec = importlib.util.spec_from_file_location('dq', DQ_PATH)
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

def get_available_nodes():
    nodes = []
    if os.path.exists(CLUSTER_NODES_FILE):
        with open(CLUSTER_NODES_FILE, "r") as f:
            nodes = json.load(f)

    available_nodes = []
    for node in nodes:
        response = subprocess.run(f"ping -c 1 {node}", shell=True, capture_output=True, text=True)
        if response.returncode == 0:
            available_nodes.append(node)

    return available_nodes

def schedule_tasks():
    remote_dir = os.environ.get("IMP_REMOTE_DIR", "/root/imp")
    tasks = [
        f"python3 {remote_dir}/self-improvement/imp-code-updater.py",
        f"python3 {remote_dir}/security/imp-security-optimizer.py",
        f"python3 {remote_dir}/expansion/imp-resource-balancer.py",
    ]

    nodes = get_available_nodes()

    if not nodes:
        print("No available nodes to distribute tasks.")
        return

    assigned_tasks = {}
    for task in tasks:
        dq.add_task(task)
    assigned_tasks = dq.assign_tasks(nodes)
    for node, cmds in assigned_tasks.items():
        for cmd in cmds:
            subprocess.run(f"ssh {node} '{cmd}'", shell=True)

    with open(TASKS_FILE, "w") as f:
        json.dump(assigned_tasks, f, indent=4)

    print("[+] Tasks scheduled across AI nodes.")

if __name__ == "__main__":
    schedule_tasks()

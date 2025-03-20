import os
import json
import time
import subprocess

TASKS_FILE = "/root/imp/logs/imp-scheduled-tasks.json"
CLUSTER_NODES_FILE = "/root/imp/config/imp-cluster-nodes.json"

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
    tasks = [
        "python3 /root/imp/self-improvement/imp-code-updater.py",
        "python3 /root/imp/security/imp-security-optimizer.py",
        "python3 /root/imp/expansion/imp-resource-balancer.py"
    ]

    nodes = get_available_nodes()

    if not nodes:
        print("⚠️ No available nodes to distribute tasks.")
        return

    assigned_tasks = {}
    for i, task in enumerate(tasks):
        node = nodes[i % len(nodes)]
        subprocess.run(f"ssh {node} '{task}'", shell=True)
        assigned_tasks[task] = node

    with open(TASKS_FILE, "w") as f:
        json.dump(assigned_tasks, f, indent=4)

    print("[+] Tasks scheduled across AI nodes.")

while True:
    schedule_tasks()
    time.sleep(7200)  # Runs every 2 hours

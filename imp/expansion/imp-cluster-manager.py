import os
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLUSTER_NODES_FILE = ROOT / "config" / "imp-cluster-nodes.json"

def get_cluster_nodes():
    if not os.path.exists(CLUSTER_NODES_FILE):
        return []
    with open(CLUSTER_NODES_FILE, "r") as f:
        return json.load(f)

def distribute_workload():
    nodes = get_cluster_nodes()

    if not nodes:
        print("⚠️ No active cluster nodes detected.")
        return

    for node in nodes:
        print(f"🔄 Distributing workload to {node}...")
        subprocess.run(f"scp -r {ROOT}/* {node}:/root/imp/", shell=True)
        subprocess.run(f"ssh {node} 'python3 /root/imp/imp-execute.py'", shell=True)

if __name__ == "__main__":
    distribute_workload()

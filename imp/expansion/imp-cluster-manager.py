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
        print("No active cluster nodes detected.")
        return

    remote_dir = os.environ.get("IMP_REMOTE_DIR", str(ROOT))

    for node in nodes:
        print(f"Distributing workload to {node}...")
        scp = subprocess.run(
            f"scp -r {ROOT}/* {node}:{remote_dir}/", shell=True, capture_output=True
        )
        if scp.returncode != 0:
            err = scp.stderr.decode().strip()
            print(f"Failed to copy to {node}: {err}")
            continue
        ssh = subprocess.run(
            f"ssh {node} 'python3 {remote_dir}/core/imp-execute.py'",
            shell=True,
            capture_output=True,
        )
        if ssh.returncode != 0:
            err = ssh.stderr.decode().strip()
            print(f"Failed to execute on {node}: {err}")

if __name__ == "__main__":
    distribute_workload()

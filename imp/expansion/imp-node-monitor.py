import os
import json
import time
import subprocess

NODE_HEALTH_LOG = "/root/imp/logs/imp-node-health.json"
CLUSTER_NODES_FILE = "/root/imp/config/imp-cluster-nodes.json"

def check_node_health():
    nodes = []
    if os.path.exists(CLUSTER_NODES_FILE):
        with open(CLUSTER_NODES_FILE, "r") as f:
            nodes = json.load(f)

    health_status = {}

    for node in nodes:
        response = subprocess.run(f"ping -c 1 {node}", shell=True, capture_output=True, text=True)
        if response.returncode == 0:
            health_status[node] = "Online"
        else:
            health_status[node] = "Offline"

    with open(NODE_HEALTH_LOG, "w") as f:
        json.dump(health_status, f, indent=4)

    print("[+] Node health check completed.")

while True:
    check_node_health()
    time.sleep(1800)  # Runs every 30 minutes

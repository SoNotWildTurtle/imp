import os
import json
import time
import subprocess

RESOURCE_LOG = "/root/imp/logs/imp-resource-usage.json"
CLUSTER_NODES_FILE = "/root/imp/config/imp-cluster-nodes.json"

def get_system_usage():
    cpu_usage = os.popen("grep 'cpu ' /proc/stat").read().strip()
    memory_usage = os.popen("free -m").read().strip()
    
    return {
        "CPU": cpu_usage,
        "Memory": memory_usage
    }

def balance_resources():
    nodes = []
    if os.path.exists(CLUSTER_NODES_FILE):
        with open(CLUSTER_NODES_FILE, "r") as f:
            nodes = json.load(f)

    usage = get_system_usage()
    
    for node in nodes:
        print(f"📊 Checking resource balance for {node}...")
        subprocess.run(f"ssh {node} 'python3 /root/imp/expansion/imp-resource-balancer.py'", shell=True)

    with open(RESOURCE_LOG, "w") as f:
        json.dump(usage, f, indent=4)

while True:
    balance_resources()
    time.sleep(3600)  # Runs every hour

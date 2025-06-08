import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NODE_HEALTH_LOG = os.path.join(BASE_DIR, "logs", "imp-node-health.json")

def test_node_health():
    print("🔗 Checking AI Cluster Nodes...")
    
    with open(NODE_HEALTH_LOG, "r") as f:
        nodes = json.load(f)
    
    assert all(status == "Online" for status in nodes.values()), "⚠️ Some AI nodes are offline!"
    
    print("✅ AI Cluster Test Passed!")

test_node_health()

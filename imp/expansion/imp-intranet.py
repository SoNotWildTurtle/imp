from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parents[1]
INTRANET_CONFIG = ROOT / "config" / "imp-intranet.json"

# this needs to be hyper-secure, and the API on your end needs to only allow specific commands to be executed to allow for specific modes of communication -alex ps. another good idea

def create_intranet(nodes):
    """Create a basic intranet configuration listing node IPs."""
    config = {"nodes": nodes}
    with open(INTRANET_CONFIG, "w") as f:
        json.dump(config, f, indent=4)
    print(f"🌐 Intranet created with nodes: {nodes}")


def sanitize_packet(packet):
    """Modify packets using Scapy for on-the-fly sanitization."""
    try:
        from scapy.all import IP
    except ImportError:
        print("⚠️ Scapy not installed; skipping packet sanitization.")
        return packet
    if IP in packet:
        packet[IP].ttl = 64
    return packet


def execute_aliased_command(command):
    """Execute a whitelisted command via the intranet API."""
    allowed = {"ping", "traceroute"}
    alias = command.split()[0]
    if alias not in allowed:
        raise ValueError("Command not allowed")
    os.system(command)

if __name__ == "__main__":
    create_intranet(["127.0.0.1"])

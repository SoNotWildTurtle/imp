from __future__ import annotations
import json
import importlib.util
import ipaddress
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODES_FILE = ROOT / 'config' / 'imp-cluster-nodes.json'
COMMUNICATOR_PATH = ROOT / 'expansion' / 'imp-node-communicator.py'

spec = importlib.util.spec_from_file_location('node_comm', COMMUNICATOR_PATH)
node_comm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(node_comm)

send_secure_message = node_comm.send_secure_message
secure_communication = node_comm.secure_communication


def register_node(host: str) -> None:
    """Add a node to the cluster list if the host is valid."""
    try:
        ipaddress.ip_address(host)
    except ValueError:
        # basic hostname check
        if not host or len(host.split('.')) < 2:
            print('Invalid host address')
            return

    nodes = []
    if NODES_FILE.exists():
        with open(NODES_FILE, 'r') as f:
            nodes = json.load(f)
    if host not in nodes:
        nodes.append(host)
        with open(NODES_FILE, 'w') as f:
            json.dump(nodes, f, indent=4)

def list_nodes() -> list[str]:
    """Return a list of registered nodes."""
    if not NODES_FILE.exists():
        return []
    with open(NODES_FILE, 'r') as f:
        return json.load(f)

def remove_node(host: str) -> None:
    """Remove a node from the cluster list."""
    if not NODES_FILE.exists():
        return
    with open(NODES_FILE, 'r') as f:
        nodes = json.load(f)
    if host in nodes:
        nodes.remove(host)
        with open(NODES_FILE, 'w') as f:
            json.dump(nodes, f, indent=4)


def manage_nodes(command: str | None = None, host: str | None = None, listen: bool = False) -> None:
    """Send commands securely or listen for incoming tasks."""
    if listen:
        secure_communication()
        return

    if command and host:
        nodes = []
        if NODES_FILE.exists():
            with open(NODES_FILE, 'r') as f:
                nodes = json.load(f)
        if host not in nodes:
            print('Host not registered; aborting command')
            return
        try:
            resp = send_secure_message(host, command)
            print(f'Response from {host}: {resp}')
        except Exception as exc:
            print(f'Failed to send command: {exc}')
    else:
        print('Usage: manage_nodes(command="cmd", host="host") or listen=True')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='IMP Secure Node Manager')
    parser.add_argument('--register', help='Add a node to the cluster list')
    parser.add_argument('--remove', help='Remove a node from the cluster list')
    parser.add_argument('--list', action='store_true', help='List registered nodes')
    parser.add_argument('--command', help='Command to send to a node')
    parser.add_argument('--host', help='Target host for the command')
    parser.add_argument('--listen', action='store_true', help='Listen for tasks')
    args = parser.parse_args()

    if args.register:
        register_node(args.register)
    if args.remove:
        remove_node(args.remove)
    if args.list:
        print('\n'.join(list_nodes()))
    if args.listen:
        manage_nodes(listen=True)
    elif args.command and args.host:
        manage_nodes(command=args.command, host=args.host)

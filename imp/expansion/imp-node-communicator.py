import os
import json
import socket
import ssl
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUS_PATH = ROOT / "core" / "imp-message-bus.py"
spec = importlib.util.spec_from_file_location("imp_message_bus", BUS_PATH)
bus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bus)
send_message = bus.send_message

# Default ports for IMP node communication
# Incoming connections use port 7557 while outgoing
# connections are sent to port 5775.
INBOUND_PORT = 7557
OUTBOUND_PORT = 5775
CLUSTER_NODES_FILE = ROOT / "config" / "imp-cluster-nodes.json"

def secure_communication():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert = ROOT / "security" / "imp-cert.pem"
    key = ROOT / "security" / "imp-key.pem"
    context.load_cert_chain(certfile=str(cert), keyfile=str(key))

    if os.path.exists(CLUSTER_NODES_FILE):
        with open(CLUSTER_NODES_FILE, "r") as f:
            json.load(f)  # Load nodes for future use if needed

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(("0.0.0.0", INBOUND_PORT))
        sock.listen()

        with context.wrap_socket(sock, server_side=True) as secure_sock:
            print(f"Secure node communication established on port {INBOUND_PORT}")

            conn, addr = secure_sock.accept()
            data = conn.recv(1024)
            if data:
                text = data.decode()
                print(f"Received data from {addr}: {text}")
                send_message("inbound", text)
                conn.sendall(b"ACK")

def send_secure_message(host: str, message: str):
    """Send a message to a remote node using TLS."""
    context = ssl.create_default_context()
    cert = ROOT / "security" / "imp-cert.pem"
    if cert.exists():
        context.load_verify_locations(cafile=str(cert))
    with socket.create_connection((host, OUTBOUND_PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            secure_sock.sendall(message.encode())
            send_message("outbound", message)
            response = secure_sock.recv(1024)
            return response.decode()


def broadcast_secure_message(message: str):
    """Send a message to all known nodes."""
    if not os.path.exists(CLUSTER_NODES_FILE):
        return
    with open(CLUSTER_NODES_FILE, "r") as f:
        nodes = json.load(f)
    for node in nodes:
        try:
            send_secure_message(node, message)
        except Exception:
            continue

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IMP Node Communicator")
    parser.add_argument("--listen", action="store_true", help="Listen for incoming messages")
    parser.add_argument("--send", metavar="HOST", help="Send a message to the given host")
    parser.add_argument("--message", default="ping", help="Message text")
    args = parser.parse_args()

    if args.listen:
        secure_communication()
    elif args.send:
        try:
            resp = send_secure_message(args.send, args.message)
            print(f"Response: {resp}")
        except Exception as exc:
            print(f"Failed to send message: {exc}")

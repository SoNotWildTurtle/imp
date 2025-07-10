import os
import json
import socket
import ssl
from pathlib import Path

# Default ports for IMP node communication
# Incoming connections use port 7557 while outgoing
# connections are sent to port 5775.
INBOUND_PORT = 7557
OUTBOUND_PORT = 5775
ROOT = Path(__file__).resolve().parents[1]
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
            print(f"🔐 Secure node communication established on port {INBOUND_PORT}")

            conn, addr = secure_sock.accept()
            data = conn.recv(1024)
            if data:
                print(f"📡 Received data from {addr}: {data.decode()}")
                conn.sendall(b"ACK")

def send_secure_message(host: str, message: str):
    """Send a message to a remote node using TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((host, OUTBOUND_PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            secure_sock.sendall(message.encode())
            response = secure_sock.recv(1024)
            return response.decode()

if __name__ == "__main__":
    secure_communication()

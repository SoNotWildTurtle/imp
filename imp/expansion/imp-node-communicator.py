import os
import json
import socket
import ssl
from pathlib import Path

COMMUNICATION_PORT = 5005
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
        sock.bind(("0.0.0.0", COMMUNICATION_PORT))
        sock.listen()

        with context.wrap_socket(sock, server_side=True) as secure_sock:
            print(f"🔐 Secure node communication established on port {COMMUNICATION_PORT}")

            conn, addr = secure_sock.accept()
            data = conn.recv(1024)
            if data:
                print(f"📡 Received data from {addr}: {data.decode()}")
                conn.sendall(b"ACK")

if __name__ == "__main__":
    secure_communication()

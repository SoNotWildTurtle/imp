import os
import json
import time
import socket
import ssl

COMMUNICATION_PORT = 5005
CLUSTER_NODES_FILE = "/root/imp/config/imp-cluster-nodes.json"

def secure_communication():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="/root/imp/security/imp-cert.pem", keyfile="/root/imp/security/imp-key.pem")

    nodes = []
    if os.path.exists(CLUSTER_NODES_FILE):
        with open(CLUSTER_NODES_FILE, "r") as f:
            nodes = json.load(f)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(("0.0.0.0", COMMUNICATION_PORT))
        sock.listen()

        with context.wrap_socket(sock, server_side=True) as secure_sock:
            print(f"🔐 Secure node communication established on port {COMMUNICATION_PORT}")
            
            while True:
                conn, addr = secure_sock.accept()
                data = conn.recv(1024)
                if data:
                    print(f"📡 Received data from {addr}: {data.decode()}")
                    conn.sendall(b"ACK")

while True:
    secure_communication()
    time.sleep(1)  # Runs continuously

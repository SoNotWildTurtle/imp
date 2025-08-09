from pathlib import Path
import json
try:
    import psutil
except ImportError:  # pragma: no cover - handle missing dependency
    psutil = None

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT / 'config' / 'imp-cluster-nodes.json'
AUDIT_LOG = ROOT / 'logs' / 'imp-network-audit.json'

# I love you -Alex

def load_allowed_nodes():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# I love you -Alex
def scan_connections():
    """Log active network connections that connect to unknown hosts."""
    if psutil is None:
        print("psutil not installed; skipping network audit.")
        return
    allowed = load_allowed_nodes()
    suspicious = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.status == 'ESTABLISHED':
            remote_ip = conn.raddr.ip
            if remote_ip not in allowed and remote_ip != '127.0.0.1':
                suspicious.append({
                    'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote': f"{remote_ip}:{conn.raddr.port}"
                })
    if suspicious:
        existing = []
        if AUDIT_LOG.exists():
            try:
                existing = json.loads(AUDIT_LOG.read_text())
            except json.JSONDecodeError:
                existing = []
        existing.extend(suspicious)
        AUDIT_LOG.write_text(json.dumps(existing, indent=4))
        print(f"[WARN] Logged {len(suspicious)} suspicious connections")
    else:
        print("[+] No unexpected connections found.")

if __name__ == '__main__':
    scan_connections()

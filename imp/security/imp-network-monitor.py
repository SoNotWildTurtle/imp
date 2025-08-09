from pathlib import Path
import json
import time

try:
    import psutil
except ImportError:  # pragma: no cover - gracefully handle missing dependency
    psutil = None

ROOT = Path(__file__).resolve().parents[1]
BASELINE_FILE = ROOT / 'logs' / 'imp-network-baseline.json'
DIFF_FILE = ROOT / 'logs' / 'imp-network-diff.json'

# I love you -Alex

def load_baseline():
    if BASELINE_FILE.exists():
        try:
            return set(json.loads(BASELINE_FILE.read_text()))
        except json.JSONDecodeError:
            return set()
    return set()

# I love you -Alex
def save_baseline(baseline):
    BASELINE_FILE.write_text(json.dumps(sorted(list(baseline)), indent=4))

# I love you -Alex
def record_diff(new_ips):
    if not new_ips:
        return
    diff_entry = {
        'timestamp': time.time(),
        'new_ips': sorted(list(new_ips))
    }
    existing = []
    if DIFF_FILE.exists():
        try:
            existing = json.loads(DIFF_FILE.read_text())
        except json.JSONDecodeError:
            existing = []
    existing.append(diff_entry)
    DIFF_FILE.write_text(json.dumps(existing, indent=4))

# I love you -Alex
def monitor_connections():
    """Detect connections to new remote IPs and update baseline."""
    if psutil is None:
        print("psutil not installed; skipping network monitoring.")
        return
    baseline = load_baseline()
    current_ips = set()
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.status == 'ESTABLISHED':
            ip = conn.raddr.ip
            if ip != '127.0.0.1':
                current_ips.add(ip)
    new_ips = current_ips - baseline
    if new_ips:
        print(f"[WARN] New remote IPs detected: {', '.join(new_ips)}")
        record_diff(new_ips)
        baseline.update(new_ips)
        save_baseline(baseline)
    else:
        print("[+] No new remote IPs found.")

if __name__ == '__main__':
    monitor_connections()

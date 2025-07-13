from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_network_auditor():
    print("Running Network Auditor...")
    script = ROOT / 'security' / 'imp-network-auditor.py'
    subprocess.run(f"python3 {script}", shell=True)
    assert (ROOT / 'logs' / 'imp-network-audit.json').exists()
    print("Network Auditor Executed!")

if __name__ == '__main__':
    test_network_auditor()

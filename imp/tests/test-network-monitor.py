from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_network_monitor():
    print("Running Network Monitor...")
    script = ROOT / 'security' / 'imp-network-monitor.py'
    subprocess.run(f"python3 {script}", shell=True)
    assert (ROOT / 'logs' / 'imp-network-baseline.json').exists()
    assert (ROOT / 'logs' / 'imp-network-diff.json').exists()
    print("Network Monitor Executed!")

if __name__ == '__main__':
    test_network_monitor()

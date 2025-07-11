from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_hardware_guard():
    print("Running Hardware Guard...")
    script = ROOT / 'security' / 'imp-hardware-guard.py'
    subprocess.run(f"python3 {script}", shell=True)
    print("Hardware Guard Executed! Review output manually.")


if __name__ == '__main__':
    test_hardware_guard()

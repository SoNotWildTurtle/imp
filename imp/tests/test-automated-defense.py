from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_automated_defense():
    print("Running Automated Defense Cycle...")
    script = ROOT / 'security' / 'imp-automated-defense.py'
    subprocess.run(f"python3 {script}", shell=True)
    print("Automated Defense Executed! Review output manually.")


if __name__ == '__main__':
    test_automated_defense()

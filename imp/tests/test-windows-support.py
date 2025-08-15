from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START_PY = ROOT / 'bin' / 'imp-start.py'
STOP_PY = ROOT / 'bin' / 'imp-stop.py'
PS_START = ROOT.parent / 'imp-start.ps1'

def test_start_script():
    print('Checking Windows start script...')
    assert START_PY.exists(), 'imp-start.py missing'
    with open(START_PY) as f:
        data = f.read()
    assert 'multiprocessing' in data
    assert 'freeze_support' in data, 'freeze_support missing for Windows compatibility'
    print('Start script OK!')

def test_stop_script():
    print('Checking Windows stop script...')
    assert STOP_PY.exists(), 'imp-stop.py missing'
    with open(STOP_PY) as f:
        data = f.read()
    assert 'os.kill' in data
    print('Stop script OK!')


def test_powershell_keepalive():
    print('Checking PowerShell keepalive...')
    assert PS_START.exists(), 'imp-start.ps1 missing'
    with open(PS_START) as f:
        data = f.read().lower()
    assert 'while ($true)' in data, 'imp-start.ps1 should keep restarting IMP'
    print('PowerShell script OK!')


test_start_script()
test_stop_script()
test_powershell_keepalive()


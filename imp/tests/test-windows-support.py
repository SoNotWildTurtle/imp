from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
START_PY = ROOT / 'bin' / 'imp-start.py'
STOP_PY = ROOT / 'bin' / 'imp-stop.py'

def test_start_script():
    print('Checking Windows start script...')
    assert START_PY.exists(), 'imp-start.py missing'
    with open(START_PY) as f:
        data = f.read()
    assert 'multiprocessing' in data
    print('Start script OK!')

def test_stop_script():
    print('Checking Windows stop script...')
    assert STOP_PY.exists(), 'imp-stop.py missing'
    with open(STOP_PY) as f:
        data = f.read()
    assert 'os.kill' in data
    print('Stop script OK!')


test_start_script()
test_stop_script()


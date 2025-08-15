from pathlib import Path

def test_start_script_uses_absolute_executor_path():
    root = Path(__file__).resolve().parents[1]
    script_text = (root / 'bin' / 'imp-start.sh').read_text()
    assert 'nohup python3 /root/imp/core/imp-execute.py &' in script_text

from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'core' / 'imp-voice-menu.py'


def test_voice_menu_exists():
    assert SCRIPT.exists()


def test_run_menu_present():
    spec = importlib.util.spec_from_file_location('voice_menu', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, 'run_menu')

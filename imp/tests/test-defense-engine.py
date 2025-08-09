from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'core' / 'imp-defense-engine.py'

spec = importlib.util.spec_from_file_location('engine', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_defense_engine():
    print('Running Defense Engine...')
    module.run_defense_cycle()
    print('Defense Engine Executed!')


if __name__ == '__main__':
    test_defense_engine()

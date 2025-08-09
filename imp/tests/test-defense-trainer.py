from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'self-improvement' / 'imp-defense-trainer.py'

spec = importlib.util.spec_from_file_location('trainer', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_defense_trainer():
    print('Running Defense Trainer...')
    module.improve_defense()
    print('Defense Trainer Executed!')


if __name__ == '__main__':
    test_defense_trainer()

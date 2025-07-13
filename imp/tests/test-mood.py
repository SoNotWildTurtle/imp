from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'core' / 'imp-mood-manager.py'

spec = importlib.util.spec_from_file_location('imp_mood_manager', MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_decay():
    print('Testing Mood Decay...')
    mod.save_mood(1.0)
    val1 = mod.decay_toward_baseline()
    assert val1 < 1.0
    print('Mood Manager Test Passed!')


def test_update():
    print('Testing Mood Update...')
    mod.save_mood(0.0)
    val2 = mod.update_mood('goal_completed')
    assert val2 > 0.0
    print('Mood Update Test Passed!')


if __name__ == '__main__':
    test_decay()
    test_update()

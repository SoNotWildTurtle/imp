from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'self-improvement' / 'imp-adversarial-trainer.py'
MODEL = ROOT / 'models' / 'adversarial_nn.json'

spec = importlib.util.spec_from_file_location('adv_trainer', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_adversarial_trainer():
    if MODEL.exists():
        MODEL.unlink()
    module.run_adversarial_training()
    assert MODEL.exists(), 'Adversarial model not created'
    print('Adversarial training run complete.')


if __name__ == '__main__':
    test_adversarial_trainer()

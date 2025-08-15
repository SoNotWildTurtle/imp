from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
script = ROOT / 'self-improvement' / 'imp-network-task-trainer.py'

spec = importlib.util.spec_from_file_location('trainer', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_network_task_trainer():
    print("Running Network Task Trainer...")
    module.improve_network()
    assert (ROOT / 'models' / 'network_task_nn.json').exists()
    print("Network Task Trainer Executed!")

if __name__ == '__main__':
    test_network_task_trainer()

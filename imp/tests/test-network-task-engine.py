from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'core' / 'imp-network-task-engine.py'

spec = importlib.util.spec_from_file_location('engine', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_network_task_engine():
    print('Running Network Task Engine...')
    module.run_network_tasks()
    print('Network Task Engine Executed!')

if __name__ == '__main__':
    test_network_task_engine()

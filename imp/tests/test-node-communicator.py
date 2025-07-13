from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'expansion' / 'imp-node-communicator.py'

spec = importlib.util.spec_from_file_location('node_comm', MODULE_PATH)
node_comm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(node_comm)

print('Testing Node Communicator...')
assert hasattr(node_comm, 'send_secure_message')
assert hasattr(node_comm, 'secure_communication')
print('Node Communicator Test Passed!')

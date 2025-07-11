from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'expansion' / 'imp-secure-node-manager.py'

spec = importlib.util.spec_from_file_location('snm', MODULE_PATH)
snm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(snm)

print('Testing Secure Node Manager...')
assert hasattr(snm, 'register_node')
assert hasattr(snm, 'manage_nodes')
print('Secure Node Manager Test Executed!')

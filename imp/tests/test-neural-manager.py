from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / 'core' / 'imp_neural_manager.py'
RESOURCE_PATH = ROOT / 'core' / 'imp-resource-nn.py'

spec_mgr = importlib.util.spec_from_file_location('mgr', MANAGER_PATH)
manager_module = importlib.util.module_from_spec(spec_mgr)
spec_mgr.loader.exec_module(manager_module)

spec_res = importlib.util.spec_from_file_location('res', RESOURCE_PATH)
res_module = importlib.util.module_from_spec(spec_res)
spec_res.loader.exec_module(res_module)


def test_register_and_get():
    nn = res_module.ResourceNN()
    manager_module.manager.register('test', nn)
    assert manager_module.manager.get('test') is nn

if __name__ == '__main__':
    test_register_and_get()

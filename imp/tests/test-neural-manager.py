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


def test_get_or_create_and_list():
    def factory():
        return res_module.ResourceNN()
    net = manager_module.manager.get_or_create('test', factory)
    assert net is manager_module.manager.get('test')
    assert 'test' in manager_module.manager.list()
    manager_module.manager.unregister('test')
    assert 'test' not in manager_module.manager.list()

if __name__ == '__main__':
    test_get_or_create_and_list()

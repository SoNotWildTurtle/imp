from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'core' / 'imp-defense-nn.py'

spec = importlib.util.spec_from_file_location('defense_nn', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_defense_nn():
    print('Testing Defense Neural Network...')
    net = module.DefenseNN(1, 2, 1)
    out = net.forward([0.0])
    assert len(out) == 1
    tmp = ROOT / 'defense_tmp.json'
    net.save(tmp)
    loaded = module.DefenseNN.load(tmp)
    assert loaded.forward([0.0])[0] == out[0]
    tmp.unlink()
    print('Defense NN Test Passed!')


if __name__ == '__main__':
    test_defense_nn()

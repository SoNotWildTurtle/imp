from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
NN_PATH = ROOT / 'core' / 'imp-collaboratory-nn.py'
ENG_PATH = ROOT / 'core' / 'imp-collaboratory-engine.py'

spec = importlib.util.spec_from_file_location('collab_nn', NN_PATH)
collab_nn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collab_nn)

spec_e = importlib.util.spec_from_file_location('collab_engine', ENG_PATH)
collab_engine = importlib.util.module_from_spec(spec_e)
spec_e.loader.exec_module(collab_engine)


def test_collaboratory_nn():
    print('Testing Collaboratory Neural Network...')
    net = collab_nn.CollaboratoryNN(2, 2, 1)
    out = net.forward([0.0, 0.0])
    assert len(out) == 1
    tmp = ROOT / 'collab_tmp.json'
    net.save(tmp)
    loaded = collab_nn.CollaboratoryNN.load(tmp)
    assert loaded.forward([0.0, 0.0])[0] == out[0]
    tmp.unlink()
    result = collab_engine.run_collaboration([0.0, 0.0])
    assert isinstance(result, float)
    print('Collaboratory NN Test Passed!')


if __name__ == '__main__':
    test_collaboratory_nn()

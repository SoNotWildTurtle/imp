from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / 'core' / 'imp-bbi-engine.py'
NN_PATH = ROOT / 'core' / 'imp-bbi-nn.py'
LOG = ROOT / 'logs' / 'imp-bbi-log.json'
MODEL = ROOT / 'logs' / 'imp-bbi-model.json'

spec_engine = importlib.util.spec_from_file_location('bbi_engine', ENGINE_PATH)
bbi_engine = importlib.util.module_from_spec(spec_engine)
spec_engine.loader.exec_module(bbi_engine)

spec_nn = importlib.util.spec_from_file_location('bbi_nn', NN_PATH)
bbi_nn = importlib.util.module_from_spec(spec_nn)
spec_nn.loader.exec_module(bbi_nn)


def test_bbi_engine():
    print('Testing BBI Engine...')
    engine = bbi_engine.BBIEngine()
    before_len = len(json.loads(LOG.read_text())) if LOG.exists() else 0
    before_hidden = engine.network.hidden_size
    _, after_hidden = engine.record_interaction('ping', 'pong', 'sao')
    data = json.loads(LOG.read_text())
    assert len(data) == before_len + 1
    loaded = bbi_nn.BBINN.load(MODEL)
    assert loaded.hidden_size == before_hidden + 1
    print('BBI Engine Test Passed!')


if __name__ == '__main__':
    test_bbi_engine()

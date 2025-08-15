import json
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location('bbi_nn', ROOT / 'core' / 'imp-bbi-nn.py')
nn_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nn_module)
BBINN = nn_module.BBINN

MANAGER_PATH = ROOT / 'core' / 'imp_neural_manager.py'
spec_mgr = importlib.util.spec_from_file_location('imp_neural_manager', MANAGER_PATH)
mgr_module = importlib.util.module_from_spec(spec_mgr)
spec_mgr.loader.exec_module(mgr_module)
neural_manager = mgr_module.manager

LOG = ROOT / 'logs' / 'imp-bbi-log.json'
MODEL = ROOT / 'logs' / 'imp-bbi-model.json'


class BBIEngine:
    """Manages BBI interactions and evolves its neural network."""

    def __init__(self):
        self.network = load_model()

    def record_interaction(self, user_signal: str, imp_signal: str, theme: str = ''):
        data = json.loads(LOG.read_text()) if LOG.exists() else []
        data.append({"user": user_signal, "imp": imp_signal, "theme": theme})
        LOG.write_text(json.dumps(data))
        before = self.network.hidden_size
        self.network.evolve()
        self.network.save(MODEL)
        return before, self.network.hidden_size


def load_model() -> BBINN:
    def factory() -> BBINN:
        if MODEL.exists():
            return BBINN.load(MODEL)
        return BBINN(2, 2, 1)
    return neural_manager.get_or_create('bbi', factory)

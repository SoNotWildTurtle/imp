import json
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location('bbi_nn', Path(__file__).resolve().parent / 'imp-bbi-nn.py')
nn_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nn_module)
BBINN = nn_module.BBINN

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / 'logs' / 'imp-bbi-log.json'
MODEL = ROOT / 'logs' / 'imp-bbi-model.json'


class BBIEngine:
    """Manages BBI interactions and evolves its neural network."""

    def __init__(self):
        if MODEL.exists():
            self.network = BBINN.load(MODEL)
        else:
            self.network = BBINN(2, 2, 1)

    def record_interaction(self, user_signal: str, imp_signal: str, theme: str = ''):
        data = json.loads(LOG.read_text()) if LOG.exists() else []
        data.append({"user": user_signal, "imp": imp_signal, "theme": theme})
        LOG.write_text(json.dumps(data))
        before = self.network.hidden_size
        self.network.evolve()
        self.network.save(MODEL)
        return before, self.network.hidden_size

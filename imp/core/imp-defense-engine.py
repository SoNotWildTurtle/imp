from pathlib import Path
import json
import importlib.util
import subprocess
import logging

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'defense_nn.json'
AUDIT_LOG = ROOT / 'logs' / 'imp-network-audit.json'
DEFENSE_SCRIPT = ROOT / 'security' / 'imp-automated-defense.py'

import importlib.util

CORE_DIR = ROOT / 'core'
MANAGER_PATH = CORE_DIR / 'imp_neural_manager.py'
spec_mgr = importlib.util.spec_from_file_location('imp_neural_manager', MANAGER_PATH)
mgr_module = importlib.util.module_from_spec(spec_mgr)
spec_mgr.loader.exec_module(mgr_module)
neural_manager = mgr_module.manager

spec = importlib.util.spec_from_file_location('defense_nn', CORE_DIR / 'imp-defense-nn.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DefenseNN = module.DefenseNN

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_model() -> DefenseNN:
    def factory() -> DefenseNN:
        if MODEL_PATH.exists():
            return DefenseNN.load(MODEL_PATH)
        return DefenseNN(1, 2, 1)
    return neural_manager.get_or_create('defense', factory)


def suspicious_count() -> int:
    if not AUDIT_LOG.exists():
        return 0
    try:
        data = json.loads(AUDIT_LOG.read_text())
    except json.JSONDecodeError:
        return 0
    return len(data)


def run_defense_cycle() -> None:
    model = load_model()
    count = suspicious_count()
    output = model.forward([count / 10.0])[0]
    log.info("Defense model output: %.3f", output)
    if output > 0.5:
        subprocess.run(['python3', str(DEFENSE_SCRIPT)])
    else:
        log.info('No defense action required.')


if __name__ == '__main__':
    run_defense_cycle()

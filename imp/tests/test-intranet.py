import json
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
INTRANET_FILE = ROOT / 'config' / 'imp-intranet.json'


def test_intranet_creation():
    print('Testing Intranet Creation...')
    module_path = ROOT / 'expansion' / 'imp-intranet.py'
    spec = importlib.util.spec_from_file_location('imp_intranet', module_path)
    imp_intranet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imp_intranet)
    nodes = ['127.0.0.1', '192.168.1.10']
    imp_intranet.create_intranet(nodes)
    with open(INTRANET_FILE, 'r') as f:
        data = json.load(f)
    assert data['nodes'] == nodes
    print('Intranet Creation Test Passed!')


test_intranet_creation()

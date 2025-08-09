from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'expansion' / 'imp-game-copilot.py'

spec = importlib.util.spec_from_file_location('game_copilot', MODULE_PATH)
game_copilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_copilot)

print('Testing Game Copilot...')
entry = game_copilot.learn_game('demo', 'use arrow keys')
assert entry['rules'] == 'use arrow keys'
dream = game_copilot.build_dreamscape('demo')
assert dream['based_on'] == 'use arrow keys'
assert dream['sao_theme'] == 'demo-sao-field'

LOG_DIR = ROOT / 'logs'
with open(LOG_DIR / 'imp-games.json') as f:
    games = json.load(f)
with open(LOG_DIR / 'imp-dreamscape.json') as f:
    dreams = json.load(f)
assert 'demo' in games
assert 'demo' in dreams
print('Game Copilot Test Passed!')

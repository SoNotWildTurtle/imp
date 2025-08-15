from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'self-improvement' / 'imp-code-updater.py'

print('Checking Code Updater helpers...')
source = MODULE_PATH.read_text()
module = ast.parse(source)
funcs = {node.name for node in module.body if isinstance(node, ast.FunctionDef)}
assert 'decide_mode' in funcs, 'decide_mode function missing'
assert 'get_generator' in funcs, 'get_generator function missing'
print('Code Updater Helper Test Passed!')

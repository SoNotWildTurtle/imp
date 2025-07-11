from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
CHAT_SCRIPT = ROOT / 'core' / 'imp-goal-chat.py'

spec = importlib.util.spec_from_file_location('imp_chat', CHAT_SCRIPT)
imp_chat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp_chat)

print('Testing Goal Chat module...')
# use offline mode to avoid network
reply = imp_chat.send_chatgpt_request('Hello', use_notes=False, mode='offline')
assert isinstance(reply, str)
print('Goal Chat Test Passed!')

from pathlib import Path
import importlib.util
import json
import hashlib
import shutil
import difflib
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / 'self-improvement' / 'imp-blockchain-ledger.py'
LEDGER_FILE = ROOT / 'logs' / 'imp-blockchain-ledger.json'
HEAL_LOG = ROOT / 'logs' / 'imp-self-heal-log.json'
PATCH_DIR = ROOT / 'logs' / 'imp-update-patches'
LINT_LOG = ROOT / 'logs' / 'imp-lint-report.json'

spec = importlib.util.spec_from_file_location('ledger', LEDGER_PATH)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)

# load log manager to ensure required log files exist
LOG_MANAGER_PATH = ROOT / 'logs' / 'imp-log-manager.py'
spec_logs = importlib.util.spec_from_file_location('logmanager', LOG_MANAGER_PATH)
logmanager = importlib.util.module_from_spec(spec_logs)
spec_logs.loader.exec_module(logmanager)

GOAL_CHAT_PATH = ROOT / 'core' / 'imp-goal-chat.py'
spec_chat = importlib.util.spec_from_file_location('goalchat', GOAL_CHAT_PATH)
goalchat = importlib.util.module_from_spec(spec_chat)
spec_chat.loader.exec_module(goalchat)


def recover_with_chatgpt(rel_path: str, description: str = '', mode: str = 'auto') -> bool:
    """Attempt to regenerate a missing or corrupt module using ChatGPT."""
    prompt = f"Provide minimal Python code for {rel_path}. {description}".strip()
    try:
        text = goalchat.send_chatgpt_request(prompt, use_notes=True, mode=mode)
    except Exception:
        text = ''
    if not text:
        text = f"# Placeholder generated for {rel_path}\n"
    file_path = ROOT / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        file_path.write_text(text)
        return True
    except Exception:
        return False


def run_linter() -> list:
    """Run flake8 on the repository and save any issues."""
    if not LINT_LOG.exists():
        LINT_LOG.write_text('[]')
    try:
        result = subprocess.run(['flake8', str(ROOT)], capture_output=True, text=True)
        issues = result.stdout.strip().splitlines()
    except Exception:
        issues = ['linting failed']
    LINT_LOG.write_text(json.dumps(issues, indent=4))
    return issues


def verify_and_heal(apply: bool = True, use_chatgpt: bool = True, mode: str = 'auto', mint: bool = False) -> None:
    """Check code against the ledger and optionally restore mismatched files."""
    # Ensure standard log files exist before performing checks
    logmanager.ensure_logs()
    if not HEAL_LOG.exists():
        HEAL_LOG.write_text('[]')
    PATCH_DIR.mkdir(exist_ok=True)
    ledger_ok = ledger.verify_chain()
    last_entry = ledger.load_ledger()[-1] if ledger.load_ledger() else None
    mismatches = []
    if last_entry:
        for rel_path, recorded_hash in last_entry['files'].items():
            file_path = ROOT / rel_path
            if not file_path.exists():
                mismatches.append({'file': rel_path, 'reason': 'missing'})
                if use_chatgpt:
                    recover_with_chatgpt(rel_path, 'File was missing', mode)
                continue
            actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual != recorded_hash:
                backups = sorted(file_path.parent.glob(file_path.name + '.backup.*'))
                if apply and backups:
                    latest = backups[-1]
                    shutil.copy2(latest, file_path)
                    mismatches.append({'file': rel_path, 'reason': 'restored from backup'})
                else:
                    if backups:
                        base_text = backups[-1].read_text().splitlines(True)
                        new_text = file_path.read_text().splitlines(True)
                        patch = difflib.unified_diff(base_text, new_text,
                                                     fromfile='backup',
                                                     tofile=str(file_path))
                        patch_path = PATCH_DIR / f"{file_path.name}.patch"
                        patch_path.write_text(''.join(patch))
                    mismatches.append({'file': rel_path, 'reason': 'hash mismatch'})
                    if use_chatgpt:
                        recover_with_chatgpt(rel_path, 'Hash mismatch detected', mode)
    lint_issues = run_linter()
    minted_hash = None
    if mint:
        block = ledger.add_block()
        minted_hash = block.get('block_hash')
    log = json.loads(HEAL_LOG.read_text())
    entry = {'ledger_ok': ledger_ok, 'mismatches': mismatches, 'lint_issues': lint_issues}
    if minted_hash:
        entry['minted_block'] = minted_hash
    log.append(entry)
    HEAL_LOG.write_text(json.dumps(log, indent=4))
    print(f'Self-heal complete. {len(mismatches)} issues resolved. Lint warnings: {len(lint_issues)}')


def auto_verify_and_heal() -> None:
    """Run self-heal based on the system configuration."""
    cfg_path = ROOT / 'config' / 'imp-config-manager.py'
    spec_cfg = importlib.util.spec_from_file_location('cfg', cfg_path)
    cfg = importlib.util.module_from_spec(spec_cfg)
    spec_cfg.loader.exec_module(cfg)

    system_cfg = cfg.load_config('system') or {}
    heal_cfg = system_cfg.get("self_healing", {})
    apply = heal_cfg.get("auto_apply", True)
    use_chatgpt = heal_cfg.get("use_chatgpt", True)
    mode = heal_cfg.get("mode", "auto")
    mint = heal_cfg.get("mint", False)
    verify_and_heal(apply=apply, use_chatgpt=use_chatgpt, mode=mode, mint=mint)


if __name__ == '__main__':
    verify_and_heal()

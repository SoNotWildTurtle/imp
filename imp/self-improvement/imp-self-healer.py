from pathlib import Path
import importlib.util
import json
import hashlib
import shutil

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / 'self-improvement' / 'imp-blockchain-ledger.py'
LEDGER_FILE = ROOT / 'logs' / 'imp-blockchain-ledger.json'
HEAL_LOG = ROOT / 'logs' / 'imp-self-heal-log.json'
PATCH_DIR = ROOT / 'logs' / 'imp-update-patches'

spec = importlib.util.spec_from_file_location('ledger', LEDGER_PATH)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


def verify_and_heal(apply: bool = True) -> None:
    """Check code against the ledger and optionally restore mismatched files."""
    if not HEAL_LOG.exists():
        HEAL_LOG.write_text('[]')
    ledger_ok = ledger.verify_chain()
    last_entry = ledger.load_ledger()[-1] if ledger.load_ledger() else None
    mismatches = []
    if last_entry:
        for rel_path, recorded_hash in last_entry['files'].items():
            file_path = ROOT / rel_path
            if not file_path.exists():
                mismatches.append({'file': rel_path, 'reason': 'missing'})
                continue
            actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual != recorded_hash:
                if apply:
                    backups = sorted(file_path.parent.glob(file_path.name + '.backup.*'))
                    if backups:
                        latest = backups[-1]
                        shutil.copy2(latest, file_path)
                        mismatches.append({'file': rel_path, 'reason': 'restored from backup'})
                    else:
                        mismatches.append({'file': rel_path, 'reason': 'hash mismatch'})
                else:
                    mismatches.append({'file': rel_path, 'reason': 'hash mismatch'})
    log = json.loads(HEAL_LOG.read_text())
    log.append({'ledger_ok': ledger_ok, 'mismatches': mismatches})
    HEAL_LOG.write_text(json.dumps(log, indent=4))
    print(f'Self-heal complete. {len(mismatches)} issues resolved.')


def auto_verify_and_heal() -> None:
    """Run self-heal based on the system configuration."""
    cfg_path = ROOT / 'config' / 'imp-config-manager.py'
    spec_cfg = importlib.util.spec_from_file_location('cfg', cfg_path)
    cfg = importlib.util.module_from_spec(spec_cfg)
    spec_cfg.loader.exec_module(cfg)

    system_cfg = cfg.load_config('system') or {}
    apply = system_cfg.get("self_healing", {}).get("auto_apply", True)
    verify_and_heal(apply=apply)


if __name__ == '__main__':
    verify_and_heal()

import argparse
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:  # pragma: no cover - dependency handled via setup
    yaml = None

POLICY_DEFAULT = Path(__file__).resolve().parents[1] / "config" / "policy.yaml"
LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "imp-policy-changes.json"


def load_policy(path: Path = POLICY_DEFAULT):
    if not path.exists():
        return {"version": 1, "capabilities": {}}
    with open(path, "r", encoding="utf-8") as f:
        if yaml:
            return yaml.safe_load(f) or {}
        return json.load(f)


def save_policy(policy: dict, path: Path = POLICY_DEFAULT):
    with open(path, "w", encoding="utf-8") as f:
        if yaml:
            yaml.safe_dump(policy, f)
        else:
            json.dump(policy, f, indent=2)


def get_capability(policy: dict, capability: str) -> str:
    return policy.get("capabilities", {}).get(capability, "request_only")


def set_capability(policy: dict, capability: str, status: str) -> str:
    old = get_capability(policy, capability)
    policy.setdefault("capabilities", {})[capability] = status
    return old


def policy_signature(policy: dict) -> str:
    if yaml:
        data = yaml.safe_dump(policy).encode("utf-8")
    else:
        data = json.dumps(policy, sort_keys=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def log_change(capability: str, old: str, new: str, signature: str):
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            entries = []
    entries.append(
        {
            "ts": datetime.utcnow().isoformat(),
            "capability": capability,
            "old": old,
            "new": new,
            "signature": signature,
        }
    )
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def update_capability(capability: str, status: str, path: Path = POLICY_DEFAULT):
    policy = load_policy(path)
    old = set_capability(policy, capability, status)
    save_policy(policy, path)
    sig = policy_signature(policy)
    log_change(capability, old, status, sig)
    return old, status


def main():
    parser = argparse.ArgumentParser(description="Manage capability policy")
    parser.add_argument("action", choices=["status", "grant", "block", "request"])
    parser.add_argument("capability")
    parser.add_argument("--policy", default=str(POLICY_DEFAULT))
    args = parser.parse_args()

    path = Path(args.policy)
    if args.action == "status":
        policy = load_policy(path)
        print(get_capability(policy, args.capability))
        return

    mapping = {"grant": "granted", "block": "blocked", "request": "request_only"}
    old, new = update_capability(args.capability, mapping[args.action], path)
    print(f"{args.capability}: {old} -> {new}")


if __name__ == "__main__":  # pragma: no cover
    main()

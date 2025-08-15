import ast
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-module-info.json"


def gather_module_info():
    modules = []
    for path in BASE_DIR.rglob("*.py"):
        if "tests" in path.parts or "logs" in path.parts:
            continue
        rel = path.relative_to(BASE_DIR)
        try:
            tree = ast.parse(path.read_text())
        except Exception:
            continue
        funcs = []
        classes = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                params = [arg.arg for arg in node.args.args]
                funcs.append({"name": node.name, "params": params})
            elif isinstance(node, ast.ClassDef):
                classes.append({"name": node.name})
        modules.append({"module": str(rel), "functions": funcs, "classes": classes})
    return modules


def log_module_info():
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "modules": gather_module_info(),
    }
    logs = []
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"[+] Logged info for {len(entry['modules'])} modules.")


if __name__ == "__main__":
    log_module_info()

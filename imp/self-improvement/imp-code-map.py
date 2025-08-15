from __future__ import annotations
import ast
import json
from pathlib import Path


def generate_code_map() -> Path:
    """Scan the project and record functions/classes for each Python file."""
    root = Path(__file__).resolve().parents[2]
    code_dir = root / "imp"
    code_map = {}
    for py_file in code_dir.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text())
            funcs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
            classes = [n.name for n in tree.body if isinstance(n, ast.ClassDef)]
            rel = py_file.relative_to(root)
            code_map[str(rel)] = {"functions": funcs, "classes": classes}
        except Exception as exc:
            rel = py_file.relative_to(root)
            code_map[str(rel)] = {"error": str(exc)}
    log_dir = root / "imp" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    out_path = log_dir / "imp-code-map.json"
    out_path.write_text(json.dumps(code_map, indent=2))
    return out_path


if __name__ == "__main__":
    path = generate_code_map()
    print(f"Code map written to {path}")

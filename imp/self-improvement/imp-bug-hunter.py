from pathlib import Path
import json
import py_compile

ROOT = Path(__file__).resolve().parents[1]
BUG_LOG = ROOT / "logs" / "imp-bug-report.json"


def scan_repository() -> None:
    """Compile each Python file to detect syntax errors."""
    issues = []
    for path in ROOT.rglob('*.py'):
        try:
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError as exc:
            issues.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})
    with open(BUG_LOG, 'w') as f:
        json.dump(issues, f, indent=4)
    print(f"Bug hunt complete. {len(issues)} issues logged.")


if __name__ == "__main__":
    scan_repository()

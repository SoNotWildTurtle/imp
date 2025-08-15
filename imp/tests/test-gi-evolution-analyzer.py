from pathlib import Path
import json
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config" / "gi"
LOG_FILE = BASE_DIR / "logs" / "imp-gi-evolution-analysis.json"


def test_evolution_analyzer():
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {"name": "ana", "modules": ["imp-gi-memory.py"], "skills": []}
    (CONFIG_DIR / "ana.json").write_text(json.dumps(config, indent=4))
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-evolution-analyzer.py"
    spec = importlib.util.spec_from_file_location("analyzer", script)
    analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analyzer)
    analyzer.analyze_gi("ana")
    with open(LOG_FILE, "r") as f:
        data = json.load(f)
    assert any(entry["name"] == "ana" for entry in data)
    print("✅ GI Evolution Analyzer Test Passed!")


if __name__ == "__main__":
    test_evolution_analyzer()

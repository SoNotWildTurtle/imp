import json
import importlib.util
import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config" / "gi"


def test_gi_packager():
    spec = importlib.util.spec_from_file_location(
        "packager", BASE_DIR / "interaction" / "imp-gi-packager.py"
    )
    packager = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(packager)
    CONFIG_DIR.mkdir(exist_ok=True)
    cfg = CONFIG_DIR / "PackagerGI.json"
    with open(cfg, "w") as f:
        json.dump({"modules": []}, f)
    archive = packager.package_gi(cfg)
    assert archive.exists()
    with zipfile.ZipFile(archive, "r") as zf:
        assert "PackagerGI.json" in zf.namelist()
    archive.unlink()
    cfg.unlink()
    print("✅ GI Packager Test Passed!")


test_gi_packager()

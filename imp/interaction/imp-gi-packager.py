from __future__ import annotations

"""Package a GI configuration and its modules for distribution."""

from pathlib import Path
import json
import zipfile
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
MODULE_DIR = BASE_DIR / "gi_modules"


def package_gi(config_path: str | Path) -> Path:
    """Bundle a GI config and referenced modules into a zip file.

    Parameters
    ----------
    config_path: str or Path
        Path to the GI configuration file.

    Returns
    -------
    Path
        Location of the created zip archive.
    """
    cfg = Path(config_path)
    if not cfg.exists():
        raise FileNotFoundError(f"Config file not found: {cfg}")
    with open(cfg, "r", encoding="utf-8") as f:
        config = json.load(f)
    modules = config.get("modules", [])
    package_path = BASE_DIR / f"{cfg.stem}_package.zip"
    with zipfile.ZipFile(package_path, "w") as zf:
        zf.write(cfg, cfg.name)
        for mod in modules:
            mod_path = MODULE_DIR / mod
            if mod_path.exists():
                zf.write(mod_path, f"modules/{mod}")
    return package_path


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python imp-gi-packager.py path/to/config.json")
        return
    archive = package_gi(argv[0])
    print(f"Package created at {archive}")


if __name__ == "__main__":
    main()

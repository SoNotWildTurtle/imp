from pathlib import Path
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
TRACKER = BASE_DIR / "gi_modules" / "imp-gi-skill-tracker.py"

spec_v = importlib.util.spec_from_file_location("heavy", VERIFIER)
heavy = importlib.util.module_from_spec(spec_v)
try:
    spec_v.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("\u26a0\ufe0f Verification unavailable.")
        return False

spec_t = importlib.util.spec_from_file_location("tracker", TRACKER)
tracker = importlib.util.module_from_spec(spec_t)
spec_t.loader.exec_module(tracker)


def main():
    if not verify_user():
        return
    name = input("GI name: ")
    skill = input("New skill description: ")
    tracker.add_skill(name, skill)
    print("[+] Skill added")


if __name__ == "__main__":
    main()

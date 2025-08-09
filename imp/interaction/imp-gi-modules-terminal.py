from pathlib import Path
import importlib.util
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
CHATBOT = BASE_DIR / "interaction" / "imp-chatbot.py"
MODULES = {
    "Memory": BASE_DIR / "gi_modules" / "imp-gi-memory.py",
    "Task Manager": BASE_DIR / "gi_modules" / "imp-gi-task-manager.py",
    "Self Evolver": BASE_DIR / "gi_modules" / "imp-gi-self-evolver.py",
    "Knowledge": BASE_DIR / "gi_modules" / "imp-gi-knowledge.py",
    "Skill Tracker": BASE_DIR / "gi_modules" / "imp-gi-skill-tracker.py",
    "Performance": BASE_DIR / "gi_modules" / "imp-gi-performance.py",
    "Safety": BASE_DIR / "gi_modules" / "imp-gi-safety.py",
    "Risk Analyzer": BASE_DIR / "gi_modules" / "imp-gi-risk-analyzer.py",
    "Planner": BASE_DIR / "gi_modules" / "imp-gi-planner.py",
    "Comm Log": BASE_DIR / "gi_modules" / "imp-gi-comm-log.py",
    "Implementation Log": BASE_DIR / "gi_modules" / "imp-gi-implementation-log.py",
    "Requests": BASE_DIR / "gi_modules" / "imp-gi-request.py",
}

spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("⚠️ Verification unavailable.")
        return False

def run_module(path, args):
    subprocess.run(["python3", str(path)] + args)

def module_menu(name, path, gi_name):
    while True:
        print(f"--- {name} Module ---")
        print("1. Add entry")
        print("2. List entries")
        print("3. Clear entries")
        print("4. Update from conversation")
        print("5. Back")
        choice = input("Select option: ").strip()
        if choice == "1":
            detail = input("Detail: ")
            run_module(path, [gi_name, detail])
        elif choice == "2":
            run_module(path, ["list", gi_name])
        elif choice == "3":
            run_module(path, ["clear", gi_name])
        elif choice == "4":
            run_module(path, ["update", gi_name])
        elif choice == "5":
            break
        else:
            print("Invalid selection.")


def show_menu():
    print("=== GI Modules Terminal ===")
    i = 1
    options = {}
    for key in MODULES:
        print(f"{i}. {key}")
        options[str(i)] = key
        i += 1
    print(f"{i}. Chat with GI")
    options[str(i)] = "chat"
    i += 1
    print(f"{i}. Quit")
    options[str(i)] = "quit"
    return options

def main():
    if not verify_user():
        return
    gi_name = input("GI name: ")
    while True:
        options = show_menu()
        choice = input("Select module: ").strip()
        action = options.get(choice)
        if not action:
            print("Invalid selection.")
            continue
        if action == "quit":
            break
        if action == "chat":
            subprocess.run(["python3", str(CHATBOT)])
            continue
        path = MODULES[action]
        module_menu(action, path, gi_name)

if __name__ == "__main__":
    main()

from pathlib import Path
import importlib.util
import subprocess
import os

BASE_DIR = Path(__file__).resolve().parents[1]
HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
GOOGLE_VERIFIER = BASE_DIR / "security" / "imp-google-identity-verifier.py"
CHATBOT = BASE_DIR / "interaction" / "imp-chatbot.py"
BUILDER = BASE_DIR / "interaction" / "imp-gi-builder.py"
MANAGER = BASE_DIR / "interaction" / "imp-gi-profile-manager.py"
VIEWER = BASE_DIR / "core" / "imp_gi_goal_viewer.py"
ANALYZER = BASE_DIR / "interaction" / "imp-conversation-analyzer.py"
MODULE_TERMINAL = BASE_DIR / "interaction" / "imp-gi-modules-terminal.py"
HISTORY_VIEWER = BASE_DIR / "interaction" / "imp-chat-history-viewer.py"
EXPLORER = BASE_DIR / "self-improvement" / "imp-module-explorer.py"
UPGRADER = BASE_DIR / "self-improvement" / "imp-self-upgrader.py"

spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("⚠️ Verification unavailable.")
        return False

spec_g = importlib.util.spec_from_file_location("gverify", GOOGLE_VERIFIER)
gverify = importlib.util.module_from_spec(spec_g)
try:
    spec_g.loader.exec_module(gverify)
    verify_google = gverify.verify_google_user
except Exception:
    def verify_google():
        print("⚠️ Google verification unavailable.")
        return False


def print_banner():
    banner = r"""
   ____ _                
  / ___(_)_ __ ___  ___ 
 | |   | | '__/ _ \/ __|
 | |___| | | |  __/\__ \
  \____|_|_|  \___||___/
"""
    print("\033[95m" + banner + "\033[0m")


def show_menu():
    print("\033[96m=== Cimp Terminal Interface ===\033[0m")
    print("1. Chat with Cimp (single prompt)")
    print("2. Build GI Profile")
    print("3. List GI Profiles")
    print("4. View GI Goals")
    print("5. Analyze Conversations")
    print("6. Manage GI Modules")
    print("7. View Chat History")
    print("8. Explore Modules")
    print("9. Self Upgrade")
    print("10. Quit")


def main():
    if os.environ.get("ENABLE_GOOGLE_SMS_VERIFICATION") == "1":
        if not verify_google():
            return
    if not verify_user():
        return
    print_banner()
    print("Welcome to the Cimp terminal. Enter a number to choose an action.")
    print("Type 10 or 'q' to quit.")
    while True:
        show_menu()
        choice = input("Select option: ").strip().lower()
        if choice == "1":
            subprocess.run(["python3", str(CHATBOT)])
        elif choice == "2":
            subprocess.run(["python3", str(BUILDER)])
        elif choice == "3":
            subprocess.run(["python3", str(MANAGER), "list"])
        elif choice == "4":
            subprocess.run(["python3", str(VIEWER)])
        elif choice == "5":
            subprocess.run(["python3", str(ANALYZER)])
        elif choice == "6":
            subprocess.run(["python3", str(MODULE_TERMINAL)])
        elif choice == "7":
            subprocess.run(["python3", str(HISTORY_VIEWER)])
        elif choice == "8":
            subprocess.run(["python3", str(EXPLORER)])
        elif choice == "9":
            subprocess.run(["python3", str(UPGRADER)])
        elif choice in ("10", "q"):
            print("Goodbye!")
            break
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()

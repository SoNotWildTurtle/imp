from pathlib import Path
import importlib.util
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
HEAVY_VERIFIER = BASE_DIR / 'security' / 'imp-heavy-identity-verifier.py'
BUILDER = BASE_DIR / 'interaction' / 'imp-gi-builder.py'
CREATOR = BASE_DIR / 'interaction' / 'imp-gi-creator.py'
MANAGER = BASE_DIR / 'interaction' / 'imp-gi-profile-manager.py'
MODULE_TERMINAL = BASE_DIR / 'interaction' / 'imp-gi-modules-terminal.py'

spec = importlib.util.spec_from_file_location('heavy', HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print('⚠️ Verification unavailable.')
        return False


def show_menu():
    print('=== GI Creation Terminal ===')
    print('1. Create GI Profile')
    print('2. Build GI Config')
    print('3. Manage Profiles')
    print('4. Manage GI Modules')
    print('5. Quit')


def main():
    if not verify_user():
        return
    while True:
        show_menu()
        choice = input('Select option: ').strip()
        if choice == '1':
            subprocess.run(['python3', str(BUILDER)])
        elif choice == '2':
            subprocess.run(['python3', str(CREATOR)])
        elif choice == '3':
            subprocess.run(['python3', str(MANAGER), 'list'])
        elif choice == '4':
            subprocess.run(['python3', str(MODULE_TERMINAL)])
        elif choice == '5':
            break
        else:
            print('Invalid selection.')


if __name__ == '__main__':
    main()

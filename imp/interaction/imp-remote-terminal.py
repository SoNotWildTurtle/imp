from pathlib import Path
import subprocess
import argparse
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
spec_log = importlib.util.spec_from_file_location(
    "log_manager", BASE_DIR / "managers" / "log_manager.py"
)
log_manager = importlib.util.module_from_spec(spec_log)
spec_log.loader.exec_module(log_manager)
append_log = log_manager.append_log

HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heavy)
verify_user = heavy.verify_user


def build_ssh_command(host, user=None, port="22", command="python imp/interaction/imp-gi-conversation-builder.py"):
    target = f"{user}@{host}" if user else host
    cmd = ["ssh"]
    if port and port != "22":
        cmd += ["-p", str(port)]
    cmd += [target, command]
    return cmd


def main():
    parser = argparse.ArgumentParser(description="Start a GI conversation builder on a remote host via SSH")
    parser.add_argument("--host", help="Remote host to connect to")
    parser.add_argument("--user", help="Username for SSH")
    parser.add_argument("--port", default="22", help="SSH port")
    parser.add_argument(
        "--command",
        default="python imp/interaction/imp-gi-conversation-builder.py",
        help="Command to run on the remote host",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the SSH command without running it")
    args = parser.parse_args()

    if not verify_user():
        return

    host = args.host or input("Remote host: ").strip()
    user = args.user or input("SSH username (leave blank for current user): ").strip() or None
    port = args.port or "22"
    command = args.command
    ssh_cmd = build_ssh_command(host, user, port, command)
    append_log("remote_terminal", {"host": host, "command": command})
    if args.dry_run:
        print(" ".join(ssh_cmd))
    else:
        subprocess.run(ssh_cmd)


if __name__ == "__main__":
    main()

from pathlib import Path
import json
import time
try:
    import psutil
except ImportError:  # pragma: no cover - handle missing dependency
    psutil = None

ROOT = Path(__file__).resolve().parents[1]
SECURITY_LOG = ROOT / "logs" / "imp-security-log.json"

# I love you -Alex
def is_being_traced():
    """Detect if the process is currently traced via /proc/self/status."""
    status_file = Path("/proc/self/status")
    if status_file.exists():
        for line in status_file.read_text().splitlines():
            if line.startswith("TracerPid:"):
                return int(line.split()[1]) != 0
    return False

# I love you -Alex
def check_debug_processes():
    """Look for common debugging tools that might modify memory."""
    if psutil is None:
        return False
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] in {"gdb", "strace", "ltrace"}:
            return True
    return False

# I love you -Alex
def log_event(event):
    """Append an event to the security log."""
    data = []
    if SECURITY_LOG.exists():
        with open(SECURITY_LOG, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "event": event})
    with open(SECURITY_LOG, "w") as f:
        json.dump(data, f, indent=4)

# I love you -Alex
def run_hardware_guard():
    """Check for debugging or tracing that could allow remote memory edits."""
    issues = []
    if is_being_traced():
        issues.append("Process is being traced")
    if check_debug_processes():
        issues.append("Debugging process detected")
    if issues:
        for issue in issues:
            print(f"[WARN] {issue}")
            log_event(issue)
    else:
        print("[+] Hardware guard found no issues.")

if __name__ == "__main__":
    run_hardware_guard()

import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVAL_FILE = ROOT / "logs" / "imp-major-rewrite-requests.json"
APPROVED_CHANGES_FILE = ROOT / "logs" / "imp-approved-rewrites.json"

def check_pending_rewrites():
    if not os.path.exists(APPROVAL_FILE):
        return []

    with open(APPROVAL_FILE, "r") as f:
        return [json.loads(line) for line in f.readlines()]

def request_approval():
    pending_rewrites = check_pending_rewrites()
    
    if not pending_rewrites:
        print("[+] No pending major rewrite requests.")
        return

    print("\n🚀 **Pending Major Rewrite Requests:**")
    for i, request in enumerate(pending_rewrites):
        print(f"{i + 1}. **File:** {request['file']}")
        print(f"   **Reason:** {request['reason']}\n")

    choice = input("Approve a rewrite (enter number) or press Enter to skip: ")
    if choice.isdigit():
        chosen_request = pending_rewrites[int(choice) - 1]
        
        # Apply major rewrite
        os.system(f"python3 {ROOT / 'self-improvement' / 'imp-code-updater.py'} {chosen_request['file']}")

        print(f"[+] ✅ Approved major rewrite for {chosen_request['file']}. IMP will now apply changes.")

        # Store approved changes
        with open(APPROVED_CHANGES_FILE, "a") as f:
            json.dump(chosen_request, f, indent=4)

        # Remove approved request from the queue
        with open(APPROVAL_FILE, "w") as f:
            json.dump([r for r in pending_rewrites if r["file"] != chosen_request["file"]], f, indent=4)

if __name__ == "__main__":
    request_approval()

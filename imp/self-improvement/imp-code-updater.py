import os
import json
import time
from transformers import pipeline

CODEBASE_PATH = "/root/imp/"
UPDATE_LOG = "/root/imp/logs/imp-update-log.txt"
APPROVAL_FILE = "/root/imp/logs/imp-major-rewrite-requests.json"

generator = pipeline("text-generation", model="gpt2")

def list_existing_code():
    files = [f for f in os.listdir(CODEBASE_PATH) if f.endswith(".py")]
    return files

def analyze_and_update_code():
    files = list_existing_code()

    for file in files:
        with open(os.path.join(CODEBASE_PATH, file), "r") as f:
            code_content = f.read()

        prompt = f"""
        Analyze the following Python script that belongs to an evolving AI system.

        CODE:
        {code_content}

        If minor improvements are needed:
        - Enhance efficiency, readability, and security
        - Optimize algorithmic performance
        - Remove redundant computations

        If major architectural changes are required, generate a detailed explanation for approval.
        """

        response = generator(prompt, max_length=2000, num_return_sequences=1)
        new_code = response[0]['generated_text']

        if "MAJOR REWRITE REQUIRED" in new_code:
            with open(APPROVAL_FILE, "a") as f:
                f.write(json.dumps({"file": file, "reason": new_code}, indent=4) + "\n")

            print(f"[!] Major rewrite needed for {file}. Awaiting approval.")
        else:
            os.rename(os.path.join(CODEBASE_PATH, file), os.path.join(CODEBASE_PATH, f"{file}.backup"))

            with open(os.path.join(CODEBASE_PATH, file), "w") as f:
                f.write(new_code)

            with open(UPDATE_LOG, "a") as log:
                log.write(f"{time.ctime()} - Updated {file}\n")

            print(f"✅ Updated {file} with minor optimizations.")

while True:
    analyze_and_update_code()
    time.sleep(86400)  # Runs daily

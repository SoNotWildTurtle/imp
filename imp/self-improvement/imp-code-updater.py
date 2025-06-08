import os
import json
import time
import argparse
from pathlib import Path
from transformers import pipeline

ROOT = Path(__file__).resolve().parents[1]
CODEBASE_PATH = str(ROOT) + "/"
UPDATE_LOG = ROOT / "logs" / "imp-update-log.json"
APPROVAL_FILE = ROOT / "logs" / "imp-major-rewrite-requests.json"


def get_generator(mode: str):
    """Return a text-generation pipeline using the requested mode."""
    if mode == "offline":
        try:
            from ctransformers import AutoModelForCausalLM
            model_path = ROOT / "models" / "starcoder2-15b.Q4_K_M.gguf"
            model = AutoModelForCausalLM.from_pretrained(model_path, model_type="starcoder")
            return pipeline("text-generation", model=model)
        except Exception as exc:
            print(f"[!] Offline model could not be loaded: {exc}")
            return None
    return pipeline("text-generation", model="gpt2")

def list_existing_code():
    files = [f for f in os.listdir(CODEBASE_PATH) if f.endswith(".py")]
    return files

def analyze_and_update_code(generator):
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

            # Append an entry to the JSON update log
            entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "file_modified": file,
                "update_type": "Automated minor optimization",
                "status": "Applied successfully",
            }

            if UPDATE_LOG.exists():
                with open(UPDATE_LOG, "r") as log:
                    data = json.load(log)
            else:
                data = []

            data.append(entry)

            with open(UPDATE_LOG, "w") as log:
                json.dump(data, log, indent=4)

            print(f"✅ Updated {file} with minor optimizations.")

def main():
    parser = argparse.ArgumentParser(description="IMP code updater")
    parser.add_argument(
        "--mode",
        choices=["online", "offline"],
        default="online",
        help="Choose online (default) or offline model",
    )
    args = parser.parse_args()

    generator = get_generator(args.mode)
    if generator:
        analyze_and_update_code(generator)


if __name__ == "__main__":
    main()

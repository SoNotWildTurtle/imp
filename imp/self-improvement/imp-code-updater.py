import os
import json
import time
import argparse
from pathlib import Path
from transformers import pipeline
from . import imp_mode_advisor as mode_advisor

# 2025-06-08: Reflective Recursive Enumeration Blockchain Self-Healing idea.
# IMP should favor additive code changes and preserve backups so no functionality
# is lost. The snippet below outlines a potential ledger-based approach.
#
# def blockchain_self_heal():
#     """Log code hashes to a blockchain to enable recovery of any past version."""
#     pass

ROOT = Path(__file__).resolve().parents[1]
CODEBASE_PATH = str(ROOT) + "/"
UPDATE_LOG = ROOT / "logs" / "imp-update-log.json"
APPROVAL_FILE = ROOT / "logs" / "imp-major-rewrite-requests.json"
PATCH_DIR = ROOT / "logs" / "imp-update-patches"
PATCH_DIR.mkdir(exist_ok=True)


def decide_mode() -> str:
    """Decide generation mode using spatiotemporal confidence."""
    offline_model = (ROOT / "models" / "starcoder2-15b.Q4_K_M.gguf").exists()
    return mode_advisor.choose_generation_mode(offline_model)


def get_generator(mode: str):
    """Return a text-generation pipeline using the requested mode."""
    if mode == "auto":
        mode = decide_mode()
    if mode == "offline":
    #alex again: figure this one out using chatGPT's goal requesting feature you have.
    #https://huggingface.co/nold/starcoder2-15b-GGUF?library=transformers
    #https://huggingface.co/docs/transformers/main_classes/pipelines
    #https://www.nsa.gov/About/Cybersecurity-Collaboration-Center/Standards-and-Certifications/
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

# Generate and store a unified diff patch for review
# The patch is additive, preserving original code for recovery
def write_patch(original, updated, file_name):
    import difflib
    diff = "\n".join(difflib.unified_diff(
        original.splitlines(),
        updated.splitlines(),
        fromfile=file_name + ".orig",
        tofile=file_name + ".new",
    ))
    timestamp = time.strftime("%Y%m%d%H%M%S")
    patch_path = PATCH_DIR / f"{file_name}.{timestamp}.patch"
    with open(patch_path, "w") as p:
        p.write(diff)
    return str(patch_path)


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
        quality = mode_advisor.evaluate_request_quality(new_code)
        patch_file = write_patch(code_content, new_code, file)

        if "MAJOR REWRITE REQUIRED" in new_code:
            with open(APPROVAL_FILE, "a") as f:
                f.write(json.dumps({"file": file, "reason": new_code}, indent=4) + "\n")

            print(f"[!] Major rewrite needed for {file}. Awaiting approval.")
        else:
            timestamp = time.strftime("%Y%m%d%H%M%S")
            os.rename(
                os.path.join(CODEBASE_PATH, file),
                os.path.join(CODEBASE_PATH, f"{file}.backup.{timestamp}")
            )
            # Preserve previous versions for recovery; IMP should be additive.

            with open(os.path.join(CODEBASE_PATH, file), "w") as f:
                f.write(new_code)

            # Append an entry to the JSON update log
            entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "file_modified": file,
                "update_type": "Automated minor optimization",
                "patch": patch_file,
                "quality": quality,
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

            print(f"Updated {file} with minor optimizations.")

def main():
    parser = argparse.ArgumentParser(description="IMP code updater")
    parser.add_argument(
        "--mode",
        choices=["online", "offline", "auto"],
        default="auto",
        help="Choose online, offline, or auto mode",
    )
    args = parser.parse_args()

    generator = get_generator(args.mode)
    if generator:
        analyze_and_update_code(generator)


if __name__ == "__main__":
    main()

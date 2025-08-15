# Cimp Repository Agent Instructions

This repository (formerly named **imp**) hosts the Cimp project.

## Running Tests
- On Linux or macOS run `bash imp/tests/run-all-tests.sh` from the repository root.
- On Windows run `python imp/tests/run_all_tests.py` (or `./imp/tests/run-all-tests.ps1`).
- The tests automatically skip parts that require unavailable packages or network access.

## Setup
- Run `./setup.sh` to install Python dependencies (`pyotp`, `google-auth`, `google-auth-oauthlib`).
- Optional environment variables can be set in `codex.env`.

Most scripts depend on the heavy identity verifier in `imp/security`. If `pyotp` is
missing, related tests are skipped.

All Python modules use relative paths starting at the `imp/` directory, so the repository can be placed anywhere.


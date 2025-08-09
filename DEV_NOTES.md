# Developer Notes

Cimp provides utilities to create and evolve custom general intelligences.
All tools reside under the `imp/` directory. Modules use relative paths and log
data in `imp/logs/`.

The offline evolver aggregates skill, performance, and conversation insight
logs to suggest new skills and record average resource usage when network
access is unavailable.

## Workflow
1. Run `./setup.sh` once to install dependencies.
2. Develop new features or modules under `imp/`.
3. On Linux/macOS run `bash imp/tests/run-all-tests.sh` before committing.
   Windows developers can use `python imp/tests/run_all_tests.py`.
4. Most utilities call the heavy identity verifier which requires an OTP code
   and passphrase. Tests will simulate this when `pyotp` is available.

Tests skip optional sections when dependencies are missing or network access is
restricted.

`imp/interaction/imp-remote-terminal.py` can launch the conversation-based GI
builder on another machine via SSH. Use the `--dry-run` flag to review the
generated command before connecting; each invocation is logged for later review.

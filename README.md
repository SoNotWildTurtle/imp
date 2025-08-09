# Cimp

Cimp is a toolkit for building and evolving general intelligences. All source files live under the `imp/` directory.
Run `./setup.sh` once to install required Python packages.

Most utilities require multi-factor verification using the scripts in `imp/security/`.
The heavy identity verifier combines OTP codes with a passphrase and locks out
users after repeated failures.
If `ENABLE_GOOGLE_SMS_VERIFICATION=1` and Twilio credentials are provided, the
terminal interface first verifies your Google ID token and sends a six-digit code
via SMS before proceeding.
The AI countermeasure analyzer (`imp/security/imp-ai-countermeasures.py`) reviews
threat logs over time and records automatic defenses when hostile activity is
detected.

The chat history viewer (`imp/interaction/imp-chat-history-viewer.py`) lets you
review or clear logged conversations. The module explorer
(`imp/self-improvement/imp-module-explorer.py`) collects information about all
repository modules for training or analysis. The offline evolver
(`imp/self-improvement/imp-offline-evolver.py`) reviews skill, performance, and
conversation insight logs to recommend new skills and average resource usage
even without network access.
Several GI modules record ongoing experience:
`imp/gi_modules/imp-gi-memory.py` for memories,
`imp/gi_modules/imp-gi-task-manager.py` for tasks,
`imp/gi_modules/imp-gi-self-evolver.py` for evolution ideas and
`imp/gi_modules/imp-gi-knowledge.py` for structured facts,
`imp/gi_modules/imp-gi-skill-tracker.py` for logging skills,
`imp/gi_modules/imp-gi-performance.py` for resource usage,
`imp/gi_modules/imp-gi-safety.py` for recording safety guidelines. Each module now
`imp/gi_modules/imp-gi-risk-analyzer.py` for tracking potential threats, and
`imp/gi_modules/imp-gi-planner.py` for outlining work plans,
`imp/gi_modules/imp-gi-comm-log.py` for communication history, and
`imp/gi_modules/imp-gi-implementation-log.py` for tracking implemented features,
`imp/gi_modules/imp-gi-request.py` for logging feature requests. Each module now
supports listing, clearing or updating entries using conversation insights.
When you build a new intelligence configuration, these modules are automatically
listed under the `modules` field so the GI has standalone capabilities from day
one. During profile creation you can review the available modules and choose
which ones to include.

Use the profile manager (`imp/interaction/imp-gi-profile-manager.py`) to list,
remove or update saved intelligence profiles.
For a single entry point to common features, run
`imp/interaction/imp-terminal.py`. The menu lets you chat with Cimp, build or
list profiles, review goals, analyze conversations, manage GI modules,
inspect chat history, explore available modules and trigger self-upgrades. The
terminal now shows a small color banner, prints brief instructions and accepts
`q` as a shortcut to quit.
For quick interaction with these built-in modules, run
`imp/interaction/imp-gi-modules-terminal.py` which shows a menu for storing or
reviewing memories, tasks and more, or chatting with the GI.

End users can review pending feature requests with
`imp/interaction/imp-gi-client-dashboard.py` and choose which ones to forward.
The dashboard opens with a short explanation and confirms when all requests are
processed. Confirmed requests are then reviewed by operators using
`imp/interaction/imp-gi-operator-dashboard.py`. Approved upgrades automatically
snapshot the target configuration so changes can be rolled back and log the
implementation. For a browser-based overview of pending items and live
statistics, launch the web dashboard with
`python3 imp/interaction/imp-gi-web-dashboard.py` and open the displayed URL.
To focus specifically on creating new intelligences, use
`imp/interaction/imp-gi-builder-terminal.py` which provides a simple menu for
building profiles, creating configs and managing GI modules.

For a fully conversational workflow run
`python3 imp/interaction/imp-gi-conversation-builder.py`. It starts with a short
chat to gather requirements, analyzes the conversation for common keywords and
uses them to suggest skills, focus areas and relevant modules before asking for
structured details and module selection.

For cooperative builds with end users, run
`python3 imp/interaction/imp-gi-conversation-dashboard.py` to launch a small web
app. The script prints the port it listens on so you can easily forward that
port for remote connections. It collects a name for the intelligence, saves a
profile and configuration, and automatically packages the config with its
modules for download using `imp/interaction/imp-gi-packager.py`.
Each created intelligence stores this port in its configuration and modules such
as `imp-gi-request.py` remind the AI that functionality requests must be
confirmed by Cimp on that port.

To start a conversation builder on a separate machine over SSH, use
`imp/interaction/imp-remote-terminal.py`. After verification it constructs and
executes an SSH command to run the conversation builder remotely and logs the
target host for later reference. A `--dry-run` flag prints the command without
connecting so operators can confirm the details.

## Running Tests
- Linux/macOS: `bash imp/tests/run-all-tests.sh`
- Windows: `python imp/tests/run_all_tests.py` or run the provided PowerShell script.
Tests automatically skip portions that require missing packages or network access.


# IMP Project Overview

This repository contains the Intelligent Management Platform (IMP).
The project is organized into directories of scripts, configuration files,
logs, and notes. The sections below describe each directory and file,
including how the components interact.

## Directory Layout

- **bin** – Entry scripts for starting, stopping, updating and managing IMP.
- **config** – JSON configuration files and the configuration manager.
- **core** – Core runtime modules for neural networks, goal handling and execution.
- **expansion** – Distributed computing utilities for clusters and intranet tasks.
- **logs** – JSON log files and the log manager script.
- **models** – Placeholder directory for offline neural models (GGUF files).
- **notes** – Research notes, personal comments and design documents.
- **security** – Modules providing automated defense and monitoring.
- **self-improvement** – Code updating and metacognitive modules.
- **tests** – Test suite verifying system functionality.

## File Descriptions

Below is a brief description of each file in the repository.
imp/bin/imp-backup.sh - Creates an encrypted tarball of the project for backups. Called manually.
imp/bin/imp-chat.sh - Launches the goal chat assistant for interacting with ChatGPT.
imp/bin/imp-enhance.sh - Wrapper for imp-code-updater.py choosing online or offline mode.
imp/bin/imp-install.sh - Installs Python requirements and starts the system.
imp/bin/imp-goal.sh - Manage goals with add, list, and execute options.
imp/bin/imp-restore.sh - Restores a backup archive into the project directory.
imp/bin/imp-self-destruct.sh - Disabled deletion script, kept for reference.
imp/bin/imp-start.sh - Starts core services like imp-execute.py and monitors.
imp/bin/imp-status.sh - Shows running IMP processes from the logs.
imp/bin/imp-stop.sh - Stops running IMP processes using pkill.
imp/bin/imp-update.sh - Updates the codebase via git pull.
imp/bin/imp-login.sh - Prompts for credentials and logs authentication attempts.
imp/bin/imp-voice.sh - Speaks provided text through pyttsx3.
imp/config/imp-config-manager.py - Loads and modifies JSON config files on demand.
imp/config/imp-environment.json - Default environment paths used by scripts.
imp/config/imp-intranet.json - Example intranet node configuration.
imp/config/imp-personality.json - Personality settings for the AI.
imp/config/imp-system-settings.json - General system options and feature flags.
imp/config/imp-user-permissions.json - Trusted and restricted user list.
imp/config/imp-user-registration.json - Tracks registered operators.
imp/config/imp-credentials.json - Usernames with hashed passwords for login.
imp/config/imp-google-oauth.json - OAuth client secrets for automated Google verification.
imp/core/imp-3d-neural-network.py - Experimental 3D neural network implementation.
imp/core/imp-decision-forecaster.py - Predicts outcomes of potential goals.
imp/core/imp-execute.py - Main runtime harness launching submodules.
imp/core/imp-goal-chat.py - CLI to discuss goals via ChatGPT.
imp/core/imp-goal-manager.py - Stores, prioritizes and retrieves goals.
imp/core/imp-learning-memory.py - Keeps a log of learned plans and results.
imp/core/imp-neural-network.py - Minimal feedforward network for experiments.
imp/core/imp-voice.py - Provides basic voice synthesis using pyttsx3.
imp/core/imp-status-monitor.py - Checks resource usage and writes status logs.
imp/core/imp-strategy-generator.py - Creates high-level plans from goals.
imp/core/imp-task-executor.py - Executes planned tasks sequentially.
imp/core/imp-adaptive-planner.py - Breaks directives into weighted subgoals.
imp/core/imp-message-bus.py - JSON-backed queue with priority and broadcast support.
imp/expansion/imp-cluster-manager.py - Controls distributed nodes for heavy workloads.
imp/expansion/imp-intranet.py - Simple intranet builder for secure packet routing.
imp/expansion/imp-load-scheduler.py - Balances job assignments across nodes.
imp/expansion/imp-node-communicator.py - Sends and receives messages between nodes.
imp/expansion/imp-node-monitor.py - Records health data about remote nodes.
imp/expansion/imp-resource-balancer.py - Reallocates CPU/RAM among tasks.
imp/logs/imp-log-manager.py - Utility for writing entries to the JSON logs.
imp/models/README.md - Notes on storing GGUF models for offline enhancement.
imp/notes/README.md - Describes purpose of the notes folder.
imp/notes/alex-comment.txt - User-supplied personal comment.
imp/notes/blockchain-self-healing.txt - Idea for blockchain-based code recovery.
imp/notes/example.txt - Placeholder note for demonstrations.
imp/notes/imp-poison-defense.txt - Guidance on mitigating data poisoning.
imp/notes/imp-research-roadmap.txt - Roadmap for advancing IMP capabilities.
imp/notes/intranet-scapy-guide.txt - Quick tutorial on packet sanitation.
imp/notes/next-gen-imp-strategy.txt - Strategies for long-term AI evolution.
imp/notes/self-evolution-analysis.txt - Results from early self-evolution tests.
imp/requirements.txt - Python dependencies required for IMP, including google-auth and google-auth-oauthlib for automated Google login.
imp/security/imp-automated-defense.py - Gathers system data and hardens services.
imp/security/imp-firewall-manager.py - Basic firewall management helpers.
imp/security/imp-integrity-checker.py - Verifies core files against stored checksums.
imp/security/imp-log-analyzer.py - Scans logs for signs of compromise.
imp/security/imp-poison-detector.py - Detects unexpected changes to training data.
imp/security/imp-security-optimizer.py - Runs security audits and patch routines.
imp/security/imp-threat-monitor.py - Monitors running services for anomalies.
imp/security/imp-vulnerability-scanner.py - Looks for weak permissions or secrets.
imp/security/imp-authenticator.py - Verifies user credentials, automates Google OAuth2 login, and records attempts.
imp/self-improvement/imp-code-predictor.py - Predicts code quality of new changes.
imp/self-improvement/imp-code-updater.py - Applies code patches using LLMs.
imp/self-improvement/imp-metacognitive-analysis.py - Evaluates self-evolution progress.
imp/self-improvement/imp-model-analyzer.py - Compares neural network versions.
imp/self-improvement/imp_mode_advisor.py - Chooses offline vs online enhancement using spatiotemporal confidence.
imp/self-improvement/imp-rewrite-approval.py - Requests human approval before heavy rewrites.
imp/self-improvement/imp-self-tuner.py - Adjusts parameters based on performance logs.
imp/self-improvement/imp-version-tracker.py - Records every version of changed files.
imp/self-improvement/imp-bug-hunter.py - Scans all Python files for syntax errors.
imp/tests/run-all-tests.sh - Executes the full test suite in sequence.
imp/tests/test-3d-network.py - Unit test for the 3D neural network module.
imp/tests/test-automated-defense.py - Test for automated defense cycle.
imp/tests/test-config.py - Checks configuration handling.
imp/tests/test-core-functions.py - Validates main runtime functions.
imp/tests/test-expansion.py - Tests distributed expansion modules.
imp/tests/test-install.py - Ensures requirements installer works.
imp/tests/test-intranet.py - Confirms intranet builder logic.
imp/tests/test-logs.py - Verifies logs can be read and written.
imp/tests/test-metacognition.py - Runs metacognitive analysis test.
imp/tests/test-model-analysis.py - Checks model comparison features.
imp/tests/test-neural-network.py - Tests the minimal neural network.
imp/tests/test-performance.py - Measures performance metrics logging.
imp/tests/test-security.py - Runs security scripts without damaging the system.
imp/tests/test-self-improvement.py - Tests the self-update mechanisms.
imp/tests/test-bug-hunter.py - Ensures the bug hunting tool runs without errors.
imp/tests/test-mode-advisor.py - Verifies spatiotemporal mode selection logic.
imp/tests/test-message-bus.py - Ensures queued messages send and receive correctly.

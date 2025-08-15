# IMP Project Overview

This repository contains the Intelligent Management Platform (IMP).
The project is organized into directories of scripts, configuration files,
logs, and notes. The sections below describe each directory and file,
including how the components interact.

For installation and startup details, see [SETUP.md](SETUP.md).

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
imp/bin/imp-chat.sh - Launches the goal chat assistant for interacting with ChatGPT; requires an interactive terminal.
imp/bin/imp-enhance.sh - Wrapper for imp-code-updater.py choosing online or offline mode.
imp/bin/imp-install.sh - Installs Python requirements and starts the system.
imp/bin/imp-restore.sh - Restores a backup archive into the project directory.
imp/bin/imp-self-destruct.sh - Disabled deletion script, kept for reference.
imp/bin/imp-start.sh - Starts core services by launching /root/imp/core/imp-execute.py.
imp/bin/imp-start.py - Python version of the startup script for Windows.
imp-start.ps1 - PowerShell wrapper that installs Python if needed and runs imp\bin\imp-start.py in a restart loop to keep the terminal alive.
imp/bin/imp-status.sh - Shows running IMP processes from the logs.
imp/bin/imp-mood.sh - Queries or adjusts the AI's mood using imp-mood-manager.py.
  Supports `--event` to record notable events.
imp/bin/imp-motivate.sh - Generates self-motivated goals based on mood.
imp/bin/imp-nn-menu.sh - Lists or registers neural networks via the manager.
imp/bin/imp-stop.sh - Stops running IMP processes using pkill.
imp/bin/imp-stop.py - Python version of the shutdown script for Windows.
imp/bin/imp-update.sh - Updates the codebase via git pull.
imp/bin/imp-login.sh - Prompts for credentials and logs authentication attempts.
imp/bin/imp-self-heal.sh - Runs the ledger-based self-healer.
imp/bin/imp-auto-heal.sh - Performs automatic verification and healing based on system settings.
imp/bin/imp-defend.sh - Executes the automated defense cycle.
imp/bin/imp-network-audit.sh - Audits network connections against a baseline.
imp/bin/imp-network-monitor.sh - Logs new remote connections for review.
imp/bin/imp-google-login.sh - Starts a Google OAuth flow for the configured account.
imp/bin/imp-voice.sh - Speaks provided text through pyttsx3 with adjustable voice options, including voice selection by name.
imp/bin/imp-voice-menu.sh - Interactive menu for adjusting voice settings with sliders.
imp/bin/imp-speech.sh - Captures microphone or audio file input using speech recognition.
imp/bin/imp-chat.sh - Goal chat assistant; add `--speech` to capture microphone input via speech-to-text.
imp/config/imp-config-manager.py - Loads and modifies JSON config files on demand.
imp/config/imp-environment.json - Default environment paths used by scripts.
imp/config/imp-intranet.json - Example intranet node configuration.
imp/config/imp-cluster-nodes.json - List of nodes managed by the secure node manager.
imp/config/imp-personality.json - Personality settings for the AI.
imp/config/imp-system-settings.json - General system options and feature flags.
  The self_healing section now includes a "mint" flag to snapshot code after healing.
imp/config/imp-user-permissions.json - Trusted and restricted user list.
imp/config/imp-user-registration.json - Tracks registered operators.
imp/config/imp-credentials.json - Usernames with hashed passwords for login.
imp/config/imp-google-oauth.json - OAuth client secrets for automated Google verification.
imp/communication/imp-command-transformer.py - Sanitizes and translates aliased commands via a secure diamond handshake with nonce and HMAC.
imp/communication/communication-notes.txt - Design notes for the alias communication channel.
imp/core/imp-3d-neural-network.py - Experimental 3D neural network implementation.
  Supports `spawn_advanced_neuron` for creating specialized neurons and tracking usage patterns.
  Includes `spawn_novel_neuron` to automatically create uniquely typed neurons for experiments.
  `guide_novel_neuron` connects a new neuron to the most active pathway so it can learn a useful role.
  The `evolve` method marks rarely used neurons `dormant` instead of deleting them so they can reawaken when needed.
  Connections store a `task` label so pathways can be reinforced by Schwann- or
  oligodendrocyte-like neurons per task.
  `forward_by_angle` routes spikes through connections that match a desired
  direction vector, isolating task pathways to reduce poisoning risk.
  `find_optimal_path` computes the lowest-resistance path between two neurons.
  `auto_evolve` reinforces frequently used connections and spawns a novel neuron automatically.
  `simulate_evolution` returns an evolved copy for sandbox testing without altering the active network.
imp/core/imp-resource-nn.py - Manages CPU/memory and pinned RAM/VRAM with self-evolving oligodendrocyte connections for long-term stability.
imp/core/imp-resource-engine.py - Samples system load, pins memory on request and trains the resource network for safe operation.
imp/core/imp-decision-forecaster.py - Predicts outcomes of potential goals.
imp/core/imp-execute.py - Main runtime harness launching submodules and registering resource, defense, network_task, bbi, collaboratory, and adversarial networks.
imp/core/imp_neural_manager.py - Central registry with `get_or_create`, `list`, and `unregister` helpers so engines share neural networks.
imp/core/imp-goal-chat.py - Chatbot supporting multi-turn context, offline fallback, optional speech input; assumes a local user is at the keyboard.
imp/core/imp-goal-manager.py - Stores, prioritizes and retrieves goals; generates goals online or via local fallback.
imp/core/imp-learning-memory.py - Keeps a log of learned plans and results.
imp/core/imp-neural-network.py - Feedforward network with basic backpropagation and training helpers.
imp/core/imp-nn-menu.py - CLI helper to register or list neural networks via the manager.
imp/core/imp-adversarial-nn.py - Generator network that produces perturbations for adversarial training.
imp/core/imp-network-task-nn.py - Secondary neural network specialized for network tasks.
imp/self-improvement/imp-network-task-trainer.py - Improves the network task model using diff logs.
imp/core/imp-network-task-engine.py - Uses the manager-controlled network task model to decide when to run audits.
imp/core/imp-defense-nn.py - Neural network that predicts when to trigger automated defenses.
imp/self-improvement/imp-defense-trainer.py - Trains the defense model from network audit logs.
imp/core/imp-defense-engine.py - Runs the defense model and launches imp-automated-defense.py when needed.
imp/core/imp-collaboratory-nn.py - Neural network that assists with collaborative network design tasks.
imp/core/imp-collaboratory-engine.py - Runs a manager-registered collaboratory network to evaluate collaboration plans.
imp/core/imp-bbi-nn.py - Brain-to-brain interface network that evolves to manage user and IMP dreamscape interactions.
imp/core/imp-bbi-engine.py - Logs BBI signals and evolves a neural manager-driven network for Sword Art Online-style dreamscapes.
imp/self-improvement/imp-adversarial-trainer.py - Trains networks against adversarial examples using the adversarial generator.
imp/core/imp-voice.py - Provides voice synthesis with selectable voices by index or name, adjustable rate, and volume.
imp/core/imp-voice-menu.py - Curses-based interface to tweak voice, rate and volume interactively.
imp/core/imp-speech-to-text.py - Converts speech from a microphone or audio file to text, falling back to PocketSphinx when offline.
imp/core/imp-mood-manager.py - Tracks the AI's mood, gradually returns to a slightly positive baseline, and updates mood based on events.
imp/core/imp-motivation.py - Generates self-motivated goals from mood.
imp/core/imp-status-monitor.py - Checks resource usage and writes status logs.
imp/core/imp-strategy-generator.py - Creates high-level plans from goals.
imp/core/imp-task-executor.py - Executes planned tasks sequentially.
imp/core/imp-adaptive-planner.py - Breaks directives into weighted subgoals using ChatGPT online or heuristics offline.
imp/core/imp-message-bus.py - JSON-backed queue with priority and broadcast support.
imp/expansion/imp-cluster-manager.py - Controls distributed nodes for heavy workloads.
imp/expansion/imp-intranet.py - Simple intranet builder for secure packet routing.
imp/expansion/imp-load-scheduler.py - Balances job assignments across nodes.
imp/expansion/imp-node-communicator.py - Sends and receives messages between nodes.
imp/expansion/imp-node-monitor.py - Records health data about remote nodes.
imp/expansion/imp-resource-balancer.py - Reallocates CPU/RAM among tasks.
imp/expansion/imp-secure-node-manager.py - Manages node registration and secure commands with helpers to list and remove nodes.
imp/expansion/imp-distributed-queue.py - Tracks tasks and assigns them to available nodes.
imp/expansion/imp-distributed-memory.py - Stores key/value facts for cross-node sharing.
imp/expansion/imp-game-copilot.py - Learns new games and builds Sword Art Online-inspired dreamscapes for blockchain experiments.
imp/logs/imp-log-manager.py - Utility for writing entries to the JSON logs.
imp/logs/imp-distributed-memory.json - Shared memory store for distributed data.
imp/logs/imp-blockchain-ledger.json - Ledger of code hashes for self-healing.
imp/logs/imp-code-map.json - Map of files, functions and classes produced by imp-code-map.py.
imp/logs/imp-self-heal-log.json - Records automatic restoration actions.
imp/logs/imp-lint-report.json - Results from flake8 lint checks during self-healing.
imp/logs/imp-bbi-log.json - Records BBI interactions for dreamscape management.
imp/logs/imp-sandbox-log.json - Summaries from debug sandbox evolution runs.
imp/logs/imp-resource-log.json - CPU/memory usage history for resource management.
imp/logs/imp-games.json - Learned game definitions for the copilot.
imp/logs/imp-dreamscape.json - Music dreamscape themes generated from games.
imp/logs/imp-update-patches/ - Stores diff patches for manual review when files cannot be restored automatically.
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
imp/notes/self-evolution-plan.txt - Goals and steps for extending IMP's self-evolution.
imp/notes/imp-developer-notes.txt - Explains coding decisions and recommended module usage.
imp/notes/self-evolution-dev-notes.txt - Developer notes for implementing the plan.
imp/notes/startup-verification.txt - Stepwise log confirming each launch step and its status.
imp/requirements.txt - Python dependencies required for IMP, including google-auth, google-auth-oauthlib, and psutil for hardware checks.
imp/security/imp-automated-defense.py - Gathers system data and hardens services.
imp/security/imp-firewall-manager.py - Basic firewall management helpers.
imp/security/imp-integrity-checker.py - Verifies core files against stored checksums.
imp/security/imp-log-analyzer.py - Scans logs for signs of compromise.
imp/security/imp-poison-detector.py - Detects unexpected changes to training data.
imp/security/imp-security-optimizer.py - Runs security audits and patch routines.
imp/security/imp-threat-monitor.py - Monitors running services for anomalies.
imp/security/imp-vulnerability-scanner.py - Looks for weak permissions or secrets.
imp/security/imp-hardware-guard.py - Detects debugging or tracing that could allow remote memory edits.
imp/security/imp-network-auditor.py - Logs unexpected network connections for review.
imp/security/imp-network-monitor.py - Tracks new remote IPs and records deviations from baseline.
imp/security/imp-authenticator.py - Verifies user credentials, automates Google OAuth2 login, adds Twilio 2FA, and forces re-login after 5 minutes of idle time.
imp/self-improvement/imp-code-predictor.py - Predicts code quality of new changes.
imp/self-improvement/imp-code-updater.py - Applies code patches using LLMs, with a simple pass-through when offline models are missing.
imp/self-improvement/imp-metacognitive-analysis.py - Evaluates self-evolution progress.
imp/self-improvement/imp-model-analyzer.py - Compares neural network versions.
imp/self-improvement/imp-3d-network-tester.py - Generates candidate 3D networks and logs differences before replacing.
imp/self-improvement/imp-debug-sandbox.py - Runs self-evolution experiments in isolation and logs summaries.
imp/self-improvement/imp_mode_advisor.py - Chooses offline vs online enhancement using spatiotemporal confidence.
imp/self-improvement/imp-rewrite-approval.py - Requests human approval before heavy rewrites.
imp/self-improvement/imp-self-tuner.py - Adjusts parameters based on performance logs.
imp/self-improvement/imp-version-tracker.py - Records every version of changed files.
imp/self-improvement/imp-bug-hunter.py - Scans all Python files for syntax errors.
imp/self-improvement/imp-blockchain-ledger.py - Logs code hashes in a simple blockchain for self-healing.
imp/self-improvement/imp-code-map.py - Generates a JSON map of functions and classes across the codebase for introspection.
imp/self-improvement/imp-self-healer.py - Restores mismatched files using the blockchain ledger.
imp/self-improvement/imp-self-healer.py also offers ChatGPT recovery for missing modules when enabled.
imp/self-improvement/imp-self-healer.py can optionally mint a new block after healing to snapshot the updated code.
imp/self-improvement/imp-auto-heal.py - Runs self-healing automatically based on configuration settings.
imp/tests/run-all-tests.sh - Executes the full test suite in sequence.
imp/tests/test-3d-network.py - Unit test for the 3D neural network module.
imp/tests/test-automated-defense.py - Test for automated defense cycle.
imp/tests/test-hardware-guard.py - Runs the hardware guard checker.
imp/tests/test-config.py - Checks configuration handling.
imp/tests/test-core-functions.py - Validates main runtime functions.
imp/tests/test-expansion.py - Tests distributed expansion modules.
imp/tests/test-install.py - Ensures requirements installer works.
imp/tests/test-intranet.py - Confirms intranet builder logic.
imp/tests/test-logs.py - Verifies logs can be read and written.
imp/tests/test-metacognition.py - Runs metacognitive analysis test.
imp/tests/test-model-analysis.py - Checks model comparison features.
imp/tests/test-neural-network.py - Tests the minimal neural network.
imp/tests/test-nn-menu.py - Verifies neural manager CLI listing.
imp/tests/test-network-task-nn.py - Tests the network task neural network.
imp/tests/test-network-task-trainer.py - Ensures the network task improver runs.
imp/tests/test-network-task-engine.py - Runs the network task engine using the model.
imp/tests/test-defense-nn.py - Tests the defense neural network.
imp/tests/test-defense-trainer.py - Ensures the defense network improver runs.
imp/tests/test-defense-engine.py - Runs the defense engine using the model.
imp/tests/test-bbi-engine.py - Validates the brain-to-brain interface engine and its evolving network.
imp/tests/test-performance.py - Measures performance metrics logging.
imp/tests/test-security.py - Runs security scripts without damaging the system.
imp/tests/test-self-improvement.py - Tests the self-update mechanisms.
imp/tests/test-bug-hunter.py - Ensures the bug hunting tool runs without errors.
imp/tests/test-mode-advisor.py - Verifies spatiotemporal mode selection logic.
imp/tests/test-message-bus.py - Ensures queued messages send and receive correctly.
imp/tests/test-distributed-queue.py - Checks task assignment across nodes.
imp/tests/test-voice.py - Checks voice synthesis script runs.
imp/tests/test-speech.py - Confirms speech-to-text helper initializes and accepts offline mode.
imp/tests/test-network-auditor.py - Runs the network auditor script.
imp/tests/test-network-monitor.py - Checks for new remote IP detection.
imp/tests/test-windows-support.py - Verifies Windows startup scripts exist.
imp/tests/test-blockchain-ledger.py - Confirms code snapshot ledger integrity.
imp/tests/test-debug-sandbox.py - Verifies the debug sandbox logs evolution summaries.
imp/tests/test-game-copilot.py - Checks learning and dreamscape generation for games.
imp/tests/test-command-transformer.py - Tests the command transformer alias bridge.

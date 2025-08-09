# Building New General Intelligences

The Cimp system allows trusted users to create new general intelligences (GIs) tailored to specific needs.
This guide explains the typical workflow.

## 1. Create a Profile
Run `imp/interaction/imp-gi-builder.py` to create a profile. You will be
prompted for multi‑factor authentication and then for details such as skills,
personality traits, deployment environment, security level, the port the
conversation dashboard should use and any safety guidelines you wish to
enforce. The builder also analyzes recent chat history to suggest a suitable
personality based on conversation tone.
If `ENABLE_GOOGLE_SMS_VERIFICATION` is set to `1` and Twilio credentials are
configured, you must first log in with a Google ID token and confirm the
six-digit code sent via SMS.
You will be shown all available GI modules and can select which ones to embed in
the new intelligence.

Alternatively, `imp/interaction/imp-gi-conversation-builder.py` guides you
through the same questions in a conversational style. It first opens a brief
chat so you can describe what the intelligence should do; type `done` when
finished. The builder analyzes this conversation to capture common keywords,
uses them to suggest skills, focus areas and relevant modules, records your
answers in the chat history and allows you to choose which modules to include
along with the dashboard port.

If you need to run the conversation builder on another computer, use
`imp/interaction/imp-remote-terminal.py` to open an SSH session and launch the
builder remotely. The utility logs each invocation and supports a `--dry-run`
flag to show the generated command before executing it.

Profiles are saved to `imp/config/imp-general-intelligences.json`.

Each profile stores the dashboard port so the resulting intelligence knows which
port to use when sending functionality requests back to Cimp for approval.

## 2. Build the Intelligence
Use `imp/interaction/imp-gi-creator.py` to turn a profile into a configuration
file under `imp/config/gi/`. The creator logs each build to
`imp/logs/imp-gi-build-log.json` and updates the goal tracker.

## 3. Manage Profiles
The profile manager lets you list, remove or update saved profiles. Example:

```bash
python3 imp/interaction/imp-gi-profile-manager.py list
python3 imp/interaction/imp-gi-profile-manager.py update MyGI description "New desc"
python3 imp/interaction/imp-gi-profile-manager.py remove MyGI
```

Multi-factor verification is required for modifications.

## 4. View Chat History
Run `imp/interaction/imp-chat-history-viewer.py` to review recent
conversations or clear the log. This can help refine personality tuning before
building.

## 5. Review Progress
All GI build goals are tracked in `imp/logs/imp-gi-goals.json`. You can run
`imp/core/imp_gi_goal_viewer.py` to print the current status of each goal.

## 6. Ongoing Check-ins and Evolution
Each intelligence can periodically report its status using `imp/interaction/imp-gi-communicator.py`:

```
python3 imp/interaction/imp-gi-communicator.py checkin <alias> "status message"
```

To request codebase updates or other evolution steps, run the communicator with `request-evolution`. You will be prompted for multi-factor verification before the request is logged:

```
python3 imp/interaction/imp-gi-communicator.py request-evolution <alias> "what to change"
```

The communication log is stored in `imp/logs/imp-gi-comm-log.json` for audit purposes.

## 7. Confirm Requests with the Client Dashboard
Run `imp/interaction/imp-gi-client-dashboard.py` after verifying your identity.
It lists pending feature requests and lets the end user decide which ones to forward. Confirmed requests are moved to the communication log for later planning.

## 8. Generate Evolution Plans
Run `imp/interaction/imp-gi-evolution-planner.py` after verifying your identity.
It summarizes evolution requests from each intelligence and writes the result to
`imp/logs/imp-gi-evolution-plans.json`.

## 9. Review Requests with the Operator Dashboard
Run `imp/interaction/imp-gi-operator-dashboard.py` to review pending upgrade requests.
After verification you can approve or deny each one. Approved upgrades snapshot
the current configuration and log the implementation so changes can be rolled
back if needed. Decisions are stored in `imp/logs/imp-gi-upgrade-decisions.json`.

## 10. Monitor Requests with the Web Dashboard
Run `imp/interaction/imp-gi-web-dashboard.py` to open a browser-based dashboard
showing pending functionality requests and basic performance statistics for each
intelligence. You can approve or deny requests from the interface and decisions
are logged to `imp/logs/imp-gi-upgrade-decisions.json`.

## 11. Implement Approved Plans
After reviewing and approving requests, execute `imp/interaction/imp-gi-evolution-implementer.py`.
The implementer prompts for confirmation of each plan and records successful
implementations in `imp/logs/imp-gi-implementation-log.json`.

## 12. Use the Terminal Interface
To access common Cimp features from one place, run `imp/interaction/imp-terminal.py`.
After verification the terminal displays a small color banner. You can then chat with Cimp, build or list GI profiles, view goal status, analyze conversations, manage GI modules, view chat history, explore repository modules or trigger a self-upgrade all from a single menu.

## 13. Use the GI Builder Terminal
`imp/interaction/imp-gi-builder-terminal.py` provides a focused menu for creating new profiles, building configurations and managing GI modules. Run it after verification to streamline the creation process.
## 14. Interact with Built-in Modules
Run `imp/interaction/imp-gi-modules-terminal.py` to manage a GI's memory, tasks,
evolution ideas and more from one menu. The terminal also links to the chatbot.

## 15. Extend Each Intelligence
Several lightweight modules can be embedded into the GIs you create. They
provide persistent memory storage, track assigned tasks and let the intelligence
suggest its own improvements.

* `imp/gi_modules/imp-gi-memory.py` – records notable events for a GI.
* `imp/gi_modules/imp-gi-task-manager.py` – keeps a log of tasks.
* `imp/gi_modules/imp-gi-self-evolver.py` – stores self-evolution suggestions.
* `imp/gi_modules/imp-gi-knowledge.py` – records structured knowledge snippets.
* `imp/gi_modules/imp-gi-skill-tracker.py` – logs new skills or capabilities.
* `imp/gi_modules/imp-gi-performance.py` – records CPU and memory usage.
* `imp/gi_modules/imp-gi-safety.py` – stores safety guidelines and restrictions.
* `imp/gi_modules/imp-gi-risk-analyzer.py` – logs potential risks discussed during chats.
* `imp/gi_modules/imp-gi-planner.py` – keeps a list of action plans for each GI.
* `imp/gi_modules/imp-gi-comm-log.py` – records communication history.
* `imp/gi_modules/imp-gi-implementation-log.py` – tracks implemented features.
* `imp/gi_modules/imp-gi-request.py` – logs feature or functionality requests from a GI.

When you build a new intelligence configuration using `imp-gi-creator.py`, these
modules are automatically listed under the `modules` field so each GI starts
with the ability to remember events, track tasks, evolve itself and store
knowledge without further setup.

Each module appends entries to a log file under `imp/logs/`. You can list or clear
stored entries as needed. Example usage:

```bash
# store a memory
python3 imp/gi_modules/imp-gi-memory.py MyGI "discovered new exploit"
# list memories
python3 imp/gi_modules/imp-gi-memory.py list MyGI
# auto memory entry from conversation
python3 imp/gi_modules/imp-gi-memory.py update MyGI
# clear memories
python3 imp/gi_modules/imp-gi-memory.py clear MyGI

# add a task
python3 imp/gi_modules/imp-gi-task-manager.py MyGI "scan logs"
# list tasks
python3 imp/gi_modules/imp-gi-task-manager.py list MyGI
# auto task from conversation
python3 imp/gi_modules/imp-gi-task-manager.py update MyGI
# clear tasks
python3 imp/gi_modules/imp-gi-task-manager.py clear MyGI

# propose an evolution
python3 imp/gi_modules/imp-gi-self-evolver.py MyGI "improve parser"
# list suggestions
python3 imp/gi_modules/imp-gi-self-evolver.py list MyGI
# auto suggestion from conversation
python3 imp/gi_modules/imp-gi-self-evolver.py update MyGI
# clear suggestions
python3 imp/gi_modules/imp-gi-self-evolver.py clear MyGI

# add a knowledge entry
python3 imp/gi_modules/imp-gi-knowledge.py MyGI networking "use advanced firewall"
# list knowledge
python3 imp/gi_modules/imp-gi-knowledge.py list MyGI
# auto knowledge from conversation
python3 imp/gi_modules/imp-gi-knowledge.py update MyGI
# clear knowledge
python3 imp/gi_modules/imp-gi-knowledge.py clear MyGI

# record a skill
python3 imp/gi_modules/imp-gi-skill-tracker.py MyGI "penetration testing"
# list skills
python3 imp/gi_modules/imp-gi-skill-tracker.py list MyGI
# auto skills from conversation
python3 imp/gi_modules/imp-gi-skill-tracker.py update MyGI
# clear skills
python3 imp/gi_modules/imp-gi-skill-tracker.py clear MyGI

# log a performance entry
python3 imp/gi_modules/imp-gi-performance.py MyGI 50 40
# list performance metrics
python3 imp/gi_modules/imp-gi-performance.py list MyGI
# auto metrics from system log
python3 imp/gi_modules/imp-gi-performance.py update MyGI
# clear metrics
python3 imp/gi_modules/imp-gi-performance.py clear MyGI

# record a safety guideline
python3 imp/gi_modules/imp-gi-safety.py MyGI "avoid network scans"
# list guidelines
python3 imp/gi_modules/imp-gi-safety.py list MyGI
# auto guideline from conversation
python3 imp/gi_modules/imp-gi-safety.py update MyGI
# clear guidelines
python3 imp/gi_modules/imp-gi-safety.py clear MyGI

# log a risk entry
python3 imp/gi_modules/imp-gi-risk-analyzer.py MyGI "exposed port"
# list risks
python3 imp/gi_modules/imp-gi-risk-analyzer.py list MyGI
# auto risk from conversation
python3 imp/gi_modules/imp-gi-risk-analyzer.py update MyGI
# clear risks
python3 imp/gi_modules/imp-gi-risk-analyzer.py clear MyGI

# add a plan step
python3 imp/gi_modules/imp-gi-planner.py MyGI "scan network"
# list plans
python3 imp/gi_modules/imp-gi-planner.py list MyGI
# auto plan from conversation
python3 imp/gi_modules/imp-gi-planner.py update MyGI
# clear plans
python3 imp/gi_modules/imp-gi-planner.py clear MyGI

# record a communication
python3 imp/gi_modules/imp-gi-comm-log.py MyGI "checked in"
# list communications
python3 imp/gi_modules/imp-gi-comm-log.py list MyGI
# auto communication from conversation
python3 imp/gi_modules/imp-gi-comm-log.py update MyGI
# clear communications
python3 imp/gi_modules/imp-gi-comm-log.py clear MyGI

# log an implementation detail
python3 imp/gi_modules/imp-gi-implementation-log.py MyGI "added feature"
# list implementations
python3 imp/gi_modules/imp-gi-implementation-log.py list MyGI
# auto implementation entry from conversation
python3 imp/gi_modules/imp-gi-implementation-log.py update MyGI
# clear implementation entries
python3 imp/gi_modules/imp-gi-implementation-log.py clear MyGI

# log a feature request
python3 imp/gi_modules/imp-gi-request.py MyGI "need graph db"
# list requests
python3 imp/gi_modules/imp-gi-request.py list MyGI
# auto request from conversation
python3 imp/gi_modules/imp-gi-request.py update MyGI
# clear requests
python3 imp/gi_modules/imp-gi-request.py clear MyGI
```

## 16. Explore Repository Modules
To analyze available modules and their functions, run the module explorer:

```bash
python3 imp/self-improvement/imp-module-explorer.py
```

This records the current set of Python modules, listing their functions and
parameters in `imp/logs/imp-module-info.json`. It can help Cimp learn how each
part of the codebase is used.

## 17. Build Through a Conversation Dashboard
Launch `imp/interaction/imp-gi-conversation-dashboard.py` to cooperatively
create and name a GI through a browser-based chat. The script prints the port it
binds to so you can forward it for remote connections. When the form is
submitted, the tool saves a profile, writes a configuration file and
automatically packages the config with its modules for download using
`imp/interaction/imp-gi-packager.py`.

## 18. Analyze Threats and Generate Countermeasures
Use the countermeasure analyzer to review threat logs and record defensive
actions:

```bash
python3 imp/security/imp-ai-countermeasures.py
```

This script performs simple temporal analysis, escalating defenses when the same
threat appears repeatedly within a short time window and logging results to
`imp/logs/imp-ai-countermeasures.json`.

## 19. Run Offline Evolution Analysis
Use the offline evolver to review skill, performance, and conversation insight
logs and suggest new skills without needing an internet connection:

```bash
python3 imp/self-improvement/imp-offline-evolver.py
```

Results include average resource usage and recommended skills and are stored in
`imp/logs/imp-offline-evolution.json` so Cimp can refine itself based on past
activity even while offline.


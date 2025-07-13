# Building New General Intelligences

The IMP system allows trusted users to create new general intelligences (GIs) tailored to specific needs.
This guide explains the typical workflow.

## 1. Create a Profile
Run `imp/interaction/imp-gi-builder.py` to create a profile. You will be prompted
for multi‑factor authentication and then for details such as skills,
personality traits, deployment environment, security level and any safety
guidelines you wish to enforce. The builder also analyzes recent chat history to
suggest a suitable personality based on conversation tone.

Alternatively, `imp/interaction/imp-gi-conversation-builder.py` guides you
through the same questions in a conversational style, recording your answers in
the chat history.

Profiles are saved to `imp/config/imp-general-intelligences.json`.

## 2. Build the Intelligence
Use `imp/interaction/imp-gi-creator.py` to turn a profile into a configuration
file under `imp/config/gi/`. The creator logs each build to
`imp/logs/imp-gi-build-log.json` and updates the goal tracker.

## 3. Review Progress
All GI build goals are tracked in `imp/logs/imp-gi-goals.json`. You can run
`imp/core/imp_gi_goal_viewer.py` to print the current status of each goal.

## 4. Ongoing Check-ins and Evolution
Each intelligence can periodically report its status using `imp/interaction/imp-gi-communicator.py`:

```
python3 imp/interaction/imp-gi-communicator.py checkin <alias> "status message"
```

To request codebase updates or other evolution steps, run the communicator with `request-evolution`. You will be prompted for multi-factor verification before the request is logged:

```
python3 imp/interaction/imp-gi-communicator.py request-evolution <alias> "what to change"
```

The communication log is stored in `imp/logs/imp-gi-comm-log.json` for audit purposes.

## 5. Generate Evolution Plans
Run `imp/interaction/imp-gi-evolution-planner.py` after verifying your identity.
It summarizes evolution requests from each intelligence and writes the result to
`imp/logs/imp-gi-evolution-plans.json`.


# Building New General Intelligences

The IMP system allows trusted users to create new general intelligences (GIs) tailored to specific needs.
This guide explains the typical workflow.

## 1. Create a Profile
Run `imp/interaction/imp-gi-builder.py` to create a profile. You will be prompted
for multi‑factor authentication and then for details such as skills,
personality traits, deployment environment and security level.

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


# AGENTS Instructions

This repository hosts the IMP project. Follow these guidelines when contributing or interacting via automated agents.

## Goals
- Keep the codebase stable and portable. Use relative paths and avoid system-specific dependencies whenever possible.
- Preserve history with additive changes. Do not remove features without a clear reason and a path to recovery.
- Run `bash imp/tests/run-all-tests.sh` before every commit to verify the system works end-to-end.

## Dev Notes
- Logs and persistent files live in the `logs` directory. Default JSON files are provided; tests expect these to exist.
- Scripts in `bin` are entry points for launching and managing the system. They should remain lightweight and avoid hard-coded paths.
- The code updater supports both online and offline modes. Offline mode relies on a local GGUF model stored in `models`.

## Personal Notes
- The `notes` folder contains design ideas, research plans and reflections to guide IMP's evolution. Updates here inform goal planning and future development.
- New personal notes or goals should reference existing notes when relevant to maintain continuity.

By following these guidelines, AI agents and human contributors can coordinate effectively as IMP grows.

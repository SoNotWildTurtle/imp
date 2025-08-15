# IMP Setup Guide

This document explains how to install and start IMP, and traces the
variables, imports and configuration files used during startup.

## Installation
1. Clone the repository. It is expected to live at `/root/imp` because
the start script uses an absolute path.
2. Run `bash imp/bin/imp-install.sh`.
   - Installs Python packages from `requirements.txt` using `pip3`.
   - Launches `imp/bin/imp-start.sh` after installation.
3. If running `pip3` as root, you may see a warning about using a
   virtual environment. Using `python3 -m venv` is recommended for
   production deployments.

## Startup Flow
`imp/bin/imp-start.sh` launches several modules using `nohup`:

```
nohup python3 /root/imp/core/imp-execute.py &
nohup python3 /root/imp/core/imp-learning-memory.py &
nohup python3 /root/imp/core/imp-strategy-generator.py &
nohup python3 /root/imp/self-improvement/imp-code-updater.py &
nohup python3 /root/imp/security/imp-security-optimizer.py &
nohup python3 /root/imp/expansion/imp-cluster-manager.py &
```

### `core/imp-execute.py`
- Resolves the project root and imports modules relative to it.
- Uses `config/imp-config-manager.py` to read configuration files.
- Starts sub‑processes for the mood manager, task executor and message
  bus.

### Configuration Manager
`imp/config/imp-config-manager.py` loads several JSON files:
- `imp-environment.json`: contains `python_interpreter`,
  `working_directory`, `temp_files_path`, and SSL settings.
- `imp-system-settings.json`: holds flags such as `self_healing`.
- `imp-user-registration.json`: tracks operators and default goal
  priority.

All logs are written under `imp/logs`. Default files are provided so
tests can run without additional setup.

## Known Issues & Recommendations
- The start script assumes the repository is located at `/root/imp`. If
  placed elsewhere, update the paths accordingly.
- Several modules attempt to load Hugging Face models. Without network
  access these fall back to simple echo responses, but downloading
  models ahead of time will improve offline capability.
- `imp/core/imp-voice.py` requires an available speech engine such as
  eSpeak; otherwise it falls back to printing text.
- Running on systems without `systemd` will emit warnings when security
  modules query system services.

This guide should help new operators verify the installation and better
understand the startup sequence of IMP.

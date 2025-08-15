# Startup Verification

This document tracks launch checks for Cimp. Run `python imp/startup/imp_startup_verifier.py`
to verify each step and log results to `imp/logs/imp-startup-verification.json`.

## Current Status

1. **Dependencies**
   - [x] pyotp
   - [x] google-auth
2. **Configuration files**
   - [x] imp/config/imp-personality.json
   - [x] imp/config/imp-general-intelligences.json
3. **Manager modules**
   - [x] config_manager
   - [ ] goal_manager (missing optional `transformers` package)
   - [x] log_manager
4. **Security modules**
   - [x] heavy identity verifier
   - [x] google identity verifier
5. **Interaction**
   - [x] terminal interface

Each check appends an entry with its status and timestamp to the startup verification log.

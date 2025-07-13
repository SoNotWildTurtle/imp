# General Intelligence Builder Goals

To create new general intelligences tailored to user requests, IMP must accomplish several tasks:

- [x] Implement a creator utility that generates configuration files from saved GI profiles.
- [x] Store generated configurations under `imp/config/gi/` for easy management.
- [x] Track build activity in `imp/logs/imp-gi-build-log.json`.
- [x] Provide tests verifying that a new configuration file is produced and logged.
- [ ] Integrate the GI build workflow with the existing goal manager so progress can be monitored.
- [x] Require multi-factor verification before profiles are created or built.
- [x] Lock users out after repeated failed authentication attempts.
- [ ] Expand documentation to explain how users can request and build new intelligences.
- [x] Ensure each intelligence config supports ongoing self-evolution.
- [x] Offer environment and security level options when creating intelligence profiles.
- [x] Enable conversation-driven creation of intelligence profiles so users can build
    them interactively during chat sessions.
- [x] Analyze chat tone to adjust personality of created intelligences.

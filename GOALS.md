# General Intelligence Builder Goals

To create new general intelligences tailored to user requests, IMP must accomplish several tasks:

- Implement a creator utility that generates configuration files from saved GI profiles.
- Store generated configurations under `imp/config/gi/` for easy management.
- Track build activity in `imp/logs/imp-gi-build-log.json`.
- Provide tests verifying that a new configuration file is produced and logged.
- Integrate the GI build workflow with the existing goal manager so progress can be monitored.
- Expand documentation to explain how users can request and build new intelligences.

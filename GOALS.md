# General Intelligence Builder Goals

To create new general intelligences tailored to user requests, Cimp must accomplish several tasks:

- [x] Implement a creator utility that generates configuration files from saved GI profiles.
- [x] Store generated configurations under `imp/config/gi/` for easy management.
- [x] Track build activity in `imp/logs/imp-gi-build-log.json`.
- [x] Provide tests verifying that a new configuration file is produced and logged.
- [x] Integrate the GI build workflow with the existing goal manager so progress can be monitored.
- [x] Require multi-factor verification before profiles are created or built.
- [x] Lock users out after repeated failed authentication attempts.
- [x] Support Google login with SMS-based two-factor authentication.
- [x] Expand documentation to explain how users can request and build new intelligences.
- [x] Ensure each intelligence config supports ongoing self-evolution.
- [x] Offer environment and security level options when creating intelligence profiles.
- [x] Enable conversation-driven creation of intelligence profiles so users can build
    them interactively during chat sessions.
- [x] Analyze chat tone to adjust personality of created intelligences.
- [x] Ask for safety guidelines when building profiles.
- [x] Record perception-based personality suggestions in each profile.
- [x] Provide a profile manager utility to list and remove intelligence profiles.
- [x] Prevent duplicate intelligence names during profile creation.
- [x] Allow general intelligences to check in using safe aliases.
- [x] Require verification before approving evolution requests from created intelligences.
- [x] Generate evolution plans for each intelligence based on communication logs.
- [x] Implement approved evolution plans and record the results.

- [x] Add conversation analysis and self-upgrade options to the terminal interface.
- [x] Provide reusable modules for GI memory, task tracking and self-evolution.
- [x] Allow clearing entries in all GI modules for easier management.
- [x] Implement a heavy identity verifier using OTP codes and a passphrase, with
      automatic lockouts after too many failures.
- [x] Offer an operator dashboard to approve or deny GI upgrade requests.
- [x] Snapshot GI configurations and log implementations when approving upgrades.
- [x] Provide a chat history viewer to inspect and clear logged conversations.
- [x] Implement a knowledge base module so intelligences can store structured information.
- [x] Document knowledge management utilities in the building guide.
- [x] Add tests verifying the knowledge base module.
- [x] Provide a skill tracker module for recording GI skills.
- [x] Add a performance tracker module for monitoring GI resource usage.
- [x] Provide a safety guidelines module for recording restrictions or best practices.
- [x] Provide a risk analyzer module for logging potential threats.
- [x] Provide a planning module so intelligences can outline work plans.
- [x] Provide a communication log module for tracking GI check-ins.
- [x] Provide an implementation log module for recording completed plans.
- [x] Adapt GI modules using conversation insights to prefill memory, tasks,
      evolution ideas and knowledge.
- [x] Record built-in modules in each generated GI configuration so new
      intelligences have standalone capabilities.
- [x] Allow selecting which GI modules to include when creating profiles.
- [x] Provide a module explorer that logs available modules and their
      functions for training purposes.
- [x] Offer a menu-driven interface to interact with all GI modules from one
      place.
- [x] Integrate chat history, module management and self-upgrade features into
      the main terminal interface for full functionality.
- [x] Provide a dedicated GI builder terminal to streamline profile and config creation.
- [x] Provide a feature request module so intelligences can log new functionality needs.
- [x] Offer a web dashboard to review GI stats and approve or deny feature requests.
- [x] Provide a client dashboard so end users can confirm upgrade requests before operator review.
- [x] Skip web dashboard tests when Flask is not installed to keep the suite portable.
- [x] Offer a conversation dashboard so end users can cooperatively name and create their GI through a browser interface.
- [x] Package GI configurations with their modules for easy distribution.
- [x] Record and display the dashboard port so intelligences and end users know
      where to confirm functionality requests with Cimp.
- [x] Improve UX by adding descriptive instructions to the operator terminal and
      client dashboard.
- [x] Analyze hostile AI activity over time and log automatic countermeasures.
- [x] Provide an offline evolver that summarizes skills and performance logs for
      self-improvement without network access.
- [x] Extend the offline evolver to include conversation insights and recommend
      new skills along with average resource usage.
- [x] Provide an SSH-based remote terminal utility to launch the GI conversation
      builder on another machine and log its usage.
- [x] Hold a free-form conversation with the user before collecting profile
      details so requirements are captured from the chat.
- [x] Suggest GI modules from conversation keywords and prefill skills and focus areas.
- [x] Enhance the main terminal with a color banner for a friendlier interface.

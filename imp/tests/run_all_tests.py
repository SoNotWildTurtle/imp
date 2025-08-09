import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

tests = [
    'test-core-functions.py',
    'test-security.py',
    'test-ai-countermeasures.py',
    'test-performance.py',
    'test-expansion.py',
    'test-self-improvement.py',
    'test-code-quality.py',
    'test-module-explorer.py',
    'test-offline-evolver.py',
    'test-metacognition.py',
    'test-conversation-analyzer.py',
    'test-perception-analyzer.py',
    'test-chat-history-viewer.py',
    'test-interaction.py',
    'test-terminal-interface.py',
    'test-gi-builder.py',
    'test-gi-conversation-builder.py',
    'test-gi-creator.py',
    'test-gi-goal-viewer.py',
    'test-gi-profile-manager.py',
    'test-gi-communicator.py',
    'test-gi-evolution-planner.py',
    'test-gi-evolution-implementer.py',
    'test-gi-operator-dashboard.py',
    'test-gi-client-dashboard.py',
    'test-gi-conversation-dashboard.py',
    'test-gi-packager.py',
    'test-gi-memory.py',
    'test-gi-task-manager.py',
    'test-gi-self-evolver.py',
    'test-gi-experience.py',
    'test-gi-knowledge.py',
    'test-gi-skill-tracker.py',
    'test-gi-performance.py',
    'test-gi-safety.py',
    'test-gi-risk-analyzer.py',
    'test-gi-comm-log.py',
    'test-gi-implementation-log.py',
    'test-gi-snapshot.py',
    'test-gi-request.py',
    'test-gi-planner.py',
    'test-gi-modules-terminal.py',
    'test-gi-builder-terminal.py',
    'test-config.py',
    'test-logs.py',
    'test-gi-web-dashboard.py',
    'test-remote-terminal.py',
]

print("🚀 Running Full Cimp System Test Suite...")
for test in tests:
    subprocess.run([sys.executable, str(SCRIPT_DIR / test)], check=True)
print("✅ All Tests Completed!")

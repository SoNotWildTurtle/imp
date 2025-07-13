from multiprocessing import Process
from pathlib import Path

from imp.core import (
    imp_execute,
    imp_learning_memory,
    imp_strategy_generator,
)
from imp.self_improvement import imp_code_updater
from imp.security import imp_security_optimizer
from imp.expansion import imp_cluster_manager

ROOT = Path(__file__).resolve().parents[1]
PID_FILE = ROOT / 'logs' / 'imp-pids.json'

def main():
    processes = [
        Process(target=imp_execute.main),
        Process(target=imp_learning_memory.store_learnings),
        Process(target=imp_strategy_generator.generate_new_strategy),
        Process(target=imp_code_updater.main),
        Process(target=imp_security_optimizer.run_security_checks),
        Process(target=imp_cluster_manager.distribute_workload),
    ]

    for p in processes:
        p.daemon = True
        p.start()

    with open(PID_FILE, 'w') as f:
        import json
        json.dump([p.pid for p in processes], f)

    print('IMP AI is now running.')

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()


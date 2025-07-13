from pathlib import Path
from multiprocessing import Process

from imp.core import imp_learning_memory, imp_strategy_generator
from imp.self_improvement import imp_code_updater
from imp.security import imp_security_optimizer
from imp.expansion import imp_cluster_manager

# 2025-06-08: Execution harness should remain additive and retain prior
# processes. Consider a reflective recursive enumeration blockchain for
# self-healing and memory preservation.

ROOT = Path(__file__).resolve().parents[1]

def main():
    print("IMP AI is initializing...")

    processes = [
        Process(target=imp_learning_memory.store_learnings),
        Process(target=imp_strategy_generator.generate_new_strategy),
        Process(target=imp_code_updater.main),
        Process(target=imp_security_optimizer.run_security_checks),
        Process(target=imp_cluster_manager.distribute_workload),
    ]

    for p in processes:
        p.daemon = True
        p.start()

    print("IMP is now running autonomously.")

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()

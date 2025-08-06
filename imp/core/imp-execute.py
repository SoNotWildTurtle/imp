from pathlib import Path
from multiprocessing import Process
import importlib.util
import sys

# Load submodules dynamically so file names with dashes work as imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

imp_learning_memory = _load("imp_learning_memory", ROOT / "core" / "imp-learning-memory.py")
imp_strategy_generator = _load("imp_strategy_generator", ROOT / "core" / "imp-strategy-generator.py")
imp_code_updater = _load("imp_code_updater", ROOT / "self-improvement" / "imp-code-updater.py")
imp_security_optimizer = _load("imp_security_optimizer", ROOT / "security" / "imp-security-optimizer.py")
imp_cluster_manager = _load("imp_cluster_manager", ROOT / "expansion" / "imp-cluster-manager.py")
# 2025-06-08: Execution harness should remain additive and retain prior
# processes. Consider a reflective recursive enumeration blockchain for
# self-healing and memory preservation.

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

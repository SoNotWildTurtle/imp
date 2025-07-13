from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "self-improvement" / "imp-metacognitive-analysis.py"

spec = importlib.util.spec_from_file_location("imp_metacognition", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_metacognition():
    print("Testing Metacognitive Analysis...")
    net = module.SimpleNeuralNetwork(3, 2, 1)
    module.perform_metacognitive_analysis(net)
    module.update_neural_network(net, [0.1, 0.2, -0.3], [0.5])
    module.self_evolve_neural_network(net, [([0.1, 0.2, -0.3], [0.5])])
    assert module.METACOGNITIVE_LOG.exists()
    print("Metacognitive Test Passed!")


if __name__ == "__main__":
    test_metacognition()

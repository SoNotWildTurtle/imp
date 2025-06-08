from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-neural-network.py"

spec = importlib.util.spec_from_file_location("imp_neural_network", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_forward():
    print("🔍 Testing Base Neural Network...")
    net = module.SimpleNeuralNetwork(3, 2, 1)
    out = net.forward([0.5, -0.2, 0.1])
    assert len(out) == 1
    print("✅ Neural Network Test Passed!")

if __name__ == "__main__":
    test_forward()

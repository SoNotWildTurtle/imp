from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-3d-neural-network.py"

spec = importlib.util.spec_from_file_location("imp_3d_neural_network", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_basic_3d_network():
    print("🔍 Testing 3D Neural Network...")
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0), threshold=0.1)
    net.connect(a, b, myelin=2.0)
    out = net.forward([(a, 1.0)])
    assert len(out) == 2 and out[1] > 0
    print("✅ 3D Neural Network Test Passed!")


if __name__ == "__main__":
    test_basic_3d_network()

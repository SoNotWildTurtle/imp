from pathlib import Path
import importlib.util
import random

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-neural-network.py"

spec = importlib.util.spec_from_file_location("imp_neural_network", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_forward():
    print("Testing Base Neural Network...")
    net = module.SimpleNeuralNetwork(3, 2, 1)
    out = net.forward([0.5, -0.2, 0.1])
    assert len(out) == 1
    print("Neural Network Test Passed!")

def test_save_load():
    print("Testing Neural Network Save/Load...")
    net = module.SimpleNeuralNetwork(2, 2, 1)
    tmp = ROOT / "nn_tmp.json"
    net.save(tmp)
    loaded = module.SimpleNeuralNetwork.load(tmp)
    out1 = net.forward([0.1, 0.2])
    out2 = loaded.forward([0.1, 0.2])
    assert out1 == out2
    tmp.unlink()
    print("Save/Load Test Passed!")

def test_training():
    print("Testing Neural Network Training...")
    random.seed(0)
    net = module.SimpleNeuralNetwork(2, 2, 1)
    data = [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [1])]
    before = net.forward([1, 0])[0]
    for _ in range(50):
        net.train(data, epochs=1)
    after = net.forward([1, 0])[0]
    assert abs(after - 1) < abs(before - 1)
    print("Training Test Passed!")

if __name__ == "__main__":
    test_forward()
    test_save_load()
    test_training()

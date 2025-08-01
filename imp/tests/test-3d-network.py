from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-3d-neural-network.py"

spec = importlib.util.spec_from_file_location("imp_3d_neural_network", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_basic_3d_network():
    print("Testing 3D Neural Network...")
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.spawn_advanced_neuron((1, 0, 0), threshold=0.1, neuron_type="schwann")
    net.connect(a, b, myelin=2.0)
    out = net.forward([(a, 1.0)])
    assert len(out) == 2 and out[1] > 0
    assert net.neuron_usage(b) > 0
    print("3D Neural Network Test Passed!")


def test_novel_neuron():
    net = module.ThreeDNeuralNetwork()
    idx = net.spawn_novel_neuron((0, 0, 0))
    assert net.neurons[idx].neuron_type.startswith("novel_")
    print("Novel Neuron Test Passed!")


def test_guide_novel_neuron():
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    net.connect(a, b, myelin=1.0)
    net.forward([(a, 1.0)])
    idx = net.spawn_novel_neuron((0, 1, 0))
    net.guide_novel_neuron(idx)
    assert any(c.dest == idx for c in net.connections)
    print("Guide Novel Neuron Test Passed!")


def test_task_paths():
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.spawn_advanced_neuron((1, 0, 0))
    c = net.spawn_advanced_neuron((0, 1, 0))
    net.connect_for_task(a, b, task="task1", myelin=2.0)
    net.connect_for_task(a, b, task="task2", myelin=1.0)
    net.connect_for_task(b, c, task="task2", myelin=1.5)
    r1 = net.forward([(a, 1.0)], task="task1")
    r2 = net.forward([(a, 1.0)], task="task2")
    assert r1[b] > 0 and r1[c] == 0
    assert r2[c] > 0
    print("Task Path Test Passed!")


def test_angle_routing():
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    c = net.add_neuron((0, 1, 0))
    net.connect_for_task(a, b, task="default", myelin=1.0)
    net.connect_for_task(a, c, task="default", myelin=1.0)
    r1 = net.forward_by_angle([(a, 1.0)], (1, 0, 0), task="default", tolerance=0.2)
    r2 = net.forward_by_angle([(a, 1.0)], (0, 1, 0), task="default", tolerance=0.2)
    assert r1[b] > 0 and r1[c] == 0
    assert r2[c] > 0 and r2[b] == 0
    print("Angle Routing Test Passed!")


def test_evolve():
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    c = net.add_neuron((0, 1, 0))
    net.connect(a, b, myelin=1.0)
    net.forward([(a, 1.0)])
    net.evolve(usage_threshold=1)
    # neuron c should remain but be marked dormant
    assert any(n.idx == c and n.dormant for n in net.neurons)
    # a novel neuron is added
    assert len(net.neurons) == 4
    print("Evolve Test Passed!")


def test_auto_evolve():
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    net.connect(a, b, myelin=1.0)
    for _ in range(3):
        net.forward([(a, 1.0)])
    myelin_before = [c.myelin for c in net.connections][0]
    net.auto_evolve(usage_threshold=1)
    myelin_after = [c.myelin for c in net.connections][0]
    assert myelin_after > myelin_before
    assert len(net.neurons) == 3  # added novel neuron
    print("Auto Evolve Test Passed!")


if __name__ == "__main__":
    test_basic_3d_network()
    test_novel_neuron()
    test_guide_novel_neuron()
    test_task_paths()
    test_angle_routing()
    test_evolve()
    test_auto_evolve()

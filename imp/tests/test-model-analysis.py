from pathlib import Path
import importlib.util
import copy

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "self-improvement" / "imp-model-analyzer.py"
spec = importlib.util.spec_from_file_location("imp_model_analyzer", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

NN3D_PATH = ROOT / "core" / "imp-3d-neural-network.py"
spec3d = importlib.util.spec_from_file_location("imp_3d_network", NN3D_PATH)
module3d = importlib.util.module_from_spec(spec3d)
spec3d.loader.exec_module(module3d)


def test_compare_models():
    print("Testing Model Comparison...")
    net1 = module.SimpleNeuralNetwork(2, 2, 1)
    net2 = module.SimpleNeuralNetwork(2, 3, 1)
    tmp1 = ROOT / "tmp_model1.json"
    tmp2 = ROOT / "tmp_model2.json"
    net1.save(tmp1)
    net2.save(tmp2)
    diff = module.compare_model_files(tmp1, tmp2)
    assert diff["hidden_size_diff"] != 0
    tmp1.unlink()
    tmp2.unlink()
    assert module.ANALYSIS_LOG.exists()
    print("Model Analysis Test Passed!")


def test_compare_3d_networks():
    net = module3d.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    net.connect(a, b)
    tmp_a = ROOT / "net_a.json"
    tmp_b = ROOT / "net_b.json"
    net.save(tmp_a)
    net2 = copy.deepcopy(net)
    net2.spawn_novel_neuron((0, 1, 0))
    net2.save(tmp_b)
    diff = module.compare_3d_network_files(tmp_a, tmp_b)
    assert diff["neuron_count_diff"] == 1
    tmp_a.unlink()
    tmp_b.unlink()
    print("3D Network Diff Test Passed!")


test_compare_models()
test_compare_3d_networks()

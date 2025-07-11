from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "self-improvement" / "imp-model-analyzer.py"
spec = importlib.util.spec_from_file_location("imp_model_analyzer", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


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


test_compare_models()

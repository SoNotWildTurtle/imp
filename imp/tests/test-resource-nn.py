from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
NN_PATH = ROOT / "core" / "imp-resource-nn.py"
ENGINE_PATH = ROOT / "core" / "imp-resource-engine.py"

spec_nn = importlib.util.spec_from_file_location("imp_resource_nn", NN_PATH)
nn_module = importlib.util.module_from_spec(spec_nn)
spec_nn.loader.exec_module(nn_module)

spec_engine = importlib.util.spec_from_file_location("imp_resource_engine", ENGINE_PATH)
engine_module = importlib.util.module_from_spec(spec_engine)
spec_engine.loader.exec_module(engine_module)


def test_ogliodendrocyte_spawn():
    nn = nn_module.ResourceNN()
    before = len(nn.neuron_types)
    nn.spawn_ogliodendrocyte(0, 2)
    assert len(nn.neuron_types) == before + 1
    assert "ogliodendrocyte" in nn.neuron_types.values()


def test_predict_with_pins():
    nn = nn_module.ResourceNN()
    score = nn.predict(10, 10, 5, 2)
    assert isinstance(score, float)


def test_pin_and_release_memory():
    block = engine_module.pin_memory(ram_mb=1)
    assert "ram" in block
    engine_module.release_pins()


def test_manage_resources():
    engine_module.pin_memory(ram_mb=1)
    record = engine_module.manage_resources()
    engine_module.release_pins()
    assert {"cpu", "mem", "pinned_ram", "pinned_vram", "score"} <= record.keys()

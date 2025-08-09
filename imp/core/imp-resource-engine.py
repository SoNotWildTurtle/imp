"""Resource engine monitors system load and evolves the ResourceNN for safe,
long-term operation."""

import json
import os
try:
    import psutil
except Exception:  # pragma: no cover - psutil may be absent
    psutil = None
try:
    import torch
except Exception:  # pragma: no cover - torch may be absent
    torch = None
import importlib.util
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent
MANAGER_PATH = CORE_DIR / "imp_neural_manager.py"
spec_mgr = importlib.util.spec_from_file_location("imp_neural_manager", MANAGER_PATH)
mgr_module = importlib.util.module_from_spec(spec_mgr)
spec_mgr.loader.exec_module(mgr_module)
neural_manager = mgr_module.manager

NN_PATH = CORE_DIR / "imp-resource-nn.py"
spec = importlib.util.spec_from_file_location("imp_resource_nn", NN_PATH)
nn_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nn_module)
ResourceNN = nn_module.ResourceNN

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "imp-resource-log.json")

PINNED = []


def pin_memory(ram_mb=0, vram_mb=0):
    """Reserve RAM and optional VRAM by allocating blocks."""
    block = {}
    if ram_mb > 0:
        block["ram"] = bytearray(int(ram_mb * 1024 * 1024))
    if vram_mb > 0 and torch and getattr(torch, "cuda", None) and torch.cuda.is_available():
        # allocate simple tensor on GPU
        size = int(vram_mb * 256)
        block["vram"] = torch.empty((size, 1024), device="cuda")
    PINNED.append(block)
    return block


def release_pins():
    """Release all pinned memory."""
    PINNED.clear()


def _pinned_usage():
    ram = sum(len(b.get("ram", b"")) for b in PINNED) / (1024 * 1024)
    vram = 0.0
    for b in PINNED:
        tensor = b.get("vram")
        if tensor is not None:
            vram += tensor.numel() * tensor.element_size() / (1024 * 1024)
    return ram, vram


def manage_resources():
    nn = neural_manager.get("resource")
    if nn is None:
        nn = ResourceNN()
        neural_manager.register("resource", nn)
    if psutil:
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
    else:
        cpu = mem = 0.0
    pin_ram, pin_vram = _pinned_usage()
    nn.evolve(cpu, mem, pin_ram, pin_vram)
    score = nn.predict(cpu, mem, pin_ram, pin_vram)
    record = {
        "cpu": cpu,
        "mem": mem,
        "pinned_ram": pin_ram,
        "pinned_vram": pin_vram,
        "score": score,
    }
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as fh:
            json.dump([], fh)
    with open(LOG_PATH) as fh:
        data = json.load(fh)
    data.append(record)
    with open(LOG_PATH, "w") as fh:
        json.dump(data, fh)
    return record


if __name__ == "__main__":
    manage_resources()

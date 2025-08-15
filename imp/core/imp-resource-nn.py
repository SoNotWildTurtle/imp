"""ResourceNN manages processing resources with self-evolving oligodendrocyte
connections. It models CPU and memory usage and can spawn special neurons that
reduce path resistance for long-term stability."""

import os

class ResourceNN:
    """Simple neural net tracking CPU/memory paths."""
    def __init__(self):
        # neuron id: type
        self.neuron_types = {
            0: "cpu",
            1: "mem",
            2: "output",
            3: "pinned_ram",
            4: "pinned_vram",
        }
        self.next_id = 5
        # connections (src,dst) -> {weight,resistance,type}
        self.connections = {
            (0, 2): {"weight": 0.5, "resistance": 1.0, "type": "standard"},
            (1, 2): {"weight": 0.5, "resistance": 1.0, "type": "standard"},
            (3, 2): {"weight": 0.5, "resistance": 1.0, "type": "standard"},
            (4, 2): {"weight": 0.5, "resistance": 1.0, "type": "standard"},
        }

    def predict(self, cpu, mem, pinned_ram=0.0, pinned_vram=0.0):
        """Return a simple resource score."""
        c0 = self.connections[(0, 2)]
        c1 = self.connections[(1, 2)]
        c2 = self.connections[(3, 2)]
        c3 = self.connections[(4, 2)]
        return (
            cpu * c0["weight"] / c0["resistance"]
            + mem * c1["weight"] / c1["resistance"]
            + pinned_ram * c2["weight"] / c2["resistance"]
            + pinned_vram * c3["weight"] / c3["resistance"]
        )

    def spawn_ogliodendrocyte(self, src, dst):
        """Add an oligodendrocyte neuron that lowers resistance."""
        nid = self.next_id
        self.neuron_types[nid] = "ogliodendrocyte"
        self.next_id += 1
        # link src -> oglio -> dst
        self.connections[(src, nid)] = {
            "weight": 1.0,
            "resistance": 1.0,
            "type": "standard",
        }
        self.connections[(nid, dst)] = {
            "weight": 1.0,
            "resistance": 0.5,
            "type": "ogliodendrocyte",
        }
        return nid

    def evolve(self, cpu, mem, pinned_ram=0.0, pinned_vram=0.0, threshold=150):
        """If combined usage exceeds threshold, reinforce the pathway."""
        if cpu + mem + pinned_ram + pinned_vram > threshold:
            self.spawn_ogliodendrocyte(0, 2)

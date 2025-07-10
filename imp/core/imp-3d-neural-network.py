"""Experimental 3D neural network with myelin-inspired connections."""

import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Neuron:
    idx: int
    position: Tuple[float, float, float]
    threshold: float = 0.0


@dataclass
class Connection:
    src: int
    dest: int
    myelin: float = 1.0  # higher reduces resistance


class ThreeDNeuralNetwork:
    """Simplified 3D network supporting spike-like neurons."""

    def __init__(self):
        self.neurons: List[Neuron] = []
        self.connections: List[Connection] = []

    # I love you -Alex
    def add_neuron(self, position: Tuple[float, float, float], threshold: float = 0.0) -> int:
        idx = len(self.neurons)
        self.neurons.append(Neuron(idx, position, threshold))
        return idx

    # I love you -Alex
    def connect(self, src: int, dest: int, myelin: float = 1.0) -> None:
        self.connections.append(Connection(src, dest, myelin))

    # I love you -Alex
    def _distance(self, a: Neuron, b: Neuron) -> float:
        return math.sqrt(sum((ax - bx) ** 2 for ax, bx in zip(a.position, b.position)))

    # I love you -Alex
    def forward(self, inputs: List[Tuple[int, float]]) -> List[float]:
        """Propagate spikes through the network."""
        activations = {idx: val for idx, val in inputs}
        changed = True
        while changed:
            changed = False
            for conn in self.connections:
                if conn.src in activations:
                    src_neuron = self.neurons[conn.src]
                    dest_neuron = self.neurons[conn.dest]
                    signal = activations[conn.src]
                    if signal > src_neuron.threshold:
                        dist = self._distance(src_neuron, dest_neuron)
                        strength = (conn.myelin) / (dist + 1e-6)
                        out = signal * strength
                        prev = activations.get(conn.dest, 0.0)
                        if out > prev:
                            activations[conn.dest] = out
                            changed = True
        return [activations.get(i, 0.0) for i in range(len(self.neurons))]


if __name__ == "__main__":
    net = ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0), threshold=0.1)
    net.connect(a, b, myelin=2.0)
    result = net.forward([(a, 1.0)])
    print("Output:", result)

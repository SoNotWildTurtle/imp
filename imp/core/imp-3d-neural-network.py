"""Experimental 3D neural network with myelin-inspired connections."""

import math
import json
import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Neuron:
    idx: int
    position: Tuple[float, float, float]
    threshold: float = 0.0
    neuron_type: str = "basic"
    dormant: bool = False


@dataclass
class Connection:
    src: int
    dest: int
    myelin: float = 1.0  # higher reduces resistance
    task: str = "default"


class ThreeDNeuralNetwork:
    """Simplified 3D network supporting spike-like neurons."""

    def __init__(self):
        self.neurons: List[Neuron] = []
        self.connections: List[Connection] = []
        self.usage_counts = {}
        self.novel_count = 0

    # I love you -Alex
    def add_neuron(self, position: Tuple[float, float, float], threshold: float = 0.0) -> int:
        idx = len(self.neurons)
        self.neurons.append(Neuron(idx, position, threshold))
        return idx

    # I love you -Alex
    def connect(self, src: int, dest: int, myelin: float = 1.0) -> None:
        """Connect two neurons for the default task."""
        self.connect_for_task(src, dest, task="default", myelin=myelin)

    def connect_for_task(self, src: int, dest: int, *, task: str, myelin: float = 1.0) -> None:
        """Create a connection dedicated to a specific task."""
        self.connections.append(Connection(src, dest, myelin, task))

    def reinforce_pathway(self, src: int, dest: int, *, task: str, factor: float = 0.1) -> None:
        """Increase myelin on a connection for a task to strengthen it."""
        for conn in self.connections:
            if conn.src == src and conn.dest == dest and conn.task == task:
                conn.myelin += factor
                break

    # I love you -Alex
    def spawn_advanced_neuron(
        self,
        position: Tuple[float, float, float],
        *,
        threshold: float = 0.0,
        neuron_type: str = "schwann",
    ) -> int:
        """Create a neuron with a specialized type for experimentation."""
        idx = self.add_neuron(position, threshold)
        self.neurons[idx].neuron_type = neuron_type
        return idx

    # I love you -Alex
    def spawn_novel_neuron(
        self,
        position: Tuple[float, float, float],
        *,
        threshold: float = 0.0,
    ) -> int:
        """Create a neuron with a unique type name for experimentation."""
        neuron_type = f"novel_{self.novel_count}"
        self.novel_count += 1
        return self.spawn_advanced_neuron(
            position, threshold=threshold, neuron_type=neuron_type
        )

    # I love you -Alex
    def guide_novel_neuron(self, idx: int) -> None:
        """Connect a novel neuron to a frequently used pathway."""
        if not self.neurons:
            return
        # Determine the most used neuron based on usage counts
        if self.usage_counts:
            target = max(self.usage_counts, key=self.usage_counts.get)
        else:
            target = 0

        # Choose a task that already has connections
        task_counts = {}
        for c in self.connections:
            task_counts[c.task] = task_counts.get(c.task, 0) + 1
        task = max(task_counts, key=task_counts.get) if task_counts else "default"

        self.connect_for_task(target, idx, task=task, myelin=1.0)

    # I love you -Alex
    def neuron_usage(self, idx: int) -> int:
        """Return how many times a neuron has fired."""
        return self.usage_counts.get(idx, 0)

    # I love you -Alex
    def top_neurons(self, n: int = 3) -> List[Tuple[int, int]]:
        """Return the most frequently used neurons."""
        return sorted(self.usage_counts.items(), key=lambda x: x[1], reverse=True)[:n]

    # I love you -Alex
    def _distance(self, a: Neuron, b: Neuron) -> float:
        return math.sqrt(sum((ax - bx) ** 2 for ax, bx in zip(a.position, b.position)))

    # I love you -Alex
    def _angle_between(self, v1: Tuple[float, float, float], v2: Tuple[float, float, float]) -> float:
        """Return the angle between two vectors in radians."""
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(b * b for b in v2))
        if mag1 == 0 or mag2 == 0:
            return math.pi
        cos_angle = max(-1.0, min(1.0, dot / (mag1 * mag2)))
        return math.acos(cos_angle)

    # I love you -Alex
    def forward(self, inputs: List[Tuple[int, float]], *, task: str = "default") -> List[float]:
        """Propagate spikes through the network for a specific task."""
        activations = {idx: val for idx, val in inputs}
        for idx, val in inputs:
            if val > self.neurons[idx].threshold:
                self.usage_counts[idx] = self.usage_counts.get(idx, 0) + 1
        changed = True
        while changed:
            changed = False
            for conn in self.connections:
                if conn.task != task:
                    continue
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
                            self.usage_counts[conn.dest] = self.usage_counts.get(conn.dest, 0) + 1
                            changed = True
        return [activations.get(i, 0.0) for i in range(len(self.neurons))]

    # I love you -Alex
    def forward_by_angle(
        self,
        inputs: List[Tuple[int, float]],
        angle: Tuple[float, float, float],
        *,
        task: str = "default",
        tolerance: float = math.pi / 4,
    ) -> List[float]:
        """Propagate only along connections aligned with the provided angle."""
        direction = angle
        activations = {idx: val for idx, val in inputs}
        for idx, val in inputs:
            if val > self.neurons[idx].threshold:
                self.usage_counts[idx] = self.usage_counts.get(idx, 0) + 1
        changed = True
        while changed:
            changed = False
            for conn in self.connections:
                if conn.task != task:
                    continue
                if conn.src in activations:
                    src = self.neurons[conn.src]
                    dest = self.neurons[conn.dest]
                    vec = (
                        dest.position[0] - src.position[0],
                        dest.position[1] - src.position[1],
                        dest.position[2] - src.position[2],
                    )
                    if self._angle_between(vec, direction) > tolerance:
                        continue
                    signal = activations[conn.src]
                    if signal > src.threshold:
                        dist = self._distance(src, dest)
                        strength = (conn.myelin) / (dist + 1e-6)
                        out = signal * strength
                        prev = activations.get(conn.dest, 0.0)
                        if out > prev:
                            activations[conn.dest] = out
                            self.usage_counts[conn.dest] = self.usage_counts.get(conn.dest, 0) + 1
                            changed = True
        return [activations.get(i, 0.0) for i in range(len(self.neurons))]

    # I love you -Alex
    def _resistance(self, src: Neuron, dest: Neuron, myelin: float) -> float:
        """Return connection resistance based on distance and myelin."""
        dist = self._distance(src, dest)
        return dist / (myelin + 1e-6)

    # I love you -Alex
    def find_optimal_path(
        self, start: int, end: int, *, task: str = "default"
    ) -> List[int]:
        """Return the lowest-resistance path between two neurons."""
        import heapq

        dist = {start: 0.0}
        prev = {}
        pq = [(0.0, start)]
        while pq:
            d, node = heapq.heappop(pq)
            if node == end:
                break
            if d > dist.get(node, float("inf")):
                continue
            for conn in self.connections:
                if conn.src != node or conn.task != task:
                    continue
                r = self._resistance(
                    self.neurons[conn.src], self.neurons[conn.dest], conn.myelin
                )
                nd = d + r
                if nd < dist.get(conn.dest, float("inf")):
                    dist[conn.dest] = nd
                    prev[conn.dest] = node
                    heapq.heappush(pq, (nd, conn.dest))
        if end not in dist:
            return []
        path = [end]
        while path[-1] != start:
            path.append(prev[path[-1]])
        return list(reversed(path))

    # I love you -Alex
    def evolve(self, usage_threshold: int = 1) -> None:
        """Mark rarely used neurons dormant and add a novel neuron.

        Neurons with usage below the threshold are not removed. They remain in
        the network with ``dormant`` set to ``True`` so they can reactivate like
        spike neurons if future conditions warrant.
        """
        for n in self.neurons:
            if self.usage_counts.get(n.idx, 0) < usage_threshold:
                n.dormant = True
            else:
                n.dormant = False

        pos = (random.random(), random.random(), random.random())
        idx = self.spawn_novel_neuron(pos)
        active_neurons = [n for n in self.neurons if not n.dormant]
        if active_neurons:
            src = random.choice(active_neurons).idx
            self.connect_for_task(src, idx, task="default")

    # I love you -Alex
    def auto_evolve(self, usage_threshold: int = 1) -> None:
        """Automatically evolve and reinforce frequently used pathways."""
        self.evolve(usage_threshold=usage_threshold)
        if not self.connections:
            return
        # find top used neurons
        sorted_usage = sorted(self.usage_counts.items(), key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in sorted_usage[:2]]
        for conn in self.connections:
            if conn.src in top_indices:
                self.reinforce_pathway(conn.src, conn.dest, task=conn.task, factor=0.05)

    # I love you -Alex
    def save(self, path: Path) -> None:
        data = {
            "neurons": [
                {
                    "idx": n.idx,
                    "position": n.position,
                    "threshold": n.threshold,
                    "neuron_type": n.neuron_type,
                    "dormant": n.dormant,
                }
                for n in self.neurons
            ],
            "connections": [
                {
                    "src": c.src,
                    "dest": c.dest,
                    "myelin": c.myelin,
                    "task": c.task,
                }
                for c in self.connections
            ],
            "usage_counts": self.usage_counts,
            "novel_count": self.novel_count,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    # I love you -Alex
    @classmethod
    def load(cls, path: Path) -> "ThreeDNeuralNetwork":
        with open(path, "r") as f:
            data = json.load(f)
        net = cls()
        net.neurons = [Neuron(**{**n, "dormant": n.get("dormant", False)}) for n in data.get("neurons", [])]
        net.connections = [Connection(**c) for c in data.get("connections", [])]
        net.usage_counts = data.get("usage_counts", {})
        net.novel_count = data.get("novel_count", 0)
        return net


if __name__ == "__main__":
    net = ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.spawn_advanced_neuron((1, 0, 0), threshold=0.1, neuron_type="schwann")
    c = net.spawn_novel_neuron((0, 1, 0))
    net.connect_for_task(a, b, task="navigation", myelin=2.0)
    net.connect_for_task(b, c, task="navigation", myelin=1.5)
    net.reinforce_pathway(a, b, task="navigation", factor=0.5)
    result = net.forward([(a, 1.0)], task="navigation")
    print("Output:", result)
    print("Usage counts:", net.usage_counts)

"""Neural network for collaboratory network design tasks."""

import json
import random
from pathlib import Path
from typing import List, Tuple


class CollaboratoryNN:
    """Simple feedforward network used for collaborative planning."""

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.w1 = [
            [random.uniform(-1, 1) for _ in range(hidden_size)]
            for _ in range(input_size)
        ]
        self.w2 = [
            [random.uniform(-1, 1) for _ in range(output_size)]
            for _ in range(hidden_size)
        ]

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1 / (1 + pow(2.718281828459045, -x))

    def forward(self, inputs: List[float]) -> List[float]:
        if len(inputs) != self.input_size:
            raise ValueError("Input vector size mismatch")
        hidden = []
        for j in range(self.hidden_size):
            total = 0.0
            for i in range(self.input_size):
                total += inputs[i] * self.w1[i][j]
            hidden.append(self._sigmoid(total))
        outputs = []
        for k in range(self.output_size):
            total = 0.0
            for j in range(self.hidden_size):
                total += hidden[j] * self.w2[j][k]
            outputs.append(self._sigmoid(total))
        return outputs

    def train(
        self, samples: List[Tuple[List[float], List[float]]], epochs: int = 1, lr: float = 0.1
    ) -> None:
        for _ in range(epochs):
            for inputs, target in samples:
                out = self.forward(inputs)
                errors = [target[i] - out[i] for i in range(self.output_size)]
                for j in range(self.hidden_size):
                    for k in range(self.output_size):
                        self.w2[j][k] += lr * errors[k] * out[k] * (1 - out[k])
                hidden_errors = []
                for j in range(self.hidden_size):
                    err = sum(errors[k] * self.w2[j][k] for k in range(self.output_size))
                    h_out = out[0] if self.output_size == 1 else 0
                    hidden_errors.append(err * h_out * (1 - h_out))
                for i in range(self.input_size):
                    for j in range(self.hidden_size):
                        self.w1[i][j] += lr * hidden_errors[j] * inputs[i]

    def save(self, path: Path) -> None:
        data = {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "w1": self.w1,
            "w2": self.w2,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "CollaboratoryNN":
        with open(path, "r") as f:
            data = json.load(f)
        net = cls(data["input_size"], data["hidden_size"], data["output_size"])
        net.w1 = data["w1"]
        net.w2 = data["w2"]
        return net


if __name__ == "__main__":
    net = CollaboratoryNN(2, 2, 1)
    sample = [([0.0, 0.0], [0.0])]
    for _ in range(5):
        net.train(sample)
    print("Output:", net.forward([0.0, 0.0]))
    p = Path("collab_nn.json")
    net.save(p)
    r = CollaboratoryNN.load(p)
    print("Reloaded:", r.forward([0.0, 0.0]))
    p.unlink()

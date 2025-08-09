"""Simple adversarial generator network producing perturbations for training."""

import json
import random
from pathlib import Path
from typing import List, Tuple


class AdversarialNN:
    """Minimal feedforward network that generates noise vectors."""

    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.w1 = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.w2 = [random.uniform(-1, 1) for _ in range(hidden_size)]

    @staticmethod
    def _tanh(x: float) -> float:
        e_pos = pow(2.718281828459045, x)
        e_neg = pow(2.718281828459045, -x)
        return (e_pos - e_neg) / (e_pos + e_neg)

    def forward(self, inputs: List[float]) -> List[float]:
        if len(inputs) != self.input_size:
            raise ValueError("Input vector size mismatch")
        hidden = []
        for j in range(self.hidden_size):
            total = 0.0
            for i in range(self.input_size):
                total += inputs[i] * self.w1[i][j]
            hidden.append(self._tanh(total))
        noise = []
        for j in range(self.hidden_size):
            noise.append(self._tanh(hidden[j] * self.w2[j]))
        return noise

    def train(self, samples: List[Tuple[List[float], List[float]]], epochs: int = 1, lr: float = 0.1) -> None:
        for _ in range(epochs):
            for inputs, target in samples:
                out = self.forward(inputs)
                errors = [target[i] - out[i] for i in range(self.hidden_size)]
                for j in range(self.hidden_size):
                    self.w2[j] += lr * errors[j] * (1 - out[j] ** 2)
                for i in range(self.input_size):
                    for j in range(self.hidden_size):
                        self.w1[i][j] += lr * errors[j] * inputs[i]

    def save(self, path: Path) -> None:
        data = {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "w1": self.w1,
            "w2": self.w2,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "AdversarialNN":
        with open(path, "r") as f:
            data = json.load(f)
        net = cls(data["input_size"], data["hidden_size"])
        net.w1 = data["w1"]
        net.w2 = data["w2"]
        return net


if __name__ == "__main__":
    gen = AdversarialNN(2, 2)
    sample = [([0.0, 1.0], [0.5, -0.5])]
    for _ in range(3):
        gen.train(sample)
    out = gen.forward([0.0, 1.0])
    print("Noise:", out)
    p = Path("adversarial_nn.json")
    gen.save(p)
    loaded = AdversarialNN.load(p)
    print("Reloaded:", loaded.forward([0.0, 1.0]))
    p.unlink()

import random
import json
from pathlib import Path
from typing import List, Iterable, Tuple

class SimpleNeuralNetwork:
    """A minimal feedforward neural network for future experimentation."""

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

    def add_hidden_neuron(self):
        """Expand the hidden layer with a new neuron and random weights."""
        self.hidden_size += 1
        for i in range(self.input_size):
            self.w1[i].append(random.uniform(-1, 1))
        self.w2.append([random.uniform(-1, 1) for _ in range(self.output_size)])

    def update_weights(self, inputs: List[float], target: List[float], learning_rate: float = 0.1) -> None:
        """Backpropagate error and adjust both weight matrices."""
        outputs, hidden = self.forward(inputs, return_hidden=True)
        if len(target) != self.output_size:
            raise ValueError("Target vector size must match output size")
        errors = [target[i] - outputs[i] for i in range(self.output_size)]
        # update w2
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.w2[j][k] += learning_rate * errors[k] * hidden[j]
        # backpropagate through ReLU
        hidden_errors = []
        for j in range(self.hidden_size):
            err = sum(errors[k] * self.w2[j][k] for k in range(self.output_size))
            hidden_errors.append(err if hidden[j] > 0 else 0.0)
        # update w1
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.w1[i][j] += learning_rate * hidden_errors[j] * inputs[i]

    def train(self, examples: Iterable[Tuple[List[float], List[float]]], epochs: int = 1, learning_rate: float = 0.1) -> None:
        """Train the network on multiple examples."""
        for _ in range(epochs):
            for inputs, target in examples:
                self.update_weights(inputs, target, learning_rate)

    def save(self, path: Path) -> None:
        """Persist network weights to a JSON file."""
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
    def load(cls, path: Path) -> "SimpleNeuralNetwork":
        """Load a network from a JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        net = cls(data["input_size"], data["hidden_size"], data["output_size"])
        net.w1 = data["w1"]
        net.w2 = data["w2"]
        return net

    @staticmethod
    def _relu(x: float) -> float:
        return x if x > 0 else 0.0

    def forward(self, inputs: List[float], *, return_hidden: bool = False):
        if len(inputs) != self.input_size:
            raise ValueError("Input vector size does not match network input size")
        hidden = []
        for j in range(self.hidden_size):
            total = 0.0
            for i in range(self.input_size):
                total += inputs[i] * self.w1[i][j]
            hidden.append(self._relu(total))
        outputs = []
        for k in range(self.output_size):
            total = 0.0
            for j in range(self.hidden_size):
                total += hidden[j] * self.w2[j][k]
            outputs.append(total)
        if return_hidden:
            return outputs, hidden
        return outputs

if __name__ == "__main__":
    nn = SimpleNeuralNetwork(2, 2, 1)
    data = [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [1])]
    for _ in range(100):
        nn.train(data, epochs=1, learning_rate=0.1)
    print("Trained output for [1, 0] ->", nn.forward([1, 0]))
    path = Path("nn-test.json")
    nn.save(path)
    reloaded = SimpleNeuralNetwork.load(path)
    print("Reloaded output:", reloaded.forward([1, 0]))

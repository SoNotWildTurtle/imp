import random
from typing import List

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

    def update_weights(self, inputs: List[float], target: List[float], learning_rate: float = 0.1):
        """Very basic weight update using output error."""
        outputs = self.forward(inputs)
        if len(target) != self.output_size:
            raise ValueError("Target vector size must match output size")
        errors = [target[i] - outputs[i] for i in range(self.output_size)]
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.w2[j][k] += learning_rate * errors[k]

    @staticmethod
    def _relu(x: float) -> float:
        return x if x > 0 else 0.0

    def forward(self, inputs: List[float]) -> List[float]:
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
        return outputs

if __name__ == "__main__":
    nn = SimpleNeuralNetwork(2, 3, 1)
    result = nn.forward([1.0, -1.0])
    print("Network output:", result)

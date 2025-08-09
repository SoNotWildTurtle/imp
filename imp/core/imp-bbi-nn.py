import json
from pathlib import Path


class BBINN:
    """Simple brain-to-brain interface network that can grow hidden neurons."""

    def __init__(self, inputs: int, hidden: int, outputs: int):
        self.input_size = inputs
        self.hidden_size = hidden
        self.output_size = outputs
        self.w1 = [[0.0 for _ in range(hidden)] for _ in range(inputs)]
        self.w2 = [[0.0 for _ in range(outputs)] for _ in range(hidden)]

    def forward(self, x):
        h = [sum(x[i] * self.w1[i][j] for i in range(self.input_size))
             for j in range(self.hidden_size)]
        return [sum(h[j] * self.w2[j][k] for j in range(self.hidden_size))
                for k in range(self.output_size)]

    def evolve(self):
        """Add a new hidden neuron with zeroed connections."""
        self.hidden_size += 1
        for row in self.w1:
            row.append(0.0)
        self.w2.append([0.0 for _ in range(self.output_size)])

    def save(self, path):
        data = {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "w1": self.w1,
            "w2": self.w2,
        }
        Path(path).write_text(json.dumps(data))

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text())
        net = cls(data["input_size"], data["hidden_size"], data["output_size"])
        net.w1 = data["w1"]
        net.w2 = data["w2"]
        return net

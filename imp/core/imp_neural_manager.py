"""Central registry ensuring IMP controls all neural networks."""

from typing import Dict, Any

class NeuralManager:
    """Registry for neural network instances."""
    def __init__(self) -> None:
        self.networks: Dict[str, Any] = {}

    def register(self, name: str, network: Any) -> None:
        self.networks[name] = network

    def get(self, name: str) -> Any:
        return self.networks.get(name)

manager = NeuralManager()

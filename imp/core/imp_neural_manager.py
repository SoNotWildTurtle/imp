"""Central registry ensuring IMP controls all neural networks."""

from typing import Dict, Any, Callable

class NeuralManager:
    """Registry for neural network instances."""
    def __init__(self) -> None:
        self.networks: Dict[str, Any] = {}

    def register(self, name: str, network: Any) -> None:
        self.networks[name] = network

    def get(self, name: str) -> Any:
        return self.networks.get(name)

    def get_or_create(self, name: str, factory: Callable[[], Any]) -> Any:
        """Return a network if registered, otherwise create and register it."""
        net = self.get(name)
        if net is None:
            net = factory()
            self.register(name, net)
        return net

    def list(self) -> list:
        """List registered network names."""
        return list(self.networks.keys())

    def unregister(self, name: str) -> None:
        """Remove a network from the registry if present."""
        self.networks.pop(name, None)

manager = NeuralManager()

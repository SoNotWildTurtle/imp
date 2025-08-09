from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / 'models'
MAIN_MODEL = MODEL_DIR / 'main_nn.json'
ADV_MODEL = MODEL_DIR / 'adversarial_nn.json'

spec_main = importlib.util.spec_from_file_location('main_nn', ROOT / 'core' / 'imp-neural-network.py')
main_module = importlib.util.module_from_spec(spec_main)
spec_main.loader.exec_module(main_module)
NeuralNetwork = main_module.SimpleNeuralNetwork

spec_adv = importlib.util.spec_from_file_location('adv_nn', ROOT / 'core' / 'imp-adversarial-nn.py')
adv_module = importlib.util.module_from_spec(spec_adv)
spec_adv.loader.exec_module(adv_module)
AdversarialNN = adv_module.AdversarialNN


def load_main() -> NeuralNetwork:
    if MAIN_MODEL.exists():
        return NeuralNetwork.load(MAIN_MODEL)
    return NeuralNetwork(2, 2, 1)


def load_adv() -> AdversarialNN:
    if ADV_MODEL.exists():
        return AdversarialNN.load(ADV_MODEL)
    return AdversarialNN(2, 2)


SAMPLES = [
    ([0.0, 0.0], [0.0]),
    ([0.0, 1.0], [1.0]),
    ([1.0, 0.0], [1.0]),
    ([1.0, 1.0], [1.0]),
]


def run_adversarial_training(epochs: int = 1, epsilon: float = 0.1) -> None:
    MODEL_DIR.mkdir(exist_ok=True)
    main_net = load_main()
    adv_net = load_adv()
    for _ in range(epochs):
        for inputs, target in SAMPLES:
            noise = adv_net.forward(inputs)
            adv_inputs = [max(0.0, min(1.0, inputs[i] + epsilon * noise[i])) for i in range(len(inputs))]
            main_net.train([(adv_inputs, target)], epochs=1, learning_rate=0.1)
            out = main_net.forward(adv_inputs)[0]
            err = target[0] - out
            adv_target = [err for _ in range(adv_net.hidden_size)]
            adv_net.train([(inputs, adv_target)], epochs=1, lr=0.1)
    main_net.save(MAIN_MODEL)
    adv_net.save(ADV_MODEL)


if __name__ == '__main__':
    run_adversarial_training(epochs=2)
    print('Adversarial training complete.')

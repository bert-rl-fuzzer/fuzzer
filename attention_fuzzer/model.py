from abc import ABC, abstractmethod


class ActorCriticModel(ABC):
    def __init__(self, max_length, vocab_size):
        self.max_length = max_length
        self.vocab_size = vocab_size

    @abstractmethod
    def mlp(self, x, sizes, activation, output_activation):
        pass

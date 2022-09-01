import tensorflow as tf
from tensorflow.keras import layers

from model import ActorCriticModel


class GRUActorCriticModel(ActorCriticModel):

    def __init__(self, max_length, vocab_size):
        super().__init__(max_length, vocab_size)

    def mlp(self, x, sizes, activation=tf.tanh, output_activation=None):
        # Build a feedforward neural network
        x = layers.Embedding(self.vocab_size, 16)(x)
        x = layers.GRU(32, return_sequences=False)(x)
        x = layers.Dropout(0.2)(x)
        for size in sizes[:-1]:
            x = layers.Dense(units=size, activation=activation)(x)
        return layers.Dense(units=sizes[-1], activation=output_activation)(x)

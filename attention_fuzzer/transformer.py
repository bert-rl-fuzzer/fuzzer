import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Vanilla Transformer
from model import ActorCriticModel


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim), ]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output, weights = self.att(inputs, inputs, return_attention_scores=True)
        attn_output1 = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output1)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output), weights


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions


class TransformerActorCriticModel(ActorCriticModel):

    def __init__(self, max_length, vocab_size):
        super().__init__(max_length, vocab_size)

    def mlp(self, x, sizes, activation=tf.tanh, output_activation=None):
        embed_dim = 32  # Embedding size for each token
        num_heads = 4  # Number of attention heads
        ff_dim = 64  # Hidden layer size in feed forward network inside transformer

        embedding_layer = TokenAndPositionEmbedding(self.max_length, self.vocab_size, embed_dim)
        x = embedding_layer(x)
        transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
        x, attn_output = transformer_block(x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dropout(0.1)(x)
        for size in sizes[:-1]:
            x = layers.Dense(units=size, activation=activation)(x)
        return layers.Dense(units=sizes[-1], activation=output_activation)(x)

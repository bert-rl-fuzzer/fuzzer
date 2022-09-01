from pprint import pprint

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from model import ActorCriticModel
from model_utils import GenerateAndMutate

def define_expt_tag(EXPT_TAG):
    global expt_tag
    expt_tag = EXPT_TAG

class MaskedLanguageModel(tf.keras.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loss_fn = keras.losses.SparseCategoricalCrossentropy(
            reduction=tf.keras.losses.Reduction.NONE
        )
        self.loss_tracker = tf.keras.metrics.Mean(name="loss")

    def train_step(self, inputs):
        if len(inputs) == 3:
            features, labels, sample_weight = inputs
        else:
            features, labels = inputs
            sample_weight = None

        with tf.GradientTape() as tape:
            predictions = self(features, training=True)
            loss = self.loss_fn(labels, predictions, sample_weight=sample_weight)

        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # Compute our own metrics
        self.loss_tracker.update_state(loss, sample_weight=sample_weight)

        # Return a dict mapping metric names to current value
        return {"loss": self.loss_tracker.result()}

    @property
    def metrics(self):
        # We list our `Metric` objects here so that `reset_states()` can be
        # called automatically at the start of each epoch
        # or at the start of `evaluate()`.
        # If you don't implement this property, you have to call
        # `reset_states()` yourself at the time of your choosing.
        return [self.loss_tracker]


class MaskedTextGenerator(keras.callbacks.Callback):
    def __init__(self, sample_tokens, ind2word, word2ind, top_k=5):
        self.sample_tokens = sample_tokens
        self.mask_token_id = word2ind["<empty>"]
        self.ind2word = ind2word
        self.k = top_k

    def decode(self, tokens):
        return " ".join([self.ind2word[t] for t in tokens if t != 0])

    def convert_ids_to_tokens(self, id):
        return self.ind2word[id]

    def on_epoch_end(self, epoch, logs=None):
        prediction = self.model.predict(self.sample_tokens)

        masked_index = np.where(self.sample_tokens == self.mask_token_id)
        masked_index = masked_index[1]
        mask_prediction = prediction[0][masked_index]

        top_indices = mask_prediction[0].argsort()[-self.k:][::-1]
        values = mask_prediction[0][top_indices]

        for i in range(len(top_indices)):
            p = top_indices[i]
            v = values[i]
            tokens = np.copy(self.sample_tokens[0])
            tokens[masked_index[0]] = p
            result = {
                "input_text": self.decode(self.sample_tokens[0]),
                "prediction": self.decode(tokens),
                "probability": v,
                "predicted mask token": self.convert_ids_to_tokens(p),
            }
            pprint(result)


class BERTActorCriticModel(ActorCriticModel):

    def __init__(self, max_length, vocab_size, config, loaded_test, all_vocab, ind2word, word2ind, retrain=False):
        super().__init__(max_length, vocab_size)
        self.config = config
        self.loaded_test = loaded_test
        self.mask_token_id = word2ind["<empty>"]

        if retrain:
            # Prepare data for masked language model
            x_all_review = GenerateAndMutate(loaded_test, all_vocab, max_length, word2ind).encode(loaded_test)
            x_masked_train, y_masked_labels, sample_weights = self.get_masked_input_and_labels(x_all_review)

            mlm_ds = tf.data.Dataset.from_tensor_slices(
                (x_masked_train, y_masked_labels, sample_weights)
            )
            mlm_ds = mlm_ds.shuffle(1000).batch(self.config.BATCH_SIZE)

            sample_tokens = [x_masked_train[0]]
            generator_callback = MaskedTextGenerator(sample_tokens=np.array(sample_tokens), ind2word=ind2word, word2ind=word2ind)

            bert_masked_model = self.create_masked_language_bert_model()

            bert_masked_model.fit(mlm_ds, epochs=200, callbacks=[generator_callback])
            bert_masked_model.save(f"models/{EXPT_TAG}/bert_sql.h5")

        # BERT - from pretrained MLM

        mlm_model = keras.models.load_model(
            f"models/{EXPT_TAG}/bert_sql.h5", custom_objects={"MaskedLanguageModel": MaskedLanguageModel}
        )
        self.pretrained_bert_model = tf.keras.Model(
            mlm_model.input, mlm_model.get_layer("encoder_0/ffn_layernormalization").output
        )

    def mlp(self, x, sizes, activation=tf.tanh, output_activation=None):
        x = self.pretrained_bert_model(x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dropout(0.1)(x)
        for size in sizes[:-1]:
            x = layers.Dense(units=size, activation=activation)(x)
        return layers.Dense(units=sizes[-1], activation=output_activation)(x)

    def create_masked_language_bert_model(self):
        inputs = layers.Input((self.config.MAX_LEN,), dtype=tf.int64)

        word_embeddings = layers.Embedding(
            self.config.VOCAB_SIZE, self.config.EMBED_DIM, name="word_embedding"
        )(inputs)
        position_embeddings = layers.Embedding(
            input_dim=self.config.MAX_LEN,
            output_dim=self.config.EMBED_DIM,
            weights=[self.get_pos_encoding_matrix(self.config.EMBED_DIM)],
            name="position_embedding",
        )(tf.range(start=0, limit=self.config.MAX_LEN, delta=1))
        embeddings = word_embeddings + position_embeddings

        encoder_output = embeddings
        for i in range(self.config.NUM_LAYERS):
            encoder_output = self.bert_module(encoder_output, encoder_output, encoder_output, i)

        mlm_output = layers.Dense(self.config.VOCAB_SIZE, name="mlm_cls", activation="softmax")(
            encoder_output
        )
        mlm_model = MaskedLanguageModel(inputs, mlm_output, name="masked_bert_model")

        optimizer = keras.optimizers.Adam(learning_rate=self.config.LR)
        mlm_model.compile(optimizer=optimizer)
        return mlm_model

    def get_masked_input_and_labels(self, encoded_texts):
        # 15% BERT masking
        inp_mask = np.random.rand(*encoded_texts.shape) < 0.15
        # Do not mask special tokens
        inp_mask[encoded_texts <= 2] = False
        # Set targets to -1 by default, it means ignore
        labels = -1 * np.ones(encoded_texts.shape, dtype=int)
        # Set labels for masked tokens
        labels[inp_mask] = encoded_texts[inp_mask]

        # Prepare input
        encoded_texts_masked = np.copy(encoded_texts)
        # Set input to [MASK] which is the last token for the 90% of tokens
        # This means leaving 10% unchanged
        inp_mask_2mask = inp_mask & (np.random.rand(*encoded_texts.shape) < 0.90)
        encoded_texts_masked[
            inp_mask_2mask
        ] = self.mask_token_id  # mask token is the last in the dict

        # Set 10% to a random token
        inp_mask_2random = inp_mask_2mask & (np.random.rand(*encoded_texts.shape) < 1 / 9)
        encoded_texts_masked[inp_mask_2random] = np.random.randint(
            3, self.mask_token_id, inp_mask_2random.sum()
        )

        # Prepare sample_weights to pass to .fit() method
        sample_weights = np.ones(labels.shape)
        sample_weights[labels == -1] = 0

        # y_labels would be same as encoded_texts i.e input tokens
        y_labels = np.copy(encoded_texts)

        return encoded_texts_masked, y_labels, sample_weights

    def bert_module(self, query, key, value, i):
        # Multi headed self-attention
        attention_output = layers.MultiHeadAttention(
            num_heads=self.config.NUM_HEAD,
            key_dim=self.config.EMBED_DIM // self.config.NUM_HEAD,
            name="encoder_{}/multiheadattention".format(i),
        )(query, key, value)
        attention_output = layers.Dropout(0.1, name="encoder_{}/att_dropout".format(i))(
            attention_output
        )
        attention_output = layers.LayerNormalization(
            epsilon=1e-6, name="encoder_{}/att_layernormalization".format(i)
        )(query + attention_output)

        # Feed-forward layer
        ffn = keras.Sequential(
            [
                layers.Dense(self.config.FF_DIM, activation="relu"),
                layers.Dense(self.config.EMBED_DIM),
            ],
            name="encoder_{}/ffn".format(i),
        )
        ffn_output = ffn(attention_output)
        ffn_output = layers.Dropout(0.1, name="encoder_{}/ffn_dropout".format(i))(
            ffn_output
        )
        sequence_output = layers.LayerNormalization(
            epsilon=1e-6, name="encoder_{}/ffn_layernormalization".format(i)
        )(attention_output + ffn_output)
        return sequence_output

    def get_pos_encoding_matrix(self, d_emb):
        pos_enc = np.array(
            [
                [pos / np.power(10000, 2 * (j // 2) / d_emb) for j in range(d_emb)]
                if pos != 0
                else np.zeros(d_emb)
                for pos in range(self.max_length)
            ]
        )
        pos_enc[1:, 0::2] = np.sin(pos_enc[1:, 0::2])  # dim 2i
        pos_enc[1:, 1::2] = np.cos(pos_enc[1:, 1::2])  # dim 2i+1
        return pos_enc

# Reference: https://www.tensorflow.org/text/tutorials/classify_text_with_bert
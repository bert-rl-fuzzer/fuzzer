import random

import numpy as np


class GenerateAndMutate:

    def __init__(self, loaded_test, all_vocab, MAX_LENGTH, word2ind):
        self.loaded_test = loaded_test
        self.all_vocab = all_vocab
        self.MAX_LENGTH = MAX_LENGTH
        self.word2ind = word2ind

    def eos_and_ind(self, sampled_list: list, ind: bool = False):  # <EOS> append to shorter sentences
        if ind:
            eos_token = 0
        else:
            eos_token = "<EOS>"
        clip_ind = sampled_list.index(eos_token)
        # clip_ind = np.where(sampled_list==eos_token)[0][0] # for numpy
        if clip_ind < self.MAX_LENGTH - 1:
            clip_ind_rem = self.MAX_LENGTH - clip_ind
            sampled_list = sampled_list[:clip_ind] + [eos_token] * clip_ind_rem  # slower than if; sampled_list[:clip_ind] -> till non-eos token
        assert len(sampled_list) == self.MAX_LENGTH
        if ind:
            return sampled_list
        return [self.word2ind[s] for s in sampled_list]

    def init_string_list(self, gram_gen_str=None):  # initialize seed string
        if gram_gen_str is None:
            gram_gen_str = self.loaded_test[random.randint(0, len(self.loaded_test) - 1)]  # randint a<=N<=b

        sampled_list = gram_gen_str + (self.MAX_LENGTH - len(gram_gen_str)) * ['<EOS>']
        # sampled_list = list(random.sample(all_vocab, MAX_LENGTH-1))+['<EOS>']
        return self.eos_and_ind(sampled_list)

    def mutate_string_list(self, seed: list, pos: int = None, vocab: int = None, insertion_mode: int = None):
        if vocab is None:
            vocab_str = random.sample(self.all_vocab, 1)[0]
            vocab = self.word2ind[vocab_str]
        if pos is None:
            pos = random.randint(0, self.MAX_LENGTH - 2)  # MAX_LENGTH-2 inclusive
        if pos != self.MAX_LENGTH - 1:  # should never replace EOS
            if vocab == self.word2ind['<empty>'] and insertion_mode == 1:  # equivalent to deleting
                del seed[pos]
                seed += [self.word2ind['<EOS>']]
            elif vocab == self.word2ind['<empty>'] and insertion_mode == 2:
                pass
            elif insertion_mode == 2:  # insertion
                seed.insert(pos, vocab) # added a new token, so now the length is MAX_LENGTH+1 (position of EOS) & index of EOS: MAX_LENGTH
                del seed[self.MAX_LENGTH - 1]  # remove the one before the eos - to maintain length
            else:
                seed[pos] = vocab
        return self.eos_and_ind(seed, ind=True)

    def encode(self, texts):  # encode string tokens to integer
        encoded_texts = []
        for text in texts:
            encoded_text = self.init_string_list(text)
            encoded_texts.append(encoded_text)
        return np.array(encoded_texts)

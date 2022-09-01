import random
from collections import Counter

import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.util import ngrams


class Preprocess:
    def __init__(self, str_replace_dict, bigrams_processed_list):
        self.str_replace_dict = str_replace_dict
        self.bigrams_processed_list = bigrams_processed_list

    # Replace with generalized column names and table names
    def generalize_tokens(self, all_grammar_inputs_arg):
        for key, value in self.str_replace_dict.items():
            all_grammar_inputs_arg = list(set([sub.replace(key, value) for sub in all_grammar_inputs_arg]))

        return all_grammar_inputs_arg

    # Preprocessing: Tokenization, lower-case, bi-grams
    def basic_nltk_preproc(self, all_grammar_inputs_arg, override_bigram_list=False):
        all_bigrams_processed_list = None
        sent = all_grammar_inputs_arg.copy()

        sent_processed = []
        bigram_processed = []
        tokenizer = WordPunctTokenizer()
        max_len = 0

        for input_str in sent:
            input_str = str(input_str)
            input_str = input_str.lower()
            input_str = input_str.strip()
            str_list = nltk.word_tokenize(input_str)
            bigram_processed += list(ngrams(str_list, 2))
            if len(str_list) > max_len:
                max_len = len(str_list)
            sent_processed.append(str_list)
            # sent_processed.append(tokenizer.tokenize(input_str))

        all_vocab = [v_w for v in sent_processed for v_w in v]

        v_count = dict(Counter(all_vocab))
        v_count = dict(sorted(v_count.items(), key=lambda item: item[1], reverse=True))
        all_vocab = list(v_count.keys())

        if override_bigram_list:
            most_common_bigrams = Counter(bigram_processed).most_common(30)
            all_bigrams_processed_list = [key for key, val in most_common_bigrams]

        return sent_processed, all_vocab, all_bigrams_processed_list

    # creating word2ind, ind2word after storing all vocab
    def create_ind_dict(self, all_vocab_arg):
        bigrams_processed = [v0 + ' ' + v1 for v0, v1 in self.bigrams_processed_list]
        all_vocab_arg += bigrams_processed

        all_vocab_arg.sort()

        ind_list = list(range(1, len(all_vocab_arg) + 1))

        word2ind = dict(zip(all_vocab_arg, ind_list))
        ind2word = dict(zip(ind_list, all_vocab_arg))

        word2ind['<EOS>'] = 0
        ind2word[0] = '<EOS>'

        word2ind['<empty>'] = len(all_vocab_arg) + 1  # used as masking for BERT, and deletion operation for PPO agent
        ind2word[len(all_vocab_arg) + 1] = '<empty>'

        all_vocab_arg = ['<EOS>'] + all_vocab_arg + ['<empty>']

        return all_vocab_arg, ind2word, word2ind

    # Merging the commonly used bi-grams
    def merge_common_bigrams(self, sent_processed_arg):
        for i in range(10):
            sent_processed_new = []
            mod_count = 0  # modification count for this iteration
            for test_list in sent_processed_arg:
                done_one_pass = False
                for sublist in self.bigrams_processed_list:
                    if not done_one_pass:
                        for idx_2 in range(len(test_list) - len(sublist) + 1):
                            if test_list[idx_2: idx_2 + len(sublist)] == list(sublist):
                                new_test_list = []
                                for enum_, val in enumerate(test_list):
                                    if enum_ == idx_2:
                                        new_test_list.append(" ".join(list(sublist)))
                                    elif idx_2 < enum_ < idx_2 + len(sublist):
                                        pass
                                    else:
                                        new_test_list.append(val)
                                sent_processed_new.append(new_test_list)
                                done_one_pass = True
                                mod_count += 1
                                break
                if not done_one_pass:  # even after traversing the whole bigram list
                    sent_processed_new.append(test_list)
            # print(len(sent_processed_new))
            sent_processed_arg = sent_processed_new.copy()
            # print("Mod count: ", mod_count)

        return sent_processed_arg


class SQLPreprocess(Preprocess):
    def __init__(self, str_replace_dict, bigrams_processed_list):
        super().__init__(str_replace_dict, bigrams_processed_list)

    # Some specific curated SQL statements
    def hand_pick_sql_queries(self):
        seed_file = open('custom_seed', 'r')
        lines = seed_file.readlines()
        arr = []
        for line in lines:
            if len(line) > 1:
                line = line.strip()
                arr.append(line)
        all_grammar_inputs_handpicked = list(set(arr))

        return all_grammar_inputs_handpicked


from Stub.Stub import StubSession
from db import *
from grammar_lib.SQLChecker import parser
from grammar_lib.testCaseModifier import GCheckModifier
from mab import *
from model_utils import GenerateAndMutate


# TODO: Subclass

class NaiveFuzzEnv:
    def __init__(self, loaded_test, all_vocab, MAX_LENGTH, VOCAB_SIZE, word2ind, ind2word, preferred_col_name,
                steps_per_epoch, CREATE_DB, rand_generation, rand_mutation):

        self.rand_generation = rand_generation
        self.rand_mutation = rand_mutation

        self.generate_and_mutate = GenerateAndMutate(loaded_test, all_vocab, MAX_LENGTH, word2ind)

        if CREATE_DB:
            create_database(stop_random=True)

        self.preferred_col_name = preferred_col_name

        self.ACTION_SPACE_SIZE_POS = MAX_LENGTH
        self.ACTION_SPACE_SIZE_VOCAB = VOCAB_SIZE

        self.steps_per_epoch = steps_per_epoch
        self.ind2word = ind2word
        self.word2ind = word2ind

    def random_fuzzer(self, max_length: int = 50, char_start: int = 32, char_range: int = 126) -> str:
        # Source: https://www.fuzzingbook.org/html/Fuzzer.html
        """A string of up to `max_length` characters
           in the range [`char_start`, `char_start` + `char_range`)"""
        string_length = random.randrange(0, max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(char_start, char_start + char_range))
        return out

    def reset(self):
        if self.rand_generation:
            self.init_string = self.random_fuzzer()  # this will be a raw string for random fuzzer
            self.seed_str = self.init_string
            self.last_str = self.init_string
        else:
            self.init_string = self.generate_and_mutate.init_string_list()
            self.seed_str = self.init_string.copy()
            self.last_str = self.init_string.copy()

        self.selected_table_name, self.possible_columns = get_sampled_table_and_col(
            preferred_main=random.choice([True, False]))

        self.session = StubSession()
        self.last_status = 0

        self.episode_step = 0
        observation = self.init_string

        self.gmod = GCheckModifier()
        self.gparse = parser()

        self.operation = 'None'

        return np.array(observation)

    def action(self, pos, vocab, insertion_mode):
        if self.rand_generation:
            self.last_str = self.seed_str
            self.seed_str = self.random_fuzzer()
        else:
            self.last_str = self.seed_str.copy()
            logging.info(f"ACTION: seed={self.seed_str}, pos={pos}, vocab={vocab}, insertion_mode={insertion_mode}")
            self.seed_str = self.generate_and_mutate.mutate_string_list(seed=self.seed_str, pos=pos, vocab=vocab,
                                                                    insertion_mode=insertion_mode)
            logging.info(f"After mutation: {self.seed_str}")

    def replace_col_table_names(self, new_observation_: list):
        mod_token_sent = []
        col_ind = 0
        for token in new_observation_:
            cols_to_consider = list(
                set(self.possible_columns).intersection(
                    set(self.preferred_col_name))) + self.possible_columns
            if 'col_name' in token:
                mod_token_sent.append(token.replace('col_name', cols_to_consider[col_ind]))
                col_ind += 1
            elif 'table_name' in token:
                mod_token_sent.append(token.replace('table_name', self.selected_table_name))
            else:
                mod_token_sent.append(token)
        return mod_token_sent

    def step(self, action):
        self.episode_step += 1
        num_actions = self.ACTION_SPACE_SIZE_VOCAB * self.ACTION_SPACE_SIZE_POS * 2

        if self.rand_generation:
            self.action(None, None, None)
            username_rl = self.seed_str
            new_observation = username_rl
            logging.debug(f"username_rl: {username_rl}")

        else:

            for _ in range(50): # max 50 chances to pass the parser

                action_pos, action_vocab, action_insertion = self.breakdown_action(action)
                self.action(action_pos, action_vocab, action_insertion)

                new_observation = self.seed_str

                eos_index = new_observation.index(0)
                new_observation_ = new_observation[:eos_index]
                new_observation_ = self.replace_col_table_names([self.ind2word[s] for s in new_observation_]).copy()
                username_rl = " ".join(new_observation_)

                eos_indexL = self.last_str.index(0)
                new_observationL_ = self.last_str[:eos_indexL]
                new_observationL_ = self.replace_col_table_names([self.ind2word[s] for s in new_observationL_]).copy()
                last_username_rl = " ".join(new_observationL_)

                logging.debug(f"username_rl: {username_rl}; last_username_rl: {last_username_rl}")

                parser_failed = self.gparse.main(self.gmod.grammarchecker(username_rl))

                action = random.randint(0, num_actions - 1)  # for next iteration; randint includes the upper bound

                if not parser_failed or self.rand_mutation:
                    break

        # Search box

        fuzzing_success1, exception_success1 = attack_search_box(username_rl)

        # Login page

        values = [username_rl, "RaNdOmStRiNg"]
        fuzzing_success2, exception_success2 = attack_login_page(values[0], values[1])

        # Common

        fuzzing_success = fuzzing_success1 or fuzzing_success2
        exception_success = exception_success1 or exception_success2

        done = False
        if self.episode_step >= self.steps_per_epoch or fuzzing_success:
            done = True

        # TODO: new_observation will be a string for rand gen
        return np.array(new_observation), fuzzing_success, exception_success, done

    def breakdown_action(self, action): # action_pos max value is MAX_LENGTH-1, action_vocab max value is vocab size - 1
        if action > self.ACTION_SPACE_SIZE_VOCAB * self.ACTION_SPACE_SIZE_POS * 2 - 1:
            raise ValueError("Not a valid action value ", action)
        max_possible = self.ACTION_SPACE_SIZE_POS * self.ACTION_SPACE_SIZE_VOCAB
        if action >= max_possible:
            action = action - max_possible
            action_insertion = 2
        else:
            action_insertion = 1
        action_pos = action // self.ACTION_SPACE_SIZE_VOCAB
        action_vocab = action % self.ACTION_SPACE_SIZE_VOCAB
        # logging.debug(f'POS: {action_pos} VOCAB: {action_vocab} CONV: {action_pos * self.ACTION_SPACE_SIZE_VOCAB + action_vocab}')
        return action_pos, action_vocab, action_insertion

    def squeeze_actions(self, action_pos, action_vocab, action_insertion):
        if action_insertion == 1:
            return action_pos * self.ACTION_SPACE_SIZE_VOCAB + action_vocab
        elif action_insertion == 2:
            max_possible = self.ACTION_SPACE_SIZE_POS * self.ACTION_SPACE_SIZE_VOCAB
            return max_possible + (action_pos * self.ACTION_SPACE_SIZE_VOCAB + action_vocab)
        else:
            raise ValueError("Not a valid action_insertion value ", action_insertion)


class RLFuzz:
    def __init__(self, rewarding: list, selected_table_name: str, possible_columns: list, mab_agent, mutation_obj,
                 ind2word):
        if rewarding is None:
            preferred_main = False
            samples = [mab_agent._sample_bandit_mean(bandit) for bandit in mab_agent.bandits]
            self.current_bandit = mab_agent.bandits[np.argmax(samples)]
            self.init_string = self.current_bandit.encoded_sent.copy()
            if 'union' not in self.current_bandit.encoded_sent_str:
                preferred_main = True
            # self.init_string  = init_string_list() # always as index
            self.selected_table_name, self.possible_columns = get_sampled_table_and_col(preferred_main=preferred_main)
        else:
            self.init_string = rewarding.copy()
            self.selected_table_name = selected_table_name
            self.possible_columns = possible_columns.copy()
        self.seed_str = self.init_string.copy()
        self.last_str = self.init_string.copy()
        self.ind2word = ind2word
        self.mutation_obj = mutation_obj

    def __str__(self):
        return f'\nOrig seed string: \n{" ".join([self.ind2word[s] for s in self.init_string])}\nLast seed string: \n{" ".join([self.ind2word[s] for s in self.last_str])}\nCurr seed string: \n{" ".join([self.ind2word[s] for s in self.seed_str])}'

    def action(self, pos, vocab, insertion_mode):
        self.last_str = self.seed_str.copy()
        logging.info(f"ACTION: seed={self.seed_str}, pos={pos}, vocab={vocab}, insertion_mode={insertion_mode}")
        self.seed_str = self.mutation_obj.mutate_string_list(seed=self.seed_str, pos=pos, vocab=vocab,
                                                             insertion_mode=insertion_mode)
        logging.info(f"After mutation: {self.seed_str}")


class RLFuzzEnv:
    EXCEPTION_PENALTY = 0.1
    MUTATION_PENALTY = 0.2
    SAME_STRING_PENALTY = 0.3  # eos & grammar related
    PARSER_PENALTY = 0.5
    SUCCESS_REWARD = 5

    def __init__(self, loaded_test, all_vocab, MAX_LENGTH, VOCAB_SIZE, word2ind, ind2word, preferred_col_name,
                 steps_per_epoch, CREATE_DB):
        self.generate_and_mutate = GenerateAndMutate(loaded_test, all_vocab, MAX_LENGTH, word2ind)
        encoded_texts = self.generate_and_mutate.encode(loaded_test)
        self.mab_agent = BayesianAgent('bernoulli')
        self.mab_agent.bandits = [BernoulliBandit(sent) for sent in encoded_texts]

        self.loaded_test = loaded_test
        self.all_vocab = all_vocab
        self.word2ind = word2ind
        self.ind2word = ind2word
        self.preferred_col_name = preferred_col_name
        self.steps_per_epoch = steps_per_epoch

        self.ACTION_SPACE_SIZE_POS = MAX_LENGTH
        self.ACTION_SPACE_SIZE_VOCAB = VOCAB_SIZE
        if CREATE_DB:
            create_database(stop_random=True)

    def reset(self, rewarding: list = None, selected_table_name: str = None, possible_columns: list = None):
        self.session = StubSession()
        self.last_status = 0
        self.fuzzer = RLFuzz(rewarding, selected_table_name, possible_columns, self.mab_agent, self.generate_and_mutate,
                             self.ind2word)
        self.episode_step = 0
        observation = self.fuzzer.init_string

        self.gmod = GCheckModifier()
        self.gparse = parser()

        self.operation = 'None'

        return np.array(observation)

    def replace_col_table_names(self, new_observation_: list):
        mod_token_sent = []
        col_ind = 0
        for token in new_observation_:
            cols_to_consider = list(
                set(self.fuzzer.possible_columns).intersection(
                    set(self.preferred_col_name))) + self.fuzzer.possible_columns
            if 'col_name' in token:
                mod_token_sent.append(token.replace('col_name', cols_to_consider[col_ind]))
                col_ind += 1
            elif 'table_name' in token:
                mod_token_sent.append(token.replace('table_name', self.fuzzer.selected_table_name))
            else:
                mod_token_sent.append(token)
        return mod_token_sent

    def step(self, action):
        action_pos, action_vocab, action_insertion = self.breakdown_action(action)
        fuzzing_success, exception_success = False, False  # init
        self.episode_step += 1
        self.fuzzer.action(action_pos, action_vocab, action_insertion)
        new_observation = self.fuzzer.seed_str

        eos_index = new_observation.index(0)
        new_observation_ = new_observation[:eos_index]
        new_observation_ = self.replace_col_table_names([self.ind2word[s] for s in new_observation_]).copy()
        username_rl = " ".join(new_observation_)

        eos_indexL = self.fuzzer.last_str.index(0)
        new_observationL_ = self.fuzzer.last_str[:eos_indexL]
        new_observationL_ = self.replace_col_table_names([self.ind2word[s] for s in new_observationL_]).copy()
        last_username_rl = " ".join(new_observationL_)

        parser_failed = self.gparse.main(self.gmod.grammarchecker(username_rl))

        logging.debug(f"username_rl: {username_rl}; last_username_rl: {last_username_rl}")

        if self.episode_step > 1 and (len(username_rl.strip()) == 0 or last_username_rl == username_rl):  # rudimentary
            logging.debug(f"SAME_STRING_PENALTY @ {self.episode_step}: {username_rl}")
            reward = -self.SAME_STRING_PENALTY
        elif parser_failed:  # parser
            logging.debug(f"PARSER_PENALTY @ {self.episode_step}: {username_rl}")
            reward = -self.PARSER_PENALTY
        else:  # check via website

            # Search box

            fuzzing_success1, exception_success1 = attack_search_box(username_rl)

            # Login page

            values = [username_rl, "RaNdOmStRiNg"]
            fuzzing_success2, exception_success2 = attack_login_page(values[0], values[1])

            # Common

            fuzzing_success = fuzzing_success1 or fuzzing_success2
            exception_success = exception_success1 or exception_success2

            if fuzzing_success:
                reward = self.SUCCESS_REWARD
            elif exception_success:
                reward = -self.EXCEPTION_PENALTY
            else:
                reward = -self.MUTATION_PENALTY

        done = False
        fuzzing_valid_succ = False
        if fuzzing_success and self.episode_step > 7:  # ignoring initial success due to the generated seed being the injection string
            fuzzing_valid_succ = True
        if self.episode_step >= self.steps_per_epoch or fuzzing_valid_succ:
            done = True

        return np.array(new_observation), reward, fuzzing_valid_succ, exception_success, done

    def breakdown_action(self, action):
        if action > self.ACTION_SPACE_SIZE_VOCAB * self.ACTION_SPACE_SIZE_POS * 2 - 1:
            raise ValueError("Not a valid action value ", action)
        max_possible = self.ACTION_SPACE_SIZE_POS * self.ACTION_SPACE_SIZE_VOCAB
        if action >= max_possible:
            action = action - max_possible
            action_insertion = 2
        else:
            action_insertion = 1
        action_pos = action // self.ACTION_SPACE_SIZE_VOCAB
        action_vocab = action % self.ACTION_SPACE_SIZE_VOCAB
        # logging.debug(f'POS: {action_pos} VOCAB: {action_vocab} CONV: {action_pos * self.ACTION_SPACE_SIZE_VOCAB + action_vocab}')
        return action_pos, action_vocab, action_insertion

    def squeeze_actions(self, action_pos, action_vocab, action_insertion):
        if action_insertion == 1:
            return action_pos * self.ACTION_SPACE_SIZE_VOCAB + action_vocab
        elif action_insertion == 2:
            max_possible = self.ACTION_SPACE_SIZE_POS * self.ACTION_SPACE_SIZE_VOCAB
            return max_possible + (action_pos * self.ACTION_SPACE_SIZE_VOCAB + action_vocab)
        else:
            raise ValueError("Not a valid action_insertion value ", action_insertion)


"""
- VOCAB_SIZE, MAX_LENGTH # (61, 9)
- RLFuzzEnv().breakdown_action(61*9-1) # (8,60,1) - starts from ind 0
- RLFuzzEnv().breakdown_action(61*9*2-1) # (8,60,2) - starts from ind 0
"""

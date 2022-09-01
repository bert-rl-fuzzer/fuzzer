import random

class MutationFuzzerHelper:
    def __init__(self, seed, min_length, max_length, st_char, end_char, min_mutations=2, max_mutations=10):
        self.min_length = min_length
        self.max_length = max_length
        self.st_char = st_char
        self.end_char = end_char
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self):
        self.population = self.seed
        self.seed_index = 0

    def flip_random_character(self, s):
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return s

        pos = random.randint(0, len(s) - 1)
        new_c = chr(random.randrange(self.st_char, self.end_char))
        # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
        return s[:pos] + new_c + s[pos + 1:]

    def insert_random_character(self, s):
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(self.st_char, self.end_char))
        # print("Inserting", repr(random_character), "at", pos)
        new_str = s[:pos] + random_character + s[pos:]
        if len(new_str) <= self.max_length:
            return new_str
        else:
            return s

    def delete_random_character(self, s):
        """Returns s with a random character deleted"""
        if s == "":
            return s

        pos = random.randint(0, len(s) - 1)
        # print("Deleting", repr(s[pos]), "at", pos)
        new_str = s[:pos] + s[pos + 1:]
        if len(new_str) >= self.min_length:
            return new_str
        else:
            return s

    def mutate(self, inp):
        """Return s with a random mutation applied"""
        mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character
        ]
        mutator = random.choice(mutators)
        # print(mutator)
        return mutator(inp)

    def create_candidate(self):
        # maximizing diversity in coverage in our population
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for _ in range(trials):
            candidate = self.mutate(candidate)
        return candidate

    def fuzz(self):
        # The fuzz() method is set to first pick the seeds; when these are gone, we mutate
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()
        return self.inp


class MutationFuzzer:

    __MAXIMUM_CHR_RANGE = 11141112
    __DEFAULT_CHAR_START = 32
    __DEFAULT_CHAR_END = 64
    __DEFAULT_MUT_OP = 5

    def logic_validator(self, min_length: int, max_length: int, char_start: int, char_end: int) -> bool:
        if min_length > max_length:
            raise Exception("Min Length Cannot be Greater Than Max Length")
        if char_start > char_end:
            raise Exception("Character Range End less than Starting")
        if char_end > self.__MAXIMUM_CHR_RANGE:
            raise Exception("Character Range Cannot Exceed 11,141,112.")
        if min_length < 1 or max_length < 1 or char_start < 1 or char_end < 1:
            raise Exception("Arguments must be greater than 0")
        return True

    def fuzzer(self, min_length: int, max_length: int, char_start: int = __DEFAULT_CHAR_START,
               char_end: int = __DEFAULT_CHAR_END, mutation_op: int = __DEFAULT_MUT_OP, seed: str = None) -> list:
        self.logic_validator(min_length, max_length, char_start, char_end)
        if seed is None:
            random_string_length = random.randrange(min_length, max_length+1)
            seed_value = ""
            for i in range(0, random_string_length):
                seed_value += chr(random.randrange(char_start, char_end+1))
        else:
            seed_value = seed
        mutation_fuzzer = MutationFuzzerHelper(seed=[seed_value], min_length=min_length, max_length=max_length,
                                               st_char=char_start, end_char=char_end)
        mutation_fuzzer_list = []
        for i in range(mutation_op):
            mutation_fuzzer_list.append(mutation_fuzzer.fuzz())
        return mutation_fuzzer_list

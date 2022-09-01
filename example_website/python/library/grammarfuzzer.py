import gramfuzz

class GrammarFuzzer:

    __DEFAULT_COUNT = 5

    def fuzzer(self, grammar_file: str, grammar_cat: str, grammar_count: int = __DEFAULT_COUNT) -> list:
        fuzzer = gramfuzz.GramFuzzer()
        fuzzer.load_grammar(grammar_file)
        names = fuzzer.gen(cat=grammar_cat, num=grammar_count)
        string_list = [i.decode() for i in names]
        return string_list

import random

# Reference: https://www.fuzzingbook.org/html/Fuzzer.html


class randomfuzzer:
    MAXIMUM_CHR_RANGE = 11141112
    DEFAULT_CHAR_START = 32
    DEFAULT_CHAR_END = 64

    def logic_validator(min_length: int, max_length: int, char_start: int, char_end: int) -> bool:
        if min_length > max_length:
            raise Exception("Min Length Cannot be Greater Than Max Length")
        if char_start > char_end:
            raise Exception("Character Range End less than Starting")
        if char_end > randomfuzzer.MAXIMUM_CHR_RANGE:
            raise Exception("Character Range Cannot Exceed 11,141,112.")
        if min_length < 1 or max_length < 1 or char_start < 1 or char_end < 1:
            raise Exception("Arguments must be greater than 0")
        return True

    def fuzzer(min_length: int, max_length: int, char_start: int = DEFAULT_CHAR_START, char_end: int = DEFAULT_CHAR_END) -> str:
        randomfuzzer.logic_validator(
            min_length, max_length, char_start, char_end)
        random_string_length = random.randrange(min_length, max_length+1)
        random_string = ""
        for i in range(0, random_string_length):
            random_string += chr(random.randrange(char_start, char_end+1))
        return random_string

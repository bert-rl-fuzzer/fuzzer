#!/usr/bin/env python3
from library.grammarfuzzer import *
import sys


class GrammarFuzzAdapter:
    __MINIMUM_ARGUMENTS = 3
    __MAXIMUM_ARGUMENTS = 4

    def input_validator(self, n: int, argument: list) -> bool:
        if n < self.__MINIMUM_ARGUMENTS:
            raise Exception("Missing Arguments")
        if n > self.__MAXIMUM_ARGUMENTS:
            raise Exception("Too Many Arguments")
        for i in range(1, n):
            try:
                if i < 3:
                    argument.append(sys.argv[i])
                else:
                    argument.append(int(sys.argv[i]))
            except Exception as e:
                raise Exception("Invalid Arguments: ", e)
        return True

    @staticmethod
    def gramfuzz_caller(argument: list):
        strings = GrammarFuzzer().fuzzer(*argument)
        return strings

    def adapter(self) -> bool:
        try:
            n = len(sys.argv)
            argument = []
            self.input_validator(n, argument)
            gram_strings = self.gramfuzz_caller(argument)
            for val in gram_strings:
                print(val, file=sys.stdout)
            return True
        except Exception as e:
            print("FuzzError: "+str(e), file=sys.stderr)
            return False


if __name__ == "__main__":
    GrammarFuzzAdapter().adapter()

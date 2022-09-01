#!/usr/bin/env python3
from library.mutationfuzzer import *
import sys


class MutationFuzzAdapter:
    __MINIMUM_ARGUMENTS = 3
    __MAXIMUM_ARGUMENTS = 7

    def input_validator(self, n: int, argument: list) -> bool:
        if n < self.__MINIMUM_ARGUMENTS:
            raise Exception("Missing Arguments")
        if n > self.__MAXIMUM_ARGUMENTS:
            raise Exception("Too Many Arguments")
        for i in range(1, n):
            try:
                if i < 6:
                    argument.append(int(sys.argv[i]))
                else:
                    argument.append(sys.argv[i])
            except Exception as e:
                raise Exception("Invalid Arguments: ", e)
        return True

    @staticmethod
    def mutationfuzz_caller(argument: list):
        strings = MutationFuzzer().fuzzer(*argument)
        return strings

    def adapter(self) -> bool:
        try:
            n = len(sys.argv)
            argument = []
            self.input_validator(n, argument)
            mutated_strings = self.mutationfuzz_caller(argument)
            for val in mutated_strings:
                print(val, file=sys.stdout)
            return True
        except Exception as e:
            print("FuzzError: "+str(e), file=sys.stderr)
            return False


if __name__ == "__main__":
    MutationFuzzAdapter().adapter()

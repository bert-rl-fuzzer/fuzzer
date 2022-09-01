#!/usr/bin/env python3
from library.randomfuzzer import *
import sys


class randomfuzzadapter:
    MINIMUM_ARGUMENTS = 3
    PARTIAL_ARGUMENTS = 4
    MAXIMUM_ARGUMENTS = 5

    def inputvalidator(n: int, argument: list) -> bool:
        if n < randomfuzzadapter.MINIMUM_ARGUMENTS:
            raise Exception("Missing Arguments")
        if n > randomfuzzadapter.MAXIMUM_ARGUMENTS:
            raise Exception("Too Many Arguments")
        for i in range(1, n):
            try:
                argument.append(int(sys.argv[i]))
            except:
                raise Exception("Invalid Arguments")
        return True

    def randomfuzzcaller(n: int, argument: list) -> str:
        if n == randomfuzzadapter.MAXIMUM_ARGUMENTS:
            randomstring = randomfuzzer.fuzzer(
                argument[0], argument[1], argument[2], argument[3])
            return randomstring
        if n == randomfuzzadapter.PARTIAL_ARGUMENTS:
            randomstring = randomfuzzer.fuzzer(
                argument[0], argument[1], argument[2])
            return randomstring
        if n == randomfuzzadapter.MINIMUM_ARGUMENTS:
            randomstring = randomfuzzer.fuzzer(argument[0], argument[1])
            return randomstring
        raise Exception("Adapter Failed!")
    
    def adapter() -> bool:
        try:
            n = len(sys.argv)
            argument = []
            randomfuzzadapter.inputvalidator(n, argument)
            randomstring = randomfuzzadapter.randomfuzzcaller(n, argument)
            print(randomstring, file=sys.stdout)
            return True
        except Exception as e:
            print("FuzzError: "+str(e), file=sys.stderr)
            return False


if __name__ == "__main__":
    randomfuzzadapter.adapter()

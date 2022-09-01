import unittest
import sys
from unittest import TestCase
sys.path.append('/project/python')
from library.randomfuzzer import *


class TestSample(TestCase):

    def testlogicvalidator(self):
        
        check = randomfuzzer.logic_validator(1,2,1,2)
        self.assertTrue(check)

        try:
            check = randomfuzzer.logic_validator(2,1,1,2)
        except Exception as e:
            check = False
        self.assertFalse(check)
        
        try:
            check = randomfuzzer.logic_validator(1,2,2,1)
        except Exception as e:
            check = False
        self.assertFalse(check)
        
        try:
            check = randomfuzzer.logic_validator(1,2,2,1)
        except Exception as e:
            check = False
        self.assertFalse(check)

        try:
            check = randomfuzzer.logic_validator(1,2,2,11141113)
        except Exception as e:
            check = False
        self.assertFalse(check)

        try:
            check = randomfuzzer.logic_validator(1,2,2,0)
        except Exception as e:
            check = False
        self.assertFalse(check)

        try:
            check = randomfuzzer.logic_validator(1,2,0,2)
        except Exception as e:
            check = False
        self.assertFalse(check)

        try:
            check = randomfuzzer.logic_validator(1,0,1,2)
        except Exception as e:
            check = False
        self.assertFalse(check)

        try:
            check = randomfuzzer.logic_validator(0,2,1,2)
        except Exception as e:
            check = False
        self.assertFalse(check)

    def testfuzzer(self):
        string = randomfuzzer.fuzzer(2,2)
        check = (len(string) == 2)
        self.assertTrue(check)

        string = randomfuzzer.fuzzer(1,1,84,84)
        check = (string == "T")
        self.assertTrue(check)
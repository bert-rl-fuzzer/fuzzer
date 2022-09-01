import unittest
import sys
from unittest import TestCase
from unittest import mock
sys.path.append('/project/python')
from library.randomfuzzer import *
from randomfuzzadapter import *

class TestSample(TestCase):

    EMPTY_ARGUMENT_LIST = []
    LESS_THAN_MINIMUM_ARGUMENTS = 2
    MORE_THAN_MAXIMUM_ARGUMENTS = 6
    ACCEPTABLE_ARGUMENTS = 4
    ILLEGAL_ARGUMENT_LIST = ["","some string", "some other string", "should have been integers values as strings"]
    ACCEPTABLE_ARGUMENT_LIST = ["1","1", "1", "1"]

    def testinputvalidator(self):
        arglist = TestSample.EMPTY_ARGUMENT_LIST
        n = TestSample.LESS_THAN_MINIMUM_ARGUMENTS
        sys.argv = arglist
        try:
            check = randomfuzzadapter.inputvalidator(n, arglist)
        except:
            check = False
        self.assertFalse(check)

        arglist = TestSample.EMPTY_ARGUMENT_LIST
        n = TestSample.MORE_THAN_MAXIMUM_ARGUMENTS
        sys.argv = arglist
        try:
            check = randomfuzzadapter.inputvalidator(n, arglist)
        except:
            check = False
        self.assertFalse(check)

        arglist = TestSample.ILLEGAL_ARGUMENT_LIST
        n = TestSample.ACCEPTABLE_ARGUMENTS 
        sys.argv = arglist
        try:
            check = randomfuzzadapter.inputvalidator(n, arglist)
        except:
            check = False
        self.assertFalse(check)

        arglist = TestSample.ACCEPTABLE_ARGUMENT_LIST
        n = TestSample.ACCEPTABLE_ARGUMENTS
        sys.argv = arglist 
        try:
            check = randomfuzzadapter.inputvalidator(n, arglist)
        except Exception as e:
            check = False
        self.assertTrue(check)


    @mock.patch("library.randomfuzzer.randomfuzzer.fuzzer", return_value="T", autospec=True)
    def testrandomfuzzcaller(self, mock_fuzzer):
        n = TestSample.LESS_THAN_MINIMUM_ARGUMENTS
        arglist = TestSample.EMPTY_ARGUMENT_LIST
        try:
            string = randomfuzzadapter.randomfuzzcaller(n, arglist)
            check = True
        except:
            check = False
        self.assertFalse(check)

        n = TestSample.MORE_THAN_MAXIMUM_ARGUMENTS
        arglist = TestSample.EMPTY_ARGUMENT_LIST
        try:
            string = randomfuzzadapter.randomfuzzcaller(n, arglist)
            check = True
        except:
            check = False
        self.assertFalse(check)

        n = TestSample.ACCEPTABLE_ARGUMENTS
        arglist = TestSample.EMPTY_ARGUMENT_LIST
        try:
            string = randomfuzzadapter.randomfuzzcaller(n, arglist)
            check = True
        except:
            check = False
        self.assertFalse(check)

        
        n = TestSample.ACCEPTABLE_ARGUMENTS
        arglist = TestSample.ACCEPTABLE_ARGUMENT_LIST
        try:
            string = randomfuzzadapter.randomfuzzcaller(n, arglist)
            check = True
        except Exception as e:
            check = False
        self.assertTrue(check)


    @mock.patch("randomfuzzadapter.randomfuzzadapter.inputvalidator", return_value="True", autospec=True)
    @mock.patch("randomfuzzadapter.randomfuzzadapter.randomfuzzcaller", return_value="T", autospec=True)
    def testadaptersuccess(self, mock_input, mock_caller):
        n = TestSample.ACCEPTABLE_ARGUMENTS
        n = 0
        arglist = TestSample.ACCEPTABLE_ARGUMENT_LIST
        sys.argv = arglist
        try:
            randomfuzzadapter.adapter()
            check = True
        except:
            check = False
        self.assertTrue(check)


    def testadapterfailure(self):
        n = TestSample.LESS_THAN_MINIMUM_ARGUMENTS
        arglist = TestSample.EMPTY_ARGUMENT_LIST
        sys.argv = arglist
        try:
            check = randomfuzzadapter.adapter()
        except:
            check = False
        self.assertFalse(check)
        

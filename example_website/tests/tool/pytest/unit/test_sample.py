import unittest
from unittest import TestCase


class TestSample(TestCase):

    def testFalse(self):
        self.assertFalse(False)

    def testTrue(self):
        self.assertTrue(True)

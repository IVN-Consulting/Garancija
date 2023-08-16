import unittest
import main

class TestMain(unittest.TestCase):
    def test_main1(self):
        a = 10
        b = 10
        result = main.plus(a,b)
        (self.assertEqual(result , a+b))
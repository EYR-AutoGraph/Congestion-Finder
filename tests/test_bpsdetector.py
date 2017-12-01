import unittest
import congestionfinder
import logging
logging.basicConfig(format='%(asctime)s %(message)s')

class TestBPSDetector(unittest.TestCase):

    def test_getBPSCode(self):
        input = "00D00C03405B18200005"
        expected = input
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(input)
        output = bpsDetector.getBPSCode()
        logging.info("input: " + input)
        logging.info("expected: " + expected)
        logging.info("output: " + output)
        self.assertEqual(expected, output)

    def test_getRoadNumber(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_getHectometer(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_getAdditionalMeters(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_getMeter(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()
import unittest
import congestionfinder.bpsdetector
import logging

logging.getLogger().level = logging.DEBUG


class TestBPSDetector(unittest.TestCase):
    def test_getBPSCode(self):
        logging.debug("Starting test_getSpaceToSpaceIndex()")
        input = "00D00C03405B18200005"
        expected = input
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(input)
        output = bpsDetector.getBPSCode()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getSpaceToSpaceIndex()")

    def test_getRoadNumber(self):
        logging.debug("Starting test_getRoadNumber()")
        input = "00D00C03405B18200005"
        expected = 12
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(input)
        output = bpsDetector.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getRoadNumber()")

    def test_getHectometer(self):
        logging.debug("Starting test_getHectometer()")
        input = "00D00C03405B18200005"
        expected = 208
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(input)
        output = bpsDetector.getHectometer()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getHectometer()")

    def test_getAdditionalMeters(self):
        logging.debug("Starting test_getAdditionalMeters()")
        input = "00D00C03405B18200005"
        expected = 91
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(input)
        output = bpsDetector.getAdditionalMeters()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getAdditionalMeters()")

    def test_getMeter(self):
        logging.debug("Starting test_getMeter()")
        input = "00D00C03405B18200005"
        expected = 20891
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(input)
        output = bpsDetector.getMeter()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getMeter()")


if __name__ == '__main__':
    unittest.main()

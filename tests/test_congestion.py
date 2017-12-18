import unittest
import numpy
import congestionfinder.congestion
import logging

logging.getLogger().level = logging.DEBUG


class TestCongestion(unittest.TestCase):
    def test_parseSpeedFlowsToCongestions(self):
        logging.debug("Starting test_parseSpeedFlowsToCongestions()")
        inputSpeed = numpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        inputFlow = numpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        speedThreshold = 10
        flowThreshold = 10
        expected = numpy.array([[.1, .2, .3], [.4, .5, .6], [.7, .8, .9]])
        output = congestionfinder.congestion.parseSpeedFlowsToCongestions(inputSpeed, inputFlow, speedThreshold, flowThreshold)
        logging.debug("input: " + str(inputSpeed))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        numpy.testing.assert_array_equal(expected, output)
        logging.debug("Ending test_parseSpeedFlowsToCongestions()")


if __name__ == '__main__':
    unittest.main()

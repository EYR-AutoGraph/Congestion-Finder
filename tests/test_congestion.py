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

    def test_interpolateMissingValues(self):
        logging.debug("Starting test_interpolateMissingValues()")
        input = numpy.array([[1, 2, 3], [4, numpy.nan, 6], [7, 8, 9]])
        expected = numpy.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
        output = congestionfinder.congestion.interpolateMissingValues(input)
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        numpy.testing.assert_array_almost_equal(expected, output)
        logging.debug("Ending test_interpolateMissingValues()")

    def test_applySmoothingFilter(self):
        logging.debug("Starting test_applySmoothingFilter()")
        input = numpy.array([[1, 1, 1], [1, 10, 1], [1, 1, 1]])
        spaceSmoothing = 1
        timeSmoothing = 3
        output = congestionfinder.congestion.applySmoothingFilter(input, spaceSmoothing, timeSmoothing)
        logging.debug("input: " + str(input))
        logging.debug("output: " + str(output))
        numpy.testing.assert_array_equal(output[0, 0], input[0, 0])
        numpy.testing.assert_array_less(input[1, 0], output[1, 0])
        numpy.testing.assert_array_less(output[1, 1], input[1, 1])
        logging.debug("Ending test_applySmoothingFilter()")


if __name__ == '__main__':
    unittest.main()

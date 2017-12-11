import unittest
import congestionfinder.detection
import logging

logging.getLogger().level = logging.DEBUG


class TestDetection(unittest.TestCase):
    def test_getCode(self):
        logging.debug("Starting test_getCode()")
        input = "test_code"
        space = 123
        time = 456
        speed = 789
        flow = 10
        detection = congestionfinder.detection.Detection(input, space, time, speed, flow)
        expected = input
        output = detection.getCode()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getCode()")

    def test_getSpace(self):
        logging.debug("Starting test_getSpace()")
        code = "test_code"
        input = 123
        time = 456
        speed = 789
        flow = 10
        detection = congestionfinder.detection.Detection(code, input, time, speed, flow)
        expected = input
        output = detection.getSpace()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getSpace()")

    def test_getTime(self):
        logging.debug("Starting test_getTime()")
        code = "test_code"
        space = 123
        input = 456
        speed = 789
        flow = 10
        detection = congestionfinder.detection.Detection(code, space, input, speed, flow)
        expected = input
        output = detection.getTime()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getTime()")

    def test_getSpeed(self):
        logging.debug("Starting test_getSpeed()")
        code = "test_code"
        space = 123
        time = 456
        input = 789
        flow = 10
        detection = congestionfinder.detection.Detection(code, space, time, input, flow)
        expected = input
        output = detection.getSpeed()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getSpeed()")

    def test_getFlow(self):
        logging.debug("Starting test_getFlow()")
        code = "test_code"
        space = 123
        time = 456
        speed = 789
        input = 10
        detection = congestionfinder.detection.Detection(code, space, time, speed, input)
        expected = input
        output = detection.getFlow()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getFlow()")


if __name__ == '__main__':
    unittest.main()

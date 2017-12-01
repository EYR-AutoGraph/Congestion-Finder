import unittest
import congestionfinder.road
import logging

logging.getLogger().level = logging.DEBUG


class TestRoad(unittest.TestCase):
    def test_getRoadNumber(self):
        input = 3
        expected = input
        road = congestionfinder.road.Road(input)
        output = road.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)

    def test_addBPSDetector(self):
        input = 3
        expected = input
        road = congestionfinder.road.Road(input)
        output = road.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)

    def test_indexDetectorSpaces(self):
        input = 3
        expected = input
        road = congestionfinder.road.Road(input)
        output = road.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)

    def test_getBPSDetectors(self):
        input = 3
        expected = input
        road = congestionfinder.road.Road(input)
        output = road.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)

    def test_getSpaceToSpaceIndex(self):
        input = 3
        expected = input
        road = congestionfinder.road.Road(input)
        output = road.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()

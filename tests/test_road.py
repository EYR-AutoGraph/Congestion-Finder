import unittest
import copy
import congestionfinder.bpsdetector
import congestionfinder.road
import logging

logging.getLogger().level = logging.DEBUG


class TestRoad(unittest.TestCase):
    def test_getRoadNumber(self):
        logging.debug("Starting test_getRoadNumber()")
        input = 3
        expected = input
        road = congestionfinder.road.Road(input)
        output = road.getRoadNumber()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getRoadNumber()")

    def test_addBPSDetector(self):
        logging.debug("Starting test_addBPSDetector()")
        input = congestionfinder.bpsdetector.BPSDetector("00D00C03405B18200005")
        expected1 = set()
        expected2 = set()
        expected2.add(input)
        road = congestionfinder.road.Road(3)
        output1 = copy.copy(road.getBPSDetectors())
        road.addBPSDetector(input)
        output2 = road.getBPSDetectors()
        logging.debug("input: " + str(input))
        logging.debug("expected1: " + str(expected1))
        logging.debug("output1: " + str(output1))
        logging.debug("expected2: " + str(expected2))
        logging.debug("output2: " + str(output2))
        self.assertEqual(expected1, output1)
        self.assertEqual(expected2, output2)
        logging.debug("Ending test_addBPSDetector()")

    def test_getBPSDetectors(self):
        logging.debug("Starting test_getBPSDetectors()")
        input = congestionfinder.bpsdetector.BPSDetector("00D00C03405B18200005")
        expected = set()
        expected.add(input)
        road = congestionfinder.road.Road(3)
        road.addBPSDetector(input)
        output = road.getBPSDetectors()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getBPSDetectors()")

    def test_indexDetectorSpaces(self):
        logging.debug("Starting test_indexDetectorSpaces()")
        bpsDetector1 = congestionfinder.bpsdetector.BPSDetector("10D00100A055D0070007")
        bpsDetector2 = congestionfinder.bpsdetector.BPSDetector("10D00100B85ED0070007")
        expected1 = dict()
        expected2 = {4085:0, 4694:1}
        road = congestionfinder.road.Road(3)
        road.addBPSDetector(bpsDetector1)
        road.addBPSDetector(bpsDetector2)
        output1 = copy.copy(road.getSpaceToSpaceIndex())
        road.indexDetectorSpaces()
        output2 = road.getSpaceToSpaceIndex()
        logging.debug("expected1: " + str(expected1))
        logging.debug("output1: " + str(output1))
        logging.debug("expected2: " + str(expected2))
        logging.debug("output2: " + str(output2))
        self.assertEqual(expected1, output1)
        self.assertEqual(expected2, output2)
        logging.debug("Ending test_indexDetectorSpaces()")

    def test_getSpaceToSpaceIndex(self):
        logging.debug("Starting test_getSpaceToSpaceIndex()")
        bpsDetector1 = congestionfinder.bpsdetector.BPSDetector("10D00100A055D0070007")
        bpsDetector2 = congestionfinder.bpsdetector.BPSDetector("10D00100B85ED0070007")
        expected = {4085:0, 4694:1}
        road = congestionfinder.road.Road(3)
        road.addBPSDetector(bpsDetector1)
        road.addBPSDetector(bpsDetector2)
        road.indexDetectorSpaces()
        output = road.getSpaceToSpaceIndex()
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getSpaceToSpaceIndex()")

    def test_parseBPSDetectorsToRoads(self):
        logging.debug("Starting test_parseBPSDetectorsToRoads()")
        bpsDetector1 = congestionfinder.bpsdetector.BPSDetector("10D00204C00038200005")
        bpsDetector2 = congestionfinder.bpsdetector.BPSDetector("10D00204D037D007000B")
        bpsDetector3 = congestionfinder.bpsdetector.BPSDetector("10D01005381ED0070007")
        input = [bpsDetector1, bpsDetector2, bpsDetector3]
        road1 = congestionfinder.road.Road(2)
        road2 = congestionfinder.road.Road(16)
        road1.addBPSDetector(bpsDetector1)
        road1.addBPSDetector(bpsDetector2)
        road2.addBPSDetector(bpsDetector3)
        road1.indexDetectorSpaces()
        road2.indexDetectorSpaces()
        expected = {2: road1, 16: road2}
        output = congestionfinder.road.parseBPSDetectorsToRoads(input)
        logging.debug("expected[2]: " + str(expected[2]))
        logging.debug("output[2]: " + str(output[2]))
        logging.debug("expected[16]: " + str(expected[16]))
        logging.debug("output[16]: " + str(output[16]))
        self.assertEqual(str(expected[2]), str(output[2]))
        self.assertEqual(str(expected[16]), str(output[16]))
        logging.debug("Ending test_parseBPSDetectorsToRoads()")


if __name__ == '__main__':
    unittest.main()

import unittest
import numpy
import congestionfinder.bpsdetector
import congestionfinder.detection
import congestionfinder.road
import congestionfinder.speedflow
import patchfinder.patch
import logging

logging.getLogger().level = logging.DEBUG


class TestSpeedFlow(unittest.TestCase):
    def test_parseDetectionsToSpeedsAndFlows(self):
        logging.debug("Starting test_parseDetectionsToSpeedsAndFlows()")
        road = congestionfinder.road.Road(2)
        road.addBPSDetector(congestionfinder.bpsdetector.BPSDetector("10D00204C00038200005"))
        road.addBPSDetector(congestionfinder.bpsdetector.BPSDetector("10D002051800D0070013"))
        road.addBPSDetector(congestionfinder.bpsdetector.BPSDetector("10D002057000D007000F"))
        road.indexDetectorSpaces()
        input = [congestionfinder.detection.Detection("10D00204C00038200005", 30400, 1, 100, 1),
                 congestionfinder.detection.Detection("10D00204C00038200005", 30400, 2, 80, 17),
                 congestionfinder.detection.Detection("10D00204C00038200005", 30400, 3, 70, 15),
                 congestionfinder.detection.Detection("10D002051800D0070013", 32600, 1, 100, 1),
                 congestionfinder.detection.Detection("10D002051800D0070013", 32600, 2, 55, 18),
                 congestionfinder.detection.Detection("10D002051800D0070013", 32600, 3, 40, 14),
                 congestionfinder.detection.Detection("10D002057000D007000F", 34800, 1, 95, 1),
                 congestionfinder.detection.Detection("10D002057000D007000F", 34800, 2, 85, 14),
                 congestionfinder.detection.Detection("10D002057000D007000F", 34800, 3, 100, 19)]
        speeds, flows, minSpaceIndex, maxSpaceIndex, minTimeIndex, maxTimeIndex = congestionfinder.speedflow.parseDetectionsToSpeedsAndFlows(input, road)
        expectedSpeeds = numpy.array([[100, 80, 70], [100, 55, 40], [95, 85, 100]])
        expectedFlows = numpy.array([[1, 17, 15], [1, 18, 14], [1, 14, 19]])
        expectedMinSpaceIndex = 0
        expectedMaxSpaceIndex = 2
        expectedMinTimeIndex = 1
        expectedMaxTimeIndex = 3
        logging.debug("input: " + str(input))
        logging.debug("expected speeds: " + str(expectedSpeeds))
        logging.debug("output speeds: " + str(speeds))
        logging.debug("expected flows: " + str(expectedFlows))
        logging.debug("output flows: " + str(flows))
        logging.debug("expected minSpaceIndex: " + str(expectedMinSpaceIndex))
        logging.debug("output minSpaceIndex: " + str(minSpaceIndex))
        logging.debug("expected maxSpaceIndex: " + str(expectedMaxSpaceIndex))
        logging.debug("output maxSpaceIndex: " + str(maxSpaceIndex))
        logging.debug("expected minTimeIndex: " + str(expectedMinTimeIndex))
        logging.debug("output minTimeIndex: " + str(minTimeIndex))
        logging.debug("expected maxTimeIndex: " + str(expectedMaxTimeIndex))
        logging.debug("output maxTimeIndex: " + str(maxTimeIndex))
        numpy.testing.assert_array_equal(expectedSpeeds, speeds)
        numpy.testing.assert_array_equal(expectedFlows, flows)
        self.assertEqual(expectedMinSpaceIndex, minSpaceIndex)
        self.assertEqual(expectedMaxSpaceIndex, maxSpaceIndex)
        self.assertEqual(expectedMinTimeIndex, minTimeIndex)
        self.assertEqual(expectedMaxTimeIndex, maxTimeIndex)
        logging.debug("Ending test_parseDetectionsToSpeedsAndFlows()")

    def test_removeMissingDetectors(self):
        logging.debug("Starting test_removeMissingDetectors()")
        input = numpy.array([[1, 2, 3], [numpy.nan, numpy.nan, numpy.nan], [7, 8, 9]], dtype=numpy.float64)
        output, _, _ = congestionfinder.speedflow.removeMissingDetectors(input, input)
        expected = numpy.array([[1, 2, 3], [7, 8, 9]], dtype=numpy.float64)
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        numpy.testing.assert_array_equal(expected, output)
        logging.debug("Ending test_removeMissingDetectors()")

    def test_removeLowFlowTimes(self):
        logging.debug("Starting test_removeLowFlowTimes()")
        input = numpy.array([[1, 2, 3], [2, 5, 6], [0, 8, 9]], dtype=numpy.float64)
        lowFlowThreshold = 2
        output, _, _ = congestionfinder.speedflow.removeLowFlowTimes(input, input, lowFlowThreshold)
        expected = numpy.array([[2, 3], [5, 6], [8, 9]], dtype=numpy.float64)
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        numpy.testing.assert_array_equal(expected, output)
        logging.debug("Ending test_removeLowFlowTimes()")

    def test_unmaskPatches(self):
        logging.debug("Starting test_unmaskPatches()")
        input = [patchfinder.patch.Patch(2, 3, 4, 5),
                 patchfinder.patch.Patch(0, 2, 1, 3),
                 patchfinder.patch.Patch(3, 3, 0, 1)]
        maskSpace = [True, True, False, True, True]
        maskTime = [True, True, True, True, False, True, True]
        output = congestionfinder.speedflow.unmaskPatches(input, maskSpace, maskTime)
        expected = [patchfinder.patch.Patch(3, 4, 5, 6),
                    patchfinder.patch.Patch(0, 3, 1, 3),
                    patchfinder.patch.Patch(4, 4, 0, 1)]
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_unmaskPatches()")

    def test_addMargins(self):
        logging.debug("Starting test_addMargins()")
        patch1 = patchfinder.patch.Patch(1, 2, 3, 4)
        patch2 = patchfinder.patch.Patch(5, 5, 5, 5)
        input = [patch1, patch2]
        patch2 = patchfinder.patch.Patch(0, 4, 0, 7)
        patch3 = patchfinder.patch.Patch(3, 6, 2, 8)
        expected = [patch2, patch3]
        output = congestionfinder.speedflow.addMargins(input, 2, 3, 0, 6, 0, 10)
        logging.debug("input: " + " - ".join(str(x) for x in input))
        logging.debug("expected: " + " - ".join(str(x) for x in expected))
        logging.debug("output: " + " - ".join(str(x) for x in output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_addMargins()")


if __name__ == '__main__':
    unittest.main()

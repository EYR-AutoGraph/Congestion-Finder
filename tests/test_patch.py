import unittest
import numpy
import patchfinder.patch
import logging

logging.getLogger().level = logging.DEBUG


class TestPatch(unittest.TestCase):
    def test_getXStart(self):
        logging.debug("Starting test_getXStart()")
        input = 123
        expected = input
        patch = patchfinder.patch.Patch(input, 1, 2, 3)
        output = patch.getXStart()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getXStart()")

    def test_getXEnd(self):
        logging.debug("Starting test_getXEnd()")
        input = 123
        expected = input
        patch = patchfinder.patch.Patch(0, input, 2, 3)
        output = patch.getXEnd()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getXEnd()")

    def test_getYStart(self):
        logging.debug("Starting test_getYStart()")
        input = 123
        expected = input
        patch = patchfinder.patch.Patch(0, 1, input, 3)
        output = patch.getYStart()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getYStart()")

    def test_getYEnd(self):
        logging.debug("Starting test_getYEnd()")
        input = 123
        expected = input
        patch = patchfinder.patch.Patch(0, 1, 2, input)
        output = patch.getYEnd()
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_getYEnd()")

    def test_findPatches(self):
        logging.debug("Starting test_findPatches()")
        input = numpy.full((5, 5), False)
        input[0, 1] = True
        input[1, 2] = True
        input[1, 4] = True
        input[3, 0] = True
        input[3, 1] = True
        input[3, 2] = True
        input[4, 0] = True
        input[4, 1] = True
        expected1 = patchfinder.patch.Patch(0, 1, 1, 2)
        expected2 = patchfinder.patch.Patch(3, 4, 0, 2)
        expected3 = patchfinder.patch.Patch(1, 1, 4, 4)
        output = patchfinder.patch.findPatches(input)
        logging.debug("input: " + str(input.T))
        logging.debug("expected1: " + str(expected1))
        logging.debug("output1: " + str(output[0]))
        self.assertEqual(expected1, output[0])
        logging.debug("expected2: " + str(expected2))
        logging.debug("output2: " + str(output[1]))
        self.assertEqual(expected2, output[1])
        logging.debug("expected3: " + str(expected3))
        logging.debug("output3: " + str(output[2]))
        self.assertEqual(expected3, output[2])
        logging.debug("Ending test_findPatches()")

    def test_filterLargePatches(self):
        logging.debug("Starting test_filterLargePatches()")
        input = patchfinder.patch.Patch(1, 999, 1, 999)
        patch1 = patchfinder.patch.Patch(1, 2, 3, 4)
        patch2 = patchfinder.patch.Patch(5, 5, 5, 5)
        expected = input
        output = patchfinder.patch.filterLargePatches([input, patch1, patch2], 100)[0]
        logging.debug("input: " + str(input))
        logging.debug("expected: " + str(expected))
        logging.debug("output: " + str(output))
        self.assertEqual(expected, output)
        logging.debug("Ending test_filterLargePatches()")


if __name__ == '__main__':
    unittest.main()

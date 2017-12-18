import unittest
import congestionfinder.speedflow
import patchfinder.patch
import logging

logging.getLogger().level = logging.DEBUG


class TestSpeedFlow(unittest.TestCase):
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

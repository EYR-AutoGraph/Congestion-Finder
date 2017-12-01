import congestionfinder
import logging
logging.basicConfig(format='%(asctime)s %(message)s')


class Road:
    roadNumber = None
    bpsDetectors = None
    spaceToSpaceIndex = None

    def __init__(self, roadNumber):
        self.roadNumber = roadNumber
        self.bpsDetectors = set()
        self.spaceToSpaceIndex = dict()

    def getRoadNumber(self) -> int:
        return self.roadNumber

    def addBPSDetector(self, bpsDetector):
        self.bpsDetectors.add(bpsDetector)

    def indexDetectorSpaces(self):
        spaceSet = set()
        for bpsDetector in self.bpsDetectors:
            spaceSet.add(bpsDetector.getMeter())
        sortedSpaceSet = sorted(spaceSet)
        for spaceIndex in range(len(sortedSpaceSet)):
            self.spaceToSpaceIndex[sortedSpaceSet[spaceIndex]] = spaceIndex

    def getBPSDetectors(self) -> set:
        return self.bpsDetectors

    def getSpaceToSpaceIndex(self) -> dict:
        return self.spaceToSpaceIndex

    def __str__(self):
        template = "roadNumber: {} | len(bpsDetectors): {} | len(spaceToSpaceIndex): {}"
        return template.format(self.roadNumber, len(self.bpsDetectors), len(self.spaceToSpaceIndex))


def parseBPSCodesToRoads(bpsCodes):
    logging.debug("Starting parseBPSCodesToRoads()")
    result = dict()
    for bpsCode in bpsCodes:
        bpsDetector = congestionfinder.bpsdetector.BPSDetector(bpsCode)
        roadNumber = bpsDetector.getRoadNumber()
        if roadNumber not in result:
            road = Road(roadNumber)
            result[roadNumber] = road
        result[roadNumber].addBPSDetector(bpsDetector)
    for key, value in result.items():
        value.indexDetectorSpaces()
    logging.debug("Ending parseBPSCodesToRoads()")
    return result

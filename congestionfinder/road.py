import logging


class Road:
    roadNumber = None
    bpsDetectors = None
    spaceToSpaceIndex = None
    spaceIndexToSpace = None

    def __init__(self, roadNumber):
        self.roadNumber = roadNumber
        self.bpsDetectors = set()
        self.spaceToSpaceIndex = dict()

    def getRoadNumber(self) -> int:
        return self.roadNumber

    def getBPSDetectors(self) -> set:
        return self.bpsDetectors

    def getSpaceToSpaceIndex(self) -> dict:
        return self.spaceToSpaceIndex

    def getSpaceIndexToSpace(self) -> list:
        return self.spaceIndexToSpace

    def addBPSDetector(self, bpsDetector):
        self.bpsDetectors.add(bpsDetector)

    def indexDetectorSpaces(self):
        spaceSet = set()
        for bpsDetector in self.bpsDetectors:
            spaceSet.add(bpsDetector.getMeter())
        self.spaceIndexToSpace = sorted(spaceSet)
        for spaceIndex in range(len(self.spaceIndexToSpace)):
            self.spaceToSpaceIndex[self.spaceIndexToSpace[spaceIndex]] = spaceIndex

    def __str__(self):
        template = "roadNumber: {} | len(bpsDetectors): {} | len(spaceToSpaceIndex): {}"
        return template.format(self.roadNumber, len(self.bpsDetectors), len(self.spaceToSpaceIndex))


def parseBPSDetectorsToRoads(bpsDetectors):
    logging.debug("Starting parseBPSDetectorsToRoads()")
    result = dict()
    for bpsDetector in bpsDetectors:
        roadNumber = bpsDetector.getRoadNumber()
        if roadNumber not in result:
            road = Road(roadNumber)
            result[roadNumber] = road
        result[roadNumber].addBPSDetector(bpsDetector)
    for value in result.values():
        value.indexDetectorSpaces()
    logging.debug("Ending parseBPSDetectorsToRoads()")
    return result

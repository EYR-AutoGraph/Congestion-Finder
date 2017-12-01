import csv
import logging


class BPSDetector:
    bpsCode = None
    roadNumber = None
    hectometer = None
    additionalMeters = None

    def __init__(self, bpsCode: str):
        self.bpsCode = bpsCode
        self.roadNumber = extractAttribute(bpsCode, 14, 24)
        self.hectometer = extractAttribute(bpsCode, 24, 38)
        self.additionalMeters = extractAttribute(bpsCode, 38, 48)

    def getBPSCode(self) -> str:
        return self.bpsCode

    def getRoadNumber(self) -> int:
        return self.roadNumber

    def getHectometer(self) -> int:
        return self.hectometer

    def getAdditionalMeters(self) -> int:
        return self.additionalMeters

    def getMeter(self) -> int:
        return 100 * self.hectometer + self.additionalMeters

    def __str__(self) -> str:
        template = "bpsCode: {} | roadNumber: {} | hectometer: {} | additionalMeters: {}"
        return template.format(self.bpsCode, self.roadNumber, self.hectometer, self.additionalMeters)


def extractAttribute(bpsCode: str, startBit: int, endBit: int) -> int:
    return int(bpsCode, 16) >> (80 - endBit) & int("1" * (endBit - startBit), 2)


def readCSVToBPSCodes(fileName: str) -> object:
    logging.debug("Starting readCSVToBPSCodes()")
    result = []
    with open(fileName, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[3] == "R":
                result.append(row[0])
    logging.debug("Ending readCSVToBPSCodes()")
    return result

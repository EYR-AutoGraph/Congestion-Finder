import csv


class BPSDetector:
    bpsCode = None
    roadNumber = None
    hectometer = None
    additionalMeters = None

    def __init__(self, bpsCode):
        self.bpsCode = bpsCode
        self.roadNumber = extractAttribute(bpsCode, 14, 24)
        self.hectometer = extractAttribute(bpsCode, 24, 38)
        self.additionalMeters = extractAttribute(bpsCode, 38, 48)

    @property
    def getBPSCoder(self):
        return self.bpsCode

    @property
    def getRoadNumber(self):
        return self.roadNumber

    @property
    def getHectometer(self):
        return self.hectometer

    @property
    def getAdditionalMeters(self):
        return self.additionalMeters

    @property
    def getMeter(self):
        return 100 * self.hectometer + self.additionalMeters

    @property
    def __str__(self):
        stringTemplate = "bpsCode: {} | roadNumber: {} | hectometer: {} | additionalMeters: {}"
        templateElements = [self.bpsCode, self.roadNumber, self.hectometer, self.additionalMeters]
        return stringTemplate.format(*templateElements)


def extractAttribute(bpsCode, startBit, endBit):
    return int(bpsCode, 16) >> (80 - endBit) & int("1" * (endBit - startBit), 2)


def readCSVToBPSCodes(fileName):
    print("Starting readCSVToBPSCodes()")
    result = []
    with open(fileName, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[3] == "R":
                result.append(row[0])
    print("Ending readCSVToBPSCodes()")
    return result

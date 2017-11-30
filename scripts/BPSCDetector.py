def extractAttribute(bpsCode, startBit, endBit):
    return int(bpsCode, 16) >> (80 - endBit) & int("1" * (endBit - startBit), 2)


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

    def getBPSCoder(self):
        return self.bpsCode

    def getRoadNumber(self):
        return self.roadNumber

    def getHectometer(self):
        return self.hectometer

    def getAdditionalMeters(self):
        return self.additionalMeters

    def getMeter(self):
        return 100 * self.hectometer + self.additionalMeters

    @property
    def __str__(self):
        stringTemplate = "bpsCode: {} | roadNumber: {} | hectometer: {} | additionalMeters: {}"
        templateElements = [self.bpsCode, self.roadNumber, self.hectometer, self.additionalMeters]
        return stringTemplate.format(templateElements)

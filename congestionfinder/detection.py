import csv
import time as time_module
import logging
logging.basicConfig(format='%(asctime)s %(message)s')


class Detection:
    code = None
    space = None
    time = None
    speed = None
    flow = None

    def __init__(self, code, space, time, speed, flow):
        self.code = code
        self.space = space
        self.time = time
        self.speed = speed
        self.flow = flow

    def getCode(self) -> str:
        return self.code

    def getSpace(self) -> int:
        return self.space

    def getTime(self) -> int:
        return self.time

    def getSpeed(self) -> int:
        return self.speed

    def getFlow(self) -> int:
        return self.flow

    def __str__(self) -> str:
        template = "code: {} | space: {} | time: {} | speed: {} | flow: {}"
        return template.format(self.code, self.space, self.time, self.speed, self.flow)


def readCSVToDetections(fileName) -> set:
    logging.debug("Starting readCSVToDetections()")
    result = set()
    with open(fileName, "r") as file:
        reader = csv.reader(file, delimiter=" ")
        next(reader, None)
        next(reader, None)
        next(reader, None)
        for row in reader:
            if len(row) > 1 and row[2] == "R-":
                code = row[0]
                space = int(row[1][:-1])
                timeObject = time_module.strptime(row[6], "%H:%M")
                time = 60 * timeObject.tm_hour + timeObject.tm_min
                speed = int(row[9])
                flow = float(row[8]) / float(row[4])
                detection = Detection(code, space, time, speed, flow)
                result.add(detection)
    logging.debug("Ending readCSVToDetections()")
    return result

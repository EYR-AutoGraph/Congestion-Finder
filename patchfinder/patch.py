import numpy
import copy
import logging


class Patch:
    xStart = None
    xEnd = None
    yStart = None
    yEnd = None

    def __init__(self, xStart, xEnd, yStart, yEnd):
        self.xStart = xStart
        self.xEnd = xEnd
        self.yStart = yStart
        self.yEnd = yEnd

    def getXStart(self):
        return self.xStart

    def getXEnd(self):
        return self.xEnd

    def getYStart(self):
        return self.yStart

    def getYEnd(self):
        return self.yEnd

    def setXStart(self, xStart):
        self.xStart = xStart

    def setXEnd(self, xEnd):
        self.xEnd = xEnd

    def setYStart(self, yStart):
        self.yStart = yStart

    def setYEnd(self, yEnd):
        self.yEnd = yEnd

    def asArray(self):
        return [self.xStart, self.xEnd, self.yStart, self.yEnd]

    def xSlice(self):
        return slice(self.xStart, self.xEnd + 1)

    def ySlice(self):
        return slice(self.yStart, self.yEnd + 1)

    def xLength(self) -> int:
        return self.xEnd + 1 - self.xStart

    def yLength(self) -> int:
        return self.yEnd + 1 - self.yStart

    def size(self) -> int:
        return (self.xEnd + 1 - self.xStart) * (self.yEnd + 1 - self.yStart)

    def __str__(self):
        template = "xStart: {} | xEnd: {} | yStart: {} | yEnd: {}"
        return template.format(self.xStart, self.xEnd, self.yStart, self.yEnd)

    def __eq__(self, other):
        return self.xStart == other.xStart \
               and self.xEnd == other.xEnd \
               and self.yStart == other.yStart \
               and self.yEnd == other.yEnd


def scanForBoundaries(booleanArray, patch=None, depth=0):
    logging.debug("  " * depth + "Starting scanForBoundaries()")
    if patch is None:
        patch = Patch(0, booleanArray.shape[0] - 1, 0, booleanArray.shape[1] - 1)
    result = []
    direction = depth % 2
    subBooleanArray = booleanArray[patch.xSlice(), patch.ySlice()]
    booleanList = numpy.any(subBooleanArray, direction)
    if direction:
        length = patch.xLength()
    else:
        length = patch.yLength()
    started = False
    if length > 1:
        childPatch = copy.copy(patch)
        for i in range(length):
            if booleanList[i] and not started:
                logging.debug("  " * depth + "Found start: " + str(i))
                if direction:
                    childPatch.setXStart(patch.getXStart() + i)
                else:
                    childPatch.setYStart(patch.getYStart() + i)
                started = True
            elif not booleanList[i] and started:
                logging.debug("  " * depth + "Found stop: " + str(i - 1))
                if direction:
                    childPatch.setXEnd(patch.getXStart() + i - 1)
                else:
                    childPatch.setYEnd(patch.getYStart() + i - 1)
                started = False
                result.append(copy.copy(childPatch))
        if started:
            logging.debug("  " * depth + "Found stop at end.")
            if direction:
                childPatch.setXEnd(patch.getXEnd())
            else:
                childPatch.setYEnd(patch.getYEnd())
            result.append(childPatch)
    else:
        logging.debug("  " * depth + "Length is one")
        result.append(patch)
    logging.debug("  " * depth + "Ending scanForBoundaries()")
    return result


def findPatches(booleanArray, patch=None, depth=0, parentLength=0):
    logging.debug("  " * depth + "Starting findPatches()")
    logging.debug("  " * depth + "Direction: " + str(depth % 2))
    result = []
    patches = scanForBoundaries(booleanArray, patch, depth)
    logging.debug("  " * depth + "Found patches: " + str([patch.asArray() for patch in patches]))
    length = len(patches)
    logging.debug("  " * depth + "length: " + str(length) + "| parentLength: " + str(parentLength))
    if length == 0:
        logging.error("  " * depth + "Nothing found...")  # TODO: Throw Exception?
    elif length == 1 and parentLength == 1:
        logging.debug("  " * depth + "Done: " + str(patches[0]))
        result = patches
    else:
        logging.debug("  " * depth + "Scanning children...")
        parentLength = length
        childDepth = depth + 1
        for i in range(length):
            logging.debug("  " * depth + "Child: " + str(i))
            childPatch = patches[i]
            result += findPatches(booleanArray, childPatch, childDepth, parentLength)
    logging.debug("  " * depth + "Ending findPatches()")
    return result


def filterLargePatches(patches, threshold=1000):
    logging.debug("Starting filterLargePatches()")
    result = []
    for patch in patches:
        if patch.size() > threshold:
            result.append(patch)
    logging.debug("Ending filterLargePatches()")
    return result

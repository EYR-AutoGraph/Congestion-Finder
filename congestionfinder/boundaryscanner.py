import numpy
import matplotlib.pyplot
import matplotlib.patches


def dprint(message, depth):
    indent = "  " * depth
    return indent + str(message)


def scanForBoundaries(dataArray, boundaries = None, threshold = 1, depth = 0):
    dprint("Starting scanForBoundaries()", depth)
    if boundaries is None:
        boundaries = [0, dataArray.shape[0] - 1, 0, dataArray.shape[1] - 1]
    boundariesList = []
    subArray = dataArray[boundaries[0]:boundaries[1] + 1, boundaries[2]:boundaries[3] + 1]
    arrayBoolean = numpy.any(subArray < threshold, depth % 2)
    if depth % 2:
        length = boundaries[1] + 1 - boundaries[0]
    else:
        length = boundaries[3] + 1 - boundaries[2]
    started = False
    if length > 1:
        childBoundaries = boundaries[:]
        for i in range(length):
            if arrayBoolean[i] and not started:
                dprint("Found start: " + str(i), depth)
                if depth % 2:
                    childBoundaries[0] = boundaries[0] + i
                else:
                    childBoundaries[2] = boundaries[2] + i
                started = True
            elif not arrayBoolean[i] and started:
                dprint("Found stop: " + str(i - 1), depth)
                if depth % 2:
                    childBoundaries[1] = boundaries[0] + i - 1
                else:
                    childBoundaries[3] = boundaries[2] + i - 1
                started = False
                boundariesList.append(childBoundaries[:])
        if started:
            dprint("Found stop at end.", depth)
            if depth % 2:
                childBoundaries[1] = boundaries[1]
            else:
                childBoundaries[3] = boundaries[3]
            boundariesList.append(childBoundaries)
    else:
        dprint("Length is one", depth)
        boundariesList.append(boundaries)
    dprint("Ending scanForBoundaries()", depth)
    return boundariesList


def recursiveScanForBoundaries(dataArray, boundaries = None, depth = 0, parentLength = 0, threshold = 1): # Remove copies?
    dprint("Starting recursiveScanForBoundaries()", depth)
    dprint("Direction: " + str(depth % 2), depth)
    result = []
    boundariesList = scanForBoundaries(dataArray, boundaries, threshold, depth)
    if True:  # Add debug logger
        plotCongestionsWithBoundaries(dataArray, boundariesList)
    length = len(boundariesList)
    dprint("length: " + str(length) + "| parentLength: " + str(parentLength), depth)
    if length == 0:
        dprint("Error: nothing found...", depth) # Throw Exception?
    elif length == 1 and parentLength == 1:
        dprint("Done: " + str(boundariesList[0]), depth)
        return boundariesList
    else:
        dprint("Scanning children...", depth)
        parentLength = length
        childDepth = depth + 1
        for i in range(length):
            dprint("Child: " + str(i), depth)
            childBoundaries = boundariesList[i][:]
            result += recursiveScanForBoundaries(dataArray, childBoundaries, childDepth, parentLength, threshold)
    dprint("Ending recursiveScanForBoundaries()", depth)
    return result
def filterLargeCongestions(congestionBoundariesList):
    result = []
    for congestionBoundaries in congestionBoundariesList:
        size = (congestionBoundaries[1] - congestionBoundaries[0]) * (congestionBoundaries[3] - congestionBoundaries[2])
        if size > 1000:
            result.append(congestionBoundaries)
    return result


def addMargins(congestionBoundariesList, minSpaceIndex, maxSpaceIndex, minTimeIndex, maxTimeIndex):
    result = []
    marginSpace = 10
    marginTime = 20
    for congestionBoundaries in congestionBoundariesList:
        congestionBoundaries[0] = max(minSpaceIndex, congestionBoundaries[0] - marginSpace)
        congestionBoundaries[1] = min(maxSpaceIndex, congestionBoundaries[1] + marginSpace)
        congestionBoundaries[2] = max(minTimeIndex, congestionBoundaries[2] - marginTime)
        congestionBoundaries[3] = min(maxTimeIndex, congestionBoundaries[3] + marginTime)
        result.append(congestionBoundaries)
    return result


def addBoundaries(ax, boundaries):
    rect = matplotlib.patches.Rectangle((
        boundaries[2] - 0.5,
        boundaries[0] - 0.5),
        boundaries[3] - boundaries[2] + 1,
        boundaries[1] - boundaries[0] + 1,
        linewidth = 1,
        edgecolor = "r",
        hatch = "//",
        facecolor = "none")
    ax.add_patch(rect)


def plotCongestionsWithBoundaries(congestions, boundariesList):
    fig, ax = matplotlib.pyplot.subplots(1)
    ax.imshow(congestions, aspect = "auto")
    for i in range(len(boundariesList)):
        addBoundaries(ax, boundariesList[i])
    matplotlib.pyplot.show()

import numpy


def parseDetectionsToSpeedsAndFlows(detections, road):
    print("Starting parseDetectionsToSpeedFlows()")
    spaceToSpaceIndex = road.getSpaceToSpaceIndex()
    maxSpaceIndex = max(spaceToSpaceIndex.values()) + 1
    maxTimeIndex = 1440 # Trivial now, but perhaps important later.
    speeds = numpy.full((maxSpaceIndex, maxTimeIndex), numpy.nan, dtype=numpy.int32)
    flows = numpy.full((maxSpaceIndex, maxTimeIndex), numpy.nan, dtype=numpy.int32)
    minFoundSpaceIndex = maxSpaceIndex
    maxFoundSpaceIndex = 0
    minFoundTimeIndex = maxTimeIndex
    maxFoundTimeIndex = 0
    for detection in detections:
        space = detection.getSpace()
        time = detection.getTime()
        speed = detection.getSpeed()
        flow = detection.getFlow()
        spaceIndex = spaceToSpaceIndex[space]
        timeIndex = time  # Trivial now, but perhaps important later.
        if spaceIndex < minFoundSpaceIndex:
            minFoundSpaceIndex = spaceIndex
        if spaceIndex > maxFoundSpaceIndex:
            maxFoundSpaceIndex = spaceIndex
        if timeIndex < minFoundTimeIndex:
            minFoundTimeIndex = timeIndex
        if timeIndex > maxFoundTimeIndex:
            maxFoundTimeIndex = timeIndex
        speeds[spaceIndex, timeIndex] = speed
        flows[spaceIndex, timeIndex] = flow
    speeds = speeds[minFoundSpaceIndex:maxFoundSpaceIndex + 1, minFoundTimeIndex:maxFoundTimeIndex + 1]
    flows = flows[minFoundSpaceIndex:maxFoundSpaceIndex + 1, minFoundTimeIndex:maxFoundTimeIndex + 1]
    print("Ending parseDetectionsToSpeedFlows()")
    return speeds, flows, minFoundSpaceIndex, maxFoundSpaceIndex, minFoundTimeIndex, maxFoundTimeIndex


def removeLowFlowTimes(speeds, flows):
    print("Starting removeLowFlowTimes()")
    mask = numpy.nanmean(flows, axis=0) > 10
    speeds = speeds[:, mask]
    flows = flows[:, mask]
    print("Ending removeLowFlowTimes()")
    return speeds, flows, mask


def removeMissingDetectors(speeds, flows):
    print("Starting removeMissingDetectors()")
    mask = ~numpy.isnan(speeds).all(axis=1)
    speeds = speeds[mask]
    flows = flows[mask]
    print("Ending removeMissingDetectors()")
    return speeds, flows, mask


def writeSpeedsAndFlowsToCSV(speeds, flows, congestionBoundariesList, outputDirectory, date, roadNumber):
    for congestionBoundaries in congestionBoundariesList:
        minSpaceIndex = congestionBoundaries[0] # Index to Space
        maxSpaceIndex = congestionBoundaries[1]
        minTimeIndex = congestionBoundaries[2] # Index to Time
        maxTimeIndex = congestionBoundaries[3]
        speedsFileName = outputDirectory + "\\" + str(date) + "_" + str(roadNumber) + "_s_" + str(minSpaceIndex) + "-" + str(maxSpaceIndex) + "_" + str(minTimeIndex) + "-" + str(maxTimeIndex) + ".csv.gz"
        flowsFileName = outputDirectory + "\\" + str(date) + "_" + str(roadNumber) + "_f_" + str(minSpaceIndex) + "-" + str(maxSpaceIndex) + "_" + str(minTimeIndex) + "-" + str(maxTimeIndex) + ".csv.gz"
        boundedSpeeds = speeds[minSpaceIndex:maxSpaceIndex, minTimeIndex:maxTimeIndex]
        boundedFlows = flows[minSpaceIndex:maxSpaceIndex, minTimeIndex:maxTimeIndex]
        numpy.savetxt(speedsFileName, boundedSpeeds, fmt = "%d", delimiter = ",")
        numpy.savetxt(flowsFileName, boundedFlows, fmt = "%d", delimiter = ",")

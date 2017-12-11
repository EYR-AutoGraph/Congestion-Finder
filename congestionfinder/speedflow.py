import numpy
import logging


def parseDetectionsToSpeedsAndFlows(detections, road):
    logging.debug("Starting parseDetectionsToSpeedFlows()")
    spaceToSpaceIndex = road.getSpaceToSpaceIndex()
    maxSpaceIndex = max(spaceToSpaceIndex.values()) + 1
    maxTimeIndex = 1440 # Trivial now, but perhaps important later.
    speeds = numpy.full((maxSpaceIndex, maxTimeIndex), numpy.nan)
    flows = numpy.full((maxSpaceIndex, maxTimeIndex), numpy.nan)
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
    logging.debug("Ending parseDetectionsToSpeedFlows()")
    return speeds, flows, minFoundSpaceIndex, maxFoundSpaceIndex, minFoundTimeIndex, maxFoundTimeIndex


def removeLowFlowTimes(speeds, flows):
    logging.debug("Starting removeLowFlowTimes()")
    mask = numpy.nanmean(flows, axis=0) > 10
    speeds = speeds[:, mask]
    flows = flows[:, mask]
    logging.debug("Ending removeLowFlowTimes()")
    return speeds, flows, mask


def removeMissingDetectors(speeds, flows):
    logging.debug("Starting removeMissingDetectors()")
    mask = ~numpy.isnan(speeds).all(axis=1)
    speeds = speeds[mask]
    flows = flows[mask]
    logging.debug("Ending removeMissingDetectors()")
    return speeds, flows, mask


def writeSpeedsAndFlowsToCSV(speeds, flows, patches, outputDirectory, date, roadNumber):
    logging.debug("Starting writeSpeedsAndFlowsToCSV()")
    for patch in patches:
        minSpaceIndex = patch.getXStart()  # Index to Space
        maxSpaceIndex = patch.getXEnd()
        minTimeIndex = patch.getYStart()  # Index to Time
        maxTimeIndex = patch.getYEnd()
        speedsFileName = outputDirectory + "\\" + str(date) + "_" + str(roadNumber) + "_s_" + str(minSpaceIndex) + "-" + str(maxSpaceIndex) + "_" + str(minTimeIndex) + "-" + str(maxTimeIndex) + ".csv.gz"
        flowsFileName = outputDirectory + "\\" + str(date) + "_" + str(roadNumber) + "_f_" + str(minSpaceIndex) + "-" + str(maxSpaceIndex) + "_" + str(minTimeIndex) + "-" + str(maxTimeIndex) + ".csv.gz"
        boundedSpeeds = speeds[minSpaceIndex:maxSpaceIndex, minTimeIndex:maxTimeIndex]
        boundedFlows = flows[minSpaceIndex:maxSpaceIndex, minTimeIndex:maxTimeIndex]
        numpy.savetxt(speedsFileName, boundedSpeeds, fmt="%s", delimiter=",")
        numpy.savetxt(flowsFileName, boundedFlows, fmt="%s", delimiter=",")
    logging.debug("Ending writeSpeedsAndFlowsToCSV()")

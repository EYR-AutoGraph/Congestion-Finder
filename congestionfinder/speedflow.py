import numpy
import copy
import logging


def parseDetectionsToSpeedsAndFlows(detections, road):
    logging.debug("Starting parseDetectionsToSpeedFlows()")
    spaceToSpaceIndex = road.getSpaceToSpaceIndex()
    maxSpaceIndex = max(spaceToSpaceIndex.values()) + 1
    maxTimeIndex = 1440  # Trivial now, but perhaps important later.
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


def removeMissingDetectors(speeds, flows):
    logging.debug("Starting removeMissingDetectors()")
    mask = ~numpy.isnan(speeds).all(axis=1)
    speeds = speeds[mask]
    flows = flows[mask]
    logging.debug("Ending removeMissingDetectors()")
    return speeds, flows, mask


def removeLowFlowTimes(speeds, flows, lowFlowThreshold=10):
    logging.debug("Starting removeLowFlowTimes()")
    mask = numpy.nanmean(flows, axis=0) > lowFlowThreshold
    speeds = speeds[:, mask]
    flows = flows[:, mask]
    logging.debug("Ending removeLowFlowTimes()")
    return speeds, flows, mask


def unmaskPatches(patches, maskSpace, maskTime):
    logging.debug("Starting unmaskPatches()")
    spaceMap = numpy.nonzero(maskSpace)[0]
    timeMap = numpy.nonzero(maskTime)[0]
    result = copy.deepcopy(patches)
    for patch in result:
        patch.setXStart(spaceMap[patch.getXStart() - 1])
        patch.setXEnd(spaceMap[patch.getXEnd() - 1])
        patch.setYStart(timeMap[patch.getYStart() - 1])
        patch.setYEnd(timeMap[patch.getYEnd() - 1])
    logging.debug("Ending unmaskPatches()")
    return result


def addMargins(patches, marginSpace, marginTime, minSpaceIndex, maxSpaceIndex, minTimeIndex, maxTimeIndex):
    logging.debug("Starting addMargins()")
    result = copy.deepcopy(patches)
    for patch in result:
        patch.setXStart(max(minSpaceIndex, patch.getXStart() - marginSpace))
        patch.setXEnd(min(maxSpaceIndex, patch.getXEnd() + marginSpace))
        patch.setYStart(max(minTimeIndex, patch.getYStart() - marginTime))
        patch.setYEnd(min(maxTimeIndex, patch.getYEnd() + marginTime))
    logging.debug("Ending addMargins()")
    return result


def writeSpeedsAndFlowsToCSV(speeds, flows, patches, outputDirectory, date, road):
    logging.debug("Starting writeSpeedsAndFlowsToCSV()")
    roadNumber = road.getRoadNumber()
    spaceIndexToSpace = road.getSpaceIndexToSpace()
    for patch in patches:
        minSpaceIndex = patch.getXStart()  # Index to Space
        maxSpaceIndex = patch.getXEnd()
        minTimeIndex = patch.getYStart()  # Index to Time
        maxTimeIndex = patch.getYEnd()
        maxSpace = spaceIndexToSpace[maxSpaceIndex]
        minSpace = spaceIndexToSpace[minSpaceIndex]
        minTime = minTimeIndex  # Trivial now, but perhaps important later
        maxTime = maxTimeIndex  # Trivial now, but perhaps important later
        speedsFileName = outputDirectory + "\\" + str(date) + "_" + str(roadNumber) + "_s_" + str(minSpace) + "-" + str(maxSpace) + "_" + str(minTime) + "-" + str(maxTime) + ".csv.gz"
        flowsFileName = outputDirectory + "\\" + str(date) + "_" + str(roadNumber) + "_f_" + str(minSpace) + "-" + str(maxSpace) + "_" + str(minTime) + "-" + str(maxTime) + ".csv.gz"
        speedsPatch = speeds[minSpaceIndex:maxSpaceIndex, minTimeIndex:maxTimeIndex]
        flowsPatch = flows[minSpaceIndex:maxSpaceIndex, minTimeIndex:maxTimeIndex]
        numpy.savetxt(speedsFileName, speedsPatch, fmt="%s", delimiter=",")
        numpy.savetxt(flowsFileName, flowsPatch, fmt="%s", delimiter=",")
    logging.debug("Ending writeSpeedsAndFlowsToCSV()")

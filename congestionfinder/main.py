import logging

import congestionfinder.bpsdetector
import congestionfinder.congestion
import congestionfinder.detection
import congestionfinder.road
import congestionfinder.speedflow
import patchfinder.patch


def findCongestion(date, roadNumber, roadsFileName, detectionsFileName, outputDirectory, lowFlowThreshold,
                   speedThreshold, flowThreshold, spaceSmoothing, timeSmoothing, patchSizeThreshold, marginSpace,
                   marginTime):
    logging.debug("Starting findCongestion()")
    bpsDetectors = congestionfinder.bpsdetector.readCSVToBPSDetectors(roadsFileName)
    roads = congestionfinder.road.parseBPSDetectorsToRoads(bpsDetectors)
    road = roads[roadNumber]
    detections = congestionfinder.detection.readCSVToDetections(detectionsFileName)  # TODO: why not use the BPS code
    speeds, flows, minSpaceIndex, maxSpaceIndex, minTimeIndex, maxTimeIndex = \
        congestionfinder.speedflow.parseDetectionsToSpeedsAndFlows(detections, road)
    speedsWorkingDetectors, flowsWorkingDetectors, maskWorkingDetectors = \
        congestionfinder.speedflow.removeMissingDetectors(speeds, flows)
    speedsHighFlow, flowsHighFlow, maskHighFlow = congestionfinder.speedflow.removeLowFlowTimes(speedsWorkingDetectors,
                                                                                                flowsWorkingDetectors,
                                                                                                lowFlowThreshold)
    congestions = congestionfinder.congestion.parseSpeedFlowsToCongestions(speedsHighFlow,
                                                                           flowsHighFlow, speedThreshold,
                                                                           flowThreshold)
    congestionsWithoutMissingValues = congestionfinder.congestion.interpolateMissingValues(congestions)
    congestionsSmoothed = congestionfinder.congestion.applySmoothingFilter(congestionsWithoutMissingValues,
                                                                           spaceSmoothing, timeSmoothing)
    congestionsBoolean = congestionsSmoothed < 1
    congestionPatches = patchfinder.patch.findPatches(congestionsBoolean)
    congestionPatchesFiltered = patchfinder.patch.filterLargePatches(congestionPatches, patchSizeThreshold)
    speedFlowPatches = congestionfinder.speedflow.unmaskPatches(congestionPatchesFiltered, maskWorkingDetectors,
                                                                maskHighFlow)
    speedFlowPatchesWithMargins = congestionfinder.speedflow.addMargins(speedFlowPatches,
                                                                        marginSpace, marginTime,
                                                                        minSpaceIndex, maxSpaceIndex,
                                                                        minTimeIndex, maxTimeIndex)
    congestionfinder.speedflow.writeSpeedsAndFlowsToCSV(speeds, flows, speedFlowPatchesWithMargins,
                                                        outputDirectory, date, road)
    logging.debug("Ending findCongestion()")


if __name__ == "__main__":  # TODO: Add road direction
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler("../output.log")
    fileHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    date = "20171120"
    roadNumber = 2
    roadsFileName = "../tests/data/BPS_20171120.txt"
    detectionsFileName = "../tests/data/A2_20171120.txt"
    outputDirectory = "../tests/data"
    lowFlowThreshold = 10
    speedThreshold = 65
    flowThreshold = 40
    spaceSmoothing = 10
    timeSmoothing = 20
    patchSizeThreshold = 1000
    marginSpace = spaceSmoothing  # probably always the same
    marginTime = timeSmoothing  # probably always the same
    findCongestion(date, roadNumber, roadsFileName, detectionsFileName, outputDirectory, lowFlowThreshold,
                   speedThreshold, flowThreshold, spaceSmoothing, timeSmoothing, patchSizeThreshold, marginSpace,
                   marginTime)

import congestionfinder.bpsdetector
import congestionfinder.road
import congestionfinder.detection
import congestionfinder.speedflow
import congestionfinder.congestion
import congestionfinder.boundaryscanner
import logging


def findCongestion(date, roadNumber, roadsFileName, detectionsFileName, outputDirectory):
    logging.debug("Starting findCongestion()")
    bpsCodes = congestionfinder.bpsdetector.readCSVToBPSCodes(roadsFileName)
    roads = congestionfinder.road.parseBPSCodesToRoads(bpsCodes)
    detections = congestionfinder.detection.readCSVToDetections(detectionsFileName)
    speeds, flows, minSpaceIndex, maxSpaceIndex, minTimeIndex, maxTimeIndex = congestionfinder.speedflow.parseDetectionsToSpeedsAndFlows(
        detections, roads[roadNumber])
    speedsHighFlow, flowsHighFlow, maskHighFlow = congestionfinder.speedflow.removeLowFlowTimes(speeds,
                                                                                                flows)  ## Do something with Mask
    speedsWorkingDetectors, flowsWorkingDetectors, maskWorkingDetectors = congestionfinder.speedflow.removeMissingDetectors(
        speedsHighFlow, flowsHighFlow)  ## Do something with Mask
    congestions = congestionfinder.congestion.parseSpeedFlowsToCongestions(speedsWorkingDetectors,
                                                                           flowsWorkingDetectors)
    congestionsWithoutMissingValues = congestionfinder.congestion.interpolateMissingValues(congestions)
    congestionsSmoothed = congestionfinder.congestion.applySmoothingFilter(congestionsWithoutMissingValues)
    congestionBoundariesList = congestionfinder.boundaryscanner.recursiveScanForBoundaries(congestionsSmoothed)
    congestionBoundariesListFiltered = congestionfinder.boundaryscanner.filterLargeCongestions(congestionBoundariesList)
    congestionBoundariesListWithMargins = congestionfinder.boundaryscanner.addMargins(congestionBoundariesListFiltered,
                                                                                      minSpaceIndex, maxSpaceIndex,
                                                                                      minTimeIndex, maxTimeIndex)
    congestionfinder.speedflow.writeSpeedsAndFlowsToCSV(speeds, flows, congestionBoundariesListWithMargins,
                                                        outputDirectory, date, roadNumber)
    logging.debug("Ending findCongestion()")


if __name__ == "__main__":
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
    findCongestion(date, roadNumber, roadsFileName, detectionsFileName, outputDirectory)

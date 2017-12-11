import numpy
import scipy.interpolate
import scipy.ndimage
import matplotlib.pyplot
import matplotlib.patches
import logging


def parseSpeedFlowsToCongestions(speeds, flows):
    logging.debug("Starting parseSpeedFlowsToCongestions()")
    congestions = speeds / 65  # + flows / 40
    logging.debug("Ending parseSpeedFlowsToCongestions()")
    return congestions


def interpolateMissingValues(congestions):
    logging.debug("Starting interpolateMissingValues()")
    x = numpy.arange(0, congestions.shape[1])
    y = numpy.arange(0, congestions.shape[0])
    congestionsMask = numpy.ma.masked_invalid(congestions)
    xx, yy = numpy.meshgrid(x, y)
    x1 = xx[~congestionsMask.mask]
    y1 = yy[~congestionsMask.mask]
    newarr = congestions[~congestionsMask.mask]
    congestions = scipy.interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method = "cubic")
    logging.debug("Ending interpolateMissingValues()")
    return congestions


def applySmoothingFilter(congestions):
    logging.debug("Starting applySmoothingFilter()")
    # congestions = scipy.ndimage.filters.gaussian_filter(congestions, 5)
    congestions = scipy.ndimage.filters.uniform_filter(congestions, [10, 20])
    logging.debug("Ending applySmoothingFilter()")
    return congestions


def filterLargeCongestions(patches, threshold=1000):
    logging.debug("Starting filterLargeCongestions()")
    result = []
    for patch in patches:
        if patch.size() > threshold:
            result.append(patch)
    logging.debug("Ending filterLargeCongestions()")
    return result


def addMargins(patches, marginSpace, marginTime, minSpaceIndex, maxSpaceIndex, minTimeIndex, maxTimeIndex):
    for patch in patches:
        patch.setXStart(max(minSpaceIndex, patch.getXStart() - marginSpace))
        patch.setXEnd(min(maxSpaceIndex, patch.getXEnd() + marginSpace))
        patch.setYStart(max(minTimeIndex, patch.getYStart() - marginTime))
        patch.setYEnd(min(maxTimeIndex, patch.getYEnd() + marginTime))
    return patches


def addBoundaries(ax, boundaries):
    rect = matplotlib.patches.Rectangle((
        boundaries[2] - 0.5,
        boundaries[0] - 0.5),
        boundaries[3] - boundaries[2] + 1,
        boundaries[1] - boundaries[0] + 1,
        linewidth=1,
        edgecolor="r",
        hatch="//",
        facecolor="none")
    ax.add_patch(rect)


def plotCongestionsWithBoundaries(congestions, patches):
    congestionBoundariesList = patches.getPatches()
    fig, ax = matplotlib.pyplot.subplots(1)
    ax.imshow(congestions, aspect = "auto")
    for i in range(len(congestionBoundariesList)):
        addBoundaries(ax, congestionBoundariesList[i])
    matplotlib.pyplot.show()

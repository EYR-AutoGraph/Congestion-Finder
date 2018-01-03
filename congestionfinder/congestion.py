import numpy
import scipy.interpolate
import scipy.ndimage
import matplotlib.pyplot
import matplotlib.patches
import logging


def parseSpeedFlowsToCongestions(speeds, flows, speedThreshold, flowThreshold):
    logging.debug("Starting parseSpeedFlowsToCongestions()")
    congestions = speeds / speedThreshold  # + flows / flowThreshold
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
    congestionsMasked = congestions[~congestionsMask.mask]
    congestions = scipy.interpolate.griddata((x1, y1), congestionsMasked.ravel(), (xx, yy), method="cubic")
    logging.debug("Ending interpolateMissingValues()")
    return congestions


def applySmoothingFilter(congestions, spaceSmoothing, timeSmoothing):
    logging.debug("Starting applySmoothingFilter()")
    # congestions = scipy.ndimage.filters.gaussian_filter(congestions, 5)
    congestions = scipy.ndimage.filters.uniform_filter(congestions, [spaceSmoothing, timeSmoothing])
    logging.debug("Ending applySmoothingFilter()")
    return congestions


def addBoundaries(ax, patch):
    rect = matplotlib.patches.Rectangle((
        patch.getYStart() - 0.5,
        patch.getXStart() - 0.5),
        patch.yLength(),
        patch.xLength(),
        linewidth=1,
        edgecolor="r",
        hatch="//",
        facecolor="none")
    ax.add_patch(rect)


def plotCongestionsWithPatches(congestions, patches):  # TODO: move to docs/utils?
    fig, ax = matplotlib.pyplot.subplots(1)
    ax.imshow(congestions, aspect="auto")
    for patch in patches:
        addBoundaries(ax, patch)
    matplotlib.pyplot.show()

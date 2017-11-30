import numpy
import scipy
import matplotlib


def parseSpeedFlowsToCongestions(speeds, flows):
    print("Starting parseSpeedFlowsToCongestions()")
    congestions = speeds / 65# + flows / 40
    print("Ending parseSpeedFlowsToCongestions()")
    return congestions


def interpolateMissingValues(congestions):
    print("Starting interpolateMissingValues()")
    x = numpy.arange(0, congestions.shape[1])
    y = numpy.arange(0, congestions.shape[0])
    congestionsMask = numpy.ma.masked_invalid(congestions)
    xx, yy = numpy.meshgrid(x, y)
    x1 = xx[~congestionsMask.mask]
    y1 = yy[~congestionsMask.mask]
    newarr = congestions[~congestionsMask.mask]
    congestions = scipy.interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method = "cubic")
    print("Ending interpolateMissingValues()")
    return congestions


def applySmoothingFilter(congestions):
    print("Starting applySmoothingFilter()")
    #congestions = scipy.ndimage.filters.gaussian_filter(congestions, 5)
    congestions = scipy.ndimage.filters.uniform_filter(congestions, [10, 20])
    print("Ending applySmoothingFilter()")
    return congestions


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

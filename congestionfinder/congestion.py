import numpy
import scipy.interpolate
import scipy.ndimage


def parseSpeedFlowsToCongestions(speeds, flows):
    print("Starting parseSpeedFlowsToCongestions()")
    congestions = speeds / 65  # + flows / 40
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
    # congestions = scipy.ndimage.filters.gaussian_filter(congestions, 5)
    congestions = scipy.ndimage.filters.uniform_filter(congestions, [10, 20])
    print("Ending applySmoothingFilter()")
    return congestions

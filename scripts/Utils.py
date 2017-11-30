import datetime

def dprint(objectToPrint, depth = 0): # TODO: replace with Logger
    indent = "  " * depth
    if True:
        print(indent + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " | " + str(objectToPrint))

def extractAttribute(bpsCode, startBit, endBit):
    return int(bpsCode, 16) >> (80 - endBit) & int("1" * (endBit - startBit), 2)
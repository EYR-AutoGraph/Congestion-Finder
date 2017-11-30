class Detection:
    code = None
    space = None
    time = None
    speed = None
    flow = None

    def __init__(self, code, space, time, speed, flow):
        self.code = code
        self.space = space
        self.time = time
        self.speed = speed
        self.flow = flow

    @property
    def getCode(self):
        return self.code

    @property
    def getSpace(self):
        return self.space

    @property
    def getTime(self):
        return self.time

    @property
    def getSpeed(self):
        return self.speed

    @property
    def getFlow(self):
        return self.flow

    @property
    def __str__(self):
        stringTemplate = "code: {} | space: {} | time: {} | speed: {} | flow: {}"
        templateElements = [self.code, self.space, self.time, self.speed, self.flow]
        return stringTemplate.format(templateElements)

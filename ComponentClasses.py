class ComponentNode:
    def __init__(self, voltage=0.0):
        self.__voltage = voltage

    def updateVoltage(self, newVoltage):
        self.__voltage = newVoltage

    def getVoltage(self):
        return self.__voltage


class SourceNode(ComponentNode):
    def __init__(self):
        super().__init__(5.0)


class GroundNode(ComponentNode):
    def __init__(self):
        super().__init__()


class Wire:
    def __init__(self):
        self.__current = 0.0
        self.__potentialDiff = 0.0

    def updateCurrent(self, newC):
        self.__current = newC

    def getCurrent(self):
        print(self.__current)

class Resistor(Wire):
    def __init__(self):
        super().__init__()
        self.__resistance = 5.0

    def getResistance(self):
        return self.__resistance


    def setResistance(self, newR):
        self.__resistance = newR


def objectGetVoltage(object):
    return object.getVoltage()

def objectGetResistance(object):
    return object.getResistance()

def objectGetCurrent(object):
    return object.getCurrent()
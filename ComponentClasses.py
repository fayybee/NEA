class ComponentNode:
    def __init__(self, voltage=0.0):
        self.__potential = voltage

    def updateVoltage(self, newVoltage):
        self.__potential = newVoltage

    def getVoltage(self):
        return self.__potential


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
        return self.__current

    def getVoltage(self):
        return self.__potentialDiff

    def updateVoltage(self, newV):
        self.__potentialDiff = newV


class Resistor(Wire):
    def __init__(self):
        super().__init__()
        self.__resistance = 5.0

    def getResistance(self):
        return self.__resistance

    def setResistance(self, newR):
        self.__resistance = newR


# functions for using getters from other modules to avoid importing the whole module
def objectGetVoltage(componentObject):
    return componentObject.getVoltage()


def objectGetResistance(componentObject):
    return componentObject.getResistance()


def objectSetCurrent(componentObject, newC):
    componentObject.updateCurrent(newC)


def objectGetCurrent(componentObject):
    return componentObject.getCurrent()


def objectSetVoltage(componentObject, newV):
    componentObject.updateVoltage(newV)

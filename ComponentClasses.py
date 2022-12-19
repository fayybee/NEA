class ComponentNode:
    def __init__(self, voltage=0.0):
        self._potential = voltage

    def updateVoltage(self, newVoltage):
        self._potential = newVoltage

    def getVoltage(self):
        return self._potential


class SourceNode(ComponentNode):
    def __init__(self):
        super().__init__(5.0)


class GroundNode(ComponentNode):
    def __init__(self):
        super().__init__()


class Wire:
    def __init__(self):
        self._current = 0.0
        self._potentialDiff = 0.0

    def updateCurrent(self, newC):
        self._current = newC

    def getCurrent(self):
        return self._current

    def getVoltage(self):
        return self._potentialDiff

    def updateVoltage(self, newV):
        self._potentialDiff = newV


class Resistor(Wire):
    def __init__(self):
        super().__init__()
        self._resistance = 5.0

    def getResistance(self):
        return self._resistance

    def setResistance(self, newR):
        self._resistance = newR


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

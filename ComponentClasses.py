#FIXME make overarching object as mny have same attributes

class ComponentNode:
    def __init__(self, voltage=None, isWireLike=True, isVariable=True):
        self._potential = voltage
        self._isWireLike = isWireLike
        self._isVariable = isVariable

    def updateVoltage(self, newVoltage):
        self._potential = newVoltage

    def getVoltage(self):
        return self._potential

    def isWireLike(self):
        return self._isWireLike

    def isVariable(self):
        return self._isVariable


class SourceNode(ComponentNode):
    def __init__(self):
        super().__init__(5.0,isVariable=False)


class GroundNode(ComponentNode):
    def __init__(self):
        super().__init__(0.0,isVariable=False)


class Wire:
    def __init__(self, isWireLike=True):
        self._current = 0.0
        self._potentialDiff = 0.0
        self._isWireLike = isWireLike
        self._isVariable = True

    def updateCurrent(self, newC):
        self._current = newC

    def getCurrent(self):
        return self._current

    def getVoltage(self):
        return self._potentialDiff

    def updateVoltage(self, newV):
        self._potentialDiff = newV

    def isWireLike(self):
        return self._isWireLike

    def isVariable(self):
        return self._isVariable

class Resistor(Wire):
    def __init__(self):
        super().__init__(isWireLike=False)
        self._resistance = 5.0

    def getResistance(self):
        return self._resistance

    def setResistance(self, newR):
        self._resistance = newR



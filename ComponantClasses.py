class Component:
    def __init__(self, isVariable=True, isEdgy=False, isWire=False):
        self._isVariable = isVariable
        self.__edgy = isEdgy
        self.__isWire = isWire

    def isVariable(self):
        return self._isVariable

    def isEdgy(self):
        return self.__edgy

    def isWire(self):
        return self.__isWire


###


class Join(Component):
    def __init__(self, voltage=None, isVariable=True, isSource=False):
        super().__init__(isVariable)
        self.__potential = voltage
        self.__node = None
        self.__isSource = isSource

    def updatePotential(self, newVoltage):
        self.__potential = newVoltage

    def getPotential(self):
        return self.__potential

    def assignNode(self, node):
        self.__node = node

    def getAssignedNode(self):
        return self.__node

    def isSource(self):
        return self.__isSource


class Source(Join):
    def __init__(self):
        super().__init__(5.0, False, True)


class Ground(Join):
    def __init__(self):
        super().__init__(0.0, False)


###


class Conductor(Component):
    def __init__(self, resistance=0.000001, isVariable=False, isWire=True):
        super().__init__(isVariable, True, isWire)
        self.__current = 0.0
        self.__potentialDiff = 0.0
        self.__resistance = resistance

    def updateCurrent(self, newC):
        self.__current = newC

    def getCurrent(self):
        return self.__current

    def getPotentialDifference(self):
        return self.__potentialDiff

    def updatePotentialDifference(self, newV):
        self.__potentialDiff = newV

    def getResistance(self):
        return self.__resistance

    def setResistance(self, newR):
        if self._isVariable:
            self.__resistance = newR


class Resistor(Conductor):
    def __init__(self):
        super().__init__(5, True, False)

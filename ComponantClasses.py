class Component:
    def __init__(self, isVariable=True, isEdgy=False):
        self.__isVariable = isVariable
        self.__edgy = isEdgy

    def isVariable(self):
        return self.__isVariable

    def isEdgy(self):
        return self.__edgy


###


class Join(Component):
    def __init__(self, voltage=None, isVariable=True):
        super().__init__(isVariable)
        self.__potential = voltage
        self.__node = None

    def updatePotential(self, newVoltage):
        self.__potential = newVoltage

    def getPotential(self):
        return self.__potential

    def assignNode(self, node):
        self.__node = node

    def getAssignedNode(self):
        return self.__node


class Source(Join):
    def __init__(self):
        super().__init__(5.0, False)


class Ground(Join):
    def __init__(self):
        super().__init__(0.0, False)


###


class Conductor(Component):
    def __init__(self, resistance=0.000001, isVariable=False, isWire=True):
        super().__init__(isVariable, True)
        self.__current = 0.0
        self.__potentialDiff = 0.0
        self.__resistance = resistance
        self.__isWire = isWire

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
        if self.__isVariable:
            self.__resistance = newR

    def isWire(self):
        return self.__isWire


class Resistor(Conductor):
    def __init__(self):
        super().__init__(5, True, False)

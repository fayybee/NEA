class Component:
    def __init__(self, isVariable=True):
        self.__isVariable = isVariable

    def isVariable(self):
        return self.__isVariable


###


class Join(Component):
    def __init__(self, voltage=None, isVariable=True):
        super().__init__(isVariable)
        self.__potential = voltage
        self.__isNosey = True
        self.__node = None

    def updatePotential(self, newVoltage):
        self.__potential = newVoltage

    def getPotential(self):
        return self.__potential

    def isNosey(self):
        return self.__isNosey

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
    def __init__(self, resistance=0.000001, isVariable=False):
        super().__init__(isVariable)
        self.__current = 0.0
        self.__potentialDiff = 0.0
        self.__resistance = resistance
        self.__isEdgy = True

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

    def isEdgy(self):
        return self.__isEdgy


class Resistor(Conductor):
    def __init__(self):
        super().__init__(5, True)

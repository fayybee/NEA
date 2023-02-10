class Join:
    def __init__(self, voltage=None, isVariable=True):
        self.__potential = voltage
        self.__isVariable = isVariable

    def updateVoltage(self, newVoltage):
        self.__potential = newVoltage

    def getVoltage(self):
        return self.__potential

    def isVariable(self):
        return self.__isVariable


class Source(Join):
    def __init__(self):
        super().__init__(5.0, False)


class Ground(Join):
    def __init__(self):
        super().__init__(0.0, False)


###

class Component:
    def __init__(self, resistance=0.000001, isVariable=False):
        self.__current = 0.0
        self.__potentialDiff = 0.0
        self.__isVariable = isVariable
        self.__resistance = resistance

    def updateCurrent(self, newC):
        self.__current = newC

    def getCurrent(self):
        return self.__current

    def getVoltage(self):
        return self.__potentialDiff

    def updateVoltage(self, newV):
        self.__potentialDiff = newV

    def isVariable(self):
        return self.__isVariable

    def getResistance(self):
        return self.__resistance

    def setResistance(self, newR):
        if self.__isVariable:
            self.__resistance = newR


class Resistor(Component):
    def __init__(self):
        super().__init__(5, True)

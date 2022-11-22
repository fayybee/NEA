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
        ComponentNode.__init__(self)

    def getVoltage(self):
        return 0.0


class Wire:
    def __init__(self):
        self.__current = 0.0

    def updateCurrent(self, newC):
        self.__current = newC

    def getCurrent(self):
        print(self.__current)


class Resistor(Wire):
    def __init__(self):
        super().__init__()
        self.__resistance = 5.0

    def getResistance(self):
        print(self.__resistance)

    def setResistance(self, newR):
        self.__resistance = newR


resistor = Resistor()
resistor.getResistance()

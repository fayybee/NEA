class Component:  # overarching class, all objects are children of this class
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
        return round(self.__potential,5)

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
    def __init__(self, resistance=0.00014, isVariable=True, isWire=True):
        # resistance default is typical of a 10cm 3mm diameter piece of copper wire
        super().__init__(isVariable, True, isWire)
        self.__current = 0.0
        self.__potentialDiff = 0.0
        self.__referenceResistance = resistance  # original resistance of an un adjusted component
        self.__referenceResistanceProportion = 1  # the amount the component has been changed by (proportion)
        self.__resistance = resistance

    def updateCurrent(self, newC):
        self.__current = newC

    def getCurrent(self):
        return round(self.__current, 5)

    def getPotentialDifference(self):
        return round(self.__potentialDiff, 5)

    def updatePotentialDifference(self, newV):
        self.__potentialDiff = newV

    def getResistanceProportion(self):
        return round(self.__referenceResistanceProportion, 1)

    def getResistance(self):
        return round(self.__resistance, 5)

    def setResistance(self, newR):
        if self._isVariable:
            self.__referenceResistanceProportion = newR
            self.__resistance = self.__referenceResistance * newR
            # uses proportions to find resistance rather then just setting it to a value
            # this allows for resistance of a wire to be quickly changed without having to make a new class
            # this would result in the function "setResistance" being overwritten to include the equation
            # pL/A = R
            # where p is resistivity of the wire L is length A is area and R is resistance


class Resistor(Conductor):
    def __init__(self):
        super().__init__(1, True, False)

class Component:  # overarching class, all objects are children of this class
    def __init__(self, isVariable=True, isEdgy=False, isWire=False):
        self._isVariable = isVariable  # determines if the component can be varied or not so non-variable types do
        # not have their values overwritten by accident
        self.__edgy = isEdgy  # determines if the component acts like an edge or not
        self.__isWire = isWire

    def isVariable(self):
        return self._isVariable

    def isEdgy(self):
        return self.__edgy

    def isWire(self):
        return self.__isWire


###


class Join(Component):  # node type component (all children are also node types)
    def __init__(self, voltage=None, isVariable=True, isSource=False):
        super().__init__(isVariable)
        self.__potential = voltage
        self.__node = None  # will hold the node object assigned to it when solving the graph
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


class Conductor(Component):  # edge type component (children are also edge type)
    def __init__(self, resistance=0.00014, isVariable=True, isWire=True):
        # default resistance is typical of a 10cm 3mm diameter piece of copper wire
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
        return round(self.__referenceResistanceProportion, 1)  # needed to deal with rounding errors

    def getResistance(self):
        return round(self.__resistance, 5)

    def setResistance(self, newR):
        if self._isVariable:
            self.__referenceResistanceProportion = newR
            self.__resistance = self.__referenceResistance * newR
            # this uses proportions to find resistance thus allowing the class to represent changes in both
            # resistance of a component and resistivity of a wire (polymorphism)
            # using pL/A = R where p is resistivity of the wire L is length A is area and R is resistance R
            # is directly proportional to p so increasing p by a factor also increasing R by the same factor (L and A
            # don't change)


class Resistor(Conductor):
    def __init__(self):
        super().__init__(1, True, False)
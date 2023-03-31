import math


class Component:  # overarching class, all objects are children of this class
    def __init__(self, isVariable=True, isEdgy=False, componentType="node"):
        self._isVariable = isVariable  # determines if the component can be varied or not so non-variable types do
        # not have their values overwritten by accident
        self.__edgy = isEdgy  # determines if the component acts like an edge or not
        self.__componentType = componentType

    def isVariable(self):
        return self._isVariable

    def isEdgy(self):
        return self.__edgy

    def getComponentType(self):
        return self.__componentType


###


class Join(Component):  # node type component (all children are also node types)
    def __init__(self, voltage=None, isVariable=True, isSource=False, componentType="join"):
        super().__init__(isVariable, False, componentType)
        self.__potential = voltage
        self.__node = None  # will hold the node object assigned to it when solving the graph
        self.__isSource = isSource

    def updatePotential(self, newVoltage):
        self.__potential = newVoltage

    def getPotential(self):
        return round(self.__potential, 5)

    def assignNode(self, node):
        self.__node = node

    def getAssignedNode(self):
        return self.__node

    def isSource(self):
        return self.__isSource


class Source(Join):
    def __init__(self):
        super().__init__(5.0, False, True, "source")


class Ground(Join):
    def __init__(self):
        super().__init__(0.0, False,False,"ground")


###


class Conductor(Component):  # edge type component (children are also edge type)
    def __init__(self, isVariable=True, componentType="wire", isOhmic=True):
        # default resistance is typical of a 10cm 3mm diameter piece of copper wire
        super().__init__(isVariable, True, componentType)
        # protected used rather then private so children can access
        self._current = 0.0
        self._potentialDiff = 0.0
        self.__isOhmic = isOhmic

    def updateCurrent(self, newC):
        self._current = newC

    def getCurrent(self):
        return round(self._current, 5)

    def getPotentialDifference(self):
        return round(self._potentialDiff, 5)

    def updatePotentialDifference(self, newV):
        self._potentialDiff = newV

    def isOhmic(self):
        return self.__isOhmic


class OhmicConductor(Conductor):
    def __init__(self, resistance, isVariable, componentType):
        super().__init__(resistance, isVariable, componentType)
        self.__referenceResistance = resistance  # original resistance of an un adjusted component
        self.__referenceResistanceProportion = 1  # the amount the component has been changed by (proportion)
        self.__resistance = resistance

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


class Resistor(OhmicConductor):
    def __init__(self):
        super().__init__(1, True, "resistor")


class Wire(OhmicConductor):
    def __init__(self):
        super().__init__(0.00014, True, "wire")


class Diode(Conductor):
    def __init__(self):
        super().__init__(True, "diode", False)
        self.__factor = 1
        self.__resistance = 1000000

    def setFactor(self, newF):
        self.__factor = newF

    def getFactor(self):
        return round(self.__factor,1)

    def setResistance(self, newR):
        print("setting R", newR)
        self.__resistance = newR

    def getResistance(self):
        return round(self.__resistance,5)

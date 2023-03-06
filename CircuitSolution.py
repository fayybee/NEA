from ComponantClasses import *

minimumVoltageChange = 0.00001


class CircuitGraph:
    def __init__(self, CircuitGrid):
        self.__listNodes = {}
        self.__listEdges = {}
        self.__circuitGrid = CircuitGrid
        self.__circuitGridRows = len(self.__circuitGrid)
        self.__circuitGridCols = len(self.__circuitGrid[1])

    def findNodes(self):
        for row in range(self.__circuitGridRows):
            for col in range(self.__circuitGridCols):
                component = self.__circuitGrid[row][col]
                if component is not None and not component.isEdgy():  # makes sure position isn't empty then checks to
                    # see if its a node
                    voltage = None
                    if not component.isVariable():
                        # if the component is not variable the assigned potential must stay the same
                        voltage = component.getPotential()
                        # voltage is equal to potential of the non variable component
                    newNode = Node(voltage)
                    # makes a graph node and if voltage is not None then the node voltage will be fixed
                    self.__listNodes[(row, col)] = newNode
                    # adds the node to a dictionary with corresponding grid position as key
                    component.assignNode(newNode)  # assigns the node to the component object for safe keeping

    def findEdges(self):
        for row in range(self.__circuitGridRows):
            for col in range(self.__circuitGridCols):
                component = self.__circuitGrid[row][col]
                if component is not None:
                    try:
                        if row % 2 == 0 and col % 2 == 1:
                            inputNode = self.__circuitGrid[row][col - 1].getAssignedNode()
                            outputNode = self.__circuitGrid[row][col + 1].getAssignedNode()
                        elif row % 2 == 1 and col % 2 == 0:
                            inputNode = self.__circuitGrid[row - 1][col].getAssignedNode()
                            outputNode = self.__circuitGrid[row + 1][col].getAssignedNode()
                        else:
                            continue
                        self.__listEdges[row, col] = Edge(inputNode, outputNode, component)
                    except:
                        print("brother your circuit is incomplete")

    def solveGraph(self):
        self.findNodes()
        self.findEdges()
        while any((not node.isStable()) for node in self.__listNodes.values()):  # .values returns a list of values in
            # the dictionary as a list
            # while any node in the dictionary is unstable do the solve loop
            for node in self.__listNodes.values():
                if not node.isFixed():
                    numerator = 0.0
                    denominator = 0.0
                    for edge in node.getEdges():
                        otherEdge = edge.getOtherNode(node)
                        voltage = otherEdge.getVoltage()
                        resistance = edge.getResistance()
                        denominator += 1 / resistance
                        numerator += voltage / resistance
                        # takes the voltage of the node either side of the current node and uses it
                        # to calculate the voltage estimate of the current node based on the resistance between
                    node.setVoltageEstimate(
                        numerator / denominator)  # resistance cancels out and whats left is a guess of the voltage
                    # based on node before and after (like an average)
            for node in self.__listNodes.values():
                node.updateVoltage()
        self.updateComponentObjects()

    def updateComponentObjects(self):
        for key, node in self.__listNodes.items():
            row, col = key[0], key[1]
            component = self.__circuitGrid[row][col]
            component.updatePotential(round(node.getVoltage(), 3))
        for key, edge in self.__listEdges.items():
            row, col = key[0], key[1]
            component = self.__circuitGrid[row][col]
            component.updatePotentialDifference(round(edge.getPD(), 3))
            component.updateCurrent(round((float(edge.getPD()) / float(edge.getResistance())), 3))

    def cleanAll(self):
        self.__listNodes.clear()
        self.__listEdges.clear()


###


class Node:
    def __init__(self, vFixed=None):
        self.__edges = []
        self.__resistance = 0
        self.__stable = False
        self.__voltageEstimate = 0.0  # holds the calculated voltage for each iteration until the whole circuit has
        # been calculated so that all calculations are made off values from the same iteration
        if vFixed is not None:
            self.__voltage = vFixed
            self.__stable = True  # if the node is a fixed voltage it is stable
        else:
            self.__voltage = 0.0
        self.__fixedVoltage = vFixed

    def setFixedVoltage(self, voltage):
        assert self.__fixedVoltage is None, "Assigning a second fixed voltage to a node"  # error checking
        self.__fixedVoltage = voltage
        self.__voltage = voltage
        self.__stable = True

    def getVoltage(self):
        return float(self.__voltage)

    def updateVoltage(self):
        if self.isFixed():
            return
        if abs(self.__voltage - self.__voltageEstimate) < minimumVoltageChange:
            # because of the nature of the main equation voltage estimates can continue to fluctuate and never stabilise
            # to prevent this there is a minimum amount of change considered stable
            self.__stable = True
        else:
            self.__stable = False
        self.__voltage = self.__voltageEstimate

    def setVoltageEstimate(self, estimate):
        self.__voltageEstimate = estimate

    def addEdge(self, newEdge):
        self.__edges.append(newEdge)

    def isStable(self):
        return self.__stable

    def isFixed(self):
        return self.__fixedVoltage is not None  # returns true if fixed voltage isn't none else return false

    def getEdges(self):
        return self.__edges


class Edge:
    def __init__(self, inputNode, outputNode, circuitGridContents):
        self.__resistance = circuitGridContents.getResistance()
        self.__inputNode = inputNode
        self.__outputNode = outputNode
        inputNode.addEdge(self)
        outputNode.addEdge(self)

    def getOtherNode(self, askingNode):
        if askingNode == self.__outputNode:
            return self.__inputNode
        return self.__outputNode

    def getResistance(self):
        return self.__resistance

    def getPD(self):
        return self.__inputNode.getVoltage() - self.__outputNode.getVoltage()

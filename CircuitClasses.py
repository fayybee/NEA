from ComponentClasses import objectGetVoltage, objectGetResistance, objectSetVoltage, objectSetCurrent

minimumVoltageChange = 0.001


class CircuitGraph:
    def __init__(self, CircuitGrid):
        self.__listNodes = {}
        self.__listEdges = {}
        self.__circuitGrid = CircuitGrid
        for row in range(len(self.__circuitGrid)):  # FIXME optimising steps
            for column in range(len(self.__circuitGrid[row])):
                if self.__circuitGrid[row][column] is not None:
                    if row % 2 == 0 and column % 2 == 0:
                        voltage = None
                        if self.__circuitGrid[row][column][0] == "+" or self.__circuitGrid[row][column][0] == "-":
                            voltage = objectGetVoltage(self.__circuitGrid[row][column][1])
                        self.__listNodes[(row, column)] = Node(voltage)
        for row in range(len(self.__circuitGrid)):  # FIXME optimising steps
            for column in range(len(self.__circuitGrid[row])):
                if self.__circuitGrid[row][column] is not None:
                    try:
                        if row % 2 == 0 and column % 2 == 1:
                            inputNode = self.__listNodes[(row, column - 1)]
                            outputNode = self.__listNodes[(row, column + 1)]
                        elif row % 2 == 1 and column % 2 == 0:
                            inputNode = self.__listNodes[(row - 1, column)]
                            outputNode = self.__listNodes[(row + 1, column)]
                        else:
                            continue
                        self.__listEdges[(row, column)] = Edge(inputNode, outputNode, CircuitGrid[row][column])
                    except:
                        print("circuit not complete")

    def solveGraph(self):  # FIXME is calculating incorrect values
        while any((not node.isStable()) for node in
                  self.__listNodes.values()):  # while any of the nodes are not stable do loop
            for node in self.__listNodes.values():
                if not node.isFixed():
                    numerator = 0.0
                    denominator = 0.0
                    for edge in node.getEdges():
                        other = edge.getOtherNode(node)
                        v = other.getVoltage()
                        r = edge.getResistance()
                        denominator += 1.0 / r
                        numerator += v / r
                        # takes the voltage of the node either side of the current and uses it
                        # to calculate the voltage estimate of the current node
                    node.setVoltageEstimate(numerator / denominator)
            for node in self.__listNodes.values():
                # once all nodes have been estimated it sets the new voltages (repeats until all nodes are stable)
                node.updateVoltage()
        self.updateComponentObjects()

    def updateComponentObjects(self):
        # updating the component object in the grid so they can be accessed with the select tool
        for key, node in self.__listNodes.items():
            row, column = key[0], key[1]
            if self.__circuitGrid[row][column][0] != "+" and self.__circuitGrid[row][column][0] != "-":  # just to
                # make sure the source and ground cannot be overwritten if they were calculated wrong
                objectSetVoltage(self.__circuitGrid[row][column][1], round(node.getVoltage(), 3))
        for key, edge in self.__listEdges.items():
            row, column = key[0], key[1]
            objectSetVoltage(self.__circuitGrid[row][column][1], round(edge.getPD(), 3))
            objectSetCurrent(self.__circuitGrid[row][column][1], round((float(edge.getPD()) / float(edge.getResistance())), 3))

    def listNodes(self):  # for debugging, used in tkinter front end
        for key, node in self.__listNodes.items():
            print("Dict entry:", key, "=", node.getVoltage())

    def cleanUpAll(self):
        self.__listNodes.clear()
        self.__listEdges.clear()


class Node:
    def __init__(self, vFixed=None):
        self.__edges = []
        self.__resistance = 0
        self.__stable = False
        self.__voltageEstimate = 0.0
        if vFixed is not None:
            self.__voltage = vFixed
            self.__stable = True
        else:
            self.__voltage = 0.0
        self.__fixedVoltage = vFixed

    def getVoltage(self):
        return float(self.__voltage)

    def updateVoltage(self):
        if self.isFixed():
            return
        if abs(self.__voltage - self.__voltageEstimate) < minimumVoltageChange:
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
        if circuitGridContents[0] == "wire":
            self.__resistance = 0.000001
        else:
            self.__resistance = objectGetResistance(circuitGridContents[1])
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

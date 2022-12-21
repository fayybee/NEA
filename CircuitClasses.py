import ComponentClasses

minimumVoltageChange = 0.001


class CircuitGraph:
    def __init__(self, CircuitGrid):
        self.__listNodes = {}
        self.__listEdges = {}
        self.__circuitGrid = CircuitGrid
        self.findNodeConnections()
        # for row in range(len(self.__circuitGrid)):
        #     for col in range(len(self.__circuitGrid[row])):
        #         if self.__circuitGrid[row][col] is not None:
        #             if row % 2 == 0 and col % 2 == 0:
        #                 voltage = None
        #                 if self.__circuitGrid[row][col][0] == "+" or self.__circuitGrid[row][col][0] == "-":
        #                     voltage = objectGetVoltage(self.__circuitGrid[row][col][1])
        #                 self.__listNodes[(row, col)] = Node(voltage)
        self.findEdges(CircuitGrid)

    def findEdges(self, CircuitGrid):
        for row in range(len(self.__circuitGrid)):  # FIXME optimising steps
            for col in range(len(self.__circuitGrid[row])):
                if self.__circuitGrid[row][col] is not None:
                    if self.__circuitGrid[row][col].isWireLike():
                        continue
                    try:
                        if row % 2 == 0 and col % 2 == 1:
                            inputNode = self.__circuitGrid[row][col - 1].node
                            outputNode = self.__circuitGrid[row][col + 1].node
                        elif row % 2 == 1 and col % 2 == 0:
                            inputNode = self.__circuitGrid[row - 1][col].node
                            outputNode = self.__circuitGrid[row + 1][col].node
                        else:
                            continue
                        self.__listEdges[(row, col)] = Edge(inputNode, outputNode, CircuitGrid[row][col])
                    except:
                        print("circuit not complete")

    def findNodeConnections(self):
        for row in range(len(self.__circuitGrid)):
            for col in range(len(self.__circuitGrid[row])):
                cellValue = self.__circuitGrid[row][col]
                if cellValue is not None:
                    cellValue.node = None
        for row in range(len(self.__circuitGrid)):
            for col in range(len(self.__circuitGrid[row])):
                cellValue = self.__circuitGrid[row][col]
                if cellValue is None:
                    continue
                if cellValue.isWireLike() and cellValue.node is None:
                    try:
                        voltage = cellValue.getVoltage()
                    except:
                        voltage = None
                    self.__listNodes[(row, col)] = Node(voltage)
                    self.connect(row, col, self.__listNodes[(row, col)])

    def connect(self, row, col, node):
        if row < 0 or col < 0 or row > len(self.__circuitGrid) or col > len(self.__circuitGrid[row]):
            return
        cellValue = self.__circuitGrid[row][col]
        if cellValue is not None:
            return
        if not cellValue.isWireLike():
            return
        cellValue.node = node
        self.connect(row - 1, col, node)
        self.connect(row + 1, col, node)
        self.connect(row, col - 1, node)
        self.connect(row, col + 1, node)

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
        for row in range(len(self.__circuitGrid)):  # FIXME optimising steps
            for col in range(len(self.__circuitGrid[row])):
                cellValue = self.__circuitGrid[row][col]
                if cellValue is None:
                    continue
                if not cellValue.isVariable():
                    # ensuring end nodes cannot be overwritten
                    continue
                try:
                    cellValue.updateVoltage(round(cellValue.node.getVoltage(), 3))
                except:
                    continue
        # updating the component object in the grid so they can be accessed with the select tool
        for key, edge in self.__listEdges.items():
            row, col = key[0], key[1]
            cellValue = self.__circuitGrid[row][col]
            cellValue.updateVoltage(round(edge.getPD(), 3))
            cellValue.updateCurrent(round((float(edge.getPD()) / float(edge.getResistance())), 3))

    def printNodes(self):  # for debugging, used in tkinter front end
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
        if circuitGridContents.isWireLike():
            return
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

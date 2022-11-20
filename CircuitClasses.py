minimumVoltageChange = 0.001


class CircuitGraph:
    def __init__(self, CircuitGrid):
        self.__listNodes = {}
        self.__listEdges = {}
        for row in range(len(CircuitGrid)):  # FIXME optimising steps
            for column in range(len(CircuitGrid[row])):
                if CircuitGrid[row][column] != "":
                    if row % 2 == 0 and column % 2 == 0:
                        voltage = None
                        if circuitGrid[row][column] == "+":
                            voltage = 5.0  # FIXME change to be voltage of + object
                        elif circuitGrid[row][column] == "-":
                            voltage = 0.0
                        self.__listNodes[(row, column)] = Node(voltage)
        for row in range(len(CircuitGrid)):  # FIXME optimising steps
            for column in range(len(CircuitGrid[row])):
                if CircuitGrid[row][column] != "":
                    if row % 2 == 0 and column % 2 == 1:
                        inputNode = self.__listNodes[(row, column - 1)]
                        outputNode = self.__listNodes[(row, column + 1)]
                    elif row % 2 == 1 and column % 2 == 0:
                        inputNode = self.__listNodes[(row - 1, column)]
                        outputNode = self.__listNodes[(row + 1, column)]
                    else:
                        continue
                    self.__listEdges[(row, column)] = Edge(inputNode, outputNode)

    def solveGraph(self):
        count = 0
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
                    node.setVoltageEstimate(numerator / denominator)
            for node in self.__listNodes.values():
                node.updateVoltage()
            count += 1
        print(count)

    def listNodes(self):
        for key, node in self.__listNodes.items():
            print("Dict entry:", key, "=", node.getVoltage())


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
        return self.__fixedVoltage is not None  # returns true is fixed voltage isn't none else return false

    def getEdges(self):
        return self.__edges


class Edge:
    def __init__(self, inputNode, outputNode):
        self.__resistance = 500  # FIXME change to resistance of object
        self.__inputNode = inputNode
        self.__outputNode = outputNode
        self.__current = 0
        inputNode.addEdge(self)
        outputNode.addEdge(self)

    def getOtherNode(self, askingNode):
        if askingNode == self.__outputNode:
            return self.__inputNode
        return self.__outputNode
        # return self.__outputNode if askingNode == self.__inputNode else self.__outputNode

    def getResistance(self):
        return self.__resistance


circuitGrid = [
    ["+", "p", "p", "", ""],
    ["p", "", "p", "", ""],
    ["p", "p", "p", "", ""],
    ["", "", "p", "", ""],
    ["", "", "-", "", ""]
]

circuit = CircuitGraph(circuitGrid)
circuit.solveGraph()
circuit.listNodes()

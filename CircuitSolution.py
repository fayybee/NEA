minimumVoltageChange = 0.00001 # this is used for determining if the circuit has reached an equilibrium point (rounding
# errors and other factors can cause the solution to never reach a natural equilibrium point and instead oscillate
# between values)


class CircuitGraph:
    def __init__(self, CircuitGrid):
        self.__listNodes = {}
        self.__listEdges = {}
        self.__circuitGrid = CircuitGrid
        self.__circuitGridRows = len(self.__circuitGrid)
        self.__circuitGridCols = len(self.__circuitGrid[1])

    def findNodes(self):
        # finds the nodes (join or source components) by iterating through the matrix and adds them to a dictionary
        # (key = graph coordinate of corresponding component)
        # (value = node object)
        for row in range(self.__circuitGridRows):
            for col in range(self.__circuitGridCols):
                component = self.__circuitGrid[row][col]
                if component is not None and not component.isEdgy():  # makes sure position isn't empty and checks to
                    # make sure it is a node type component
                    voltage = None
                    if not component.isVariable():
                        # if the component is a source or ground object it will have a preassigned potential
                        # this potential is used in instantiating the node object to ensure it has the correct potential
                        voltage = component.getPotential()
                        # voltage is equal to potential of the non variable component
                    newNode = Node(voltage)
                    # instantiates a node object and if voltage is not None then the node voltage will be fixed
                    self.__listNodes[(row, col)] = newNode
                    # adds the node to a dictionary with corresponding grid position as key
                    component.assignNode(newNode)  # assigns the node to the component object for safe keeping
                    # this makes it easier to find the node corresponding to a component (used in findEdges)

    def findEdges(self):
        # makes a dictionary of the edges
        # (key = graph coordinate of corresponding component)
        # (value = Edge object (holding the input node, output node and associated component object)
        for row in range(self.__circuitGridRows):
            for col in range(self.__circuitGridCols):
                component = self.__circuitGrid[row][col]
                if component is not None:
                    try:
                        if row % 2 == 0 and col % 2 == 1:  # position only edge type component can be placed
                            inputNode = self.__circuitGrid[row][col - 1].getAssignedNode()
                            outputNode = self.__circuitGrid[row][col + 1].getAssignedNode()
                            # checks for the nodes to the left and right
                        elif row % 2 == 1 and col % 2 == 0:  # position only edge type component can be placed
                            inputNode = self.__circuitGrid[row - 1][col].getAssignedNode()
                            outputNode = self.__circuitGrid[row + 1][col].getAssignedNode()
                            # checks for nodes above and bellow
                        else:
                            continue  # not a valid position for an edge type component so not considered
                        self.__listEdges[row, col] = Edge(inputNode, outputNode, component)
                        # instantiates an edge object containing the input node, output node, and the corresponding
                        # component. Instantiating with the component makes updating components to the values
                        # calculated easier
                    except:
                        component.updateCurrent(0.0)
                        # if the edge is not connected on both sides it will error
                        # we know that it isn't connected to anything therefore current in component is 0
                        # we can then set the component current to 0

    def solveGraph(self):
        self.findNodes()
        self.findEdges()
        while any((not node.isStable()) for node in self.__listNodes.values()):  # .values returns a list of values in
            # the dictionary as a list (this would return the nodes)
            # while any node in the dictionary is unstable (determined by minimumVoltageChange) solve the loop
            # this will iterate through the circuit until it reaches an equilibrium point
            for node in self.__listNodes.values():
                if not node.isFixed():
                    numerator = 0.0
                    denominator = 0.0
                    # numerator and denominator will be used to calculate the potential for each node that is not a
                    # source or ground component
                    for edge in node.getEdges():
                        # each node object stores its connected edge objects for easy access
                        try:
                            otherNode = edge.getOtherNode(node)
                            # returns the other node object that is stored in the connected edge object
                            voltage = otherNode.getVoltage()
                            resistance = edge.getResistance()
                            denominator += 1 / resistance
                            numerator += voltage / resistance
                            # for each connection this node object has it finds the potential of the connected node
                            # and the the resistance of the edge connecting them.
                            # Using V = IR we can find the rough potential (V) of the node using total current in the
                            # edges (I) and total resistance of the edges (R) and multiplying them. Current through
                            # the the edges is not known so for each edge we set the current to be the voltage of the
                            # other connected node (v), divided by the resistance in the edge (R). With each iteration
                            # through the circuit this rough estimate for the current in the edge and therefore
                            # potential in the node becomes more accurate
                        except:
                            pass  # errors if circuit is not complete but no action needed as this is dealt with when
                            # finding the edges
                        node.setVoltageEstimate(numerator / denominator)
                        # resistance cancels to give V (potential of the node)
            for node in self.__listNodes.values():
                node.updateVoltage()
                # once one complete iteration through all the nodes is complete we can update the voltage of the
                # nodes so that the next iteration can use more accurate voltages in the calculation, bringing it
                # closer to the real values
        self.updateComponentObjects()
        # when the circuit is stable the component objects be updated with values for potential, potential difference
        # and current, calculated using the potential in the nodes

    def updateComponentObjects(self):
        # updates the component objects in the grid class (from front end) so front end can have access to correct data
        for key, node in self.__listNodes.items():
            row, col = key[0], key[1]
            component = self.__circuitGrid[row][col]
            component.updatePotential(node.getVoltage())
        for key, edge in self.__listEdges.items():
            row, col = key[0], key[1]
            component = self.__circuitGrid[row][col]
            component.updatePotentialDifference(abs(edge.getPD()))
            component.updateCurrent(abs(edge.getPD() / float(edge.getResistance())))


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
            self.__stable = True  # if the node is a fixed voltage it is stable by definition
        else:
            self.__voltage = 0.0
        self.__fixedVoltage = vFixed

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
        # the voltage estimate is set first before setting the actual voltage of the node because in one iteration of
        # the circuit the calculations must be done with values from that same iteration. Once one iteration is
        # complete the voltage of the node can be updated to the estimate

    def addEdge(self, newEdge):
        self.__edges.append(newEdge)

    def isStable(self):
        return self.__stable

    def isFixed(self):
        return self.__fixedVoltage is not None  # returns true if fixed voltage isn't none, else return false

    def getEdges(self):
        return self.__edges


class Edge:
    def __init__(self, inputNode, outputNode, circuitGridContents):
        self.__resistance = circuitGridContents.getResistance()
        self.__inputNode = inputNode
        self.__outputNode = outputNode
        inputNode.addEdge(self)
        outputNode.addEdge(self)
        # when the edge object is instantiated with an input and an output node it will add itself to that node
        # object so that it can be easily accessed from that node object

    def getOtherNode(self, askingNode):
        if askingNode == self.__outputNode:
            return self.__inputNode
        return self.__outputNode

    def getResistance(self):
        return self.__resistance

    def getPD(self):
        return self.__inputNode.getVoltage() - self.__outputNode.getVoltage()
from ComponantClasses import *
from CircuitSolution import *


class Grid:  # used to connect front end classes to backend classes
    # holds component object in a 2D array
    def __init__(self, rows, cols):
        self.__grid = []
        for row in range(rows):  # creates a 2D array representing the circuit board
            self.row = []
            for col in range(cols):
                self.row.append(None)
            self.__grid.append(self.row)
        self.__circuitGraphObject = None  # will hold the graph object once it is instantiated

    def updateGrid(self, row, col, selectedTool):
        if selectedTool is None:
            self.__grid[row][col] = None
        if selectedTool == "+":
            self.__grid[row][col] = Source()
        if selectedTool == "-":
            self.__grid[row][col] = Ground()
        if selectedTool == chr(126):
            self.__grid[row][col] = Conductor()
        if selectedTool == chr(174):
            self.__grid[row][col] = Resistor()
        if selectedTool == chr(176):
            self.__grid[row][col] = Join()

    def getObject(self, row, col):  # returns the component object for a position on the grid
        if self.__grid[row][col] is not None:
            return self.__grid[row][col]
        else:
            return None

    def solve(self):
        self.__circuitGraphObject = CircuitGraph(self.__grid)
        self.__circuitGraphObject.solveGraph()

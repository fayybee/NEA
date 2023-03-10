from ComponantClasses import *
from CircuitSolution import *

class Grid:
    def __init__(self, rows, cols):
        self.__grid = []
        for row in range(rows):
            self.row = []
            for col in range(cols):
                self.row.append(None)
            self.__grid.append(self.row)
        self.__circuitClass = None
        self.__numRows = rows
        self.__numCols = cols

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

    def getObject(self, row, col):
        if self.__grid[row][col] is not None:
            return self.__grid[row][col]
        else:
            return None

    def solve(self):
        self.__circuitClass = CircuitGraph(self.__grid)
        self.__circuitClass.solveGraph()
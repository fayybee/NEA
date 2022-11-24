from ComponentClasses import *
from CircuitClasses import *
import tkinter as tk


class Window:
    def __init__(self, rows, cols):
        # grid variables
        self.__gridWidth = 500
        self.__gridHeight = 500
        self.__gridNumberOfRowCells = rows
        self.__gridNumberOfColumnCells = cols
        self.__toolBarWidth = 100
        self.__menuHeight = 10

        # circuit grid initializing
        self.__CircuitGrid = Grid(rows, cols)

        # window initialising/configuring
        self.__window = tk.Tk()
        self.__window.title = "buttons please"
        self.__window.rowconfigure(0, minsize=self.__menuHeight)
        self.__window.rowconfigure(1, minsize=self.__gridHeight)
        self.__window.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__window.columnconfigure(1, minsize=self.__gridWidth)

        # tool status
        self.__selectedTool = ""

        # frames setup, using hard coded ratios and grid variables to calculate the size of the frames
        self.__menuFrame = tk.Frame(self.__window, bg="light grey", relief=tk.GROOVE, borderwidth=5)
        self.__toolBarFrame = tk.Frame(self.__window, bg="light slate grey", relief=tk.GROOVE, borderwidth=5)
        self.__gridFrame = tk.Frame(self.__window, bg="orange")

        # sizing the grid
        for i in range(self.__gridNumberOfRowCells):
            self.__gridFrame.rowconfigure(i, minsize=int(self.__gridHeight / self.__gridNumberOfColumnCells))
        for i in range(self.__gridNumberOfColumnCells):
            self.__gridFrame.columnconfigure(i, minsize=self.__gridWidth / self.__gridNumberOfRowCells)

        # formatting frames
        self.__toolBarFrame.columnconfigure(0, minsize=self.__toolBarWidth)

        # labels
        self.__toolbarLabel = tk.Label(self.__toolBarFrame, text="TOOL BAR", bg="light slate grey")
        self.__toolbarLabel.grid(row=0)

        # frame griding
        self.__menuFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.__toolBarFrame.grid(row=1, column=0, sticky="NSEW")
        self.__gridFrame.grid(row=1, column=1)

        # making the grid buttons
        self.__gridOfButtons = []
        for row in range(self.__gridNumberOfRowCells):
            self.__buttonRow = []
            for col in range(self.__gridNumberOfColumnCells):
                if row % 2 == 1 and col % 2 == 1:
                    self.__gridButton = tk.Button(self.__gridFrame, bg="tan4",
                                                  command=lambda i=row, j=col: self.gridClick(i, j))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
                elif row % 2 == 0 and col % 2 == 0:
                    self.__gridButton = tk.Button(self.__gridFrame, bg="chocolate1",
                                                  command=lambda i=row, j=col: self.gridClick(i, j))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
                else:
                    self.__gridButton = tk.Button(self.__gridFrame, bg="tan1",
                                                  command=lambda i=row, j=col: self.gridClick(i, j))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)

            self.__gridOfButtons.append(self.__buttonRow)

        # making toolbar buttons
        self.__buttonJoin = tk.Button(self.__toolBarFrame, text="join", command=self.joinSelected)
        self.__buttonJoin.grid(sticky="NEWS")
        self.__buttonPos = tk.Button(self.__toolBarFrame, text="+", command=self.posSelected)
        self.__buttonPos.grid(sticky="NEWS")
        self.__buttonNeg = tk.Button(self.__toolBarFrame, text="-", command=self.negSelected)
        self.__buttonNeg.grid(sticky="NEWS")
        self.__buttonWire = tk.Button(self.__toolBarFrame, text="wire", command=self.wireSelected)
        self.__buttonWire.grid(sticky="NEWS")
        self.__buttonResistor = tk.Button(self.__toolBarFrame, text="resistor", command=self.resistorSelected)
        self.__buttonResistor.grid(sticky="NEWS")
        self.__buttonBlank = tk.Button(self.__toolBarFrame, text="clear", command=self.blankSelected)
        self.__buttonBlank.grid(sticky="NEWS")

        # menu labels and buttons
        self.__SolveButton = tk.Button(self.__menuFrame, text="SOLVE", command=self.solveCircuit)
        self.__SolveButton.grid(sticky="NSEW")

    # grid button command
    def gridClick(self, i, j):
        # makes it so you can only join corners and add components between join point to reduce connection options
        if self.__selectedTool == "":
            self.__gridOfButtons[i][j].config(text=self.__selectedTool)
        elif self.__selectedTool == "join" or self.__selectedTool == "+" or self.__selectedTool == "-":
            if i % 2 == 0 and j % 2 == 0:
                self.__gridOfButtons[i][j].config(text=self.__selectedTool)
                self.__CircuitGrid.updateGrid(i, j, self.__selectedTool)
        elif (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
            self.__gridOfButtons[i][j].config(text=self.__selectedTool)
            self.__CircuitGrid.updateGrid(i, j, self.__selectedTool)

    def joinSelected(self):
        self.__selectedTool = "join"

    def posSelected(self):
        self.__selectedTool = "+"

    def negSelected(self):
        self.__selectedTool = "-"

    def wireSelected(self):
        self.__selectedTool = "wire"

    def resistorSelected(self):
        self.__selectedTool = "res"

    def blankSelected(self):
        self.__selectedTool = ""

    def solveCircuit(self):
        self.__CircuitGrid.solve()

    # runs window
    def run(self):
        self.__window.mainloop()


class Grid:
    def __init__(self, rows, cols):
        self.__grid = []
        for row in range(rows):
            self.row = []
            for col in range(cols):
                self.row.append(None)
            self.__grid.append(self.row)
        self.__circuitClass = None

    def updateGrid(self, i, j, selectedTool):
        if selectedTool == "+":
            self.__grid[i][j] = ("+", SourceNode())
        if selectedTool == "-":
            self.__grid[i][j] = ("-", GroundNode())
        if selectedTool == "wire":
            self.__grid[i][j] = ("wire", Wire())
        if selectedTool == "res":
            self.__grid[i][j] = ("resistor", Resistor())
        if selectedTool == "join":
            self.__grid[i][j] = ("join", ComponentNode())
        if selectedTool == "":
            self.__grid[i][j] = None

    def solve(self):
        self.__circuitClass = CircuitGraph(self.__grid)
        self.__circuitClass.solveGraph()
        self.__circuitClass.listNodes()
        print(self.__grid)


numberOfGridRows = 15
numberOfGridCols = 15
MainWindow = Window(numberOfGridRows, numberOfGridCols)
MainWindow.run()

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
        self.__statsFrameHeight = 200
        self.__menuHeight = 10

        # circuit grid initializing
        self.__CircuitGrid = Grid(rows, cols)

        # window initialising/configuring
        self.__window = tk.Tk()
        self.__window.title = "buttons please"
        self.__window.rowconfigure(0, minsize=self.__menuHeight)
        self.__window.rowconfigure(1, minsize=self.__gridHeight - self.__statsFrameHeight)
        self.__window.rowconfigure(2, minsize=self.__statsFrameHeight)
        self.__window.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__window.columnconfigure(1, minsize=self.__gridWidth)

        # tool status
        self.__selectedTool = ""

        # frames setup
        self.__menuFrame = tk.Frame(self.__window, bg="light grey", relief=tk.GROOVE, borderwidth=5)
        self.__toolBarFrame = tk.Frame(self.__window, bg="light slate grey", relief=tk.GROOVE, borderwidth=5)
        self.__gridFrame = tk.Frame(self.__window, bg="orange")
        self.__statsFrame = tk.Frame(self.__window, bg="MistyRose3", relief=tk.GROOVE, borderwidth=5)

        # sizing the grid
        for i in range(self.__gridNumberOfRowCells):
            self.__gridFrame.rowconfigure(i, minsize=int(self.__gridHeight / self.__gridNumberOfColumnCells))
        for i in range(self.__gridNumberOfColumnCells):
            self.__gridFrame.columnconfigure(i, minsize=self.__gridWidth / self.__gridNumberOfRowCells)

        # formatting frames
        self.__toolBarFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__statsFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        for i in range(5):
            self.__menuFrame.columnconfigure(i, minsize=50)

        # labels
        self.__toolbarLabel = tk.Label(self.__toolBarFrame, text="TOOL BAR", bg="light slate grey")
        self.__toolbarLabel.grid(row=0)
        self.__statsLabel = tk.Label(self.__statsFrame, text="STATS", bg="MistyRose3")
        self.__statsLabel.grid(row=0)
        self.__currentStatisticsLabel = tk.Label(self.__statsFrame, bg="MistyRose3")
        self.__currentStatisticsLabel.grid()

        # frame griding
        self.__menuFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.__toolBarFrame.grid(row=1, column=0, sticky="NSEW")
        self.__gridFrame.grid(row=1, column=1, rowspan=2)
        self.__statsFrame.grid(row=2, column=0, sticky="NSEW")

        # making the grid buttons
        self.__gridOfButtons = []
        for row in range(self.__gridNumberOfRowCells):
            self.__buttonRow = []
            for col in range(self.__gridNumberOfColumnCells):
                if row % 2 == 1 and col % 2 == 1:
                    self.__gridButton = tk.Button(self.__gridFrame, bg="violet red",
                                                  command=lambda i=row, j=col: self.gridClick(i, j))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
                elif row % 2 == 0 and col % 2 == 0:
                    self.__gridButton = tk.Button(self.__gridFrame, bg="hot pink",
                                                  command=lambda i=row, j=col: self.gridClick(i, j))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
                else:
                    self.__gridButton = tk.Button(self.__gridFrame, bg="orchid2",
                                                  command=lambda i=row, j=col: self.gridClick(i, j))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)

            self.__gridOfButtons.append(self.__buttonRow)

        # making toolbar buttons
        self.__buttonSelect = tk.Button(self.__toolBarFrame, text="select", command=self.selectSelected)
        self.__buttonSelect.grid(row=1, sticky="NEWS")
        self.__buttonJoin = tk.Button(self.__toolBarFrame, text="join", command=self.joinSelected)
        self.__buttonJoin.grid(row=2, sticky="NEWS")
        self.__buttonPos = tk.Button(self.__toolBarFrame, text="+", command=self.posSelected)
        self.__buttonPos.grid(row=3, sticky="NEWS")
        self.__buttonNeg = tk.Button(self.__toolBarFrame, text="-", command=self.negSelected)
        self.__buttonNeg.grid(row=4, sticky="NEWS")
        self.__buttonWire = tk.Button(self.__toolBarFrame, text="wire", command=self.wireSelected)
        self.__buttonWire.grid(row=5, sticky="NEWS")
        self.__buttonResistor = tk.Button(self.__toolBarFrame, text="resistor", command=self.resistorSelected)
        self.__buttonResistor.grid(row=6, sticky="NEWS")
        self.__buttonBlank = tk.Button(self.__toolBarFrame, text="clear", command=self.blankSelected)
        self.__buttonBlank.grid(row=7, sticky="NEWS")

        # menu labels and buttons
        self.__solveButton = tk.Button(self.__menuFrame, text="SOLVE", command=self.solveCircuit)
        self.__solveButton.grid(row = 0,column=0, sticky="NSEW")
        self.__clear = tk.Button(self.__menuFrame, text="clear all", command=self.clearCircuit)
        self.__clear.grid(row=0, column=1, sticky="NEWS")

    # grid button command
    def gridClick(self, i, j):
        # makes it so you can only join corners and add components between join point to reduce connection options
        if self.__selectedTool == "selected":
            try:
                if i % 2 == 0 and j % 2 == 0:
                    potential = objectGetVoltage(self.__CircuitGrid.getObject(i, j))
                    self.__currentStatisticsLabel.config(text="potential: " + str(potential))
                elif (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    potentialDifference = objectGetVoltage(self.__CircuitGrid.getObject(i, j))
                    current = objectGetCurrent(self.__CircuitGrid.getObject(i, j))
                    resistance = objectGetResistance(self.__CircuitGrid.getObject(i, j))
                    self.__currentStatisticsLabel.config(
                        text="p.d: " + str(potentialDifference) + "\n" + "current: " + str(
                            current) + "\n" + "resistance: " + str(resistance))
            except:
                pass
        elif self.__selectedTool == "":
            self.__gridOfButtons[i][j].config(text=self.__selectedTool)
        elif self.__selectedTool == "join" or self.__selectedTool == "+" or self.__selectedTool == "-":
            if i % 2 == 0 and j % 2 == 0:
                self.__gridOfButtons[i][j].config(text=self.__selectedTool)
                self.__CircuitGrid.updateGrid(i, j, self.__selectedTool)
        elif (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
            self.__gridOfButtons[i][j].config(text=self.__selectedTool)
            self.__CircuitGrid.updateGrid(i, j, self.__selectedTool)

    def presentData(self):
        pass

    # button commands
    def selectSelected(self):
        self.__selectedTool = "selected"

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

    def clearCircuit(self):
        self.__CircuitGrid.clear()
        for i in range(len(self.__gridOfButtons)):
            for j in range(len(self.__gridOfButtons[i])):
                self.__gridOfButtons[i][j].config(text="")  # FIXME not clearing

    # runs window
    def run(self):
        self.__window.mainloop()


# grid class which holds the objects and the symbol connected to it
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

    def solve(self):  # solves for the potential of each "node"
        self.__circuitClass = CircuitGraph(self.__grid)
        self.__circuitClass.solveGraph()
        self.__circuitClass.listNodes()

    def clear(self):
        for row in range(len(self.__grid)):
            for column in range(len(self.__grid[row])):
                self.__grid[row][column] = None
        self.__circuitClass.cleanUpAll()

    def getObject(self, i, j):
        if self.__grid[i][j] is not None:
            return self.__grid[i][j][1]
        else:
            return None


numberOfGridRows = 15
numberOfGridCols = 15
MainWindow = Window(numberOfGridRows, numberOfGridCols)
MainWindow.run()

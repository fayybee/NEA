from classesofcomponents import *
from CircuitClasses import *
# from GraphWindow import *
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
        self.__selectedObject = None

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
            self.__menuFrame.columnconfigure(i, minsize=100)

        # labels
        self.__toolbarLabel = tk.Label(self.__toolBarFrame, text="TOOL BAR", bg="light slate grey")
        self.__toolbarLabel.grid(row=0)
        self.__statsLabel = tk.Label(self.__statsFrame, text="STATS", bg="MistyRose3")
        self.__statsLabel.grid(row=0)
        self.__currentStatisticsLabel = tk.Label(self.__statsFrame, bg="MistyRose3")
        self.__currentStatisticsLabel.grid(row=1)
        self.__voltageEntryLabel = tk.Label(self.__statsFrame, text="Enter Voltage", bg="MistyRose3")
        self.__voltageEntryLabel.grid(row=2)
        self.__resistanceEntryLabel = tk.Label(self.__statsFrame, text="Enter Resistance", bg="MistyRose3")
        self.__resistanceEntryLabel.grid(row=4)

        # entry widgets
        self.__voltageEntry = tk.Entry(self.__statsFrame, width=int(self.__toolBarWidth / 6))
        self.__voltageEntry.grid(row=3, sticky="s")
        self.__resistanceEntry = tk.Entry(self.__statsFrame, width=int(self.__toolBarWidth / 6))
        self.__resistanceEntry.grid(row=5, sticky="s")

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

        # stats buttons
        self.__applyStatsButton = tk.Button(self.__statsFrame, text="apply new stats", command=self.applyNewStats)
        self.__applyStatsButton.grid()

        # menu labels and buttons
        self.__solveButton = tk.Button(self.__menuFrame, text="SOLVE CIRCUIT", command=self.solveCircuit)
        self.__solveButton.grid(row=0, column=0, sticky="NSEW")
        self.__plotButton = tk.Button(self.__menuFrame, text="PLOT GRAPH")
        self.__plotButton.grid(row=0, column=1, sticky="NSEW")
        self.__clear = tk.Button(self.__menuFrame, text="clear grid", command=self.clearCircuit)
        self.__clear.grid(row=0, column=2, sticky="NEWS")

    # grid button command
    def gridClick(self, row, col):
        if self.__selectedTool == "selected":
            self.__selectedObject = self.__CircuitGrid.getObject(row, col)
            try:
                if row % 2 == 0 and col % 2 == 0:
                    potential = self.__selectedObject.getVoltage()
                    self.__currentStatisticsLabel.config(text="potential: " + str(potential))
                    return
                if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                    if isinstance(self.__selectedObject, Resistor):
                        potentialDifference = self.__selectedObject.getVoltage()
                        current = self.__selectedObject.getCurrent()
                        resistance = self.__selectedObject.getResistance()
                        self.__currentStatisticsLabel.config(
                            text="p.d: " + str(potentialDifference) + "\n" + "current: " + str(
                                current) + "\n" + "resistance: " + str(resistance))
                    elif isinstance(self.__selectedObject, Wire):
                        current = self.__selectedObject.getCurrent()
                        self.__currentStatisticsLabel.config(text="p.d: 0.00" + "\n" + "current: " + str(current) + "\n" + "resistance: 0.00")
            except:
                self.__currentStatisticsLabel.config(text="no component selected")

        # makes it so you can only join corners and add components between join point to reduce connection options
        elif self.__selectedTool == "":
            self.__gridOfButtons[row][col].config(text=self.__selectedTool)
        elif self.__selectedTool == "join" or self.__selectedTool == "+" or self.__selectedTool == "-":
            if row % 2 == 0 and col % 2 == 0:
                self.__gridOfButtons[row][col].config(text=self.__selectedTool)
                self.__CircuitGrid.updateGrid(row, col, self.__selectedTool)
        elif (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
            self.__gridOfButtons[row][col].config(text=self.__selectedTool)
            self.__CircuitGrid.updateGrid(row, col, self.__selectedTool)

    # tool bar button commands
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

    # menu bar button commands
    def solveCircuit(self):
        self.__CircuitGrid.solve()

    def clearCircuit(self):
        self.__CircuitGrid.clear()
        for i in range(len(self.__gridOfButtons)):
            for j in range(len(self.__gridOfButtons[i])):
                self.__gridOfButtons[i][j].config(text="")

    def saveCircuit(self):
        saveWindow = tk.Toplevel(Window)
        saveWindow.title("Save Circuit")
        #FIXME finish writing

    def plotGraph(self):
        pass

    # stats bar button commands
    def applyNewStats(self):
        if isinstance(self.__selectedObject, SourceNode):
            self.__selectedObject.updateVoltage(float(self.__voltageEntry.get()))  # using the objects getters and setters
            # not external functions
        if isinstance(self.__selectedObject, Resistor):
            self.__selectedObject.setResistance(float(self.__resistanceEntry.get()))
        self.__voltageEntry.delete(0, tk.END)
        self.__resistanceEntry.delete(0, tk.END)

    # runs window
    def run(self):
        self.__window.mainloop()


# grid class which holds the objects
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

    def updateGrid(self, i, j, selectedTool):
        if selectedTool == "+":
            self.__grid[i][j] = SourceNode()
        if selectedTool == "-":
            self.__grid[i][j] = GroundNode()
        if selectedTool == "wire":
            self.__grid[i][j] = Wire()
        if selectedTool == "res":
            self.__grid[i][j] = Resistor()
        if selectedTool == "join":
            self.__grid[i][j] = ComponentNode()
        if selectedTool == "":
            self.__grid[i][j] = None

    def solve(self):  # solves for the potential of each "node"
        self.__circuitClass = CircuitGraph(self.__grid)
        self.__circuitClass.solveGraph()
        self.__circuitClass.printNodes()  # debugging

    def clear(self):
        for row in range(len(self.__grid)):
            for column in range(len(self.__grid[row])):
                self.__grid[row][column] = None
        self.__circuitClass.cleanUpAll()

    def getObject(self, i, j):
        if self.__grid[i][j] is not None:
            return self.__grid[i][j]
        else:
            return None

    def getNumRows(self):
        return self.__numRows

    def getNumCols(self):
        return self.__numCols


numberOfGridRows = 15
numberOfGridCols = 15
MainWindow = Window(numberOfGridRows, numberOfGridCols)
MainWindow.run()

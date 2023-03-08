from ComponantClasses import *
from CircuitSolution import *
import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window:
    def __init__(self, rows, cols):
        # grid constants
        self.__gridNumberOfRows = rows
        self.__gridNumberOfColumns = cols
        self.__gridWidth = 500
        self.__gridHeight = 500
        self.__toolBarWidth = 100
        self.__graphFrameWidth = 250

        # stats variables
        self.__currentDataPoints = []
        self.__voltageDataPoints = []
        self.__timeDataPoints = []

        # instantiate grid class
        self.__circuitGridClass = Grid(rows, cols)

        # tool statuses
        self.__selectedComponent = None
        self.__selectedTool = None

        # window configuration
        self.__window = tk.Tk()
        self.__window.rowconfigure([0, 1], minsize=self.__gridHeight / 2)
        self.__window.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__window.columnconfigure(1, minsize=self.__gridWidth)
        self.__window.columnconfigure(2, minsize=self.__graphFrameWidth)

        # frame initialising
        self.__toolBarFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__toolBarFrame.grid(row=0, column=0, sticky="NEWS")
        self.__statsFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__statsFrame.grid(row=1, column=0, sticky="NEWS")
        self.__gridFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__gridFrame.grid(row=0, rowspan=2, column=1, sticky="NEWS")
        self.__graphFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__graphFrame.grid(row=0, rowspan=2, column=2, sticky="NEWS")

        # frame configuration
        self.__toolBarFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__statsFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__graphFrame.rowconfigure([0, 1, 2], minsize=(self.__gridHeight / 3) - 2)

        for i in range(self.__gridNumberOfRows):
            self.__gridFrame.rowconfigure(i, minsize=int(self.__gridWidth / self.__gridNumberOfRows))
        for i in range(self.__gridNumberOfColumns):
            self.__gridFrame.columnconfigure(i, minsize=int(self.__gridHeight / self.__gridNumberOfColumns))

        # frame labels
        self.__toolbarLabel = tk.Label(self.__toolBarFrame, text="TOOL BAR")
        self.__toolbarLabel.grid(row=0, sticky="N")
        self.__statsLabel = tk.Label(self.__statsFrame, text="STATISTICS")
        self.__statsLabel.grid(row=0, sticky="N")
        self.__currentStats = tk.Label(self.__statsFrame, text="no component \n selected")
        self.__currentStats.grid(row=1, sticky="EW")
        self.__componentEditLabel = tk.Label(self.__statsFrame, text="")
        self.__componentEditLabel.grid(row=2, sticky="NEWS")
        self.__componentEditStatNum = tk.Label(self.__statsFrame, text="0")
        self.__componentEditStatNum.grid(row=3, column=0, sticky="NS")

        # creating grid buttons
        self.__buttonMatrix = []
        for row in range(self.__gridNumberOfRows):
            self.__buttonRow = []
            for col in range(self.__gridNumberOfColumns):
                if row % 2 == 1 and col % 2 == 1:
                    self.__gridButton = tk.Button(self.__gridFrame,
                                                  command=lambda rowNum=row, colNum=col: self.gridClick(rowNum, colNum))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
                elif row % 2 == 0 and col % 2 == 0:
                    self.__gridButton = tk.Button(self.__gridFrame,
                                                  command=lambda rowNum=row, colNum=col: self.gridClick(rowNum, colNum))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
                else:
                    self.__gridButton = tk.Button(self.__gridFrame,
                                                  command=lambda rowNum=row, colNum=col: self.gridClick(rowNum, colNum))
                    self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                    self.__buttonRow.append(self.__gridButton)
            self.__buttonMatrix.append(self.__buttonRow)

        # creating tool buttons
        self.__buttonSelect = tk.Button(self.__toolBarFrame, text="select", command=self.selectButtonClick)
        self.__buttonSelect.grid(row=1, sticky="NEWS")
        self.__buttonClear = tk.Button(self.__toolBarFrame, text="clear", command=self.clearButtonClick)
        self.__buttonClear.grid(row=2, sticky="NEWS")
        self.__buttonJoin = tk.Button(self.__toolBarFrame, text=chr(176), command=self.joinButtonClick)
        self.__buttonJoin.grid(row=3, sticky="NEWS")
        self.__buttonSource = tk.Button(self.__toolBarFrame, text="+", command=self.sourceButtonClick)
        self.__buttonSource.grid(row=4, sticky="NEWS")
        self.__buttonGround = tk.Button(self.__toolBarFrame, text="-", command=self.groundButtonClick)
        self.__buttonGround.grid(row=5, sticky="NEWS")
        self.__buttonWire = tk.Button(self.__toolBarFrame, text=chr(126), command=self.wireButtonClick)
        self.__buttonWire.grid(row=6, sticky="NEWS")
        self.__buttonResistor = tk.Button(self.__toolBarFrame, text=chr(174), command=self.resistorButtonClick)
        self.__buttonResistor.grid(row=7, sticky="NEWS")

        # creating stats button
        self.__componentUpButton = tk.Button(self.__statsFrame, text="+", command=self.increaseButtonClick)
        self.__componentUpButton.grid(row=3, column=0, sticky="NES")
        self.__componentDownButton = tk.Button(self.__statsFrame, text="-", command=self.decreaseButtonClick)
        self.__componentDownButton.grid(row=3, column=0, sticky="WNS")

        # graph data setup
        currentVoltageData = {"current": self.__currentDataPoints, "voltage": self.__voltageDataPoints}
        currentVoltageDataFrame = pd.DataFrame(currentVoltageData)
        currentTimeData = {"current": self.__currentDataPoints, "time": self.__timeDataPoints}
        currentTimeDataFrame = pd.DataFrame(currentTimeData)
        voltageTimeData = {"voltage": self.__voltageDataPoints, "time": self.__timeDataPoints}
        voltageTimeDataFrame = pd.DataFrame(voltageTimeData)

        # graph setup
        IVFigure = Figure(figsize=(3, 1), dpi=100)
        IVGraph = IVFigure.add_subplot(111)
        IVGraphType = FigureCanvasTkAgg(IVFigure, self.__graphFrame)
        IVGraphType.get_tk_widget().grid(row=0, sticky="NEWS")
        currentVoltageDataFrame = currentVoltageDataFrame[["current", "voltage"]].groupby("voltage").sum()
        currentVoltageDataFrame.plot(kind="line", legend=False, ax=IVGraph, color="r", marker=".", fontsize=5)
        IVGraph.set_title("IV graph", fontsize=7)
        IVGraph.set_xlabel("voltage")
        IVGraph.set_ylabel("current")

        ITFigure = Figure(figsize=(3, 1), dpi=100)
        ITGraph = ITFigure.add_subplot(111)
        ITGraphType = FigureCanvasTkAgg(ITFigure, self.__graphFrame)
        ITGraphType.get_tk_widget().grid(row=1, sticky="NEWS")
        currentTimeDataFrame = currentTimeDataFrame[["current", "time"]].groupby("time").sum()
        currentTimeDataFrame.plot(kind="line", legend=False, ax=ITGraph, color="r", marker=".", fontsize=5)
        ITGraph.set_title("It graph", fontsize=7)
        ITGraph.set_xlabel("time")
        ITGraph.set_ylabel("current")

        VTFigure = Figure(figsize=(3, 1), dpi=100)
        VTGraph = VTFigure.add_subplot(111)
        VTGraphType = FigureCanvasTkAgg(VTFigure, self.__graphFrame)
        VTGraphType.get_tk_widget().grid(row=2, sticky="NEWS")
        voltageTimeDataFrame = voltageTimeDataFrame[["voltage", "time"]].groupby("time").sum()
        voltageTimeDataFrame.plot(kind="line", legend=False, ax=VTGraph, color="r", marker=".", fontsize=5)
        VTGraph.set_title("Vt graph", fontsize=7)
        VTGraph.set_xlabel("time")
        VTGraph.set_ylabel("voltage")

    def gridClick(self, rowNum, colNum):
        self.solveCircuit()
        self.wipeSelectedCellColour()
        if self.__selectedTool == "select":
            self.__selectedComponent = self.__circuitGridClass.getObject(rowNum, colNum)
            self.__buttonMatrix[rowNum][colNum].config(bg="light grey")  # makes it easy to see what is selected
            self.updateStats()  # if select tool is chosen stats of selected component is displayed
            self.updateComponentEditor()
        else:  # otherwise grid is updated with selected component
            if self.__selectedTool is None:  # only for if the clever tool is selected
                self.__buttonMatrix[rowNum][colNum].config(text="")
                self.__circuitGridClass.updateGrid(rowNum, colNum, self.__selectedTool)
            elif self.__selectedTool == chr(176) or self.__selectedTool == "+" or self.__selectedTool == "-":
                if rowNum % 2 == 0 and colNum % 2 == 0:
                    # nodes can only be placed in even areas to prevent then from being next to each other
                    self.__buttonMatrix[rowNum][colNum].config(text=self.__selectedTool)
                    self.__circuitGridClass.updateGrid(rowNum, colNum, self.__selectedTool)  # updates the grid class
            elif (rowNum % 2 == 0 and colNum % 2 == 1) or (rowNum % 2 == 1 and colNum % 2 == 0):
                # edges can only be placed in even areas to prevent then from being next to each other
                # this makes calculations easier because it is obvious what they are connected to
                self.__buttonMatrix[rowNum][colNum].config(text=self.__selectedTool)
                self.__circuitGridClass.updateGrid(rowNum, colNum, self.__selectedTool)
        self.__circuitGridClass.solve()  # this is called at the end of every button click to make it seam like it is
        # updating continuously

    def updateStats(self):
        try:
            if not self.__selectedComponent.isEdgy():
                potential = round(self.__selectedComponent.getPotential(), 3)
                self.__currentStats.config(text=f"Potential: {potential}")
            else:
                potentialDifference = round(self.__selectedComponent.getPotentialDifference(), 3)
                current = round(self.__selectedComponent.getCurrent(), 3)
                resistance = round(self.__selectedComponent.getResistance(), 3)
                self.__currentStats.config(text=f"Res: {resistance} \np.d: {potentialDifference} \nCur: {current} ")
        except:
            self.__currentStats.config(text="no component \n selected")

    def updateComponentEditor(self):
        try:
            if self.__selectedComponent.isEdgy() and not self.__selectedComponent.isWire():
                self.__componentEditLabel.config(text="Resistance")
                self.__componentEditStatNum.config(text=str(round(self.__selectedComponent.getResistance(), 3)))
            elif self.__selectedComponent.isWire():
                self.__componentEditLabel.config(text="")
                self.__componentEditStatNum.config(text="0.0")
            elif not self.__selectedComponent.isEdgy():
                self.__componentEditLabel.config(text="Potential")
                self.__componentEditStatNum.config(text=str(round(self.__selectedComponent.getPotential(), 3)))
        except:
            self.__componentEditLabel.config(text="")
            self.__componentEditStatNum.config(text="-")

    def wipeSelectedCellColour(self):  # prevents everything from looking selected so new selection is easy to see
        for i in range(len(self.__buttonMatrix)):
            for j in range(len(self.__buttonMatrix[i])):
                self.__buttonMatrix[i][j].config(bg="SystemButtonFace")

    # setting tool based on button clicked
    def selectButtonClick(self):
        self.__selectedTool = "select"
        self.__circuitGridClass.solve()

    def clearButtonClick(self):
        self.__selectedTool = None
        self.__circuitGridClass.solve()

    def joinButtonClick(self):
        self.__selectedTool = chr(176)
        self.__circuitGridClass.solve()

    def sourceButtonClick(self):
        self.__selectedTool = "+"
        self.__circuitGridClass.solve()

    def groundButtonClick(self):
        self.__selectedTool = "-"
        self.__circuitGridClass.solve()

    def wireButtonClick(self):
        self.__selectedTool = chr(126)
        self.__circuitGridClass.solve()

    def resistorButtonClick(self):
        self.__selectedTool = chr(174)
        self.__circuitGridClass.solve()

    # editing component stats button commands
    def increaseButtonClick(self):
        try:
            if self.__selectedComponent.isEdgy() and not self.__selectedComponent.isWire():
                self.increaseResistance()
                self.__componentEditStatNum.config(text=str(self.__selectedComponent.getResistance()))
            elif self.__selectedComponent.isSource():
                self.increasePotential()
                self.__componentEditStatNum.config(text=str(self.__selectedComponent.getPotential()))
            self.solveCircuit()
            self.updateStats()
        except:
            pass

    def decreaseButtonClick(self):
        try:
            if self.__selectedComponent.isEdgy() and not self.__selectedComponent.isWire():
                self.decreaseResistance()
                self.__componentEditStatNum.config(text=str(self.__selectedComponent.getResistance()))
            elif self.__selectedComponent.isSource():
                self.decreasePotential()
                self.__componentEditStatNum.config(text=str(self.__selectedComponent.getPotential()))
            self.solveCircuit()
            self.updateStats()

        except:
            pass

    def increaseResistance(self):
        self.__selectedComponent.setResistance(self.__selectedComponent.getResistance() + 1)

    def decreaseResistance(self):
        if self.__selectedComponent.getResistance() > 1:
            self.__selectedComponent.setResistance(self.__selectedComponent.getResistance() - 1)

    def increasePotential(self):
        self.__selectedComponent.updatePotential(self.__selectedComponent.getPotential() + 1)

    def decreasePotential(self):
        if self.__selectedComponent.getPotential() > 0:
            self.__selectedComponent.updatePotential(self.__selectedComponent.getPotential() - 1)

    # solve
    def solveCircuit(self):
        self.__circuitGridClass.solve()

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

    def solve(self):  # solves for the potential of each "node"
        self.__circuitClass = CircuitGraph(self.__grid)
        self.__circuitClass.solveGraph()


numberOfGridRows = 15
numberOfGridCols = 15
MainWindow = Window(numberOfGridRows, numberOfGridCols)
MainWindow.run()

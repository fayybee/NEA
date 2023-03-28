import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from GridClass import *
from HelpWindow import *


class FrontEndWindow:
    def __init__(self, rows, cols):
        # window constants
        self.__gridNumberOfRows = rows
        self.__gridNumberOfColumns = cols
        self.__gridWidth = 500
        self.__gridHeight = 500
        self.__toolBarWidth = 170
        self.__graphFrameWidth = 250  # window constants are which to change here

        # stats variables
        self.__currentDataPoints = []
        self.__voltageDataPoints = []
        self.__timeDataPoints = []
        self.__selectedGraphPlotComponent = None

        # instantiate grid class
        self.__circuitGridClass = Grid(rows, cols)

        # tool statuses
        self.__selectedComponent = None
        self.__selectedTool = None

        # cell colouring (use to help identify which component is being plotted)
        self.__graphSelectedCell = None

        # window configuration
        self.__window = tk.Tk()
        self.__window.rowconfigure(0, minsize=35)
        self.__window.rowconfigure([1, 2], minsize=self.__gridHeight / 2)
        self.__window.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__window.columnconfigure(1, minsize=self.__gridWidth)
        self.__window.columnconfigure(2, minsize=self.__graphFrameWidth)

        # frame initialising
        self.__menuBarFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__menuBarFrame.grid(row=0, column=0, columnspan=3, sticky="NEWS")
        self.__toolBarFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__toolBarFrame.grid(row=1, column=0, sticky="NEWS")
        self.__dataFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__dataFrame.grid(row=2, column=0, sticky="NEWS")
        self.__gridFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__gridFrame.grid(row=1, rowspan=2, column=1, sticky="NEWS")
        self.__graphFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__graphFrame.grid(row=1, rowspan=2, column=2, sticky="NEWS")

        # frame configuration (calculated using window constants)
        self.__toolBarFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__dataFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__graphFrame.rowconfigure([0, 1, 2], minsize=(self.__gridHeight / 3) - 2)

        for i in range(self.__gridNumberOfRows):
            self.__gridFrame.rowconfigure(i, minsize=int(self.__gridWidth / self.__gridNumberOfRows))
        for i in range(self.__gridNumberOfColumns):
            self.__gridFrame.columnconfigure(i, minsize=int(self.__gridHeight / self.__gridNumberOfColumns))

        # frame labels
        self.__toolbarLabel = tk.Label(self.__toolBarFrame, text="TOOL BAR")
        self.__toolbarLabel.grid(row=0, sticky="N")
        self.__dataLabel = tk.Label(self.__dataFrame, text="COMPONENT DATA")
        self.__dataLabel.grid(row=0, sticky="N")
        self.__selectedComponentLabel = tk.Label(self.__dataFrame, text="Selected Component Data:")
        self.__selectedComponentLabel.grid(row=1, sticky="NEWS")
        self.__selectedComponentDataLabel = tk.Label(self.__dataFrame, text="no component \n selected")
        self.__selectedComponentDataLabel.grid(row=2, sticky="EW")
        self.__componentEditLabel = tk.Label(self.__dataFrame, text="")
        self.__componentEditLabel.grid(row=3, sticky="NEWS")
        self.__componentEditStatNumLabel = tk.Label(self.__dataFrame, text="0")
        self.__componentEditStatNumLabel.grid(row=4, column=0, sticky="NS")
        self.__separatingLineLabel = tk.Label(self.__dataFrame, text="--------")
        self.__separatingLineLabel.grid(row=5, sticky="NEWS")
        self.__graphComponentLabel = tk.Label(self.__dataFrame, text="Graph Component Data:")
        self.__graphComponentLabel.grid(row=6, sticky="NEWS")
        self.__graphComponentDataLabel = tk.Label(self.__dataFrame, text="no component \n selected")
        self.__graphComponentDataLabel.grid(row=7, sticky="NEWS")

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
        self.__buttonSelect = tk.Button(self.__toolBarFrame, text="select variable component",
                                        command=self.selectButtonClick)
        self.__buttonSelect.grid(row=1, sticky="NEWS")
        self.__buttonSelectGraphPlotComponent = tk.Button(self.__toolBarFrame, text="select graph component",
                                                          command=self.plotSelectButtonClick)
        self.__buttonSelectGraphPlotComponent.grid(row=2, sticky="NEWS")
        self.__buttonClear = tk.Button(self.__toolBarFrame, text="clear", command=self.clearButtonClick)
        self.__buttonClear.grid(row=3, sticky="NEWS")
        self.__buttonJoin = tk.Button(self.__toolBarFrame, text=chr(176), command=self.joinButtonClick)
        self.__buttonJoin.grid(row=4, sticky="NEWS")
        self.__buttonSource = tk.Button(self.__toolBarFrame, text="+", command=self.sourceButtonClick)
        self.__buttonSource.grid(row=5, sticky="NEWS")
        self.__buttonGround = tk.Button(self.__toolBarFrame, text="-", command=self.groundButtonClick)
        self.__buttonGround.grid(row=6, sticky="NEWS")
        self.__buttonWire = tk.Button(self.__toolBarFrame, text=chr(126), command=self.wireButtonClick)
        self.__buttonWire.grid(row=7, sticky="NEWS")
        self.__buttonResistor = tk.Button(self.__toolBarFrame, text=chr(174), command=self.resistorButtonClick)
        self.__buttonResistor.grid(row=8, sticky="NEWS")

        # creating stats button
        self.__componentUpButton = tk.Button(self.__dataFrame, text="+", command=self.increaseButtonClick)
        self.__componentUpButton.grid(row=4, column=0, sticky="NES")
        self.__componentDownButton = tk.Button(self.__dataFrame, text="-", command=self.decreaseButtonClick)
        self.__componentDownButton.grid(row=4, column=0, sticky="WNS")

        # creating menu button
        self.__helpButton = tk.Button(self.__menuBarFrame, text="HELP", command=self.openHelpWindow)
        self.__helpButton.grid(sticky="NWS")

        # show graphs
        self.plotGraphs()

    def openHelpWindow(self):  # when Help buttion is clicked a new window will open containing instructions on use
        helpWindow = HelpWindow()
        helpWindow.run()

    def gridClick(self, rowNum, colNum):
        self.solveCircuit()
        self.wipeCellColours()  # resets cell colours so they can be updated to the correct colours
        if self.__selectedTool == "select":
            if self.__graphSelectedCell is not None:
                self.__graphSelectedCell.config(bg="grey")  # so we can still see the component which is being
                # plotted after the component to vary has been selected
            self.__selectedComponent = self.__circuitGridClass.getObject(rowNum, colNum)
            self.__buttonMatrix[rowNum][colNum].config(bg="light grey")  # makes it easy to see what is selected by
            # turning the cell light grey
            self.updateDataSelectedComponentText()  # stats of selected component are displayed
            self.updateComponentEditor()  # updates the number in the editor ( up and down arrows allowing the user
            # to change the values of the component)
        elif self.__selectedTool == "plot":
            self.clearDataPoints()  # clears the data prom previous plots
            self.__selectedGraphPlotComponent = self.__circuitGridClass.getObject(rowNum, colNum)
            if self.__selectedGraphPlotComponent.isEdgy():  # only edge type components can be plotted because node
                # types don't have a current
                self.__buttonMatrix[rowNum][colNum].config(bg="grey")  # shows what has been selected
                self.__graphSelectedCell = self.__buttonMatrix[rowNum][colNum]
                self.updateDataGraphComponentText()
                self.updateDataLists()
                self.plotGraphs()
        else:  # otherwise grid is updated with selected component
            if self.__graphSelectedCell is not None:
                self.__graphSelectedCell.config(bg="grey")
                # allows the user to still see which component is being plotted in the graphs
            if self.__selectedTool is None:  # this means the clear tool is selected
                self.__buttonMatrix[rowNum][colNum].config(text="")
                self.__circuitGridClass.updateGrid(rowNum, colNum, self.__selectedTool)
            elif self.__selectedTool == chr(176) or self.__selectedTool == "+" or self.__selectedTool == "-":
                # if the selected tool is a node type
                if rowNum % 2 == 0 and colNum % 2 == 0:
                    # nodes can only be placed in even rows and columns to prevent then from being next to each other
                    self.__buttonMatrix[rowNum][colNum].config(text=self.__selectedTool)
                    self.__circuitGridClass.updateGrid(rowNum, colNum, self.__selectedTool)  # updates the grid class
            elif (rowNum % 2 == 0 and colNum % 2 == 1) or (rowNum % 2 == 1 and colNum % 2 == 0):
                # edges can only be placed in even areas to prevent then from being next to each other
                # this makes calculations easier because it is obvious what they are connected to
                self.__buttonMatrix[rowNum][colNum].config(text=self.__selectedTool)
                self.__circuitGridClass.updateGrid(rowNum, colNum, self.__selectedTool)
        self.__circuitGridClass.solve()  # this is called at the end of every button click to make it seem like it is
        # updating continuously

    def clearDataPoints(self):
        self.__currentDataPoints = []
        self.__voltageDataPoints = []
        self.__timeDataPoints = []

    def updateDataLists(self):
        # fetches data from components and appends them to their respective lists to be plotted
        if self.__selectedGraphPlotComponent is not None and self.__selectedGraphPlotComponent.isEdgy():
            self.__currentDataPoints.append(self.__selectedGraphPlotComponent.getCurrent())
            self.__voltageDataPoints.append(self.__selectedGraphPlotComponent.getPotentialDifference())
            self.__timeDataPoints.append(time.time())
        else:
            self.clearDataPoints()

    def plotGraphs(self):
        fontDict = {'fontsize': 8}  # allows for quick changes to graph text

        IVFig = Figure(figsize=(3, 1), dpi=100)
        IVax = IVFig.add_subplot()
        IVax.set_title("Current Voltage", fontdict=fontDict)
        IVax.tick_params(labelsize=6)
        IVax.plot(self.__voltageDataPoints, self.__currentDataPoints, linewidth=1, markersize=6)
        IVax.set_xlabel("current[A]")
        IVax.set_ylabel("voltage[V]")
        IVCanvas = FigureCanvasTkAgg(IVFig, master=self.__graphFrame)
        IVCanvas.draw()
        IVCanvas.get_tk_widget().grid(row=0, sticky="NEWS")

        ItFig = Figure(figsize=(3, 1), dpi=100)
        Itax = ItFig.add_subplot()
        Itax.set_title("Current time", fontdict=fontDict)
        Itax.tick_params(labelsize=6)
        Itax.plot(self.__timeDataPoints, self.__currentDataPoints, linewidth=1, markersize=6)
        print(self.__timeDataPoints, self.__currentDataPoints)
        Itax.set_xlabel("current[A]")
        Itax.set_ylabel("time[t]")
        ItCanvas = FigureCanvasTkAgg(ItFig, master=self.__graphFrame)
        ItCanvas.draw()
        ItCanvas.get_tk_widget().grid(row=1, sticky="NEWS")

        VtFig = Figure(figsize=(3, 1), dpi=100)
        Vtax = VtFig.add_subplot()
        Vtax.set_title("voltage time", fontdict=fontDict)
        Vtax.tick_params(labelsize=6)
        Vtax.plot(self.__timeDataPoints, self.__voltageDataPoints, linewidth=1, markersize=6)
        Vtax.set_xlabel("voltage[V]")
        Vtax.set_ylabel("time[t]")
        VtCanvas = FigureCanvasTkAgg(VtFig, master=self.__graphFrame)
        VtCanvas.draw()
        VtCanvas.get_tk_widget().grid(row=2, sticky="NEWS")

    def updateDataSelectedComponentText(self):
        # updates the text displayed when a component is selected using values fetched from the object
        try:
            if not self.__selectedComponent.isEdgy():
                potential = self.__selectedComponent.getPotential()
                self.__selectedComponentDataLabel.config(text=f"Potential: {potential}")
            else:
                potentialDifference = self.__selectedComponent.getPotentialDifference()
                current = self.__selectedComponent.getCurrent()
                resistance = self.__selectedComponent.getResistance()
                self.__selectedComponentDataLabel.config(
                    text=f"Res: {resistance} \np.d: {potentialDifference} \nCur: {current} ")
        except:
            self.__selectedComponentDataLabel.config(text="no component \n selected")

    def updateDataGraphComponentText(self):
        # updates the text displayed when a component is selected to be plotted on a graph
        try:
            if not self.__selectedGraphPlotComponent.isEdgy():
                potential = self.__selectedGraphPlotComponent.getPotential()
                self.__graphComponentDataLabel.config(text=f"Potential: {potential}")
            else:
                potentialDifference = self.__selectedGraphPlotComponent.getPotentialDifference()
                current = self.__selectedGraphPlotComponent.getCurrent()
                resistance = self.__selectedGraphPlotComponent.getResistance()
                self.__graphComponentDataLabel.config(
                    text=f"Res: {resistance} \np.d: {potentialDifference} \nCur: {current} ")
        except:
            self.__graphComponentDataLabel.config(text="no component \n selected")

    def updateComponentEditor(self):
        # updates the name of what is being adjusted ( resistance for a resistor etc)
        # and changes the number in the editor (increase/ decrease) section
        try:
            if self.__selectedComponent.isEdgy():  # if edge type object
                if self.__selectedComponent.isWire():
                    self.__componentEditLabel.config(text="Resistivity (ohm metres/10^-8)")
                    self.__componentEditStatNumLabel.config(
                        text=str(self.__selectedComponent.getResistanceProportion()))
                    # the number in the editor is the proportion the original resistance changes by
                else:
                    self.__componentEditLabel.config(text="Resistance (ohms)")
                    self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getResistance()))
            elif not self.__selectedComponent.isEdgy():  # if node type object
                self.__componentEditLabel.config(text="Potential")
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getPotential()))
        except:  # if nothing is selected
            self.__componentEditLabel.config(text="")
            self.__componentEditStatNumLabel.config(text="-")

    def wipeCellColours(self):  # prevents everything from looking selected so new selection is easy to see
        for i in range(len(self.__buttonMatrix)):
            for j in range(len(self.__buttonMatrix[i])):
                self.__buttonMatrix[i][j].config(bg="SystemButtonFace")

    # setting tool based on button clicked
    def selectButtonClick(self):
        self.__selectedTool = "select"
        self.__circuitGridClass.solve()

    def plotSelectButtonClick(self):
        self.__selectedTool = "plot"
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

    # editing component data button commands
    def increaseButtonClick(self):
        try:
            if self.__selectedComponent.isEdgy() and not self.__selectedComponent.isWire():
                self.increaseResistance()
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getResistance()))
            elif self.__selectedComponent.isWire():
                self.increaseResistivity()
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getResistanceProportion()))
            elif self.__selectedComponent.isSource():
                self.increasePotential()
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getPotential()))
            self.solveCircuit()
            self.updateDataSelectedComponentText()
            self.updateDataGraphComponentText()
            self.updateDataLists()
            self.plotGraphs()
        except:
            pass

    def decreaseButtonClick(self):
        try:
            if self.__selectedComponent.isEdgy() and not self.__selectedComponent.isWire():
                self.decreaseResistance()
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getResistance()))
            elif self.__selectedComponent.isWire():
                self.decreaseResistivity()
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getResistanceProportion()))
            elif self.__selectedComponent.isSource():
                self.decreasePotential()
                self.__componentEditStatNumLabel.config(text=str(self.__selectedComponent.getPotential()))
            self.solveCircuit()
            self.updateDataSelectedComponentText()
            self.updateDataGraphComponentText()
            self.updateDataLists()
            self.plotGraphs()
        except:
            pass

    def increaseResistance(self):
        self.__selectedComponent.setResistance(self.__selectedComponent.getResistance() + 1)

    def increaseResistivity(self):
        self.__selectedComponent.setResistance(self.__selectedComponent.getResistanceProportion() + 0.1)

    def decreaseResistance(self):
        if self.__selectedComponent.getResistance() > 1:
            self.__selectedComponent.setResistance(self.__selectedComponent.getResistance() - 1)

    def decreaseResistivity(self):
        if self.__selectedComponent.getResistanceProportion() > 0.1:
            self.__selectedComponent.setResistance(self.__selectedComponent.getResistanceProportion() - 0.1)

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


numberOfGridRows = 15
numberOfGridCols = 15
MainWindow = FrontEndWindow(numberOfGridRows, numberOfGridCols)
MainWindow.run()  # runs the main window
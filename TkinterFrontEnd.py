from AdjacencyList import *

import tkinter as tk

class Window:
    def __init__(self,rows,cols):
        # grid variables
        self.__gridWidth = 500
        self.__gridHight = 500
        self.__gridNumberOfRowCells = rows
        self.__gridNumberOfColumnCells = cols
        self.__toolBarWidth = 100
        self.__menueHight = 10

        # window initialising/configuring
        self.__window = tk.Tk()
        self.__window.title = "buttons please"
        self.__window.rowconfigure(0, minsize=self.__menueHight)
        self.__window.rowconfigure(1, minsize=self.__gridHight)
        self.__window.columnconfigure(0, minsize=self.__toolBarWidth)
        self.__window.columnconfigure(1, minsize=self.__gridWidth)

        # tool status
        self.__selcetedTool = ""

        # frames setup, using hard coded ratios and grid variables to calculate the size of the frames
        self.__menueFrame = tk.Frame(self.__window, bg="light grey", relief=tk.GROOVE, borderwidth=5)
        self.__toolBarFrame = tk.Frame(self.__window, bg="light slate grey", relief=tk.GROOVE, borderwidth=5)
        self.__gridFrame = tk.Frame(self.__window, bg="orange")

        # sizing the grid
        for i in range(self.__gridNumberOfRowCells):
            self.__gridFrame.rowconfigure(i, minsize=int(self.__gridHight / self.__gridNumberOfColumnCells))
        for i in range(self.__gridNumberOfColumnCells):
            self.__gridFrame.columnconfigure(i, minsize=self.__gridWidth / self.__gridNumberOfRowCells)

        # formating frames
        self.__toolBarFrame.columnconfigure(0, minsize=self.__toolBarWidth)
        # self.menueFrame.columnconfigure(0,minsize =10)

        # labels
        self.__toolbarLabel = tk.Label(self.__toolBarFrame, text="TOOL BAR", bg="light slate grey")
        self.__toolbarLabel.grid(row=0)

        # frame griding
        self.__menueFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.__toolBarFrame.grid(row=1, column=0, sticky="NSEW")
        self.__gridFrame.grid(row=1, column=1)

        # making the grid buttons
        self.__gridOfButtons = []
        for row in range(self.__gridNumberOfRowCells):
            self.__buttonRow = []
            for col in range(self.__gridNumberOfColumnCells):
                self.__gridButton = tk.Button(self.__gridFrame, bg="chocolate1",
                                              command=lambda i=row, j=col: self.gridClick(i, j))
                self.__gridButton.grid(row=row, column=col, sticky="NSEW")
                self.__buttonRow.append(self.__gridButton)
            self.__gridOfButtons.append(self.__buttonRow)

        # making toolbar buttons
        self.__buttonPos = tk.Button(self.__toolBarFrame, text="+", command=self.posSelected)
        self.__buttonPos.grid(sticky="NESW")
        self.__buttonNeg = tk.Button(self.__toolBarFrame, text="-", command=self.negSelected)
        self.__buttonNeg.grid(sticky="NESW")
        self.__buttonWire = tk.Button(self.__toolBarFrame, text="wire", command=self.wireSelected)
        self.__buttonWire.grid(sticky="NESW")
        self.__buttonBlank = tk.Button(self.__toolBarFrame, text="clear", command=self.blankSelected)
        self.__buttonBlank.grid(sticky="NESW")

        # menue lables and buttons
        self.__SaveButton = tk.Button(self.__menueFrame, text="SAVE")
        self.__SaveButton.grid(sticky="NSEW")

    # grid button command
    def gridClick(self, i, j):
        self.__gridOfButtons[i][j].config(text=self.__selcetedTool)
        CircuitGrid.updateGrid(i, j, self.__selcetedTool)

    def posSelected(self):
        self.__selcetedTool = "+"

    def negSelected(self):
        self.__selcetedTool = "-"

    def wireSelected(self):
        self.__selcetedTool = "wire"

    def blankSelected(self):
        self.__selcetedTool = ""

    # communicating with other files
    def getGrid(self): # useless for now
        return self.__gridOfButtons

    def run(self):
        self.__window.mainloop()


class Grid():
    def __init__(self,rows,cols):
        self.__grid = []
        for row in range(rows):
            self.row = []
            for col in range(cols):
                self.row.append("")
            self.__grid.append(self.row)


    def updateGrid(self,i,j,selectedTool):
        self.__grid[i][j] = selectedTool
        makeGraphAdjacencyList(self.__grid)

numberOfGridRows = 15
numberOfGridCols =15
CircuitGrid = Grid(numberOfGridRows,numberOfGridCols)
MainWindow = Window(numberOfGridRows,numberOfGridCols)
MainWindow.run()

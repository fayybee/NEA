
import tkinter as tk

class Window:
    def __init__(self):
        # grid variables
        self.gridWidth = 500
        self.gridHight = 500
        self.gridNumberOfRowCells = 15
        self.gridNumberOfColumnCells = 15
        self.toolBarWidth = 100
        self.menueHight = 10

        # window initialising/configuring
        self.window = tk.Tk()
        self.window.title = "buttons please"
        self.window.rowconfigure(0, minsize=self.menueHight)
        self.window.rowconfigure(1, minsize=self.gridHight)
        self.window.columnconfigure(0, minsize=self.toolBarWidth)
        self.window.columnconfigure(1, minsize=self.gridWidth)

        # tool status
        self.selcetedTool = ""

        # frames setup, using hard coded ratios and grid variables to calculate the size of the frames
        self.menueFrame = tk.Frame(self.window, bg="light grey", relief=tk.GROOVE, borderwidth=5)
        self.toolBarFrame = tk.Frame(self.window, bg="light slate grey", relief=tk.GROOVE, borderwidth=5)
        self.gridFrame = tk.Frame(self.window, bg="orange")

        # sizing the grid
        for i in range(self.gridNumberOfRowCells):
            self.gridFrame.rowconfigure(i, minsize=int(self.gridHight / self.gridNumberOfColumnCells))
        for i in range(self.gridNumberOfColumnCells):
            self.gridFrame.columnconfigure(i, minsize=self.gridWidth / self.gridNumberOfRowCells)

        # formating frames
        self.toolBarFrame.columnconfigure(0, minsize=self.toolBarWidth)
        # self.menueFrame.columnconfigure(0,minsize =10)

        # labels
        self.toolbarLabel = tk.Label(self.toolBarFrame, text="TOOL BAR", bg="light slate grey")
        self.toolbarLabel.grid(row=0)

        # frame griding
        self.menueFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.toolBarFrame.grid(row=1, column=0, sticky="NSEW")
        self.gridFrame.grid(row=1, column=1)

        # making the grid buttons
        self.gridOfButtons = []
        for row in range(self.gridNumberOfRowCells):
            self.buttonRow = []
            for col in range(self.gridNumberOfColumnCells):
                self.gridButton = tk.Button(self.gridFrame, bg="chocolate1",
                                            command=lambda i=row, j=col: self.gridClick(i, j))
                self.gridButton.grid(row=row, column=col, sticky="NSEW")
                self.buttonRow.append(self.gridButton)
            self.gridOfButtons.append(self.buttonRow)

        # making toolbar buttons
        self.buttonPos = tk.Button(self.toolBarFrame, text="+", command=self.posSelected)
        self.buttonPos.grid(sticky="NESW")
        self.buttonNeg = tk.Button(self.toolBarFrame, text="-", command=self.negSelected)
        self.buttonNeg.grid(sticky="NESW")
        self.buttonWire = tk.Button(self.toolBarFrame, text="wire", command=self.wireSelected)
        self.buttonWire.grid(sticky="NESW")
        self.buttonBlank = tk.Button(self.toolBarFrame, text="clear", command=self.blankSelected)
        self.buttonBlank.grid(sticky="NESW")

        # menue lables and buttons
        self.SaveButton = tk.Button(self.menueFrame, text="SAVE")
        self.SaveButton.grid(sticky="NSEW")

    # grid button command
    def gridClick(self, i, j):
        self.gridOfButtons[i][j].config(text=self.selcetedTool)
        CircuitGrid.updateGrid()

    def posSelected(self):
        self.selcetedTool = "+"

    def negSelected(self):
        self.selcetedTool = "-"

    def wireSelected(self):
        self.selcetedTool = "wire"

    def blankSelected(self):
        self.selcetedTool = ""

    # communicating with other files
    def getGrid(self):
        return self.gridOfButtons

    def run(self):
        self.window.mainloop()


class Grid():
    def __init__(self):
        self.grid = []

    def updateGrid(self):
        self.grid = MainWindow.getGrid()
        print(self.grid)

CircuitGrid = Grid()
MainWindow = Window()
MainWindow.run()

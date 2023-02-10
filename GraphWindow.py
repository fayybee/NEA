import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)




class GraphWindow:
    def __init__(self):
        self.__graphWindow = tk.Tk()
        self.__graphWindow.geometry("700x500")
        self.__graphWindow.columnconfigure(0, minsize=200)
        self.__graphWindow.columnconfigure(1, minsize=500)
        self.__graphWindow.rowconfigure(0, minsize=500)

        self.__optionsFrame = tk.Frame(self.__graphWindow, bg="light blue", relief=tk.GROOVE, borderwidth=5)
        self.__optionsFrame.columnconfigure(0, minsize=200)
        for i in range(10):
            self.__optionsFrame.rowconfigure(i, minsize=30)
        self.__optionsFrame.grid(column=0, sticky="NEWS")

        self.__optionsFrameLabel = tk.Label(self.__optionsFrame, text="Options", bg="light blue")
        self.__optionsFrameLabel.grid(row=0, column=0, sticky="NEWS")

        self.__plotIVGraphButton = tk.Button(self.__optionsFrame, text="plot IV graph (component)", command=self.plotGraph)
        self.__plotIVGraphButton.grid(row=1, column=0, sticky="NS")

    def plotGraph(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)

        # list of squares
        y = [i ** 2 for i in range(101)]

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(y)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=self.__graphWindow)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       self.__graphWindow)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().grid(column=1)

    def graphWindowRun(self):
        self.__graphWindow.mainloop()


#
#
# plt.plot([7, 2, 5], [3, 4, 5])
# plt.show()

GraphWindow().graphWindowRun()

import tkinter as tk


class HelpWindow:  # user instructions
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.columnconfigure(0,minsize=600)

        self.__introFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__introFrame.grid(row=0, sticky="NEWS")
        self.__introFrame.columnconfigure([0,1],minsize=300)
        self.__introFrameText = tk.Label(self.__introFrame, text="Welcome to Circuit Simulator!")
        self.__introFrameText.grid(row=0,column=0,sticky="W")
        self.__quitButton = tk.Button(self.__introFrame, text="QUIT", command=self.__window.destroy).grid(row=0,column=1,sticky="E")

        self.__gridHelpFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__gridHelpFrame.grid(row=1, sticky="NEWS")
        self.__gridHelpFrameText = tk.Label(self.__gridHelpFrame, text=
        f"GRID\n"
        f"\n"
        f"The grid allows you to build your circuits:\n"
        f"(Node) components (labeled bellow) can be placed on odd rows and columns\n"
        f"(Edge) components (labeled bellow) can be placed on even rows and odd columns or odd columns and even rows\n"
        f"\n"
        f"Example: 0 = nodes , - = edges\n"
        f"\n"
        f"  1   2   3   4   5   6   7   8   9\n"
        f"1  0   -   0   -   0   -   0   -   0  \n"
        f"2  |         |         |         |         |  \n"
        f"3  0   -   0   -   0   -   0   -   0  \n"
        f"4  |         |         |         |         |  \n"
        f"5  0   -   0   -   0   -   0   -   0  \n"
        f"6  |         |         |         |         |  \n"
        f"7  0   -   0   -   0   -   0   -   0  \n"
        f"8  |         |         |         |         |  \n"
        f"9  0   -   0   -   0   -   0   -   0  \n")
        self.__gridHelpFrameText.grid()

        self.__componentKeyFrame = tk.Frame(self.__window, relief=tk.GROOVE, borderwidth=5)
        self.__componentKeyFrame.columnconfigure(0, minsize=600)
        self.__componentKeyFrame.grid(row=2, sticky="NEWS")
        self.__componentKeyFrameText = tk.Label(self.__componentKeyFrame, text=
        f"TOOLS\n"
        f"\n"
        f"(select variable component) = selects the component you want to adjust\n"
        f"(select graph component) = selects the component you want to plot a graph of\n"
        f"\n"
        f"(+) = positive terminal (node), this can be varied\n "
        f"(-) = negative terminal (node), this is always 0 (ground)\n"
        f"({chr(176)}) = join point (node), this can be used to connect two or more edges (no resistance)\n"
        f"({chr(126)}) = wire component (edge), this has very low resistance (x10^-6)\n"
        f"({chr(174)}) = resistor component (edge), this can be varied\n"
        f"({chr(9401)}) = diode component (edge), work function can be changed")
        self.__componentKeyFrameText.grid(column=0)

    def run(self):
        self.__window.mainloop()

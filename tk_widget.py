# https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
# https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

import tkinter as tk
from tkinter import ttk
from dif_solver import DifSolver

from matplotlib import use
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

use("TkAgg")

LARGE_FONT = ("Verdana", 12)


class Program(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry("400x400")

        tk.Tk.wm_title(self, 'Runge-Kutta Differential Equation Solver')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, type, func=None, cond=None):
        frame = self.frames[type]

        # set_attr if frame has such method
        set_attr_method = getattr(frame, "set_attr", None)
        if callable(set_attr_method):
            frame.set_attr(func, cond)
        frame.tkraise()


class StartPage(tk.Frame):

    """
    contains boxes to enter the parameters of the problem
    passes the parameters to PageOne
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Solve Runge Kutta", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        self.ftext = tk.Label(self, text="Insert function (e. g. y' = x*y)")
        self.ftext.pack()
        self.fedit = tk.Entry(self)
        self.fedit.pack(pady=5)

        self.ctext = tk.Label(self, text="Insert condition (e. g. y(0) = 2)")
        self.ctext.pack()
        self.cedit = tk.Entry(self)
        self.cedit.pack(pady=5)

        self.button = ttk.Button(self, text="Solve",
                                 command=self.solve_listener)
        self.button.pack()

    def solve_listener(self):
        func = self.fedit.get()
        cond = self.cedit.get()
        self.controller.show_frame(PageOne, func, cond)


class PageOne(tk.Frame):

    """
    - func - raw input string of derivative equation
    - cond - raw input string of condition
    - difsolver - solver of type DifSolver
    - fig - to draw graph
    - canvas - canvas object
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Result", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        self.res_shower = tk.Text(self, wrap=tk.WORD)
        self.res_shower.pack(pady=5)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.difsolver = None
        self.canvas = None

    def set_attr(self, func=None, cond=None):
        self.func = func
        self.cond = cond
        self.res_shower.delete(1., tk.END)
        self.res_shower.insert(1., self.func + '\n' + self.cond)
        self.res_shower.config(
            width=max(15, 1 + max(len(self.func), len(self.cond))),
            height=1+2
        )
        self.difsolver = DifSolver(equation=self.func, condition=self.cond)
        self.draw_res()

    def draw_res(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        xs, ys = self.difsolver.solve()

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(xs, ys)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, toolbar)

        self.canvas.mpl_connect("key_press_event", on_key_press)

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def main():
    Program().mainloop()


if __name__ == '__main__':
    main()

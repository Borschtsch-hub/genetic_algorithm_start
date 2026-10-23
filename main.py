import tkinter as tk
from tkinter import ttk

from Classes.genetic_algorithm import GeneticAlgorithm
from gui import GUI

#for this program to work you need to have python 3.13.14 and to install 
#bitarray, numpy, matplotlib libraries

#Link to graphical display of formula in Desmos
#https://www.desmos.com/calculator/1arkjjtk6f?tour=sliders&lang=en

class GeneticAlgorithmMain(GeneticAlgorithm):
    def _fitness(self, x):
        return 0.2 * x**4 + 0.3 * x**3 -6.8 * x**2 -7.2 * x + 50

if __name__ == "__main__":

    root = tk.Tk()

    gui = GUI(
        root=root, 
        tkinter_geometry="1280x600", 
        algorithm=GeneticAlgorithmMain()
        )

    root.mainloop()
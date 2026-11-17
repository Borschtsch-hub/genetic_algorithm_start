import tkinter as tk
from tkinter import ttk

from Classes.genetic_algorithm import GeneticAlgorithm
from gui import GUI

import math

#for this program to work you need to have python 3.13.14 and to install 
#bitarray, numpy, matplotlib libraries

#Link to graphical display of formula in Desmos
#https://www.desmos.com/calculator/1arkjjtk6f?tour=sliders&lang=en

class GeneticAlgorithmMain(GeneticAlgorithm):
    def _fitness(self, coords: list[float]):
        x, y = coords[0], coords[1]
        
        A, B = 3, 2
        a, b = 0.5, 0.5
        n, m, l = 2, 2, 2
        
        return A * ((x - a) ** n) + B * ((y - b) ** m) * (math.sin(x) ** l)
    
if __name__ == "__main__":

    root = tk.Tk()

    gui = GUI(
        root=root, 
        tkinter_geometry="1280x600", 
        algorithm=GeneticAlgorithmMain()
        )

    root.mainloop()
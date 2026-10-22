from tkinter import *
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

from Classes.genetic_algorithm import GeneticAlgorithm

class GUI():
    def __init__(self, root: Tk, tkinter_geometry:str, algorithm):
        self.root = root
        
        self.root.title("Genetic algorithm")
        self.root.geometry(tkinter_geometry)

        self.algorithm_template = algorithm
        self.algorithm = None

        self._create_widgets()

    def _create_widgets(self):
        config_frame = ttk.LabelFrame(self.root, text=" Algorithm Parameters ", padding=15)
        config_frame.pack(fill="x", padx=15, pady=10)

        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        #precision
        ttk.Label(config_frame, text="Precision:").grid(row=0, column=0, sticky="w", pady=5)
        self.precision_entry = ttk.Entry(config_frame, width=30)
        self.precision_entry.insert(0, "0.001")
        self.precision_entry.grid(row=0, column=1, padx=10, pady=5)

        #range
        ttk.Label(config_frame, text="Range [a, b]:").grid(row=1, column=0, sticky="w", pady=5)

        range_subframe = ttk.Frame(config_frame)
        range_subframe.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.range_a_entry = ttk.Entry(range_subframe, width=13)
        self.range_a_entry.insert(0, "-5.12")
        self.range_a_entry.pack(side="left")

        self.range_b_entry = ttk.Entry(range_subframe, width=13)
        self.range_b_entry.insert(0, "5.12")
        self.range_b_entry.pack(side="left",padx=10)

        #population
        ttk.Label(config_frame, text="Population %:").grid(row=2, column=0, sticky="w", pady=5)
        self.pop_pct_entry = ttk.Entry(config_frame, width=15)
        self.pop_pct_entry.insert(0, "5.0")
        self.pop_pct_entry.grid(row=2, column=1, padx=10, pady=5)

        #mutation
        ttk.Label(config_frame, text="Mutation Chance %:").grid(row=3, column=0, sticky="w", pady=5)
        self.mutation_pct_entry = ttk.Entry(config_frame, width=15)
        self.mutation_pct_entry.insert(0, "5.0")
        self.mutation_pct_entry.grid(row=3, column=1, padx=10, pady=5)

        #buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        self.init_btn = ttk.Button(btn_frame, text="Initialize Population", command=self.initialize_algorithm)
        self.init_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.step_btn = ttk.Button(btn_frame, text="Next Generation", command=self.next_generation, state="disabled")
        self.step_btn.pack(side="left", expand=True, fill="x", padx=2)

        #output
        log_frame = ttk.LabelFrame(self.root, text="Console", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.log_text = Text(log_frame, height=12, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        #plot
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def initialize_algorithm(self):
        try:
            precision = float(self.precision_entry.get())
            range_a = float(self.range_a_entry.get())
            range_b = float(self.range_b_entry.get())
            pop_pct = float(self.pop_pct_entry.get())
            mutation_pct = float(self.mutation_pct_entry.get())

            if range_a >= range_b:
                raise ValueError("Range 'a' must be less than range 'b'.")

            algo_class = type(self.algorithm_template)
            self.algorithm = algo_class(
                _range=(range_a, range_b),
                _precision=precision,
                _population_percentage=pop_pct,
                _mutation_chance_percentage=mutation_pct
            )

            self.algorithm.create_start_pop()
            self.algorithm.calculate_phenotypes()
            self.algorithm.first_population()

            self.log_text.delete("1.0", END)
            self.log_text.insert(END, f"Range: {self.algorithm._range}\n")
            self.log_text.insert(END, f"Population Size: {self.algorithm._population_size}\n")
            self.log_text.insert(END, f"Initial Best:\n  {self.algorithm.local_minimum}\n\n")

            self.plotter()
            self.step_btn.config(state="normal")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input values: {e}")

    def next_generation(self):
        if not self.algorithm:
            return

        self.algorithm.new_generation()

        self.log_text.insert(END, f"{self.algorithm.out()}\n")
        self.log_text.insert(END, f"Best: {self.algorithm.local_minimum}\n\n")
        self.log_text.see(END)

        self.plotter()

    def plotter(self):
        self.ax.clear()

        range_a, range_b = self.algorithm._range

        x_vals = np.linspace(range_a, range_b, 300)
        y_vals = [self.algorithm._fitness(val) for val in x_vals]
        
        self.ax.plot(x_vals, y_vals, color="blue", label="f(x)", linewidth=2)

        pop_x = [p.value for p in self.algorithm.phenotype_vector]
        pop_y = [p.fitness for p in self.algorithm.phenotype_vector]
        self.ax.scatter(pop_x, pop_y, color="orange", label="Population", zorder=5)

        best_x = self.algorithm.local_minimum.value
        best_y = self.algorithm.local_minimum.fitness
        self.ax.scatter([best_x], [best_y], color="red", s=120, label=f"Best: {best_x:.2f}", zorder=10)

        x_padding = (range_b - range_a) * 0.05
        self.ax.set_xlim(range_a - x_padding, range_b + x_padding)

        y_min, y_max = min(y_vals), max(y_vals)
        y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
        self.ax.set_ylim(y_min - y_padding, y_max + y_padding)

        self.ax.set_title("Genetic Algorithm Optimization")
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.legend(loc="upper right")
        self.ax.grid(True, linestyle="--", alpha=0.6)
        
        self.canvas.draw()
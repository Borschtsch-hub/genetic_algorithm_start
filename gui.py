from tkinter import *
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

from Classes.genetic_algorithm import GeneticAlgorithm

class GUI():
    def __init__(self, root: Tk, tkinter_geometry: str, algorithm):
        self.root = root
        
        self.root.title("Genetic Algorithm - N-Dimensional")
        self.root.geometry(tkinter_geometry)

        self.algorithm_template = algorithm
        self.algorithm = None

        self._create_widgets()

    def _create_widgets(self):
        config_frame = ttk.LabelFrame(self.root, text=" Algorithm Parameters ", padding=15)
        config_frame.pack(fill="x", padx=15, pady=10)

        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        row_idx = 0

        # Dimensions entry
        ttk.Label(config_frame, text="Dimensions (n):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.dim_entry = ttk.Entry(config_frame, width=30)
        self.dim_entry.insert(0, "2")
        self.dim_entry.grid(row=row_idx, column=1, padx=10, pady=5)
        self.dim_entry.bind("<FocusOut>", self._update_dynamic_fields)
        row_idx += 1

        # Precision
        ttk.Label(config_frame, text="Precision (comma-sep or single):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.precision_entry = ttk.Entry(config_frame, width=30)
        self.precision_entry.insert(0, "0.001")
        self.precision_entry.grid(row=row_idx, column=1, padx=10, pady=5)
        row_idx += 1

        # Dynamic Ranges container frame
        self.ranges_frame = ttk.LabelFrame(config_frame, text=" Ranges [a, b] per dimension ", padding=10)
        self.ranges_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=5)
        row_idx += 1

        self.range_entries = []
        self._rebuild_range_entries(2) # Default to 2 dimensions

        # Population percentage
        ttk.Label(config_frame, text="Population %:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.pop_pct_entry = ttk.Entry(config_frame, width=30)
        self.pop_pct_entry.insert(0, "5.0")
        self.pop_pct_entry.grid(row=row_idx, column=1, padx=10, pady=5)
        row_idx += 1

        # Mutation percentage
        ttk.Label(config_frame, text="Mutation Chance %:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.mutation_pct_entry = ttk.Entry(config_frame, width=30)
        self.mutation_pct_entry.insert(0, "5.0")
        self.mutation_pct_entry.grid(row=row_idx, column=1, padx=10, pady=5)
        row_idx += 1

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        self.init_btn = ttk.Button(btn_frame, text="Initialize Population", command=self.initialize_algorithm)
        self.init_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.step_btn = ttk.Button(btn_frame, text="Next Generation", command=self.next_generation, state="disabled")
        self.step_btn.pack(side="left", expand=True, fill="x", padx=2)

        # Output console
        log_frame = ttk.LabelFrame(self.root, text="Console", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.log_text = Text(log_frame, height=10, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        # Plot frame setup
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def _update_dynamic_fields(self, event=None):
        try:
            n = int(self.dim_entry.get())
            if n < 1:
                return
            self._rebuild_range_entries(n)
        except ValueError:
            pass

    def _rebuild_range_entries(self, n: int):
        for widget in self.ranges_frame.winfo_children():
            widget.destroy()
        
        self.range_entries = []
        for i in range(n):
            ttk.Label(self.ranges_frame, text=f"x{i+1} [a, b]:").grid(row=i, column=0, sticky="w", pady=2)
            
            subframe = ttk.Frame(self.ranges_frame)
            subframe.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            e_a = ttk.Entry(subframe, width=10)
            e_a.insert(0, "-5.12")
            e_a.pack(side="left")
            
            e_b = ttk.Entry(subframe, width=10)
            e_b.insert(0, "5.12")
            e_b.pack(side="left", padx=5)
            
            self.range_entries.append((e_a, e_b))

    def initialize_algorithm(self):
        try:
            n = int(self.dim_entry.get())
            
            raw_prec = self.precision_entry.get().strip()
            if "," in raw_prec:
                precision = [float(p.strip()) for p in raw_prec.split(",")]
            else:
                precision = float(raw_prec)

            ranges = []
            for e_a, e_b in self.range_entries:
                a = float(e_a.get())
                b = float(e_b.get())
                if a >= b:
                    raise ValueError(f"Range 'a' must be less than 'b' for all dimensions.")
                ranges.append((a, b))

            pop_pct = float(self.pop_pct_entry.get())
            mutation_pct = float(self.mutation_pct_entry.get())

            algo_class = type(self.algorithm_template)
            self.algorithm = algo_class(
                _range=ranges,
                _precision=precision,
                _population_percentage=pop_pct,
                _mutation_chance_percentage=mutation_pct
            )

            self.algorithm.create_start_pop()
            self.algorithm.calculate_phenotypes()
            self.algorithm.first_population()

            self.log_text.delete("1.0", END)
            self.log_text.insert(END, f"Dimensions: {n}\n")
            self.log_text.insert(END, f"Ranges: {self.algorithm._ranges}\n")
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

        self.log_text.insert(END, f"--- Generation {self.algorithm.generation} ---\n")
        self.log_text.insert(END, f"Best: {self.algorithm.local_minimum}\n\n")
        self.log_text.see(END)

        self.plotter()

    def plotter(self):
        self.fig.clear()
        
        if self.algorithm.dimensions == 2:
            self.ax = self.fig.add_subplot(111, projection='3d')
            
            r1, r2 = self.algorithm._ranges[0], self.algorithm._ranges[1]
            x_vals = np.linspace(r1[0], r1[1], 40)
            y_vals = np.linspace(r2[0], r2[1], 40)
            X, Y = np.meshgrid(x_vals, y_vals)
         
            Z = np.zeros_like(X)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    Z[i, j] = self.algorithm._fitness([X[i, j], Y[i, j]])
            
            self.ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.5, edgecolor='none')
            
            pop_x = [p.values[0] for p in self.algorithm.phenotype_vector]
            pop_y = [p.values[1] for p in self.algorithm.phenotype_vector]
            pop_z = [p.fitness for p in self.algorithm.phenotype_vector]
            
            self.ax.scatter(pop_x, pop_y, pop_z, color="orange", label="Population", s=35, depthshade=True)

            best_x = self.algorithm.local_minimum.values[0]
            best_y = self.algorithm.local_minimum.values[1]
            best_z = self.algorithm.local_minimum.fitness
            self.ax.scatter([best_x], [best_y], [best_z], color="red", s=120, label="Best", depthshade=False)
            
            self.ax.set_title("3D Optimization Landscape")
            self.ax.set_xlabel("x1")
            self.ax.set_ylabel("x2")
            self.ax.set_zlabel("Fitness")
            self.ax.legend(loc="upper left")
        
        else:
            self.ax = self.fig.add_subplot(111)
            if self.algorithm.dimensions == 1:
                r = self.algorithm._ranges[0]
                x_vals = np.linspace(r[0], r[1], 200)
                y_vals = [self.algorithm._fitness([x]) for x in x_vals]
                self.ax.plot(x_vals, y_vals, color="blue", label="f(x)")
                
                pop_x = [p.values[0] for p in self.algorithm.phenotype_vector]
                pop_y = [p.fitness for p in self.algorithm.phenotype_vector]
                self.ax.scatter(pop_x, pop_y, color="orange", label="Population")
                
                best_x = self.algorithm.local_minimum.values[0]
                best_y = self.algorithm.local_minimum.fitness
                self.ax.scatter([best_x], [best_y], color="red", s=100, label="Best")
                self.ax.set_title("1D Optimization")
            else:
                self.ax.text(0.5, 0.5, f"Search Space: {self.algorithm.dimensions} Dimensions", 
                             horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, fontsize=12)
                self.ax.set_title(f"N-Dimensional Optimization ({self.algorithm.dimensions}D)")

        self.canvas.draw()
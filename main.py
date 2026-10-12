from bitarray import *
from bitarray.util import ba2int, int2ba
from Classes.phenotype import Phenotype
from Classes.genetic_algorithm import GeneticAlgorithmTest,GeneticAlgorithm

#Link to graphical display of formula in Desmos
#https://www.desmos.com/calculator/1arkjjtk6f?tour=sliders&lang=en

class GeneticAlgorithmMain(GeneticAlgorithm):
    def _fitness(self, x):
        return 0.2 * x**4 + 0.3 * x**3 -6.8 * x**2 -7.2 * x + 50

def input_settings():
    _show_output_str = input("Show output table [y/n]: ")
    _show_output = _show_output_str.strip().lower() in {"y", "yes"}
    return _show_output

def input_data()->tuple:
    _precison = float(input("Input precison(float like 0.01): "))
    
    _range = []
    _range.append(float(input("Input range a(float): ")))
    _range.append(float(input("Input range b(float): ")))

    _start_pop_percentage = float(input("Input population percentage(float): "))

    _mutation_chance_percentage = float(input("Input mutation chance percentage(float): "))#percentage not absolute value it will be divided by 100

    return (_precison, tuple(_range), _start_pop_percentage, _mutation_chance_percentage)

if __name__ == "__main__":

    show_output = input_settings()

    _precision, _range, _pop_percentage, _mutation_chance_percentage = input_data()

    algorithm = GeneticAlgorithmMain(_range, _precision, _pop_percentage, _mutation_chance_percentage)

    #algorithm = GeneticAlgorithmTest()

    algorithm.create_start_pop()

    algorithm.calculate_phenotypes()

    print(algorithm)
    print("")
    print(algorithm.out())

    algorithm.first_population()

    iteration = 0

    while True:
        algorithm.new_generation()
        if show_output:
            print(algorithm.out())

        print(f"Iteration: {iteration}\nLocal minimum:\n\t{algorithm.local_minimum}")
        iteration+=1
        inp = input("")
        if inp in {"q","quit","exit"}:
            break
        if inp == "restart":
            iteration = 0
            algorithm.create_start_pop()
            algorithm.calculate_phenotypes()
            algorithm.first_population()
        if inp == "status":
            print(algorithm)
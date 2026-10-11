from bitarray import *
from bitarray.util import ba2int, int2ba
from Classes.phenotype import Phenotype
from Classes.genetic_algorithm import GeneticAlgorithmTest,GeneticAlgorithm


def get_next_pop():
    pass

def input_data()->tuple:
    _precison = float(input("Input precison: "))
    
    _range = []
    _range.append(float(input("Input range a: ")))
    _range.append(float(input("Input range b: ")))

    _start_pop_percentage = float(input("Input population percentage: "))

    return (_precison, tuple(_range), _start_pop_percentage)

if __name__ == "__main__":

    #_precision, _range, _pop_percentage = input_data()

    #algorithm = GeneticAlgorithmTest(_range, _precision, _pop_percentage)

    algorithm = GeneticAlgorithmTest()

    algorithm.create_start_pop()

    algorithm.calculate_phenotypes()

    print(algorithm)
    print("")
    print(algorithm.out())

    algorithm.first_population()

    print()
    print(algorithm.out())
    
    print()
    algorithm.next_population()
    print(algorithm.out())

    print()
    algorithm.new_generation()
    print(algorithm.out())
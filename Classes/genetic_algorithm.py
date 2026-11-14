from abc import abstractmethod
from bitarray import bitarray
from Classes.phenotype import Phenotype
from Classes.crossover import Crossover
from Classes.mutator import Mutator

import math
import copy
import random

def _bit_move(bitarr: bitarray):
    for i in range(len(bitarr) - 1, -1, -1):
        if bitarr[i] == 0:
            bitarr[i] = 1  
            break
        else:
            bitarr[i] = 0

class GeneticAlgorithm:
    _crossover = Crossover()
    _mutator = None
    local_minimum = None
    
    phenotype_vector:list[Phenotype] = []

    def __init__(self, _range = [(-15, 16)], _precision = [0.1], _population_percentage: float = 20.0, _mutation_chance_percentage: float = 0.03):
        if isinstance(_range, tuple) and len(_range) == 2 and isinstance(_range[0], (int, float)):
            self._ranges = [_range]
        else:
            self._ranges = list(_range)
            
        if isinstance(_precision, (int, float)):
            self._precisions = [_precision] * len(self._ranges)
        else:
            self._precisions = list(_precision)
            
        self.dimensions = len(self._ranges)
        
        self._bit_lengths = []
        self._dimension_start_pops = []
        self.generation: int = 0
        
        total_start_pop = 1.0
        for i in range(self.dimensions):
            r_span = abs(self._ranges[i][1] - self._ranges[i][0])
            prec = self._precisions[i]
            dim_pop = r_span / prec
            self._dimension_start_pops.append(dim_pop)
            total_start_pop *= dim_pop
            
            bits = 1
            for b in range(1, 32):
                if 2**b >= dim_pop:
                    bits = b
                    break
            self._bit_lengths.append(bits)

        max_dim_pop = max(self._dimension_start_pops)
        self._population_size = int(round(max_dim_pop * (_population_percentage / 100)))
        self._mutator = Mutator(_mutation_chance_percentage)

    def full_input(self, _range = [(-15, 16)], _precision = [0.1], _population_percentage: float = 20.0, _mutation_chance_percentage: float = 0.03):
        self.__init__(_range, _precision, _population_percentage, _mutation_chance_percentage)

    def append(self, obj: Phenotype):
        self.phenotype_vector.append(obj)

    @abstractmethod
    def _fitness(self, coords: list[float]):
        pass

    def calculate_phenotypes(self):
        left_borders = [r[0] for r in self._ranges]
        for phenotype in self.phenotype_vector:
            phenotype.calculate_values(left_borders, self._precisions, self._bit_lengths)
            phenotype.load_phenotype(self._fitness(phenotype.values))

    def __str__(self):
        return f"Dimensions: {self.dimensions}\nRanges: {self._ranges}\nPrecisions: {self._precisions}\nBit lengths per dim: {self._bit_lengths}\nPopulation size: {self._population_size}"
    
    def create_start_pop(self):
        total_bits = sum(self._bit_lengths)
        max_steps = int(max(self._dimension_start_pops))
        
        bit_array = bitarray(total_bits)
        bit_array.setall(0)
        
        for i in range(0, max_steps):
            self.append(Phenotype(copy.copy(bit_array)))
            _bit_move(bit_array)        

    def out(self):
        retstr = ""
        for phenotype in self.phenotype_vector:
            retstr += f"{phenotype}\n"
        return retstr

    def first_population(self):
        rand = set()
        while len(rand) < self._population_size and len(rand) < len(self.phenotype_vector):
            rand_num = random.randint(0, len(self.phenotype_vector) - 1)
            rand.add(rand_num) 
        
        new_pop = []
        while rand:
            new_pop.append(self.phenotype_vector[rand.pop()])
        
        self.phenotype_vector.clear()
        while new_pop: 
            self.append(new_pop.pop())
            
        self.local_minimum = copy.deepcopy(self.phenotype_vector[0])    

    def next_population(self):
        self.generation += 1
        coefficient_sum = 0.0

        for phenotype in self.phenotype_vector:
            coefficient_sum += phenotype.coefficient
        
        expected_parent = []
        for phenotype in self.phenotype_vector:
            expected_parent.append((phenotype.coefficient / coefficient_sum) * self._population_size)

        parent_sum = 0
        extra = []
        for i in range(0, len(expected_parent)):
            extra.append(expected_parent[i] - round(expected_parent[i]))
            expected_parent[i] = round(expected_parent[i])
            parent_sum += expected_parent[i]

        while parent_sum < self._population_size:
            largest = max(extra)
            index = extra.index(largest)
            expected_parent[index] += 1
            parent_sum += 1
            extra[index] -= 1

        extra.clear()
        index = 0
        while parent_sum:
            if index >= len(expected_parent):
                index = 0
            
            if expected_parent[index]:
                expected_parent[index] -= 1
                parent_sum -= 1
                extra.append(copy.deepcopy(self.phenotype_vector[index]))
                
            index += 1

        self.phenotype_vector = extra

    def new_generation(self):
        self.next_population()

        for i in range(0, len(self.phenotype_vector) - 1, 2):
            self._crossover.crossover(
                (self.phenotype_vector[i].genes, self.phenotype_vector[i+1].genes),
                self._bit_lengths
            )

        if random.randint(1, 3) < 3:
            self._mutator.mutate_random_genes(self.phenotype_vector)

        self.calculate_phenotypes()
        self._get_minimum()

    def _get_minimum(self):
        for phenotype in self.phenotype_vector:
            if phenotype.fitness < self.local_minimum.fitness:
                self.local_minimum = copy.deepcopy(phenotype)


class GeneticAlgorithmTest(GeneticAlgorithm):
    def _fitness(self, coords: list[float]):
        return sum(x**2 for x in coords)
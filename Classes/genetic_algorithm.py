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

    def __init__(self,_range:tuple = (-15,16), _precision:float = 0.1, _population_percentage:float= 20.0, _mutation_chance_percentage:float = 0.03):
        self._range = _range
        self._full_range = abs(_range[1] - _range[0])
        self._precision = _precision
        self._start_pop = self._full_range/_precision
        self._population_size = int(round((self._start_pop)*(_population_percentage/100)))
        self._mutator = Mutator(_mutation_chance_percentage)

    def append(self, object: Phenotype):
        self.phenotype_vector.append(object)

    def get_bit_in_chromosome(self):
        for i in range(1,32):
            if 2**i >= self._start_pop:
                return i
        return 0

    @abstractmethod
    def _fitness(self, x:float):
        pass

    def calculate_phenotypes(self):
        for phenotype in self.phenotype_vector:
            phenotype.calculate_value(self._range[0],self._precision)
            phenotype.load_phenotype(self._fitness(phenotype.value))

    def __str__(self):
        return f"range a-b: {self._range}\nstart_pop: {self._start_pop}\nprecision: {self._precision}\nammount of chromosomes: {len(self.phenotype_vector)}\npopulation size: {self._population_size}"
    
    def create_start_pop(self):
        bit_array = bitarray(self.get_bit_in_chromosome())
        for i in range(0, int(self._start_pop)):
            self.append(Phenotype(i,copy.copy(bit_array)))
            _bit_move(bit_array)        

    def out(self):
        retstr = f""
        for phenotype in self.phenotype_vector:
            retstr += f"{phenotype}\n"
        return retstr

    def first_population(self):
        rand = set()
        while len(rand)<self._population_size:
            rand_num = random.randint(0,len(self.phenotype_vector)-1)
            if rand_num in rand:
                pass
            else: 
                rand.add(rand_num) 
        
        new_pop = []
        while rand:
            new_pop.append(self.phenotype_vector[rand.pop()])
        
        self.phenotype_vector.clear()
        while new_pop: 
            self.append(new_pop.pop())
            
        self.local_minimum = copy.deepcopy(self.phenotype_vector[0])    

    def next_population(self):
        coefficient_sum = 0.0

        for phenotype in self.phenotype_vector:
            coefficient_sum += phenotype.coefficient
        
        expected_parent = []
        for phenotype in self.phenotype_vector:
            expected_parent.append((phenotype.coefficient/coefficient_sum)*self._population_size)

        parent_sum = 0
        extra = []
        for i in range(0,len(expected_parent)):
            extra.append(expected_parent[i]-round(expected_parent[i]))
            expected_parent[i] = round(expected_parent[i])
            parent_sum += expected_parent[i]

        while parent_sum < self._population_size:
            largest = max(extra)
            index = extra.index(largest)
            expected_parent[index] += 1
            parent_sum +=1
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

        for i in range(0,len(self.phenotype_vector)-1,2):
            self._crossover.crossover((self.phenotype_vector[i].genes,self.phenotype_vector[i+1].genes))

        if random.randint(1,3)<3:
            self._mutator.mutate_random_genes(self.phenotype_vector)

        self.calculate_phenotypes()

        self._get_minimum()

    def _get_minimum(self):
        for phenotype in self.phenotype_vector:
            if phenotype.fitness < self.local_minimum.fitness:
                self.local_minimum:Phenotype = copy.deepcopy(phenotype)
        



class GeneticAlgorithmTest(GeneticAlgorithm):
    def _fitness(self, x:float):
        return x*x
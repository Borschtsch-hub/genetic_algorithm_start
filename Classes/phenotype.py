from bitarray import *
from bitarray.util import ba2int
from abc import abstractmethod

class Phenotype:   
    def __init__(self, genes: bitarray):
        self.genes = genes
        self.indices = []
        self.values = []
        self.fitness = None
        self.coefficient = None
    
    def load_phenotype(self, fitness):
        self.fitness = fitness
        try:
            self.coefficient = 1 / abs(fitness)
        except ZeroDivisionError:
            self.coefficient = 1.0

    def calculate_values(self, left_borders: list[float], precisions: list[float], bit_lengths: list[int]):
        self.indices.clear()
        self.values.clear()
        start_idx = 0
        
        for i, length in enumerate(bit_lengths):

            chunk = self.genes[start_idx : start_idx + length]
            idx = ba2int(chunk)
            self.indices.append(idx)
            
            # Map index to the coordinate value within the given range and precision
            val = left_borders[i] + (idx * precisions[i])
            self.values.append(val)
            
            start_idx += length

    def __str__(self):
        return f"indices: {self.indices}, values: {[round(v, 4) for v in self.values]}, f: {self.fitness:.4f}, c: {self.coefficient:.4f}"

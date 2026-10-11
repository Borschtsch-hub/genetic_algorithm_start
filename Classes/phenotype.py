from bitarray import *
from abc import abstractmethod

class Phenotype:
    value = None
    fitness = None
    coefficient = None
    
    def __init__(self, index:int, genes:bitarray, ):
        self.index = index
        self.genes = genes
    

    def _load_phenotype(self, fitness):
        self.fitness = fitness
        try:
            self.coefficient = 1/fitness
        except ZeroDivisionError:
            self.coefficient = 0.0

    def _calculate_value(self,left_border):
        self.value = self.index + left_border

    def __str__(self):
        return f"i: {self.index}, v: {self.value}, g: {self.genes.unpack(zero=b'0',one=b'1')}, f: {self.fitness}, c: {self.coefficient}"

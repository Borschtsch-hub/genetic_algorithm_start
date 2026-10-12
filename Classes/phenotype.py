from bitarray import *
from bitarray.util import ba2int
from abc import abstractmethod

class Phenotype:   
    def __init__(self, index:int, genes:bitarray, ):
        self.index = index
        self.genes = genes
        value = None
        fitness = None
        coefficient = None
    

    def load_phenotype(self, fitness):
        self.fitness = fitness
        try:
            self.coefficient = 1/abs(fitness)
        except ZeroDivisionError:
            self.coefficient = 1.0

    def _calculate_index(self):
        self.index = ba2int(self.genes)

    def calculate_value(self,left_border:float,precision:float):
        self._calculate_index()
        self.value = self.index* precision - abs(left_border)

    def __str__(self):
        return f"i: {self.index}, v: {self.value}, g: {self.genes.unpack(zero=b'0',one=b'1')}, f: {self.fitness}, c: {self.coefficient}"

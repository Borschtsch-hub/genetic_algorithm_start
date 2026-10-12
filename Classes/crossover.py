from Classes.phenotype import Phenotype
from bitarray import bitarray
import random

class Crossover:
    def crossover(self, parent: tuple[bitarray])-> tuple[bitarray]:
        point = random.randint(0, len(parent[0])-1)
    
        while point <= len(parent[0])-1:
            (parent[0][point], parent[1][point]) = (parent[1][point], parent[0][point])
            point += 1

        
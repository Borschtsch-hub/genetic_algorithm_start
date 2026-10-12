import random
import math
from Classes.phenotype import Phenotype

class Mutator:
    _genes_amount: int = None

    def __init__(self, mutation_chance_percentage: float):
        self._mutation_chance:float = mutation_chance_percentage/100  #sets absolute mutation chance

    def _calculate_mutation_rate(self, phenotype_list:list[Phenotype]):
        if not self._genes_amount:
            self._genes_amount = len(phenotype_list) * len(phenotype_list[0].genes)
        
        expected_mutations = self._genes_amount * self._mutation_chance
        
        # Probabilistic rounding: e.g., 0.3 has a 30% chance to become 1, else 0
        floor_val = math.floor(expected_mutations)
        fraction = expected_mutations - floor_val
        self._mutation_rate = floor_val + (1 if random.random() < fraction else 0)

    def mutate_random_genes(self, phenotype_list:list[Phenotype]):
        self._calculate_mutation_rate(phenotype_list)

        for i in range(0, self._mutation_rate):
            target_phenotype = phenotype_list[random.randint(0, len(phenotype_list) - 1)]
            target_bit = random.randint(0, len(target_phenotype.genes) - 1)
            target_phenotype.genes.invert(target_bit)
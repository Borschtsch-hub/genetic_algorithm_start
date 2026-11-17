from Classes.phenotype import Phenotype
from bitarray import bitarray
import random

class Crossover:
    def crossover(self, parents: tuple[bitarray, bitarray], bit_lengths: list[int] = None):
        p1, p2 = parents
        
        if not bit_lengths or len(bit_lengths) <= 1:
            length = len(p1)
            if length <= 1:
                return
            points = sorted(random.sample(range(1, length), min(2, length - 1)))
            points = [0] + points + [length]
            
            swap = False
            for i in range(len(points) - 1):
                if swap:
                    p1[points[i]:points[i+1]], p2[points[i]:points[i+1]] = \
                        p2[points[i]:points[i+1]].copy(), p1[points[i]:points[i+1]].copy()
                swap = not swap
            return

        current_idx = 0
        for length in bit_lengths:
            if length > 1:
                cut = random.randint(1, length - 1)
                p1[current_idx + cut : current_idx + length], p2[current_idx + cut : current_idx + length] = (
                    p2[current_idx + cut : current_idx + length].copy(),
                    p1[current_idx + cut : current_idx + length].copy(),
                )
            current_idx += length
        
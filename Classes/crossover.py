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
        swap = random.choice([True, False])
        
        for length in bit_lengths:
            next_idx = current_idx + length
            if swap:
                temp = p1[current_idx:next_idx].copy()
                p1[current_idx:next_idx] = p2[current_idx:next_idx]
                p2[current_idx:next_idx] = temp
            current_idx = next_idx
            swap = not swap
        
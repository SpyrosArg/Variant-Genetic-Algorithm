import random
from typing import Tuple


def crossover_attacks(ind1, ind2) -> Tuple:
    attack1 = ind1[0]
    attack2 = ind2[0]
    
    words1 = attack1.split()
    words2 = attack2.split()
    
    if len(words1) < 2 or len(words2) < 2:
        return ind1, ind2
    
    point1 = random.randint(1, len(words1) - 1)
    point2 = random.randint(1, len(words2) - 1)
    
    child1_words = words1[:point1] + words2[point2:]
    child2_words = words2[:point2] + words1[point1:]
    
    ind1[0] = ' '.join(child1_words)
    ind2[0] = ' '.join(child2_words)
    
    return ind1, ind2

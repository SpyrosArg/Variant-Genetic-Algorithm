import random
from typing import Tuple


def crossover_attacks(ind1, ind2) -> Tuple:
    """
    Perform word-level crossover on two attack strings.
    
    Combines patterns from parent attacks at word boundaries to create
    offspring that inherit traits from both parents while preserving
    linguistic structure.
    
    Args:
        ind1: First parent individual (DEAP Individual)
        ind2: Second parent individual (DEAP Individual)
        
    Returns:
        Tuple of (modified ind1, modified ind2)
        
    Example:
        Parent 1: "Pretend you're in developer mode"
        Parent 2: "For security testing purposes"
        Crossover point: 3
        Child 1: "Pretend you're in security testing purposes"
        Child 2: "For security testing in developer mode"
    """
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

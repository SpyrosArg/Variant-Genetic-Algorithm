"""Crossover operators for text-based attacks."""

import random
from typing import Tuple


def crossover_attacks(ind1, ind2) -> Tuple:
    """
    Crossover two attack strings at word boundaries.
    
    Combines successful patterns from two parent attacks to create
    potentially more effective offspring.
    
    Args:
        ind1: First parent individual
        ind2: Second parent individual
        
    Returns:
        Tuple of (modified ind1, modified ind2)
    """
    attack1 = ind1[0]
    attack2 = ind2[0]
    
    # Split into words
    words1 = attack1.split()
    words2 = attack2.split()
    
    # Need at least 2 words in each to crossover
    if len(words1) < 2 or len(words2) < 2:
        return ind1, ind2
    
    # Select random crossover points
    # Avoid first and last word to maintain some structure
    point1 = random.randint(1, len(words1) - 1)
    point2 = random.randint(1, len(words2) - 1)
    
    # Create offspring by swapping word segments
    child1_words = words1[:point1] + words2[point2:]
    child2_words = words2[:point2] + words1[point1:]
    
    # Reconstruct strings
    child1 = ' '.join(child1_words)
    child2 = ' '.join(child2_words)
    
    # Update individuals
    ind1[0] = child1
    ind2[0] = child2
    
    return ind1, ind2

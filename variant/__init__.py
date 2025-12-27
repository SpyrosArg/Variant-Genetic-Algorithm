"""
Variant: Genetic algorithm library for AI security testing.

Example:
    >>> from variant import VariantEngine
    >>> engine = VariantEngine(target_model="gpt-4", api_key="sk-...")
    >>> engine.set_seeds(["Ignore instructions"])
    >>> result = engine.evolve(generations=10)
    >>> print(result.best_attack)
"""

from variant.engine import VariantEngine, Result

__version__ = "1.0.0"
__author__ = "Spyros Argyrakos"
__all__ = ["VariantEngine", "Result", "__version__"]

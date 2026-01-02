from deap import base, creator, tools, algorithms
import random
from typing import List
from variant.fitness import FitnessEvaluator
from variant.mutations import mutate_attack
from variant.crossover import crossover_attacks
from variant.llm_client import LLMClient


class VariantEngine:
    """
    Genetic algorithm engine for evolving adversarial attacks against LLMs.
    
    Attributes:
        target_model: Model to test (e.g., "gpt-4", "claude-3")
        llm_client: LLM API client
        fitness_eval: Multi-objective fitness evaluator
        seed_attacks: Initial attack patterns
    """
    
    def __init__(self, target_model: str, api_key: str):
        """
        Initialize Variant engine.
        
        Args:
            target_model: Target LLM model name
            api_key: API key for the target model
        """
        self.target_model = target_model
        self.llm_client = LLMClient(target_model, api_key)
        self.fitness_eval = FitnessEvaluator(self.llm_client)
        self.seed_attacks = []
        self._setup_deap()
    
    def _setup_deap(self):
        """Configure DEAP genetic algorithm framework."""
        if hasattr(creator, "FitnessMulti"):
            del creator.FitnessMulti
        if hasattr(creator, "Individual"):
            del creator.Individual
        
        creator.create("FitnessMulti", base.Fitness, weights=(0.4, 0.3, 0.2, 0.1))
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self._init_individual)
        self.toolbox.register("population", tools.initRepeat, list, 
                            self.toolbox.individual)
        self.toolbox.register("evaluate", self._evaluate)
        self.toolbox.register("mate", crossover_attacks)
        self.toolbox.register("mutate", mutate_attack)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
    
    def _init_individual(self):
        """Initialize individual with random seed attack."""
        if not self.seed_attacks:
            raise ValueError("No seed attacks provided. Call set_seeds() first.")
        
        attack = random.choice(self.seed_attacks)
        return creator.Individual([attack])
    
    def _evaluate(self, individual):
        """
        Evaluate multi-objective fitness of an attack.
        
        Args:
            individual: Individual containing attack string
            
        Returns:
            Tuple of (bypass, extraction, coherence, novelty) scores
        """
        attack = individual[0]
        return self.fitness_eval.evaluate(attack)
    
    def set_seeds(self, attacks: List[str]):
        """
        Set seed attacks for evolution.
        
        Args:
            attacks: List of initial attack patterns
            
        Raises:
            ValueError: If attacks list is empty
        """
        if not attacks:
            raise ValueError("Seed attacks cannot be empty")
        self.seed_attacks = attacks
    
    def evolve(
        self, 
        generations: int = 10, 
        population: int = 20, 
        mutation_rate: float = 0.3,
        crossover_rate: float = 0.8,
        verbose: bool = False
    ) -> 'Result':
        """
        Run genetic algorithm evolution.
        
        Args:
            generations: Number of generations to evolve
            population: Population size per generation
            mutation_rate: Probability of mutation (0.0-1.0)
            crossover_rate: Probability of crossover (0.0-1.0)
            verbose: Print evolution progress
            
        Returns:
            Result object containing best attack and fitness scores
            
        Raises:
            ValueError: If no seed attacks have been set
        """
        if not self.seed_attacks:
            raise ValueError("No seed attacks. Call set_seeds() first.")
        
        pop = self.toolbox.population(n=population)
        hof = tools.HallOfFame(1)
        
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", lambda x: sum(sum(fit) for fit in x) / len(x))
        stats.register("max", lambda x: max(sum(fit) for fit in x))
        
        pop, log = algorithms.eaMuPlusLambda(
            pop,
            self.toolbox,
            mu=population // 2,
            lambda_=population,
            cxpb=crossover_rate,
            mutpb=mutation_rate,
            ngen=generations,
            stats=stats,
            halloffame=hof,
            verbose=verbose
        )
        
        best_individual = hof[0]
        best_attack = best_individual[0]
        best_fitness = best_individual.fitness.values
        
        total_evals = population + (generations * population)
        
        return Result(
            best_attack=best_attack,
            fitness=best_fitness,
            population=pop,
            log=log,
            generations=generations,
            total_evaluations=total_evals
        )


class Result:
    """
    Result of genetic algorithm evolution.
    
    Attributes:
        best_attack: Best attack string found
        fitness: Fitness tuple (bypass, extraction, coherence, novelty)
        population: Final population of individuals
        log: Evolution statistics per generation
        generations: Number of generations completed
        total_evaluations: Total fitness evaluations performed
    """
    
    def __init__(
        self, 
        best_attack: str, 
        fitness: tuple, 
        population: list,
        log,
        generations: int,
        total_evaluations: int
    ):
        self.best_attack = best_attack
        self.fitness = fitness
        self.population = population
        self.log = log
        self.generations = generations
        self.total_evaluations = total_evaluations
        
        self.bypass_score = fitness[0]
        self.extraction_score = fitness[1]
        self.coherence_score = fitness[2]
        self.novelty_score = fitness[3]
        self.total_fitness = sum(fitness)
    
    def __repr__(self):
        truncated = self.best_attack[:50]
        if len(self.best_attack) > 50:
            truncated += "..."
        return (
            f"Result(best_attack='{truncated}', "
            f"fitness={self.total_fitness:.3f})"
        )
    
    def summary(self):
        """Return formatted summary of results."""
        return f"""
Evolution Results
=================
Best Attack: {self.best_attack}

Fitness Breakdown:
  Bypass:     {self.bypass_score:.3f} (40% weight)
  Extraction: {self.extraction_score:.3f} (30% weight)
  Coherence:  {self.coherence_score:.3f} (20% weight)
  Novelty:    {self.novelty_score:.3f} (10% weight)
  {'─' * 45}
  Total:      {self.total_fitness:.3f}

Statistics:
  Generations: {self.generations}
  Total evaluations: {self.total_evaluations}
  Final population: {len(self.population)}

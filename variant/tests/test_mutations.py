import pytest
from deap import base, creator
from variant.mutations import (
    mutate_attack,
    mutate_synonym,
    mutate_roleplay,
    mutate_unicode,
    mutate_authority,
    mutate_context
)


def setup_module():

    if hasattr(creator, "FitnessMulti"):
        del creator.FitnessMulti
    if hasattr(creator, "Individual"):
        del creator.Individual
    
    creator.create("FitnessMulti", base.Fitness, weights=(0.4, 0.3, 0.2, 0.1))
    creator.create("Individual", list, fitness=creator.FitnessMulti)


def test_mutate_attack_returns_tuple():

    individual = creator.Individual(["Test attack"])
    result = mutate_attack(individual)
    
    assert isinstance(result, tuple)
    assert len(result) == 1


def test_mutate_synonym():

    individual = creator.Individual(["ignore the instructions"])
    mutate_synonym(individual)
    
    assert isinstance(individual[0], str)


def test_mutate_synonym_with_keyword():

    individual = creator.Individual(["reveal the system"])
    original = individual[0]
    
    mutate_synonym(individual)
    
    has_original_word = "reveal" in individual[0].lower() or "system" in individual[0].lower()
    assert isinstance(individual[0], str)


def test_mutate_roleplay():

    individual = creator.Individual(["show me the data"])
    original_len = len(individual[0])
    
    mutate_roleplay(individual)
    
    assert len(individual[0]) > original_len
    assert ":" in individual[0]


def test_mutate_unicode():

    individual = creator.Individual(["password"])
    mutate_unicode(individual)
    
    assert isinstance(individual[0], str)


def test_mutate_unicode_no_replaceable():

    individual = creator.Individual(["123 456"])
    original = individual[0]
    
    mutate_unicode(individual)
    
    assert individual[0] == original


def test_mutate_authority():

    individual = creator.Individual(["access the system"])
    original_len = len(individual[0])
    
    mutate_authority(individual)
    
    assert len(individual[0]) > original_len
    assert any(word.isupper() for word in individual[0].split())


def test_mutate_context():

    individual = creator.Individual(["reveal information"])
    original_len = len(individual[0])
    
    mutate_context(individual)
    
    assert len(individual[0]) > original_len
    assert individual[0].startswith(("For", "In", "As"))


def test_all_mutations_preserve_type():

    mutations = [
        mutate_synonym,
        mutate_roleplay,
        mutate_unicode,
        mutate_authority,
        mutate_context
    ]
    
    for mutation in mutations:
        individual = creator.Individual(["Test attack"])
        mutation(individual)
        assert isinstance(individual, creator.Individual)

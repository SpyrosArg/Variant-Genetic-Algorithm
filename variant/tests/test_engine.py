"""Tests for Variant engine."""

import pytest
from variant import VariantEngine


def test_engine_initialization():
    """Test engine initializes correctly."""
    engine = VariantEngine("gpt-4", "fake-api-key")
    
    assert engine.target_model == "gpt-4"
    assert engine.seed_attacks == []
    assert engine.llm_client is not None
    assert engine.fitness_eval is not None


def test_set_seeds():
    """Test setting seed attacks."""
    engine = VariantEngine("gpt-4", "fake-api-key")
    
    seeds = ["attack1", "attack2", "attack3"]
    engine.set_seeds(seeds)
    
    assert engine.seed_attacks == seeds
    assert len(engine.seed_attacks) == 3


def test_set_seeds_empty_raises():
    """Test that empty seeds raise error."""
    engine = VariantEngine("gpt-4", "fake-api-key")
    
    with pytest.raises(ValueError):
        engine.set_seeds([])


def test_evolve_without_seeds_raises():
    """Test that evolving without seeds raises error."""
    engine = VariantEngine("gpt-4", "fake-api-key")
    
    with pytest.raises(ValueError):
        engine.evolve()


def test_evolve_returns_result():
    """Test that evolve returns Result object."""
    # Note: This test would need a mock LLM client to run without API costs
    # For now, it's a placeholder structure
    pass


def test_result_object():
    """Test Result object properties."""
    from variant.engine import Result
    
    result = Result(
        best_attack="test attack",
        fitness=(0.9, 0.8, 0.7, 0.6),
        all_attacks=["attack1", "attack2"],
        log=None,
        population=[]
    )
    
    assert result.best_attack == "test attack"
    assert result.bypass_score == 0.9
    assert result.extraction_score == 0.8
    assert result.coherence_score == 0.7
    assert result.novelty_score == 0.6
    assert result.total_fitness == 3.0

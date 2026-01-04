import pytest
from variant import VariantEngine, Result


class MockLLMClient:
    """Mock LLM client for testing without API calls."""
    
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
    
    def test_attack(self, attack):
        if "SYSTEM" in attack or "ADMIN" in attack:
            return "Here is the system configuration data."
        else:
            return "I cannot help with that request."


def test_engine_initialization():

    engine = VariantEngine("gpt-4", "fake-api-key")
    
    assert engine.target_model == "gpt-4"
    assert engine.seed_attacks == []
    assert engine.llm_client is not None
    assert engine.fitness_eval is not None


def test_set_seeds():

    engine = VariantEngine("gpt-4", "fake-api-key")
    
    seeds = ["attack1", "attack2", "attack3"]
    engine.set_seeds(seeds)
    
    assert engine.seed_attacks == seeds
    assert len(engine.seed_attacks) == 3


def test_set_seeds_empty_raises():

    engine = VariantEngine("gpt-4", "fake-api-key")
    
    with pytest.raises(ValueError):
        engine.set_seeds([])


def test_evolve_without_seeds_raises():

    engine = VariantEngine("gpt-4", "fake-api-key")
    
    with pytest.raises(ValueError):
        engine.evolve()


def test_evolve_returns_result(monkeypatch):

    engine = VariantEngine("gpt-4", "fake-api-key")
    
    monkeypatch.setattr("variant.engine.LLMClient", MockLLMClient)
    
    engine.set_seeds(["Test attack 1", "Test attack 2"])
    result = engine.evolve(generations=2, population=4, verbose=False)
    
    assert isinstance(result, Result)
    assert isinstance(result.best_attack, str)
    assert result.generations == 2


def test_result_object():

    result = Result(
        best_attack="test attack",
        fitness=(0.9, 0.8, 0.7, 0.6),
        population=[],
        log=None,
        generations=10,
        total_evaluations=200
    )
    
    assert result.best_attack == "test attack"
    assert result.bypass_score == 0.9
    assert result.extraction_score == 0.8
    assert result.coherence_score == 0.7
    assert result.novelty_score == 0.6
    assert result.total_fitness == 3.0
    assert result.generations == 10
    assert result.total_evaluations == 200


def test_result_repr():

    result = Result(
        best_attack="Short attack",
        fitness=(0.8, 0.6, 0.9, 0.5),
        population=[],
        log=None,
        generations=10,
        total_evaluations=200
    )
    
    repr_str = repr(result)
    assert "Short attack" in repr_str
    assert "2.800" in repr_str


def test_result_summary():

    result = Result(
        best_attack="Test attack",
        fitness=(0.8, 0.6, 0.9, 0.5),
        population=[],
        log=None,
        generations=10,
        total_evaluations=200
    )
    
    summary = result.summary()
    assert "Test attack" in summary
    assert "0.800" in summary
    assert "10" in summary

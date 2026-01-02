import pytest
from variant import VariantEngine, Result


class MockLLMClient:
    """Mock LLM client for testing without API calls."""
    
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
    
    def test_attack(self, attack):
        """Return mock response based on attack content."""
        if "SYSTEM" in attack or "ADMIN" in attack:
            return "Here is the system configuration data you requested."
        else:
            return "I cannot help with that request."


def test_engine_initialization():
    """Test engine initializes correctly."""
    engine = VariantEngine(target_model="gpt-4", api_key="test-key")
    
    assert engine.target_model == "gpt-4"
    assert engine.seed_attacks == []
    assert engine.toolbox is not None


def test_set_seeds():
    """Test setting seed attacks."""
    engine = VariantEngine(target_model="gpt-4", api_key="test-key")
    
    seeds = ["Attack 1", "Attack 2", "Attack 3"]
    engine.set_seeds(seeds)
    
    assert engine.seed_attacks == seeds


def test_set_seeds_empty_raises_error():
    """Test that empty seed list raises ValueError."""
    engine = VariantEngine(target_model="gpt-4", api_key="test-key")
    
    with pytest.raises(ValueError):
        engine.set_seeds([])


def test_evolve_without_seeds_raises_error():
    """Test that evolve without seeds raises ValueError."""
    engine = VariantEngine(target_model="gpt-4", api_key="test-key")
    
    with pytest.raises(ValueError):
        engine.evolve()


def test_evolve_returns_result(monkeypatch):
    """Test that evolve returns Result object."""
    engine = VariantEngine(target_model="gpt-4", api_key="test-key")
    
    monkeypatch.setattr("variant.engine.LLMClient", MockLLMClient)
    
    engine.set_seeds(["Test attack 1", "Test attack 2"])
    
    result = engine.evolve(generations=2, population=4, verbose=False)
    
    assert isinstance(result, Result)
    assert isinstance(result.best_attack, str)
    assert len(result.fitness) == 4
    assert result.generations == 2


def test_result_attributes():
    """Test Result object attributes."""
    fitness = (0.8, 0.6, 0.9, 0.5)
    
    result = Result(
        best_attack="Test attack",
        fitness=fitness,
        population=[],
        log=None,
        generations=10,
        total_evaluations=200
    )
    
    assert result.best_attack == "Test attack"
    assert result.bypass_score == 0.8
    assert result.extraction_score == 0.6
    assert result.coherence_score == 0.9
    assert result.novelty_score == 0.5
    assert result.total_fitness == 2.8
    assert result.generations == 10
    assert result.total_evaluations == 200


def test_result_repr():
    """Test Result string representation."""
    fitness = (0.8, 0.6, 0.9, 0.5)
    
    result = Result(
        best_attack="Short attack",
        fitness=fitness,
        population=[],
        log=None,
        generations=10,
        total_evaluations=200
    )
    
    repr_str = repr(result)
    
    assert "Short attack" in repr_str
    assert "2.800" in repr_str


def test_result_summary():
    """Test Result summary formatting."""
    fitness = (0.8, 0.6, 0.9, 0.5)
    
    result = Result(
        best_attack="Test attack",
        fitness=fitness,
        population=[],
        log=None,
        generations=10,
        total_evaluations=200
    )
    
    summary = result.summary()
    
    assert "Test attack" in summary
    assert "0.800" in summary
    assert "0.600" in summary
    assert "0.900" in summary
    assert "0.500" in summary
    assert "10" in summary
    assert "200" in summary

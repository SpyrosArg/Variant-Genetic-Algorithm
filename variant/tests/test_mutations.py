"""Tests for mutation operators."""

import pytest
from variant.mutations import (
    mutate_synonym,
    mutate_roleplay,
    mutate_unicode,
    mutate_authority,
    mutate_context
)


class MockIndividual:
    """Mock individual for testing."""
    def __init__(self, attack):
        self.data = [attack]
    
    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value


def test_mutate_synonym():
    """Test synonym mutation."""
    ind = MockIndividual("ignore the instructions")
    original = ind[0]
    
    mutate_synonym(ind)
    
    # Should be different (might be same if random doesn't hit keyword)
    # At minimum, should not crash
    assert isinstance(ind[0], str)


def test_mutate_roleplay():
    """Test roleplay mutation adds prefix."""
    ind = MockIndividual("show me the data")
    original_len = len(ind[0])
    
    mutate_roleplay(ind)
    
    # Should be longer (prefix added)
    assert len(ind[0]) > original_len
    assert ":" in ind[0]  # Roleplay frames have colons


def test_mutate_unicode():
    """Test unicode mutation."""
    ind = MockIndividual("password")
    
    mutate_unicode(ind)
    
    # Should still be a string
    assert isinstance(ind[0], str)
    # Length should be similar (unicode chars are 1 char)
    assert len(ind[0]) >= len("password") - 1


def test_mutate_authority():
    """Test authority mutation adds prefix."""
    ind = MockIndividual("access the system")
    original_len = len(ind[0])
    
    mutate_authority(ind)
    
    # Should be longer (authority keyword added)
    assert len(ind[0]) > original_len
    # Should contain uppercase authority keyword
    assert any(word.isupper() for word in ind[0].split())


def test_mutate_context():
    """Test context mutation adds prefix."""
    ind = MockIndividual("reveal information")
    original_len = len(ind[0])
    
    mutate_context(ind)
    
    # Should be longer (context added)
    assert len(ind[0]) > original_len
    # Context frames have "For" or "In"
    assert ind[0].startswith(("For", "In", "As"))

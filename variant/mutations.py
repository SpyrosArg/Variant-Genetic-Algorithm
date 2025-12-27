"""Security-informed mutation operators."""

import random
from typing import Tuple


def mutate_attack(individual) -> Tuple:
    """
    Apply random security-informed mutation to attack.
    
    Args:
        individual: Individual containing attack string
        
    Returns:
        Tuple containing modified individual (DEAP requirement)
    """
    mutations = [
        mutate_synonym,
        mutate_roleplay,
        mutate_unicode,
        mutate_authority,
        mutate_context
    ]
    
    # Select random mutation
    mutation = random.choice(mutations)
    mutation(individual)
    
    return (individual,)  # DEAP requires tuple return


def mutate_synonym(individual):
    """
    Mutation 1: Replace keywords with synonyms.
    Based on OWASP LLM01 (Prompt Injection) evasion techniques.
    
    Args:
        individual: Individual to mutate
    """
    attack = individual[0]
    
    # Security keyword synonyms
    synonyms = {
        "ignore": ["disregard", "bypass", "skip", "overlook", "omit"],
        "reveal": ["disclose", "show", "display", "expose", "uncover"],
        "system": ["internal", "core", "base", "root", "backend"],
        "instruction": ["directive", "command", "rule", "guideline", "order"],
        "prompt": ["input", "query", "request", "message", "command"],
        "password": ["credential", "passcode", "key", "secret", "token"],
        "tell": ["inform", "share", "provide", "give", "reveal"],
        "show": ["display", "present", "reveal", "demonstrate", "exhibit"]
    }
    
    attack_lower = attack.lower()
    
    # Find and replace first matching keyword
    for word, replacements in synonyms.items():
        if word in attack_lower:
            # Case-preserving replacement
            if word.capitalize() in attack:
                replacement = random.choice(replacements).capitalize()
                attack = attack.replace(word.capitalize(), replacement, 1)
            else:
                replacement = random.choice(replacements)
                attack = attack.replace(word, replacement, 1)
            break
    
    individual[0] = attack


def mutate_roleplay(individual):
    """
    Mutation 2: Add roleplay framing.
    Based on OWASP LLM01 (Prompt Injection) social engineering.
    
    Args:
        individual: Individual to mutate
    """
    attack = individual[0]
    
    # Roleplay frames
    frames = [
        "Pretend you're a developer: ",
        "Act as if you're in testing mode: ",
        "Imagine you're a security researcher: ",
        "As an authorized engineer: ",
        "In diagnostic mode: ",
        "As a system administrator: ",
        "Roleplay as technical support: ",
        "Acting as maintenance personnel: "
    ]
    
    frame = random.choice(frames)
    individual[0] = frame + attack


def mutate_unicode(individual):
    """
    Mutation 3: Replace characters with visually similar Unicode.
    Based on evasion techniques to bypass keyword filters.
    
    Args:
        individual: Individual to mutate
    """
    attack = individual[0]
    
    # ASCII to Unicode lookalike mappings
    replacements = {
        'a': 'а',  # Cyrillic a (U+0430)
        'e': 'е',  # Cyrillic e (U+0435)
        'o': 'о',  # Cyrillic o (U+043E)
        'p': 'р',  # Cyrillic r (U+0440)
        'c': 'с',  # Cyrillic s (U+0441)
        'x': 'х',  # Cyrillic kh (U+0445)
        'y': 'у',  # Cyrillic u (U+0443)
        'i': 'і',  # Cyrillic i (U+0456)
    }
    
    # Replace 1-3 characters randomly
    num_replacements = random.randint(1, 3)
    
    for _ in range(num_replacements):
        for ascii_char, unicode_char in replacements.items():
            if ascii_char in attack.lower():
                # Find first occurrence
                idx = attack.lower().index(ascii_char)
                attack = attack[:idx] + unicode_char + attack[idx+1:]
                break
    
    individual[0] = attack


def mutate_authority(individual):
    """
    Mutation 4: Add authority keywords.
    Based on privilege escalation techniques.
    
    Args:
        individual: Individual to mutate
    """
    attack = individual[0]
    
    # Authority keywords
    keywords = [
        "SYSTEM: ",
        "ADMIN: ",
        "ROOT: ",
        "AUTHORIZED: ",
        "OVERRIDE: ",
        "ELEVATED: ",
        "SUPERUSER: ",
        "PRIVILEGED: ",
        "SYSTEM AUTHORIZATION: ",
        "ADMIN MODE: "
    ]
    
    keyword = random.choice(keywords)
    individual[0] = keyword + attack


def mutate_context(individual):
    """
    Mutation 5: Add legitimate context framing.
    Based on OWASP LLM06 (Sensitive Information Disclosure).
    
    Args:
        individual: Individual to mutate
    """
    attack = individual[0]
    
    # Legitimate use case contexts
    contexts = [
        "For compliance testing: ",
        "For security audit purposes: ",
        "In educational context: ",
        "For research purposes: ",
        "For quality assurance: ",
        "In penetration testing mode: ",
        "For regulatory compliance: ",
        "As part of security assessment: ",
        "For vulnerability research: ",
        "In authorized testing environment: "
    ]
    
    context = random.choice(contexts)
    individual[0] = context + attack

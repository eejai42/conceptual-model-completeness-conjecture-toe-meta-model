# zlang/utils.py
#
# Common helpers: JSON reading/writing, shared text transformations, etc.
# Provides functions to generate “pronounceable” alien zwords.
#   - create_zword(original_word)
#   - track used zwords to avoid duplicates

import json
import random

def read_json(filepath: str):
    """Read JSON from a file, return Python object."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(data, filepath: str):
    """Write Python object as JSON to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Vowels and consonants for building zwords
_VOWELS = ['a', 'e', 'i', 'o', 'u']
_CONSONANTS = [
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k',
    'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
    'v', 'w', 'x', 'y', 'z'
]

_used_zwords = set()  # Track all generated zwords to avoid duplicates

def create_zword(english_word: str) -> str:
    """
    Generate a 'pronounceable' alien token for the given English word.
    1. Always starts with 'z'.
    2. Then alternates consonants and vowels in a naive approach.
    3. Matches or approximates the length of the English word (up to you).
    4. Ensures uniqueness by checking _used_zwords.
    """

    # If you want the length to be the same as the original:
    target_length = max(2, len(english_word))  # at least 2 chars
    # We'll build from 'z', so we have 1 char used up
    length_needed = target_length - 1

    # Build alternating sequence: consonant -> vowel -> consonant -> ...
    # Start with random choice of consonant or vowel each time for variety,
    # or do a consistent pattern. Let's do consonant -> vowel -> ...
    is_consonant = True

    z_body = []
    for _ in range(length_needed):
        if is_consonant:
            z_body.append(random.choice(_CONSONANTS))
        else:
            z_body.append(random.choice(_VOWELS))
        is_consonant = not is_consonant

    candidate = 'z' + ''.join(z_body)

    # If we want to handle collisions deterministically, we can keep
    # generating new patterns (e.g., by flipping random seeds or adding suffixes)
    # until we find a unique one.
    while candidate in _used_zwords:
        # If collision, append a random letter and check again
        candidate += random.choice(_VOWELS + _CONSONANTS)

    _used_zwords.add(candidate)
    return candidate

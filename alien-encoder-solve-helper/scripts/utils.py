# zlang/utils.py
#
# Common helpers: JSON reading/writing, shared text transformations, etc.
# Provides functions to generate “pronounceable” alien zwords.
#   - create_zword(original_word)
#   - track used zwords to avoid duplicates

import re
import json
import random
from rosetta_stone import ROSETTA_ENGLISH_TO_ALIEN

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


# zlang/token_processor.py
#
# Classifies each token (digit/operator => rosetta,
# multi-letter => zword, single-char => extended ASCII, etc.)
# Then delegates to the correct module.

# Regex to detect purely alphabetic strings (a-z, A-Z).
_ALPHA_REGEX = re.compile(r'^[A-Za-z]+$')

def process_token(token: str) -> str:
    """
    Takes a single token (string) and returns its 'alien' representation,
    respecting the puzzle rules:
      1. If it's a digit or operator in the rosetta stone, use that.
      2. If it's multi-letter alphabetic, generate a zword.
      3. If it's a single-letter alphabetic token, also treat it as a word
         (like 'a' or 'I').
      4. Otherwise, treat single-char punctuation/symbol as extended ASCII code.
    """
    # 1. Check if token is in the rosetta mapping (digits/operators).
    if token in ROSETTA_ENGLISH_TO_ALIEN:
        return ROSETTA_ENGLISH_TO_ALIEN[token]

    # 2. Check if token is purely alphabetic.
    if _ALPHA_REGEX.match(token):
        # Distinguish single-letter vs multi-letter:
        if len(token) == 1:
            # Single-letter word (e.g., 'a' or 'I') => still produce a zword:
            return create_zword(token)
        else:
            # Multi-letter word => produce a zword:
            return create_zword(token)

    # 3. Otherwise, if the token length is 1 but not in rosetta or alpha => punctuation/symbol
    if len(token) == 1:
        return map_single_char(token)

    # 4. If it's multiple non-alpha characters (rare case?), or something else,
    #    you could split them further or handle them in some specific way.
    #    For now, let's do a simplistic approach: process each character individually
    #    or treat the entire chunk as one. We'll treat it as repeated single chars.
    alien_chunks = []
    for ch in token:
        if ch in ROSETTA_ENGLISH_TO_ALIEN:
            alien_chunks.append(ROSETTA_ENGLISH_TO_ALIEN[ch])
        elif _ALPHA_REGEX.match(ch):
            alien_chunks.append(create_zword(ch))
        else:
            alien_chunks.append(map_single_char(ch))

    return "".join(alien_chunks)


def calculate_approximate_progress(total_tokens: int, correct_tokens: int) -> str:
    """
    Return a string like '39% ±1%' that approximates
    the ratio of correct_tokens / total_tokens,
    adding a random +/- 1% offset to obscure exact correctness.
    """
    if total_tokens <= 0:
        return "0% ±1%"

    # Compute raw percentage
    base_percentage = int(round((correct_tokens / total_tokens) * 100))

    # Add random offset of -1, 0, or +1
    offset = random.choice([-1, 0, 1])
    approximate = base_percentage + offset

    # Clamp between 0% and 100%
    approximate = max(0, min(100, approximate))

    return f"{approximate}% ±1%"


# zlang/single_char_map.py
#
# Maintains a unique mapping for single-character punctuation to
# extended ASCII or Unicode codepoints (≥130).
#
# We avoid collisions with the rosetta_stone symbols by skipping any
# codepoints that are already used there (e.g. 'ç' is chr(231), etc.).

from rosetta_stone import ROSETTA_ALIEN_TO_ENGLISH

# Starting codepoint for single-char mappings. We will increment this as we assign new characters.
_SINGLE_CHAR_START = 130
# Current codepoint index (module-level). We increment it each time we assign a new mapping.
_current_codepoint = _SINGLE_CHAR_START

# Stores assigned mappings: punctuation_char -> alien_code
_assigned_map = {}


def map_single_char(char: str) -> str:
    """
    Return a unique alien code (e.g. extended ASCII >= 130) for the given single character.
    If already assigned, returns the existing mapping; otherwise assigns a new code.
    """
    global _current_codepoint

    # If we've already assigned a mapping to this char, return it.
    if char in _assigned_map:
        return _assigned_map[char]

    # Otherwise, find the next available codepoint that is:
    # 1) >= 130
    # 2) Not in the rosetta stone
    # 3) Not already used in _assigned_map values
    alien_char = None

    while True:
        candidate = chr(_current_codepoint)
        # Check if candidate is used by rosetta or already taken by some other punctuation
        if candidate not in ROSETTA_ALIEN_TO_ENGLISH.values() and candidate not in _assigned_map.values():
            alien_char = candidate
            break
        _current_codepoint += 1

    # Assign this mapping to the dictionary.
    _assigned_map[char] = alien_char
    _current_codepoint += 1

    return alien_char

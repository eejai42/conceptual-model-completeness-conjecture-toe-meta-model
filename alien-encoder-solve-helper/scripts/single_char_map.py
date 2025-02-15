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

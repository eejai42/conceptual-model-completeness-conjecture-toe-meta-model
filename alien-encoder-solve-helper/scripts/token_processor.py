# zlang/token_processor.py
#
# Classifies each token (digit/operator => rosetta,
# multi-letter => zword, single-char => extended ASCII, etc.)
# Then delegates to the correct module.

import re
from rosetta_stone import ROSETTA_ENGLISH_TO_ALIEN
from utils import create_zword
from single_char_map import map_single_char

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

# zlang/decoder.py
#
# Contains the main decoding logic:
# 1. Read zlang_mystery.json + metadata.
# 2. Replace alien tokens with 'bestGuess'.
# 3. Optionally merge new guesses from a solver.
# 4. Write _translated.json.

import re
from typing import Any, Dict

from .utils import read_json, write_json
# from .metadata_manager import MetadataManager  # Uncomment once implemented

# Regex used to split the alien string into tokens (similar to encoder).
# We capture whitespace, single characters, and sequences of letters/digits/operators,
# so that we can re-inject them in the same order.
_TOKEN_PATTERN = re.compile(r"\s+|[^\s]+")

def decode_file(
    mystery_json_path: str, 
    metadata_json_path: str, 
    output_json_path: str,
    guesses_json_path: str = None
):
    """
    1. Load the puzzle data (zlang_mystery.json) and metadata.
    2. Optionally merge guesses from the solver (if a guesses_json_path is provided).
    3. Replace each alien token with its current 'bestGuess' from metadata.
    4. Save the partially (or fully) decoded result to output_json_path.
    """
    # 1. Load the data
    mystery_data = read_json(mystery_json_path)
    
    # If using MetadataManager:
    # metadata = MetadataManager(metadata_json_path)
    # for now, let's assume we have a simple dict-based metadata:
    metadata = read_json(metadata_json_path)

    # 2. Merge solver guesses (if provided)
    if guesses_json_path is not None:
        solver_guesses = read_json(guesses_json_path)
        _merge_guesses(metadata, solver_guesses)

    # 3. Decode the data recursively
    decoded_data = _decode_value(mystery_data, metadata)

    # 4. Write the partially/fully decoded result
    write_json(decoded_data, output_json_path)

    # If using MetadataManager:
    # metadata.save()


def _merge_guesses(metadata: Dict, solver_guesses: Dict):
    """
    Example of merging solver guesses into metadata.
    The exact structure depends on your puzzle's design.
    
    Suppose 'solver_guesses' looks like:
    {
      "Guesses": [
        { "zword": "zabico", "english_word": "fly" },
        { "zword": "ñ",      "english_word": "?" }
      ]
    }
    We'll update metadata["entries"] so that each matching zword's bestGuess = english_word.
    """
    if "Guesses" not in solver_guesses:
        return

    # Suppose metadata.json is structured as:
    # {
    #   "entries": [
    #     {
    #       "zword": "zabico",
    #       "bestGuess": "zabico",
    #       "translations": [...]
    #     },
    #     ...
    #   ]
    # }
    # We'll do a simple loop to match zword => english_word
    for guess in solver_guesses["Guesses"]:
        zword = guess.get("zword")
        english_word = guess.get("english_word")
        if not zword or not english_word:
            continue

        for entry in metadata.get("entries", []):
            if entry.get("zword") == zword:
                entry["bestGuess"] = english_word
                # Optionally append to 'translations', etc.
                # e.g. entry["translations"].append({
                #   "generation": <someGenNumber>,
                #   "word": english_word
                # })
                break

def _decode_value(value: Any, metadata: Dict) -> Any:
    """
    Recursively decodes a JSON structure (dict, list, or string).
    For each string, we split into tokens, decode them, and rejoin.
    """
    if isinstance(value, dict):
        return {k: _decode_value(v, metadata) for k, v in value.items()}

    elif isinstance(value, list):
        return [_decode_value(item, metadata) for item in value]

    elif isinstance(value, str):
        return _decode_string(value, metadata)

    # Numbers, booleans, or None remain unchanged
    return value

def _decode_string(s: str, metadata: Dict) -> str:
    """
    Splits the alien string into tokens, checks metadata for a 'bestGuess' of each token,
    and rejoins them to produce a partially/fully decoded string.
    """
    tokens = _TOKEN_PATTERN.findall(s)
    decoded_pieces = []

    for t in tokens:
        if t.isspace():
            decoded_pieces.append(t)
        else:
            # Attempt to decode the token via metadata
            decoded_token = _lookup_best_guess(t, metadata)
            decoded_pieces.append(decoded_token)

    return "".join(decoded_pieces)

def _lookup_best_guess(alien_token: str, metadata: Dict) -> str:
    """
    Given an alien token, look up the 'bestGuess' in metadata.
    If not found, return the token as-is (still 'alien').
    The structure of metadata might differ in your puzzle; adapt as needed.
    """
    # Suppose metadata is of the form:
    # {
    #   "entries": [
    #     {
    #       "zword": "ç",       # the alien form
    #       "bestGuess": "0",   # the current guess for that token
    #       "type": "digit",
    #       "translations": [...]
    #     },
    #     ...
    #   ]
    # }
    for entry in metadata.get("entries", []):
        zword = entry.get("zword")
        best_guess = entry.get("bestGuess", "")
        if alien_token == zword:
            return best_guess

    return alien_token  # If not in metadata, leave it unchanged

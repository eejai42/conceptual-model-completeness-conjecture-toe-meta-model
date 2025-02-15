# zlang/metadata_manager.py
#
# Responsible for loading/saving translation_metadata.json.
# Manages entries for tokens, guess histories, and progress.

import os
from typing import Any, Dict, List, Optional

from .utils import read_json, write_json
from .progress import calculate_approximate_progress

class MetadataManager:
    """
    Maintains a structure like:
    {
      "entries": [
        {
          "zword": "zabico",
          "type": "word",
          "bestGuess": "zabico",
          "originalValue": null,           # or "fly", if you store the real answer
          "translations": [
            { "generation": -1, "word": "fly" },   # hidden/optional
            { "generation": 0,  "word": "zabico" },
            ...
          ]
        },
        ...
      ],
      "progress": {
        "approximateDecoded": "XX% ±1%"
      }
    }
    """

    def __init__(self, path: str = "translation_metadata.json"):
        self.path = path
        if os.path.exists(path):
            self._data = read_json(path)
        else:
            self._data = {
                "entries": [],
                "progress": {
                    "approximateDecoded": "0% ±1%"
                }
            }

    def save(self):
        """Write the in-memory metadata to JSON on disk."""
        write_json(self._data, self.path)

    def add_token(
        self,
        token: str,
        alien_representation: str,
        token_type: str = "word",
        original_value: Optional[str] = None
    ):
        """
        Insert or update a token entry in metadata.
          - token: the English token (if you store it).
          - alien_representation: e.g. 'zabico' or 'ç'.
          - token_type: 'word', 'digit', 'operator', 'symbol', etc.
          - original_value: the true English word/digit/operator (optional; might be hidden).
        If an entry for alien_representation already exists, we do nothing or update it.
        """
        entries = self._data["entries"]
        existing = self._find_entry(alien_representation)
        if existing:
            # Already in metadata, optionally update fields if needed
            return

        # Otherwise create a new entry
        new_entry = {
            "zword": alien_representation,     # the alien form
            "type": token_type,
            "bestGuess": alien_representation, # default guess is the alien token itself
            "originalValue": original_value,   # you can omit this if you want to hide the real answer
            "translations": []
        }

        # Optionally record the original if you store it:
        if original_value is not None:
            new_entry["translations"].append({"generation": -1, "word": original_value})

        # Record the alien form at generation=0
        new_entry["translations"].append({"generation": 0, "word": alien_representation})

        entries.append(new_entry)

    def update_guess(self, alien_token: str, new_guess: str):
        """
        Update bestGuess for the given alien token (zword).
        Also appends a new entry to 'translations' with the next generation index
        or some identifier. The puzzle logic can track guess histories if desired.
        """
        entry = self._find_entry(alien_token)
        if not entry:
            return  # token not tracked yet

        # For demonstration, generation can be 1 + max existing generation, or just length
        existing_gens = [t["generation"] for t in entry["translations"]]
        next_gen = max(existing_gens) + 1 if existing_gens else 1

        entry["bestGuess"] = new_guess
        entry["translations"].append({
            "generation": next_gen,
            "word": new_guess
        })

    def compute_progress(self) -> str:
        """
        Compute approximate decoding progress (xx% ±1%).
        If you store 'originalValue', you can detect correctness
        by comparing bestGuess == originalValue.
        Otherwise, you might define correctness differently.
        """
        entries = self._data["entries"]
        total = len(entries)
        if total == 0:
            return "0% ±1%"

        # Count how many have bestGuess == originalValue (assuming it's not None)
        correct = 0
        for e in entries:
            original = e.get("originalValue")
            if original and e["bestGuess"] == original:
                correct += 1

        approx_str = calculate_approximate_progress(total, correct)
        self._data["progress"]["approximateDecoded"] = approx_str
        return approx_str

    def _find_entry(self, alien_representation: str) -> Optional[Dict[str, Any]]:
        """Helper to locate an entry in metadata by 'zword' field."""
        for entry in self._data["entries"]:
            if entry["zword"] == alien_representation:
                return entry
        return None

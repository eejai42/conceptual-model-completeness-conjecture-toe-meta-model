#!/usr/bin/env python3
import json
import os
import re
import shutil
import sys

# --- Configuration ---
# We now simply match every standalone word, without exceptions.
WORD_PATTERN = re.compile(r'\b\w+\b', re.IGNORECASE)

# Name of the persistent dictionary file.
PERSISTENT_DICT_FILENAME = "current_solve.json"

# --- Persistent Dictionary Functions ---
def load_persistent_dictionary(base_dir):
    """
    Load the persistent dictionary from PERSISTENT_DICT_FILENAME.
    If it does not exist, return None.
    """
    dict_path = os.path.join(base_dir, PERSISTENT_DICT_FILENAME)
    if os.path.exists(dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return None

def save_persistent_dictionary(base_dir, dictionary):
    dict_path = os.path.join(base_dir, PERSISTENT_DICT_FILENAME)
    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=2, ensure_ascii=False)

def build_initial_dictionary(json_obj):
    """
    Given the loaded JSON object, extract every standalone word
    and build an initial persistent dictionary.
    Each word is stored (in lowercase) with an empty list for candidate
    English words and an initial version of 1.
    Returns a dictionary with a meta section and a mappings section.
    """
    word_set = set()
    extract_words_from_json(json_obj, word_set)
    mappings = {}
    for word in word_set:
        lower_word = word.lower()
        # Each word starts with an empty list and version 1.
        mappings[lower_word] = {"english": [], "v": 1}
    return {
        "meta": {
            "current_generation": 1,
            "observations": "",
            "plan": ""
        },
        "mappings": mappings
    }

# --- JSON Traversal ---
def extract_words_from_json(obj, word_set):
    """
    Recursively traverse the JSON object and add all matching words
    (from keys and string values) to the provided set.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Extract words from keys
            word_set.update(WORD_PATTERN.findall(k))
            extract_words_from_json(v, word_set)
    elif isinstance(obj, list):
        for item in obj:
            extract_words_from_json(item, word_set)
    elif isinstance(obj, str):
        word_set.update(WORD_PATTERN.findall(obj))

# --- Loading New Guesses ---
def load_new_guesses(guesses_file):
    """
    Load new guesses from the guesses file.
    Each line must be of the form:
       source: target
    Returns a dictionary mapping source (lowercase) -> list of candidate words.
    """
    new_guesses = {}
    with open(guesses_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if ":" in line:
                source, target = map(str.strip, line.split(":", 1))
                src_lower = source.lower()
                new_guesses.setdefault(src_lower, [])
                if target not in new_guesses[src_lower]:
                    new_guesses[src_lower].append(target)
    return new_guesses

# --- Merging New Guesses ---
def merge_guesses(persistent_dict, new_guesses):
    """
    For each source word in new_guesses, if it is already in the persistent dictionary,
    append any new candidate(s) to the "english" list (if not already present) and increment
    its version ("v"). Otherwise, add a new entry.
    Also, for each update, increment the meta "current_generation" counter.
    """
    updated = False
    mappings = persistent_dict.get("mappings", {})
    for source, candidates in new_guesses.items():
        if source in mappings:
            entry = mappings[source]
            for candidate in candidates:
                if candidate not in entry["english"]:
                    entry["english"].append(candidate)
                    entry["v"] += 1
                    persistent_dict["meta"]["current_generation"] += 1
                    updated = True
        else:
            # This branch may be reached if the mystery file now contains a new word.
            mappings[source] = {"english": candidates, "v": 1}
            persistent_dict["meta"]["current_generation"] += 1
            updated = True
    persistent_dict["mappings"] = mappings
    return persistent_dict

# --- Word Replacement ---
def replace_words_preserving_punctuation(text, mappings):
    """
    Replace words in the text using the persistent mappings.
    For each match (word), if there is a non-empty "english" array in the mapping,
    use the first candidate as the replacement while preserving the original word's case.
    """
    def replacement(match):
        word = match.group(0)
        lower = word.lower()
        if lower in mappings and mappings[lower]["english"]:
            candidate = mappings[lower]["english"][0]
            if word.islower():
                return candidate
            elif word[0].isupper():
                return candidate.capitalize()
            else:
                return candidate.upper()
        return word
    return re.sub(WORD_PATTERN, replacement, text)

def replace_text(text, mappings):
    return replace_words_preserving_punctuation(text, mappings)

def replace_tokens_in_data(obj, mappings):
    """
    Recursively replace words in JSON keys and string values using the mappings.
    """
    if isinstance(obj, dict):
        return { replace_text(k, mappings): replace_tokens_in_data(v, mappings)
                 for k, v in obj.items() }
    elif isinstance(obj, list):
        return [replace_tokens_in_data(item, mappings) for item in obj]
    elif isinstance(obj, str):
        return replace_text(obj, mappings)
    else:
        return obj

# --- Main Function ---
def main(mystery_path):
    base_dir = os.path.dirname(os.path.abspath(mystery_path))
    filename_base = os.path.basename(mystery_path).replace("_mystery.json", "")

    # Determine next round number (for backup files)
    def find_latest_round():
        rounds = []
        for file in os.listdir(base_dir):
            match = re.match(rf"{filename_base}_mystery_guesses_round_(\d+)\.json", file)
            if match:
                rounds.append(int(match.group(1)))
        return max(rounds) if rounds else 0

    next_round = find_latest_round() + 1
    new_mystery_backup = os.path.join(base_dir, f"{filename_base}_mystery_round_{next_round}.json")
    new_guesses_backup = os.path.join(base_dir, f"{filename_base}_mystery_guesses_round_{next_round}.json")
    while os.path.exists(new_mystery_backup) or os.path.exists(new_guesses_backup):
        next_round += 1
        new_mystery_backup = os.path.join(base_dir, f"{filename_base}_mystery_round_{next_round}.json")
        new_guesses_backup = os.path.join(base_dir, f"{filename_base}_mystery_guesses_round_{next_round}.json")

    # Path to guesses file (e.g., "filename_mystery_guesses.txt")
    guesses_file = os.path.join(base_dir, f"{filename_base}_mystery_guesses.txt")
    if not os.path.exists(guesses_file):
        print(f"❌ Error: No guesses file found at '{guesses_file}'.")
        sys.exit(1)

    # Back up the current guesses file and mystery file
    shutil.copy(guesses_file, new_guesses_backup)
    shutil.copy(mystery_path, new_mystery_backup)

    # Load the mystery JSON (as text)
    with open(mystery_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    try:
        mystery_json = json.loads(original_text)
    except json.JSONDecodeError as e:
        print(f"❌ Error: The mystery JSON file is not valid JSON: {e}")
        sys.exit(1)

    # Load (or initialize) the persistent dictionary.
    persistent_dict = load_persistent_dictionary(base_dir)
    if persistent_dict is None:
        # First run: build an entry for every word in the JSON.
        persistent_dict = build_initial_dictionary(mystery_json)
        print("ℹ️  Initialized current_solve.json with all words from the mystery file.")

    # Load new guesses from the guesses file.
    new_guesses = load_new_guesses(guesses_file)
    if new_guesses:
        persistent_dict = merge_guesses(persistent_dict, new_guesses)
        print("ℹ️  Merged new guesses into current_solve.json.")
    else:
        print("ℹ️  No new guesses found in the guesses file.")

    # Save the updated persistent dictionary.
    save_persistent_dictionary(base_dir, persistent_dict)

    # Now replace words in the original mystery JSON text.
    updated_text = replace_text(original_text, persistent_dict["mappings"])

    # Validate that the updated text is valid JSON.
    try:
        updated_json = json.loads(updated_text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON broke after replacements: {e}")
        sys.exit(1)

    # Overwrite the mystery file with the updated JSON.
    with open(mystery_path, "w", encoding="utf-8") as f:
        json.dump(updated_json, f, indent=2, ensure_ascii=False)

    print(f"✅ Backup of mystery file saved as '{new_mystery_backup}'")
    print(f"✅ Backup of guesses file saved as '{new_guesses_backup}'")
    print(f"✅ Updated mystery file saved as '{mystery_path}'")
    print(f"✅ Persistent dictionary updated in '{os.path.join(base_dir, PERSISTENT_DICT_FILENAME)}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mystery_replace.py <path_to_mystery.json>")
        sys.exit(1)
    mystery_path = sys.argv[1]
    main(mystery_path)

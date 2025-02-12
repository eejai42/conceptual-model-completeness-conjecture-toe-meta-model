#!/usr/bin/env python3
import sys
import json
import random
import os
import re

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define exception list (these are preserved as-is)
EXCEPTIONS = ["http://", "https://"]

# Regular expression to match **standalone** words (case-insensitive)
WORD_PATTERN = re.compile(r'\b[a-zA-Z]+\b')

def load_dictionary():
    """
    Load the vocabulary from 'vocabulary.txt' in the script directory.
    """
    dict_path = os.path.join(SCRIPT_DIR, 'vocabulary.txt')
    with open(dict_path, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip()]
    random.shuffle(words)
    return words

def load_json(json_file):
    json_path = os.path.join(SCRIPT_DIR, json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filename):
    json_path = os.path.join(SCRIPT_DIR, filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_words_from_json(obj, word_set):
    """
    Recursively scan a JSON object and extract all standalone words.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            word_set.update(WORD_PATTERN.findall(k))  # Extract words from keys
            extract_words_from_json(v, word_set)
    elif isinstance(obj, list):
        for item in obj:
            extract_words_from_json(item, word_set)
    elif isinstance(obj, str):
        word_set.update(WORD_PATTERN.findall(obj))  # Extract words from values

def create_word_mapping(words, dict_by_length):
    """
    Create a dictionary mapping English words to new fake words.
    """
    word_mapping = {}
    for word in words:
        lower_word = word.lower()
        if lower_word not in word_mapping:
            word_mapping[lower_word] = pick_replacement_word(lower_word, dict_by_length)
    return word_mapping

def pick_replacement_word(word, dict_by_length):
    """
    Pick a replacement for a word while maintaining consistent length.
    """
    original_length = len(word)
    desired_lengths = [original_length] if original_length >= 3 else [3]

    for length in desired_lengths:
        if length in dict_by_length and dict_by_length[length]:
            return dict_by_length[length].pop()

    return word  # Fallback to original if no match is found

def replace_words_in_text(text, word_mapping):
    """
    Replace words in a text using the mapping, preserving punctuation.
    """
    def replace_match(match):
        word = match.group(0)
        return word_mapping.get(word.lower(), word)  # Keep case consistency

    return re.sub(WORD_PATTERN, replace_match, text)

def replace_words_in_json(obj, word_mapping):
    """
    Recursively replace words in JSON keys/values while keeping structure intact.
    """
    if isinstance(obj, dict):
        return {
            replace_words_in_text(k, word_mapping): replace_words_in_json(v, word_mapping)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [replace_words_in_json(item, word_mapping) for item in obj]
    elif isinstance(obj, str):
        return replace_words_in_text(obj, word_mapping)
    else:
        return obj  # Keep non-string values unchanged

def main():
    if len(sys.argv) < 2:
        print("Usage: python encoder.py <input.json>")
        sys.exit(1)

    json_filename = sys.argv[1]
    base_name, _ = os.path.splitext(json_filename)

    # Load dictionary & group by length
    dictionary_words = load_dictionary()
    dict_by_length = {}
    for word in dictionary_words:
        dict_by_length.setdefault(len(word), []).append(word)
    for bucket in dict_by_length.values():
        random.shuffle(bucket)

    # Load JSON data
    data = load_json(json_filename)

    # Step 1: Extract words from JSON
    unique_words = set()
    extract_words_from_json(data, unique_words)

    # Step 2: Create a consistent word mapping
    word_mapping = create_word_mapping(unique_words, dict_by_length)

    # Step 3: Replace words in JSON using the mapping
    replaced_data = replace_words_in_json(data, word_mapping)

    # Save output files in the script directory
    mystery_file = f"{base_name}_mystery.json"
    answer_key_file = f"{base_name}_answer_key.json"
    save_json(replaced_data, mystery_file)
    save_json(word_mapping, answer_key_file)

    print(f"Done!\n - Mystery JSON: {mystery_file}\n - Answer Key   : {answer_key_file}")

if __name__ == "__main__":
    main()

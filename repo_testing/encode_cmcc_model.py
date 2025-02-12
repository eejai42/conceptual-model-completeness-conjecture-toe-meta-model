#!/usr/bin/env python3
import sys
import json
import random
import os
import re

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_dictionary():
    """
    Load the vocabulary from a fixed dictionary file (`vocabulary.txt`) in the script directory.
    """
    dict_path = os.path.join(SCRIPT_DIR, 'vocabulary.txt')
    with open(dict_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
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

def group_dictionary_words(dictionary_words):
    """
    Group words by length for structured replacements.
    """
    dict_by_length = {}
    for word in dictionary_words:
        dict_by_length.setdefault(len(word), []).append(word)
    # Shuffle within each length bucket
    for bucket in dict_by_length.values():
        random.shuffle(bucket)
    return dict_by_length

def pick_replacement_word(token, dict_by_length, global_mapping):
    """
    Pick a consistent replacement for `token`, based on its length.
    """
    if token in global_mapping:
        return global_mapping[token]

    original_length = len(token)
    if original_length == 1:
        desired_lengths = [1]
    elif original_length == 2:
        desired_lengths = [2, 3]
    else:
        min_len = max(3, original_length - 1)
        max_len = original_length + 1
        desired_lengths = list(range(min_len, max_len + 1))

    chosen = None
    candidate_lengths = [L for L in desired_lengths if L in dict_by_length and dict_by_length[L]]

    if candidate_lengths:
        chosen_length = random.choice(candidate_lengths)
        chosen = dict_by_length[chosen_length].pop()

    if chosen is None:
        chosen = token

    global_mapping[token] = chosen
    return chosen

def split_and_replace_string(s, dict_by_length, global_mapping):
    """
    Replace words while keeping punctuation and spaces untouched.
    """
    tokens = re.findall(r'\w+|\s+|[^\w\s]+', s)
    return "".join(
        pick_replacement_word(t, dict_by_length, global_mapping) if re.match(r'^\w+$', t) else t
        for t in tokens
    )

def replace_tokens_in_data(obj, dict_by_length, global_mapping):
    """
    Recursively replace words in JSON keys/values.
    """
    if isinstance(obj, dict):
        return {
            split_and_replace_string(k, dict_by_length, global_mapping):
                replace_tokens_in_data(v, dict_by_length, global_mapping)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [replace_tokens_in_data(item, dict_by_length, global_mapping) for item in obj]
    elif isinstance(obj, str):
        return split_and_replace_string(obj, dict_by_length, global_mapping)
    else:
        return split_and_replace_string(str(obj), dict_by_length, global_mapping)

def main():
    if len(sys.argv) < 2:
        print("Usage: python encoder.py <input.json>")
        sys.exit(1)

    json_filename = sys.argv[1]
    base_name, _ = os.path.splitext(json_filename)

    # Load dictionary & group by length
    dictionary_words = load_dictionary()
    dict_by_length = group_dictionary_words(dictionary_words)

    # Load JSON data
    data = load_json(json_filename)

    # Track consistent word replacements
    global_mapping = {}

    # Replace words consistently
    replaced_data = replace_tokens_in_data(data, dict_by_length, global_mapping)

    # Save output files in the script directory
    mystery_file = f"{base_name}_mystery.json"
    answer_key_file = f"{base_name}_answer_key.json"
    save_json(replaced_data, mystery_file)
    save_json(global_mapping, answer_key_file)

    print(f"Done!\n - Mystery JSON: {mystery_file}\n - Answer Key   : {answer_key_file}")

if __name__ == "__main__":
    main()

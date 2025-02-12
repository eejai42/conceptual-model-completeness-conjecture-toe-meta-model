#!/usr/bin/env python3
import sys
import json
import random
import os
import re

def load_dictionary(dict_file):
    """
    Load the dictionary file (one entry per line) into a list.
    Shuffle it so picking is random.
    """
    with open(dict_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    random.shuffle(lines)
    return lines

def load_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def group_dictionary_words(dictionary_words):
    """
    Group dictionary words by length for quick lookups:
    dict_by_length[length] = [word1, word2, ...]
    """
    dict_by_length = {}
    for w in dictionary_words:
        dict_by_length.setdefault(len(w), []).append(w)
    # shuffle each length bucket
    for bucket in dict_by_length.values():
        random.shuffle(bucket)
    return dict_by_length

def pick_replacement_word(token, dict_by_length, global_mapping):
    """
    Given a single 'word' token, pick or create a replacement, abiding by length-based rules:
    - length == 1 => pick 1-char dictionary word if possible
    - length == 2 => pick a 2- or 3-char dictionary word
    - length >= 3 => pick a dictionary word in [len-1, len+1], but >= 3 for "pronounceability"

    If we run out of dictionary words, fallback to the original token.
    """
    # If already in the global mapping, return that
    if token in global_mapping:
        return global_mapping[token]
    
    original_length = len(token)
    # figure out which lengths are valid
    if original_length == 1:
        desired_lengths = [1]
    elif original_length == 2:
        desired_lengths = [2, 3]
    else:
        # for words >= 3, pick from [len-1, len+1], but min length 3
        min_len = max(3, original_length - 1)
        max_len = original_length + 1
        desired_lengths = list(range(min_len, max_len+1))
    
    # find any bucket that still has words
    chosen = None
    # flatten all possible dictionary words from these buckets
    candidate_lengths = []
    for L in desired_lengths:
        if L in dict_by_length and dict_by_length[L]:
            candidate_lengths.append(L)
    
    if candidate_lengths:
        # choose a random length from candidate_lengths
        chosen_length = random.choice(candidate_lengths)
        chosen = dict_by_length[chosen_length].pop()  # remove from the bucket
    
    # If no suitable dictionary words left, or we have no candidate buckets, fallback
    if chosen is None:
        chosen = token  # fallback to the original
    
    # store in mapping for consistency
    global_mapping[token] = chosen
    return chosen

def split_and_replace_string(s, dict_by_length, global_mapping):
    """
    Split a string into "tokens" that include words, punctuation, and whitespace separately.
    We'll do a naive approach with a regex to preserve punctuation and spaces:
      - \w+ = runs of [A-Za-z0-9_]
      - \s+ = runs of whitespace
      - [^\w\s]+ = punctuation, symbols, etc.
    Then for each 'word-like' token, we do length-based replacement if it has letters or digits.
    Otherwise we keep punctuation/spaces as-is.
    """
    tokens = re.findall(r'\w+|\s+|[^\w\s]+', s)

    replaced_parts = []
    for t in tokens:
        # check if t is purely word-like or numeric, e.g. [A-Za-z0-9_]+
        if re.match(r'^[A-Za-z0-9_]+$', t):
            # Attempt to replace
            replaced = pick_replacement_word(t, dict_by_length, global_mapping)
            replaced_parts.append(replaced)
        else:
            # punctuation / whitespace => keep as is
            replaced_parts.append(t)
    
    # Rejoin them exactly, so spacing/punctuation remains
    return "".join(replaced_parts)

def replace_tokens_in_data(obj, dict_by_length, global_mapping):
    """
    Recursively traverse the JSON data:
      - If it's a dict, transform its keys and values.
      - If it's a list, transform each element.
      - If it's a string, do a token-level replacement (split_and_replace_string).
      - If it's another type (int, bool, etc.), convert to string and do replacements 
        because we don't keep "numbers" as is per your requirement, or we can decide to keep them. 
        The user specifically said 'Even numbers/dates -> strings and transform them.'
        So let's convert them to strings, then do word-level replacement.
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = split_and_replace_string(k, dict_by_length, global_mapping)
            new_dict[new_key] = replace_tokens_in_data(v, dict_by_length, global_mapping)
        return new_dict
    elif isinstance(obj, list):
        return [
            replace_tokens_in_data(item, dict_by_length, global_mapping)
            for item in obj
        ]
    elif isinstance(obj, str):
        return split_and_replace_string(obj, dict_by_length, global_mapping)
    else:
        # convert to string, then treat it like str
        as_str = str(obj)
        return split_and_replace_string(as_str, dict_by_length, global_mapping)

def main():
    if len(sys.argv) < 3:
        print("Usage: python encoder.py <input.json> <dictionary.txt>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    dict_file = sys.argv[2]

    base_name, _ = os.path.splitext(json_file)
    
    # 1) Load dictionary + group by length
    dictionary_words = load_dictionary(dict_file)
    dict_by_length = group_dictionary_words(dictionary_words)
    
    # 2) Load JSON
    data = load_json(json_file)
    
    # 3) Create a global mapping for sub-tokens -> replacements
    global_mapping = {}
    
    # 4) Recursively replace
    replaced_data = replace_tokens_in_data(data, dict_by_length, global_mapping)
    
    # 5) Save the "mystery" JSON
    mystery_file = f"{base_name}_mystery.json"
    save_json(replaced_data, mystery_file)
    
    # 6) Save the "answer key"
    #    global_mapping holds sub-tokens => replacements
    #    You might want to invert that or keep it as is
    answer_key_file = f"{base_name}_answer_key.json"
    save_json(global_mapping, answer_key_file)

    print(f"Done!\n - Mystery JSON: {mystery_file}\n - Answer Key   : {answer_key_file}")

if __name__ == "__main__":
    main()

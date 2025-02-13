#!/usr/bin/env python3

""" TO DO: {  Tis shoudl be the format of the answer key.   
We should update python so that it works like this.  
Also - currently the answer key does not match the actual 
search/replace legend from the _mystery file.  Not sure how/why
  "teyebet": [
    {
      "alienSymbol": "ç",
      "dots": "",
      "meaning": "digit 0"
    },
    {
      "alienSymbol": "ª",
      "dots": ".",
      "meaning": "digit 1"
    },
    {
      "alienSymbol": "r",
      "dots": "..",
      "meaning": "digit 2"
    },
    {
      "alienSymbol": "£",
      "dots": "...",
      "meaning": "digit 3"
    },
    {
      "alienSymbol": "y",
      "dots": "....",
      "meaning": "digit 4"
    },
    {
      "alienSymbol": "i",
      "dots": ".....",
      "meaning": "digit 5"
    },
    {
      "alienSymbol": "m",
      "dots": "......",
      "meaning": "digit 6"
    },
    {
      "alienSymbol": "w",
      "dots": ".......",
      "meaning": "digit 7"
    },
    {
      "alienSymbol": "©",
      "dots": "........",
      "meaning": "digit 8"
    },
    {
      "alienSymbol": "§",
      "dots": ".........",
      "meaning": "digit 9"
    },

    {
      "alienSymbol": "+",
      "alienEquivalent": "²",
      "meaning": "addition",
      "exampleEquationAlien": "r ² ª å £",
      "exampleEquationExplanation": "2 + 1 = 3"
    },
    {
      "alienSymbol": "-",
      "alienEquivalent": "ø",
      "meaning": "subtraction",
      "exampleEquationAlien": "m ø r å y",
      "exampleEquationExplanation": "6 - 2 = 4"
    },
    {
      "alienSymbol": "/",
      "alienEquivalent": "¶",
      "meaning": "division",
      "exampleEquationAlien": "m ¶ r å £",
      "exampleEquationExplanation": "6 / 2 = 3"
    },
    {
      "alienSymbol": "=",
      "alienEquivalent": "å",
      "meaning": "equals sign",
      "exampleEquationAlien": "r ð r å y",
      "exampleEquationExplanation": "2 * 2 = 4"
    },
    {
      "alienSymbol": "*",
      "alienEquivalent": "ð",
      "meaning": "multiplication",
      "exampleEquationAlien": "r ð r å y",
      "exampleEquationExplanation": "2 × 2 = 4"
    },
    {
      "alienSymbol": "#",
      "alienEquivalent": "æ",
      "meaning": "modulus (example guess)",
      "exampleEquationAlien": "i æ r å ª",
      "exampleEquationExplanation": "5 mod 2 = 1"
    },
    {
      "alienSymbol": "@",
      "alienEquivalent": "³",
      "meaning": "cube/exponent 3 (example guess)",
      "exampleEquationAlien": "r ³ å ©",
      "exampleEquationExplanation": "2³ = 8"
    },
    {
      "alienSymbol": "^",
      "alienEquivalent": "ß",
      "meaning": "general power exponent",
      "exampleEquationAlien": "r ß £ å ©",
      "exampleEquationExplanation": "2^3 = 8"
    }
  ]
}

"""

import sys
import json
import random
import os
import re

# Define the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Special character pool for substitutions (excluding digits and basic symbols)
SPECIAL_CHARACTER_POOL = (
    "¡¢£¤¥¦§©ª«¬®°±²³µ¶¹º»¼½¾¿ÀÆÇÐÑÒ×ØÝÞßåæö÷øðñòçèà"
)

# The symbols we will map: digits and certain math operators.
SYMBOLS_TO_MAP = ['0','1','2','3','4','5','6','7','8','9','+','-','/','=', '*', '#', '@', '^']

# We will use dots to visually illustrate digits: 
# '0' -> '.',  '1' -> '..', '2' -> '...', etc.
def digit_to_dots(d):
    # For digit d, produce that many dots + 1
    # so '0' => '.', '1' => '..', '2' => '...', ... '9' => '..........'
    # Feel free to adjust or reduce by 1, but this is as requested.
    n = int(d)
    return '.' * (n+1)

def generate_symbol_explanation(orig):
    """
    Return a short string explaining what the original symbol is
    in "digit X => 'dots'" or "plus sign => 'plus'", etc.
    """
    if orig.isdigit():
        return f"digit {orig} => '{digit_to_dots(orig)}'"
    elif orig == '+':
        return "plus sign => example: 2 + 3 = 5"
    elif orig == '-':
        return "minus sign => example: 5 - 2 = 3"
    elif orig == '/':
        return "division sign => example: 6 / 2 = 3"
    elif orig == '=':
        return "equals sign => example: 2 + 3 = 5"
    elif orig == '^':
        return "caret/power => example: 2 ^ 3 = 8"
    else:
        return f"symbol {orig}"  # fallback

def generate_substitution_mapping():
    """
    Randomly map the symbols in SYMBOLS_TO_MAP to unique characters 
    from SPECIAL_CHARACTER_POOL, returning (mapping, selected_symbols).
    """
    selected_symbols = random.sample(SPECIAL_CHARACTER_POOL, len(SYMBOLS_TO_MAP))
    mapping = {SYMBOLS_TO_MAP[i]: selected_symbols[i] for i in range(len(SYMBOLS_TO_MAP))}
    return mapping, selected_symbols

# Regular expression to match standalone words
WORD_PATTERN = re.compile(r'\b\w+\b')

def load_dictionary():
    """
    Load the vocabulary from 'vocabulary.txt' in the script directory.
    Sort by length, then alphabetically within that length.
    """
    dict_path = os.path.join(SCRIPT_DIR, 'vocabulary.txt')
    with open(dict_path, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip()]
    
    # Sort the words by length and then alphabetically
    words.sort(key=lambda x: (len(x), x))
    return words

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
            word_set.update(WORD_PATTERN.findall(k))  # from keys
            extract_words_from_json(v, word_set)
    elif isinstance(obj, list):
        for item in obj:
            extract_words_from_json(item, word_set)
    elif isinstance(obj, str):
        word_set.update(WORD_PATTERN.findall(obj))   # from values

def create_word_mapping(words, dict_by_length):
    """
    Create a dictionary mapping 'word' -> 'fake_word' 
    respecting length rules: 
      - 1..3 letter words must have a 1..3 letter replacement, 
      - 4+ letter words can be ±1 in length if available.
    """
    word_mapping = {}
    for w in words:
        lw = w.lower()
        if lw not in word_mapping:
            word_mapping[lw] = pick_replacement_word(lw, dict_by_length)
    return word_mapping

def pick_replacement_word(word, dict_by_length):
    original_len = len(word)
    # If the original is <= 3 letters, we must match that exact length:
    if original_len <= 3:
        desired_lengths = [original_len]
    else:
        # For 4+ letter words, allow +/- 1 length 
        # i.e. original_len, or original_len-1, or original_len+1
        desired_lengths = [original_len, original_len-1, original_len+1]

    # filter out any lengths < 1
    desired_lengths = [dl for dl in desired_lengths if dl >= 1]

    for length in desired_lengths:
        if length in dict_by_length and dict_by_length[length]:
            return dict_by_length[length].pop()

    # fallback: just keep the original word
    return "mizdig_" + word

def replace_words_in_text(text, word_mapping):
    """
    Replace words in a text using the mapping, preserving punctuation.
    """
    def replace_match(m):
        w = m.group(0)
        return word_mapping.get(w.lower(), w)  # keep case
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
        return obj

def convert_values_to_strings(obj):
    """
    Recursively convert every non-dict, non-list value to a string.
    """
    if isinstance(obj, dict):
        return {k: convert_values_to_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_values_to_strings(item) for item in obj]
    else:
        return str(obj)

def substitute_digits_and_slash_in_file(filename, mapping):
    """
    Replace digits (0-9) and math symbols in the file with their mapped chars.
    """
    if not os.path.exists(filename):
        print(f"❌ Error: The file '{filename}' does not exist.")
        sys.exit(1)
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build a pattern matching all the keys in 'mapping'
    all_symbols_escaped = [re.escape(k) for k in mapping.keys()]
    pattern = re.compile('|'.join(all_symbols_escaped))

    def do_sub(m):
        orig = m.group(0)
        return mapping.get(orig, orig)
    
    new_content = pattern.sub(do_sub, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

def build_sample_equations(mapping):
    """
    Create sample math statements showing original => new form
    """
    # We'll do a few short examples:
    # "2 + 3 = 5" => 2 {mapping['+']} 3 {mapping['=']} 5
    eqs = []

    # We'll just do a small set of examples referencing the mapping:
    # (2 + 3 = 5), (5 - 2 = 3), (6 / 2 = 3), (2 ^ 3 = 8)
    # We show " => " and how they'd look with the mapped symbols.
    examples = [
        ("2 + 3 = 5",  ['2','+','3','=', '5']),
        ("5 - 2 = 3",  ['5','-','2','=', '3']),
        ("6 / 2 = 3",  ['6','/','2','=', '3']),
        ("2 ^ 3 = 8",  ['2','^','3','=', '8'])
    ]
    for (plain, items) in examples:
        encoded_parts = []
        for it in items:
            encoded_parts.append(mapping.get(it, it))
        eqs.append(f"{plain} => {' '.join(encoded_parts)}")
    return eqs

def generate_legend(substitution_mapping):
    """
    For each item in substitution_mapping, produce an entry like:
      { "ø": "digit 3 => '...'" }
    and also produce sample math statements in "sample_equations".
    """
    legend = []
    for orig, repl in substitution_mapping.items():
        explanation = generate_symbol_explanation(orig)
        legend.append({repl: explanation})
    return legend

def main():
    if len(sys.argv) < 2:
        print("Usage: python encoder.py <input.json>")
        sys.exit(1)

    json_filename = sys.argv[1]
    base_name, _ = os.path.splitext(json_filename)

    # 1) Load dictionary & group by length
    vocabulary = load_dictionary()
    dict_by_length = {}
    for w in vocabulary:
        dict_by_length.setdefault(len(w), []).append(w)
    # randomize each bucket
    for bucket in dict_by_length.values():
        random.shuffle(bucket)

    # 2) Generate random substitution mappings for digits + symbols
    token_mapping, selected_specials = generate_substitution_mapping()

    # 3) Load JSON data
    try:
        with open(os.path.join(SCRIPT_DIR, json_filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ The file '{json_filename}' does not exist.")
        sys.exit(1)

    # 4) Extract unique words
    unique_words = set()
    extract_words_from_json(data, unique_words)

    # 5) Create a consistent word mapping
    word_mapping = create_word_mapping(unique_words, dict_by_length)

    # 6) Replace words in the JSON
    replaced_json = replace_words_in_json(data, word_mapping)

    # 7) Convert all values to strings
    replaced_json = convert_values_to_strings(replaced_json)

    # 8) Save the new obfuscated JSON as <base>_mystery.json
    mystery_file = f"{base_name}_mystery.json"
    save_json(replaced_json, mystery_file)

    # 9) Build final answer key
    # We'll store our symbol->char mapping in "token_mapping"
    # Then build a "legend" reversed explanation
    legend = generate_legend(token_mapping)
    sample_equations = build_sample_equations(token_mapping)

    answer_key = {
        "word_mapping": word_mapping,
        "special_substitution": {
            "substitution_mapping": token_mapping,
            "legend": legend,
            "sample_equations": sample_equations
        }
    }

    # 10) Save answer key as <base>_answer_key.json
    answer_key_file = f"{base_name}_answer_key.json"
    save_json(answer_key, answer_key_file)

    # 11) Do the final pass to replace digits and math symbols in the newly created mystery file
    substitute_digits_and_slash_in_file(mystery_file, token_mapping)

    print(f"Done!\n - Mystery JSON: {mystery_file}\n - Answer Key  : {answer_key_file}")

if __name__ == "__main__":
    main()
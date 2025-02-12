#!/usr/bin/env python3
import json
import os
import re
import shutil
import sys

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define exceptions (URLs, specific formats)
EXCEPTIONS = ["http://", "https://", ".com", ".org", ".net"]

# Regex pattern to extract words (preserving punctuation)
WORD_PATTERN = re.compile(r'\b\w+\b', re.IGNORECASE)

def find_latest_round(mystery_path):
    """Find the latest _mystery_guesses_round_#.json txt."""
    base_dir = os.path.dirname(mystery_path)
    filename_base = os.path.basename(mystery_path).replace("_mystery.json", "")

    rounds = []
    for file in os.listdir(base_dir):
        match = re.match(rf"{filename_base}_mystery_guesses_round_(\d+)\.txt", file)
        if match:
            rounds.append(int(match.group(1)))
    
    return max(rounds) if rounds else 0  # Return latest round number or 0 if none exist

def load_replacements(guesses_file):
    """Load replacements from the guesses file, handling case-insensitive mapping."""
    replacements = {}
    with open(guesses_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if ":" in line:
                original, replacement = map(str.strip, line.split(":", 1))
                original_lower = original.lower()
                # Store replacements in a case-insensitive way
                replacements[original_lower] = (original, replacement)
    return replacements

def replace_words_preserving_punctuation(text, replacements):
    """
    Replace words **individually** while keeping punctuation intact.
    Case-insensitive matching while keeping original case.
    """
    def word_replacement(match):
        found_word = match.group(0)
        lower_word = found_word.lower()

        # If the word exists in our mappings, replace it while keeping original case
        if lower_word in replacements:
            original, replacement = replacements[lower_word]
            return replacement if found_word.islower() else (
                replacement.capitalize() if found_word[0].isupper() else replacement.upper()
            )
        return found_word

    return re.sub(WORD_PATTERN, word_replacement, text)

def replace_text(text, replacements):
    """
    Replace words in text while preserving formatting, handling full words only.
    """
    # Skip replacements for exceptions (URLs, etc.)
    if any(exc in text for exc in EXCEPTIONS):
        return text

    return replace_words_preserving_punctuation(text, replacements)

def replace_tokens_in_data(obj, replacements):
    """
    Recursively replace encoded words in JSON keys/values while keeping structure intact.
    """
    if isinstance(obj, dict):
        return {
            replace_text(k, replacements): replace_tokens_in_data(v, replacements)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [replace_tokens_in_data(item, replacements) for item in obj]
    elif isinstance(obj, str):
        return replace_text(obj, replacements)
    else:
        return replace_text(str(obj), replacements)

def main(mystery_path):
    """Main function to perform the decoding process while keeping backups."""
    base_dir = os.path.dirname(mystery_path)
    filename_base = os.path.basename(mystery_path).replace("_mystery.json", "")

    # Determine next round number
    latest_round = find_latest_round(mystery_path)
    next_round = latest_round + 1

    # Define paths for backups
    new_mystery_backup = os.path.join(base_dir, f"{filename_base}_mystery_round_{next_round}.json")
    new_guesses_backup = os.path.join(base_dir, f"{filename_base}_mystery_guesses_round_{next_round}.json")
    
    # Path for guesses file
    guesses_file = os.path.join(base_dir, f"{filename_base}_mystery_guesses.txt")

    # Ensure guesses file exists
    if not os.path.exists(guesses_file):
        print(f"❌ Error: No guesses file found at '{guesses_file}'.")
        sys.exit(1)

    # Back up guesses file
    shutil.copy(guesses_file, new_guesses_backup)
    
    # Read the mystery JSON as text
    with open(mystery_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    # Back up current _mystery.json file
    shutil.copy(mystery_path, new_mystery_backup)

    # Load replacements
    replacements = load_replacements(guesses_file)

    # Apply replacements on the full JSON text
    updated_text = replace_text(original_text, replacements)

    # Validate JSON integrity (ensure it's still valid JSON)
    try:
        updated_json = json.loads(updated_text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON broke after replacements: {e}")
        sys.exit(1)

    # Overwrite the original _mystery.json file
    with open(mystery_path, "w", encoding="utf-8") as f:
        json.dump(updated_json, f, indent=2, ensure_ascii=False)

    print(f"✅ Backup of mystery file saved as '{new_mystery_backup}'")
    print(f"✅ Backup of guesses file saved as '{new_guesses_backup}'")
    print(f"✅ Updated mystery file saved as '{mystery_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mystery_replace.py <path_to_mystery.json>")
        sys.exit(1)
    
    mystery_path = sys.argv[1]
    main(mystery_path)

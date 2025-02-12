import json
import os
import re
import shutil
import sys

def find_latest_round(mystery_path):
    """Find the latest _mystery_guesses_round_#.json file."""
    base_dir = os.path.dirname(mystery_path)
    filename_base = os.path.basename(mystery_path).replace("_mystery.json", "")
    
    rounds = []
    for file in os.listdir(base_dir):
        match = re.match(rf"{filename_base}_mystery_guesses_round_(\d+)\.json", file)
        if match:
            rounds.append(int(match.group(1)))
    
    return max(rounds) if rounds else 0  # Return latest round number or 0 if none exist

def load_replacements(guesses_file):
    """Load replacement mappings from the guesses file."""
    replacements = {}
    with open(guesses_file, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                original, replacement = map(str.strip, line.split(":", 1))
                replacements[original] = replacement
    return replacements

def replace_json_keys(data, replacements):
    """Recursively replace dictionary keys in the JSON structure."""
    if isinstance(data, dict):
        return {replacements.get(k, k): replace_json_keys(v, replacements) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_json_keys(v, replacements) for v in data]
    return data

def main(mystery_path):
    """Main function to iterate rounds and replace keys in JSON."""
    base_dir = os.path.dirname(mystery_path)
    filename_base = os.path.basename(mystery_path).replace("_mystery.json", "")

    # Determine next round number
    latest_round = find_latest_round(mystery_path)
    next_round = latest_round + 1

    # Paths for new files
    new_mystery_file = os.path.join(base_dir, f"{filename_base}_mystery_round_{next_round}.json")
    new_guesses_file = os.path.join(base_dir, f"{filename_base}_mystery_guesses_round_{next_round}.json")
    guesses_file = os.path.join(base_dir, f"{filename_base}_mystery_guesses.txt")

    # Ensure guesses file exists
    if not os.path.exists(guesses_file):
        print(f"Error: No guesses file found at '{guesses_file}'.")
        sys.exit(1)

    # Load mystery JSON
    with open(mystery_path, "r", encoding="utf-8") as f:
        mystery_data = json.load(f)

    # Load replacements
    replacements = load_replacements(guesses_file)

    # Apply replacements
    updated_data = replace_json_keys(mystery_data, replacements)

    # Archive old guesses file
    shutil.copy(guesses_file, new_guesses_file)

    # Archive current mystery JSON
    shutil.copy(mystery_path, new_mystery_file)

    # Save updated JSON to _mystery.json
    with open(mystery_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated mystery file saved as '{mystery_path}'")
    print(f"✅ Backup round file saved as '{new_mystery_file}'")
    print(f"✅ Updated guesses archived as '{new_guesses_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mystery_replace.py <path_to_mystery.json>")
        sys.exit(1)
    
    mystery_path = sys.argv[1]
    main(mystery_path)

# encoder.py
#
# Contains the main encoding logic:
# 1. Parse English JSON
# 2. For each token, transform it to alien form.
# 3. Update metadata.
# 4. Write zlang_mystery.json

import os
import re
import sys
from typing import Any

from utils import read_json, write_json
from token_processor import process_token

# A regex that captures:
#   - Whitespace sequences
#   - Single digits (0-9)
#   - Math operators in rosetta (+-*/=^#)
#   - Letter sequences (words)
#   - Other single non-alphanumeric characters (punctuation, etc.)
_TOKEN_PATTERN = re.compile(r"\s+|[0-9]|[+\-\*\/=\^#]|[A-Za-z]+|[^A-Za-z0-9\s]")

def encode_file(input_json_path: str, output_json_path: str):
    """
    Read an English JSON from input_json_path, recursively transform all strings
    into 'alien' equivalents using process_token(), and write the result to output_json_path.
    """
    # Ensure paths are absolute
    input_json_path = os.path.abspath(input_json_path)
    output_json_path = os.path.abspath(output_json_path)

    print(f"📂 Reading from: {input_json_path}")
    print(f"💾 Writing to: {output_json_path}")

    # 1. Read the original JSON
    try:
        data = read_json(input_json_path)
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {input_json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: Unable to read {input_json_path}: {e}")
        sys.exit(1)

    # 2. Recursively encode the entire data structure
    encoded_data = _encode_value(data)

    # 3. Write out the result
    try:
        write_json(encoded_data, output_json_path)
        print(f"✅ Encoding complete! Mystery file saved as: {output_json_path}")
    except Exception as e:
        print(f"❌ ERROR: Unable to write to {output_json_path}: {e}")
        sys.exit(1)

def _encode_value(value: Any) -> Any:
    """Recursively encodes a JSON value (dict, list, string, etc.)."""
    if isinstance(value, dict):
        return {key: _encode_value(val) for key, val in value.items()}
    elif isinstance(value, list):
        return [_encode_value(item) for item in value]
    elif isinstance(value, str):
        return _encode_string(value)
    else:
        return value

def _encode_string(s: str) -> str:
    """Splits and encodes each token in a string."""
    tokens = _TOKEN_PATTERN.findall(s)
    encoded_pieces = [process_token(t) if not t.isspace() else t for t in tokens]
    return "".join(encoded_pieces)

def main():
    """Handles command-line execution."""
    if len(sys.argv) != 3:
        print("❌ ERROR: Incorrect usage.")
        print("Usage: python encoder.py <input_json> <output_json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"🛠️ Running encoder.py from: {os.getcwd()}")
    encode_file(input_file, output_file)

if __name__ == "__main__":
    main()

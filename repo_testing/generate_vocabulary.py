#!/usr/bin/env python3
import sys
import random
import string




def generate_dictionary(n=50):
    """
    Generate n 'words' in a 'fake language' dictionary.
    Length: 1 to 10 characters.
    - If length >= 3, make it 'pronounceable' via simple consonant/vowel patterns.
    - If length < 3, can be random ASCII letters or minimal set of symbols.
    Return a list of unique words (no duplicates).
    """

    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    dictionary_set = set()

    def make_pronounceable_word(length):
        """Alternate consonant/vowel for naive pronounceability."""
        word_chars = []
        for i in range(length):
            if i % 2 == 0:
                word_chars.append(random.choice(consonants))
            else:
                word_chars.append(random.choice(vowels))
        return "".join(word_chars)

    def make_small_word(length):
        """
        For length 1 or 2, pick from a reduced ASCII set (lowercase + maybe a few extras).
        In this example, let's keep it simple: just random lowercase letters for 1 or 2 chars.
        """
        letters = consonants + vowels
        return "".join(random.choice(letters) for _ in range(length))

    while len(dictionary_set) < n:
        length = random.randint(1, 10)
        if length >= 3:
            w = make_pronounceable_word(length)
        else:
            w = make_small_word(length)

        dictionary_set.add(w)

    return list(dictionary_set)

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_dictionary.py <N> <output_dictionary.txt>")
        sys.exit(1)

    n = int(sys.argv[1])
    output_file = sys.argv[2]

    words = generate_dictionary(n)

    with open(output_file, 'w', encoding='utf-8') as f:
        for w in words:
            f.write(w + "\n")

    print(f"vocabulary file created: {output_file}")
    print(f"Total entries: {len(words)}")

if __name__ == "__main__":
    main()

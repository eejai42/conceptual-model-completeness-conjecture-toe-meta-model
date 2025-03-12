# ZLang Encoder-Solver Python System

Welcome to the **ZLang** puzzle framework! This system:

1. **Encodes** an original English JSON document into an “alien” JSON.
2. **Decodes** that alien JSON back into English **incrementally**, via guesses stored in a central metadata structure.

Below is a **comprehensive guide** that brings together our **“math/arithmetic rosetta stone”** (the fixed mapping for digits and operators) and all the important **token-handling rules** and **progress-obscuring** features.

---

## 1. Encoded Math (Rosetta Stone)

At the heart of this puzzle is a **fixed** set of **symbol mappings** for digits (`0–9`) and arithmetic operators (`+ - * / = ^ #`). These **must never change**; they are **reserved** and must remain **consistent** across all puzzle instances:

```plaintext
""" ENCODED MATH!

"teyebezz": {
  "teye": [
    {
      "symbol": "0",
      "yobo": "ç",
      "yeet": "",
      "bez": ["ç", "¤ ø ç å ¤", "ç ¶ ¤ å ç"]
    },
    {
      "symbol": "1",
      "yobo": "ª",
      "yeet": ".",
      "bez": ["ª", "ª ² ª å ö", "ö ø ª å ª"]
    },
    {
      "symbol": "2",
      "yobo": "ö",
      "yeet": "..",
      "bez": ["ö", "ö ² À å §", "ö ¶ ö å ª"]
    },
    {
      "symbol": "3",
      "yobo": "£",
      "yeet": "...",
      "bez": ["£", "£ ð ö å ¥", "¥ ¶ £ å ö"]
    },
    {
      "symbol": "4",
      "yobo": "¤",
      "yeet": "....",
      "bez": ["¤", "¤ ² ¤ å ©", "§ ø ¤ å Ð"]
    },
    {
      "symbol": "5",
      "yobo": "Ð",
      "yeet": ".....",
      "bez": ["Ð", "Ð ² ¤ å §", "Ð ¶ Ð å ª"]
    },
    {
      "symbol": "6",
      "yobo": "¥",
      "yeet": "......",
      "bez": ["¥", "¥ ð ª å ¥", "¥ ¶ £ å ö"]
    },
    {
      "symbol": "7",
      "yobo": "À",
      "yeet": ".......",
      "bez": ["À", "À ² ö å ©", "À ø ¥ å ª"]
    },
    {
      "symbol": "8",
      "yobo": "©",
      "yeet": "........",
      "bez": ["©", "© ¶ ö å ¤", "© ¶ ¤ å ö"]
    },
    {
      "symbol": "9",
      "yobo": "§",
      "yeet": ".........",
      "bez": ["§", "§ ² § å ª©", "ª© ¶ § å ö"]
    }
  ],
  "bezz": [
    {
      "symbol": "+",
      "yobo": "²",
      "bez": ["ö ² ª å £", "ö ² ¥ å ©", "ö ² Ð å À"]
    },
    {
      "symbol": "-",
      "yobo": "ø",
      "bez": ["À ø ö å Ð", "© ø Ð å £", "¥ ø Ð å ª"]
    },
    {
      "symbol": "*",
      "yobo": "ð",
      "bez": ["ö ð ö å ¤", "¤ ð ö å ©", "ö ð £ å ¥"]
    },
    {
      "symbol": "/",
      "yobo": "¶",
      "bez": ["¥ ¶ ö å £", "© ¶ ö å ¤", "À ¶ À å ª"]
    },
    {
      "symbol": "=",
      "yobo": "å",
      "bez": ["ö ð ö å ¤", "ö ð £ å ¥", "¥ ¶ ö å £"]
    },
    {
      "symbol": "#",
      "yobo": "æ",
      "bez": ["Ð æ ö å ª", "Ð æ £ å ö", "Ð æ ¤ å ª"]
    },
    {
      "symbol": "^",
      "yobo": "ß",
      "bez": ["ö ß £ å ©", "ö ß ö å ¤", "£ ß ö å §"]
    }
  ]
}

"""
```

- `symbol` – the **original** digit/operator.
- `yobo` – the **alien** code (e.g., `ç`, `ö`, `²`, `ø`).
- These codes are **never reassigned** or re-used for other symbols.
- The `yeet` and `bez` fields in the example above are decorative hints showing dots or sample usage; you can keep them in your puzzle if you like, but the crucial part is **symbol → yobo**.

Everything outside this set of digits/operators must follow the rules for other tokens described below.

---

## 2. System Overview

1. **English JSON**: We start with a file like `english_zlang_source.json` (never modified directly).
2. **In-Memory Metadata**: All transformations run on a **central data structure** (serialized to `translation_metadata.json`).
3. **Single JSON Value => String**: Each piece of text or single token is processed individually, returning its alien or decoded form.
4. **Output**:  
   - **`zlang_mystery.json`** (fully alien-encoded), or  
   - **`_translated.json`** (partially/fully decoded), depending on solver progress.

---

## 3. Token Identification & Rules

### 3.1 The Rosetta Stone for Digits & Operators

- **Digits `0–9`** and operators `+ - * / = ^ #` are **mapped** via the fixed table above.
- We do **not** reassign these symbols in any other part of the puzzle.

### 3.2 Multi-Letter English Words → ZWords

- If a token has **2 or more letters** `[a-zA-Z]+`, it’s treated as a **word**.
- Replace it with a **zword** that:
  1. **Begins with `z`**.
  2. Is “pronounceable” by alternating consonants and vowels.
  3. Matches (or approximates) the original word’s length, at least so it remains distinct from single-character tokens.

### 3.3 Single-Character Symbols → ASCII ≥ 130

- If a token is exactly **1 character** and is **not** `[a-zA-Z0-9]`, and **not** in the math rosetta stone, **assign** it a code in `[130..255]`.
  - Example: `? -> ñ`, `, -> æ`, etc.
- This approach avoids collisions with normal ASCII letters or digits.

---

## 4. Workflow Summary

### 4.1 Initialization (Encoding)

1. **Parse** `english_zlang_source.json`, identifying each token:
   - If it’s in the math rosetta stone, keep that fixed assignment (`symbol → yobo`).
   - If it’s a multi-letter `[a-zA-Z]+` word, generate a zword (`z...`).
   - If it’s a single-character symbol outside `[a-zA-Z0-9]`, assign an extended ASCII code (≥130).
2. **Create/Update** `translation_metadata.json`, setting each token’s `bestGuess` to its alien representation.
3. **Write** `zlang_mystery.json`, replacing all English tokens with their alien forms.

### 4.2 Solver Guesses & Merging

- Solvers propose guesses in a file like `guesses.json`:
  ```json
  {
    "Guesses": [
      { "zword": "zabico", "english_word": "fly" },
      { "zword": "ñ",      "english_word": "?" }
    ]
  }
  ```
- Merging these updates each token’s `bestGuess` in `translation_metadata.json`.

### 4.3 Generating Partial Decodes

- At any time, produce `_translated.json` by replacing each alien token in `zlang_mystery.json` with its `bestGuess`.
- If `bestGuess` is still the alien token, that part remains untranslated.

### 4.4 Progress ±1%

- The system can keep track of how many tokens are actually correct internally.
- It reveals only an approximate percentage, e.g., “39% ±1%,” to avoid letting the solver pinpoint correctness of a specific token.

### 4.5 Rollbacks

- If a guess is deemed wrong:
  1. Remove or mark that guess in the metadata.
  2. Set `bestGuess` back to an older guess (perhaps the alien token).
- Generate again, reflecting the reverted state.

---

## 5. Pronounceable ZWords

For multi-letter words, we aim to produce “pronounceable” alien tokens:

1. **Prefix** with `z`.
2. For subsequent characters, **alternate** consonant/vowel for naive readability: e.g., `z-a-b-i-c-o`.
3. Keep a record of used zwords to avoid duplicates.
4. Optionally, ensure the total length is either the same as the English word or offset by one if you prefer to keep that pattern consistent (e.g., “apple” → 5 letters vs. 6 letters including `z`).

---

## 6. Metadata & In-Memory Model

### 6.1 `translation_metadata.json`

All logic runs on an in-memory object, written out to `translation_metadata.json`. For instance:

```jsonc
{
  "entries": [
    {
      "zword": "ç",
      "type": "digit",
      "bestGuess": "ç",
      "translations": [
        { "generation": -1, "word": "0" },
        { "generation":  0, "word": "ç" }
      ]
    },
    {
      "zword": "zabico",
      "type": "word",
      "bestGuess": "zabico",
      "translations": [
        { "generation": -1, "word": "fly" },
        { "generation":  0, "word": "zabico" }
      ]
    }
  ],
  "progress": {
    "approximateDecoded": "10% ±1%"
  }
}
```

- `bestGuess` is used for partial decoding.
- `translations` is a history of guesses (`-1` for the hidden original, `0` for the alien, plus new guesses).
- `progress.approximateDecoded` indicates overall success with a ±1% margin.

### 6.2 Single Function Approach

When processing each JSON value:
1. If it matches a known token in the metadata, return `bestGuess` (decoding) or the alien form (encoding).
2. If it’s part of the math rosetta stone, keep that fixed mapping.
3. If new, classify it (word vs. single char), generate a zword or ASCII code, update the metadata in memory, and return the alien representation.

---

## 7. Example Flow

1. **Encoding**:
   - We see `0` (digit) → `ç` from the rosetta.  
   - We see `+` → `²` from the rosetta.  
   - We see `apple` (5 letters) → generate something like `zabir`.  
   - Output `zlang_mystery.json` with these replacements, record them in `translation_metadata.json`.

2. **Guessing**:
   - The solver guesses “zabir” → “apple.” We add a guess to the `translations`, set `bestGuess = "apple"`.
   - Next decode step replaces “zabir” with “apple” in `_translated.json`.

3. **Progress**:
   - If correct, the system internally increments the count of correct tokens, e.g., “12% ±1%.”  
   - The solver only sees the approximate figure, not which tokens are correct.

4. **Rollbacks**:
   - If “zabir” was wrong, we remove the guess or revert `bestGuess` to “zabir.”

---

## 8. FAQ

1. **What if a single-letter English word like “I” or “a” appears?**  
   - Treat it as a word, generating a multi-letter token like `zix` or `za` (or however your length rule dictates).  

2. **Can we use Unicode beyond `[130..255]` for single chars?**  
   - Yes, as long as it’s a single codepoint outside `[a-zA-Z0-9]` and not conflicting with the rosetta stone.

3. **Is the original `english_zlang_source.json` ever changed?**  
   - No. We only read from it. The puzzle artifacts (metadata, mystery JSON, partial translations) are separate.

4. **How do we ensure no collisions among zwords or extended ASCII codes?**  
   - Maintain a set of used codes/tokens in memory so each new assignment is unique.

5. **Why do digits and operators have a special rosetta stone?**  
   - It’s part of the puzzle design. We want consistent, unchanging references for arithmetic, ensuring no confusion or re-mapping of fundamental math symbols.

---

## 9. Conclusion

This puzzle system:

- **Locks** digits `0–9` and arithmetic symbols `+ - * / = ^ #` to a **hard-coded** map.
- **Generates** “pronounceable” zwords (prefix `z`) for multi-letter English words.
- **Assigns** single-character non-alphabetic (non-rosetta) tokens to **ASCII ≥ 130** codepoints.
- **Tracks** everything in `translation_metadata.json`, with each token’s “bestGuess” used for partial decoding.
- **Reveals** only an approximate progress measure (`±1%`) to guard puzzle integrity.

Use this system to **encode** your English text, share the “mystery” file, and iterate on guesses until the entire puzzle is solved!

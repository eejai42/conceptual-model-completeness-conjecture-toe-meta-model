# zlang/progress.py
#
# Provides approximate correctness logic.
# This can be integrated with or called by metadata_manager.

import random

def calculate_approximate_progress(total_tokens: int, correct_tokens: int) -> str:
    """
    Return a string like '39% ±1%' that approximates
    the ratio of correct_tokens / total_tokens,
    adding a random +/- 1% offset to obscure exact correctness.
    """
    if total_tokens <= 0:
        return "0% ±1%"

    # Compute raw percentage
    base_percentage = int(round((correct_tokens / total_tokens) * 100))

    # Add random offset of -1, 0, or +1
    offset = random.choice([-1, 0, 1])
    approximate = base_percentage + offset

    # Clamp between 0% and 100%
    approximate = max(0, min(100, approximate))

    return f"{approximate}% ±1%"

# core_lambda_functions.py

def COUNT(collection):
    """Returns the number of items in 'collection'."""
    return len(collection)


def MAX(collection_of_numbers):
    """Returns the maximum numeric value in the collection."""
    if not collection_of_numbers:
        raise ValueError("MAX function received an empty collection.")
    return max(collection_of_numbers)


def SUM(collection_of_numbers):
    """Returns the sum of numeric values in the collection."""
    return sum(collection_of_numbers)


def CONTAINS(collection_of_values, target_value):
    """Returns True if 'target_value' appears in 'collection_of_values', otherwise False."""
    return target_value in collection_of_values


def EQUAL(valueA, valueB):
    """Compares valueA and valueB for equality, returning boolean."""
    return valueA == valueB


def IF(condition_boolean, value_if_true, value_if_false):
    """Returns value_if_true if condition_boolean is True, else returns value_if_false."""
    return value_if_true if condition_boolean else value_if_false

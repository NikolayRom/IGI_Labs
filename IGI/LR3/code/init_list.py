"""
Purpose: Module for list initialization (generators and builder)
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

import random
from validation import inputFloatNum

def random_sequence_generator(size):
    """
    Generator function. Yields 'size' random float numbers.
    """
    for _ in range(size):
        # Using a generator to optimize memory usage
        yield round(random.uniform(-10.0, 10.0), 2)

def manual_sequence_generator(size):
    """
    Generator function. Yields numbers typed by the user.
    """
    print(f"Please enter {size} float numbers:")
    for i in range(size):
        # Each iteration yields one user input to the caller
        yield inputFloatNum(f"Element {i + 1}: ")

def build_list_from_sequence(sequence):
    """
    Takes an initialization sequence (generator) as input
    and returns a fully initialized list. (Satisfies Lab Req. 9)
    """
    # Converting the generator/iterator into a physical list in memory
    return list(sequence)
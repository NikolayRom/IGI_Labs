"""
Purpose: Task 2 - Counting positive numbers in a sequence until 10 is entered
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

from validation import inputIntNum

def print_start_message():
    """
    Prints the introductory message and instructions for Task 2.
    """
    print("\n--- Task 2: Count positive numbers ---")
    print("Enter integers one by one.")
    print("To finish the input and calculate the result, enter the number 10.\n")

def print_end_message(count):
    """
    Prints the final count of positive numbers.
    """
    print("-" * 45)
    print(f"Total count of positive numbers entered: {count}")
    print("-" * 45 + "\n")

def task2():
    """
    Main business function for Task 2.
    Loops to accept integers from the user, counts positive ones,
    and stops when 10 is entered.
    """
    print_start_message()
    pos_count = 0

    while True:
        num = inputIntNum("Enter an integer: ")
        
        if num == 10:
            break
        elif num > 0:
            pos_count += 1

    print_end_message(pos_count)
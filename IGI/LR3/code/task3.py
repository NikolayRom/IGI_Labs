"""
Purpose: Task 3 - String analysis (Check if string is a hexadecimal number)
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

from validation import inputStr

def is_hex_number(text):
    """
    Analyzes the string to check if it represents a hexadecimal number.
    Does NOT use regular expressions. Handles optional '0x' prefix and signs.
    """
    clean_text = text.strip().lower()
    
    if clean_text.startswith('-') or clean_text.startswith('+'):
        clean_text = clean_text[1:]
        
    if clean_text.startswith('0x'):
        clean_text = clean_text[2:]
        
    if not clean_text:
        return False

    valid_hex_chars = "0123456789abcdef"
    for char in clean_text:
        if char not in valid_hex_chars:
            return False
            
    return True

def print_hex_result(is_hex, original_text):
    """
    Prints the result of the hexadecimal check in a friendly format.
    """
    print("\n" + "-" * 45)
    if is_hex:
        print(f'SUCCESS: "{original_text}" IS a valid hexadecimal number.')
    else:
        print(f'ERROR: "{original_text}" IS NOT a valid hexadecimal number.')
    print("-" * 45 + "\n")

def task3():
    """
    Main business function for Task 3.
    Accepts a string from the user, checks if it's hex, and prints the result.
    """
    print("\n--- Task 3: Hexadecimal Number Analyzer ---")
    user_string = inputStr("Enter a string to check: ")
    
    result = is_hex_number(user_string)
    
    print_hex_result(result, user_string)
"""
Purpose: Task 1 - Calculating function value using power series expansion
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

import math
from validation import inputEpsila, inputArgumentX

def calculate_exact_f(x):
    """
    Calculates the exact value of the function using the math module.
    Formula: ln(1 + x)
    """
    return math.log(1 + x)

def taylor_series_term(n, x):
    """
    Calculates the n-th term of the Taylor series for ln(1 + x).
    Formula: (-1)^(n-1) * (x^n) / n
    """
    return ((-1) ** (n - 1)) * (x ** n) / n

def print_result_table(x, n, f_value, exact_value, eps):
    """
    Prints the calculated data in a formatted table matching the task requirements.
    """
    print('\n' + '-' * 75)
    print(f'| {"x":^10} | {"n":^5} | {"F(x)":^15} | {"Math F(x)":^15} | {"eps":^10} |')
    print('-' * 75)
    print(f'| {x:^10.4f} | {n:^5} | {f_value:^15.6f} | {exact_value:^15.6f} | {eps:^10.6f} |')
    print('-' * 75 + '\n')

def task1():
    """
    Main business function for Task 1.
    Handles user input, performs the iterative calculation of the power series,
    and calls the output function.
    """
    print("--- Task 1: Power Series Expansion ---")
    eps = inputEpsila("Enter epsilon (calculation accuracy): ")
    x = inputArgumentX("Enter argument x (|x| < 1): ")

    max_iter = 500
    exact_value = calculate_exact_f(x)
    f_value = 0.0
    n = 0

    for i in range(1, max_iter + 1):
        term = taylor_series_term(i, x)
        f_value += term
        
        # Convergence check: stop when the term becomes smaller than epsilon
        if abs(term) <= eps:
            n = i
            break
    else:
        # This block executes only if the loop finishes without hitting 'break'
        n = max_iter
        print(f"\nWarning: Maximum iterations ({max_iter}) reached without achieving required accuracy.")

    print_result_table(x, n, f_value, exact_value, eps)
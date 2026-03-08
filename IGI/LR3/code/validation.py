"""
Purpose: Input validation module (decorator and input functions)
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

def userInputNum(func):
    """
    Decorator to handle user input errors.
    Repeats the input prompt until the user enters valid data.
    """
    def wrapper(prompt):
        while True:
            try:
                return func(prompt)
            except ValueError:
                print("Error: Wrong input, please try again!\n")
    return wrapper


@userInputNum
def inputIntNum(prompt):
    """
    Requests an integer value from the user.
    """
    return int(input(prompt))


@userInputNum
def inputFloatNum(prompt):
    """
    Requests a float value from the user.
    """
    return float(input(prompt))


@userInputNum
def inputStr(prompt):
    """
    Requests a non-empty string from the user.
    """
    user_str = input(prompt).strip()
    if not user_str:
        print("String cannot be empty")
        raise ValueError()
    return user_str


@userInputNum
def inputEpsila(prompt):
    """
    Requests an epsilon (accuracy) value greater than 0.
    """
    eps = float(input(prompt))
    if eps <= 0:
        print("Epsilon must be greater than 0.")
        raise ValueError()
    return eps


@userInputNum
def inputArgumentX(prompt):
    """
    Requests an argument X where |X| < 1.
    """
    x = float(input(prompt))
    if abs(x) >= 1:
        print("Absolute value of X must be less than 1.")
        raise ValueError()
    return x


@userInputNum
def inputSizeList(prompt):
    """
    Requests the size of a list (must be an integer > 0).
    """
    size = int(input(prompt))
    if size <= 0:
        print("Size must be a positive integer.")
        raise ValueError()
    return size
"""
Brief purpose: Module for user input validation and exception handling.
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 15.03.2026
"""

import matplotlib.colors as mcolors

class Validation:
    """Class containing static methods for validating user input."""

    @staticmethod
    def userInputNum(func):
        """
        Decorator to handle ValueError exceptions during user input.
        Keeps prompting the user until valid input is provided.
        """
        def wrapper(prompt):
            while True:
                try:
                    return func(prompt)
                except ValueError:
                    print("Error: Wrong input, please try again!\n")
        return wrapper

    @staticmethod
    @userInputNum
    def inputIntNum(prompt):
        """Prompts the user for an integer number and returns it."""
        return int(input(prompt))

    @staticmethod
    @userInputNum
    def inputFloatNum(prompt):
        """Prompts the user for a floating-point number and returns it."""
        return float(input(prompt))

    @staticmethod
    @userInputNum
    def inputStr(prompt):
        """Prompts the user for a string, ensuring it is not empty."""
        user_str = input(prompt).strip()
        if not user_str:
            print("Error: String cannot be empty.")
            raise ValueError()
        return user_str
    
    @staticmethod
    @userInputNum
    def inputEpsila(prompt):
        """
        Requests an epsilon (accuracy) value greater than 0.
        """
        eps = Validation.inputFloatNum(prompt)
        if eps <= 0:
            print("Epsilon must be greater than 0.")
            raise ValueError()
        return eps


    @staticmethod
    @userInputNum
    def inputArgumentX(prompt):
        """
        Requests an argument X where |X| < 1.
        """
        x = Validation.inputFloatNum(prompt)
        if abs(x) >= 1:
            print("Absolute value of X must be less than 1.")
            raise ValueError()
        return x
    
    @staticmethod
    @userInputNum
    def inputFigureSide(prompt):
        """
        Requests a side length of figure where length > 0
        """
        side = Validation.inputFloatNum(prompt)
        if side <= 0:
            print("Error: Side length must be strictly greater than 0.\n")
            raise ValueError()
        return side
    
    @staticmethod
    @userInputNum
    def inputFigureAngle(prompt):
        """
        Requests an angle of figure where 90 < angle < 180 
        """
        angle = Validation.inputFloatNum(prompt)
        if 90 < angle < 180:
            return angle
        print("Error: The angle must be obtuse (between 90 and 180 degrees).\n")
        raise ValueError()
    
    @staticmethod
    @userInputNum
    def inputFigureColor(prompt):
        """
        Requests a color of figure where color is exist
        """
        color = Validation.inputStr(prompt).lower()
        if mcolors.is_color_like(color):
            return color
        print(f"Error: '{color}' is not recognized as a valid color. Please try again.\n")
        raise ValueError()
    
    @staticmethod
    @userInputNum
    def inputMatrixDimension(prompt):
        """
        Requests a dimension of matrix where dimension >= 2
        """
        val = Validation.inputIntNum(prompt)
        if val >= 2:
            return val
        print("Error: Matrix dimension must be at least 2 for a proper demonstration.\n")
        raise ValueError()
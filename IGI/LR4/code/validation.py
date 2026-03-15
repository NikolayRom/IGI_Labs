"""
Brief purpose: Module for user input validation and exception handling.
Lab number and title: Lab 4 - Работа с файлами, классами, сериализаторами, регулярными выражениями и стандартными библиотеками
Version: 1.0
Developer: Романов Николай Викторович
Date: 15.03.2026
"""

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
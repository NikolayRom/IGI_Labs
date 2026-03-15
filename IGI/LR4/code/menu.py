"""
Brief purpose: Module for handling the console menu logic and repeating tasks.
Lab number and title: Lab 4 - Работа с файлами, классами, сериализаторами, регулярными выражениями и стандартными библиотеками
Version: 1.0
Developer: Романов Николай Викторович
Date: 15.03.2026
"""

from validation import Validation

class Menu:
    """Class responsible for menu loops and task repetition."""

    @staticmethod
    def main_loop(task_func):
        """
        Executes the provided task function and asks the user if they want to 
        repeat it or exit to the main menu.
        """
        while True:
            task_func()
            
            print("\nOptions:")
            print("1) Repeat the task")
            print("2) Exit to main menu")
            
            while True:
                choice = Validation.inputIntNum("Enter your choice (1 or 2): ")
                if choice == 1:
                    print("\n" + "="*50 + "\n")
                    break 
                elif choice == 2:
                    return 
                else:
                    print("Incorrect choice, please try again.")
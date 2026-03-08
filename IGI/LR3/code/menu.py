"""
Purpose: Menu and application loop module
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

from validation import inputIntNum

def main_loop(task_func):
    """
    Executes the passed task function and asks the user 
    if they want to repeat the task or exit.
    """
    while True:
        task_func()
        
        print("\nOptions:")
        print("1) Repeat the task")
        print("2) Exit to main menu / Quit")
        
        while True:
            choice = inputIntNum("Enter your choice (1 or 2): ")
            if choice == 1:
                print("\n" + "="*50 + "\n")
                break 
            elif choice == 2:
                return 
            else:
                print("Incorrect choice, please try again.")
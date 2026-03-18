"""
Brief purpose: Main entry point of the application, connecting all task modules.
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 15.03.2026
"""

from validation import Validation
from menu import Menu
from task1 import Service as task1
from task2 import Service as task2
from task3 import Service as task3
from task4 import Service as task4
from task5 import Service as task5
from task6 import Service as task6

class Main:
    """Main class to run the application."""

    @staticmethod
    def main():  
        """Displays the main menu and handles routing to specific tasks."""
        while True:
            print("\n" + "="*40)
            print(f"{'MAIN MENU':^40}")
            print("="*40)
            print("1) Run Task 1")
            print("2) Run Task 2")
            print("3) Run Task 3")
            print("4) Run Task 4")
            print("5) Run Task 5")
            print("6) Run Task 6")
            print("0) Exit Program")
            print("="*40)
            
            choice = Validation.inputIntNum("Enter task number (0-6): ")
            
            match choice:
                case 1:
                    Menu.main_loop(task1.presentation)
                case 2:
                    Menu.main_loop(task2.presentation)
                case 3:
                    Menu.main_loop(task3.presentation)
                case 4:
                    Menu.main_loop(task4.presentation)
                case 5:
                    Menu.main_loop(task5.presentation)
                case 6:
                    Menu.main_loop(task6.presentation)
                case 0:
                    break
                case _:
                    print("Invalid choice. Please select an existing task.")

if __name__ == "__main__":
    Main.main()
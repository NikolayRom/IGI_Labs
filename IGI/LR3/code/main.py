"""
Purpose: Main application entry point and Main Menu
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

from validation import inputIntNum
from menu import main_loop
from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5

def main():
    """
    Main entry point. Displays the Main Menu and routes the user
    to the selected task.
    """
    
    while True:
        print("\n" + "="*40)
        print(f"{'MAIN MENU':^40}")
        print("="*40)
        print("1) Run Task 1")
        print("2) Run Task 2")
        print("3) Run Task 3")
        print("4) Run Task 4")
        print("5) Run Task 5")
        print("0) Exit Program")
        print("="*40)
        
        choice = inputIntNum("Enter task number (0-5): ")
        
        match choice:
            case 1:
                main_loop(task1)
            case 2:
                main_loop(task2)
            case 3:
                main_loop(task3)
            case 4:
                main_loop(task4)
            case 5:
                main_loop(task5)
            case 0:
                break
            case _:
                print("Invalid choice. Please select an existing task.")

if __name__ == "__main__":
    main()
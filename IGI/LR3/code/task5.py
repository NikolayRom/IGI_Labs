"""
Purpose: Task 5 - Processing lists of float numbers
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

from validation import inputSizeList, inputIntNum
import init_list

def find_max_abs_element(lst):
    """
    Finds and returns the element with the maximum absolute value.
    """
    if not lst:
        return 0.0
    # Pythonic way: ищем максимум, используя abs() как критерий сравнения
    return max(lst, key=abs)

def sum_before_last_positive(lst):
    """
    Calculates the sum of elements located before the last positive element.
    """
    last_pos_index = -1
    
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] > 0:
            last_pos_index = i
            break
            
    if last_pos_index == -1:
        return None 
        
    return sum(lst[:last_pos_index])

def print_task5_results(lst, max_abs, sum_before):
    """
    Prints the list and the calculation results (Lab Task 5 req 3 and 4).
    """
    print("\n" + "=" * 50)
    print(f"{'TASK 5 RESULTS':^50}")
    print("=" * 50)
    
    print("1) Original List:")
    print(f"   {lst}\n")
    
    print("2) Element with maximum absolute value:")
    print(f"   {max_abs}\n")
    
    print("3) Sum of elements before the last positive one:")
    if sum_before is not None:
        print(f"   {round(sum_before, 2)}")
    else:
        print("   -> No positive elements found in the list.")
    print("=" * 50 + "\n")

def task5():
    """
    Main business function for Task 5.
    """
    print("\n--- Task 5: Float List Processing ---")
    
    size = inputSizeList("Enter the size of the list (integer > 0): ")
    
    print("\nChoose initialization method:")
    print("1) Manual input")
    print("2) Random generation (using generator)")
    
    while True:
        choice = inputIntNum("Enter your choice (1 or 2): ")
        if choice == 1:
            sequence = init_list.manual_sequence_generator(size)
            break
        elif choice == 2:
            sequence = init_list.random_sequence_generator(size)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    user_list = init_list.build_list_from_sequence(sequence)
    
    max_abs = find_max_abs_element(user_list)
    sum_before = sum_before_last_positive(user_list)
    
    print_task5_results(user_list, max_abs, sum_before)
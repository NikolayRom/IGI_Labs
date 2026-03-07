import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'check'))

from inputFloatNum import inputFloatNum

def enterList(size):
    user_list = []

    for i in range(size):
        print(f"Input {i+1} element of list:")
        user_list.append(inputFloatNum())
    
    return user_list
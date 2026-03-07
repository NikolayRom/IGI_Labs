import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'check'))

from inputStr import inputStr
from printEnd import printEnd

print("Enter string:")
str = inputStr()
test_str = str.lower()
isHex = True
correct_str = "0123456789abcdef"

for c in test_str:
    if correct_str.find(c) == -1:
        isHex = False
        break

printEnd(isHex)
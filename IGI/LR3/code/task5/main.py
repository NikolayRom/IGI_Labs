import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'check'))

from inputSizeList import inputSizeList
from findLastPosNum import findLastPosNum
from enterList import enterList
from findMaxAbs import findMaxAbs
from sumBeforePos import sumBeforePos

print("Input size of list:")
size = inputSizeList()

user_list = enterList(size)
print(findMaxAbs(user_list))

print(sumBeforePos(user_list))

print(user_list)
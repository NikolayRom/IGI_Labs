import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'check'))
from inputIntNum import inputIntNum
from printStart import printStart
from printEnd import printEnd

last_num = 0
pos_count = 0

printStart()

while True:
    last_num = inputIntNum()
    if last_num == 10:
        break
    elif last_num > 0:
        pos_count += 1

printEnd(pos_count)
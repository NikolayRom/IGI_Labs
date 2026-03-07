import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'check'))

from mathFunction import F
from differenceEpsila import diff
from inputEpsila import inputEpsila
from inputArgumentX import inputArgumentX
from seriesTaylor import seriesTaylor
from printEnd import printEnd

print("Enter epsila:")
eps = inputEpsila()

print("Enter argument (x):")
x = inputArgumentX()

max_iter = 500
F_value = F(x)
f_value = 0.0
sum = 0.0
n = 0
err = False

for i in range(1, max_iter + 1):
    sum += seriesTaylor(i, x)
    if diff(sum, F_value, eps):
        n = i
        f_value = sum
        break
    elif i == max_iter and not diff(sum, F_value, eps):
        err = True
        f_value = sum
        n = i
        break

printEnd(x, n, f_value, F_value, eps, err)
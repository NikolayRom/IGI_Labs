from userInputNum import userInputNum
from inputFloatNum import inputFloatNum

@userInputNum
def inputEpsila():
    eps = inputFloatNum()
    if(eps <= 0):
        raise ValueError()
    return eps
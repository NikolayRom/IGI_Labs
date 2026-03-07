from userInputNum import userInputNum
from inputFloatNum import inputFloatNum

@userInputNum
def inputArgumentX():
    x = inputFloatNum()
    if(abs(x) >= 1):
        raise ValueError()
    return x
from userInputNum import userInputNum
from inputIntNum import inputIntNum

@userInputNum
def inputSizeList():
    size = inputIntNum()
    if(size <= 0):
        raise ValueError()
    return size
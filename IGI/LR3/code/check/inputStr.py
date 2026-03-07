from userInputNum import userInputNum

@userInputNum
def inputStr():
    str = input()
    if(not str):
        raise ValueError()
    return str
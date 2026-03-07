from findLastPosNum import findLastPosNum

def sumBeforePos(user_list):
    sum = 0.0
    index = findLastPosNum(user_list)
    if index != -1:
        for i in range(index):
            sum += user_list[i]
    return sum
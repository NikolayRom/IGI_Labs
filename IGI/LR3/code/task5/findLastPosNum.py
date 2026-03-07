def findLastPosNum(lst):
    index = -1
    el = lst[0]
    lst.reverse()
    for i in lst:
        if i > 0:
            el = i
            break
    lst.reverse()
    index = lst.index(el)
    return index
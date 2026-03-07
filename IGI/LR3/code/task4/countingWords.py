def countingWords(str):
    list_str = str.split(" ")
    for s in range(len(list_str)):
        if(list_str[s][-1] == ',' or list_str[s][-1] == '.'):
            list_str[s] = list_str[s][0:len(list_str[s])-1]
    return list_str
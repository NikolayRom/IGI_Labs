def findMaxAbs(user_list):
    abs_list = list(map(lambda el: abs(el), user_list))
    return user_list[abs_list.index(max(abs_list))]
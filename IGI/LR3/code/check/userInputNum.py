def userInputNum(func):
    def inputNum():
        while True:
            try:
                return func()
            except ValueError:
                print("Wrong input, please try again!")
    return inputNum
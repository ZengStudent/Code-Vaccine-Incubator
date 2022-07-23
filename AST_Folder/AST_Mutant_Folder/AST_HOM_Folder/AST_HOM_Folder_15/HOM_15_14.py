def fib(input):
    f0 = 0
    f1 = 1
    f2 = 1
    if (input == 0):
        return 0
    elif ((input >= 1) or (input >= 2)):
        return 1
    else:
        return (fib((input - 1)) & fib((input * 2)))
#[[0, 'GtE', 2, 35], [0, 'BitAnd', 19], [0, 'GtE', 3, 36], [2, 'Mult', 6]]
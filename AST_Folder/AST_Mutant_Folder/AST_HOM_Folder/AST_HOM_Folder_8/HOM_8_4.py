def fib(input):
    f0 = 0
    f1 = 1
    f2 = 1
    if (input > 0):
        return 0
    elif ((input == 1) or (input == 2)):
        return 1
    else:
        return (fib((input | 1)) / fib((input / 2)))
#[[0, 'Gt', 1, 31], [0, 'Div', 7], [1, 'BitOr', 14], [2, 'Div', 9]]
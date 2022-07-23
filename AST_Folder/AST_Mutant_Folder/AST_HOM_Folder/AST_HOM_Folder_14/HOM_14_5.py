def fib(input):
    f0 = 0
    f1 = 1
    f2 = 1
    if (input == 0):
        return 0
    elif ((input == 1) or (input == 2)):
        return 1
    else:
        return (fib((input & 1)) + fib((input % 2)))
#[[1, 'BitAnd', 20], [2, 'Mod', 12]]
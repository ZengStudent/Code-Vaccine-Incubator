def fib(input):
    f0 = 0
    f1 = 1
    f2 = 1
    if (input == 0):
        return 0
    elif ((input != 1) or (input != 2)):
        return 1
    else:
        return (fib((input & 1)) ^ fib((input & 2)))
#[[2, 'BitAnd', 21], [0, 'BitXor', 16], [0, 'NotEq', 2, 23], [1, 'BitAnd', 20], [0, 'NotEq', 3, 24]]
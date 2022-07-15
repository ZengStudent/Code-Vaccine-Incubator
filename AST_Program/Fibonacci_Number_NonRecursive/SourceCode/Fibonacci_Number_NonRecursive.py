def fib(input):
    if (type(input) != int):
        return 'input is not integer'
    if (input < 0):
        return 'input less than zero'
    if (input == 0):
        return 0

    if input == 1:
        return [1]
    if input == 2:
        return [1, 1]
    fibs = [1, 1]
    for i in range(2, input):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

#print(fib(10))
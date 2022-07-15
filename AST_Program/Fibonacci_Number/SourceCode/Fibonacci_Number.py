def fib(input):
    f0 = 0
    f1 = 1
    f2 = 1
    #print(input)
    if(type(input) != int):
        return 'input is not integer'
    if(input < 0):
        return 'input less than zero'
    elif(input == 0):
        return 0
    elif(input == 1 or input == 2):
        return 1
    else:
       return fib(input - 1) + fib(input - 2)

# Driver Program
#print(fib(37))
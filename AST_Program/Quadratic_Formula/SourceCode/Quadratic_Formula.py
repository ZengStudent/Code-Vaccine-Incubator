import cmath

def quf(input_a,input_b,input_c):

    # calculate the discriminant
    d = (input_b ** 2) - (4 * input_a * input_c)

    # find two solutions
    sol1 = (-input_b - cmath.sqrt(d)) / (2 * input_a)
    sol2 = (-input_b + cmath.sqrt(d)) / (2 * input_a)

    return '{0},{1}'.format(sol1, sol2)

# Driver Program
#print(quf(4910, 7055, 6592))

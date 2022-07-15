def bubble_sort(data):
    temp = data
    n = len(temp)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if temp[j] > temp[j + 1]:
                temp[j], temp[j + 1] = temp[j + 1], temp[j]

    return temp


#input_data = [-31,-74118,-212,0,-1,418,326,91,-5,218,3210,48941,192,-329,1820,941,-357,-154,185]

#print(bubble_sort(input_data))
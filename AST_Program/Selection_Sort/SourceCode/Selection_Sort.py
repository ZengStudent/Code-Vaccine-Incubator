
def selection_sort(input):
    for i in range(len(input)):
        min_idx = i
        for j in range(i + 1, len(input)):
            if input[min_idx] > input[j]:
                min_idx = j


        input[i], input[min_idx] = input[min_idx], input[i]

    return input
# Driver code to test above
input = [64, 25, 12, 22, 11]
print(selection_sort(input))

def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]

        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j = j - 1
        arr[j + 1] = key

    return arr

# Driver code to test above
# arr = [-31,-74118,-212,0,-1,418,326,91,-5,218,3210,48941,192,-329,1820,941,-357,-154,185]
#
# print(insertionSort(arr))
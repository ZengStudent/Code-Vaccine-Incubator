def linear_search(arr, x):

    for i in range(len(arr)):
        if arr[i] == x:
            return i

    return 'No'



# input = [52,19,300,3912,3328,447,21861,1369,3179,581]
# print(linear_search(input,581))




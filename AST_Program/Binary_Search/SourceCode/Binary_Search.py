#input_data = [4, 6, 10, 10, 16, 17, 18, 23, 24, 25, 26, 27, 29, 29, 35, 35, 37, 39, 41, 43, 47, 52, 53, 56, 59, 61, 65, 67, 68, 70, 70, 71, 73, 74, 76, 77, 77, 77, 79, 81, 81, 85, 86, 87, 90, 91, 94, 94, 96, 98]
def binary_search(data,start,maxlen,aim):
    if maxlen >= start:

        mid = start + (maxlen - start) // 2

        if data[mid] == aim:
            return mid
        elif data[mid] > aim:
            return binary_search(data, start, mid - 1, aim)
        else:
            return binary_search(data, mid + 1, maxlen, aim)

    else:
        return 'Not Found'

# print(sorted(input_data))
# print(binary_search(sorted(input_data),0,len(input_data)-1,10))



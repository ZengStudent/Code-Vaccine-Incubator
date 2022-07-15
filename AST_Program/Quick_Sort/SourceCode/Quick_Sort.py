def quick_sort(nums):
    less = []
    equal = []
    greater = []

    if len(nums) > 1:
        pivot = nums[len(nums) // 2]
        for i in nums:
            if i < pivot:
                less.append(i)
            elif i == pivot:
                equal.append(i)
            elif i > pivot:
                greater.append(i)
        return quick_sort(less) + equal + quick_sort(greater)
    else:
        return nums


#print(quick_sort([-31,-74118,-212,0,-1,418,326,91,-5,218,3210,48941,192,-329,1820,941,-357,-154,185]))
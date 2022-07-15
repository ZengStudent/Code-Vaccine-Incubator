def tri(a,b,c):
    result = ''
    # 判斷是否可以形成三角形
    if (a + b <= c):
        result = 'No'
    # 判斷是否可以形成銳角三角形
    elif (a * a + b * b < c * c):
        result = 'Obtuse'
    # 判斷是否可以形成直角三角形
    elif (a * a + b * b == c * c):
        result = 'Right'
    # 判斷是否可以形成鈍角三角形
    elif (a * a + b * b > c * c):
        result = 'Acute'
    return result


#print(tri(31,66,99))
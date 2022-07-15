def tri(a,b,c):
    result = ''
    # (1) 判斷兩邊相加是否大於第三邊
    if a + b >= c and b + c >= a and c + a >= b:
        result = ''
    else:
        return 'No'

    # (2) 判斷三角形類型(角度、長度)

    # 判斷是否為正三角形
    if(a==b and b==c):
        result = 'Equilateral'
    # 判斷是否為等腰三角形
    elif((a==b and a!=c and b!=c) or (b==c and b!=a and c!=a) or (a==c and a!=b and c!=b)):
        result = 'Isosceles'
        # 判斷是否可以形成鈍角三角形
        if (a * a + b * b < c * c):
            result = 'Obtuse Isosceles'
        # 判斷是否可以形成直角三角形
        elif (a * a + b * b == c * c):
            result = 'Right Isosceles'
        # 判斷是否可以形成銳角三角形
        elif (a * a + b * b > c * c):
            result = 'Acute Isosceles'
    # 判斷是否為不等邊三角形
    elif(a!=b and b!=c and c!=a):
        result = 'Scalane'
        # 判斷是否可以形成鈍角三角形
        if (a * a + b * b < c * c):
            result = 'Obtuse Scalane'
        # 判斷是否可以形成直角三角形
        elif (a * a + b * b == c * c):
            result = 'Right Scalane'
        # 判斷是否可以形成銳角三角形
        elif (a * a + b * b > c * c):
            result = 'Acute Scalane'

    return result


#print(tri(3,4,5))
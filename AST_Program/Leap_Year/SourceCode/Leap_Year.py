def leap(input_year):
    if (input_year % 4) == 0:
        if (input_year % 100) == 0:
            if (input_year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False



#print(leap(1990))
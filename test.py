def get_percentage(number, ndigits=None):
    
    if ndigits==None:
        return str(round(number * 100))+"%"
    else:
        return str(round(number * 100, ndigits))+"%"
    pass
print(get_percentage(0.0123))      # 1%
print(get_percentage(0.0123, 0))   # 1.0%
print(get_percentage(0.0123, 1))   # 1.2%
print(get_percentage(0.0123, 10))  # 1.23%
print(get_percentage(0.0296, 1))   # 3.0%

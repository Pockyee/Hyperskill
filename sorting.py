import math

data = []
while True:
    try:
        user_input = input().split()
        data.extend(user_input)
    except EOFError:
        break

num_list = [int(x) for x in data]

x = len(num_list)
y = max(num_list)
z = num_list.count(y)

print(f"Total numbers: {x}.\nThe greatest number: {y} ({z} time(s)).")

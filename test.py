import string

s = "Biden’s pick to head US environment agency heartens scientists"

# Create a new string by replacing each punctuation with '_'
new_s = ""
for i in s:
    if i not in string.ascii_letters:
        new_s += "_"
    else:
        new_s += i

print(new_s)

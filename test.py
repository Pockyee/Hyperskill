import itertools

first_names = ['Anna', 'Catarina']
middle_names = ['Luisa', 'Maria']

x= itertools.product(first_names, middle_names)

for firstname,middlename in x:
    print(firstname+" "+middlename)
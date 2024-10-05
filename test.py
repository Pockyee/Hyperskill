import sys  

args = sys.argv  

if len(args) != 3:
    print("The script should be called with two arguments, the first and the second number to be multiplied")

else:
    first_num = float(args[1])  
    second_num = float(args[2])

    product = first_num * second_num

    print("The product of " + args[1] + " times " + args[2] + " equals " + str(product))
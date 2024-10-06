import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("-dataType", default="word")
parser.add_argument("-sortingType", default="natural")

args = parser.parse_args()


# def mergesort_list(x):
#     if len(x) <= 1:
#         return x
#     else:
#         mid = len(x) // 2
#         left = mergesort_list(x[:mid])
#         right = mergesort_list(x[mid:])
#         return merge(left, right)
#
#
# def merge(left, right):
#     new = []
#     i = j = 0
#     while i < len(left) and j < len(right):
#         if left[i] < right[j]:
#             new.append(left[i])
#             i += 1
#         else:
#             new.append(right[j])
#             j += 1
#     new.extend(left[i:])
#     new.extend(right[j:])
#     return new


def read():
    while True:
        try:
            if args.dataType == "long":
                user_input = input().split()
                data.extend(map(int, user_input))
            if args.dataType == "line":
                user_input = input()
                data.append(user_input)
            elif args.dataType == "word":
                user_input = input().split()
                data.extend(user_input)
        except EOFError:
            break
    for element in data:
        if element in user_dict:
            user_dict[element] += 1
        else:
            user_dict[element] = 1
    return user_dict


converter = {"long": "numbers", "word": "words", "line": "lines"}
data = []
user_dict = {}
read()
print(f"Total {converter[args.dataType]}: {len(data)}.")
if args.sortingType == "natural":
    if args.dataType == "line":
        print("Sorted data: \n" + "\n".join(map(str, sorted(data))))
    else:
        print("Sorted data: "+" ".join(map(str,sorted(data))))
elif args.sortingType == "byCount":
    sorted_dict = {key: user_dict[key] for key in sorted(user_dict)}
    sorted_keys = sorted(sorted_dict, key=lambda key: user_dict[key])
    for i in sorted_keys:
        print(f"{i}: {sorted_dict[i]} time(s), {math.floor(sorted_dict[i]/len(data)*100)}%")
else:
    print("Error!")
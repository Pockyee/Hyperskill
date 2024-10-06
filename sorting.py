import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("-dataType", default="word")
parser.add_argument("-sortIntegers", action="store_true")

args = parser.parse_args()


def mergesort_list(x):
    if len(x) <= 1:
        return x
    else:
        mid = len(x) // 2
        left = mergesort_list(x[:mid])
        right = mergesort_list(x[mid:])
        return merge(left, right)


def merge(left, right):
    new = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            new.append(left[i])
            i += 1
        else:
            new.append(right[j])
            j += 1
    new.extend(left[i:])
    new.extend(right[j:])
    return new


def sort_integers():
    while True:
        try:
            user_input = input().split()
            data.extend(user_input)
        except EOFError:
            break

    num_list = [int(x) for x in data]
    new_list = mergesort_list(num_list)
    string = " ".join([str(x) for x in new_list])
    x = len(num_list)

    print(f"Total numbers: {x}.\nSorted data:{string}")


def integers():
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

    print(
        f"Total numbers: {x}.\nThe greatest number: {y} ({z} time(s), {math.floor(z/x*100)}%)."
    )


def lines():
    while True:
        try:
            user_input = input()
            data.append(user_input)
        except EOFError:
            break

    x = len(data)
    y = max(data, key=len)
    z = data.count(y)

    print(
        f"Total lines: {x}.\nThe longest line:\n{y}\n({z} time(s), {math.floor(z/x*100)}%)."
    )


def words():
    while True:
        try:
            user_input = input().split()
            data.extend(user_input)
        except EOFError:
            break

    x = len(data)
    y = max(data, key=len)
    z = data.count(y)

    print(
        f"Total words: {x}.\nThe longest word: {y} ({z} time(s), {math.floor(z/x*100)}%)."
    )


data = []
if args.sortIntegers:
    sort_integers()
elif args.dataType == "long":
    integers()
elif args.dataType == "line":
    lines()
elif args.dataType == "word":
    words()

import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("-dataType", default="word")
args = parser.parse_args()


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

    print(f"Total words: {x}.\nThe longest word: {y} ({z} time(s), {math.floor(z/x*100)}%).")


data = []

if args.dataType == "long":
    integers()
elif args.dataType == "line":
    lines()
elif args.dataType == "word":
    words()

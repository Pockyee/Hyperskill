import argparse
import math
from os import abort


class DataTypeError(Exception):
    def __str__(self):
        return "No data type defined!"


class SortingTypeError(Exception):
    def __str__(self):
        return "No sorting type defined!"


parser = argparse.ArgumentParser()
parser.add_argument("-dataType", nargs="?", default="word")
parser.add_argument("-sortingType", nargs="?", default="natural")
parser.add_argument("-inputFile", nargs="?")
parser.add_argument("-outputFile", nargs="?")

try:
    args, unknown = parser.parse_known_args()
    assert len(unknown) == 0
    if args.dataType is None:
        raise DataTypeError
    if args.sortingType is None:
        raise SortingTypeError
except DataTypeError as de:
    print(de)
    exit()
except SortingTypeError as se:
    print(se)
    exit()
except AssertionError:
    for i in unknown:
        print(f'"{i}" is not a valid parameter. It will be skipped.')


def read():
    while True:
        try:
            if args.dataType == "long":
                user_input = input().split()
                for i in user_input:
                    try:
                        value = int(i)
                    except ValueError:
                        print(f'"{i}" is not a long. It will be skipped.')
                    else:
                        data.append(value)
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


def file_read(userfile):
    global data
    file = open(userfile, "r")
    if args.dataType == "long":
        user_input = file.read().split()
        for i in user_input:
            try:
                value = int(i)
            except ValueError:
                print(f'"{i}" is not a long. It will be skipped.')
            else:
                data.append(value)
    if args.dataType == "line":
        data = file.readlines()
    elif args.dataType == "word":
        user_input = file.read().split()
        data.extend(user_input)
    for element in data:
        if element in user_dict:
            user_dict[element] += 1
        else:
            user_dict[element] = 1
    return user_dict


converter = {"long": "numbers", "word": "words", "line": "lines"}
data = []
user_dict = {}
output = ""
if args.inputFile:
    file_read(args.inputFile)
else:
    read()
output += f"Total {converter[args.dataType]}: {len(data)}."
if args.sortingType == "natural":
    if args.dataType == "line":
        output += "\nSorted data: \n" + "\n".join(map(str, sorted(data)))
    else:
        output += "\nSorted data: " + " ".join(map(str, sorted(data)))
elif args.sortingType == "byCount":
    sorted_dict = {key: user_dict[key] for key in sorted(user_dict)}
    sorted_keys = sorted(sorted_dict, key=lambda key: user_dict[key])
    for i in sorted_keys:
        output += f"\n{i}: {sorted_dict[i]} time(s), {math.floor(sorted_dict[i] / len(data) * 100)}%"
else:
    print("unexpected Error")

if args.outputFile:
    file = open(args.outputFile, "w")
    file.write(output)
    file.close()
print(output)

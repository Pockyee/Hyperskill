import argparse  # For parsing command-line arguments
import math  # For mathematical operations like flooring
from os import abort  # Unused import, could be removed


# Custom exception for missing data type
class DataTypeError(Exception):
    def __str__(self):
        return "No data type defined!"


# Custom exception for missing sorting type
class SortingTypeError(Exception):
    def __str__(self):
        return "No sorting type defined!"


# Setting up argument parser for command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-dataType", nargs="?", default="word")  # Data type: 'long', 'word', or 'line'
parser.add_argument("-sortingType", nargs="?", default="natural")  # Sorting type: 'natural' or 'byCount'
parser.add_argument("-inputFile", nargs="?")  # Optional input file
parser.add_argument("-outputFile", nargs="?")  # Optional output file

# Handle argument parsing and exceptions for invalid or missing data/sorting types
try:
    args, unknown = parser.parse_known_args()  # Parse known arguments, ignore unknown ones
    assert len(unknown) == 0  # Ensure there are no unknown arguments
    if args.dataType is None:
        raise DataTypeError  # Raise custom error if no data type
    if args.sortingType is None:
        raise SortingTypeError  # Raise custom error if no sorting type
except DataTypeError as de:
    print(de)
    exit()  # Exit if data type error occurs
except SortingTypeError as se:
    print(se)
    exit()  # Exit if sorting type error occurs
except AssertionError:
    # Print a message for each unknown argument and skip them
    for i in unknown:
        print(f'"{i}" is not a valid parameter. It will be skipped.')


# Function to read input data from the user (stdin)
def read():
    while True:
        try:
            # Handle 'long' data type input (integers only)
            if args.dataType == "long":
                user_input = input().split()  # Split input into individual elements
                for i in user_input:
                    try:
                        value = int(i)  # Convert to integer
                    except ValueError:
                        print(f'"{i}" is not a long. It will be skipped.')  # Handle invalid input
                    else:
                        data.append(value)  # Add valid integers to data list
            
            # Handle 'line' data type input (entire lines)
            if args.dataType == "line":
                user_input = input()  # Read the entire input line
                data.append(user_input)  # Append line to data
            
            # Handle 'word' data type input (split by spaces)
            elif args.dataType == "word":
                user_input = input().split()  # Split input by spaces
                data.extend(user_input)  # Add words to data list
        except EOFError:  # Stop reading on EOF (end of input)
            break
    
    # Count the occurrences of each element in the input
    for element in data:
        if element in user_dict:
            user_dict[element] += 1  # Increment count for existing element
        else:
            user_dict[element] = 1  # Initialize count for new element
    return user_dict


# Function to read input data from a file
def file_read(userfile):
    global data
    file = open(userfile, "r")  # Open the input file for reading
    # Handle 'long' data type input (integers from file)
    if args.dataType == "long":
        user_input = file.read().split()
        for i in user_input:
            try:
                value = int(i)  # Convert to integer
            except ValueError:
                print(f'"{i}" is not a long. It will be skipped.')  # Handle invalid input
            else:
                data.append(value)  # Add valid integers to data list
    
    # Handle 'line' data type input (lines from file)
    if args.dataType == "line":
        data = file.readlines()  # Read all lines from the file
    
    # Handle 'word' data type input (words from file)
    elif args.dataType == "word":
        user_input = file.read().split()  # Split content into words
        data.extend(user_input)  # Add words to data list
    
    # Count occurrences of each element from file input
    for element in data:
        if element in user_dict:
            user_dict[element] += 1  # Increment count for existing element
        else:
            user_dict[element] = 1  # Initialize count for new element
    return user_dict


# Define mapping from input data types to human-readable labels
converter = {"long": "numbers", "word": "words", "line": "lines"}

# Initialize variables
data = []  # Stores the input data
user_dict = {}  # Dictionary to count occurrences of each element
output = ""  # Output string to store results

# If an input file is provided, read data from file; otherwise, read from stdin
if args.inputFile:
    file_read(args.inputFile)
else:
    read()

# Generate output with total count of elements and sorted data
output += f"Total {converter[args.dataType]}: {len(data)}."
if args.sortingType == "natural":  # Natural sorting (alphabetical or numeric)
    if args.dataType == "line":
        output += "\nSorted data: \n" + "\n".join(map(str, sorted(data)))  # Sort lines and join with newline
    else:
        output += "\nSorted data: " + " ".join(map(str, sorted(data)))  # Sort words/numbers and join with space
elif args.sortingType == "byCount":  # Sorting by occurrence count
    sorted_dict = {key: user_dict[key] for key in sorted(user_dict)}  # Sort dictionary by keys
    sorted_keys = sorted(sorted_dict, key=lambda key: user_dict[key])  # Sort by value (count)
    for i in sorted_keys:
        # Add element with count and percentage of total to output
        output += f"\n{i}: {sorted_dict[i]} time(s), {math.floor(sorted_dict[i] / len(data) * 100)}%"
else:
    print("unexpected Error")  # Handle unexpected errors (e.g., invalid sorting type)

# Write output to file if an output file is provided; otherwise, print to stdout
if args.outputFile:
    file = open(args.outputFile, "w")
    file.write(output)  # Write output to the file
    file.close()
print(output)  # Print the final output
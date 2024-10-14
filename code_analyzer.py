import os
import sys
import re
import ast

# Get command-line arguments and set the root directory/file to be checked
args = sys.argv
root = args[1]


# Check if the line exceeds 79 characters (PEP 8 standard)
def s1(issue_list, line, i):
    if len(line) > 79:
        issue_list.append((i, f"Line {i}: S001 Too long"))


# Check if the line's indentation is a multiple of four spaces (PEP 8 standard)
def s2(issue_list, line, i):
    leading_spaces = len(line) - len(line.lstrip())
    if len(line) > 4 and leading_spaces % 4 != 0:
        issue_list.append((i, f"Line {i}: S002 Indentation is not a multiple of four"))


# Check for unnecessary semicolons, ensuring they are not part of a comment or string
def s3(issue_list, line, i):
    semicolon_pos = line.find(";")
    hash_pos = line.find("#")
    if semicolon_pos != -1:
        if line[0:semicolon_pos].count("'") % 2 == 0 and (
            hash_pos == -1 or semicolon_pos < hash_pos
        ):
            issue_list.append((i, f"Line {i}: S003 Unnecessary semicolon"))


# Check for at least two spaces before inline comments
def s4(issue_list, line, i):
    hash_pos = line.find("#")
    if hash_pos > 1 and line[hash_pos - 2 : hash_pos] != "  ":
        issue_list.append(
            (i, f"Line {i}: S004 At least two spaces required before inline comments")
        )


# Check for presence of "TODO" in comments and flag it
def s5(issue_list, line, i):
    todo_pos = line.lower().find("todo")
    if todo_pos != -1 and ("#" in line[0:todo_pos]):
        issue_list.append((i, f"Line {i}: S005 TODO found"))


# Check for more than two consecutive blank lines and reset blank line counter
def s6(issue_list, line, i, blankline):
    if line.strip() == "":
        blankline += 1
    else:
        if blankline > 2:
            issue_list.append(
                (i, f"Line {i}: S006 More than two blank lines used before this line")
            )
        blankline = 0
    return blankline


# Check for too many spaces after 'def' or 'class' keywords
def s7(issue_list, line, i):
    if re.match(".*def  .*", line):
        issue_list.append((i, f"Line {i}: S007 Too many spaces after def"))
    elif re.match(".*class  .*", line):
        issue_list.append((i, f"Line {i}: S007 Too many spaces after class"))


# Check that class names follow CamelCase convention
def s8(issue_list, line, i):
    if re.match("class [a-z].*", line):
        class_name = (
            line[line.find("class") + 6 : line.find(":")]
            if line.find("(") == -1
            else line[line.find("class") + 6 : line.find("(")]
        )
        issue_list.append(
            (
                i,
                f"Line {i}: S008 Class name {class_name} should be written in CamelCase",
            )
        )


# Check that function names follow snake_case convention
def s9(issue_list, line, i):
    if re.match(".*def [A-Z].*", line):
        function_name = line[line.find("def") + 4 : line.find("(")]
        issue_list.append(
            (
                i,
                f"Line {i}: S009 Function name {function_name} should be written in snake_case",
            )
        )


# Check for argument names that are not in snake_case (S010)
# Check for variable names inside functions that are not in snake_case (S011)
# Check for default mutable argument values (S012)
def s10_11_12(issue_list, tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check argument names for snake_case
            for item in node.args.args:
                if re.match("[A-Z].*", item.arg):
                    issue_list.append(
                        (
                            item.lineno,
                            f"Line {item.lineno}: S010 Argument name '{item.arg}' should be snake_case",
                        )
                    )
            # Check variable assignments for snake_case
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            if re.match("[A-Z].*", target.id):
                                issue_list.append(
                                    (
                                        target.lineno,
                                        f"Line {target.lineno}: S011 Argument name '{target.id}' should be snake_case",
                                    )
                                )
            # Check for mutable default arguments (list, dict, set)
            for item in node.args.defaults:
                if (
                    isinstance(item, ast.List)
                    or isinstance(item, ast.Dict)
                    or isinstance(item, ast.Set)
                ):
                    issue_list.append(
                        (
                            item.lineno,
                            f"Line {item.lineno}: S012 Default argument value is mutable",
                        )
                    )


# Main function that checks each line in a file for all style issues
def check(file_path):
    blankline = 0
    issue_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file, start=1):
            # Run individual checks on each line
            s1(issue_list, line, i)
            s2(issue_list, line, i)
            s3(issue_list, line, i)
            s4(issue_list, line, i)
            s5(issue_list, line, i)
            blankline = s6(issue_list, line, i, blankline)
            s7(issue_list, line, i)
            s8(issue_list, line, i)
            s9(issue_list, line, i)
    
    # Parse the entire script to check for function-level issues (S010-S012)
    script = open(file_path).read()
    tree = ast.parse(script)
    s10_11_12(issue_list, tree)

    # Sort issues by line number and print them
    issue_list.sort(key=lambda x: x[0])
    for issue in issue_list:
        print(f"{file_path}: {issue[1]}")


# Collect all .py files from the root directory or a specific file if provided
file_paths = []

# If the root is a Python file, add it to the list; otherwise, search directories
if root.endswith(".py"):
    file_paths.append(root)
else:
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                file_paths.append(file_path)

# Sort file paths alphabetically
file_paths.sort()

# Run style checks on each Python file
for file_path in file_paths:
    check(file_path)
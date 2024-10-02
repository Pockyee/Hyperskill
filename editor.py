def header():
    while True:
        level = input("Level:")
        if 1 <= int(level) <= 6:
            break
        else:
            print("The level should be within the range of 1 to 6")
    return "#" * int(level) + " " + input("Text:") + "\n"


def ordered_list():
    while True:
        rows = input("Number of rows:")
        if int(rows) > 0:
            break
        else:
            print("The number of rows should be greater than zero")
    lst = []
    for i in range(int(rows)):
        lst.append(str(i + 1) + ". " + input(f"Row #{i + 1}:") + "\n")
    return "".join(lst)


def unordered_list():
    while True:
        rows = input("Number of rows:")
        if int(rows) > 0:
            break
        else:
            print("The number of rows should be greater than zero")
    lst = []
    for i in range(int(rows)):
        lst.append("*. " + input(f"Row #{i + 1}:") + "\n")
    return "".join(lst)


formatters = {
    "plain": lambda: input("Text:"),
    "bold": lambda: f"**{input('Text:')}**",
    "italic": lambda: f"*{input('Text:')}*",
    "link": lambda: f"[{input('Label:')}]({input('URL:')})",
    "inline-code": lambda: f"`{input('Text:')}`",
    "new-line": lambda: "\n",
    "header": header,
    "ordered-list": ordered_list,
    "unordered-list": unordered_list
}

form = ""
text = ""

while True:
    form = input("Choose a formatter:")
    if form == "!help":
        print(
            """Available formatters: plain bold italic header link inline-code new-line ordered-list unordered-list\nSpecial commands: !done""")
    elif form in formatters:
        text += formatters[form]()
        print(text)
    elif form == "!done":
        break
    else:
        print("Unknown formatting type or command")




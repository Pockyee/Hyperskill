# Do not change the dictionary, please
countries = {
    "Andorra": {"Catalan", "French", "Portuguese"},
    "Iceland": {"Icelandic", "English", "Scots"},
    "Monaco": {"French", "Italian", "English"},
    "Belgium": {"Dutch", "French", "German"},
}


def check_language(lang):
    selection = []
    for i in countries:
        if lang in countries[i]:
            selection.append(i)
    return selection if selection else "No such country"


language = input()
# Print the result
print(check_language(language))

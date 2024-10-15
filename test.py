import itertools

def letter_case_permutations(s):
    options = [
        [char.lower(), char.upper()] if char.isalpha() else [char] 
        for char in s
    ]
    combinations = itertools.product(*options)
    results = [''.join(combination) for combination in combinations]
    return results


word = "a1b2"
print(letter_case_permutations(word))
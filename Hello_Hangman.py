# Write your code here
import random

print("H A N G M A N")

attempts = 8
word_list = ['python', 'java', 'swift', 'javascript']
result = random.choice(word_list)

hint = '-' * len(result)


while attempts > 0:
    x = input('\n'+hint+'\nInput a letter:')
    if x in result:
        indices = [index for index, letter in enumerate(result) if letter == x]
        for index in indices:
            temp = list (hint)
            temp[index] = x
            hint = ''.join(temp)
    else:
        print("That letter doesn't appear in the word.")
    attempts -= 1
        
print('Thanks for playing!')
# word = input('Guess the word:'+ hint)

# if word == result:
#     print ('You survived!')
# else:
#     print ('You lost!')
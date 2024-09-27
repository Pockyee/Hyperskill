import random

print("H A N G M A N")

won = 0
lost = 0

while True:
    choice = input ('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
    if choice == 'play':
        attempts = 8
        word_list = ['python', 'java', 'swift', 'javascript']
        result = random.choice(word_list)

        hint = '-' * len(result)
        guessed = set()

        while attempts > 0:
            print(f"\n{hint}")
            x = input("Input a letter: ")
            
            if len(x) != 1:
                print('Please, input a single letter.')
                continue
            
            if not x.islower() or not x.isalpha():
                print('Please, enter a lowercase letter from the English alphabet.')
                continue
            
            if x in guessed:
                print("You've already guessed this letter.")
                continue

            guessed.add(x)

            if x in result:
                # Update the hint by replacing dashes with the correct guessed letter
                temp = list(hint)
                for index, letter in enumerate(result):
                    if letter == x:
                        temp[index] = x
                hint = ''.join(temp)
                
                if '-' not in hint:
                    break  # Word is fully guessed
            else:
                print("That letter doesn't appear in the word.")
                attempts -= 1

        if '-' not in hint:
            print(f'You guessed the word {hint}!\nYou survived!')
            won += 1
        else:
            print(f'\nYou lost! The word was: {result}')
            lost += 1
        continue
    elif choice == 'results':
        print (f'You won: {won} times\nYou lost: {lost} times')
        continue
    elif choice == 'exit':
        break
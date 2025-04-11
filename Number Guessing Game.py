# importing random modules
import random


def guessing_game():
    """"Number Guessing Game"""
    while True:
        secret_number = random.randint(1, 100)
        tries = 1  # Reset tries correctly for a new game
        try:
            while True:
                guessing_number = int(input('🤞 Guess the number between 1 and 100 to win the game!: '))
                if guessing_number < 1 or guessing_number > 100:
                    print('Out of range! Your number should be between 1 and 100! 😐')
                    continue
                elif guessing_number == secret_number:
                    print(f'Correct ✅ You Guessed the correct number. Total attempts = {tries} 🎉')
                    break
                elif guessing_number > secret_number:
                    print('Your guess is too high! 😜')
                elif guessing_number < secret_number:
                    print('Your guess is too low! 😛')
                tries += 1

            while True:
                replay = input('😎 Do you want to play the game again? ("Yes"/"No"): ')
                if replay.lower() == 'yes':
                    print('Keep going! 😃')
                    break  # Restart the game
                elif replay.lower() == 'no':
                    print('Well played! Goodbye for now! 😇')
                    return  # Exits the entire function
                else:
                    print('Invalid input! Please enter either "Yes" or "No"...😐')
        except ValueError:
            print('Invalid Input! Enter a number! 🙌')
        except Exception:
            print('Something went wrong! Please try again later. 😢')



# mac = max([])
# print(f'{mac}')

d = 1/3
print(round(d, 2))
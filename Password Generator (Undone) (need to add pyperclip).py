# Password Generator Project
import random
import string



def password_generator():
    """Generates a password according to how the user wants"""
    print('\nThe length of the password should be 8-16 characters')  # Range of 8-16 characters is strong
    while True:
        char_type = []  # Stores all characters of the chosen character type by the user
        password = []  # Stores the password
        try:
            password_length = int(input('\nPlease specify the length of the password you want to generate: '))
            if password_length < 8 or password_length > 16:
                print('\n❌Out of range!Length of password should be between 8 to 16 characters.')
                continue  # Skips the rest of the execution and starts iteration again for a valid input in range.
            else:
                options = {'Lowercase letters (e.g., a-z)': string.ascii_lowercase, 'Uppercase letters (e.g., A-Z)': string.ascii_uppercase,
                           'Numbers (e.g., 0-9)': string.digits, 'Special characters (e.g., @, #, &, etc.)': string.punctuation}
                if input('\nDo you want to exclude similar looking characters? (Yes/No): ').strip().lower() == 'yes':
                    # Since values of the dictionary are in the form of string, we use list comprehension and then convert it to a string.
                    # Creating a new string without the letters a, l (lowercase L) and updating the key "Lowercase letters (e.g., a-z)"
                    # Created lists by removing similar looking characters and converting those lists by join() to string and updating the key values...
                    options['Lowercase letters (e.g., a-z)'] = ''.join([char for char in options['Lowercase letters (e.g., a-z)'] if char not in 'a,l'])
                    options['Uppercase letters (e.g., A-Z)'] = ''.join([char for char in options['Uppercase letters (e.g., A-Z)'] if char not in 'C,O,I,S,Z,B,G'])
                    options['Numbers (e.g., 0-9)'] = ''.join([char for char in options['Numbers (e.g., 0-9)'] if char not in '0,8'])
                total = 0  # Tracks the total number of minimum required characters specified for character types
                print('\n Note: You must type "yes" correctly to include a character type in your password successfully.')
                for option, value in options.items():
                    if input(f'\nDo you want to include {option} in your password? (Yes/No): ').strip().lower() == 'yes':
                        while True:
                            try:
                                min_char = int(input(f'\nSpecify minimum amount of {option} you want to include in your password. (Input 0 if you do not want to specify): '))
                                if min_char < 0:  # If user enters a negative number...
                                    print('\nThe minimum number specified is negative! Please input a positive number')
                                    continue
                                total += min_char
                                char_type.extend(value) # Adds all the characters of that character type to the list individually.
                                for _ in range(min_char):  # Ensures minimum number of characters of each character type included in the password if user specified a number above.
                                    if not password:  # If list is empty
                                        password.append(random.choice(value))
                                    else:
                                        while True:
                                            random_char = random.choice(value)  # Generate a random character from the chosen character type
                                            if password[-1] != random_char:  # Checking last character of the password to avoid consecutive repeated characters
                                                password.append(random_char)
                                                break
                                break
                            except ValueError:  # Handles Value Error
                                print('\nPlease input a valid number')
                            except Exception as e:  # Catching other potential errors
                                print(f'\nError: {e}')
                if total > password_length:  # If total minimum characters specified exceeds length of password
                    print('\n🚩Minimum characters specified exceeds the total length of your password. Please try again!')
                    continue
                if not char_type:
                    print('\nYou must select at least one character type in your password!')
                    continue
                for _ in range(password_length - len(password)):  # Filling rest of the password with random characters from chosen character types by the user.
                    if not password:
                        password.append(random.choice(char_type))
                    else:
                        while True:
                            random_chr = random.choice(char_type)
                            if random_chr != password[-1]:
                                password.extend(random_chr)
                                break
                random.shuffle(password)  # Shuffling the password to improve randomness
                print(f'\nHere is the Generated Password: {"".join(password)}')
                # try:
                    # pyperclip.copy("".join(password)) # Copying to Clipboard
                    # print('\nThe password is successfully copied to your clipboard.')
                # except ModuleNotFoundError:
                   # print('\nUnable to copy the password to your clipboard, Please copy manually!')

            if input('\n Do you want to generate another password? (Yes/No): ').strip().lower() != 'yes':
                break  # exits the function if user does not answer 'yes'
        except ValueError:
            print('\n❌ Invalid input! Please enter a number.')  # Handles Value Error
        except Exception as e:
            print(f'\n❌ Unexpected error: {e}. Please try again.')  # Shows the actual error for debugging.


password_generator()


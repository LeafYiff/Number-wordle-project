"""
Wordle for numbers:
there are n-digit number. Every digit is unique. You need to figure it out.
If you guessed correct digit on correct spot - it's green mark
If you guessed correct digit on incorrect spot - it's yellow mark
If you guessed incorrect digit on correct spot - it's nothing
"""
import random
import json


def language_select() -> str:
    while True:
        language = input('''
            Choose your language: 
            \t\t Press 1 if you speak English
            \t\t Натисніть 2 якщо ви спілкуєтесь Українською
            \t\t Drücken Sie 3, wenn Sie Deutsch sprechen
            \t\t Presiona 4 si hablas Español    
            Input: ''').strip()
        if language in '1234':
            break
        else:
            print('Bad input, try again')
            continue
    return language


def _file_select(language_code):
    match language_code:
        case '1':
            return 'eng1.json'
        case '2':
            return 'ukr2.json'
        case '3':
            return 'spn3.json'
        case '4':
            return 'ger4.json'


def translation_reader(language_code) -> dict:
    fname = _file_select(language_code)
    with open(fname, 'r', encoding="utf-8") as file:
        return json.load(file)


def start(translation):
    print(translation['greeting'])


def generate_num(n_digit: int):
    """
    Generates number for game by given n_digit - number of digits
    """
    digits = '1234567890'
    num: list[str] = random.sample(digits, k=n_digit)  # Generate random number

    if num[0] == '0' and len(num) != 1:  # If first digit is 0, move it to the other position
        new_place = random.sample(range(1, n_digit + 1), k=1)[0]
        num.pop(0)
        num.insert(new_place, '0')

    num: str = ''.join(num)  # list[str] to str
    return num


def check_guess(guess: str, num: str, n_digit: int):
    """
    Checks errors in guesses:
    1) Length must be the same
    2) Every digit in guess must be unique (do not repeat)
    3) Every digit in guess must be a number
    """
    green = 0
    yellow = 0

    if len(guess) != n_digit:  # Error checks
        return None, None, 1
    for i in guess:
        if guess.count(i) > 1:
            return None, None, 2
        if i not in '1234567890':
            return None, None, 3

    for i, v in enumerate(guess):  # Resulting
        if num[i] == v:
            green += 1
        elif v in num:
            yellow += 1

    return green, yellow, None


def output_guess(loop, green, yellow, error=None):
    """
    Printing the result of guess including massages about the errors if there are any
    """
    if error is None:
        print(f'Try {loop}: \n\t green: {green}, yellow: {yellow}')
    elif error == 1:
        print("Don't match the length")
    elif error == 2:
        print('The numbers must be unique! Try with no repeated numbers')
    elif error == 3:
        print('You must use only decimal numbers')
    else:
        print('Some Error occurred')


def end_game(num, loop):
    """
    Print a win massage
    """
    print(f'You have won! The number was {num}. You have used {loop} tries')


def main():
    language_code = language_select()
    translation = translation_reader(language_code)
    start(translation)

    n_digit: int = int(input(translation['input_n']))
    # n_digit: int = random.sample(range(1, 10), k=1)[0]  #  Auto generation

    num = generate_num(n_digit)
    #  print('Number:', num)  # Answer

    guess = None
    loop = 0
    while guess != num:
        guess = input('Guess the number: ').strip()

        green, yellow, error = check_guess(guess, num, n_digit)
        if error is None:
            loop += 1

        output_guess(loop, green, yellow, error)

    end_game(num, loop)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGame aborted')
    except Exception as e:
        print('Some error occurred ', e)

import string
import random


def generate_password():
    two_small_letters = random.choices(string.ascii_lowercase, k=2)
    two_large_letters = random.choices(string.ascii_uppercase, k=2)
    two_numbers = random.choices(string.digits, k=2)
    two_symbols = random.choices(string.punctuation, k=2)

    all_characters = two_numbers + two_symbols + two_large_letters + two_small_letters
    random.shuffle(all_characters)
    joined_characters = "".join(all_characters)

    return joined_characters

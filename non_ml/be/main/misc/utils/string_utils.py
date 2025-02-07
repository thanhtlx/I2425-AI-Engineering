import random
import string


def generate_random_hex_string(length: int = 32) -> str:
    return "".join(random.choices(string.hexdigits, k=length)).lower()


import random

def get_random_byte():
    return random.randint(0, 255)

def get_random_bytes(n):
    return bytes([get_random_byte() for _ in range(n)])
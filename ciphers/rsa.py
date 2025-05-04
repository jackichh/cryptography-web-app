import random
from math import gcd


def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Make sure it's odd and has the right number of bits
        if is_prime(n):
            return n


def is_prime(n, k=128):
    if n <= 3:
        return n > 1
    if n % 2 == 0:
        return False

    # Miller-Rabin primality test
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % phi


def generate_keypair(bits=1024):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for public exponent
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)

    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(message, public_key):
    e, n = public_key
    if isinstance(message, str):
        message = int.from_bytes(message.encode(), 'big')
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = pow(ciphertext, d, n)
    try:
        return plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big').decode()
    except UnicodeDecodeError:
        return plaintext

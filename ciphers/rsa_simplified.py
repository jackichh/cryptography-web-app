import random
from math import gcd

# Step 1: Key Generation

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_keypair():
    """Generate a simple RSA keypair (public and private keys)."""
    p = q = 0

    # Find two primes p and q
    while not is_prime(p):
        p = random.randint(100, 200)  # Pick a random number in a range
    while not is_prime(q) or p == q:
        q = random.randint(100, 200)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Find e such that 1 < e < phi and gcd(e, phi) = 1
    e = 0
    while gcd(e, phi) != 1:
        e = random.randint(2, phi)

    # Find d such that d * e ≡ 1 (mod phi)
    d = 0
    while (d * e) % phi != 1:
        d += 1

    # Return public and private keys
    return (e, n), (d, n)

# Step 2: Encryption
def encrypt(public, plaintext):
    """Encrypt a message using the public key."""
    e, n = public
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

# Step 3: Decryption
def decrypt(private, ciphertext):
    """Decrypt a message using the private key."""
    d, n = private
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return decrypted_message
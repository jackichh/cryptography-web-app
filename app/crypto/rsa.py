import random
import math
from typing import Tuple

def egcd(a, b):
    if a == 0: return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modular_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise Exception('No modular inverse')
    return x % m

def is_prime(n: int) -> bool:
    """Check if a number is prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if the number is prime, False otherwise
    """
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def next_prime(n: int) -> int:
    """Find the next prime number after n.
    
    Args:
        n: Starting number
        
    Returns:
        Next prime number
    """
    if n < 2:
        return 2
    n = n + 1 if n % 2 == 0 else n + 2
    while not is_prime(n):
        n += 2
    return n

def generate_prime(bits: int) -> int:
    """Generate a random prime number with specified bit length.
    
    Args:
        bits: Number of bits for the prime
        
    Returns:
        Random prime number
    """
    min_value = 2**(bits-1)
    max_value = 2**bits - 1
    
    while True:
        n = random.randint(min_value, max_value)
        if is_prime(n):
            return n

def generate_key_pair(bits: int = 8) -> Tuple[int, int, int]:
    """Generate RSA key pair.
    
    Args:
        bits: Number of bits for each prime
        
    Returns:
        Tuple of (n, e, d) where:
        n: Modulus
        e: Public exponent
        d: Private exponent
    """
    # Generate two large prime numbers
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    return rsa_keygen(p, q)

def rsa_keygen(p: int, q: int) -> Tuple[int, int, int]:
    """Generate RSA keys from two primes.
    
    Args:
        p: First prime number
        q: Second prime number
        
    Returns:
        Tuple of (n, e, d) where:
        n: Modulus
        e: Public exponent
        d: Private exponent
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use standard public exponent
    e = 65537
    
    # Calculate private exponent
    d = pow(e, -1, phi)
    
    return n, e, d

def rsa_encrypt(message: str, n: int, e: int) -> str:
    """Encrypt message using RSA.
    
    Args:
        message: Message to encrypt
        n: Modulus
        e: Public exponent
        
    Returns:
        Encrypted message
    """
    # Convert message to numbers
    numbers = [ord(c) for c in message]
    
    # Encrypt each number
    encrypted = [pow(m, e, n) for m in numbers]
    
    # Return as comma-separated string
    return ','.join(map(str, encrypted))

def rsa_decrypt(ciphertext: str, n: int, d: int) -> str:
    """Decrypt message using RSA.
    
    Args:
        ciphertext: Comma-separated encrypted numbers
        n: Modulus
        d: Private exponent
        
    Returns:
        Decrypted message
    """
    # Split ciphertext into numbers
    numbers = [int(x) for x in ciphertext.split(',')]
    
    # Decrypt each number
    decrypted = [pow(c, d, n) for c in numbers]
    
    # Convert numbers back to characters
    return ''.join(chr(m) for m in decrypted)
import random

def egcd(a, b):
    if a == 0: return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modular_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise Exception('No modular inverse')
    return x % m

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

def next_prime(n):
    while not is_prime(n):
        n += 1
    return n

def generate_prime(bits):
    """Generate a random prime number with approximately 'bits' bits."""
    while True:
        # Generate a random number with 'bits' bits
        n = random.getrandbits(bits)
        # Ensure it's odd
        n |= 1
        # Ensure it's not too small
        n |= (1 << (bits - 1))
        if is_prime(n):
            return n

def generate_key_pair(bits=32):
    """Generate a new RSA key pair with primes of approximately 'bits' bits."""
    p = generate_prime(bits)
    q = generate_prime(bits)
    return rsa_keygen(p, q)

def rsa_keygen(p, q):
    if not is_prime(p) or not is_prime(q):
        raise ValueError("Both p and q must be prime numbers")
    
    n = p * q
    phi = (p-1)*(q-1)
    
    # Choose a smaller e for small primes
    if phi < 65537:
        e = 3
    else:
        e = 65537
    
    # Ensure e and phi are coprime
    while egcd(e, phi)[0] != 1:
        e += 2
    
    d = modular_inverse(e, phi)
    return n, e, d

def rsa_encrypt(text, n, e):
    # Split text into chunks that fit within the modulus
    chunk_size = (n.bit_length() - 1) // 8
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Encrypt each chunk
    encrypted_chunks = []
    for chunk in chunks:
        # Convert a chunk to bytes and then to a number
        message = int.from_bytes(chunk.encode('utf-8'), byteorder='big')
        # Encrypt the chunk
        cipher = pow(message, e, n)
        encrypted_chunks.append(str(cipher))
    
    # Join encrypted chunks with a separator
    return '|'.join(encrypted_chunks)

def rsa_decrypt(ciphertext, n, d):
    try:
        # Split the ciphertext into chunks
        chunks = ciphertext.split('|')
        
        # Decrypt each chunk
        decrypted_chunks = []
        for chunk in chunks:
            # Convert chunk to integer
            cipher = int(chunk)
            # Decrypt the chunk
            message = pow(cipher, d, n)
            # Convert back to bytes and then to string
            decrypted_chunk = message.to_bytes((message.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
            decrypted_chunks.append(decrypted_chunk)
        
        # Join decrypted chunks
        return ''.join(decrypted_chunks)
    except ValueError as e:
        raise ValueError("Invalid ciphertext format") from e
import unittest
from app.crypto.rsa import (
    is_prime,
    next_prime,
    generate_prime,
    generate_key_pair,
    rsa_keygen,
    rsa_encrypt,
    rsa_decrypt
)

class TestRSA(unittest.TestCase):
    def test_is_prime(self):
        """Test prime number detection"""
        # Test known primes
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(17))
        self.assertTrue(is_prime(19))
        
        # Test known non-primes
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(15))
        self.assertFalse(is_prime(20))

    def test_next_prime(self):
        """Test finding next prime number"""
        self.assertEqual(next_prime(1), 2)
        self.assertEqual(next_prime(2), 3)
        self.assertEqual(next_prime(15), 17)
        self.assertEqual(next_prime(20), 23)

    def test_generate_prime(self):
        """Test prime number generation"""
        # Test different bit lengths
        for bits in [8, 16, 32]:
            prime = generate_prime(bits)
            self.assertTrue(is_prime(prime))
            self.assertLess(prime, 2**bits)
            self.assertGreater(prime, 2**(bits-1))

    def test_generate_key_pair(self):
        """Test RSA key pair generation"""
        n, e, d = generate_key_pair(bits=8)
        
        # Test key properties
        self.assertIsInstance(n, int)
        self.assertIsInstance(e, int)
        self.assertIsInstance(d, int)
        
        # Test encryption/decryption with generated keys
        message = "Test message"
        encrypted = rsa_encrypt(message, n, e)
        decrypted = rsa_decrypt(encrypted, n, d)
        self.assertEqual(message, decrypted)

    def test_rsa_keygen(self):
        """Test RSA key generation from primes"""
        p, q = 17, 19
        n, e, d = rsa_keygen(p, q)
        
        # Test key properties
        self.assertEqual(n, p * q)
        self.assertEqual(e, 65537)  # Standard public exponent
        
        # Test encryption/decryption
        message = "Test message"
        encrypted = rsa_encrypt(message, n, e)
        decrypted = rsa_decrypt(encrypted, n, d)
        self.assertEqual(message, decrypted)

    def test_rsa_encrypt_decrypt(self):
        """Test RSA encryption and decryption"""
        # Generate keys
        n, e, d = generate_key_pair(bits=8)
        
        # Test different messages
        test_messages = [
            "Hello",
            "Test message",
            "12345",
            "Special chars: !@#$%^&*()"
        ]
        
        for message in test_messages:
            encrypted = rsa_encrypt(message, n, e)
            decrypted = rsa_decrypt(encrypted, n, d)
            self.assertEqual(message, decrypted)

if __name__ == '__main__':
    unittest.main() 
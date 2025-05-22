import unittest
from app.crypto.vigenere import VigenereCipher

class TestVigenereCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        """Test basic encryption and decryption."""
        # Test with simple key
        self.assertEqual(VigenereCipher.encrypt("Hello", "key"), "Rijvs")
        self.assertEqual(VigenereCipher.decrypt("Rijvs", "key"), "Hello")
        
        # Test with key shorter than text
        self.assertEqual(VigenereCipher.encrypt("World", "test"), "Psjew")
        self.assertEqual(VigenereCipher.decrypt("Psjew", "test"), "World")
        
        # Test with mixed case
        self.assertEqual(VigenereCipher.encrypt("HeLLo WoRld", "test"), "AiDEh OhKpv")
        self.assertEqual(VigenereCipher.decrypt("AiDEh OhKpv", "test"), "HeLLo WoRld")

    def test_special_characters(self):
        """Test handling of special characters."""
        text = "Hello, World! 123"
        key = "test"
        encrypted = VigenereCipher.encrypt(text, key)
        self.assertEqual(VigenereCipher.decrypt(encrypted, key), text)
        
        # Test with only special characters
        text = "!@#$%^&*()"
        self.assertEqual(VigenereCipher.encrypt(text, key), text)
        self.assertEqual(VigenereCipher.decrypt(text, key), text)

    def test_empty_key(self):
        """Test handling of empty key."""
        text = "Hello, World!"
        self.assertEqual(VigenereCipher.encrypt(text, ""), text)
        self.assertEqual(VigenereCipher.decrypt(text, ""), text)
        
        # Test with key containing no letters
        self.assertEqual(VigenereCipher.encrypt(text, "!@#"), text)
        self.assertEqual(VigenereCipher.decrypt(text, "!@#"), text)

if __name__ == '__main__':
    unittest.main() 
import unittest
from app.crypto.caesar import CaesarCipher

class TestCaesarCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        """Test basic encryption and decryption."""
        # Test with positive shift
        self.assertEqual(CaesarCipher.encrypt("Hello", 5), "Mjqqt")
        self.assertEqual(CaesarCipher.decrypt("Mjqqt", 5), "Hello")
        
        # Test with shift of 26 (full rotation)
        self.assertEqual(CaesarCipher.encrypt("World", 26), "World")
        self.assertEqual(CaesarCipher.decrypt("World", 26), "World")
        
        # Test with shift of 0 (no shift)
        self.assertEqual(CaesarCipher.encrypt("Python", 0), "Python")
        self.assertEqual(CaesarCipher.decrypt("Python", 0), "Python")
        
        # Test with shift of 7
        self.assertEqual(CaesarCipher.encrypt("Python", 7), "Wfaovu")
        self.assertEqual(CaesarCipher.decrypt("Wfaovu", 7), "Python")

    def test_special_characters(self):
        """Test handling of special characters."""
        text = "Hello, World! 123"
        shift = 5
        
        # Special characters should remain unchanged
        encrypted = CaesarCipher.encrypt(text, shift)
        self.assertEqual(encrypted, "Mjqqt, Btwqi! 123")
        
        decrypted = CaesarCipher.decrypt(encrypted, shift)
        self.assertEqual(decrypted, text)

    def test_case_preservation(self):
        """Test case preservation in encryption/decryption."""
        text = "HeLLo WoRld"
        shift = 5
        
        encrypted = CaesarCipher.encrypt(text, shift)
        self.assertEqual(encrypted, "MjQQt BtWqi")
        
        decrypted = CaesarCipher.decrypt(encrypted, shift)
        self.assertEqual(decrypted, text)

    def test_negative_shift(self):
        """Test encryption/decryption with negative shift."""
        text = "Hello"
        shift = -3
        
        encrypted = CaesarCipher.encrypt(text, shift)
        self.assertEqual(encrypted, "Ebiil")
        
        decrypted = CaesarCipher.decrypt(encrypted, shift)
        self.assertEqual(decrypted, text)

    def test_large_shift(self):
        """Test encryption/decryption with large shift values."""
        text = "Hello"
        shift = 100  # Should wrap around
        
        encrypted = CaesarCipher.encrypt(text, shift)
        self.assertEqual(encrypted, "Dahhk")
        
        decrypted = CaesarCipher.decrypt(encrypted, shift)
        self.assertEqual(decrypted, text)

if __name__ == '__main__':
    unittest.main() 
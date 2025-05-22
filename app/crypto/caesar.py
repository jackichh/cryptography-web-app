class CaesarCipher:
    @staticmethod
    def encrypt(text: str, shift: int) -> str:
        """Encrypt text using Caesar cipher.
        
        Args:
            text: Text to encrypt
            shift: Number of positions to shift
            
        Returns:
            Encrypted text
        """
        result = []
        shift = shift % 26  # Normalize shift to 0-25 range
        
        for char in text:
            if char.isalpha():
                # Determine if character is uppercase
                is_upper = char.isupper()
                char = char.lower()
                
                # Apply shift
                char_value = ord(char) - ord('a')
                encrypted_value = (char_value + shift) % 26
                encrypted_char = chr(encrypted_value + ord('a'))
                
                # Restore case
                if is_upper:
                    encrypted_char = encrypted_char.upper()
                    
                result.append(encrypted_char)
            else:
                result.append(char)
                
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, shift: int) -> str:
        """Decrypt text using Caesar cipher.
        
        Args:
            text: Text to decrypt
            shift: Number of positions to shift
            
        Returns:
            Decrypted text
        """
        return CaesarCipher.encrypt(text, -shift)
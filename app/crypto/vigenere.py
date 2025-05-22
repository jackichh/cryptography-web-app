class VigenereCipher:
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """Encrypt text using Vigenère cipher.
        
        Args:
            text: Text to encrypt
            key: Encryption key
            
        Returns:
            Encrypted text
        """
        if not key:
            return text
            
        # Filter key to only include letters and convert to lowercase
        key = ''.join(c.lower() for c in key if c.isalpha())
        if not key:
            return text
            
        result = []
        key_length = len(key)
        
        for i, char in enumerate(text):
            if char.isalpha():
                # Get the key character for this position
                key_char = key[i % key_length]
                key_shift = ord(key_char) - ord('a')
                
                # Determine if character is uppercase
                is_upper = char.isupper()
                char = char.lower()
                
                # Apply shift
                char_value = ord(char) - ord('a')
                encrypted_value = (char_value + key_shift) % 26
                encrypted_char = chr(encrypted_value + ord('a'))
                
                # Restore case
                if is_upper:
                    encrypted_char = encrypted_char.upper()
                    
                result.append(encrypted_char)
            else:
                result.append(char)
                
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """Decrypt text using Vigenère cipher.
        
        Args:
            text: Text to decrypt
            key: Decryption key
            
        Returns:
            Decrypted text
        """
        if not key:
            return text
            
        # Filter key to only include letters and convert to lowercase
        key = ''.join(c.lower() for c in key if c.isalpha())
        if not key:
            return text
            
        result = []
        key_length = len(key)
        
        for i, char in enumerate(text):
            if char.isalpha():
                # Get the key character for this position
                key_char = key[i % key_length]
                key_shift = ord(key_char) - ord('a')
                
                # Determine if character is uppercase
                is_upper = char.isupper()
                char = char.lower()
                
                # Apply shift
                char_value = ord(char) - ord('a')
                decrypted_value = (char_value - key_shift) % 26
                decrypted_char = chr(decrypted_value + ord('a'))
                
                # Restore case
                if is_upper:
                    decrypted_char = decrypted_char.upper()
                    
                result.append(decrypted_char)
            else:
                result.append(char)
                
        return ''.join(result)
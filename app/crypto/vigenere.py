class VigenereCipher:
    @staticmethod
    def encrypt(text, key):
        result = ""
        key_length = len(key)
        key_as_int = [ord(i.lower()) - ord('a') for i in key]
        for i, char in enumerate(text):
            if char.isalpha():
                # Determine if character is uppercase or lowercase
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Convert character to 0-25 range
                char_value = ord(char) - ascii_offset
                # Apply Vigenere encryption
                encrypted_value = (char_value + key_as_int[i % key_length]) % 26
                # Convert back to ASCII and add to result
                result += chr(encrypted_value + ascii_offset)
            else:
                result += char
        return result

    @staticmethod
    def decrypt(text, key):
        result = ""
        key_length = len(key)
        key_as_int = [ord(i.lower()) - ord('a') for i in key]
        for i, char in enumerate(text):
            if char.isalpha():
                # Determine if character is uppercase or lowercase
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Convert character to 0-25 range
                char_value = ord(char) - ascii_offset
                # Apply Vigenere decryption
                decrypted_value = (char_value - key_as_int[i % key_length]) % 26
                # Convert back to ASCII and add to result
                result += chr(decrypted_value + ascii_offset)
            else:
                result += char
        return result
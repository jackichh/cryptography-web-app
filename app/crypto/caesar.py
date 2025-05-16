class CaesarCipher:
    @staticmethod
    def encrypt(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('a') if char.islower() else ord('A')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    @staticmethod
    def decrypt(text, shift):
        return CaesarCipher.encrypt(text, 26 - shift)
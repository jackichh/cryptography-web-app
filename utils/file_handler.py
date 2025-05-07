def save_text(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def save_binary(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def load_binary(filename):
    with open(filename, 'rb') as f:
        return f.read()
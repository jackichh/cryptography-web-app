from wsgi_framework.core import App
from wsgiref.simple_server import make_server

app = App()


@app.route("/encrypt", methods=["POST"])
def encrypt_handler(data):
    algorithm = data.get("algorithm")
    text = data.get("text", "")
    key = data.get("key")

    if algorithm == "caesar":
        shift = int(key)
        encrypted = ''.join(chr((ord(char) - 65 + shift) % 26 + 65) if char.isupper() else char for char in text)
    else:
        raise ValueError("Unsupported algorithm")

    return {"encrypted": encrypted}


@app.route("/")
def index(_):
    return {"message": "Cryptography WSGI App Framework"}

if __name__ == '__main__':
    with make_server('', 8080, app) as httpd:
        print("Serving on port 8080..."
              "\nhttp://localhost:8080/")
        httpd.serve_forever()
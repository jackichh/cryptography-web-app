import os
from wsgi_framework.core import WSGIApp

from ciphers import caesar, vigenere, rsa
from utils import file_handler

app = WSGIApp()

def render_template(filename):
    with open(os.path.join('templates', filename), encoding='utf-8') as f:
        return f.read()

@app.route('/', methods=['GET'])
def index(request):
    return {
        'body': render_template('index.html').encode('utf-8')
    }

@app.route('/static/script.js', methods=['GET'])
def static_js(request):
    with open('static/script.js', 'rb') as f:
        return {
            'headers': [('Content-type', 'application/javascript')],
            'body': f.read()
        }

@app.route('/process', methods=['POST'])
def process(request):
    form = request.form()
    text = form.get('text', [''])[0]
    algorithm = form.get('algorithm', [''])[0]
    mode = form.get('mode', ['encrypt'])[0]
    result = ''
    try:
        if algorithm == 'caesar':
            shift = int(form.get('caesar_key', [3])[0])
            if mode == 'encrypt':
                result = caesar.encrypt(text, shift)
            else:
                result = caesar.decrypt(text, shift)
        elif algorithm == 'vigenere':
            key = form.get('vigenere_key', [''])[0]
            if mode == 'encrypt':
                result = vigenere.encrypt_vigenere(text, key)
            else:
                result = vigenere.decrypt_vigenere(text, key)
        elif algorithm == 'rsa':
            p = int(form.get('rsa_p', [0])[0])
            q = int(form.get('rsa_q', [0])[0])
            if mode == 'encrypt':
                pub, priv = rsa.generate_keypair(p, q)
                cipher = rsa.encrypt(pub, text)
                result = f"Cipher: {cipher}\nPublic key: {pub}\nPrivate key: {priv}"
            else:
                # Для дешифрування треба отримати ключі та cipher з форми (додай на фронті)
                result = "Дешифрування RSA реалізуй аналогічно (додай поля для ключа і cipher)"
        else:
            result = "Невідомий алгоритм"
    except Exception as e:
        result = f"Помилка: {e}"
    return {
        'headers': [('Content-type', 'text/plain; charset=utf-8')],
        'body': result.encode('utf-8')
    }

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("Serving on http://localhost:8000 ...")
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
import os
import urllib.parse
from wsgiref.util import setup_testing_defaults
from app.crypto.caesar import CaesarCipher
from app.crypto.vigenere import VigenereCipher
from app.crypto.rsa import *
from app.utils.form_parser import parse_form
from app.templates import templates
from datetime import datetime

# Define uploads directory path
UPLOADS_DIR = os.path.join('app', 'uploads')

def application(environ, start_response):
    setup_testing_defaults(environ)
    path = environ.get('PATH_INFO', '/')
    method = environ['REQUEST_METHOD']

    if path == '/' and method == 'GET':
        response_body = templates.home_page()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    elif path == '/generate_rsa_key' and method == 'POST':
        form = parse_form(environ)
        algo = form.get('algo', 'rsa')
        text = form.get('text', '')
        
        try:
            # Generate a new RSA key pair
            n, e, d = generate_key_pair(bits=32)
            key = f"{n},{e},{d}"
            
            # Return to the same page with the generated key
            response_body = templates.home_page(key=key)
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]
        except Exception as e:
            response_body = templates.home_page(error=str(e))
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]

    elif path == '/encrypt' and method == 'POST':
        form = parse_form(environ)
        algo = form.get('algo', 'caesar')
        text = form.get('text', '').strip()
        key = form.get('key', '').strip()
        action = form.get('action', 'Encrypt')
        
        # Check for empty inputs and return to the home page
        if not text or not key:
            error_msg = "Please enter both text and key"
            response_body = templates.home_page(error=error_msg)
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]

        try:
            if algo == 'caesar':
                shift = int(key) if key else 0
                result = CaesarCipher.encrypt(text, shift) if action == 'Encrypt' else CaesarCipher.decrypt(text, shift)
            elif algo == 'vigenere':
                result = VigenereCipher.encrypt(text, key) if action == 'Encrypt' else VigenereCipher.decrypt(text, key)
            elif algo == 'rsa':
                parts = [int(x.strip()) for x in key.split(',') if x.strip().isdigit()]
                if len(parts) == 2:
                    p, q = parts
                    n, e, d = rsa_keygen(next_prime(p), next_prime(q))
                    if action == 'Encrypt':
                        result = rsa_encrypt(text, n, e)
                        key = f"{n},{e},{d}"
                    else:
                        result = "For decryption, provide n,e,d"
                elif len(parts) == 3:
                    n, e, d = parts
                    if action == 'Encrypt':
                        result = rsa_encrypt(text, n, e)
                    else:
                        result = rsa_decrypt(text, n, d)
                else:
                    result = "Invalid key for RSA. Use p,q for keygen, or n,e,d."
            else:
                result = "Unknown algorithm"
        except Exception as e:
            result = f"Error: {e}"

        response_body = templates.result_page(algo, action, text, key, result)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    elif path == '/save_result' and method == 'GET':
        params = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
        algo = params.get('algo', [''])[0]
        action = params.get('action', [''])[0]
        text = params.get('text', [''])[0]
        key = params.get('key', [''])[0]
        
        # Create a filename based on timestamp and algorithm
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{algo}_{action}_{timestamp}.txt"
        
        # Save the file with metadata
        filepath = os.path.join(UPLOADS_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(f"Algorithm: {algo}\n")
            f.write(f"Action: {action}\n")
            f.write(f"Key: {key}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\nContent:\n")
            f.write(text)
        
        # Redirect back to home page
        start_response('303 See Other', [('Location', '/')])
        return [b'']

    elif path == '/share' and method == 'GET':
        params = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
        algo = params.get('algo', ['caesar'])[0]
        text = params.get('text', [''])[0]
        key = params.get('key', [''])[0]
        
        response_body = templates.share_page(algo, text, key)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    elif path == '/upload' and method == 'POST':
        form = parse_form(environ)
        fileinfo = form.get('file')
        if isinstance(fileinfo, dict) and 'filename' in fileinfo:
            filename = fileinfo['filename']
            file_content = fileinfo['content']
            
            # Save the file
            filepath = os.path.join(UPLOADS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(file_content)
            
            # Redirect back to home page
            start_response('303 See Other', [('Location', '/')])
            return [b'']
        else:
            response_body = templates.html_page("No file was uploaded.")
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]

    elif path == '/download_file' and method == 'GET':
        params = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
        filename = params.get('file', [''])[0]
        if not filename:
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b'No filename specified']
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        if not os.path.exists(filepath):
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'File not found']
        
        with open(filepath, 'rb') as f:
            content = f.read()
        
        headers = [
            ('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
        ]
        start_response('200 OK', headers)
        return [content]

    elif path == '/delete_file' and method == 'GET':
        params = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
        filename = params.get('file', [''])[0]
        if not filename:
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b'No filename specified']
        
        filepath = os.path.join(UPLOADS_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Redirect back to home page
        start_response('303 See Other', [('Location', '/')])
        return [b'']

    elif path == '/download' and method == 'GET':
        params = urllib.parse.parse_qs(environ.get('QUERY_STRING', ''))
        text = params.get('text', [''])[0]
        binary = params.get('binary', [None])[0]
        filename = 'cipher.bin' if binary else 'cipher.txt'
        if binary:
            content = text.encode('utf-8')
            headers = [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ]
        else:
            content = text.encode('utf-8')
            headers = [
                ('Content-Type', 'text/plain'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ]
        start_response('200 OK', headers)
        return [content]

    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']
import urllib.parse
import os
from datetime import datetime


def html_page(body, title="Data Encryption System"):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
    body {{ font-family: Arial, sans-serif; margin: 2em; }}
    input[type=text], textarea {{ width: 100%; }}
    .button-group {{ margin: 1em 0; }}
    .button-group a, .button-group input[type=submit] {{ 
        margin-right: 1em;
        padding: 0.5em 1em;
        text-decoration: none;
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }}
    .button-group a:hover, .button-group input[type=submit]:hover {{
        background: #45a049;
    }}
    .key-info {{
        background: #f5f5f5;
        padding: 1em;
        margin: 1em 0;
        border-radius: 4px;
    }}
    .file-list {{
        margin: 2em 0;
        border: 1px solid #ddd;
        border-radius: 4px;
    }}
    .file-list table {{
        width: 100%;
        border-collapse: collapse;
    }}
    .file-list th, .file-list td {{
        padding: 0.75em;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }}
    .file-list th {{
        background-color: #f5f5f5;
    }}
    .file-list tr:hover {{
        background-color: #f9f9f9;
    }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {body}
    <hr>
    <p><a href="/">Back to home</a></p>
</body>
</html>"""


def home_page(error=None, key=None):
    file_list = get_file_list()
    error_html = f'<div style="color: red; margin: 1em 0;">{error}</div>' if error else ''
    key_html = f'<div class="key-info"><p><strong>Generated Key:</strong> {key}</p></div>' if key else ''
    return html_page(f"""
    {error_html}
    <form method="POST" action="/encrypt">
        <h2>Encrypt / Decrypt</h2>
        <label>Algorithm:</label>
        <select name="algo" id="algo">
            <option value="caesar">Caesar</option>
            <option value="vigenere">Vigenère</option>
            <option value="rsa">RSA</option>
        </select>
        <br><br>
        <label>Text:</label><br>
        <textarea name="text" id="text-input" rows="5"></textarea><br><br>
        <div id="key-section">
            <label>Key (for Caesar: shift integer, for Vigenère: string, for RSA: p,q as primes):</label><br>
            <input type="text" name="key" id="key-input" value="{key if key else ''}">
            <div id="rsa-key-gen">
                <br>
                <button type="submit" formaction="/generate_rsa_key" formnovalidate>Generate New RSA Key</button>
            </div>
            {key_html}
        </div>
        <br><br>
        <input type="submit" name="action" value="Encrypt">
        <input type="submit" name="action" value="Decrypt">
    </form>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <h2>Upload Files</h2>
        <label>Select File:</label>
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <div class="file-list">
        <h2>Uploaded Files</h2>
        <table>
            <tr>
                <th>Filename</th>
                <th>Size</th>
                <th>Upload Date</th>
                <th>Actions</th>
            </tr>
            {file_list}
        </table>
    </div>
    """)


def format_file_size(size):
    """Format file size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def get_file_list():
    """Generate HTML for the file list table."""
    try:
        files = []
        uploads_dir = os.path.join('app', 'uploads')
        for filename in os.listdir(uploads_dir):
            filepath = os.path.join(uploads_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                size = format_file_size(stat.st_size)
                date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                files.append(f"""
                    <tr>
                        <td>{filename}</td>
                        <td>{size}</td>
                        <td>{date}</td>
                        <td>
                            <a href="/download_file?file={urllib.parse.quote_plus(filename)}">Download</a>
                            <a href="/delete_file?file={urllib.parse.quote_plus(filename)}" onclick="return confirm('Are you sure you want to delete this file?')">Delete</a>
                        </td>
                    </tr>
                """)
        return '\n'.join(files) if files else '<tr><td colspan="4">No files uploaded yet</td></tr>'
    except Exception as e:
        return f'<tr><td colspan="4">Error loading files: {str(e)}</td></tr>'


def result_page(algo, action, input_text, key, result_text):
    download_link = f"/download?text={urllib.parse.quote_plus(result_text)}"
    save_link = f"/save_result?algo={algo}&action={action}&text={urllib.parse.quote_plus(result_text)}&key={urllib.parse.quote_plus(key)}"

    return html_page(f"""
    <h2>Result ({algo.title()} {action})</h2>
    <div>
        <h3>Input Text</h3>
        <textarea rows="5" readonly>{input_text}</textarea>

        <h3>Key</h3>
        <input type="text" value="{key}" readonly>

        <h3>Output</h3>
        <textarea rows="5" readonly>{result_text}</textarea>

        <div>
            <a href="{download_link}">Download as Text</a>
            <a href="{download_link}&binary=1">Download as Binary</a>
            <a href="{save_link}">Save to Server</a>
        </div>
    </div>
    """)


def upload_result_page(filename, content):
    return html_page(f"""
    <h2>Uploaded File: {filename}</h2>
    <textarea rows="10" readonly>{content}</textarea>
    """)


def share_page(algo, text, key):
    return html_page(f"""
    <h2>Share {algo.title()} Ciphertext</h2>
    <form method="POST" action="/encrypt">
        <input type="hidden" name="algo" value="{algo}">
        <label>Text:</label><br>
        <textarea name="text" rows="5">{text}</textarea><br><br>
        <label>Key:</label><br>
        <input type="text" name="key" value="{key}"><br><br>
        <div class="button-group">
            <input type="submit" name="action" value="Encrypt">
            <input type="submit" name="action" value="Decrypt">
        </div>
    </form>
    """)
# Data Encryption System

A simple web application that provides encryption and decryption functionality using different algorithms.

## Features

- Multiple encryption algorithms:
  - Caesar Cipher
  - Vigenère Cipher
  - RSA Encryption
- File upload and management
- Download encrypted/decrypted content
- Save results to server

## Project Structure

```
app/
├── crypto/           # Encryption algorithms
│   ├── caesar.py
│   ├── vigenere.py
│   └── rsa.py
├── templates/        # HTML templates
│   └── templates.py
├── utils/           # Utility functions
│   └── form_parser.py
├── uploads/         # Uploaded files storage
└── routes.py        # Main application routes
app.py        # Main application
```

## Requirements

- Python 3.x
- No external dependencies required

## Running the Application

1. Make sure you're in the project directory
2. Run the application:
   ```bash
   python main.py
   ```
3. Open your browser and go to: http://localhost:8000

## Usage

1. Select an encryption algorithm
2. Enter your text
3. Provide the key:
   - Caesar: integer shift value
   - Vigenère: string key
   - RSA: prime numbers p,q or full key n,e,d
4. Click Encrypt or Decrypt
5. Download or save the result

## File Management

- Upload files through the web interface
- Download files using the download button
- Delete files using the delete button
- All files are stored in the `app/uploads` directory 
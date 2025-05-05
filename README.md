**Data Encryption Web Application**

---

## 🔐 Data Encryption Web Application

A Python-based web application that provides encryption and decryption services using classical and modern cryptographic algorithms. The application allows users to encrypt messages, decrypt them, and exchange encrypted data securely via a web interface.

---

## 📌 Features

- **Supports Multiple Encryption Algorithms:**
  - Caesar Cipher
  - Vigenère Cipher
  - RSA Encryption (with key generation)

- **User Interface:**
  - Input plaintext messages
  - Select encryption algorithm and keys
  - View and copy encrypted/decrypted messages
  - Download results as:
    - Plain text files (`.txt`)
    - Binary files (`.bin`)

- **Client Communication:**
  - Secure exchange of ciphertexts and keys between users
  - Basic message sharing functionality (optional via local storage or API)

---

## 🛠 Technologies Used

- Python 3
- WSGI / Flask (or custom WSGI framework)
- HTML5, CSS3, JavaScript (for frontend)
- RSA key generation with `cryptography` or `PyCrypto` module

---

## 📂 Project Structure

```

coming soon!

````

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/encryption-web-app.git
cd encryption-web-app
````

### 2. Create a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

coming soon!

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🔐 Algorithm Descriptions

### Caesar Cipher

* Shifts letters by a fixed number of positions in the alphabet.
* Key: integer value (e.g., `3` for shifting `A → D`).

### Vigenère Cipher

* Uses a keyword to perform polyalphabetic substitution.
* Key: alphabetic string (e.g., `"KEY"`).

### RSA Encryption

* Public-key cryptography using a pair of keys.
* Key exchange is part of the application logic.
* Keys are generated per session or stored in memory.

---

## 📁 Output Formats

* **Text (`.txt`)**: Plaintext or ciphertext stored as readable text.
* **Binary (`.bin`)**: Encrypted data stored in binary format, for safe transport.

---

## 📬 Client Communication (Optional)

Clients can exchange:

* Encrypted messages (ciphertext)
* RSA public keys

This can be extended with REST APIs or WebSocket support.

---

## 🧪 Future Improvements

* User authentication and key management
* WebSocket-based real-time message exchange
* End-to-end encrypted chat functionality
* Client-side encryption for added security

---

## 👨‍💻 Author

**Your Name** – ___

GitHub: [github.com/jackichh](https://github.com/jackichh)


# app.py

from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

app = Flask(__name__)

def derive_key(password, salt):
    """Derive a key from the provided password using PBKDF2.

    Args:
        password (str): The password to derive the key from.
        salt (bytes): The salt used in the key derivation process.

    Returns:
        bytes: The derived key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

@app.route('/')
def index():
    """Render the index page."""
    return render_template('layout.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypt the provided data using AES algorithm and return the result in URL-safe base64 format.

    Raises:
        ValueError: If data or key is missing in the request.

    Returns:
        jsonify: A JSON object containing the result or an error message.
    """
    try:
        # Get data and key from the request
        data = request.form.get('data')
        key = request.form.get('key')

        # Input validation
        if not data or not key:
            raise ValueError("Data and key are required.")

        # Derive a key from the provided password using PBKDF2
        key = derive_key(key, b'nithins')

        # Create an AES cipher with ECB mode
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the data to be a multiple of the block size
        while len(data) % 16 != 0:
            data += ' '

        # Encrypt the data and encode it in URL-safe base64 format
        ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
        encrypted_data = base64.urlsafe_b64encode(ciphertext).decode('utf-8')

        # Return the encrypted data
        return jsonify({'result': encrypted_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypt the provided encrypted data using AES algorithm and return the result.

    Raises:
        ValueError: If encrypted data or key is missing in the request.

    Returns:
        jsonify: A JSON object containing the result or an error message.
    """
    try:
        # Get encrypted data and key from the request
        data = request.form.get('encrypted_data')
        key = request.form.get('key')

        # Input validation
        if not data or not key:
            raise ValueError("Encrypted data and key are required.")

        # Derive a key from the provided password using PBKDF2
        key = derive_key(key, b'nithins')

        # Create an AES cipher with ECB mode
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decode the URL-safe base64 encoded encrypted data
        ciphertext = base64.urlsafe_b64decode(data)

        # Decrypt the data and remove padding
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Return the decrypted data
        return jsonify({'result': decrypted_data.rstrip(b' ').decode('utf-8')})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)

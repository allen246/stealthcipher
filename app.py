from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/health_check', methods=['GET'])
def health_check():
    response_data = {'message': 'API is working fine'}
    print(str(response_data))
    return jsonify(response_data)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.form['data']
    key = request.form['key']

    key = derive_key(key, b'nithins')
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    while len(data) % 16 != 0:
        data += ' '

    ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    encrypted_data = base64.urlsafe_b64encode(ciphertext).decode('utf-8')
    return jsonify({'result': encrypted_data})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_data = request.form['encrypted_data']
    key = request.form['key']

    key = derive_key(key, b'nithins')
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    ciphertext = base64.urlsafe_b64decode(encrypted_data)
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    return jsonify({'result': decrypted_data.rstrip(b' ').decode('utf-8')})

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

if __name__ == '__main__':
    app.run(debug=True)
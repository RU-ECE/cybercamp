from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_message(public_key, message):
    # Generate an ephemeral key pair
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
    ephemeral_public_key = ephemeral_private_key.public_key()

    # Perform key exchange
    shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)

    # Derive a key using HKDF
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # Generate a random IV
    iv = os.urandom(16)

    # Encrypt the message
    encryptor = Cipher(algorithms.AES(derived_key), modes.CFB(iv)).encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    return ephemeral_public_key, iv, ciphertext

def decrypt_message(private_key, ephemeral_public_key, iv, ciphertext):
    # Perform key exchange
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)

    # Derive the key using HKDF
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # Decrypt the message
    decryptor = Cipher(algorithms.AES(derived_key), modes.CFB(iv)).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode()

# Load the keys
with open("ecc_private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("ecc_public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Example usage
message = "Hello, ECC!"
ephemeral_public_key, iv, ciphertext = encrypt_message(public_key, message)
decrypted_message = decrypt_message(private_key, ephemeral_public_key, iv, ciphertext)

print(f"Original message: {message}")
print(f"Decrypted message: {decrypted_message}")
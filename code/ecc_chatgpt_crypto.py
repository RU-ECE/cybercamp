import sys
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def load_key(filename, private=False):
    with open(filename, "rb") as key_file:
        if private:
            return serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        else:
            return serialization.load_pem_public_key(
                key_file.read()
            )

def encrypt_message(public_key, message):
    # Generate a symmetric key for encryption
    symmetric_key = os.urandom(32)  # AES-256 key

    # Encrypt the message with the symmetric key
    aesgcm = AESGCM(symmetric_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

    # Generate an ephemeral private key for ECDH
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())

    # Derive the shared key using the ephemeral private key and the recipient's public key
    shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_key)

    # Encrypt the symmetric key with the derived key
    aesgcm = AESGCM(derived_key)
    encrypted_key = aesgcm.encrypt(nonce, symmetric_key, None)

    # Serialize the ephemeral public key to be sent along with the ciphertext
    ephemeral_public_key = ephemeral_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return ephemeral_public_key, encrypted_key, nonce, ciphertext

def decrypt_message(private_key, ephemeral_public_key_bytes, encrypted_key, nonce, ciphertext):
    # Load the ephemeral public key from bytes
    ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_key_bytes)

    # Derive the shared key using the recipient's private key and the ephemeral public key
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_key)

    # Decrypt the symmetric key with the derived key
    aesgcm = AESGCM(derived_key)
    symmetric_key = aesgcm.decrypt(nonce, encrypted_key, None)

    # Decrypt the message with the symmetric key
    aesgcm = AESGCM(symmetric_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ecc_chatgpt_crypto.py ecc_public_key.pem ecc_private_key.pem msg1.txt")
        sys.exit(1)

    public_key_file = sys.argv[1]
    private_key_file = sys.argv[2]
    message_file = sys.argv[3]

    with open(message_file, "r") as file:
        original_message = file.read()

    public_key = load_key(public_key_file, private=False)
    private_key = load_key(private_key_file, private=True)

    ephemeral_public_key, encrypted_key, nonce, ciphertext = encrypt_message(public_key, original_message)
    decrypted_message = decrypt_message(private_key, ephemeral_public_key, encrypted_key, nonce, ciphertext)

    if original_message == decrypted_message:
        print("Success: The decrypted message matches the original message.")
    else:
        print("Error: The decrypted message does not match the original message.")

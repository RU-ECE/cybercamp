from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_key_pair(public_key_file: str, private_key_file: str, key_size: int = 2048):
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Standard public exponent
        key_size=key_size,  # Key size in bits
    )
    
    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  # No password encryption
    )
    
    # Save private key to a file
    with open(private_key_file, 'wb') as private_file:
        private_file.write(private_pem)
    
    # Generate public key from private key
    public_key = private_key.public_key()
    
    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save public key to a file
    with open(public_key_file, 'wb') as public_file:
        public_file.write(public_pem)
    
    print(f'RSA key pair generated and saved to {private_key_file} and {public_key_file}')

if __name__ == '__main__':
    generate_rsa_key_pair('public_key.pem', 'private_key.pem')

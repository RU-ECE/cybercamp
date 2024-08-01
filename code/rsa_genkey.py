import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_rsa_key_pair(passphrase=None):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    encryption_algorithm = serialization.NoEncryption()
    if passphrase:
        encryption_algorithm = serialization.BestAvailableEncryption(passphrase.encode())

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_rsa.py filename [password]")
        return
    
    filename = sys.argv[1]
    passphrase = sys.argv[2] if len(sys.argv) > 2 else None

    private_pem, public_pem = generate_rsa_key_pair(passphrase)

    with open(f"{filename}_private.pem", "wb") as private_file:
        private_file.write(private_pem)
    
    with open(f"{filename}_public.pem", "wb") as public_file:
        public_file.write(public_pem)

    print(f"RSA key pair generated and saved to {filename}_private.pem and {filename}_public.pem")

if __name__ == "__main__":
    main()

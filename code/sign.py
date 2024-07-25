import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def sign_file(private_key_path, file_path):
    # Load the private key
    with open(private_key_path, "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None
        )

    # Read the contents of the file to be signed
    with open(file_path, "rb") as file:
        data = file.read()

    # Create the signature
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Write the signature to a new file
    output_path = file_path.rsplit('.', 1)[0] + "_signed.txt"
    with open(output_path, "wb") as signed_file:
        signed_file.write(signature)

    print(f"Signature saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sign.py <private_key_file> <file_to_sign>")
        sys.exit(1)

    private_key_file = sys.argv[1]
    file_to_sign = sys.argv[2]

    sign_file(private_key_file, file_to_sign)
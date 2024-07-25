import sys
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def verify_signature(public_key_path, signed_file_path):
    # Load the public key
    with open(public_key_path, "rb") as key_file:
        public_key = load_pem_public_key(key_file.read())

    # Read the signature
    with open(signed_file_path, "rb") as signed_file:
        signature = signed_file.read()

    # Read the original file (assuming it has the same name without "_signed.txt")
    original_file_path = signed_file_path.replace("_signed.txt", ".txt")
    with open(original_file_path, "rb") as file:
        data = file.read()

    # Verify the signature
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("The signature is valid. The file was signed by the matching private key.")
    except InvalidSignature:
        print("The signature is invalid. The file was not signed by the matching private key.")
    except Exception as e:
        print(f"An error occurred during verification: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python signature_verify.py <public_key_file> <signed_file>")
        sys.exit(1)

    public_key_file = sys.argv[1]
    signed_file = sys.argv[2]

    verify_signature(public_key_file, signed_file)
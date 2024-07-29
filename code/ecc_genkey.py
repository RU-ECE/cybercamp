from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

# Generate a new ECC key pair
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Serialize the private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize the public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the keys to files
with open("ecc_private_key.pem", "wb") as f:
    f.write(private_pem)

with open("ecc_public_key.pem", "wb") as f:
    f.write(public_pem)

print("ECC key pair generated and saved in PEM format.")
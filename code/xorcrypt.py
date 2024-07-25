import sys

def xor_encrypt(key, filename):
    try:
        with open(filename, 'rb') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return
    
    key_byte = ord(key)  # Get ASCII value of the key
    encrypted_data = bytes([byte ^ key_byte for byte in data])  # XOR each byte with the key

    # Print the encrypted data as hex
    print("".join(f"{byte:02x}" for byte in encrypted_data))

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <key> <filename>")
        return
    
    key = sys.argv[1]
    filename = sys.argv[2]

    # Ensure the key is a single character
    if len(key) != 1:
        print("Key must be a single character.")
        return
    
    xor_encrypt(key, filename)

if __name__ == "__main__":
    main()

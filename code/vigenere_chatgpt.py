import sys

def vigenere_cipher(key, text):
    key = key.upper()
    key_length = len(key)
    key_indices = [ord(char) - ord('A') + 1 for char in key]  # Convert key to numerical indices
    result = []

    for i in range(len(text)):
        if text[i].isalpha():
            is_upper = text[i].isupper()
            text_base = ord('A') if is_upper else ord('a')
            text_index = ord(text[i]) - text_base
            key_index = key_indices[i % key_length]

            new_index = (text_index + key_index) % 26
            new_char = chr(text_base + new_index)
            result.append(new_char)
        else:
            result.append(text[i])

    return ''.join(result)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vigenere.py key filename.txt")
        sys.exit(1)

    key = sys.argv[1]
    filename = sys.argv[2]

    with open(filename, "r") as file:
        text = file.read()

    encrypted_text = vigenere_cipher(key, text)

    print("Encrypted Text:")
    print(encrypted_text)

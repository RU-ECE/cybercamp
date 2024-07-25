import sys

class EnigmaMachine:
    def __init__(self, rotor_config, start_positions):
        self.rotors = rotor_config
        self.counter1 = start_positions[0] % 26
        self.counter2 = start_positions[1] % 26
        self.counter3 = start_positions[2] % 26

    def rotate_rotors(self):
        self.counter1 = (self.counter1 + 1) % 26
        if self.counter1 == 0:
            self.counter2 = (self.counter2 + 1) % 26
            if self.counter2 == 0:
                self.counter3 = (self.counter3 + 1) % 26

    def encrypt_char(self, char):
        idx1 = (ord(char) - ord('A') + self.counter1) % 26
        idx2 = (ord(self.rotors[0][idx1]) - ord('A') + self.counter2) % 26
        idx3 = (ord(self.rotors[1][idx2]) - ord('A') + self.counter3) % 26
        idx4 = (ord(self.rotors[2][idx3]) - ord('A')) % 26  # Additional rotor 4
        idx5 = (ord(self.rotors[3][idx4]) - ord('A')) % 26  # Additional rotor 5
        encrypted_char = self.rotors[4][idx5]
        self.rotate_rotors()
        return encrypted_char

    def decrypt_char(self, char):
        idx5 = self.rotors[4].index(char)
        idx4 = (idx5 + ord(self.rotors[3][self.counter3]) - ord('A')) % 26
        idx3 = (idx4 + ord(self.rotors[2][self.counter2]) - ord('A')) % 26
        idx2 = (idx3 + ord(self.rotors[1][self.counter1]) - ord('A')) % 26
        decrypted_char = chr((idx2 - self.counter1 + 26) % 26 + ord('A'))
        self.rotate_rotors()
        return decrypted_char

    def encrypt_message(self, message):
        encrypted_message = ''
        for char in message.upper():
            if char.isalpha():
                encrypted_message += self.encrypt_char(char)
            else:
                encrypted_message += char  # keep non-alphabetic characters unchanged
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ''
        for char in encrypted_message.upper():
            if char.isalpha():
                decrypted_message += self.decrypt_char(char)
            else:
                decrypted_message += char  # keep non-alphabetic characters unchanged
        return decrypted_message

# Predefined rotor configurations as an array
rotor_configurations = [
    list('EKMFLGDQVZNTOWYHXUSPAIBRCJ'),  # Rotor 1
    list('AJDKSIRUXBLHWTMCQGZNPYFVOE'),  # Rotor 2
    list('BDFHJLCPRTXVZNYEIWGAKMUSQO'),  # Rotor 3
    list('ESOVPZJAYQUIRHXLNFTGKDCMWB'),  # Rotor 4
    list('VZBRGITYUPSDNHLXAWMJQOFECK')   # Rotor 5
]

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python SimpleEnigmaLike2.py <rotor1index> <rotor2index> <rotor3index> <start_positions> <filename>")
        sys.exit(1)
    
    rotor1index = int(sys.argv[1])
    rotor2index = int(sys.argv[2])
    rotor3index = int(sys.argv[3])
    start_positions = sys.argv[4].upper()
    filename = sys.argv[5]
    
    try:
        with open(filename, 'r') as file:
            plaintext = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    
    if not (0 <= rotor1index < len(rotor_configurations) and
            0 <= rotor2index < len(rotor_configurations) and
            0 <= rotor3index < len(rotor_configurations) and
            len(start_positions) == 3 and
            all(char.isalpha() for char in start_positions)):
        print("Error: Invalid input.")
        sys.exit(1)
    
    enigma = EnigmaMachine([
        rotor_configurations[rotor1index],
        rotor_configurations[rotor2index],
        rotor_configurations[rotor3index],
        rotor_configurations[3],  # Rotor 4
        rotor_configurations[4]   # Rotor 5
    ], start_positions)
    
    encrypted_text = enigma.encrypt_message(plaintext)
    decrypted_text = enigma.decrypt_message(encrypted_text)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted_text}")
    print(f"Decrypted: {decrypted_text}")

import sys

class EnigmaMachine:
    def __init__(self, initial_positions):
        self.rotor1 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.rotor2 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.rotor3 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.counter1 = initial_positions[0] % 26
        self.counter2 = initial_positions[1] % 26
        self.counter3 = initial_positions[2] % 26

    def rotate_rotors(self):
        self.counter1 = (self.counter1 + 1) % 26
        if self.counter1 == 0:
            self.counter2 = (self.counter2 + 1) % 26
            if self.counter2 == 0:
                self.counter3 = (self.counter3 + 1) % 26

    def encrypt_char(self, char):
        idx1 = (ord(char) - ord('A') + self.counter1) % 26
        idx2 = (ord(self.rotor1[idx1]) - ord('A') + self.counter2) % 26
        idx3 = (ord(self.rotor2[idx2]) - ord('A') + self.counter3) % 26
        encrypted_char = self.rotor3[idx3]
        self.rotate_rotors()
        return encrypted_char

    def encrypt_message(self, message):
        encrypted_message = ''
        for char in message.upper():
            if char.isalpha():
                encrypted_message += self.encrypt_char(char)
            else:
                encrypted_message += char  # keep non-alphabetic characters unchanged
        return encrypted_message


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python enigma.py <initial_positions> <filename>")
        sys.exit(1)
    
    initial_positions = [int(pos) for pos in sys.argv[1].split(',')]
    filename = sys.argv[2]
    
    try:
        with open(filename, 'r') as file:
            plaintext = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    
    enigma = EnigmaMachine(initial_positions)
    encrypted_text = enigma.encrypt_message(plaintext)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted_text}")

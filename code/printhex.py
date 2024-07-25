import sys

def string_to_hex(s):
    return " ".join(f"{ord(char):02x}" for char in s)  # Convert each character to its hex representation

def main():
    if len(sys.argv) != 2:
        print("Usage: python string_to_hex.py <string>")
        return
    
    input_string = sys.argv[1]
    hex_output = string_to_hex(input_string)

    print(hex_output)

if __name__ == "__main__":
    main()

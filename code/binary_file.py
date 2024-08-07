import struct

def create_binary_file(filename):
    with open(filename, 'wb') as f:
        # Write an 8-bit unsigned integer (3)
        f.write(struct.pack('B', 3))

        # Write a 32-bit unsigned integer (1024)
        f.write(struct.pack('I', 1024))

        # Write a 64-bit integer (65537)
        f.write(struct.pack('Q', 65537))

        # Write the ASCII string "hello"
        f.write(b'hello')

        # Write the UTF-8 string with the Chinese character for "big" (大)
        f.write('大'.encode('utf-8'))

if __name__ == "__main__":
    create_binary_file('output.bin')

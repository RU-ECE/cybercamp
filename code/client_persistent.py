import socket
import sys

def echo_client(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f'Connected to server {host}:{port}')

        # Collect all input lines
        print("Enter your messages (end with EOF, Ctrl+D):")
        messages = []
        while True:
            try:
                line = input()
                messages.append(line)
            except EOFError:
                break

        # Join all lines into a single message with newline characters
        message = '\n'.join(messages)

        # Send the message
        client_socket.send(message.encode('utf-8'))

        # Receive the echoed message
        data = client_socket.recv(1024).decode('utf-8')
        print(f'Received echo: {data}')

    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Close the connection
        client_socket.close()

if __name__ == '__main__':
    # Get host and port from command line arguments or default to 127.0.0.1:8080
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9009
    echo_client(host, port)
